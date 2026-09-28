# Format with oxfmt in Zed

Zed formats JS, TS, CSS, HTML, JSON, YAML, and Markdown with its own bundled
Prettier unless told otherwise. That copy ignores `.oxfmtrc.json`, so saving a
file and running `bunx oxfmt` would disagree.

The Oxc extension provides an `oxfmt` language server that reads the project's
configuration. Turn Prettier off in the project's `.zed/settings.json` and name
`oxfmt` as the formatter for each language the project contains:

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

Naming the formatter for each language keeps Zed's behavior independent of the
extension's defaults. Add or remove languages, such as `TSX` or `YAML`, to match
the files the project has.

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
