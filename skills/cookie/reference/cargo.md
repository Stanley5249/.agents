# cargo projects

## Layout

- Workspace shape: a `crates/` directory of members, or sibling member directories listed in the root `Cargo.toml`'s `[workspace] members`. Start with a workspace even when single-crate, if a second crate is plausible later (e.g. a `-core` / `-cli` split) — restructuring later is more disruptive.

## Lint/format

- `clippy.toml` is tailored per project, not copied from a shared baseline. Typical knobs: `msrv`, `doc-valid-idents` for project-specific terms, `allow-unwrap-in-tests`, `missing-docs-in-crate-items`. Pick what the project needs; don't cargo-cult a full list.
- `rustfmt.toml` stays at defaults. Only add overrides for a concrete, stated reason.

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

Use `tombi` (`tombi.toml`).

## Hooks

Stage `cargo fmt --check` as a cheap commit-time check and `cargo clippy` / `cargo doc` (with `RUSTDOCFLAGS=-D warnings`) as the expensive pre-push checks. See the `commit-message` skill for how to wire up the hook manager itself (`prek`, or `cocogitto` for a pure-cargo repo).

## Justfile

Recurring recipe names: `build`, `test`, `check` (`cargo check` / `cargo clippy`), `format`/`fmt`, `ci` composing the above. For a cargo+bun desktop app (Tauri/Dioxus with a `web/` frontend), combine with `reference/bun.md` — one justfile, recipes for both sides. See `reference/justfile.md` for the baseline Windows shell block and naming/lint-split conventions this follows.
