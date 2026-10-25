# Tests

- For a bug fix, write a test that fails without the fix.
- Test each rule at the layer that decides it. When decision logic is separate from I/O, test it with plain inputs and outputs, and test the I/O layer only for waiting, cancellation, and cleanup.
- Synchronize a test on an explicit event, such as a message, a channel end, or a virtual clock. A fixed wait fails on a slow machine, and a check that something did not happen still passes when it happens after the wait.
