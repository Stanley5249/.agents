---
name: commit-message
description: Conventional Commit guidance useful when preparing commits or configuring message enforcement.
---

## Convention

- `type(scope): imperative summary` — Conventional Commits. Common types: `feat`, `fix`, `docs`, `style`, `refactor`, `perf`, `test`, `build`, `ci`, `chore`, `revert`. Add `!` before the colon for a breaking change.
- **Scope = an existing top-level directory name — never invent one.** Omit the scope for a repo-wide change.
- Body is the exception, not the rule — most commits here are a single-line subject. When one is needed: at most 2 sections or 5 bullet lines.
- Amend for an immediate fix to the last commit rather than stacking a `fix typo` commit. Prefer coherent commits over artificially small ones; batch related, non-conflicting changes, then format and test the batch once. Commit outside `main` by default, ask before merging back.
- Never let a stray token (an accidental `@mention`, a pasted co-author tag) precede the `type:` in the subject — the most common real failure mode, and what `reference/commit-msg-hook.sh` catches.
- **Before every commit, run the project formatter and full CI gate.** If either is unavailable, run the closest equivalent verification. Do not commit with failed checks.
- **Check `git status` before committing.** Review every untracked generated or data path, and ignore it when it is local-only rather than letting it slip into the commit.
- Do not commit files under `.claude/`, `.codex/`, `.pi/`, or similar tool-local directories unless the repository intentionally tracks that integration.
- **This is the machine default, not a hard rule.** A stricter project convention wins — e.g. Angular-style: mandatory body except for `docs` commits, project-specific scopes, 72-column body wrap, `BREAKING CHANGE`/`Fixes`/`NEXT` footers. Check for a `.github/prompts/commit-message.prompt.md` or similar project-local override first.

### Branch naming

- Default branch is `main` (`init.defaultBranch` is set globally on this machine). If a repo somehow still starts on `master`, rename it: `git branch -m main`.
- Code branches: `feat/<topic>`, `fix/<topic>`.
- Branches for a content/instance rather than code (a talk deck, a play session, a generated artifact run) are **date-prefixed**: `<kind>/<date>-<name>`, e.g. `deck/<group>/<date>-<venue>-<topic>`.
- Never use a version suffix — no `-v2`, `-final`, `-wip`. Amend or open a fresh dated branch instead.

## Enforcement when a repository needs it

Repositories here generally carry no commit-message hook. Validate ordinary commits against the convention above without adding one. Configure enforcement when the user asks, when hardening a shared repository, or when the project already uses managed hooks:

1. **Check for an existing hook manager first** — `.pre-commit-config.yaml` (run by either `prek` or `pre-commit`), `.husky/`, `lefthook.yml`. If the repo has one, add a commit-msg stage to it rather than installing a second mechanism alongside it.
2. **Otherwise, prefer `prek` running the `conventional-pre-commit` hook** — see `reference/pre-commit-config.yaml`. `prek` (github.com/j178/prek) is a Rust-native, single-binary, drop-in replacement for `pre-commit` reading the same `.pre-commit-config.yaml`; standardize on it rather than mixing the two across projects, and fall back to plain `pre-commit` only where `prek` isn't available. `conventional-pre-commit` only inspects the commit message text, so it validates the same way in a cargo, uv, bun, or pixi repo without forcing a Node or Python toolchain onto a repo that doesn't otherwise need one — unlike `commitlint` (npm) or `gitlint` (pip).
   - For a pure-cargo repo where a full hook framework feels heavier than needed, `cocogitto` (`cog install-hook commit-msg`, single Rust binary via `cargo binstall`) is lighter and brings semver/changelog tooling for free — but it doesn't compose with an existing `.pre-commit-config.yaml`, so pick one per repo.
3. **Check whether the environment already exposes a skill or tool for wiring up hooks/config**, and use it to install whichever of the above applies rather than hand-editing config files.
4. **If none of the above can be installed** — offline, a repo you don't control, a one-off review — fall back to `reference/commit-msg-hook.sh`, a zero-dependency raw script, or to checking the message yourself before the commit goes through. Last resort, not the default.
