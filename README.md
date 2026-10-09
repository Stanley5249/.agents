# Agents

Shared instructions, rules, skills, and reusable prompts for coding agents.

## Installation

Clone this repository from the home directory:

```sh
git clone https://github.com/Stanley5249/.agents.git
```

## Contents

- [`AGENTS.md`](AGENTS.md): shared instructions and the index of applicable
  rules.
- [`rules/`](rules/): guidance loaded for specific activities.
- [`skills/`](skills/): skills with a `SKILL.md` entry point and optional
  supporting files.
- [`prompts/`](prompts/): reusable Markdown prompts. Each file defines its
  purpose and usage.

## Usage

### Instructions

Connect your agent's global instruction file to `AGENTS.md` using its supported
import or symlink mechanism.

### Skills

Pi and Codex discover `~/.agents/skills/` automatically. For Claude Code, link
selected skills:

```sh
ln -s ~/.agents/skills/browser ~/.claude/skills/browser
```

### Prompts

Any agent can follow files in `prompts/`. To expose them as Pi commands, add to
`~/.pi/agent/settings.json`, preserving existing settings and prompt paths:

```json
{
  "prompts": ["~/.agents/prompts"]
}
```

Run `/reload`, then type `/` to find available prompt commands.

## Contributing

See [CONTRIBUTING.md](CONTRIBUTING.md) for commit conventions.

## License

[MIT](LICENSE)
