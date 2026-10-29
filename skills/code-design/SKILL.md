---
name: code-design
description: Design conventions for state, errors, resource ownership, cleanup, lint suppression, file size, and test structure. Use when planning, writing, or reviewing non-trivial code, such as a new module, a lifecycle, a background job, or a refactor.
---

# Code design

## Size

Size is a signal for review, not a cap. Aim for files a reader can review in one sitting, about 400 lines, and going somewhat over is fine. Split a file along a concept boundary when the current change already edits that file and the boundary is clear. Keep code and comments at their natural size instead of compressing them to fit.

## Simplicity

- Remove a type, field, or layer whose only reason is to keep another part working.
- Keep values in the form the platform already gives, instead of adding wrappers and type conversions.
- Code you move or merge keeps its error handling and validation.
- Between options of equal size, take the one that is correct on edge cases. A one-liner that needs decoding is not short.

## State

- When two or more flags or optionals describe one thing, make them one enum or tagged union.
- Anything with a lifecycle, such as a job, a request, or a screen, moves through one transition function that rejects an illegal move. Moving to the current state again is a repeated report, so accept it.
- Elsewhere, keep logic flat, with early returns or one `match` or `switch` on its variants, and at most two levels of nesting.

## Errors

- Every error is propagated, shown to the user, or logged. Ignoring one needs a comment that says why.
- Log an error where you handle it, not where you propagate it.

## Ownership

A stateful resource, such as a file, a child process, or a connection, has one owner that opens and closes it. Others act on it through the owner, such as by calling its methods or sending it a message, instead of holding the resource themselves.

## Cleanup

- Write each cleanup once, such as removing a partial file, stopping a child process, or reporting a terminal state. When several exits share it, do the work in an inner function and clean up in one outer place, use a guard, or let the transition function own it. Guards include `Drop` in Rust, `finally` in TypeScript, and `with` in Python.
- Cleanup runs on every exit, including early returns, exceptions, panics, and cancellation.

## Lints

Silence a lint at the narrowest scope, such as one line or one item, with a reason. Turn a lint off project-wide only in the lint config, with a comment that says why.

## Tests

- Test each rule at the layer that decides it. When decision logic is separate from I/O, test it with plain inputs and outputs, and test the I/O layer only for waiting, cancellation, and cleanup.
- Synchronize a test on an explicit event, such as a message, a channel end, or a virtual clock. A fixed wait fails on a slow machine, and a check that something did not happen still passes when it happens after the wait.
