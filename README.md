# Gitingest Action

[![CI](https://github.com/ysskrishna/gitingest-action/actions/workflows/test.yml/badge.svg)](https://github.com/ysskrishna/gitingest-action/actions/workflows/test.yml)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

A GitHub Action to analyze Git repositories and generate text digests optimized for LLMs. Powered by [gitingest](https://github.com/coderamp-labs/gitingest).

## Quick Start

```yaml
- uses: actions/checkout@v4

- uses: ysskrishna/gitingest-action@v1
  with:
    output-dir: 'gitingest-output'

- run: cat gitingest-output/summary.txt
```

## Inputs

| Input | Description | Required | Default |
|-------|-------------|----------|---------|
| `source` | Repository URL or local path to analyze | No | Current workspace |
| `max-file-size` | Maximum file size in bytes | No | `10485760` (10MB) |
| `include-patterns` | Newline-separated glob patterns to include | No | — |
| `exclude-patterns` | Newline-separated glob patterns to exclude | No | — |
| `branch` | Branch to analyze | No | Default branch |
| `tag` | Tag to analyze | No | — |
| `include-gitignored` | Include .gitignore'd files | No | `false` |
| `include-submodules` | Include Git submodules | No | `false` |
| `token` | GitHub token for private repos | No | — |
| `output-dir` | Output directory path | No | `gitingest-output` |

## Outputs

| Output | Description |
|--------|-------------|
| `summary-file` | Path to the generated `summary.txt` file |
| `tree-file` | Path to the generated `tree.txt` file |
| `content-file` | Path to the generated `content.txt` file |

## Output Files

The action writes three files to the `output-dir` directory:

| File | Contents | Typical Use Case |
|------|----------|------------------|
| `summary.txt` | Stats: file count, token estimate, repo info | Quick overview, CI checks |
| `tree.txt` | Directory tree structure | Understanding repo layout |
| `content.txt` | Concatenated file contents | Feeding to LLMs, code analysis |

## Accessing Results

Results can be accessed in three ways:

1. **Action outputs** — reference file paths via `steps.<id>.outputs.summary-file`, `tree-file`, `content-file`
2. **Output files** — read files directly from the `output-dir` directory
3. **Job summary** — a markdown summary is automatically added to the workflow run's Summary page

## Large Repositories

The `gitingest` library enforces these limits to prevent memory issues:

| Limit | Value | Effect |
|-------|-------|--------|
| **MAX_FILE_SIZE** | 10 MB/file | Individual files > 10MB are skipped |
| **MAX_TOTAL_SIZE_BYTES** | 500 MB cumulative | Files are skipped once 500MB total is reached |
| **MAX_FILES** | 10,000 | Files are skipped once 10,000 files are processed |
| **MAX_DIRECTORY_DEPTH** | 20 levels | Directories deeper than 20 levels are skipped |

When these limits are hit, files are silently skipped and warnings are logged. The digest will be partial but still usable.

Use `include-patterns`, `exclude-patterns`, or a subdirectory `source` to scope analysis for large repos.

## Error Handling

The action fails with a clear error when:

- **Repository not found** — invalid URL or insufficient permissions
- **Git clone failed** — network issues or invalid branch/tag
- **File system error** — output directory not writable
- **Invalid input** — `max-file-size` is not a positive integer, or `output-dir` is empty
- **Source outside workspace** — local source path resolves outside `GITHUB_WORKSPACE`

Errors are surfaced in the GitHub Actions UI via `::error::` workflow commands.

## Credits

Built on [gitingest](https://github.com/coderamp-labs/gitingest) by [Romain Courtois](https://github.com/cyclotruc) & [Filip Christiansen](https://github.com/filipchristiansen).

## License

MIT © [Y. Siva Sai Krishna](https://github.com/ysskrishna) - see [LICENSE](LICENSE) for details.

---

<p align="left">
  <a href="https://github.com/ysskrishna">Author's GitHub</a> •
  <a href="https://linkedin.com/in/ysskrishna">Author's LinkedIn</a> •
  <a href="https://github.com/coderamp-labs/gitingest">gitingest Library</a> •
  <a href="https://github.com/ysskrishna/gitingest-action/issues">Report Issues</a> •
  <a href="https://github.com/ysskrishna/gitingest-action/releases">Releases</a>
</p>
