# Format with oxfmt in Zed

Zed formats JS, TS, CSS, HTML, JSON, YAML, and Markdown with its own bundled
Prettier by default. The Oxc extension provides an `oxfmt` language server that
respects `.oxfmtrc.json`, but another language server can take priority over it.
The Svelte language server, for example, formats `.svelte` files with its own
Prettier. Either way, saving a file and running `bunx oxfmt` would disagree.

Turn Prettier off in the project's `.zed/settings.json` and name `oxfmt` as the
formatter for each language the project contains:

```json
{
  "prettier": {
    "allowed": false
  },
  "languages": {
    "JavaScript": {
      "formatter": { "language_server": { "name": "oxfmt" } }
    },
    "TypeScript": {
      "formatter": { "language_server": { "name": "oxfmt" } }
    },
    "Svelte": {
      "formatter": { "language_server": { "name": "oxfmt" } }
    },
    "JSON": {
      "formatter": { "language_server": { "name": "oxfmt" } }
    },
    "JSONC": {
      "formatter": { "language_server": { "name": "oxfmt" } }
    },
    "HTML": {
      "formatter": { "language_server": { "name": "oxfmt" } }
    },
    "CSS": {
      "formatter": { "language_server": { "name": "oxfmt" } }
    },
    "Markdown": {
      "formatter": { "language_server": { "name": "oxfmt" } }
    }
  }
}
```

Naming the formatter for each language keeps Zed's behavior independent of
language server priority and the extension's defaults. Add or remove languages,
such as `TSX` or `YAML`, to match the files the project has.

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

The Oxc extension also starts the `oxlint` language server. When the project
lints with ESLint instead, turn it off at the top level so the editor does not
show a second, disagreeing set of diagnostics:

```json
{
  "language_servers": ["!oxlint", "..."]
}
```
