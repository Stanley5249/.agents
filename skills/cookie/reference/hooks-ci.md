# hooks and CI

## CI gate

Prefer a local `just ci` merge gate for personal projects. Add hosted CI when a project is shared, publishes releases, or the user asks for it. Hosted CI should call the same underlying checks as the local gate instead of defining a second workflow.

## Hooks

Projects carry no commit hook or hook manager by default. Add one only when requested, when hardening a shared repository, or when extending hooks the project already uses.

1. Detect an existing manager such as `.pre-commit-config.yaml`, `.husky/`, or `lefthook.yml`, and extend it rather than adding another.
2. Use an environment-provided skill or hook configuration tool when one is available.
3. Otherwise add the smallest direct hook or CI configuration that meets the requirement.

For commit-message hooks and templates, read the `commit-message` skill.
