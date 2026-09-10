# first commit

Set up repository-wide metadata before history accumulates:

- Add `.gitattributes` with LF normalization and binary declarations appropriate to the project:
  ```gitattributes
  * text=auto eol=lf

  *.png binary
  *.ico binary
  ```
- Mark generated lockfiles as binary merge targets when useful, and adjust entries for Cargo, bun, uv, or pixi.
- Rust crates use `LICENSE-APACHE` and `LICENSE-MIT`; non-Rust projects normally use one `LICENSE`.
- Do not add `.editorconfig` by default when language formatters already cover the repository. Add it when a polyglot or shell-heavy project needs settings those formatters do not own.
- Configure commit-message enforcement only when the project wants it.
