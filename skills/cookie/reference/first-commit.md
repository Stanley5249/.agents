# first commit

Set up repository-wide metadata before history accumulates:

- Add `.gitattributes` with LF normalization, binary declarations, and generated lockfile handling appropriate to the project:
  ```gitattributes
  * text=auto eol=lf

  *.png binary
  *.ico binary

  # Lockfiles: avoid git merge conflict markers, mark generated, suppress noisy diffs
  bun.lock merge=binary linguist-language=JSON linguist-generated=true -diff
  Cargo.lock merge=binary linguist-language=TOML linguist-generated=true -diff
  uv.lock merge=binary linguist-language=TOML linguist-generated=true -diff
  pixi.lock merge=binary linguist-language=YAML linguist-generated=true -diff
  ```
- Always configure package lockfiles with `merge=binary linguist-language=<LANG> linguist-generated=true -diff`. This prevents corrupted lockfiles from automatic 3-way git merges, flags them as generated on GitHub, and collapses noisy lockfile diffs.
- Rust crates use `LICENSE-APACHE` and `LICENSE-MIT`; non-Rust projects normally use one `LICENSE`.
- Do not add `.editorconfig` by default when language formatters already cover the repository. Add it when a polyglot or shell-heavy project needs settings those formatters do not own.
- Configure commit-message enforcement only when the project wants it.
