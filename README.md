# Skills

These tool-agnostic skills are shared across coding agents on this machine,
including Claude Code and pi. They live under `.agents/` because they are meant
to persist when switching agents, unlike `.claude/` or `.codex/`, which hold
ephemeral, tool-specific scratch data.

## Convention

Each skill is a directory under `skills/`:

```
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

## What's here

- **justfile**: Covers recipe interfaces, verification gates, execution,
  environment handling, safety, portability, and modularization.
- **ffmpeg**: Covers this machine's hardware encoder choice (QSV/Arc iGPU), the
  proven AV1/Opus command line, and known Windows path gotchas.
- **browser**: Covers driving Chrome or Edge with `bunx chrome-devtools`,
  attaching to an open browser, failure modes, and a socket client for scripts.
- **oxfmt**: Covers oxfmt configuration, ignores, migration from Prettier, and
  Zed integration.
- **skill-creator**: Creates, improves, evaluates, and benchmarks agent skills.

Policy files, such as version control and project setup, live under `rules/`.
`~/.agents/AGENTS.md` indexes the general rules with their loading conditions,
and `rules/project-setup.md` indexes the per-tool setup rules.

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

For example: `feat: prefer mapped justfile dependencies`.

## Using an existing skill from another agent tool

Link skills into each agent's skill-discovery directory instead of copying them,
so the files here remain the single source of truth. Prefer symbolic links; use
junctions only as a fallback when symbolic links are not practical. For example:

```
ln -s ~/.agents/skills/browser ~/.claude/skills/browser
```

## Adding a new skill

1. Create `skills/<name>/SKILL.md` with the frontmatter above.
2. Add `reference/*.md` files if the skill has detail worth deferring.
3. Symlink it from each agent tool's skill-lookup directory, such as
   `~/.claude/skills/<name>` for Claude Code.
