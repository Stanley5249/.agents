# uv projects

## Layout

- `pyproject.toml` + `uv.lock`. Pin `.python-version` at the repo root.
- Run project Python commands with `uv run python`. Do not use `pip install --user` or create a loose virtual environment.

## Lint/format

- `ruff` is the only Python lint/format tool here — no black, isort, or flake8. Its defaults are usually enough; the one common addition is `[tool.ruff.lint] extend-select = ["I"]` for import sorting. Don't configure more rules than the project asked for.

## justfile

Script- and library-shaped uv projects get no justfile; bare `uv run pytest` and `uv run ruff check` are enough. When an application grows multiple entry points or a composed CI gate, read `reference/justfile.md`.
