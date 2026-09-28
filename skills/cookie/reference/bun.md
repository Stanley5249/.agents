# Bun projects

The most consistent pattern on this machine.

## Layout

- Use `bun.lock`, with no `package-lock.json` or `yarn.lock`.
- In `.gitattributes`, configure:
  ```gitattributes
  bun.lock merge=binary linguist-language=JSON linguist-generated=true -diff
  ```
- Keep `package.json` to `dependencies` and `devDependencies`, with no `scripts`
  field when a justfile provides the command surface.

## Lint and format

Format with oxfmt, and load the `oxfmt` skill to configure it. For a Svelte
project, use `svelte-check` for type checking, separate from formatting and
tests.

## Justfile

Keep commands out of `package.json` scripts and invoke local executables
directly. Follow the shared recipe split in the
[Justfile skill](../../justfile/SKILL.md), adding only the recipes the project
currently needs. Typical Bun-backed mappings include `fmt` and `fmt-check`
through `bunx oxfmt`, and `test` through `bun test`; `typecheck`, `lint`, `dev`,
and `build` depend on the frontend tooling in use. Add `install` only when a
dedicated `bun install` entry point is useful to the workflow.
