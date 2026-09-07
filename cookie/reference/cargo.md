# cargo projects

## Layout

- Workspace shape: a `crates/` directory of members, or sibling member directories listed in the root `Cargo.toml`'s `[workspace] members`. Start with a workspace even when single-crate, if a second crate is plausible later (e.g. a `-core` / `-cli` split) — restructuring later is more disruptive.
- Never use a git worktree for a Rust project — a new worktree triggers a fresh `target/` build.

## Lint/format

- `clippy.toml` is tailored per project, not copied from a shared baseline. Typical knobs: `msrv`, `doc-valid-idents` for project-specific terms, `allow-unwrap-in-tests`, `missing-docs-in-crate-items`. Pick what the project needs; don't cargo-cult a full list.
- `rustfmt.toml` stays at defaults. Only add overrides for a concrete, stated reason.
- Install CLI tools with `cargo binstall`.

## Release automation (only when the project ships releases)

- `deny.toml` + `cargo-deny` for dependency/license/advisory checks
- `git-cliff` for changelog generation from conventional-commit history
- `release-plz` for automated version bumping and release PRs

None of this is the right default for a personal/WIP project — add it only when the project is actually released.

## Toolchain pinning

Keep `rust-toolchain.toml` minimal — pin the channel and guarantee components, not an exact version unless a specific regression requires it:

```toml
[toolchain]
channel = "stable"
components = ["rustfmt", "clippy"]
```

## TOML formatting

Use `tombi` (`tombi.toml`). `taplo` is deprecated — don't add new `taplo.toml` configs, and migrate an existing one when touching that project's tooling anyway.

## When a justfile recipe needs real logic

A single shelled-out command in a recipe is fine; once a recipe needs control flow, use an `xtask` crate (a plain binary crate invoked as `cargo run -p xtask -- <command>`, aliased from a recipe) instead of inline shell.

## Hooks

`prek` (native `prek.toml`, not necessarily `.pre-commit-config.yaml`) can split cheap commit-time checks (`cargo fmt --check`) from expensive `pre-push` ones (`cargo clippy`, `cargo doc` with `RUSTDOCFLAGS=-D warnings`) — see the `commit-message` skill's `reference/prek.toml` for the template. Comment _why_ each check is staged where; that isn't obvious from the config.

## justfile recipes

Recurring recipe names: `build`, `test`, `check` (`cargo check` / `cargo clippy`), `format`/`fmt`, `ci` composing the above. For cargo+bun desktop apps (Tauri/Dioxus with a `web/` frontend), combine with `reference/bun.md` — one justfile, recipes for both sides.
