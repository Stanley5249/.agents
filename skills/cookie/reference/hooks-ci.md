# hooks and CI

## CI gate

Prefer a local `just ci` merge gate for personal projects. Add hosted CI when a
project is shared, publishes releases, or the user asks for it. Hosted CI should
call the same underlying checks as the local gate instead of defining a second
workflow.

## Hooks

Projects carry no commit hook or hook manager by default. Add one only when
requested, when hardening a shared repository, or when extending hooks the
project already uses.

1. Detect and extend an existing hook manager rather than adding another.
2. Otherwise, use the hook tool selected by the version-control practice.
3. Add only the smallest hook or CI configuration that meets the requirement.
