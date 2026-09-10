# uv projects

## Layout

- `pyproject.toml` + `uv.lock`. Pin `.python-version` at the repo root.
- Run project Python commands with `uv run python`. Do not use `pip install --user` or create a loose virtual environment.

## Lint/format

- `ruff` is the only Python lint/format tool here — no black, isort, or flake8. Its defaults are usually enough; the one common addition is `[tool.ruff.lint] extend-select = ["I"]` for import sorting. Don't configure more rules than the project asked for.

## justfile

Script- and library-shaped uv projects get **no justfile** — bare `uv run pytest`, `uv run ruff check` is enough. Add one only when the project grows real surface (multiple entry points, a `ci` gate); that's app-shaped, so follow the recipe naming in `reference/bun.md` (`install`/`dev`/`format`/`lint`/`check`/`test`/`ci`).
