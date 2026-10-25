# Code

Design rules for writing, planning, and reviewing code.

## Scope

Before editing, read the task and the code it touches. List every place the change must reach: callers, tests, fixtures, config, and exports. Check what the change could break for users: data it would destroy or expose, and callers that stop working. That is scope, and extra features sit outside it.

## Smallest change

Take the first option that fully works:

1. Does it need to exist? Skip features, options, and flexibility nobody asked for, and name them in one line. A vague request, such as "build me X", gets the smallest version that does the core job.
2. Is it already in this codebase as a helper, component, service, or pattern? Use it the way the surrounding code does.
3. Does the standard library or platform provide it? Use it, unless the project has its own.
4. Does an installed dependency provide it? Use it. Add a dependency only when it replaces more than a few lines.
5. Can it be one line a reader understands at a glance? Write one line.
6. Otherwise, write the minimum code that works.

- Keep the solution lazy and the change complete. Finish every part the task needs, including the callers, tests, and fixtures the change breaks.
- Write only the abstractions, wrappers, type conversions, options, config, and boilerplate the task needs now, and leave out "for later" code. Keep values in the form the platform already gives. For a fix or a small feature, keep the structure the codebase already has: its layers, interfaces, and conventions. Prefer deletion to addition.
- For a redesign, build to the reviewed target design. Port old code only where it fits the target, and delete the rest.
- Remove a type, field, or layer whose only reason is to keep another part working.
- The working change with the least new code wins, once you know everything it must touch.- For a bug fix, grep every caller of the function you touch before you edit, then fix the root cause once in the shared code.
- Code you move or merge keeps its error handling and validation.
- Between options of equal size, take the one that is correct on edge cases.

Never cut validation at trust boundaries, error handling that prevents data loss, security, accessibility, the calibration real hardware needs, or anything the user asked for.

## Quality

Size is a signal for review, not a cap:

- Aim for files a reader can review in one sitting, about 400 lines. Going somewhat over is fine. Split a file along a concept boundary when the current change already edits that file and the boundary is clear. Keep code and comments at their natural size instead of compressing them to fit.
- When a subdirectory or module contains more than eight hand-maintained files, consider modularizing it or simplifying its structure.

## Comments

- Comment why the code is the way it is, not what it does.

## Compatibility

- In my own unpublished project, change interfaces, formats, and schemas in place and remove the old form.
- In my own published project, keep them compatible, and ask before a breaking change that gives a clearly cleaner design.
- In other projects, keep them compatible.

## State

- When two or more flags or optionals describe one thing, make them one enum or tagged union.
- Anything with a lifecycle, such as a job, a request, or a screen, moves through one transition function that rejects an illegal move. Moving to the current state again is a repeated report, so accept it.
- Elsewhere, keep logic flat: early returns or one `match` or `switch` on its variants, with at most two levels of nesting.

## Errors

- Every error is propagated, shown to the user, or logged. Ignoring one needs a comment that says why.
- Log an error where you handle it, not where you propagate it.

## Ownership

- A stateful resource, such as a file, a child process, or a connection, has one owner that opens and closes it. Others act on it through the owner, such as by calling its methods or sending it a message, instead of holding the resource themselves.

## Cleanup

- Write each cleanup once, such as removing a partial file, stopping a child process, or reporting a terminal state. When several exits share it, do the work in an inner function and clean up in one outer place, use a guard, or let the transition function own it. Guards include `Drop` in Rust, `finally` in TypeScript, and `with` in Python.
- Cleanup runs on every exit, including early returns, exceptions, panics, and cancellation.

## Coupling

- Keep module dependencies acyclic. If two modules need each other, merge them or move the shared part to their parent.

## Lints

- Silence a lint at the narrowest scope, such as one line or one item, with a reason. Turn a lint off project-wide only in the lint config, with a comment that says why.

## Tests

- For a bug fix, write a test that fails without the fix.
- Give new non-trivial logic, such as a branch, a loop, a parser, money or security code, or a new script or app, one small test or an assert-based self-check. A trivial change needs neither.
- Test each rule at the layer that decides it. When decision logic is separate from I/O, test it with plain inputs and outputs, and test the I/O layer only for waiting, cancellation, and cleanup.
- Synchronize a test on an explicit event, such as a message, a channel end, or a virtual clock. A fixed wait fails on a slow machine, and a check that something did not happen still passes when it happens after the wait.

## Review

- Check decisions recorded in docs against the rules they serve, and report a decision whose cost a rule forbids.
