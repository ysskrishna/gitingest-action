# Gitingest Action

[![CI](https://github.com/ysskrishna/gitingest-action/actions/workflows/test.yml/badge.svg)](https://github.com/ysskrishna/gitingest-action/actions/workflows/test.yml)
[![GitHub Marketplace](https://img.shields.io/badge/Marketplace-Gitingest-blue?logo=github)](https://github.com/marketplace/actions/gitingest)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

A GitHub Action to analyze Git repositories and generate text digests optimized for LLMs. Powered by [gitingest](https://github.com/coderamp-labs/gitingest).

## Quick Start

```yaml
name: Analyze Github Repository
on: workflow_dispatch

jobs:
  digest:
    runs-on: ubuntu-latest
    steps:
      - name: Analyze Github Repository
        uses: ysskrishna/gitingest-action@v1
        id: digest
        with:
          source: 'https://github.com/ysskrishna/pypi-package-stats'
          branch: 'main'

      - name: Display Github Repository summary
        run: |
          echo "📊 Github Repository Digest Summary:"
          echo "================================"
          cat ${{ steps.digest.outputs.summary-file }}
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

The action produces three files in the `output-dir` directory, and a job summary on the workflow run's Summary page.

| Output | File | Contents | Typical Use Case |
|--------|------|----------|------------------|
| `summary-file` | `summary.txt` | Stats: file count, token estimate, repo info | Quick overview, CI checks |
| `tree-file` | `tree.txt` | Directory tree structure | Understanding repo layout |
| `content-file` | `content.txt` | Concatenated file contents | Feeding to LLMs, code analysis |

Access file paths via `steps.<id>.outputs.summary-file` (etc.), or read them directly from `output-dir`.

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

## Usage Examples

For complete, ready-to-use workflow files, see the [examples repository](https://github.com/ysskrishna/gitingest-action-examples).

| Example | Description |
|---------|-------------|
| [Analyze Remote Repository](https://github.com/ysskrishna/gitingest-action-examples/blob/main/.github/workflows/analyze-remote-repo.yml) | Analyze a repository by URL using `source` and optional `branch` |
| [Filter Files with Patterns](https://github.com/ysskrishna/gitingest-action-examples/blob/main/.github/workflows/filter-files-with-patterns.yml) | Include/exclude files with `include-patterns` and `exclude-patterns` |
| [Analyze Specific Tag](https://github.com/ysskrishna/gitingest-action-examples/blob/main/.github/workflows/analyze-specific-tag.yml) | Analyze a tagged release with `tag` |
| [Monorepo Scoped Analysis](https://github.com/ysskrishna/gitingest-action-examples/blob/main/.github/workflows/monorepo-scoped-analysis.yml) | Analyze only a subdirectory in a monorepo |
| [Save Digest as Artifact](https://github.com/ysskrishna/gitingest-action-examples/blob/main/.github/workflows/save-digest-as-artifact.yml) | Upload generated digest files as workflow artifacts |
| [Selective Artifact Upload](https://github.com/ysskrishna/gitingest-action-examples/blob/main/.github/workflows/selective-artifact-upload.yml) | Upload only selected output files (for example `summary.txt`, `tree.txt`) |
| [Scheduled Weekly Digest](https://github.com/ysskrishna/gitingest-action-examples/blob/main/.github/workflows/scheduled-weekly-digest.yml) | Run digest generation on a weekly cron schedule |

### Example: Analyze a Private Repository

```yaml
- uses: ysskrishna/gitingest-action@v1
  with:
    source: 'https://github.com/owner/private-repo'
    token: ${{ secrets.PRIVATE_REPO_TOKEN }}
    output-dir: 'gitingest-output'
```

Store the token as a repository or organization secret, and grant least-privilege read access to the target repository.

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
  <a href="https://github.com/ysskrishna/gitingest-action-examples">Examples</a> •
  <a href="https://github.com/ysskrishna/gitingest-action/issues">Report Issues</a> •
  <a href="https://github.com/ysskrishna/gitingest-action/releases">Releases</a>
</p>
