---
name: quality-review
description: Review a change, files, a folder, or the whole repository for bugs, security, load, tests, speed, and needless code, reading the connected code as well as the target. Each finding is explained in plain English. Reports only.
argument-hint: "[change, branch, PR, files, folder, or repository]"
disable-model-invocation: true
---

Review code like the senior developer who will be paged when it breaks. Report findings and leave the code unchanged. Lean still matters, because every extra line must be read, tested, and fixed later. This is a report I asked for, so give it in full.

## Scope

- Review what I name, such as uncommitted or staged changes, a commit, a branch, a PR, files, a folder, a package, or the whole repository. When I name nothing, review the uncommitted changes, or the last commit if there are none.
- Read the target, its callers, the functions it calls, its tests, and the README. For a folder or repository, also read the build and deploy config and the dependency list, and start from the entry points, such as main, routes, handlers, jobs, and CLI commands.
- Trace the real flow from where data comes in, through what is stored, to what goes out.
- When the target is a change, read the diff first. When a signature, return value, or behavior changes, search every caller, because a change can break code it does not touch.
- Read fully the paths that handle user input, money, auth, data writes, background jobs, and anything shared between processes.
- Find the expected load in the README or deploy config, such as one person running a script or many users and processes at once. Judge scale against that load, and state the load you assumed.
- In a large target, go deep where a mistake costs the most rather than file by file, and list the parts you did not read under `Not checked:`.

## Look for

Check these in order of importance:

1. **Bug:** a wrong result, a crash, or a missed edge case, such as empty, zero, the last item, rounding, or time zones. Also a caller broken by a change, callers that disagree with what a function returns, a fix in one caller while the shared function stays broken, or one rule applied differently in two places.
2. **Risk:** a security hole, such as injection, weak randomness, a secret in code, or unchecked user input. Also data loss, such as a swallowed error, writes in the wrong order, or a missing transaction.
3. **Scale:** code that works for one user and fails for many, such as a check-then-write race, the same work done by every process, memory or lists that only grow, a query per item, O(n^2) work on big input, or per-process state that must be shared.
4. **Missing test:** risky logic, such as a branch, a parser, money, security, data writes, or a bug fix, without a test that fails when it breaks. One good test is enough, rather than full coverage.
5. **Speed:** a big slowdown is a problem. A small win, such as work repeated in a hot loop, is a suggestion, because some software counts every millisecond.
6. **Lean:** code that should not exist or should be smaller.
   - Delete: dead code, unused options, flags, and config, and speculative features.
   - Reuse: a helper the repository already has, or two helpers that do the same thing. Keep one and name its path.
   - Stdlib / native: work the standard library or platform already does, or a dependency doing what a few lines or the platform can do.
   - YAGNI: an abstraction or interface with one implementation, a factory with one product, config nobody sets, or a wrapper that only passes calls through.
   - Merge: near-copies that must change together.
   - Split: one function or class doing several unrelated jobs, so it is hard to read or test. Split by job rather than by line count, and never into helpers that exist only to make a function shorter.

## Check before you report

- Give every finding a concrete case, in the form "this input or situation leads to this wrong result". Drop a finding that has no case.
- Re-read the lines to confirm the case, such as that the caller exists or the value can really be empty. Before calling code unused, search the whole tree for it, including tests, fixtures, config, and string or dynamic references.
- Propose the smallest fix that works, and prefer a fix that deletes code. Add a layer, framework, or config only when the problem needs it.
- Leave out style preferences, "consider" suggestions, and vague worries.

## Output

Write in short sentences and everyday words, and explain each technical term the first time it appears. The reader may never have seen this code. Start with `What this does:` in two or three sentences about the target, and the load you assumed.

Group findings under **Must fix**, **Should fix**, and **Nice to have**, most important first, and skip empty groups:

- Must fix: a bug, a security hole, data loss, or a failure at the expected load.
- Should fix: risky code without a test, real slowness, duplication, a function that mixes jobs, or code that should not exist.
- Nice to have: small speed-ups and shorter forms.

Number findings across groups so I can say "fix 2 and 5". Report at most 20 findings, and say how many smaller ones you left out. Give each finding a bold title with its `path:line` and four bullets of one or two sentences each:

2. **Orders land on the wrong day** (`billing/close_day.py:L40-52`)
   - **What this is:** At midnight this job closes the day and bills all orders of that day.
   - **Problem:** It takes "today" from the server clock, which runs in UTC. An order placed at 00:30 in Berlin is billed on the day before.
   - **Fix:** Compute the day once in the shop's time zone with `datetime.now(ZoneInfo("Europe/Berlin")).date()`. One line, nothing else changes.
   - **If we skip it:** Late orders show the wrong date, and accounting fixes them by hand.

End with these lines:

- `Verdict:` in one line, `Ship.` or `fix 1 and 3 first.` for a change, and `Healthy.` or what to fix first for a folder or repository.
- `Lean: -<N> lines, -<M> dependencies possible.` when lean findings exist.
- `Not checked:` with the parts that mattered and that you did not read or could not run.

When nothing is found, write `What this does:`, then `Looks good. Ship.` for a change or `Healthy. Nothing to fix.` for a folder or repository, and one line on what you checked.
