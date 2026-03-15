# Gitingest Action

[![CI](https://github.com/ysskrishna/gitingest-action/actions/workflows/test.yml/badge.svg)](https://github.com/ysskrishna/gitingest-action/actions/workflows/test.yml)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

A GitHub Action to analyze Git repositories and generate text digests optimized for LLMs. Powered by [gitingest](https://github.com/coderamp-labs/gitingest).

## Quick Start

```yaml
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

## Output Files

The action writes three files to the `output-dir` directory:

| File | Contents | Typical Use Case |
|------|----------|------------------|
| `summary.txt` | Stats: file count, token estimate, repo info | Quick overview, CI checks |
| `tree.txt` | Directory tree structure | Understanding repo layout |
| `content.txt` | Concatenated file contents | Feeding to LLMs, code analysis |

## Accessing Results

### 1. Output Files

Read the files directly in subsequent steps:

```yaml
- run: cat gitingest-output/summary.txt
- run: cat gitingest-output/tree.txt
- run: python process.py gitingest-output/content.txt
```

### 2. Job Summary

A markdown summary is automatically added to the workflow run's Summary page with the repository overview and directory tree.

## Usage Examples

### Analyze current repository

```yaml
- uses: actions/checkout@v4

- uses: ysskrishna/gitingest-action@v1
  with:
    output-dir: 'gitingest-output'

- run: cat gitingest-output/summary.txt
```

### Analyze a remote repository

```yaml
- uses: ysskrishna/gitingest-action@v1
  with:
    source: 'https://github.com/coderamp-labs/gitingest'
    branch: 'main'
```

### Filter files with patterns

```yaml
- uses: ysskrishna/gitingest-action@v1
  with:
    include-patterns: |
      *.py
      *.md
    exclude-patterns: |
      tests/*
      docs/*
```

### Analyze a private repository

```yaml
- uses: ysskrishna/gitingest-action@v1
  with:
    source: 'https://github.com/owner/private-repo'
    token: ${{ secrets.GITHUB_TOKEN }}
```

### Save digest as artifact

```yaml
- uses: ysskrishna/gitingest-action@v1
  with:
    output-dir: 'digest'

- uses: actions/upload-artifact@v4
  with:
    name: repo-digest
    path: digest/
```

### Upload only summary and tree (skip large content file)

```yaml
- uses: ysskrishna/gitingest-action@v1

- uses: actions/upload-artifact@v4
  with:
    name: repo-overview
    path: |
      gitingest-output/summary.txt
      gitingest-output/tree.txt
```

## Large Repositories

The `gitingest` library enforces these limits to prevent memory issues:

| Limit | Value | Effect |
|-------|-------|--------|
| **MAX_FILE_SIZE** | 10 MB/file | Individual files > 10MB are skipped |
| **MAX_TOTAL_SIZE_BYTES** | 500 MB cumulative | Files are skipped once 500MB total is reached |
| **MAX_FILES** | 10,000 | Files are skipped once 10,000 files are processed |
| **MAX_DIRECTORY_DEPTH** | 20 levels | Directories deeper than 20 levels are skipped |

When these limits are hit, files are silently skipped and warnings are logged. The digest will be partial but still usable.

### Recommendations for Large Repos

- **Use pattern filtering**: Scope the analysis to relevant files using `include-patterns` and `exclude-patterns`
- **Analyze specific directories**: Pass a subdirectory path as `source`
- **Lower the file size limit**: Use `max-file-size` to skip large files earlier
- **The digest file is the primary output**: Don't rely on inline outputs for large repos

Example for a monorepo:

```yaml
- uses: ysskrishna/gitingest-action@v1
  with:
    source: './packages/my-package'
    include-patterns: |
      *.ts
      *.tsx
      *.json
    exclude-patterns: |
      node_modules/*
      dist/*
      *.test.ts
```

## Error Handling

The action fails with a clear error when:

- **Repository not found** — invalid URL or insufficient permissions
- **Git clone failed** — network issues or invalid branch/tag
- **File system error** — output directory not writable

Errors are surfaced in the GitHub Actions UI via `::error::` workflow commands.

## License

MIT © [Y. Siva Sai Krishna](https://github.com/ysskrishna) - see [LICENSE](LICENSE) for details.

## Credits

Built on [gitingest](https://github.com/coderamp-labs/gitingest) by Romain Courtois & Filip Christiansen.

---

<p align="left">
  <a href="https://github.com/ysskrishna">Author's GitHub</a> •
  <a href="https://linkedin.com/in/ysskrishna">Author's LinkedIn</a> •
  <a href="https://github.com/coderamp-labs/gitingest">gitingest Library</a> •
  <a href="https://github.com/ysskrishna/gitingest-action/issues">Report Issues</a> •
  <a href="https://github.com/ysskrishna/gitingest-action/releases">Releases</a>
</p>
