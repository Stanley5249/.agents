# Pixi projects

## When to use pixi

Pixi is for multi-language projects or projects with heavy native or GPU
dependencies, such as a cargo workspace that also needs a pinned CUDA toolchain
from conda-forge. Plain Rust or Python projects use cargo or uv directly,
because pixi's conda-forge toolchain handling pays off only when native
dependencies need it.

## Layout

- `pixi.toml` at the root, and `.pixi/` holds the resolved environment, which is
  gitignored.
- Can wrap a full cargo workspace with multiple member crates in a single pixi
  environment: pixi manages the native toolchain and GPU dependencies, cargo
  still manages the Rust build inside it.

## Lint, format, and justfile

Follow the rules of the wrapped language. Run commands through `pixi run <task>`
or a justfile recipe shelling out to `pixi run`, whichever the project already
uses.
