# Agents

Shared instructions, rules, and skills for coding agents.

## Installation

Clone this repository from the home directory:

```sh
git clone https://github.com/Stanley5249/.agents.git
```

## Contents

- [`AGENTS.md`](AGENTS.md): shared instructions and the index of applicable rules.
- [`rules/`](rules/): guidance loaded for specific activities.
- [`skills/`](skills/): skills with a `SKILL.md` entry point and optional supporting files.
- [`docs/ponytail.md`](docs/ponytail.md): notes on the adapted upstream work, Ponytail.
- [`docs/decisions.md`](docs/decisions.md): deliberate rule decisions to read before reviewing rules.

## Usage

### Instructions

Connect your agent's global instruction file to `AGENTS.md` using its supported import or symlink mechanism.

### Rules

`AGENTS.md` defines when agents should load each rule and which files an activity requires. Keep rules focused on one topic, and put loading conditions in `AGENTS.md` instead of cross-rule references.

### Skills

Run `just link` to choose local skills for Pi, Codex, and Claude Code. Requires [just](https://just.systems/) and [Bun](https://bun.sh/).

Agents pass explicit skill names and `--yes` to `just link`. For third-party skills, use [Vercel Skills](https://github.com/vercel-labs/skills) non-interactively with explicit skills, target agents, and scope.

Preview broken Claude skill links with `bun scripts/clean-skill-links.ts`. Add `--apply` to remove them.

## Contributing

See [CONTRIBUTING.md](CONTRIBUTING.md) for commit conventions.

## License

[MIT](LICENSE). Parts of [`rules/code.md`](rules/code.md) and [`quality-review`](skills/quality-review/SKILL.md) are based on [Ponytail](https://github.com/DietrichGebert/ponytail/tree/2961b52fc1fe6a5a87c7a959a79512e5c2f3ffe5) by DietrichGebert, also under MIT. See [`docs/ponytail.md`](docs/ponytail.md) for what was adapted.
