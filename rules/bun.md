# Bun projects

## Layout

- Keep `bun.lock` as the only lockfile.
- Keep `package.json` to `dependencies` and `devDependencies` when a justfile
  provides the command surface.

## Type checking

For a Svelte project, use `svelte-check` for type checking, separate from
formatting and tests.

## Justfile

Put commands in justfile recipes that invoke local executables directly. Add
only the justfile recipes the project currently needs. Typical Bun-backed
mappings include `fmt` and `fmt-check` through `bunx oxfmt`, and `test` through
`bun test`; `typecheck`, `lint`, `dev`, and `build` depend on the frontend
tooling in use. Add `install` only when a dedicated `bun install` entry point is
useful to the workflow.
