# bun projects

The most consistent pattern on this machine. Existing bun projects follow it near-identically; read the `AGENTS.md` of one when scaffolding the same shape.

## Layout

- `bun.lock`, no `package-lock.json`/`yarn.lock`. Prefer bun, then deno, then node/npm.
- `package.json` holds only `dependencies`/`devDependencies` — **no `scripts` field**.

## justfile

Windows shell line first, then one command per recipe (avoid multi-line shell blocks in a recipe body — comment why if you must):

```
[windows]
set shell := ["pwsh", "-NoLogo", "-NoProfile", "-Command"]

set default-list

install:
    bun install

dev:
    bun run dev

format:
    bunx prettier --write .

lint:
    bunx prettier --check $(git diff --name-only --diff-filter=d; git ls-files --others --exclude-standard)

lint-all:
    bunx prettier --check .

check:
    bunx svelte-check

test:
    bun test

build:
    bun run build

ci: lint-all check build
```

Keep the `lint` (diff-only) vs `lint-all` (full sweep, used by `ci`) split.

## Lint/format

- **Prettier is the universal formatter; ESLint is not used here.** Standard config:
  ```json
  {
    "useTabs": true,
    "singleQuote": true,
    "trailingComma": "none",
    "printWidth": 100
  }
  ```
  Always add `prettier-plugin-svelte` for a Svelte project (Svelte is the default frontend choice here), and `prettier-plugin-tailwindcss` when Tailwind is in use.
- `svelte-check` is the type check the `check` recipe runs, distinct from `lint` (formatting) and `test`.

## CI

No `.github/workflows` — locally run `just ci` is the gate, unless the project is shared or the user asks.
