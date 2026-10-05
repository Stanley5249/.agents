# Code

Design rules for writing, planning, and reviewing code. Language rules add
idioms for their stack.

## Quality

I insist on project quality and a clean, modular codebase. These size thresholds
prompt a review:

- When a single hand-maintained code file grows beyond 400 lines, consider
  splitting it into focused modules. If keeping it together is clearer, record
  the reason in the file-level documentation.
- When a subdirectory or module contains more than eight hand-maintained files,
  consider modularizing it or simplifying its structure.
- Comment why the code is the way it is, not what it does.
- In unpublished, private, or pre-0.1.0 projects, change interfaces, formats,
  and schemas in place and remove the old form.

## State

- When two or more flags or optionals describe one thing, make them one enum or
  tagged union.
- Anything with a lifecycle, such as a job, a request, or a screen, moves
  through one transition function that rejects an illegal move. Moving to the
  current state again is a repeated report, so accept it.
- Elsewhere, keep logic flat: early returns or one `match` or `switch` on its
  variants, with at most two levels of nesting.

## Errors

- Every error is propagated, shown to the user, or logged. Ignoring one needs a
  comment that says why.
- Log an error where you handle it, not where you propagate it.

## Ownership

- A stateful resource, such as a file, a child process, or a connection, has one
  owner that opens and closes it. Others act on it through the owner, such as by
  calling its methods or sending it a message, instead of holding the resource
  themselves.

## Cleanup

- Write each cleanup once, such as removing a partial file, stopping a child
  process, or reporting a terminal state. When several exits share it, do the
  work in an inner function and clean up in one outer place, use a guard, or let
  the transition function own it. Guards include `Drop` in Rust, `finally` in
  TypeScript, and `with` in Python.
- Cleanup runs on every exit, including early returns, exceptions, panics, and
  cancellation.

## Coupling

- Keep module dependencies acyclic. If two modules need each other, merge them
  or move the shared part to their parent.

## Tests

- For a bug fix, write a test that fails without the fix.
