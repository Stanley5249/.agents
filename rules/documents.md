# Documents

## Where things go

| File          | Reader      |
| ------------- | ----------- |
| `README.md`   | humans      |
| `AGENTS.md`   | agents      |
| `docs/*.md`   | humans      |
| code comments | maintainers |
| changelog     | users       |

- State each fact in one place and link to it elsewhere. Point to the command
  surface, such as `justfile`, instead of copying commands into prose.

<!--we shuold move changelog to ci-->

- Generate the changelog with `git-cliff` from Conventional Commits for
  published projects. Unpublished projects keep no changelog.

## Core rules

- Minimal and concise.
- Single source of truth. No duplication.
- Ask for approval before adding sections to or restructuring `README.md`,
  `AGENTS.md`, or other documents. Keep existing content accurate without
  asking.

## README

Start with the smallest shape appropriate to the audience.

- Title: with an optional one-line description.
- Installation: optional, user-facing. How to install the project.
- Requirements: developer-facing. Link each tool to its installation guide.
- Commands: point to a command runner such as `justfile` when present, and start
  with the essential ones only.
- Documents: links to hosted docs when present, plus relative paths to local
  docs.
- License: required for published projects. Ask the user to choose one.

Add more sections when appropriate, such as:

- badges for release, documentation, CI, coverage, and license
- usage
- comparison
- FAQ
- references

## Agent instruction files

- In a monorepo, move subproject rules to `<subproject>/AGENTS.md` when they
  start to fill the root `AGENTS.md`.
- Don't repeat the global instructions.
- Add personal workflow or preferences only when the user asks.

## Document locations

- When the project has no document location, start at `docs/`. Otherwise follow
  the project convention.

## Markdown

- Write headings in sentence case. Prefer noun phrases.
- Give every code fence a language tag.
