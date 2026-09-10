# repository conventions

## First commit

Set up repository-wide metadata before history accumulates:

- Add `.gitattributes` with LF normalization and binary declarations appropriate to the project:
  ```gitattributes
  * text=auto eol=lf

  *.png binary
  *.ico binary
  ```
- Mark generated lockfiles as binary merge targets when useful, and adjust entries for Cargo, bun, uv, or pixi.
- Rust crates use `LICENSE-APACHE` and `LICENSE-MIT`; non-Rust projects normally use one `LICENSE`.
- Do not add `.editorconfig` by default when language formatters already cover the repository. Add it when a polyglot or shell-heavy project needs settings those formatters do not own.
- Configure commit-message enforcement only when the project wants it.

## README

Choose the smallest shape appropriate to the audience.

A personal or work-in-progress project normally has no badges and may omit the README when `AGENTS.md` is enough. When present, use:

- A title and optional one-line description.
- Setup or command instructions through the project's command surface.
- Domain-specific sections only for behavior that is not evident from the code.
- A documentation section linking to focused files under `docs/`.
- A status section while major work remains.

A published library should additionally provide release, documentation, CI, coverage, and license badges; runnable basic usage; comparison or FAQ material; and an explicit license section.

## Agent instruction files

- `AGENTS.md` is the source of truth. `CLAUDE.md` imports it with the one-line `@AGENTS.md` syntax instead of copying it.
- Prefer symbolic links for shared skills, data directories, and other paths without an import mechanism.
- In a monorepo, keep the root `AGENTS.md` as a thin index directing agents to nested files such as `catalog/AGENTS.md` and `web/AGENTS.md`. Do not duplicate subproject details at the root.
- Split an instruction file only when it becomes hard to scan. Put durable topic files under `.agents/rules/`, one topic per file, and reference them from the root.
- Keep durable backlogs, plans, and shared skills under `.agents/`. Treat `.claude/` and `.codex/` as tool-specific scratch or session state.
