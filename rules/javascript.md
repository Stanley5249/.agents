# JavaScript projects

This rule extends `project-setup.md` for JavaScript and TypeScript projects. Use
Bun as the runtime and package manager. TypeScript is the default dialect for
application code.

## Repository metadata

In `.gitattributes`, configure `bun.lock`:

```gitattributes
bun.lock merge=binary linguist-language=JSON linguist-generated=true -diff
```

## Layout

- Keep `bun.lock` as the only lockfile.
- Keep `package.json` to `dependencies` and `devDependencies` when a justfile
  provides the command surface.

## Lint and type checking

- Lint plain JavaScript and TypeScript with type-aware oxlint: add `oxlint` and
  `oxlint-tsgolint` to `devDependencies` and set `typeAware` and `denyWarnings`
  under `options` in `.oxlintrc.json`.
- Lint a Svelte project with ESLint, `typescript-eslint`, and
  `eslint-plugin-svelte`, because oxlint has no counterpart to the Svelte
  plugin's template rules. Run ESLint with `--max-warnings 0`, and type-check
  with `svelte-check`, separate from formatting and tests.
- Every lint disable comment needs a reason. Never disable a rule for a whole
  file.

## Justfile

Put commands in justfile recipes that invoke local executables directly. Typical
Bun-backed mappings include `fmt` and `fmt-check` through `bunx oxfmt`, and
`test` through `bun test`; `typecheck`, `lint`, `dev`, and `build` depend on the
frontend tooling in use. Add `install` only when a dedicated `bun install` entry
point is useful to the workflow.

Add a `lock-check` recipe that runs `bun install --frozen-lockfile` and include
it in `ci`.
