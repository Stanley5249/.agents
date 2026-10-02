# Pixi projects

## When this is the right choice

Pixi is for multi-language or native/GPU-dependency-heavy projects, such as a
cargo workspace that also needs a pinned CUDA/conda-forge toolchain. Not the
default for a plain Rust or Python project, because it adds conda-forge-managed
native toolchain handling that most projects don't need.

## Layout

- `pixi.toml` at the root, `.pixi/` holds the resolved environment (gitignore
  it).
- Can wrap a full cargo workspace (multiple member crates) in a single pixi
  environment: pixi manages the native toolchain/GPU deps, cargo still manages
  the Rust build inside it.

## Lint/format/justfile

No pixi-specific convention beyond what the wrapped language already needs. Run
commands through `pixi run <task>` or a justfile recipe shelling out to
`pixi run`, whichever the project already uses.
