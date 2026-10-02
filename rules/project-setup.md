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
