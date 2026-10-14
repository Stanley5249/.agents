# Code

Design rules for writing, planning, and reviewing code.

## Scope

Before editing, read the task and the code it touches. List every place the
change must reach: callers, tests, fixtures, config, and exports. Check what the
change could break for users: data it would destroy or expose, and callers that
stop working. That is scope, and extra features sit outside it.

## Smallest change

Take the first option that fully works:

1. Does it need to exist? Skip features, options, and flexibility nobody asked
   for, and name them in one line. A vague request, such as "build me X", gets
   the smallest version that does the core job.
2. Is it already in this codebase as a helper, component, service, or pattern?
   Use it the way the surrounding code does.
3. Does the standard library or platform provide it? Use it, unless the project
   has its own.
4. Does an installed dependency provide it? Use it. Add a dependency only when
   it replaces more than a few lines.
5. Can it be one line a reader understands at a glance? Write one line.
6. Otherwise, write the minimum code that works.

- Keep the solution lazy and the change complete. Finish every part the task
  needs, including the callers, tests, and fixtures the change breaks.
- Write only the abstractions, wrappers, type conversions, options, config, and
  boilerplate the task needs now, and leave out "for later" code. Keep values in
  the form the platform already gives. Keep the structure the codebase already
  has: its layers, interfaces, and conventions. Prefer deletion to addition.
- The working change with the least new code wins, once you know everything it
  must touch. A one-liner that needs decoding is not short.
- For a bug fix, grep every caller of the function you touch before you edit,
  then fix the root cause once in the shared code.
- Code you move or merge keeps its error handling and validation.
- Between options of equal size, take the one that is correct on edge cases.

Never cut validation at trust boundaries, error handling that prevents data
loss, security, accessibility, the calibration real hardware needs, or anything
the user asked for.

## Quality

I insist on project quality and a clean, modular codebase. These size thresholds
prompt a review:

- When a single hand-maintained code file grows beyond 400 lines, consider
  splitting it into focused modules. If keeping it together is clearer, record
  the reason in the file-level documentation.
- When a subdirectory or module contains more than eight hand-maintained files,
  consider modularizing it or simplifying its structure.

## Comments

- Comment why the code is the way it is, not what it does.

## Compatibility

- Keep interfaces, formats, and schemas compatible by default. In my own
  repository, ask before a breaking change that gives a clearly cleaner design.
- In my own unpublished or pre-0.1.0 project, change them in place and remove
  the old form.

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

## Lints

- Silence a lint at the narrowest scope, such as one line or one item, with a
  reason. Turn a lint off project-wide only in the lint config, with a comment
  that says why.

## Tests

- For a bug fix, write a test that fails without the fix.
- Give new non-trivial logic, such as a branch, a loop, a parser, money or
  security code, or a new script or app, one small test or an assert-based
  self-check. A trivial change needs neither.

## Review

- Rank findings in this order: correct, safe, holds under load, tested, fast,
  lean.
- Look for what these rules cannot show, such as security holes, races under
  concurrent load, a query per item, and edge cases like empty, zero, rounding,
  or time zones.
- Give each finding a concrete case, confirm it in the code, and propose the
  smallest fix. Drop findings without a case, including style preferences.
