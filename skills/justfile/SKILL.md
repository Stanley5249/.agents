---
name: justfile
description:
  Guidance for creating and maintaining justfiles, including recipe design,
  verification gates, and Windows PowerShell configuration.
---

# justfile

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

Use `_name` for a small private helper and `[private]` when a public-looking
name improves readability. Add `[group("name")]` when a large recipe list needs
navigation, and reserve aliases for clear public shortcuts.

## Recipe interfaces

Use recipe parameters with defaults for controlled variants. For non-trivial
public recipes, prefer named options with `[arg("name", long, help="...")]` over
unclear positional arguments.

Quote scalar `{{ parameter }}` substitutions for the active shell. Use `+args`
for one-or-more values and a trailing `*args` for intentional optional
passthrough:

```just
test *args:
    cargo test {{ args }}
```

Keep standard behavior explicit in the recipe. Without lists, `{{ args }}`
forwards one whitespace-separated string through the shell. With lists,
`quote(args)` quotes each element using Bourne-shell syntax; use native argument
handling in PowerShell. See the Just README for shell-specific forwarding
details.

## Verification recipes

Select applicable verification recipes and group them by whether they rewrite
project sources:

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

Dependencies compose verification gates sequentially. Use `[parallel]` for
independent, concurrency-safe prerequisites and `--jobs` to bound concurrency.
Dependencies before `&&` precede the recipe body, dependencies after it follow
the body, and identical invocations run once. See the Just README for advanced
dependency-graph behavior.

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

Mapped dependencies run sequentially; add `[parallel]` to the parent recipe for
concurrent mapping.

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

Use `set dotenv-load` when the project expects a local `.env` file. Loaded
values are environment variables: read them as `$NAME` in `sh` and `$env:NAME`
in PowerShell. Keep existing environment values authoritative, enabling
`dotenv-override` when dotenv should replace them.

Prefer per-recipe `[env(...)]` or `export NAME := "value"` for required
configuration. Choose a global export policy when the whole project needs it.

## Safety

Failures stop recipes by default. Prefix a command with `-` only when failure is
explicitly best-effort.

Require `[confirm("...")]` for deploys, releases, migrations, and destructive
cleanup. State the operation and target clearly. Automation can approve prompts
with `--yes`; see the Just README for confirmation behavior in dependency
graphs.

## Windows shell

`just` uses `sh` by default, including on Windows. For PowerShell-based
projects, select an installed executable explicitly near the start of the file:

```just
[windows]
set shell := ["pwsh", "-NoLogo", "-NoProfile", "-Command"]
```

Use `[windows]` and `[unix]` for genuinely platform-specific recipes or
settings. For positional arguments, select PowerShell 7.4+ with
`-CommandWithArgs`; ordinary recipes use `-Command` as above.

## Modularization

Use `import "path.just"` to merge definitions into the current namespace and
`mod name "path.just"` for an isolated command domain. Invoke module recipes as
`just name recipe` or `just name::recipe`; they normally run relative to their
module source. Modularize when the root justfile becomes difficult to scan. See
the Just README for namespace, setting, and working-directory details.

## Conditional features

Place `set minimum-version := "x.y.z"` before syntax that requires that version.
Use `[timestamp]` or `--timestamp` to diagnose long-running recipes.

Accept unstable features when they materially improve structure, such as native
lists and mapped dependencies replacing shell loops. Opt in with `set unstable`
and enable separately gated features such as `set lists`; consult the Just
README for their evolving contracts.

## References

See the
[Just README on GitHub](https://github.com/casey/just/blob/master/README.md),
which tracks the latest `master` branch.
