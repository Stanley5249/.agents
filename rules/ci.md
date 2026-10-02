# CI

Prefer a local `just ci` merge gate for personal projects. Add hosted CI when a
project is shared, publishes releases, or the user asks for it. Hosted CI should
call the same underlying checks as the local gate instead of defining a second
workflow. Add only the smallest CI configuration that meets the requirement.
