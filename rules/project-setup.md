# Project setup

Load this file to scaffold a new project or to migrate an existing repository to
these conventions. Detect the repository shape, then read only the rules it
needs from `~/.agents/rules/`:

- `cargo.md`: Rust workspace or crate
- `uv.md`: Python project
- `bun.md`: JavaScript or TypeScript project, especially Svelte
- `pixi.md`: multi-language projects or heavy native or GPU dependencies
- `ci.md`: local or hosted CI setup
- `documents.md`: README and `AGENTS.md`

A project can use multiple package-manager rules, such as `cargo` + `bun` for a
desktop app or `cargo` + `uv` for a Rust core with a Python harness.

## Scaffold a new project

- Start from an existing project with a similar structure, and introduce a new
  pattern only for a stated reason.
- Set up the repository metadata below before history accumulates.
- Write an `AGENTS.md` that encodes these conventions.
- Make the first commit with a Conventional Commit subject, such as
  `chore: first commit`.

## Migrate an existing repository

- Audit the repository against the core conventions, the repository metadata,
  and each rule file it needs. List each gap with its planned change.
- Show the list and ask which changes to apply. The user decides which existing
  conventions to replace.
- Work on a task branch, such as `chore/migrate-conventions`.
- Commit each accepted change separately, such as a formatter switch, the
  reformat it causes, and a new `.gitattributes`.
- After changing line-ending rules in `.gitattributes`, run
  `git add --renormalize .` and commit the result on its own.

## Core conventions

- Format TOML files with `tombi` (`tombi.toml`) regardless of the package
  manager. It covers `Cargo.toml`, `pyproject.toml`, `pixi.toml`, and its own
  configuration file.
- Format JS, TS, CSS, HTML, JSON, YAML, and Markdown with oxfmt wherever those
  file types appear. Do not use ESLint here.
- Use `user/` for local, Git-ignored runtime data such as databases or
  application state.
- Keep the toolchain for a secondary language scoped to the subdirectory that
  needs it unless the whole workspace depends on it.
- Prefer the smallest setup that provides a clear local verification gate. Add
  release automation, team workflows, or hosted automation only when the project
  needs them.

## Repository metadata

- Add `.gitattributes` with LF normalization, binary declarations, and generated
  lockfile handling appropriate to the project:

  ```gitattributes
  * text=auto eol=lf

  *.png binary
  *.ico binary

  # Lockfiles: avoid git merge conflict markers, mark generated, suppress noisy diffs
  bun.lock merge=binary linguist-language=JSON linguist-generated=true -diff
  Cargo.lock merge=binary linguist-language=TOML linguist-generated=true -diff
  uv.lock merge=binary linguist-language=TOML linguist-generated=true -diff
  pixi.lock merge=binary linguist-language=YAML linguist-generated=true -diff
  ```

- Always configure package lockfiles with
  `merge=binary linguist-language=<LANG> linguist-generated=true -diff`. This
  prevents corrupted lockfiles from automatic 3-way git merges, flags them as
  generated on GitHub, and collapses noisy lockfile diffs.
- Rust crates use `LICENSE-APACHE` and `LICENSE-MIT`; non-Rust projects normally
  use one `LICENSE`.
- Let language formatters own whitespace settings. Add `.editorconfig` when a
  polyglot or shell-heavy project needs settings beyond what those formatters
  cover.
