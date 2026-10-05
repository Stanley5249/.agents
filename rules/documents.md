# Documents

## Core rules

- Keep documents minimal and concise.
- State each fact once, in a single source of truth.
- When a hand-maintained document grows beyond 400 lines, consider splitting it
  into focused documents. If keeping it together is clearer, say why at its top.
- Ask for approval before adding sections to or restructuring `README.md`,
  `AGENTS.md`, or other documents. Keep existing content accurate without
  asking.

## README

Start with the smallest shape appropriate to the audience.

- Title: with an optional one-line description.
- Installation: optional, user-facing. How to install the project.
- Requirements: developer-facing. Link each tool to its installation guide.
- Commands: point to a command runner such as `justfile` when present instead of
  copying its commands, and start with the essential ones only.
- Documents: links to hosted docs when present, plus relative paths to local
  docs.

Add more sections when appropriate, such as:

- badges for release, documentation, CI, coverage, and license
- usage
- comparison
- FAQ
- references

## Agent instruction files

- In a monorepo, move subproject rules to `<subproject>/AGENTS.md` when they
  start to fill the root `AGENTS.md`.
- Refer to the global instructions instead of repeating them.
- Add personal workflow or preferences only when the user asks.

## Document locations

- When the project has no document location, start at `docs/`. Otherwise follow
  the project convention.
- Only the index, `README.md` or `AGENTS.md`, links to docs. Docs do not link to
  each other, and code does not link to docs by default.
