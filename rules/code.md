# Code

Design rules for writing, planning, and reviewing code. Language rules add
idioms for their stack, and a project's `AGENTS.md` may tighten any rule here.

## Quality

I insist on project quality and a clean, modular codebase. Treat these size
thresholds as review prompts, not hard limits:

- When a single hand-maintained code file grows beyond 400 lines, consider
  splitting it into focused modules. If keeping it together is clearer, record
  the reason in the file-level documentation.
- When a subdirectory or module contains more than eight hand-maintained files,
  consider modularizing it or simplifying its structure.
- Comment why the code is the way it is, not what it does.
- Do not maintain backward compatibility for unpublished, private, or pre-0.1.0
  projects.

## State

- When two or more flags or optionals describe one thing, make them one enum.
- Anything with a lifecycle, such as a job, a request, or a screen, moves
  through one transition function that rejects an illegal move. Reporting the
  current state again is not a move.
- Elsewhere, keep logic flat: early returns or one `match` or `switch` on an
  enum, with no more than two levels of nesting.

## Errors

- Every error is returned, shown to the user, or logged. Ignoring one needs a
  comment that says why.
- Log an error where you handle it, not where you return it.

## Ownership

- A resource has one owner. Others reach it through a handle to that owner, such
  as a channel sender, never through a shared copy.

## Cleanup

- Write each cleanup once, such as removing a partial file, stopping a child
  process, or reporting a terminal state. When several exits share it, do the
  work in an inner function and clean up in one outer place, use a guard such as
  `Drop` in Rust or `finally` in TypeScript, or let the transition function own
  it.
- Cleanup runs on every exit, including early returns, cancellation, and a
  panic.
- A guard that cannot await holds only synchronous cleanup that logs its own
  failure. Await async cleanup on the outer path.

## Coupling

- No cycles between modules. If two modules need each other, merge them or move
  the shared part to their parent.

## Tests

- For a bug fix, write a test that fails without the fix.
