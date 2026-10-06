# Python projects

This rule extends `project-setup.md` for Python projects. Use uv for package
management and virtual environment handling.

## Repository metadata

In `.gitattributes`, configure `uv.lock`:

```gitattributes
uv.lock merge=binary linguist-language=TOML linguist-generated=true -diff
```

## Layout

- Keep `pyproject.toml`, `uv.lock`, and a pinned `.python-version` at the
  repository root.
- Add packages with `uv add` and let uv manage the project's `.venv`.

## Build backend

- For packaged libraries, use uv's native build backend:

  ```toml
  [build-system]
  requires = ["uv_build>=0.12.0"]
  build-backend = "uv_build"
  ```

- For standalone applications or scripts that do not publish wheels, disable
  package building in `pyproject.toml`:

  ```toml
  [tool.uv]
  package = false
  ```

## Python version and syntax

Check the target Python version in `.python-version` or `pyproject.toml`
(`requires-python`) before writing code, and use the latest syntax supported by
that version.

## Lint, format, and type checking

- Use `ruff` as the only linter and formatter. Start every project with all
  rules selected and Google-style docstrings:

  ```toml
  [tool.ruff.lint]
  select = ["ALL"]
  ignore = [
    "COM812", # conflicts with the formatter
  ]

  [tool.ruff.lint.pydocstyle]
  convention = "google"
  ```

- Type-check with pyrefly's strict preset:

  ```toml
  [tool.pyrefly]
  preset = "strict"
  ```

## Justfile

Put commands in justfile recipes that invoke local executables through `uv run`.
Typical mappings include `fmt` and `fmt-check` through `uv run ruff format`,
`lint` through `uv run ruff check`, `typecheck` through `uv run pyrefly check`,
and `test` through `uv run pytest`.

Add a `lock-check` recipe that runs `uv lock --check` and include it in `ci`.
