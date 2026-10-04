# Windows 11

## System

- [Developer Mode](https://learn.microsoft.com/en-us/windows/apps/get-started/enable-your-device-for-development)
  is enabled. Prefer symbolic links over other link types.
- Keep large files off the system drive (`$env:SystemDrive`) and put them on a
  [Dev Drive](https://learn.microsoft.com/en-us/windows/dev-drive/). The disk
  space query below lists Dev Drives as ReFS volumes.
- Tool homes and caches live on the Dev Drives through tool-specific environment
  variables such as `CARGO_HOME`, `PIXI_HOME`, and `UV_CACHE_DIR`. Read these
  variables instead of hard-coding paths.

## Shell

PowerShell 7 (`pwsh`) and Git Bash (`$env:ProgramFiles\Git\bin\bash.exe`) are
installed.

## Global installer

Use
[`winget`](https://learn.microsoft.com/en-us/windows/package-manager/winget/)
only when the preferred installers cannot meet the requirement.

## Disk space

Before installations, downloads, or builds over 100 MB, query the total and
available bytes of each volume with a drive letter:

```powershell
Get-Volume |
  Where-Object DriveLetter |
  Sort-Object DriveLetter |
  Select-Object DriveLetter, FileSystemType,
    @{n="SizeBytes";e={$_.Size}},
    @{n="FreeBytes";e={$_.SizeRemaining}}
```
