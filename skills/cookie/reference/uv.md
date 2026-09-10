# uv projects

## Layout

- `pyproject.toml` + `uv.lock`. Pin `.python-version` at the repo root.
- Run project Python commands with `uv run python`. Do not use `pip install --user` or create a loose virtual environment.

## Lint/format

- `ruff` is the only Python lint/format tool here — no black, isort, or flake8. Its defaults are usually enough; the one common addition is `[tool.ruff.lint] extend-select = ["I"]` for import sorting. Don't configure more rules than the project asked for.
- For type checking, follow whatever the project or editor already has configured (`ty`, `basedpyright`, or another LSP); default to `pyrefly` when none is set up yet.

## justfile

Script- and library-shaped uv projects get no justfile; bare `uv run pytest` and `uv run ruff check` are enough. Add one only when an application grows multiple entry points or needs a composed CI gate.
