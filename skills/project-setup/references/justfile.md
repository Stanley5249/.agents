# Justfile

Conventions for writing every justfile. The [Just README](https://github.com/casey/just/blob/master/README.md) covers the syntax.

## Recipes

Give every project a justfile as its command surface for recurring tasks. Docs may run other commands directly.

- Always `set default-list`, and document each public recipe so it appears in `just --list`.
- Make unsuffixed recipes cover the primary language, and add `-all` variants that also cover the other languages and slow test suites. Keep recipes that cover only the other languages private, such as `_lint-py`, and keep a scoped recipe public only when docs or messages refer to it, such as `test-e2e`.
- Prefer native just syntax, such as functions, lists, and dependencies, over shell commands. Set a variable with `[env("NAME", "value")]` instead of a shell assignment, and change directory with `[working-directory("path")]` instead of `cd`. A `[script]` recipe or shell script is the last resort, with its comments above the recipe instead of inside the body.
- Run a recipe over a known list with mapped dependencies, not a shell loop. Put the per-item step in a helper. This needs `set unstable`, `set lists`, and a `minimum-version`:

  ```just
  set minimum-version := "1.53.0"
  set unstable
  set lists

  documents := ["resume.typ", "essay.typ"]

  _lint doc:
      tinymist lint "{{ doc }}"

  [parallel]
  lint: *(_lint *documents)
  ```

- Expose a trailing `*args` wherever a recipe wraps one tool, and forward it as `{{ args }}`, which works in every shell, instead of `quote(args)` or `-CommandWithArgs`. An aggregate recipe takes no arguments; pass arguments to the single-tool recipe instead. When passing arguments on the command line, run one recipe per `just` command, because a variadic parameter takes the words after it as arguments, including later recipe names.
- Quote a scalar `{{ parameter }}` with double quotes, which both PowerShell and `sh` accept.
- When the recipe itself needs an option, declare it with `[arg("name", long, help="...")]` and a default, alongside `*args`.
- Name a private helper `_name`. Use `[private]` only when a public-looking name reads better.
- Name a custom recipe with a verb first, such as `link` or `gen-docs`, and a helper as `_<verb>-<object>`, such as `_fmt-just`. The role names below keep their established forms.
- Give each formatter one `_fmt-<tool> *args` helper. `fmt` calls the helpers, and `check` calls them with each tool's check flag. Both always include `_fmt-just`, which runs `just --fmt`:

  ```just
  [parallel]
  fmt: _fmt-tombi _fmt-just

  [parallel]
  check: (_fmt-tombi "--check") (_fmt-just "--check") lint

  _fmt-tombi *args:
      tombi format --quiet {{ args }} .

  _fmt-just *args:
      just --fmt {{ args }}
  ```

- Mark a recipe `[parallel]` when its jobs ignore order, write no shared output, and there are at least two, without timing the jobs first. Pass each tool its quiet flag, not an environment variable, so the output does not interleave.
- Add `[confirm("...")]` to irreversible work, such as a deploy, release, or migration, including deleting regenerable files. A recipe that `check` or `ci` depends on never confirms, because a gate must run unattended; `--yes` is for automation that runs a confirming recipe on purpose.
- Guard `set shell` and shell-specific recipes with `[windows]` or `[unix]`. On Windows, select PowerShell explicitly:

  ```just
  [windows]
  set shell := ["pwsh", "-NoLogo", "-NoProfile", "-Command"]
  ```

- Use these names where their roles apply: `install`, `build`, `dev`, `prod`, `fmt`, `fix`, `typecheck`, `lint`, `check`, `test`, and `ci`. Prefer `dev` and `prod` over `start` and `run`.
  - `fmt` rewrites sources by formatting only, and `fix` runs `fmt`, then the linters' automatic fixes.
  - `typecheck`, `lint`, `check`, and `test` preserve sources. `lint` treats warnings as errors where the tool supports it.
  - `check` is the fast local gate that runs format checks and linters, and `ci` composes `check` and `test`, plus `build` when the project needs it.
