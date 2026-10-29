---
name: project-setup
description: Scaffold or migrate a repository, or change its tooling, including justfile, oxfmt, pixi, tombi, Zed settings, CI, .gitattributes, licenses, README, agent instruction files, and release notes. Use when creating a project, adopting these conventions, editing any of those files, or formatting files with oxfmt.
---

# Project setup

Read the reference for each tool you touch, and the `rust`, `python`, or `javascript` skill for each language in the project:

- Any justfile: `references/justfile.md`.
- oxfmt, or formatting JS, JSON, YAML, or Markdown: `references/oxfmt.md`.
- pixi, for native or GPU dependencies: `references/pixi.md`.
- Zed project settings: `references/zed.md`.
- README and agent instruction files: `references/docs.md`.
- Changelog and release notes: `references/release.md`.

## Repository metadata

- Add `* text=auto eol=lf` to a root `.gitattributes` before history accumulates.
- Mark each generated lockfile `merge=binary linguist-generated=true -diff`, so a 3-way merge cannot corrupt it and its diff stays collapsed.
- Check upstream templates and dependency licenses for compatibility. Default to dual `LICENSE-APACHE` and `LICENSE-MIT` for Rust crates, and an MIT `LICENSE` otherwise.
- Format TOML with `tombi`, configured in `tombi.toml`, whatever the package manager.
- Scope a secondary language's toolchain to the subdirectory that needs it.

## CI

Call the tools directly instead of through the justfile, so a broken recipe and a broken check fail separately, and run the same checks as the local gate. Run independent checks as parallel jobs.

## Migration

- Audit the repository against these conventions, show each gap with its planned change, and let the user choose which to apply. Work on a task branch.
- Merge a project `CLAUDE.md` into `AGENTS.md` and delete `CLAUDE.md`, because Claude Code reads `AGENTS.md` when no `CLAUDE.md` exists. Keep a `CLAUDE.md` that only imports `@AGENTS.md` when contributors may run Claude Code versions that cannot read `AGENTS.md` directly.
- Commit each accepted change separately, such as a formatter switch, the reformat it causes, and a new `.gitattributes`.
- After changing line-ending rules, run `git add --renormalize .` and commit the result on its own.
