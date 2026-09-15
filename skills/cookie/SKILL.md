---
name: cookie
description: Guidance for project setup, including scaffolding, audits, toolchains, formatting, CI, hooks, and agent conventions.
---

## Scope

Cookie covers project setup and tooling conventions. Detect the repository shape, then read only the references needed for the task.

## Reference index

- Local or hosted CI and hook setup: `reference/hooks-ci.md`
- Repository-wide metadata for a new project (`.gitattributes`, license, `.editorconfig`): `reference/first-commit.md`
- README shape and content: `reference/readme.md`
- `AGENTS.md`/`CLAUDE.md` conventions and the `.agents/` layer: `reference/agent-files.md`
- Rust workspace or crate: `reference/cargo.md`
- Python project: `reference/uv.md`
- JavaScript or TypeScript project, especially Svelte: `reference/bun.md`
- Multi-language projects or projects with heavy native or GPU dependencies: `reference/pixi.md`

A project can use multiple package-manager references, such as `cargo` + `bun` for a desktop app or `cargo` + `uv` for a Rust core with a Python harness.

## Core conventions

- Format TOML files with `tombi` (`tombi.toml`) regardless of the package manager. It covers `Cargo.toml`, `pyproject.toml`, `pixi.toml`, and its own configuration file.
- Format JS, TS, CSS, HTML, JSON, YAML, and Markdown with `bunx prettier` wherever those file types appear. Do not use ESLint here. See `reference/bun.md` for the standard configuration and framework plugins.
- Match an existing project with a similar structure instead of introducing a new pattern without reason.
- Write an `AGENTS.md` that encodes these conventions when scaffolding a new project.
- Use `user/` for local, Git-ignored runtime data such as databases or application state.
- Keep the toolchain for a secondary language scoped to the subdirectory that needs it unless the whole workspace depends on it.
- Prefer the smallest setup that provides a clear local verification gate. Add release automation, team workflows, or hosted automation only when the project needs them.
