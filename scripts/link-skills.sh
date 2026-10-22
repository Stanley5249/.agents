#!/usr/bin/env bash
set -euo pipefail
# Git Bash on Windows copies files on `ln -s` unless told to make real links.
export MSYS=winsymlinks:nativestrict

source=$(cd "$(dirname "$0")/../skills" && pwd -P)
target="${CLAUDE_CONFIG_DIR:-$HOME/.claude}/skills"
mkdir -p "$target"

skills=()
for dir in "$source"/*/; do
  if [[ -f "$dir/SKILL.md" ]]; then skills+=("$(basename "$dir")"); fi
done

# Only symlinks into this repository and broken symlinks are managed, so other
# entries in the Claude Code skills folder, such as `synced`, stay untouched.
linked=()
stale=()
for path in "$target"/*; do
  if [[ ! -L "$path" ]]; then
    continue
  elif [[ ! -e "$path" ]]; then
    stale+=("$(basename "$path")")
  elif [[ -d "$path" ]] && [[ "$(cd "$path" && pwd -P)" == "$source"/* ]]; then
    linked+=("$(basename "$path")")
  fi
done

selected=()
if ((${#linked[@]})); then
  selected=(--selected "$(IFS=,; echo "${linked[*]}")")
fi
chosen=$(gum choose --no-limit --header 'Skills linked into Claude Code' \
  --selected-prefix '[x] ' --unselected-prefix '[ ] ' --cursor-prefix '[ ] ' \
  "${selected[@]}" "${skills[@]}") || exit

add=()
remove=()
while IFS= read -r name; do
  if [[ -z $name ]] || printf '%s\n' "${linked[@]}" | grep -qxF "$name"; then
    continue
  fi
  if [[ -e "$target/$name" ]]; then
    echo "Skipped $name, because $target/$name already exists." >&2
  else
    add+=("$name")
  fi
done <<<"$chosen"
for name in "${linked[@]}"; do
  if ! grep -qxF "$name" <<<"$chosen"; then remove+=("$name"); fi
done

if ((${#stale[@]} + ${#add[@]} + ${#remove[@]} == 0)); then
  echo 'No changes.'
  exit
fi
for name in "${stale[@]}"; do echo "x $name (broken)"; done
for name in "${add[@]}"; do echo "+ $name"; done
for name in "${remove[@]}"; do echo "- $name"; done
gum confirm "Apply $((${#stale[@]} + ${#add[@]} + ${#remove[@]})) changes?" || exit 0

# Broken links go first, so a skill linked under the same name can replace one.
for name in "${stale[@]}"; do rm "$target/$name"; done

for name in "${add[@]}"; do
  if [[ -e "$target/$name" || -L "$target/$name" ]]; then
    echo "Skipped $name, because $target/$name already exists." >&2
  else
    ln -s "$source/$name" "$target/$name"
  fi
done
for name in "${remove[@]}"; do rm "$target/$name"; done
