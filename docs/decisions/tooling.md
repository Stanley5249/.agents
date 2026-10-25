# Tooling decisions

- **Rust worktree approval**: `rust.md` asks before creating a worktree, which overrides the general worktree rule in `workflow.md`, because each worktree builds its own `target/`. Relax it if Cargo shares build output across worktrees.
- **Lockfile checks**: `rust.md` needs no `lock-check` recipe because `--locked` covers `Cargo.lock`. `pixi.md` and `python.md` need one for `pixi.lock` and `uv.lock`.
- **oxfmt `printWidth` 80**: oxfmt's default is 100 according to its configuration schema, so `oxfmt.md` sets 80 to keep Prettier-era output. It does not conflict with the rule to drop settings that match the default.
- **Installed-tool lists**: the lists in `workflow.md` and `rust.md` tell an agent which tools it may call without installing them.
- **One-off CLI tools**: `AGENTS.md` pre-approves a tool that is installed, read-only, a formatter, or a fixer. Any other one-off tool needs approval.
