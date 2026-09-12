---
name: version-control
description: Use for any version-control task, including ignore decisions, Git status and diffs, commits and amendments, branches, merges, and rebases.
---

## User practices

### Ignore

- Ignore user-specific data by default. Track source and logic, but not local configuration, databases, or runtime artifacts. Track project assets because they are not user data.
- Do not commit editor and agent-specific dotpaths such as `.zed/`, `.agents/`, and `.claude/` by default. Ignore them unless the repository intentionally tracks them.
- For a local temporary or scratch directory, add a local `.gitignore` containing `*`. Otherwise, ignore the directory from its nearest parent `.gitignore`.

### Commit

- Check status before changing status. Preserve unrelated user changes.
- You may handle several independent small changes in one batch. Run the formatter and checks once after the batch, then commit each coherent change separately.
- For large changes, keep each commit focused on one scope and make it reviewable.
- Run the formatter and static checks before committing so each commit is clean.
- Run tests after all tasks are complete by default so slow tests do not block iteration.

### Amend

These rules apply only to local, unpublished commits:

- During fast prototyping or concept discussion, defer the commit until the user is satisfied.
- Amend the latest commit when a small follow-up belongs to the same change.
- Do not amend published or shared commits without explicit approval.

## Commit messages

Use Conventional Commits. Keep the subject under 50 characters and each body line at 72 characters or fewer.

```text
<type>[optional scope]: <description>

[optional body]

[optional footer(s)]
```

### Title

- Common types are `feat`, `fix`, `docs`, `style`, `refactor`, `perf`, `test`, `build`, `ci`, `chore`, and `revert`.
- Add `!` before the colon for a breaking change.
- Write the description as a concise imperative statement. Most commits need only the subject line.
- Use a directory, package, or crate name as the scope by default. Omit the scope for a repository-wide change.
- Use the `agents` scope for agent-related changes, including `.agents/`, `AGENTS.md`, `.claude/`, `CLAUDE.md`, and skills.

### Body

- Add a body when details are not clear from the title.
- Keep it to at most two sections or five bullet items by default.

### Footer

- Use `BREAKING CHANGE: <description>` for a breaking API change.

### Exceptions

Use `!` and `BREAKING CHANGE` only after the project has been published and has a compatibility contract.

## Branch

- Use `main` as the default branch. If a new repository starts on `master`, rename it with `git branch -m main`.
- Ask before merging a task branch into `main`.
- For a single small change, work on the current branch directly. Otherwise, use a task branch instead of committing directly to `main`.
- Name code branches `<type>/<topic>` using a Conventional Commit type and a short, specific kebab-case topic, such as `feat/search`, `fix/login-timeout`, or `refactor/parser`.

## Optional tools

- Use [`git-cliff`](https://git-cliff.org/) to generate changelogs for published projects.
- Use [`prek`](https://prek.j178.dev/) when a project needs fast pre-commit hooks.

## Reference

- [Conventional Commits 1.0.0](https://www.conventionalcommits.org/en/v1.0.0/)
