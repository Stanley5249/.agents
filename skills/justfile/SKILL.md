---
name: justfile
description:
  Guidance for creating and maintaining justfiles, including recipe design,
  verification gates, and Windows PowerShell configuration.
---

## Scope

Use this skill when creating, updating, or reviewing a justfile.

## When to add one

Use a justfile when a project needs a composed command surface for recurring
development and verification commands. Small script- or library-shaped projects
can use their package manager directly until that surface becomes useful.

## Public command surface

When a justfile exists, document and invoke its recipes instead of duplicating
raw commands elsewhere. Start with the smallest useful set of recipes for the
project's current workflow, then add more as the workflow grows. Use consistent
names when their roles apply: `install`, `build`, `dev`, `prod`, `fmt`, `fix`,
`typecheck`, `lint`, `check`, `fmt-check`, `test`, and `ci`. Prefer `dev` and
`prod` over generic names such as `start` and `run` when a project has distinct
development and production modes.

Document public recipes so their descriptions appear in `just --list`. Set
`default-list` for command-oriented projects, use `just --usage` for
parameterized recipes, and use `just --show` when inspecting a recipe.

Mark composition-only recipes `[private]` so they do not appear in the public
surface. Use `[group("name")]` only when a large recipe list needs navigation.
Add aliases only for clear, public shortcuts.

## Recipe interfaces

Use recipe parameters with defaults for controlled variants. For non-trivial
public recipes, prefer named options with `[arg("name", long, help="...")]` over
unclear positional arguments.

Quote every `{{parameter}}` substitution that might contain spaces. Use `+args`
only when at least one value is required.

### Optional passthrough flags

Expose a trailing `*args` parameter when callers may need to forward optional
flags to the underlying command. It must remain optional, so `just test` works
without extra arguments.

```just
test *args:
    cargo test {{args}}
```

Use this only for intentional passthrough. Keep the recipe's standard behavior
explicit rather than making callers supply normal project defaults.

## Verification recipes

Group verification recipes by whether they rewrite project sources. Not every
project needs every recipe:

- `fmt` is the safe write recipe and performs formatting only.
- `fix` composes `fmt`, then applies automatic lint fixes.
- `typecheck` validates types or compilation without rewriting project sources.
- `lint` performs source-preserving bug, smell, and anti-pattern checks with
  warnings treated as failures where supported.
- `check` is the fast local source-preserving gate and composes `typecheck` and
  `lint`.
- `fmt-check` verifies formatting without modifying files. Include
  `just --fmt --check` here to also verify the justfile's own formatting.
- `test` runs the test suite.
- `ci` is the strict source-preserving pull-request gate and composes the
  applicable checks, commonly `fmt-check`, `check`, and `test`, plus `build`
  when the project needs it.

## Other recipes

Add recipes for tedious workflow, such as rendering an LLM prompt or
regenerating diagrams.

## Dependencies and parallelism

Dependencies compose verification gates sequentially by default. Use
`[parallel]` only for independent, source-preserving prerequisites. Limit
concurrency with `--jobs` when a project needs it.

When the same recipe must run for a known list of items, prefer a native list
and mapped dependencies over a shell loop, especially a platform-specific
PowerShell loop. Put the per-item operation in a private helper so failures
remain attributable to individual items and the public command surface stays
small:

```just
set minimum-version := "1.53.0"
set unstable
set lists

targets := ["app", "docs"]

_build target:
    build-tool "{{ target }}"

build: *(_build *targets)
```

## Execution context

Recipes normally run from the directory containing their justfile, even when
`just` is invoked from a subdirectory. Use `[no-cd]` only for a command
intentionally operating on the caller's directory. Use
`[working-directory("path")]` only when a recipe belongs in a fixed
subdirectory.

Each ordinary recipe line runs in a separate shell. Call commands and scripts
directly, using explicit shell invocation only when a different shell or
shell-specific execution mode is required.

Use a `[script(COMMAND)]` recipe for a small multi-line task when it is clearer
than shell lines. Move reusable or complex control flow into a dedicated script
or task runner.

## Environment

Use `set dotenv-load` only when the project expects a local `.env` file. Loaded
values are environment variables and must be read as `$NAME`, not `just`
variables. Do not enable `dotenv-override` by default.

Prefer per-recipe `[env(...)]` or `export NAME := "value"` for required
environment configuration. Do not enable a global export policy without a
project-specific reason.

## Safety

Failures stop recipes by default. Prefix a command with `-` only when failure is
explicitly best-effort.

Require `[confirm("...")]` for deploys, releases, migrations, and destructive
cleanup. The confirmation text must state the operation and target clearly.

## Windows shell

`just` uses `sh` by default, including on Windows. Put this Windows
configuration first for PowerShell-based projects:

```just
[windows]
set shell := ["pwsh", "-NoLogo", "-NoProfile", "-Command"]
```

Use `[windows]` and `[unix]` only for genuinely platform-specific recipes or
settings. Do not enable `set positional-arguments` with this PowerShell
configuration unless the project explicitly requires PowerShell 7.4+ with
`-CommandWithArgs`.

## Modularization

Use `import "path.just"` to split a growing justfile while retaining one command
namespace. Use `mod name "path.just"` for a self-contained command domain that
callers invoke as `just name recipe` or `just name::recipe`. Do not modularize
before the justfile becomes difficult to scan.

## Conditional features

Use `set minimum-version := "x.y.z"` when the justfile depends on newer syntax.

Use the `[timestamp]` attribute or the `--timestamp` flag to diagnose
long-running recipes.

Accept unstable features, such as using native lists and mapped dependencies.

## References

See the official Just manual at <https://just.systems/man/en/>.
