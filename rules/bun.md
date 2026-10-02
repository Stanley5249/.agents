# Bun projects

## Layout

- Use `bun.lock`, with no `package-lock.json` or `yarn.lock`.
- Keep `package.json` to `dependencies` and `devDependencies`, with no `scripts`
  field when a justfile provides the command surface.

## Type checking

For a Svelte project, use `svelte-check` for type checking, separate from
formatting and tests.

## Justfile

Keep commands out of `package.json` scripts and invoke local executables
directly. Add only the justfile recipes the project currently needs. Typical
Bun-backed mappings include `fmt` and `fmt-check` through `bunx oxfmt`, and
`test` through `bun test`; `typecheck`, `lint`, `dev`, and `build` depend on the
frontend tooling in use. Add `install` only when a dedicated `bun install` entry
point is useful to the workflow.
