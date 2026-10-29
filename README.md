# Agents

Shared instructions and skills for Claude Code, Codex, and Pi.

## Installation

Clone this repository from the home directory, so it lands at `~/.agents`:

```sh
git clone https://github.com/Stanley5249/.agents.git
```

## Contents

- [`AGENTS.md`](AGENTS.md): global instructions that every agent loads in every session.
- [`skills/`](skills/): skills with a `SKILL.md` entry point and optional supporting files. Language and project-setup conventions live here and load when their description matches the task.
- [`scripts/`](scripts/): `sysinfo.py` for machine facts, and helpers for skill links and validation.

## Usage

### Instructions

Connect each agent's global instruction file to `AGENTS.md`:

- Claude Code: `~/.claude/CLAUDE.md` holds the line `@~/.agents/AGENTS.md`.
- Codex: symlink `~/.codex/AGENTS.md` to `~/.agents/AGENTS.md`.
- Pi: symlink `~/.pi/agent/AGENTS.md` to `~/.agents/AGENTS.md`.

### Skills

Codex and Pi read `~/.agents/skills` directly, so the skills work there without a link. Claude Code reads `~/.claude/skills`, so run `just link` to link the skills there. Requires [just](https://just.systems/) and [Bun](https://bun.sh/).

Agents pass explicit skill names and `--yes` to `just link`. For third-party skills, use [Vercel Skills](https://github.com/vercel-labs/skills) non-interactively with explicit skills, target agents, and scope.

Preview broken Claude skill links with `bun scripts/clean-skill-links.ts`. Add `--apply` to remove them.

## Contributing

See [CONTRIBUTING.md](CONTRIBUTING.md).

## License

[MIT](LICENSE). Parts of the Code section in [`AGENTS.md`](AGENTS.md) and the [`code-design`](skills/code-design/SKILL.md) and [`quality-review`](skills/quality-review/SKILL.md) skills are based on [Ponytail](https://github.com/DietrichGebert/ponytail/tree/2961b52fc1fe6a5a87c7a959a79512e5c2f3ffe5) by DietrichGebert, also under MIT.
