# justfile conventions

## When to add one

Use a justfile when a project needs a composed command surface for recurring development and verification commands. Small script- or library-shaped projects can use their package manager directly until that surface becomes useful.

## Recipe surface

When a justfile exists, document and invoke its recipes instead of duplicating raw commands elsewhere. Start with the smallest useful set of recipes for the project's current workflow, then add more as the workflow grows. Use consistent names when their roles apply: `install`, `build`, `dev`, `prod`, `fmt`, `fix`, `typecheck`, `lint`, `check`, `fmt-check`, `test`, and `ci`. Add other recipes when the project needs them.

### Verification recipes

Group verification recipes by whether they rewrite project sources. Not every project needs every recipe:

- `fmt` is the safe write recipe and performs formatting only.
- `fix` composes `fmt`, then applies automatic lint fixes.
- `typecheck` validates types or compilation without rewriting project sources.
- `lint` performs source-preserving bug, smell, and anti-pattern checks with warnings treated as failures where supported.
- `check` is the fast local source-preserving gate and composes `typecheck` and `lint`.
- `fmt-check` verifies formatting without modifying files.
- `test` runs the test suite.
- `ci` is the strict source-preserving pull-request gate and composes the applicable checks, commonly `fmt-check`, `check`, and `test`, plus `build` when the project needs it.

### Other recipes

Add recipes for tedious workflow, such as rendering an LLM prompt or regenerating diagrams.

Prefer `dev` and `prod` over generic names such as `start` and `run` when a project has distinct development and production modes.

## Preferences

### Windows shell

Put the Windows shell configuration first:

```just
[windows]
set shell := ["pwsh", "-NoLogo", "-NoProfile", "-Command"]
```

### List

Document public recipes so their descriptions appear in `just --list`:

```just
set default-list

# This is the description.
foo:
    ...
```

### No nested shell

Call commands and scripts directly, using explicit shell invocation only when a different shell or shell-specific execution mode is required.

```just
bar:
    ./path/to/script.ps1
```

### Complexity

When a recipe needs complex control flow, move it into a dedicated script or task runner instead of inlining it in the justfile.

## References

See official Just manual at `https://just.systems/man/en/`.
