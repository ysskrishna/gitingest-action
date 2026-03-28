#!/usr/bin/env python3
"""Entrypoint for gitingest GitHub Action."""

import html
import os
import re
import sys
import traceback
from pathlib import Path

STEP_SUMMARY_TEMPLATE = """\
### 📄 Gitingest Digest for `{slug}`

{summary}

<details>
<summary>Directory Tree</summary>

{fence}
{tree}
{fence}

</details>
"""


def get_input(name, required=False, default=None):
    """Read action input from INPUT_* env var."""
    value = os.environ.get(f"INPUT_{name.upper().replace('-', '_')}", "").strip()
    if not value:
        if required:
            print(f"::error::Required input '{name}' is missing or empty.")
            sys.exit(1)
        return default
    return value


def parse_bool(value):
    """Parse a string boolean input."""
    return value.lower() in ("true", "1", "yes") if value else False


def parse_patterns(value):
    """Parse newline-separated patterns into a set."""
    if not value:
        return None
    patterns = {p.strip() for p in value.splitlines() if p.strip()}
    return patterns if patterns else None


def format_size(size_bytes):
    """Format file size in human-readable form."""
    for unit in ['B', 'KB', 'MB', 'GB']:
        if size_bytes < 1024.0:
            return f"{size_bytes:.1f} {unit}"
        size_bytes /= 1024.0
    return f"{size_bytes:.1f} TB"


def sanitize_url(url):
    """Strip embedded credentials from a URL for safe logging."""
    # Matches https://user:token@host/... or https://token@host/...
    return re.sub(r"(https?://)([^@]+)@", r"\1***@", url)


def extract_slug(source):
    """Extract an owner/repo slug from a GitHub URL, or return source as-is."""
    match = re.match(r"https?://[^/]+/([^/]+/[^/]+?)(?:\.git)?/?$", source)
    return match.group(1) if match else source


def safe_code_fence(text):
    """Return a backtick fence long enough that `text` cannot break out of it."""
    longest_run = 0
    for m in re.finditer(r"`+", text):
        longest_run = max(longest_run, len(m.group()))
    return "`" * max(3, longest_run + 1)


def main():
    # Read inputs (use dash-style names matching action.yml input names)
    # Defaults are defined in action.yml — Python side only validates or uses
    # None as a "not provided" sentinel. No duplicate defaults.
    source = get_input("source", default="")
    max_file_size_str = get_input("max-file-size", required=True)
    include_patterns_str = get_input("include-patterns")
    exclude_patterns_str = get_input("exclude-patterns")
    branch = get_input("branch")
    tag = get_input("tag")
    include_gitignored = parse_bool(get_input("include-gitignored"))
    include_submodules = parse_bool(get_input("include-submodules"))
    token = get_input("token")
    output_dir = get_input("output-dir", required=True)

    # Mask token in logs so GitHub Actions redacts it from all output
    if token:
        print(f"::add-mask::{token}")

    # Resolve source
    if not source:
        source = os.environ.get("GITHUB_WORKSPACE", ".")
    print(f"Source: {sanitize_url(source)}")

    # Parse and validate max_file_size
    try:
        max_file_size = int(max_file_size_str)
    except (ValueError, TypeError):
        print(f"::error::Invalid max-file-size value: '{max_file_size_str}'. Must be an integer.")
        sys.exit(1)
    if max_file_size <= 0:
        print(f"::error::max-file-size must be a positive integer, got {max_file_size}.")
        sys.exit(1)

    # Parse patterns
    include_patterns = parse_patterns(include_patterns_str)
    exclude_patterns = parse_patterns(exclude_patterns_str)

    # Validate source — local paths must stay inside the workspace
    workspace = Path(os.environ.get("GITHUB_WORKSPACE", ".")).resolve()
    is_url = source.startswith(("http://", "https://"))
    if not is_url:
        resolved_source = Path(source).resolve()
        if not resolved_source.is_relative_to(workspace):
            print(f"::error::source '{source}' resolves outside the workspace.")
            sys.exit(1)

    # Validate output directory
    resolved_output_dir = (workspace / output_dir).resolve()
    if not resolved_output_dir.is_relative_to(workspace):
        print(f"::error::output-dir '{output_dir}' resolves outside the workspace.")
        sys.exit(1)

    # Import gitingest
    try:
        from gitingest import ingest
    except ImportError:
        print("::error::Failed to import gitingest. Is the package installed?")
        sys.exit(1)

    # Run ingestion
    print(f"Running gitingest on: {sanitize_url(source)}")
    try:
        summary, tree, content = ingest(
            source,
            max_file_size=max_file_size,
            include_patterns=include_patterns,
            exclude_patterns=exclude_patterns,
            branch=branch,
            tag=tag,
            include_gitignored=include_gitignored,
            include_submodules=include_submodules,
            token=token,
            output=None,  # We handle file writing ourselves
        )

        # Create output directory
        resolved_output_dir.mkdir(parents=True, exist_ok=True)

        # Write three separate files
        summary_file = resolved_output_dir / "summary.txt"
        tree_file = resolved_output_dir / "tree.txt"
        content_file = resolved_output_dir / "content.txt"

        summary_file.write_text(summary, encoding="utf-8")
        tree_file.write_text(tree, encoding="utf-8")
        content_file.write_text(content, encoding="utf-8")

        # Print success message with file info
        print(f"\nDigest files written to: {resolved_output_dir}")
        print(f"  summary.txt:  {format_size(summary_file.stat().st_size)}")
        print(f"  tree.txt:     {format_size(tree_file.stat().st_size)}")
        print(f"  content.txt:  {format_size(content_file.stat().st_size)}")

        # Derive a slug for display (owner/repo for URLs, GITHUB_REPOSITORY for local)
        if source == os.environ.get("GITHUB_WORKSPACE", "."):
            slug = os.environ.get("GITHUB_REPOSITORY", "") or source
        else:
            slug = extract_slug(source)

        # GitHub Step Summary (sanitize to prevent markdown/HTML injection)
        # GitHub imposes a 1 MB limit on step summary content.
        STEP_SUMMARY_LIMIT = 1_000_000  # 1 MB
        summary_file_path = os.environ.get("GITHUB_STEP_SUMMARY")
        if summary_file_path:
            safe_summary = html.escape(summary)
            safe_tree = html.escape(tree)

            # Check how much space is already used in the summary file
            existing_size = 0
            try:
                existing_size = os.path.getsize(summary_file_path)
            except OSError:
                pass

            budget = STEP_SUMMARY_LIMIT - existing_size
            fence = safe_code_fence(safe_tree)
            step_content = STEP_SUMMARY_TEMPLATE.format(
                slug=slug,
                summary=safe_summary,
                tree=safe_tree,
                fence=fence,
            )

            # If the content exceeds the remaining budget, truncate the tree
            if len(step_content.encode("utf-8")) > budget:
                truncation_note = "\n\n[Tree truncated — exceeds GitHub step summary size limit]"
                # Rebuild with a shorter tree to fit within budget
                safe_tree_truncated = safe_tree
                while True:
                    fence = safe_code_fence(safe_tree_truncated)
                    step_content = STEP_SUMMARY_TEMPLATE.format(
                        slug=slug,
                        summary=safe_summary,
                        tree=safe_tree_truncated + truncation_note,
                        fence=fence,
                    )
                    if len(step_content.encode("utf-8")) <= budget or not safe_tree_truncated:
                        break
                    # Cut the tree in half each iteration to converge quickly
                    safe_tree_truncated = safe_tree_truncated[: len(safe_tree_truncated) // 2]

            with open(summary_file_path, "a", encoding="utf-8") as f:
                f.write(step_content)

        print(
            f"\nDigest files are available at {output_dir}/ and can be used in"
            " subsequent workflow steps or uploaded as artifacts."
        )

    except ValueError as e:
        print(f"::error::Ingestion error: {sanitize_url(str(e))}")
        sys.exit(1)
    except RuntimeError as e:
        print(f"::error::Git operation failed: {sanitize_url(str(e))}")
        sys.exit(1)
    except OSError as e:
        print(f"::error::File system error: {sanitize_url(str(e))}")
        sys.exit(1)
    except Exception as e:
        print(f"::error::Unhandled error: {sanitize_url(str(e))}")
        traceback.print_exc()
        sys.exit(1)


if __name__ == "__main__":
    main()
