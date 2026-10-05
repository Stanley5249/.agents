# Rust projects

This rule extends `project-setup.md` for Rust workspaces and crates.

## Repository metadata

In `.gitattributes`, configure `Cargo.lock`:

```gitattributes
Cargo.lock merge=binary linguist-language=TOML linguist-generated=true -diff
```

## Layout

- Use a workspace with its members under `crates/` or listed in the root
  `Cargo.toml`'s `[workspace] members`. Start with one even for a single crate
  when a second is likely, such as a `-core` and `-cli` split, because
  restructuring later is more disruptive.

## Code

- A panic is for a ruled-out case, and its message names the invariant, such as
  `expect("worker never exits before the app does")`. Anything a user, a disk,
  or a child process can cause is an error.
- Use only `pub` or private. If an item seems to need `pub(crate)` or
  `pub(super)`, move it to the shared parent or merge the modules.
- Clone a value only when a second owner needs its own copy, such as across a
  thread, a task, or a process. Otherwise borrow it or move it. Cloning an `Arc`
  or `Rc` copies a handle, which this rule allows.
- `Drop` runs synchronously and returns nothing, so a guard holds only
  synchronous cleanup that logs its own failure. Await async cleanup on the
  outer path.
- Silence a lint with `#[expect(..., reason = "...")]`. Never use `#[allow]`.
- When a file's tests outgrow its code, move them to `<module>/tests.rs` behind
  `#[cfg(test)] mod tests;`.
- With `tracing`, put `#[instrument(skip_all, fields(...))]` on each unit of
  work, such as a request, a job, or a child process run. Add `err` only where
  the error is handled. Use `level = "debug"` for a span on a hot path, such as
  a query a screen calls on every refresh.
- Tracing messages are constant lowercase phrases, such as
  `failed to <verb> <object>` or a past-tense event. Variables go in fields with
  the same names everywhere.

## Lint and format

- Tailor `clippy.toml` to each project. Typical settings: `msrv`,
  `doc-valid-idents` for project-specific terms, `allow-unwrap-in-tests`,
  `missing-docs-in-crate-items`. Set only the ones the project needs.
- Enable Clippy's `pedantic` group as warnings in the root `Cargo.toml`, and
  have each member opt in with `[lints] workspace = true`. The group needs
  `priority = -1` so single-lint overrides beside it win. Because `lint` runs
  with `-D warnings`, pedantic findings fail the gate, so set a lint the project
  rejects to `"allow"` in the same table. Two restriction lints enforce the
  `#[expect]` rule in Code:

  ```toml
  [workspace.lints.clippy]
  pedantic = { level = "warn", priority = -1 }
  allow_attributes = "warn"
  allow_attributes_without_reason = "warn"
  ```

- `rustfmt.toml` stays at defaults. Only add overrides for a concrete, stated
  reason.

## Release automation

- `cargo-deny` with a `deny.toml` for dependency, license, and advisory checks
- `release-plz` for automated version bumps and release PRs

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
