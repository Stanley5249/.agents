set default-list

[windows]
set shell := ["pwsh", "-NoLogo", "-NoProfile", "-Command"]

# Pick which skills to link into Claude Code
[windows]
link:
    & "$env:ProgramFiles\Git\bin\bash.exe" scripts/link-skills.sh

# Pick which skills to link into Claude Code
[unix]
link:
    ./scripts/link-skills.sh

# Format files
fmt: _fmt-oxfmt _fmt-just

# Check formatting
check: (_fmt-oxfmt "--check") (_fmt-just "--check")

_fmt-oxfmt *args:
    bunx oxfmt {{ args }}

_fmt-just *args:
    just --fmt {{ args }}
