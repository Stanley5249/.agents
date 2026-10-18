$ErrorActionPreference = 'Stop'

$source = (Resolve-Path (Join-Path $PSScriptRoot '..\skills')).Path
$config = $env:CLAUDE_CONFIG_DIR ?? (Join-Path $HOME '.claude')
$target = Join-Path $config 'skills'
New-Item -ItemType Directory -Force $target | Out-Null

$skills = Get-ChildItem $source -Directory |
  Where-Object { Test-Path (Join-Path $_.FullName 'SKILL.md') } |
  ForEach-Object Name

# Only symlinks into this repository are managed, so other entries in the
# Claude Code skills folder, such as `synced`, stay untouched.
$linked = @(Get-ChildItem $target -Force |
  Where-Object { $_.LinkType -eq 'SymbolicLink' -and $_.Target -like "$source\*" } |
  ForEach-Object Name)

$selected = $linked ? @('--selected', ($linked -join ',')) : @()
$chosen = @(gum choose --no-limit --header 'Skills linked into Claude Code' `
    --selected-prefix '[x] ' --unselected-prefix '[ ] ' --cursor-prefix '[ ] ' `
    @selected @skills)
if ($LASTEXITCODE -ne 0) { exit $LASTEXITCODE }

$add = @(foreach ($name in $chosen | Where-Object { $_ -notin $linked }) {
    $path = Join-Path $target $name
    if (Get-Item $path -Force -ErrorAction SilentlyContinue) {
      Write-Warning "Skipped $name, because $path already exists."
    } else {
      $name
    }
  })
$remove = @($linked | Where-Object { $_ -notin $chosen })
if (-not ($add -or $remove)) {
  'No changes.'
  exit
}

$add | ForEach-Object { "+ $_" }
$remove | ForEach-Object { "- $_" }
gum confirm "Apply $($add.Count + $remove.Count) changes?"
if ($LASTEXITCODE -ne 0) { exit }

foreach ($name in $add) {
  New-Item -ItemType SymbolicLink -Path (Join-Path $target $name) -Target (Join-Path $source $name) | Out-Null
}
foreach ($name in $remove) {
  Remove-Item (Join-Path $target $name)
}
