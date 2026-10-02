# uv projects

## Layout

- `pyproject.toml` + `uv.lock`. Pin `.python-version` at the repo root.
- Do not use `pip install --user` or create a loose virtual environment.

## Lint and format

- Do not add black, isort, or flake8 next to `ruff`. Its defaults are usually
  enough; the one common addition is `[tool.ruff.lint] extend-select = ["I"]`
  for import sorting. Don't configure more rules than the project asked for.

## Justfile

Script- and library-shaped uv projects get no justfile; bare `uv run pytest` and
`uv run ruff check` are enough. Add one only when an application grows multiple
entry points or needs a composed CI gate.
