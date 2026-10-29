---
name: javascript
description: JavaScript and TypeScript conventions for Bun, oxlint, Svelte linting with ESLint, and justfile recipes. Use when writing, reviewing, or setting up JavaScript, TypeScript, or Svelte code.
---

# JavaScript and TypeScript

Use Bun as the runtime and package manager. Ask before adding or using `node`. TypeScript is the default dialect for application code.

## Layout

- Keep `bun.lock` as the only lockfile, and configure it in `.gitattributes`:

  ```gitattributes
  bun.lock merge=binary linguist-language=JSON linguist-generated=true -diff
  ```

- Keep `package.json` to `dependencies` and `devDependencies` when a justfile provides the command surface.

## Lint and type checking

- Lint plain JavaScript and TypeScript with type-aware oxlint. Add `oxlint` and `oxlint-tsgolint` to `devDependencies`, and set `typeAware`, `typeCheck`, and `denyWarnings` under `options` in `.oxlintrc.json`.
- Lint a Svelte project with ESLint, `typescript-eslint`, and `eslint-plugin-svelte`, because the Svelte plugin's template rules run only in ESLint. Run ESLint with `--max-warnings 0`, and type-check with `svelte-check`, separate from formatting and tests.
- Silence a lint with a `disable-next-line` comment that names the rule and gives the reason.
- Format with oxfmt, which the `project-setup` skill covers.

## Justfile

Put commands in justfile recipes that invoke local executables, and run `devDependencies` tools with `bun run <tool>`. Map `test` to `bun test`. `typecheck`, `lint`, `dev`, and `build` depend on the frontend tooling in use. Add `install` only when a dedicated `bun install` entry point is useful to the workflow.

Add a `lock-check` recipe that runs `bun install --frozen-lockfile` and include it in `ci`.
