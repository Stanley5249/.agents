# Contributing

## Checks

Run `just check` before committing. It checks formatting, validates skill metadata and Markdown links, and runs the script tests.

## Instructions

- `AGENTS.md` loads in every session of every agent. Keep it to what applies to most tasks and what an agent cannot infer from code or standard tooling. Put topic knowledge in a skill whose description names when to use it.
- When a rule must hold without exceptions, prefer a check in `just check`, a formatter, or harness configuration over an instruction.
- Keep the reason next to a rule, because an agent follows a rule better when it knows why.
- Drop lines an agent cannot act on, such as "keep documents concise", and replace a vague trigger with an observable one. Judgment words such as "non-trivial" and "somewhat over" are deliberate, so do not replace them with a number.
- Verify each review finding before editing. Small models such as Haiku invent numeric thresholds and flag deliberate judgment words.

## Skills

- A skill references its own supporting files by relative path, and other skills by name.
- Keep invocation settings in sync across harnesses. For a manual-only skill, set `disable-model-invocation: true` in `SKILL.md` for Pi and Claude Code, and `policy.allow_implicit_invocation: false` in `agents/openai.yaml` for Codex. For implicit invocation, omit both. `scripts/validate-skills.ts` checks this.

## Scripts

`scripts/sysinfo.py` holds only facts that take several platform-specific commands to collect, such as installer paths, global packages, Dev Drives, and the preferred link type, plus a minimal `machine` overview for harnesses that do not report the platform. A fact one shell command answers, such as a tool version, stays out.

## Commit conventions

Use unscoped Conventional Commit subjects, because the repository itself is the scope.

Skills and instructions are text that agents execute, so type their changes by the effect on agent behavior:

- `feat`: add, change, or remove guidance.
- `fix`: correct wrong or misleading guidance.
- `refactor`: restructure without changing behavior, such as moving a reference.
- `style`: change only wording, headings, or formatting.
- `docs`: change repository documentation.
- `build`: change repository tooling, such as formatter or editor settings.

For example: `feat: prefer mapped justfile dependencies`.
