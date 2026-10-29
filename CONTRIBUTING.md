# Contributing

Run `just check` before committing. It checks formatting, validates skill metadata and Markdown links, and runs the script tests.

## Instructions

- `AGENTS.md` loads in every session of every agent, so keep only what applies to most tasks and what an agent cannot infer or would otherwise rediscover. Put topic knowledge in a skill whose description says when to use it.
- Delete a line a current model already follows by default, rather than moving it elsewhere. Keep the reason next to a rule that stays.
- Prefer a check in `just check`, a formatter, or harness configuration over an instruction for a rule that needs no exceptions.
- Verify each review finding before editing, because small reviewers such as Haiku invent numeric thresholds, flag deliberate judgment words such as "non-trivial", and ask to restore deleted defaults.

## Skills

- A skill references its own files by relative path, and other skills by name.
- For a manual-only skill, set `disable-model-invocation: true` in `SKILL.md` for Claude Code and Pi, and `policy.allow_implicit_invocation: false` in `agents/openai.yaml` for Codex. `scripts/validate-skills.ts` checks that both agree.

## Scripts

`scripts/sysinfo.py` holds only facts that take several platform-specific commands to collect. A fact one shell command answers, such as a tool version, stays out.

## Commit conventions

Use unscoped Conventional Commit subjects, because the repository itself is the scope. Type a change to skills or instructions by its effect on agent behavior:

- `feat`: add, change, or remove guidance.
- `fix`: correct wrong or misleading guidance.
- `refactor`: restructure without changing behavior, such as moving a reference.
- `style`: change only wording, headings, or formatting.
- `docs`: change repository documentation.
- `build`: change repository tooling, such as formatter or editor settings.
