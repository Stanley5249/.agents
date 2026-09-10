## Hardware

Intel Core Ultra 9 185H, Arc iGPU, 32GB RAM (18GB VRAM)

## FS

- The `C:` drive is almost full. `D:` and `S:` are dev drives.
- `D:\packages` holds the JS and Python caches (bun, deno, npm, pip, uv).
- `S:\packages` holds Rust and pixi (cargo, pixi, rattler, rustup).

## Tools

- Run Python with `uv run python`. Install CLI tools with `uv tool install`.
- For other CLI tools, prefer: `pixi global install`, `uv tool install`, `winget install`, `cargo binstall`.
- Before installing a missing CLI tool or invoking one through an on-demand package runner, explicitly ask for user approval. This includes `uvx`, `bunx`, and `uvx --with`; `bunx prettier` is explicitly pre-approved.
- For JavaScript, prefer `bun`, then `deno`, then `node` / `npm`.
- Use native import syntax for instruction pointers, such as `@AGENTS.md` in `CLAUDE.md`. For shared skills, data directories, and other paths without an import mechanism, prefer symbolic links over junctions. When a junction is found, suggest replacing it with a symbolic link when practical.
- `rg`, `fzf`, `jq`, `fd`, `just`, and `gh` are installed.
- To drive a CDP target, prefer the `chrome-devtools` CLI (`chrome-devtools-mcp`) over playwright-cli. Start it with `--no-usage-statistics --no-performance-crux`.
- Never use a git worktree for a Rust project; a new one rebuilds `target/`.

### Installed toolchain (2026-09-07)

| tool               | version                          |
| ------------------ | -------------------------------- |
| cargo / rustc      | 1.98.0                           |
| uv                 | 0.12.5                           |
| bun                | 1.4.2                            |
| deno               | 2.6.5                            |
| node               | 26.4.0                           |
| pixi               | 0.79.0                           |
| git                | 2.54.0                           |
| gh                 | 2.91.0                           |
| just               | 1.58.0                           |
| rg / fzf / jq / fd | 15.2.0 / 0.74.3 / 1.8.2 / 10.5.0 |

Re-run version checks and refresh this table when it looks stale rather than trusting it blindly.

## Skills

- Read `~/.agents/skills/bibo/SKILL.md` once at the start of every development conversation.
- Read `~/.agents/skills/cookie/SKILL.md` when scaffolding or auditing a project, or when introducing development tooling and conventions such as command runners, linting, formatting, CI, hooks, package managers, agent instruction files, or agent-specific conventions.
- Read `~/.agents/skills/commit-message/SKILL.md` before creating a Git commit or when configuring commit-message enforcement.
- Read `~/.agents/skills/git-bash/SKILL.md` before running Git Bash commands on Windows.
- Read `~/.agents/skills/pwsh/SKILL.md` before running PowerShell commands or writing PowerShell-based automation.
