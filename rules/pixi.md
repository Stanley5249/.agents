# Pixi projects

This rule serves as an environment overlay on top of `project-setup.md`
alongside one or more language rules.

## When to use pixi

Pixi is for multi-language projects or projects with heavy native or GPU
dependencies, such as a cargo workspace that also needs a pinned CUDA toolchain
from conda-forge. Plain Rust or Python projects use cargo or uv directly,
because pixi's conda-forge toolchain handling pays off only when native
dependencies need it.

## Repository metadata

In `.gitattributes`, configure `pixi.lock`:

```gitattributes
pixi.lock merge=binary linguist-language=YAML linguist-generated=true -diff
```

## Layout

- A Python project keeps pixi's configuration under `[tool.pixi.*]` in
  `pyproject.toml`, so one manifest holds the package and its environments.
  Other projects use `pixi.toml` at the root.
- `.pixi/` holds the resolved environment and is gitignored.
- A single pixi environment can wrap a full cargo workspace with multiple member
  crates: pixi manages the native toolchain and GPU dependencies, cargo still
  manages the Rust build inside it.

## Tools environment

Lock the command-line tools that recipes and CI call, such as just, ruff, and
tombi, in their own environment, so their pins never move the runtime libraries:

```toml
[tool.pixi.feature.tools.dependencies]
just = "*"
ruff = "*"
tombi = "*"

[tool.pixi.environments]
ci = { features = ["tools"], no-default-feature = true }
```

In `pixi.toml`, drop the `tool.pixi.` prefix.

## Lint, format, and justfile

Use the wrapped language's tools, but run them with `pixi run -e <environment>`
from justfile recipes instead of pixi tasks. Name the environment in every call,
because inside an activated environment a bare `pixi run` uses that one.

Export `PIXI_LOCKED := "true"` in the justfile, so every `pixi run` fails on a
stale `pixi.lock` instead of re-solving. Add a `lock-check` recipe that runs
`pixi lock --check --dry-run` and include it in `ci`.
