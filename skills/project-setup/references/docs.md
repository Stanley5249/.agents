# README and agent instruction files

## README

Start with the smallest shape the audience needs, and add sections such as badges, usage, or FAQ only when the project needs them:

- Title: with an optional one-line description.
- Installation: optional, user-facing.
- Requirements: developer-facing, linking each tool to its installation guide.
- Commands: point to the justfile instead of copying its commands.
- Documents: links to hosted docs, plus relative paths to local docs.

## Agent instruction files

- Keep a project's `AGENTS.md` to what an agent cannot infer from the code and would otherwise rediscover every session, such as the check commands, misleading code, and decisions made outside the repository. Leave out architecture and file layout.
- Move rules that need no exceptions into a check, a formatter, or harness configuration, and move rarely needed procedures into a project skill.
- In a monorepo, move subproject rules to `<subproject>/AGENTS.md` once they crowd the root file.
- Refer to the global instructions instead of repeating them.

## Markdown

- Put documents in `docs/` unless the project has another location.
- Link to a stable target, such as a relative path or the latest page of a library's docs. Pin a commit SHA only to cite that exact version.
- Use a tight list without blank lines unless most items hold paragraphs or code blocks.
- Keep table cells to a few words. Replace a table that needs a sentence in a cell with sections or a `label: text` list.
