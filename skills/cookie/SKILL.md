---
name: cookie
description: Project-setup guidance useful for scaffolding, audits, toolchains, formatting, CI, hooks, and agent conventions.
---

## Scope

Cookie covers project setup and tooling conventions. `bibo` covers communication style and ongoing development preferences. Detect the repository shape, then read only the references needed for the task.

## Reference index

- Justfile command surface and recipe naming conventions: `reference/justfile.md`
- Hooks and local or hosted CI: `reference/hooks-ci.md`
- Repository metadata, README, and agent instructions: `reference/repository.md`
- Rust workspace or crate: `reference/cargo.md`
- Python project: `reference/uv.md`
- JavaScript or TypeScript project, especially Svelte: `reference/bun.md`
- Multi-language or native/GPU-dependency-heavy project: `reference/pixi.md`

A project can combine package-manager references, such as cargo+bun for a desktop app or cargo+uv for a Rust core with a Python harness.

## Core conventions

- Match an existing same-shape project instead of introducing a new pattern without reason.
- Write an `AGENTS.md` encoding these conventions when scaffolding a new project.
- Use `user/` for local, gitignored runtime data such as databases or application state.
- Keep a secondary language toolchain scoped to the subdirectory that needs it unless the whole workspace depends on it.
- Prefer the smallest setup that provides a clear local verification gate. Add release, team, or hosted automation only when the project needs it.
