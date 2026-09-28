# Migrate from Prettier

The goal is a switch that changes no formatted output. Settle any style change
in its own later commit, so the migration diff contains only tooling.

## Translate the configuration

Start with the built-in migration:

```sh
bunx oxfmt --migrate=prettier
```

It writes `.oxfmtrc.json` from the Prettier configuration. It pins
`printWidth: 80`, because Prettier's default is 80 and oxfmt's is 100. It also
sets `sortPackageJson: false`, because Prettier never sorted `package.json`.
`prettier-plugin-svelte` becomes `"svelte": {}`, `prettier-plugin-tailwindcss`
becomes `sortTailwindcss`, and `.prettierignore` is copied into
`ignorePatterns`. Then review the result:

- **Drop settings that match oxfmt's defaults,** such as `endOfLine: "lf"`.
- **Prune `ignorePatterns`.** Remove entries that `.gitignore` already covers
  and lockfiles such as `bun.lock`, which oxfmt does not format.
- **Handle `overrides` by hand.** The migration skips them. An override that
  only set the Svelte parser can go, because oxfmt picks the parser from the
  extension.

## Swap the dependencies

Remove `prettier` and its plugins from `devDependencies`. Add `oxfmt` when the
project installs dependencies, or use `bunx oxfmt` when it does not. Keep the
`svelte` package, because oxfmt loads the Svelte plugin at runtime but does not
bundle the compiler.

## Prove the output is unchanged

Start from a clean tree that Prettier formatted, then:

1. Run `bunx oxfmt`. `git diff` should be empty apart from the configuration and
   dependency files.
2. For a stronger check, reformat the tree with deliberately wrong settings,
   such as `printWidth: 40` and `useTabs: true`, then restore the real
   configuration and run `bunx oxfmt` again. An empty `git diff` shows oxfmt
   reproduces every file on its own, instead of merely leaving already formatted
   files alone.

If a file differs, compare it with Prettier's output before changing settings.
The difference may be an oxfmt bug, which belongs in an ignore entry or an
upstream issue, not in a setting that shifts the rest of the tree.

## Clean up

- Delete `.prettierrc*` and `.prettierignore`.
- Replace `prettier` in justfile recipes, CI, and agent instructions.
- Update the editor configuration. For Zed, see [zed.md](zed.md).

Commit this as one `build` change, such as `build: replace Prettier with oxfmt`.
If the new configuration intentionally reflows files, such as by turning on
`proseWrap: "always"`, commit that reformat separately.
