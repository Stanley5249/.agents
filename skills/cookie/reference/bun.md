# bun projects

The most consistent pattern on this machine.

## Layout

- Use `bun.lock`, with no `package-lock.json` or `yarn.lock`.
- Keep `package.json` to `dependencies` and `devDependencies`, with no `scripts` field when a justfile provides the command surface.

## Lint and format

Standard config:

```json
{
  "useTabs": true,
  "singleQuote": true,
  "trailingComma": "none",
  "printWidth": 100
}
```

Add `prettier-plugin-svelte` for Svelte and `prettier-plugin-tailwindcss` when using Tailwind. For a Svelte project, use `svelte-check` for type checking, separate from formatting and tests.

## Justfile

Keep commands out of `package.json` scripts and invoke local executables directly. `install`, `format`, `lint` (and `lint-all`, if the project splits diff-only from full-sweep linting), and `test` are bun-driven regardless of framework (`bun install`, `bunx prettier`, `bun test`); `dev`, `check`, and `build` depend on the frontend tooling in use (Vite, SvelteKit, or otherwise) and aren't a bun convention.
