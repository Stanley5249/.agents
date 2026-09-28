# Migrate from Prettier

The goal is a switch that changes no formatted output. Settle any style change
in its own later commit, so the migration diff contains only tooling.

## Translate the configuration

Start with the built-in migration:

```sh
bunx oxfmt --migrate=prettier
```

It writes `.oxfmtrc.json` from the Prettier configuration, including plugins and
`.prettierignore`, and pins the Prettier defaults that oxfmt does not share,
such as `printWidth: 80`. Then review the result:

- **Drop settings that match oxfmt's defaults,** such as `endOfLine: "lf"`, and
  settings with nothing to act on, such as `sortPackageJson` in a repository
  without `package.json`.
- **Prune `ignorePatterns`.** Remove entries that `.gitignore` already covers
  and lockfiles such as `bun.lock`, which oxfmt does not format.
- **Handle `overrides` by hand.** The migration skips them. An override that
  only set the Svelte parser can go, because oxfmt picks the parser from the
  extension.

## Swap the dependencies

Skip this section when the repository has no `package.json`. Otherwise, remove
`prettier` and its plugins from `devDependencies`. Add `oxfmt` when the project
installs dependencies, or use `bunx oxfmt` when it does not. Keep the `svelte`
package, because oxfmt loads the Svelte plugin at runtime but does not bundle
the compiler.

## Prove the output is unchanged

Start from a tree where `bunx prettier --check .` passes. Then delete
`.prettierrc*` and `.prettierignore` before running oxfmt, because oxfmt also
reads `.prettierignore`, which would hide a missing `ignorePatterns` entry. Run
`bunx oxfmt` on the tracked files only:

```sh
git ls-files -z | xargs -0 bunx oxfmt --no-error-on-unmatched-pattern
```

Limiting the run to tracked files keeps untracked user data out of it.
`ignorePatterns` still applies to paths passed this way, so check that the file
count in the `Finished ... on N files` line matches what should be formatted.
`git diff` should then be empty apart from the configuration and dependency
files.

Do not try to prove parity by reformatting with deliberately wrong settings and
then restoring. `objectWrap` defaults to `"preserve"` in both formatters, so an
object that a narrow `printWidth` expanded stays expanded, and the restore
leaves hundreds of false differences.

A few files may still differ, because oxfmt does not match Prettier in every
corner. Read each difference before changing settings. If it is a small layout
choice, accept it and commit the reformat separately as a `style` change. If it
looks like a bug, keep the file out with `ignorePatterns` and report it
upstream, rather than changing a setting that shifts the rest of the tree.

## Clean up

- Replace `prettier` in justfile recipes, CI, and agent instructions. Also
  search comments and documents for `prettierrc` and `prettierignore`, which a
  search for the command alone can miss. Prettier's `--ignore-unknown` has no
  counterpart because oxfmt already skips file types it cannot parse. Use
  `--no-error-on-unmatched-pattern` so a batch made only of such files, such as
  a list of changed files, does not fail.
- Keep ESLint presets such as `eslint-plugin-svelte`'s `flat/prettier`. They
  turn off rules that conflict with Prettier-style output, which oxfmt produces.
- Configure the editor in use, even if the project has no editor settings yet.
  An editor with a bundled Prettier keeps using it after the migration, and
  without `.prettierrc` that copy falls back to Prettier's defaults. With format
  on save, saved files then drift from `bunx oxfmt`. For Zed, see
  [zed.md](zed.md).

Commit this as one `build` change, such as `build: replace Prettier with oxfmt`.
