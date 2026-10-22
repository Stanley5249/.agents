# Contributing

## Formatting check

Before committing, run `just check` from the repository root.

## Rule loading

`AGENTS.md` indexes `rules/` and owns all loading conditions. Rule files hold
only topic content, without loading conditions or references to other rules.

## Skills

When changing this repository's skills, keep invocation settings in sync across
harnesses. For manual-only skills, set:

- `disable-model-invocation: true` in `SKILL.md` for Pi and Claude Code.
- `policy.allow_implicit_invocation: false` in `agents/openai.yaml` for Codex.

For implicit invocation, omit both settings. Check both when changing a skill,
and preserve unrelated metadata.

## Commit conventions

Use unscoped Conventional Commit subjects. This repository shares agent
resources across projects, so the repository itself provides the scope. This
overrides the `agents` scope in `rules/workflow.md`.

Skills are instructions that agents execute, so type skill changes by their
effect on agent behavior:

- `feat`: add, change, or remove guidance.
- `fix`: correct wrong or misleading guidance.
- `refactor`: restructure without changing behavior, such as moving a reference.
- `style`: change only wording, headings, or formatting.
- `docs`: change repository documentation.
- `build`: change repository tooling, such as formatter or editor settings.

For example: `feat: prefer mapped justfile dependencies`.
