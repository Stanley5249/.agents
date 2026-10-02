# uv projects

## Layout

- `pyproject.toml` + `uv.lock`. Pin `.python-version` at the repo root.
- Add packages with `uv add` and let uv manage the project's `.venv`.

## Lint, format, and type checking

- Use `ruff` as the only linter and formatter. Start every project with all
  rules selected and Google-style docstrings. Ignore a rule when the project
  needs to, with a comment that says why:

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

Until the project has a justfile, run `uv run pytest` and `uv run ruff check`
directly.
