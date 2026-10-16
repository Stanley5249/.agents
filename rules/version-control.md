# Version control

## User practices

### Branch

Decide this before the first edit, because choosing a branch after the work
means moving the commits onto it.

- Use `main` as the default branch. If a new repository starts on `master`,
  rename it with `git branch -m main`.
- For a change that fits in one commit, work on the current branch directly.
  Otherwise, use a task branch instead of committing directly to `main`.
- Name code branches `<type>/<topic>` using a Conventional Commit type and a
  short, specific kebab-case topic, such as `feat/search`, `fix/login-timeout`,
  or `refactor/parser`.

### Commit

- Before the first commit in a repository, read its README and contributing
  guide for commit conventions, which override these rules.
- Check the worktree status before changing it. Preserve unrelated user changes.
- On a non-default branch, commit and amend local commits without asking. Ask
  before merging, pushing, or rewriting published history.
- Commit each action as soon as it is done. One action is one feature with its
  tests and required docs, or one move, rename, dependency update, reformat, or
  refactor.
- Tracked files hold only portable content: repository-relative paths,
  environment variables, and placeholders. Keep user data, machine paths, and
  machine-specific settings in ignored files such as `.env`.
- Amend the latest commit when a small follow-up belongs to the same change.
- Before a commit, run the formatter, fast static checks, and the tests for the
  changed code. Leave the full suite and slow builds for the end of the task.

### Worktree

- Use the agent's built-in worktree feature when it has one. Otherwise, create
  the worktree at `.agents/worktrees/<topic>` and ignore it as a local scratch
  directory.
- Remove a worktree when its branch is merged or abandoned.

## Commit messages

Use Conventional Commits. Keep the subject under 50 characters and each body
line at 72 characters or fewer.

```text
<type>[optional scope]: <description>

[optional body]

[optional footer(s)]
```

### Title

- Common types are `feat`, `fix`, `docs`, `style`, `refactor`, `perf`, `test`,
  `build`, `ci`, `chore`, and `revert`.
- Add `!` before the colon for a breaking change.
- Write the description as a concise imperative statement. Most commits need
  only the subject line.
- Use a directory, package, or crate name as the scope by default. Omit the
  scope for a repository-wide change.
- Use the `agents` scope for agent-related changes, including `.agents/`,
  `AGENTS.md`, `.claude/`, and skills.

### Body

- Add a body when details are not clear from the title.
- Keep it to at most two sections or five bullet items by default.

### Footer

- Use `BREAKING CHANGE: <description>` for a breaking API change.

### Exceptions

Use `!` and `BREAKING CHANGE` only after the project has been published and has
a compatibility contract.

## Contributions to repositories I do not own

### Safety

- Every remote write needs an explicit yes: opening, editing, or closing a PR or
  issue, a comment or review reply, and a push to a PR branch.
- Show the full draft text and the exact command first, then wait.
- Read-only `gh` calls such as `view`, `list`, `status`, `diff`, and search need
  no approval.

### Before planning a PR

- Search for duplicates in open and closed PRs and issues.
- If related PRs have sat about a month without review or merge, report them to
  the user and ask before opening another PR in that area.

## Release

- Only published projects keep a changelog. Generate it or the release notes
  with [`git-cliff`](https://git-cliff.org/) from Conventional Commits.
- Changelogs and release notes may use emoji, such as in section headings.

## Tools

`git`, [`git-filter-repo`](https://github.com/newren/git-filter-repo), and `gh`
are installed.

## Reference

- [Conventional Commits 1.0.0](https://www.conventionalcommits.org/en/v1.0.0/)
