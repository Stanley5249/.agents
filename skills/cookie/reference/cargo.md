# cargo projects

## Layout

- Workspace shape: a `crates/` directory of members, or sibling member
  directories listed in the root `Cargo.toml`'s `[workspace] members`. Start
  with a workspace even when single-crate, if a second crate is plausible later
  (e.g. a `-core` / `-cli` split) — restructuring later is more disruptive.
- In `.gitattributes`, configure:
  ```gitattributes
  Cargo.lock merge=binary linguist-language=TOML linguist-generated=true -diff
  ```

## Lint/format

- `clippy.toml` is tailored per project, not copied from a shared baseline.
  Typical knobs: `msrv`, `doc-valid-idents` for project-specific terms,
  `allow-unwrap-in-tests`, `missing-docs-in-crate-items`. Pick what the project
  needs; don't cargo-cult a full list.
- `rustfmt.toml` stays at defaults. Only add overrides for a concrete, stated
  reason.

## Release automation (only when the project ships releases)

- `deny.toml` + `cargo-deny` for dependency/license/advisory checks
- `release-plz` for automated version bumping and release PRs

None of this is the right default for a personal/WIP project — add it only when
the project is actually released.

## Toolchain pinning

Keep `rust-toolchain.toml` minimal — pin the channel and guarantee components,
not an exact version unless a specific regression requires it:

```toml
[toolchain]
channel = "stable"
components = ["rustfmt", "clippy"]
```

## Hooks

Stage `cargo fmt --check` as a cheap commit-time check and
`cargo clippy --workspace --all-targets -- -D warnings` /
`cargo doc --workspace` (with `RUSTDOCFLAGS=-D warnings`) as the expensive
pre-push checks.

## Justfile

Follow the shared recipe split in the [Justfile skill](../../justfile/SKILL.md),
adding only the recipes the project currently needs. Typical mappings are `fmt`
to `cargo fmt --all`, `fmt-check` to `cargo fmt --all --check`, `typecheck` to
`cargo check --workspace --all-targets`, `lint` to
`cargo clippy --workspace --all-targets -- -D warnings`, and `test` to
`cargo test --workspace`. Let `check` and `ci` compose the applicable
source-preserving recipes; add `build` or `install` only when the workflow needs
an explicit recipe for them.

`--all-targets` also covers tests, benches, and examples for `check`/`clippy`,
but `cargo test --all-targets` silently skips doctests — run
`cargo test --workspace` without it, or add `--doc` alongside, when the project
has doctests worth covering.
