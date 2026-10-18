set default-list

[windows]
set shell := ["pwsh", "-NoLogo", "-NoProfile", "-Command"]

# Pick which skills to link into Claude Code
[windows]
link:
    ./scripts/link-skills.ps1

# Format files
fmt: _fmt-oxfmt _fmt-just

# Check formatting
check: (_fmt-oxfmt "--check") (_fmt-just "--check")

_fmt-oxfmt *args:
    bunx oxfmt {{ args }}

_fmt-just *args:
    just --fmt {{ args }}
