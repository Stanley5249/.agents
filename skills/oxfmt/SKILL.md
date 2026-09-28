---
name: oxfmt
description:
  Configure and run oxfmt, the Prettier-compatible formatter from Oxc, for JS,
  TS, Svelte, CSS, HTML, JSON, YAML, and Markdown, including migration from
  Prettier and Zed editor integration.
---

# oxfmt

oxfmt is a single native binary that formats what Prettier formats, with the
Svelte and Tailwind CSS plugins built in. Its output matches Prettier's for the
same settings in all but a few corners, so it replaces Prettier without
restyling a codebase.

## Install

- **Projects with a JS toolchain**, such as a Svelte app or a Tauri frontend:
  add `oxfmt` to `devDependencies` so the version is locked with everything
  else.
- **Documentation-first repositories** with no `package.json`: run `bunx oxfmt`
  and add no dependency.

`bunx oxfmt` uses the local copy when one is installed, so recipes can use the
same command in both cases.

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

| Setting           | Default      | Why set it                                                                |
| ----------------- | ------------ | ------------------------------------------------------------------------- |
| `printWidth`      | `100`        | Prettier's default is 80, so set 80 to keep Prettier-era output unchanged |
| `proseWrap`       | `"preserve"` | `"always"` wraps Markdown prose at `printWidth`, useful for documentation |
| `sortPackageJson` | `true`       | set `false` to leave the key order that `bun add` and humans wrote        |
| `svelte`          | disabled     | `{}` enables `.svelte` files and needs the `svelte` package installed     |
| `sortTailwindcss` | disabled     | `{ "stylesheet": "src/app.css" }` sorts classes for Tailwind CSS v4       |
| `ignorePatterns`  | `[]`         | gitignore-style globs, rooted at the directory holding the config         |

Keep `proseWrap` at `"preserve"` when author-chosen line breaks matter, such as
text rendered by a line-break-sensitive viewer.

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
not formatted on save either. Do not ignore files that people edit and expect to
be formatted.

Prefer `ignorePatterns` over a `.prettierignore`, so one file holds the whole
configuration.

## Commands

```sh
bunx oxfmt            # format the tree in place
bunx oxfmt --check    # fail on unformatted files, change nothing
```

In a justfile, map these to `fmt` and `fmt-check`. When TOML is excluded, the
oxfmt and tombi recipes touch disjoint files and can run in parallel.

## Further reading

- [reference/migrate-from-prettier.md](reference/migrate-from-prettier.md):
  replacing Prettier in an existing project and proving the output is unchanged.
- [reference/zed.md](reference/zed.md): making Zed format with oxfmt instead of
  its bundled Prettier.
