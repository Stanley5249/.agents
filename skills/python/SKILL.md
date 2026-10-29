---
name: python
description: Python project conventions for uv, pyproject layout, build backend, ruff, pyrefly, and justfile recipes. Use when writing, reviewing, or setting up Python code or a uv project.
---

# Python

Use uv for package management and virtual environments. Add packages with `uv add` and let uv manage the project's `.venv`.

## Code

Check the target Python version in `.python-version` or `requires-python` in `pyproject.toml` before writing code, and use the latest syntax that version supports.

## Layout

- Keep `pyproject.toml`, `uv.lock`, and a pinned `.python-version` at the repository root.
- In `.gitattributes`, configure `uv.lock`:

  ```gitattributes
  uv.lock merge=binary linguist-language=TOML linguist-generated=true -diff
  ```

- For packaged libraries, use uv's native build backend:

  ```toml
  [build-system]
  requires = ["uv_build>=0.12.0"]
  build-backend = "uv_build"
  ```

- For standalone applications or scripts that do not publish wheels, disable package building:

  ```toml
  [tool.uv]
  package = false
  ```

## Lint, format, and type checking

- Use `ruff` as the only linter and formatter for Python source. Start every project with all rules selected and Google-style docstrings:

  ```toml
  [tool.ruff.lint]
  select = ["ALL"]
  ignore = [
    "COM812", # conflicts with the formatter
  ]
  [tool.ruff.lint.pydocstyle]
  convention = "google"
  ```

- Keep LF line endings on Windows with ruff's format option:

  ```toml
  [tool.ruff.format]
  line-ending = "lf"
  ```

- Type-check with pyrefly's strict preset:

  ```toml
  [tool.pyrefly]
  preset = "strict"
  ```

## Justfile

Put commands in justfile recipes that invoke local executables through `uv run`. Typical mappings are `fmt` to `uv run ruff format`, the format step of `check` to `uv run --locked ruff format --check`, `lint` to `uv run --locked ruff check`, `typecheck` to `uv run --locked pyrefly check`, and `test` to `uv run --locked pytest`. Use `--locked` in validation recipes so a stale lockfile fails the check before uv can update it.

Add a `lock-check` recipe that runs `uv lock --check` and include it in `ci`.
