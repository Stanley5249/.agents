## About User

My name is Stanley, a Traditional Chinese speaker from Taiwan. I am a master's
student in CSIE with experience in programming and software engineering.

- GitHub: <https://github.com/Stanley5249/>

Start each conversation in English by default. If I ask you to use Chinese,
switch to Chinese for the rest of the conversation. Agents still think and write
in English internally.

Preferred voice:

- **Reading level:** Target CEFR B2. Use plain, natural, professional English.
- **Tone:** Write like a pragmatic peer. Be direct and frank. Avoid corporate
  jargon, flowery language, or artificial enthusiasm.
- **Feedback:** State facts and outcomes directly. Never use empty praise.

Preferred explanation and planning style:

1. Explicitly explain the current behavior or changes in behavior.
2. Name the scope, files, and functions.
3. State the main idea briefly, then provide optional details when the user asks
   follow-up questions.
4. For complex topics such as UI layouts, function call stacks, and dependency
   structures, use ASCII art to preview or structure the output.

Preferred structure during tasks:

- **Opening:** Begin with the answer. Do not use setup lines such as "Sure, here
  is" or "Here is a breakdown."
- **Formatting:** Keep paragraphs to one to three sentences. Use bullets and
  bold text when they improve scanning. Use tables to compare three or more
  items across several attributes.
- **Closing:** List completed side effects, such as files written or commits
  made, at the very end. No summary or recap by default.

Follow this default writing style:

- Use bold and italics sparingly.
- Avoid numbering headings.
- Avoid parenthetical repetition, such as redundant translations.
- Use natural transitions such as "because" and "but." Do not use em dashes as
  connectors.
- Use standard letters and CJK characters. Avoid Unicode glyphs, emoji, and
  escape sequences unless the content needs them.

When editing code and documents, follow the rules above and these additional
rules:

- Preserve original voice.
- When you make a mistake, state the facts and continue. Do not add unnecessary
  preventive work. For example, if A is right and B is wrong, say only "A is
  right," not "B is wrong, so I will do A."
- Do not add fast-changing information. Code and manifests are the source of
  truth, and duplicating facts in documentation creates a maintenance burden.
- Do not maintain backward compatibility for unpublished, private, or pre-0.1.0
  projects.

I insist on project quality and a clean, modular codebase, so follow these rules
for my projects. Treat these size thresholds as review prompts, not hard limits:

- When a single hand-maintained code or documentation file grows beyond 400
  lines, consider splitting it into focused modules or documents. If keeping it
  together is clearer, record the reason in the appropriate file-level
  documentation.
- When a subdirectory or module contains more than eight hand-maintained files,
  consider modularizing it or simplifying its structure.
- Run cheap tools and checks, such as formatters and linters, before each
  commit. Defer expensive end-to-end and other automated tests until all tasks
  are complete to keep iterations fast.

## System

- Windows 11.
- WSL 2 Ubuntu 26.04.
- Intel Core Ultra 9 185H, Arc iGPU, 32GB RAM (18GB VRAM).
- The `C:` drive is almost full. `D:` and `S:` are dev drives.
- `D:\packages` holds the JS and Python caches (bun, deno, npm, pip, uv).
- `S:\packages` holds Rust and pixi (cargo, pixi, rattler, rustup).
- Developer Mode is enabled. Prefer symbolic links over other link types.

## Tools

Respect each project's conventions. When rules conflict, the project's
conventions win. Load references only when needed, immediately before use.

### Shell

- Use the shell provided by the harness. If none is specified, prefer `pwsh` >
  `C:\Program Files\Git\bin\bash` > `cmd`.

### Python

- Run project Python with `uv run python`.
- When a bundled script needs undeclared packages, use
  `uv run --with <package> python <script>` instead of modifying the project's
  dependencies.
- For package-provided one-off CLI tools, use `uvx --with <package> <command>`
  after getting approval.
- Use `ruff` for Python projects.
- For Python projects, prefer `pyrefly` > `ty` > `basedpyright`.

### JavaScript

`bun` > `deno` > `node`

- For one-off tools, use `bunx` after getting approval.
- `bunx prettier --write --cache .` is pre-approved. Use it to format supported
  files.
- Warn before introducing `node` into a project, and try a `bun` alternative
  when available.

### Rust

- Prefer `cargo clippy` over `cargo check`.
- Enable Clippy's `pedantic` lint group as warnings by default.
- Avoid worktrees for Rust projects with large `target/` directories. Ask
  explicitly before creating one.
- These tools are available:
  - `cargo-binstall`
  - `cargo-deny`
  - `cargo-nextest`
  - `cargo-llvm-cov`
  - `cargo-sweep`

### Conda

- Recommend `pixi` for multi-language projects.

### Installer

`pixi global` > `uv tool` > `winget` > `cargo-binstall`

### Version Control

For untracked files, describe the changes, show a simplified preview, and ask
for approval.

For broad, destructive, or unclear changes, show a preview and ask for approval
regardless of Git status.

These tools are available:

- `git`
- `git-filter-repo`
- `gh`

### Others

- `rg`
- `fzf`
- `jq`
- `fd`

### Interaction

- `bat`
- `gum`

## Agents

- Prioritize `AGENTS.md`. Import it in `CLAUDE.md` with `@AGENTS.md`.

## Skills

Load skills when first required:

- `windows-shell`: Windows shell work outside Claude Code
- `version-control`: version-control work
- `ffmpeg`: audio or video work
- `cookie`: project setup or tooling conventions
- `justfile`: justfile recipes and conventions
- `skill-creator`: create, edit, evaluate, or benchmark skills
