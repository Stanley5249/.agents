---
name: code-design
description: Design conventions for state, resource ownership, cleanup, lint suppression, file size, and test synchronization. Use when planning, writing, or reviewing a new module, a lifecycle, a background job, or a refactor.
---

# Code design

- Files around 400 lines are a review signal, not a cap. Split along a concept boundary only when the current change already edits the file.
- When two or more flags or optionals describe one thing, make them one enum or tagged union.
- Anything with a lifecycle, such as a job, a request, or a screen, moves through one transition function that rejects an illegal move and accepts a move to the current state as a repeated report.
- A stateful resource, such as a file, a child process, or a connection, has one owner that opens and closes it. Others act on it through the owner.
- Write each cleanup once, in one outer place, a guard, or the transition function, so it runs on every exit, including early returns, exceptions, panics, and cancellation.
- Log an error where it is handled, not where it is propagated. Ignoring an error needs a comment that says why.
- Silence a lint at the narrowest scope with a reason. Turn a lint off project-wide only in the lint config, with a comment.
- Test a rule at the layer that decides it. Keep decision logic apart from I/O and test it with plain inputs and outputs.
- Synchronize a test on an explicit event, such as a message, a channel end, or a virtual clock, instead of a fixed wait, because a wait fails on a slow machine and hides late events.
