# Zed

## Project settings

- Global settings are at `%APPDATA%\Zed\settings.json`.
- For lists such as `file_scan_exclusions`, use `"..."` before project entries
  to preserve inherited values, such as
  `"file_scan_exclusions": ["...", "**/node_modules"]`. Check each setting's
  [Zed documentation](https://zed.dev/docs/reference/all-settings) for marker
  support and behavior.
- Set `language_servers` in each language block that needs an override, because
  per-language settings replace top-level settings.
- In `language_servers`, `"..."` includes other registered servers. Keep
  explicit server priorities and `!server` exclusions from the defaults when
  needed, as
  [Zed's language-server documentation](https://zed.dev/docs/configuring-languages#working-with-language-servers)
  explains.
- Track `.zed/settings.json` for shared project tooling. Keep personal editor
  preferences in global settings.

## Formatting with oxfmt

- With `"formatter": "auto"`, Zed uses bundled Prettier when allowed, or the
  first language server that can format the file otherwise.
- Disable bundled Prettier and select `oxfmt` in each project language block so
  the editor uses `.oxfmtrc.json`. Keep only the languages the project contains:

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

- For Svelte, enable `"svelte": {}` in `.oxfmtrc.json` and keep the `svelte`
  package installed so oxfmt formats `.svelte` files in the editor and on the
  command line.

## Other formatters

- When another tool owns a language, select that tool's formatter and exclude
  oxfmt for that language. For example, when `tombi` owns TOML:

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

- In plain JavaScript or TypeScript projects, keep the Oxc extension's `oxlint`
  server active.
- In Svelte projects, use ESLint for code and template linting. Disable oxlint
  with `"language_servers": ["!oxlint", "..."]` at the top level and in each
  relevant language block.
- In Rust projects, configure rust-analyzer to check with Clippy so the editor
  uses the same lints as the `lint` recipe:

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

- In WSL, `zed` is available through Windows Zed's
  [WSL integration](https://zed.dev/docs/reference/cli#wsl-integration-windows).
