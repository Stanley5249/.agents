# justfile conventions

## When to add one

Use a justfile when a project needs a composed command surface for recurring development and verification commands. Small script- or library-shaped projects can use their package manager directly until that surface becomes useful.

When a justfile exists, document and invoke its recipes instead of duplicating raw commands elsewhere. Use the recurring names that apply: `install`, `dev`, `format`, `check`, `lint`, `test`, `build`, and `ci`.

- `check` type-checks or compile-checks (`tsc --noEmit`, `svelte-check`, `cargo check`/`clippy`) without necessarily enforcing style.
- `lint` checks formatting and style across the whole repository by default. If the project also defines `lint-all`, `lint` switches meaning to the diff-only fast variant and `lint-all` becomes the full sweep used by `ci` — split them out only once the full sweep is slow enough to matter; most projects here just run one `lint` over everything.
- `ci` composes whichever of `lint`(`-all`)/`check`/`test`/`build` apply, e.g. `ci: lint check test build`.
- Add recipes for non-code verification that normal tests cannot cover, such as rendering an LLM prompt or regenerating diagrams.

## Baseline

Put the Windows shell configuration first:

```just
[windows]
set shell := ["pwsh", "-NoLogo", "-NoProfile", "-Command"]

set default-list
```

Keep recipes to one command when practical. Comment why a non-obvious flag or multi-line shell block is needed, not what an obvious command does. When a recipe needs substantial control flow, move it into a dedicated script or task runner instead of inlining it in the justfile.
