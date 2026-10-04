# Windows 11

## System

- [Developer Mode](https://learn.microsoft.com/en-us/windows/apps/get-started/enable-your-device-for-development)
  is enabled. Prefer symbolic links, and use junctions only when symbolic links
  are not practical.
- Keep large files off the system drive (`$env:SystemDrive`) and put them on a
  [Dev Drive](https://learn.microsoft.com/en-us/windows/dev-drive/). The disk
  space query below lists Dev Drives as ReFS volumes.

## Shell

PowerShell 7 (`pwsh`) and Git Bash (`$env:ProgramFiles\Git\bin\bash.exe`) are
installed.

## Global installer

Use
[`winget`](https://learn.microsoft.com/en-us/windows/package-manager/winget/)
when the preferred installers cannot meet the requirement.

## Disk space

Query the total and available bytes of each volume with a drive letter:

```powershell
Get-Volume |
  Where-Object DriveLetter |
  Sort-Object DriveLetter |
  Select-Object DriveLetter, FileSystemType, Size, SizeRemaining
```
