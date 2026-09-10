# agent instruction files

- `AGENTS.md` is the source of truth. `CLAUDE.md` imports it with the one-line `@AGENTS.md` syntax instead of copying it.
- Prefer symbolic links for shared skills, data directories, and other paths without an import mechanism.
- In a monorepo, keep the root `AGENTS.md` as a thin index directing agents to nested files such as `catalog/AGENTS.md` and `web/AGENTS.md`. Do not duplicate subproject details at the root.
- Split an instruction file only when it becomes hard to scan. Put durable topic files under `.agents/rules/`, one topic per file, and reference them from the root.
- Keep durable plans and shared skills under `.agents/`; name the durable backlog itself `.agents/AGENTS.md` — that filename gets the same automatic read/injection a nested `AGENTS.md` gets, instead of needing an explicit instruction to open it every time. Treat `.claude/` and `.codex/` as tool-specific scratch or session state.
