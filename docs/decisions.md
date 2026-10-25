# Decisions

Rules that look wrong but are deliberate. Read this before reviewing or changing `AGENTS.md` or `rules/`, and add an item when a review finding is rejected.

- **Amend without asking**: `workflow.md` lets an agent amend local commits on a non-default branch, because only unpublished history changes. Rewriting published history still needs approval.
- **Commit scope in this repository**: `CONTRIBUTING.md` overrides the `agents` scope in `workflow.md` on purpose.
- **Project `CLAUDE.md`**: `setup.md` deletes it, including an import-only file, because Claude Code reads `AGENTS.md`.
- **CI calls tools directly**: `setup.md` keeps CI independent of the justfile, so the local gate and CI can fail for different reasons.
- **Rust worktree approval**: `rust.md` asks before creating a worktree, which overrides the general worktree rule in `workflow.md`, because each worktree builds its own `target/`. Relax it if Cargo shares build output across worktrees.
- **Lockfile checks**: `rust.md` needs no `lock-check` recipe because `--locked` covers `Cargo.lock`. `pixi.md` and `python.md` need one for `pixi.lock` and `uv.lock`.
- **oxfmt `printWidth` 80**: oxfmt's default is 100 according to its configuration schema, so `oxfmt.md` sets 80 to keep Prettier-era output. It does not conflict with the rule to drop settings that match the default.
- **Installed-tool lists**: the lists in `workflow.md` and `rust.md` tell an agent which tools it may call without installing them.
- **One-off CLI tools**: `AGENTS.md` pre-approves a tool that is installed, a formatter, or a fixer. Any other one-off tool needs approval, including a read-only one, because a downloaded package runs its own code.
- **Judgment words**: "somewhat over" 400 lines, "clear boundary", "lazy", "changes the plan", "complex topics", "when a second crate is likely", and "non-trivial logic" in the test rule leave room for judgment on purpose. Do not replace them with a number.
- **Duplicated rules across files**: a rule may repeat in two files when the files load in different situations, such as one-line Markdown paragraphs in `documents.md` and `oxfmt.md`. Rule files cannot reference each other.
- **Reasons kept in rules**: sentences that explain why, such as the Prettier note in `zed.md` and the lockfile attributes in `setup.md`, stay because an agent follows a rule better when it knows the reason.
- **Negative statements and prohibitions**: `AGENTS.md` rewrites a statement of absence as what is true, but keeps a prohibition paired with its replacement action. The two rules cover different sentences.
- **pixi beside uv or cargo**: `AGENTS.md` lists `pixi.md` as project tooling, not a language stack. A project uses one of them, or they are interchangeable, so no rule sets precedence between them.
- **No review rule**: the `quality-review` and `feedback-loop` skills cover reviews, so no rule file does. A review prompt outside the skills gets no rule.
- **`[parallel]` without a timing test**: `justfile.md` marks a recipe `[parallel]` without checking how long its jobs take, because an agent cannot see run time without measuring it.
- **No disk placement rule**: `windows.md` lists volumes, including Dev Drives, but says nothing about where files go, so agents spend no effort on drive choice.
- **Weak sentences removed**: lines an agent cannot act on, such as "keep documents minimal and concise", "I insist on project quality", and "consider splitting", stay out. Replace a vague trigger with an observable one instead of softening it.
- **Haiku reviews**: Haiku invents numeric thresholds and flags author-chosen judgment words. Verify each finding before editing.
