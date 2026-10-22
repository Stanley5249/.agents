set default-list

[windows]
set shell := ["pwsh", "-NoLogo", "-NoProfile", "-Command"]

# Link local skills for Pi, Codex, and Claude Code
link *args:
    bunx skills add ./skills --global --agent pi codex claude-code {{ args }}

# Format files
fmt: _fmt-oxfmt _fmt-just

# Check formatting
check: (_fmt-oxfmt "--check") (_fmt-just "--check")

_fmt-oxfmt *args:
    bunx oxfmt {{ args }}

_fmt-just *args:
    just --fmt {{ args }}
