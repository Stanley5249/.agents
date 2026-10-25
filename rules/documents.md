# Documents

## Core rules

- State each fact once, in a single source of truth. Point to code and manifests for facts that change, such as versions, counts, and file lists.
- When a hand-maintained document grows beyond 400 lines, split it into focused documents, or say at its top why it stays whole.
- Ask for approval before adding sections to or restructuring `README.md`, `AGENTS.md`, or other documents. Keep existing content accurate without asking.

## README

Start with the smallest shape appropriate to the audience.

- Title: with an optional one-line description.
- Installation: optional, user-facing. How to install the project.
- Requirements: developer-facing. Link each tool to its installation guide.
- Commands: point to a command runner such as `justfile` when present instead of copying its commands, and start with the essential ones only.
- Documents: links to hosted docs when present, plus relative paths to local docs.

Propose more sections for approval when appropriate, such as:

- badges for release, documentation, CI, coverage, and license
- usage
- comparison
- FAQ
- references

## Agent instruction files

- Keep the project's `AGENTS.md` as an index that every task loads. List each doc with the facts it holds and when to read it, then the few rules every task needs. Put detailed rules in docs that the index points to.
- In a monorepo, move subproject rules to `<subproject>/AGENTS.md` when they start to fill the root `AGENTS.md`.
- Refer to the global instructions instead of repeating them.
- Add personal workflow or preferences only when the user asks.

## Markdown

- Keep proper nouns, package names, and code in their own case in headings.
- Use a tight list, with no blank lines, unless most items hold paragraphs or code blocks.
- Write each paragraph or list item on one line. Never wrap by hand, because a one-word edit then stays on one line.
- Link to a stable target, such as a relative path or the latest page of a library's docs. Pin a commit SHA only to cite that exact version as evidence.
- Search for anchor links to a heading in the same commit that renames it.
- Keep table cells to a few words. In a review, flag a table with a sentence in a cell or a row longer than 80 characters, and suggest sections or a `**label**: text` list.

## Document locations

- When the project has no document location, start at `docs/`. Otherwise follow the project convention.
- Only the index, `README.md` or `AGENTS.md`, links to docs. A doc that needs another one names it in prose only when the reader needs it to finish the task, and code comments explain themselves without doc links by default.
