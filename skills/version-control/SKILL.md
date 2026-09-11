---
name: version-control
description: Use for any version-control task, including Git status, diffs, commits, amendments, branches, merges, rebases, and commit-message enforcement.
---

## Repository context and safety

- Treat these guidelines as the machine default. A stricter project convention wins. Check repository instructions and files such as `.github/prompts/commit-message.prompt.md` before acting.
- Check `git status` before changing version-control state. Preserve unrelated user changes and review every untracked generated or data path.
- Ignore local-only generated or data paths instead of letting them enter a commit accidentally.
- Do not commit files under `.claude/`, `.codex/`, `.pi/`, or similar tool-local directories unless the repository intentionally tracks that integration.

## Commit practice

### When to commit or amend

- Commit a coherent, reviewable unit of work after its formatter and CI gate pass. If either is unavailable, run the closest equivalent verification. Do not commit with failed checks.
- Size a commit by reviewable purpose, not diff size. Batch small related changes, but split a large change when each part builds, passes checks, and reviews sensibly on its own.
- Keep an indivisible wiring change, rename, parameter change, or API migration in one commit when intermediate commits would be broken or meaningless.
- Amend the latest commit when an immediate correction belongs to that same unit of work, such as a typo, formatting fix, or missed related file. Do not stack a separate `fix typo` commit.
- Do not amend published or shared history without explicit approval because amending rewrites the commit ID and may require a force push.
- Create a new commit when the change has a distinct purpose, the earlier commit is not the branch tip, or rewriting shared history would be unsafe.

### How to write commit messages

- Use Conventional Commits: `type(scope): imperative summary`.
- Common types are `feat`, `fix`, `docs`, `style`, `refactor`, `perf`, `test`, `build`, `ci`, `chore`, and `revert`. Add `!` before the colon for a breaking change.
- Use an existing directory or crate/package name as the scope. Never invent one. In a flat repository, use the top-level directory. In a multi-crate workspace, use the crate or package name, such as `hidpp` rather than `crates/openlogi-hidpp`. Omit the scope for a repository-wide change.
- Write the summary as a concise imperative statement. Most commits need only the subject line.
- Add a body only when the reason, tradeoff, or migration detail is not clear from the subject and diff. Keep it to at most two sections or five bullet lines unless a project convention requires more.
- Never place a stray token, accidental `@mention`, or pasted co-author tag before the `type:`. The fallback hook at `reference/commit-msg-hook.sh` catches this common failure.
- Follow stricter project formats when present, such as mandatory bodies, project-specific scopes, 72-column wrapping, or `BREAKING CHANGE`, `Fixes`, and `NEXT` footers.

## Branch practice

### How to use branches

- Use `main` as the default branch. If a new repository starts on `master`, rename it with `git branch -m main`.
- Work on a task branch instead of committing directly to `main` by default.
- Keep each branch focused on one feature, fix, refactor, or content instance. Continue using the current branch when new work belongs to its existing purpose; otherwise create a separate branch.
- Keep commits on the branch coherent and independently reviewable where practical. Amend local corrections instead of adding cleanup commits.
- Ask before merging a task branch into `main`. Do not rewrite a shared branch or force push without explicit approval.

### How to name branches

- Name code branches `<type>/<topic>` using a Conventional Commit type, such as `feat/search`, `fix/login-timeout`, `refactor/parser`, or `chore/dependencies`.
- Use lowercase kebab-case for the topic. Keep it short but specific.
- Date-prefix branches for a content instance such as a talk deck, play session, or generated artifact run: `<kind>/<date>-<name>`. For example, `deck/<group>/<date>-<venue>-<topic>`.
- Do not use version or status suffixes such as `-v2`, `-final`, or `-wip`. Amend the branch or open a fresh dated branch instead.

## Commit-message enforcement

Repositories here generally carry no commit-message hook. Validate ordinary commits against the convention above without adding one. Configure enforcement only when the user asks, when hardening a shared repository, or when the project already uses managed hooks.

1. Check for an existing hook manager first, including `.pre-commit-config.yaml`, `.husky/`, or `lefthook.yml`. Add a `commit-msg` stage to it rather than installing a second mechanism.
2. Otherwise, prefer `prek` running `conventional-pre-commit`; see `reference/pre-commit-config.yaml`. It validates messages without imposing a Node or Python toolchain on the repository. Fall back to plain `pre-commit` only when `prek` is unavailable.
   - In a pure Cargo repository where a hook framework is unnecessary, `cocogitto` is a lighter option. Install its hook with `cog install-hook commit-msg`. It does not compose with `.pre-commit-config.yaml`, so use only one approach per repository.
3. Use an available skill or tool for hook configuration instead of hand-editing managed configuration when possible.
4. When no tool can be installed, use `reference/commit-msg-hook.sh` or validate the message manually. Treat this as a fallback, not the default.
