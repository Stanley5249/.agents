---
name: project-setup
description: Scaffold or migrate a repository, or change its tooling, including justfile, oxfmt, pixi, tombi, Zed settings, CI, .gitattributes, licenses, README, agent instruction files, and release notes. Use when creating a project, adopting these conventions, editing any of those files, or formatting files with oxfmt.
---

# Project setup

Read the reference for each tool you touch, and the `rust`, `python`, or `javascript` skill for each language in the project.

| Topic                                         | Reference                |
| --------------------------------------------- | ------------------------ |
| Any justfile                                  | `references/justfile.md` |
| oxfmt, or formatting JS, JSON, YAML, Markdown | `references/oxfmt.md`    |
| pixi, for native or GPU dependencies          | `references/pixi.md`     |
| Zed project settings                          | `references/zed.md`      |
| README and agent instruction files            | `references/docs.md`     |
| Changelog and release notes                   | `references/release.md`  |

## Repository metadata

- Add `.gitattributes` with LF normalization at the repository root:

  ```gitattributes
  * text=auto eol=lf
  ```

- Configure generated lockfiles with `merge=binary`, `linguist-generated=true`, and `-diff`. This prevents corrupted lockfiles from automatic 3-way merges, flags them as generated on GitHub, and collapses noisy lockfile diffs.
- Inspect upstream templates and dependency licenses first to confirm compatibility. Default to dual `LICENSE-APACHE` and `LICENSE-MIT` for Rust crates, and `LICENSE` with MIT for other projects.
- Format TOML files with `tombi` (`tombi.toml`) regardless of the package manager. It covers `Cargo.toml`, `pyproject.toml`, `pixi.toml`, and its own configuration file.
- Keep the toolchain for a secondary language scoped to the subdirectory that needs it unless the whole workspace depends on it.

## CI

- Call the tools directly instead of through the justfile, and run the same checks as the local gate. CI then stays independent of the justfile, so a broken recipe and a broken check fail separately.
- Run independent checks as parallel jobs, and keep each job's output visible so a failure shows its cause.

## Scaffolding

- Start from an existing project with a similar structure, and introduce a new pattern only for a stated reason.
- Set up the repository metadata before history accumulates.
- Make the first commit with a Conventional Commit subject, such as `chore: first commit`.

## Migration

- Audit the repository against these conventions and list each gap with its planned change.
- Show the list and ask which changes to apply. The user decides which existing conventions to replace.
- Work on a task branch, such as `chore/migrate-conventions`.
- Move the instructions in a project `CLAUDE.md` into `AGENTS.md`, merging them with what is already there, then delete `CLAUDE.md`, including one that only imports `@AGENTS.md`. Claude Code reads `AGENTS.md` when no `CLAUDE.md` exists, so one file serves every agent.
- Commit each accepted change separately, such as a formatter switch, the reformat it causes, and a new `.gitattributes`.
- After changing line-ending rules in `.gitattributes`, run `git add --renormalize .` and commit the result on its own.
