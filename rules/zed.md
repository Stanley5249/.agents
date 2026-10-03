# Zed

## Project settings

Read the global settings at `%APPDATA%\Zed\settings.json` before changing a
project's `.zed/settings.json`, and set only what differs from them. A list
setting such as `file_scan_exclusions` replaces Zed's default list, so a project
that adds entries also copies the defaults it still needs.

Zed's built-in settings also set `language_servers` per language, and a
per-language list replaces the top-level one. Set it in each language block, and
copy the built-in entries the language still needs. `zed: open default settings`
shows them.

Track `.zed/settings.json` when it aligns formatters or linters with the
project's command-line tools, so every checkout formats the same way as the
command line. When the file holds only personal language-server tweaks, leave it
untracked.

## Format with oxfmt

Zed's default formatter, `"auto"`, uses its bundled Prettier for every language
where `prettier.allowed` is true, and falls back to a language server only
otherwise. Prettier is allowed by default for JS, TS, Svelte, CSS, HTML, JSON,
YAML, and Markdown, so it wins over the Oxc extension's `oxfmt` language server
even when that server is running. The bundled Prettier ignores `.oxfmtrc.json`.
Without a `.prettierrc`, it uses Prettier's defaults, so, for example, it never
wraps Markdown prose.

Turning Prettier off is not enough on its own. With `"auto"`, Zed then uses the
first language server that can format the file, which may not be oxfmt. The
Svelte language server, for example, formats `.svelte` files with its own copy
of Prettier.

So turn Prettier off and name `oxfmt` as the formatter for each language the
project contains:

```json
{
  "prettier": { "allowed": false },
  "languages": {
    "JavaScript": { "formatter": { "language_server": { "name": "oxfmt" } } },
    "TypeScript": { "formatter": { "language_server": { "name": "oxfmt" } } },
    "TSX": { "formatter": { "language_server": { "name": "oxfmt" } } },
    "Svelte": { "formatter": { "language_server": { "name": "oxfmt" } } },
    "JSON": { "formatter": { "language_server": { "name": "oxfmt" } } },
    "JSONC": { "formatter": { "language_server": { "name": "oxfmt" } } },
    "HTML": { "formatter": { "language_server": { "name": "oxfmt" } } },
    "CSS": { "formatter": { "language_server": { "name": "oxfmt" } } },
    "YAML": { "formatter": { "language_server": { "name": "oxfmt" } } },
    "Markdown": { "formatter": { "language_server": { "name": "oxfmt" } } }
  }
}
```

Keep only the languages the project contains.

For Svelte, also enable `"svelte": {}` in `.oxfmtrc.json`. Without it, oxfmt
skips `.svelte` files, both on the command line and in the editor.

## When another tool owns a language

oxfmt also offers to format TOML. When `tombi` owns TOML, name its language
server and exclude oxfmt, so Zed does not pick the wrong one:

```json
{
  "languages": {
    "TOML": {
      "formatter": { "language_server": { "name": "tombi" } },
      "language_servers": ["!oxfmt", "..."]
    }
  }
}
```

## Linters

The Oxc extension also starts the `oxlint` language server. In a plain
JavaScript or TypeScript project, keep oxlint active as `javascript.md`
describes.

In a Svelte project, oxlint cannot lint Svelte templates, so ESLint handles
linting instead. Turn off oxlint so the editor does not show conflicting
diagnostics. Keep a root-level fallback, and disable oxlint in each language
block that the repository contains:

```json
{
  "language_servers": ["!oxlint", "..."],
  "languages": {
    "JavaScript": {
      "language_servers": ["!oxlint", "..."]
    },
    "TypeScript": {
      "language_servers": ["!oxlint", "..."]
    },
    "Svelte": {
      "language_servers": ["!oxlint", "..."]
    }
  }
}
```

Zed defaults already run `vtsls` and disable `typescript-language-server`, so
writing `["!oxlint", "..."]` disables oxlint while preserving all built-in
defaults without restating them.

In a Rust project, have rust-analyzer check with Clippy, so the editor shows the
same lints as the `lint` recipe:

```json
{
  "lsp": {
    "rust-analyzer": {
      "initialization_options": { "check": { "command": "clippy" } }
    }
  }
}
```

## WSL

WSL projects use Zed's
[WSL remote server](https://zed.dev/docs/remote-development#opening-a-local-folder-in-wsl).
