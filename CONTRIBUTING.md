# Contributing

Thanks for your interest. A-Team 2.0 is the curated public slice of a larger
private system — so a few things work differently from a typical repo.

## What's welcome

- Fixes: broken links, wrong commands, typos, inaccurate claims in docs.
- Small improvements to an existing skill, agent, or command.
- Bug reports with clear, minimal reproduction steps.

## What may be declined

Because this pack is a curated mirror, larger feature proposals or new
skills/agents may be declined even if they are good — they may belong to the
private system, or may not fit the pack's scope. Open an issue to discuss before
investing time in a large change.

## Ground rules

- **No private data.** Never add infrastructure, credentials, internal paths, or
  private references. Every change runs through a no-secrets gate (`gitleaks` +
  `trufflehog`) locally and in CI; the maintainer also runs an additional private
  denylist. A change that trips the gate will not be merged.
- **Keep it self-contained.** No skill may depend on anything outside this
  repository.
- **Validate before you push.** From the repo root:

  ```bash
  claude plugin validate --strict
  ```

  CI additionally runs the secret scan on every push.

## How to propose a change

1. Fork the repository and create a branch.
2. Make the change; keep the diff focused.
3. Run `claude plugin validate --strict` and make sure it passes.
4. Open a pull request describing what changed and why.

By contributing, you agree that your contribution is licensed under the
repository's [MIT License](LICENSE).
