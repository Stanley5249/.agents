# oxfmt

Prefer [oxfmt](https://oxc.rs/docs/guide/usage/formatter.html) for JS, TS,
Svelte, CSS, HTML, JSON, YAML, and Markdown. Svelte and Tailwind CSS plugins are
built in. Review output differences when replacing Prettier.

## Install

- **Projects with a JS toolchain**, such as a Svelte app or a Tauri frontend:
  add `oxfmt` to `devDependencies` so the version is locked with everything
  else.
- **Other repositories**, including Rust, Python, and documentation projects:
  run `bunx oxfmt` for supported files when oxfmt is not installed locally.

## Configuration

Put the configuration in `.oxfmtrc.json` at the repository root. Point `$schema`
at the installed package when there is one, because it always matches the
running version:

```json
{
  "$schema": "./node_modules/oxfmt/configuration_schema.json",
  "printWidth": 80,
  "proseWrap": "always"
}
```

Without `node_modules`, use
`https://cdn.jsdelivr.net/npm/oxfmt/configuration_schema.json`.

Record only settings that differ from oxfmt's defaults. Check a default in the
schema's descriptions instead of guessing, and drop any setting that turns out
to match it. The settings below are the ones that usually matter:

| Setting           | Why set it                                                                |
| ----------------- | ------------------------------------------------------------------------- |
| `printWidth`      | Prettier's default is 80, so set 80 to keep Prettier-era output unchanged |
| `proseWrap`       | `"always"` wraps Markdown prose; keep the default if line breaks matter   |
| `svelte`          | `{}` enables `.svelte` files and needs the `svelte` package installed     |
| `sortTailwindcss` | `{ "stylesheet": "src/app.css" }` sorts classes for Tailwind CSS v4       |
| `ignorePatterns`  | gitignore-style globs, rooted at the directory holding the config         |

`proseWrap: "always"` breaks lines only at spaces. A paragraph of Chinese or
Japanese without spaces stays on one line, because a line break between two CJK
characters renders as a space in Markdown. Prettier behaves the same way.

## Ignores

oxfmt already skips `node_modules` and reads `.gitignore` and `.prettierignore`,
so `ignorePatterns` needs only files that are tracked but must not be formatted:

- **Files another formatter owns.** oxfmt formats TOML too. When `tombi` or
  another tool owns TOML, add `"**/*.toml"`, or the two formatters fight and
  parallel recipes race on the same files.
- **Vendored files** that must stay byte-identical to upstream, such as skills
  installed with `bunx skills add`.

Ignores also apply to content an editor passes to oxfmt, so an ignored file is
not formatted on save either. Ignore a file only when another formatter owns it
or it must stay byte-identical.

Prefer `ignorePatterns` over a `.prettierignore`, so one file holds the whole
configuration.

## Commands

When oxfmt is installed in `devDependencies`, use the locked local tool:

```sh
bun run oxfmt
bun run oxfmt --check
```

In repositories without a local oxfmt dependency, use:

```sh
bunx oxfmt
bunx oxfmt --check
```

The first command formats files in place. `--check` validates formatting while
preserving files.

## Migration from Prettier

- Start from a clean worktree where the existing Prettier check passes. Run
  `bunx oxfmt --migrate=prettier`, review settings and ignores, and handle
  `overrides` by hand.
- Replace Prettier and its plugins with oxfmt, keeping `svelte` where needed.
  Update recipes, CI, agent instructions, and editor integration. Keep ESLint
  presets that disable conflicting formatting rules.
- Move required ignores into `.oxfmtrc.json`, then remove the old Prettier
  configuration and `.prettierignore`.
- Format tracked files only. Use
  `git ls-files -z | xargs -0 bun run oxfmt --no-error-on-unmatched-pattern`,
  substituting `bunx oxfmt` when there is no local oxfmt dependency. Verify the
  formatted file count and inspect every diff.
- Compare against the clean baseline. Trial settings can leave expanded objects
  expanded because `objectWrap` preserves their layout. For a suspected bug,
  preserve the file with an ignore pattern and report the issue upstream.
- Run formatting checks, static checks, and tests. Commit tooling as `build` and
  formatting-only changes separately as `style`.
