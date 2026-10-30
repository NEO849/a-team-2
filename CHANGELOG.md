# Changelog

All notable changes to this project are documented here. The format is based on
[Keep a Changelog](https://keepachangelog.com/en/1.1.0/), and this project aims to
follow [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [0.1.0] - 2026-10-30

First tagged release: the curated public slice of the system, with the repository
made to say exactly what it is.

### Added
- 38 skills, 16 subagents, and 5 commands, installable as a Claude Code plugin
  (`a-team-2@neo849`).
- README "Meet the crew": a 16-agent table, each with a one-line description
  sourced from that agent's own definition and a link to it.
- Collapsible skill families, a Mermaid studio-flow diagram, status badges, and a
  dark/light hero image.
- `SECURITY.md`, `CONTRIBUTING.md`, and this changelog.
- `.github/badges/crew.json` for the crew-size badge; a plugin icon.

### Changed
- README corrected to match the repository exactly: removed an unavailable skill
  claim, listed `slop-check` / `skill-doctor` as commands (not skills), and
  dropped references to agents that do not exist in the pack.
- Pinned the `trufflehog` CI action from a moving tag to a commit SHA (v3.99.7).
- Documented the bundled icon-set licences (Tabler and Phosphor, both MIT) in
  `THIRD_PARTY_LICENSES/`.

### Removed
- The `chunk-filled` icon set (no discoverable licence, author, or upstream), and
  all references to it in the icon resolver and docs.

[0.1.0]: https://github.com/NEO849/a-team-2/releases/tag/v0.1.0
