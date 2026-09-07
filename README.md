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
description: <what it does and when to use it>
---
```

`description` is what an agent matches against to auto-trigger the skill —
write it as a trigger condition ("use when..."), not a summary. The body
holds the actual instructions.

If a skill has enough detail that dumping it all upfront would waste context,
split the long tail into `reference/*.md` files and have `SKILL.md` point to
them by name (a decision tree, a lookup table) so an agent reads only the
file it needs instead of the whole skill upfront.

## What's here

- **cookie** — scaffolding/audit conventions for a project's package manager,
  lint/formatter choice, justfile surface, and CI/hook wiring. Reference
  files per package manager: `cargo.md`, `uv.md`, `bun.md`, `pixi.md`.
- **commit-message** — this machine's commit message convention (Conventional
  Commits, concise body) and how to enforce it with a hook. Reference files:
  `commit-msg-hook.sh` (zero-dependency fallback), `pre-commit-config.yaml`
  and `prek.toml` (preferred enforcement path).
- **git-bash** — token-efficient Git Bash usage on Windows: MSYS path quirks,
  batching/silencing commands.
- **pwsh** — same idea for PowerShell: syntax traps, batching, quiet flags.
- **bibo** — conversation tone and formatting: reading level, structure,
  when to edit a file directly vs. preview first.

`cookie`, `commit-message`, and `bibo` are all symlinked into
`~/.claude/skills/` so Claude Code picks them up; the files here are the
source of truth, not a copy.

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
