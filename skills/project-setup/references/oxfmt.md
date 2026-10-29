# oxfmt

Prefer [oxfmt](https://oxc.rs/docs/guide/usage/formatter.html) for JS, TS, Svelte, CSS, HTML, JSON, YAML, and Markdown. Svelte and Tailwind CSS plugins are built in.

## Install and run

- In a project with a JS toolchain, add `oxfmt` to `devDependencies` and run `bun run oxfmt`, so the version is locked.
- Elsewhere, including Rust, Python, and documentation projects, run `bunx oxfmt`.
- Add `--check` to validate without writing.

## Configuration

Put the configuration in `.oxfmtrc.json` at the repository root. Point `$schema` at `./node_modules/oxfmt/configuration_schema.json` when the package is installed, because it matches the running version, and at `https://cdn.jsdelivr.net/npm/oxfmt/configuration_schema.json` otherwise.

Record only settings that differ from the defaults, and check a default in the schema instead of guessing:

- `printWidth`: the default is 100 but Prettier's is 80, so set 80 to keep Prettier-era output.
- `svelte`: `{}` enables `.svelte` files and needs the `svelte` package.
- `sortTailwindcss`: `{ "stylesheet": "src/app.css" }` sorts classes for Tailwind CSS v4.
- `ignorePatterns`: gitignore-style globs rooted at the config's directory.

Leave `proseWrap` at `"preserve"`, because `"always"` rewraps a whole paragraph after a one-word edit.

## Ignores

oxfmt already skips `node_modules` and reads `.gitignore` and `.prettierignore`. Put the rest in `ignorePatterns` instead of a `.prettierignore`, and ignore only these tracked files, because an ignored file is not formatted on save either:

- Files another formatter owns. oxfmt formats TOML too, so add `"**/*.toml"` when `tombi` owns TOML, or the two formatters fight and parallel recipes race.
- Vendored files that must stay byte-identical to upstream, such as skills installed with `bunx skills add`.

## Agent use

- Fix formatting by running the formatter on the files `--check` lists, never by hand.
- Format only the files you changed, such as `bunx oxfmt <file>...`, so unrelated files stay out of the diff.
- Re-read a file after formatting it before editing it again.

## Migration from Prettier

- Start from a clean worktree where the Prettier check passes, run `bunx oxfmt --migrate=prettier`, and port `overrides` by hand.
- Replace Prettier and its plugins, keeping `svelte` where needed, and update recipes, CI, agent instructions, and editor settings. Keep ESLint presets that disable conflicting formatting rules.
- Format tracked files only, with `git ls-files -z | xargs -0 bun run oxfmt --no-error-on-unmatched-pattern`, or `bunx oxfmt` without a local dependency, and inspect every diff against the clean baseline. `objectWrap` keeps trial-expanded objects expanded.
- For a suspected oxfmt bug, ignore the file and draft an upstream issue for approval.
- Commit the tooling as `build` and the reformat separately as `style`.
