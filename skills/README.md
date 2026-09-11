# skills

Tool-agnostic skills shared across coding agents on this machine (Claude Code,
pi, others). Lives under `.agents/` because it's meant to survive a switch of
agent, unlike `.claude/` or `.codex/`, which are ephemeral per-tool scratch.

## Convention

Each skill is a directory:

```
<name>/
  SKILL.md          # entry point
  reference/*.md     # optional, loaded on demand
```

`SKILL.md` starts with frontmatter:

```yaml
---
name: <name>
description: <what it does and when it may be useful>
---
```

`description` is a concise summary with a soft discovery condition. Put exact
loading conditions in `~/.agents/AGENTS.md`, while the skill body holds the
actual instructions.

If a skill has enough detail that dumping it all upfront would waste context,
split the long tail into `reference/*.md` files and have `SKILL.md` point to
them by name (a decision tree, a lookup table) so an agent reads only the
file it needs instead of the whole skill upfront.

## What's here

- **cookie** — project-setup index for package managers, justfiles, CI/hooks,
  repository metadata, and agent conventions. Details are split into focused
  files under `reference/`.
- **version-control** covers repository safety, commit and branch practice,
  Conventional Commits, and optional message enforcement.
  Reference files provide fallback and managed-hook configurations.
- **windows-shell** — efficient Git Bash and PowerShell usage on Windows,
  including syntax differences, path handling, batching, and output control.
- **bibo** — communication style, editing behavior, and ongoing development
  preferences such as when to consider modularizing large files or crowded
  modules.
- **ffmpeg** — this machine's hardware encoder choice (QSV/Arc iGPU), the
  proven AV1/Opus command line, and known Windows path gotchas.

Link skills into each agent's skill-discovery directory instead of copying
them. Prefer symbolic links; use junctions only as a fallback when symbolic
links are not practical. For instruction files with an import mechanism, such
as Claude's `@AGENTS.md` syntax, prefer an import over a symlink. The files here
are the source of truth.

## Using an existing skill from another agent tool

Symlink from that tool's own skill-lookup directory into this one, e.g.:

```
ln -s ~/.agents/skills/cookie ~/.claude/skills/cookie
```

Point at the skill directory here, don't copy it — one source of truth.

## Adding a new skill

1. Create `<name>/SKILL.md` here, with the frontmatter above.
2. Add `reference/*.md` files if the skill has detail worth deferring.
3. Symlink it from wherever each agent tool looks for skills, e.g.
   `~/.claude/skills/<name>` for Claude Code.
