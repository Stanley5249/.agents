# justfile conventions

## When to add one

Use a justfile when a project needs a composed command surface for recurring development and verification commands. Small script- or library-shaped projects can use their package manager directly until that surface becomes useful.

When a justfile exists, document and invoke its recipes instead of duplicating raw commands elsewhere. Use the recurring names that apply: `install`, `dev`, `format`, `lint`, `lint-all`, `check`, `test`, `build`, and `ci`.

- `lint` checks changed and untracked files for fast iteration.
- `lint-all` checks the complete repository.
- `ci` composes the full merge gate, such as `ci: lint-all check test build`.
- Add recipes for non-code verification that normal tests cannot cover, such as rendering an LLM prompt or regenerating diagrams.

## Baseline

Put the Windows shell configuration first:

```just
[windows]
set shell := ["pwsh", "-NoLogo", "-NoProfile", "-Command"]

set default-list
```

Keep recipes to one command when practical. Comment why a non-obvious flag or multi-line shell block is needed, not what an obvious command does. When a recipe needs substantial control flow, move it into a dedicated script or task runner instead of inlining it in the justfile.

For which of these names apply to a given package manager, and which are tool-specific rather than universal, read `reference/bun.md` or `reference/cargo.md`.
