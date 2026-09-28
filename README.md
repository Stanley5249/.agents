# Skills

These tool-agnostic skills are shared across coding agents on this machine,
including Claude Code and pi. They live under `.agents/` because they are meant
to persist when switching agents, unlike `.claude/` or `.codex/`, which hold
ephemeral, tool-specific scratch data.

## Convention

Each skill is a directory:

```
<name>/
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

`description` is a concise summary with a soft discovery condition. Put exact
loading conditions in `~/.agents/AGENTS.md` and the actual instructions in the
skill body.

Load skills lazily. Do not preload a skill at the start of a conversation merely
because it is available. Read it only when the current task requires it,
immediately before its first use.

If a skill contains enough detail that loading all of it upfront would waste
context, move the supporting details into `reference/*.md` files. Have
`SKILL.md` point to them by name, such as in a decision tree or lookup table, so
an agent reads only the file it needs instead of the entire skill upfront.

## What's here

- **cookie**: Project-setup index for package managers, CI, repository metadata,
  and agent conventions. Its details are split into focused files under
  `reference/`.
- **justfile**: Covers recipe interfaces, verification gates, execution,
  environment handling, safety, portability, and modularization.
- **version-control**: Covers ignore decisions, commit and amendment practices,
  Conventional Commit messages, branching practices, and optional Git tools.
- **windows-shell**: Covers efficient Git Bash and PowerShell usage on Windows,
  including syntax differences, path handling, batching, and output control.
- **ffmpeg**: Covers this machine's hardware encoder choice (QSV/Arc iGPU), the
  proven AV1/Opus command line, and known Windows path gotchas.
- **skill-creator**: Creates, improves, evaluates, and benchmarks agent skills.

## Version control

Use unscoped Conventional Commit subjects because this repository has no
distinct package scopes. For example: `docs: clarify commit boundaries`.

Link skills into each agent's skill-discovery directory instead of copying them.
Prefer symbolic links; use junctions only as a fallback when symbolic links are
not practical. For instruction files with an import mechanism, such as Claude's
`@AGENTS.md` syntax, prefer an import over a symlink. The files here are the
source of truth.

## Using an existing skill from another agent tool

Create a symlink from that tool's skill-lookup directory into this one. For
example:

```
ln -s ~/.agents/skills/cookie ~/.claude/skills/cookie
```

Point to the skill directory here instead of copying it so that it remains the
single source of truth.

## Adding a new skill

1. Create `<name>/SKILL.md` here with the frontmatter above.
2. Add `reference/*.md` files if the skill has detail worth deferring.
3. Symlink it from each agent tool's skill-lookup directory, such as
   `~/.claude/skills/<name>` for Claude Code.
