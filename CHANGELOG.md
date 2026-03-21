# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [1.0.0]

### Added

- Initial release of Gitingest GitHub Action
- Composite action using `gitingest` Python library (v0.3.1)
- Inputs:
  - `source` (optional, default: current workspace) — repository URL or local path
  - `max-file-size` (optional, default: 10MB) — maximum file size in bytes
  - `include-patterns` (optional) — newline-separated glob patterns to include
  - `exclude-patterns` (optional) — newline-separated glob patterns to exclude
  - `branch` (optional) — branch to analyze
  - `tag` (optional) — tag to analyze
  - `include-gitignored` (optional, default: false) — include gitignored files
  - `include-submodules` (optional, default: false) — include submodules
  - `token` (optional) — GitHub PAT for private repositories
  - `output-dir` (optional, default: gitingest-output) — output directory path
- Output files written to configurable directory:
  - `summary.txt` — text summary with file count and token estimate
  - `tree.txt` — directory tree structure
  - `content.txt` — concatenated file contents
- GitHub Job Summary with repository summary and collapsible directory tree
- Error handling with `::error::` workflow commands
- CI workflow with 4 test jobs (default source, remote repo, patterns, invalid source)

[1.0.0]: https://github.com/ysskrishna/gitingest-action/releases/tag/v1.0.0
