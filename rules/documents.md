# Documents

## Where things go

| File          | Reader      | Holds                                 |
| ------------- | ----------- | ------------------------------------- |
| `README.md`   | humans      | what the project is and how to run it |
| `AGENTS.md`   | agents      | conventions and commands agents need  |
| `docs/*.md`   | humans      | one focused topic per file            |
| code comments | maintainers | why the code is the way it is         |
| changelog     | users       | release notes generated from commits  |

- State each fact in one place and link to it elsewhere. Point to the command
  surface, such as `just --list`, instead of copying commands into prose.
- Generate the changelog with `git-cliff` from Conventional Commits for
  published projects. Unpublished projects keep no changelog.

## README

Choose the smallest shape appropriate to the audience.

A personal or work-in-progress project normally has no badges and may omit the
README when `AGENTS.md` is enough. When present, use:

- A title and optional one-line description.
- Setup or command instructions through the project's command surface.
- Domain-specific sections only for behavior that is not evident from the code.
- A documentation section linking to focused files under `docs/`.
- A status section while major work remains.

A published library should additionally provide release, documentation, CI,
coverage, and license badges; runnable basic usage; comparison or FAQ material;
and an explicit license section.

## Agent instruction files

- `AGENTS.md` is the source of truth for agent instructions.
- Prefer symbolic links for shared skills, data directories, and other paths
  without an import mechanism.
- In a monorepo, keep the root `AGENTS.md` as a thin index directing agents to
  nested files such as `catalog/AGENTS.md` and `web/AGENTS.md`. Do not duplicate
  subproject details at the root.
- Split an instruction file only when it becomes hard to scan. Put durable topic
  files under `.agents/rules/`, one topic per file, and reference them from the
  root.
- Keep durable plans and shared skills under `.agents/`; name the durable
  backlog itself `.agents/AGENTS.md`, because that filename gets the same
  automatic read/injection a nested `AGENTS.md` gets, instead of needing an
  explicit instruction to open it every time. Treat `.claude/` and `.codex/` as
  tool-specific scratch or session state.

## docs/

- Keep one topic per file and name the file after its topic.
- Link each file from the README's documentation section.
- Record the reason for a non-obvious design decision in the doc for its topic.

## Code comments

- Explain why the code is the way it is. The code already says what it does.
- Give public APIs doc comments, such as rustdoc, docstrings, or JSDoc. Write
  examples in them as doctests where the language supports it.
- When a file stays over the 400-line threshold, record the reason in its
  file-level comment.

## Markdown

- Format with oxfmt at a print width of 80 with `proseWrap: "always"`.
- Write headings in sentence case.
- Give every code fence a language tag.
- Use relative links inside the repository, and link to files rather than line
  numbers, because line numbers go stale.
