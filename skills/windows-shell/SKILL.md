---
name: windows-shell
description: Windows shell guidance useful for efficient Git Bash and PowerShell commands, path handling, and output control.
---

# Windows shell efficiency

Identify the active shell before choosing syntax. Each tool call starts a fresh process: the working directory carries over, but shell variables do not.

## Shared practices

- Batch related checks into one call and keep output focused with quiet flags, filters, and `head`/`tail` or `Select-Object` limits.
- Separate command groups with `---` labels so compact output remains readable.
- Use the coding harness's precise edit tool for normal changes. For large-scale mechanical edits, or when only a shell is available, use a reviewed scripted replacement and inspect the diff afterward.
- Run control and test cases in the same call when comparing behavior.

## Git Bash

Git Bash uses MSYS2 bash at `/usr/bin/bash`.

- MSYS converts leading slashes to drive paths. Write Windows-style flags such as `/flag` as `//flag`, or run with `MSYS_NO_PATHCONV=1`.
- Standard Windows paths such as `C:/path` work, while POSIX output uses `/c/path`. Pass paths with forward slashes.
- CRLF can break string matching. Strip `\r` when piping Windows output to `grep` or `awk`.
- Discard output with `> /dev/null 2>&1`.
- Chain with `;` or `&&`:
  ```bash
  echo "--- branch ---"; git branch --show-current; echo "--- status ---"; git status -s
  ```
- Filter noisy commands before their output reaches the agent:
  ```bash
  cargo check -q 2>&1 | tail -n 15
  command 2>&1 | grep -E "error|warn"
  ```

## PowerShell

- Environment variables use `$env:NAME`, not `$NAME`.
- Discard output with `> $null` or `Out-Null`; `/dev/null` does not work.
- Use PowerShell commands rather than POSIX syntax, such as `Remove-Item -Recurse -Force` instead of `rm -rf`.
- Chain with `;` or `&&` and filter with `Select-Object` or `Select-String`:
  ```powershell
  Write-Output "--- git ---"; git status -s
  Write-Output "--- test ---"; bun test -q 2>&1 | Select-Object -Last 10
  ```
- Trim oversized single-line output with `.Substring`, after checking its length.
