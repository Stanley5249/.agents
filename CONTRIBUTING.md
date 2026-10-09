# Contributing

## Formatting check

Before committing, run `bunx oxfmt --check` from the repository root.

## Commit conventions

Use unscoped Conventional Commit subjects. This repository shares agent
resources across projects, so the repository itself provides the scope. This
overrides the `agents` scope in `rules/version-control.md`.

Skills are instructions that agents execute, so type skill changes by their
effect on agent behavior:

- `feat`: add, change, or remove guidance.
- `fix`: correct wrong or misleading guidance.
- `refactor`: restructure without changing behavior, such as moving a reference.
- `style`: change only wording, headings, or formatting.
- `docs`: change repository documentation.
- `build`: change repository tooling, such as formatter or editor settings.

For example: `feat: prefer mapped justfile dependencies`.
