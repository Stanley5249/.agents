---
name: pwsh
description: Token-efficient PowerShell on Windows. Use when running pwsh commands to batch checks, silence noisy CLI tools, and slice output.
---

# PowerShell token efficiency

Shell calls run in `pwsh`. Each call is a fresh process; working directory carries over, but variables do not.

## Non-intuitive syntax traps

- Variables require `$env:NAME`, not `$NAME`.
- Redirection to `/dev/null` fails. Use `> $null` or `Out-Null`.
- Heredocs and POSIX flags fail. Use `Remove-Item -Recurse -Force` instead of `rm -rf`.
- Missing binaries trigger cmdlet errors. Use runners like `bunx <tool>` directly instead of probing PATH.

## Batching and silencing noise

Roundtrips and noisy output waste context. Chain steps into one call, run in quiet mode, and discard unneeded output.

- Favor quiet flags such as `-q`, `-s`, or `--silent`. Redirect discarded streams to `> $null`.
- Chain multiple checks with `;` or `&&`. Separate them with `---` labels:
  ```powershell
  Write-Output "--- git ---"; git status -s; Write-Output "--- test ---"; bun test -q 2>&1 | Select-Object -Last 10
  ```
- Filter verbose tools (cargo, chrome devtools, package managers) at the source:
  - `cargo build -q 2>&1 | Select-Object -Last 15`
  - `Select-String -Pattern "error|warning"` instead of dumping full compiler output.
  - `.Substring(0, 600)` to trim oversized single-line JSON or logs.
- Test and control in the same call:
  ```powershell
  Write-Output "--- before ---"; cmd 2>&1 | Select-Object -First 3
  Write-Output "--- after ---"; $env:FLAG = "1"; cmd 2>&1 | Select-Object -First 3
  ```
