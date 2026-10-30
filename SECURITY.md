# Security Policy

A-Team 2.0 is a Claude Code plugin: skills, subagents and a few helper scripts.
It ships no server and collects no data. The security surface is therefore (a) the
bundled scripts a user may run, and (b) the guarantee that no private data or
secrets are present in the repository.

## Supported versions

| Version | Supported |
| --- | --- |
| 0.1.x | Yes |
| < 0.1 | No |

Pre-release: names and contents may still change.

## Reporting a vulnerability

Please report security issues **privately**, not in a public issue:

- Use GitHub's **"Report a vulnerability"** button under the repository's
  **Security** tab (Security Advisories). This opens a private channel with the
  maintainer.

Include, where possible: the affected file or skill, a description of the issue,
and the steps to reproduce it. You can expect an initial response within a few
days. Please give a reasonable window to fix the issue before any public
disclosure.

## What counts as a security issue here

- A bundled script that performs an unexpected, unguarded, or destructive action.
- Any secret, credential, private path, or private infrastructure detail that
  slipped into the repository or its history.
- A skill or agent definition that instructs unsafe behaviour (for example,
  running remote code without review).

Prompt content that merely *describes* security testing techniques is the subject
matter of several skills and is not itself a vulnerability.

## How this repository is kept clean

Every change passes an automated no-secrets gate before commit and push
(`gitleaks` + `trufflehog` plus a private denylist), and CI repeats the scan on
every push. See [`.github/workflows/secret-scan.yml`](.github/workflows/secret-scan.yml).
