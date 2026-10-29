# README and agent instruction files

## README

Start with the smallest shape appropriate to the audience:

- Title: with an optional one-line description.
- Installation: optional, user-facing. How to install the project.
- Requirements: developer-facing. Link each tool to its installation guide.
- Commands: point to a command runner such as `justfile` when present instead of copying its commands, and start with the essential ones only.
- Documents: links to hosted docs when present, plus relative paths to local docs.

Add other sections when the project needs them, such as badges for release, documentation, CI, coverage, and license, usage, comparison, FAQ, and references.

## Agent instruction files

- Keep the project's `AGENTS.md` to what every task needs and an agent cannot infer from the code, such as commands, constraints, and where docs live. Put detailed or rarely needed knowledge in docs that `AGENTS.md` points to, or in a project skill.
- In a monorepo, move subproject rules to `<subproject>/AGENTS.md` when they start to fill the root `AGENTS.md`.
- Refer to the global instructions instead of repeating them.

## Markdown

- When the project has no document location, start at `docs/`. Otherwise follow the project convention.
- Link to a stable target, such as a relative path or the latest page of a library's docs. Pin a commit SHA only to cite that exact version as evidence.
- Search for anchor links to a heading in the same commit that renames it.
- Use a tight list, with no blank lines, unless most items hold paragraphs or code blocks.
- Keep table cells to a few words. Replace a table with a sentence in a cell or a row longer than 80 characters with sections or a `**label**: text` list.
