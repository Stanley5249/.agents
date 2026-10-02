# Project setup

Detect the repository shape, then read only the rules needed for the task.

A project can use multiple package-manager rules, such as `cargo` + `bun` for a
desktop app or `cargo` + `uv` for a Rust core with a Python harness.

## Core conventions

- Format TOML files with `tombi` (`tombi.toml`) regardless of the package
  manager. It covers `Cargo.toml`, `pyproject.toml`, `pixi.toml`, and its own
  configuration file.
- Format JS, TS, CSS, HTML, JSON, YAML, and Markdown with oxfmt wherever those
  file types appear. Do not use ESLint here.
- Match an existing project with a similar structure instead of introducing a
  new pattern without reason.
- Write an `AGENTS.md` that encodes these conventions when scaffolding a new
  project.
- Use `user/` for local, Git-ignored runtime data such as databases or
  application state.
- Keep the toolchain for a secondary language scoped to the subdirectory that
  needs it unless the whole workspace depends on it.
- Prefer the smallest setup that provides a clear local verification gate. Add
  release automation, team workflows, or hosted automation only when the project
  needs them.

## First commit

Set up repository-wide metadata before history accumulates:

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
- Do not add `.editorconfig` by default when language formatters already cover
  the repository. Add it when a polyglot or shell-heavy project needs settings
  those formatters do not own.
- Make the first commit with a Conventional Commit subject, such as
  `chore: first commit`.
