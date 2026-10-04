# Agents

This repository holds the global `AGENTS.md`, rules, and tool-agnostic skills
shared across coding agents on this machine, including Claude Code and pi. They
live under `.agents/` because they are meant to persist when switching agents,
unlike `.claude/` or `.codex/`, which hold ephemeral, tool-specific scratch
data.

## Installation

Clone this repository from the home directory:

```sh
git clone https://github.com/Stanley5249/.agents.git
```

For Claude Code, import `AGENTS.md` from `~/.claude/CLAUDE.md`:

```markdown
@~/.agents/AGENTS.md
```

## Skills

Each skill is a directory under `skills/`:

```text
skills/<name>/
  SKILL.md          # entry point
  reference/*.md    # optional, loaded on demand
```

`SKILL.md` starts with frontmatter:

```yaml
---
name: <name>
description: <what it does and when it may be useful>
---
```

`description` states what the skill does and when to load it. The harness
injects it into each session, so nothing else needs to index skills.

Keep each skill self-contained: it depends only on files inside its own
directory, so any agent can load it alone. Files in `rules/` may refer to each
other.

Load skills lazily. Do not preload a skill at the start of a conversation merely
because it is available. Read it only when the current task requires it,
immediately before its first use.

If a skill contains enough detail that loading all of it upfront would waste
context, move the supporting details into `reference/*.md` files. Have
`SKILL.md` point to them by name, such as in a decision tree or lookup table, so
an agent reads only the file it needs instead of the entire skill upfront.

## Rules

Policy files, such as version control and project setup, live under `rules/`.
`~/.agents/AGENTS.md` indexes every rule with its loading condition.

`rules/` stays flat even past eight files. Each file is short and loaded alone
by its index entry, so a subdirectory would add path depth without making
anything easier to find.

## Version control

Use unscoped Conventional Commit subjects. This repository is shared by all
projects and every change concerns skills or rules, so a scope adds no
information. This overrides the `agents` scope in the version-control rule.

Skills are instructions that agents execute, so type skill changes by their
effect on agent behavior:

- `feat`: add, change, or remove guidance.
- `fix`: correct wrong or misleading guidance.
- `refactor`: restructure without changing behavior, such as moving a reference.
- `style`: change only wording, headings, or formatting.
- `docs`: change this README.
- `build`: change repository tooling, such as formatter or editor settings.

For example: `feat: prefer mapped justfile dependencies`.

## Using an existing skill from another agent tool

Link skills into each agent's skill-discovery directory instead of copying them,
so the files here remain the single source of truth. For example:

```sh
ln -s "$HOME/.agents/skills/browser" "$HOME/.claude/skills/browser"
```

## License

[MIT](LICENSE)
