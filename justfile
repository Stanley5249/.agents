set default-list

[windows]
set shell := ["pwsh", "-NoLogo", "-NoProfile", "-Command"]

# Link local skills for Claude Code; Codex and Pi read skills/ directly
link *args:
    bunx skills add ./skills --global --agent pi codex claude-code {{ args }}

# Format files
fmt: _fmt-oxfmt _fmt-just

# Check formatting and skills, then run the script tests
check: (_fmt-oxfmt "--check") (_fmt-just "--check") validate test

# Validate skill metadata, references, and Markdown links
validate:
    bun scripts/validate-skills.ts

# Run the script tests
test: _test-ts _test-py

_fmt-oxfmt *args:
    bunx oxfmt {{ args }}

_fmt-just *args:
    just --fmt {{ args }}

_test-ts:
    bun test scripts

_test-py:
    uv run python -m unittest discover --start-directory scripts --quiet
