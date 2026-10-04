# Project setup

Detect the repository shape, then read:

- the language and environment rules that `~/.agents/AGENTS.md` indexes for it
- `documents.md` for README and `AGENTS.md`
- `zed.md` for editor settings

A project can combine multiple language rules, such as `rust.md` +
`javascript.md` for a desktop app or `rust.md` + `python.md` for a Rust core
with a Python harness. Heavy native or GPU dependencies add `pixi.md` as an
environment overlay.

## Language extensions

Language rules (`python.md`, `rust.md`, `javascript.md`) extend this setup. Each
rule defines:

- Manifests and pinned toolchain versions
- Lockfile git attributes and frozen lockfile checks
- Linter, formatter, and type-checker choices
- Language-specific workspace layout and test setup
- Base justfile recipes (`fmt`, `lint`, `typecheck`, `test`, `lock-check`)

## Formatting and validation

- Format JS, TS, CSS, HTML, JSON, YAML, and Markdown with oxfmt wherever those
  file types appear. Lint them as `javascript.md` describes.
- Format TOML files with `tombi` (`tombi.toml`) regardless of the package
  manager. It covers `Cargo.toml`, `pyproject.toml`, `pixi.toml`, and its own
  configuration file.
- Prefer the smallest setup that provides a clear local verification gate. Add
  release automation, team workflows, or hosted automation only when the project
  needs them.

## Repository metadata

### Git attributes

- Add `.gitattributes` with LF normalization at the repository root:

  ```gitattributes
  * text=auto eol=lf
  ```

- Append generated lockfile handling for each language or environment in use, as
  specified in the corresponding extension rule (`python.md`, `rust.md`,
  `javascript.md`, `pixi.md`):

  ```gitattributes
  <lockfile> merge=binary linguist-language=<LANG> linguist-generated=true -diff
  ```

  This prevents corrupted lockfiles from automatic 3-way git merges, flags them
  as generated on GitHub, and collapses noisy lockfile diffs. Extension rules
  contain only the concrete lockfile pattern; this section defines the
  rationale.

### Licenses

- Inspect upstream templates and dependency licenses first to confirm
  compatibility. Default to dual `LICENSE-APACHE` and `LICENSE-MIT` for Rust
  crates, and default to `LICENSE` with MIT for other projects.

## Workspace layout

- Keep the toolchain for a secondary language scoped to the subdirectory that
  needs it unless the whole workspace depends on it.

## Scaffolding

- Start from an existing project with a similar structure, and introduce a new
  pattern only for a stated reason.
- Set up the repository metadata before history accumulates.
- Add a justfile as `justfile.md` describes.
- Make the first commit with a Conventional Commit subject, such as
  `chore: first commit`.

## Migration

- Audit the repository against the core conventions, the repository metadata,
  and each rule file it needs. List each gap with its planned change.
- Show the list and ask which changes to apply. The user decides which existing
  conventions to replace.
- Work on a task branch, such as `chore/migrate-conventions`.
- Move the instructions in a project `CLAUDE.md` into `AGENTS.md`, merging them
  with what is already there, then delete `CLAUDE.md`, including one that only
  imports `@AGENTS.md`.
- Audit the justfile as `justfile.md` describes.
- Commit each accepted change separately, such as a formatter switch, the
  reformat it causes, and a new `.gitattributes`.
- After changing line-ending rules in `.gitattributes`, run
  `git add --renormalize .` and commit the result on its own.
