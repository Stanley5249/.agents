---
name: python
description: Python project conventions for uv, pyproject layout, build backend, ruff, pyrefly, and justfile recipes. Use when writing, reviewing, or setting up Python code or a uv project.
---

# Python

Use uv for packages and the project's `.venv`, and add packages with `uv add`. Use the latest syntax that the version in `.python-version` or `requires-python` supports.

## Layout

- Keep `pyproject.toml`, `uv.lock`, and a pinned `.python-version` at the repository root.
- In `.gitattributes`, configure `uv.lock`:

  ```gitattributes
  uv.lock merge=binary linguist-language=TOML linguist-generated=true -diff
  ```

- Build a packaged library with uv's native backend:

  ```toml
  [build-system]
  requires = ["uv_build>=0.12.0"]
  build-backend = "uv_build"
  ```

- For an application or scripts that publish no wheels, set `package = false` under `[tool.uv]`.

## Lint, format, and type checking

Use `ruff` as the only linter and formatter, starting with all rules, Google-style docstrings, and LF output on Windows, and type-check with pyrefly's strict preset:

```toml
[tool.ruff.lint]
select = ["ALL"]
ignore = [
  "COM812", # conflicts with the formatter
]
[tool.ruff.lint.pydocstyle]
convention = "google"

[tool.ruff.format]
line-ending = "lf"

[tool.pyrefly]
preset = "strict"
```

## Justfile

Run every tool through `uv run --locked`, so a stale lockfile fails instead of being updated, and `ci` needs no separate `lock-check` recipe. Typical mappings are `fmt` and the format step of `check` to one `_fmt-ruff` helper over `ruff format`, `lint` to `ruff check`, `typecheck` to `pyrefly check`, and `test` to `pytest`.
