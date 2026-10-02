# uv projects

## Layout

- `pyproject.toml` + `uv.lock`. Pin `.python-version` at the repo root.
- Add packages with `uv add` and let uv manage the project's `.venv`.

## Lint and format

- Use `ruff` as the only linter and formatter. Its defaults are usually enough;
  the one common addition is `[tool.ruff.lint] extend-select = ["I"]` for import
  sorting. Configure only the rules the project asks for.

## Justfile

Script- and library-shaped uv projects run `uv run pytest` and
`uv run ruff check` directly. Add a justfile when an application grows multiple
entry points or needs a composed CI gate.
