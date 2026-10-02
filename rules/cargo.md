# Cargo projects

## Layout

- Workspace shape: a `crates/` directory of members, or sibling member
  directories listed in the root `Cargo.toml`'s `[workspace] members`. Start
  with a workspace even when single-crate, if a second crate is plausible later
  such as a `-core` and `-cli` split, because restructuring later is more
  disruptive.

## Lint and format

- `clippy.toml` is tailored per project, not copied from a shared baseline.
  Typical knobs: `msrv`, `doc-valid-idents` for project-specific terms,
  `allow-unwrap-in-tests`, `missing-docs-in-crate-items`. Pick what the project
  needs; don't cargo-cult a full list.
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

None of this is the right default for a personal or work-in-progress project.
Add it only when the project is actually released.

## Toolchain pinning

Keep `rust-toolchain.toml` minimal. Pin the channel and guarantee components,
not an exact version unless a specific regression requires it:

```toml
[toolchain]
channel = "stable"
components = ["rustfmt", "clippy"]
```

## Justfile

Add only the justfile recipes the project currently needs. Typical mappings are
`fmt` to `cargo fmt --all`, `fmt-check` to `cargo fmt --all --check`,
`typecheck` to `cargo check --workspace --all-targets`, `lint` to
`cargo clippy --workspace --all-targets -- -D warnings`, and `test` to
`cargo test --workspace`. A docs check runs `cargo doc --workspace` with
`RUSTDOCFLAGS=-D warnings`. Let `check` and `ci` compose the applicable
source-preserving recipes; add `build` or `install` only when the workflow needs
an explicit recipe for them.

`--all-targets` also covers tests, benches, and examples for `cargo check` and
`cargo clippy`, but `cargo test --all-targets` silently skips doctests. Run
`cargo test --workspace` without it, or add `--doc` alongside, when the project
has doctests worth covering.
