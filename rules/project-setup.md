# Project setup

Repository-wide setup and migration conventions.

## Formatting and validation

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

- Configure generated lockfiles to preserve their format and avoid automatic
  merges:

  ```gitattributes
  <lockfile> merge=binary linguist-language=<LANG> linguist-generated=true -diff
  ```

  This prevents corrupted lockfiles from automatic 3-way git merges, flags them
  as generated on GitHub, and collapses noisy lockfile diffs.

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
- Commit each accepted change separately, such as a formatter switch, the
  reformat it causes, and a new `.gitattributes`.
- After changing line-ending rules in `.gitattributes`, run
  `git add --renormalize .` and commit the result on its own.
