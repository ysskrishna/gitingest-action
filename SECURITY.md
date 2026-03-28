# Security Policy

## Supported Versions

| Version | Supported |
|---------|-----------|
| v1.x    | Yes       |

## Reporting Vulnerabilities

If you discover a security vulnerability in this project, please report it responsibly:

1. **Do not** open a public issue.
2. Email the maintainer at the address listed in the repository profile, or use [GitHub's private vulnerability reporting](https://docs.github.com/en/code-security/security-advisories/guidance-on-reporting-and-writing-information-about-vulnerabilities/privately-reporting-a-security-vulnerability) on this repository.
3. Include steps to reproduce and any relevant context (workflow snippet, logs with secrets redacted).

You should receive an acknowledgement within 72 hours. Fixes for confirmed issues will be released as a patch version.

## Security Design Decisions

### Token handling
- Tokens supplied via the `token` input are masked immediately with `::add-mask::` so GitHub Actions redacts them from all log output, including exception tracebacks.

### Error messages in public logs
- Exception messages are passed through `sanitize_url()` to strip any embedded URL credentials before printing.
- Beyond URL credentials, error messages may contain runner filesystem paths (e.g. `/home/runner/work/...`). These paths are predictable on GitHub-hosted runners and do not constitute sensitive information.
- For public repositories, the repository contents themselves are already public, so their appearance in error output does not create new exposure.

### SSRF protection
- Remote `source` URLs are resolved via DNS before being passed to `gitingest`. If any resolved address falls within private (RFC 1918), loopback (`127.0.0.0/8`), link-local (`169.254.0.0/16`), or IANA-reserved ranges, the action exits with an error.
- This prevents a misconfigured or malicious workflow from using the action to reach internal services (e.g. cloud instance metadata at `169.254.169.254`) on self-hosted runners.
- If DNS resolution fails, the action defers to `gitingest` to surface the connection error rather than silently proceeding.

### Path traversal
- Local source paths and the output directory are validated to stay within `GITHUB_WORKSPACE` before any file operations occur.
