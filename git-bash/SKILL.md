---
name: git-bash
description: Token-efficient Git Bash on Windows. Use when running bash commands to batch checks, silence noisy CLI tools, and slice output.
---

# Git Bash token efficiency

Shell calls run in MSYS2 bash (`/usr/bin/bash`). Each call is a fresh subshell; working directory carries over, but variables do not.

## Non-intuitive Windows quirks

- MSYS converts leading slashes to drive paths. Flags like `/flag` break unless written as `//flag` or run with `MSYS_NO_PATHCONV=1`.
- Standard Windows paths `C:/path` work, but POSIX output prints `/c/path`. Always pass forward slashes.
- Windows CRLF breaks string matching. Strip `\r` when piping command output to `grep` or `awk`.

## Batching and silencing noise

Roundtrips and verbose CLI output waste context. Chain commands into one call, run quiet mode, and edit in place.

- Use `sed -i 's/old/new/g' path` for direct edits instead of reading and rewriting entire files through file tools.
- Prefer quiet flags such as `-q`, `-s`, or `--silent`. Discard unneeded output with `> /dev/null 2>&1`.
- Chain checks with `;` or `&&`. Separate sections with `---` headers:
  ```bash
  echo "--- branch ---"; git branch --show-current; echo "--- status ---"; git status -s
  ```
- Filter verbose tools (cargo, chrome-devtools, compilers) before text hits context:
  - `cargo check -q 2>&1 | tail -n 15`
  - Pipe through `grep -E "error|warn"` instead of dumping full build transcripts.
  - Cap large outputs with `head -n 30` or `tail -n 30`.
- Run control and test steps in a single call to verify behavior side by side.
