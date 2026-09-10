---
name: cookie
description: Project-setup guidance useful for scaffolding, audits, toolchains, formatting, CI, hooks, and agent conventions.
---

## Scope

Cookie covers project setup and tooling conventions. `bibo` covers communication style and ongoing development preferences.

## Quick index

- Package manager or language toolchain: detect it from the repository, then read only the matching reference below.
- Justfile, formatter, linter, CI, or hooks: see **Cross-cutting conventions**, **First commit checklist**, and **Hooks and CI**.
- `AGENTS.md`, `CLAUDE.md`, or Claude conventions: see **Agent instruction files**.
- Project README structure: see **README convention**.

Package-manager references:

- Rust workspace or crate -> `reference/cargo.md`
- Python project -> `reference/uv.md`
- JS/TS project, especially Svelte -> `reference/bun.md`
- Multi-language or native/GPU-dependency-heavy project -> `reference/pixi.md`

A project can combine two, such as cargo+bun for a Tauri/Dioxus desktop app or cargo+uv for a Rust core with a Python harness. Read both reference files.

## Cross-cutting conventions

These hold across every package manager on this machine:

- **When a project warrants a justfile, make it the command surface.** Put recurring install, dev, format, lint, check, test, and build commands there. Small script- or library-shaped projects can use their package manager directly until they need a composed command surface.
- **Keep JavaScript commands out of `package.json` scripts when a justfile is present.** Store dependencies there, and have recipes invoke local executables directly.
- **Windows shell line first.** Every justfile here opens with:
  ```
  [windows]
  set shell := ["pwsh", "-NoLogo", "-NoProfile", "-Command"]

  set default-list
  ```
- **A `ci` recipe composes the others as the merge gate**, e.g. `ci: lint check build` or `ci: lint-all check build`. Personal projects here usually have no `.github/workflows` — `just ci` run locally _is_ the gate. Add GitHub Actions only when the project is shared, has releases to automate, or the user asks.
- **Split fast local lint from full-sweep lint**: `lint` checks only `git diff` + untracked files; `lint-all` sweeps the repo and is what `ci` calls.
- **Comment the "why", not the "what"** in justfile recipes — a non-obvious flag, or why multi-line shell isn't used.
- **Write an `AGENTS.md` encoding these conventions** when scaffolding; match an existing same-shape project's style rather than reinventing it.
- **`user/` is the fixed name for local, gitignored runtime data** (a sqlite db, local state) — not `data/`, not `.local/`.
- **Add a verification recipe for any non-code artifact tests can't catch** — e.g. `just prompt <scenario>` to render the actual text an LLM would receive, or a recipe that redraws generated diagrams after a rename. Justfiles here aren't limited to build/test/lint.
- **A secondary language toolchain can stay scoped to a subdirectory** instead of promoted to the workspace root — e.g. a `pyproject.toml`+`uv.lock` inside one subcrate of an otherwise pure-cargo workspace. Don't force a root-level multi-language setup when only one part needs it.

## First commit checklist

Set these up in the first commit, not retrofitted later:

- **`.gitattributes`** — normalize line endings up front; this is a Windows machine mixing with Unix-style repos:
  ```
  * text=auto eol=lf

  *.png binary
  *.ico binary

  Cargo.lock merge=binary linguist-language=TOML linguist-generated=true -diff
  bun.lock   merge=binary linguist-language=JSON linguist-generated=true -diff
  ```
  Adjust the lockfile line for the project's package manager (`uv.lock`, `pixi.lock`), and add `binary` lines for other binary asset types.
- **License** — Rust crates dual-license as `LICENSE-APACHE` + `LICENSE-MIT`, per Rust ecosystem convention. Non-Rust projects ship a single `LICENSE`.
- **`.editorconfig`** — don't add by default; prettier/rustfmt/ruff already cover per-language formatting. Only worth it for a polyglot, shell-heavy setup.
- Wire up commit-message enforcement now if the project wants it (see the `commit-message` skill), not after bad-format commits are in history.

## README convention

Two shapes, chosen by whether the project has external users. Don't apply the heavier one to a personal project.

**Personal/WIP project**: terse, no badges.

- `# Title`, optionally a one-line description under it.
- `## Setup` or `## Commands` — install and run through the project's command surface. Use justfile recipes such as `just install`, `just dev`, and `just ci` when the project has them.
- Domain-specific sections only where behavior isn't obvious from the code.
- `## Documentation` linking to `docs/*.md` (design, architecture, roadmap, troubleshooting) rather than growing the README.
- `## Status` — what's done vs. not, while the project is mid-flight.
- No License section even when a `LICENSE` file exists — the file speaks for itself.
- A project with no external audience can skip the README entirely and rely on `AGENTS.md`.

**Published library** (crates.io or PyPI): heavier convention.

- A badge row under the title: version, docs, CI, coverage, license, plus MSRV for a crate.
- A Quick Start / Basic Usage section with runnable code examples, not just install instructions.
- A Comparison or FAQ section: why this over the alternatives.
- An explicit License section.
- An Origin / why-this-was-built section is common — short and factual, not marketing copy.

## Agent instruction files

- **`AGENTS.md` is the single source of truth.** `CLAUDE.md` imports it with the one-line `@AGENTS.md` syntax instead of copying its contents. Prefer symbolic links for shared skills, data directories, and other paths that do not support an import mechanism.
- **Monorepo: nest, don't duplicate.** The root `AGENTS.md` is a thin index directing agents to each subproject's file, such as `catalog/AGENTS.md` and `web/AGENTS.md`. Never copy subproject detail upward. Nest one layer deeper for content- or instance-specific rules that don't belong in the app's own file.
- **Split a file that outgrows a page by topic** — `.agents/rules/ci.md`, `rust.md`, or `cross-platform.md`, one topic per file and referenced from the root. Only split once the single file is actually hard to scan; don't pre-split a new project.
- **`.agents/` is the durable, tool-agnostic layer** — a living `backlog.md` (first-person, priority-ordered, written _to_ whichever agent picks it up next) and per-feature `plans/*.md` design docs live here. `.claude/` and `.codex/` stay ephemeral scratch and session state; anything meant to survive a switch of coding agent, including a shared `skills/` directory those dirs symlink into, belongs under `.agents/`.

## Hooks and CI: detect before you build

Projects here carry no commit hook or pre-commit manager by default. Add one only when requested, when hardening a shared repository, or when extending hooks the project already uses:

1. Check for an existing hook manager — `.pre-commit-config.yaml`, `.husky/`, `lefthook.yml`. If one exists, add to it.
2. Check whether the environment exposes a skill or CLI for wiring this up (e.g. a settings/hook-config helper); use it rather than hand-rolling.
3. Otherwise write the hook directly — a plain script under `.git/hooks/<name>`, or the CI yaml. Never assume Claude-Code-specific tooling is present; this skill has to work the same way under any agent or terminal.

For commit-message hooks, see the `commit-message` skill.
