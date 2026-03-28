# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [1.1.0]

### Added

- SSRF protection: `source` URLs that resolve to private, loopback, link-local, or reserved IPs are now blocked
- `SECURITY.md` with vulnerability reporting guidelines
- Full traceback printed on unhandled exceptions for easier debugging
- `STEP_SUMMARY_LIMIT` (1 MB) constant to respect GitHub's step summary size cap; tree is progressively truncated when the summary would exceed the limit

### Changed

- Extracted `read_inputs()`, `validate_paths()`, `validate_url()`, `run_ingestion()`, `write_output_files()`, and `write_step_summary()` from monolithic `main()`
- Large `content` string is now freed before step-summary work to reduce peak memory

## [1.0.1]

### Added

- README usage examples section with links to ready-to-use workflows in `gitingest-action-examples`
- Private repository usage snippet showing `token` + `secrets.PRIVATE_REPO_TOKEN`

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

[1.1.0]: https://github.com/ysskrishna/gitingest-action/compare/v1.0.1...v1.1.0
[1.0.1]: https://github.com/ysskrishna/gitingest-action/compare/v1.0.0...v1.0.1
[1.0.0]: https://github.com/ysskrishna/gitingest-action/releases/tag/v1.0.0
