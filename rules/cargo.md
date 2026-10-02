# Cargo projects

## Layout

- Workspace shape: a `crates/` directory of members, or sibling member
  directories listed in the root `Cargo.toml`'s `[workspace] members`. Start
  with a workspace even when single-crate, if a second crate is plausible later
  such as a `-core` and `-cli` split, because restructuring later is more
  disruptive.

## Lint and format

- Tailor `clippy.toml` to each project. Typical knobs: `msrv`,
  `doc-valid-idents` for project-specific terms, `allow-unwrap-in-tests`,
  `missing-docs-in-crate-items`. Set only the knobs the project needs.
- Enable Clippy's `pedantic` group as warnings in the root `Cargo.toml`, and
  have each member opt in with `[lints] workspace = true`. The group needs
  `priority = -1` so single-lint overrides beside it win. Because `lint` runs
  with `-D warnings`, pedantic findings fail the gate, so allow a lint
  explicitly when it does not fit the project:

  ```toml
  [workspace.lints.clippy]
  pedantic = { level = "warn", priority = -1 }
  ```

- `rustfmt.toml` stays at defaults. Only add overrides for a concrete, stated
  reason.

## Release automation

- `deny.toml` + `cargo-deny` for dependency, license, and advisory checks
- `release-plz` for automated version bumping and release PRs

Add these once the project ships releases. Until then, the local gate is enough.

## Toolchain pinning

Keep `rust-toolchain.toml` minimal. Pin the channel and the required components,
and pin an exact version only when a specific regression requires it:

```toml
[toolchain]
channel = "stable"
components = ["rustfmt", "clippy"]
```

## Justfile

Typical mappings are `fmt` to `cargo fmt --all`, `fmt-check` to
`cargo fmt --all --check`, `typecheck` to
`cargo check --workspace --all-targets`, `lint` to
`cargo clippy --locked --workspace --all-targets -- -D warnings`, and `test` to
`cargo test --locked --workspace`. A docs check runs `cargo doc --workspace`
with `RUSTDOCFLAGS=-D warnings`. Let `check` and `ci` compose the applicable
source-preserving recipes; add `build` or `install` only when the workflow needs
an explicit recipe for them.

`--locked` fails the gate when `Cargo.lock` disagrees with `Cargo.toml`, so `ci`
also proves the committed lockfile is current.

`--all-targets` also covers tests, benches, and examples for `cargo check` and
`cargo clippy`, but `cargo test --all-targets` silently skips doctests. Run
`cargo test --workspace` without it, or add `--doc` alongside, when the project
has doctests worth covering.
