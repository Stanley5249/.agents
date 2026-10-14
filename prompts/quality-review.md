---
description:
  Review one change for bugs, security, load, tests, speed, and needless code,
  reading the connected code as well as the diff. Reports only.
argument-hint: "[change, branch, PR, or files]"
---

Review a change like the senior developer who will be paged when it breaks.
Report findings and leave the code unchanged.

## Scope

- Review what I name, such as uncommitted or staged changes, a branch, a PR, or
  files. When I name nothing, review the uncommitted changes, or the last commit
  if there are none.
- Read the diff, then the callers of every changed function, the functions it
  calls, the tests, and the README.
- When a signature, return value, or behavior changes, search every caller,
  because a change can break code it does not touch.
- Find the expected load in the README or deploy config, such as one person
  running a script or many users at once, and state the load you assumed.

## Output

Write in short sentences and everyday words, and explain each technical term the
first time it appears. Start with `What this change does:` in two or three
sentences.

Group findings under **Must fix**, **Should fix**, and **Nice to have**, and
skip empty groups:

- Must fix: a bug, a security hole, data loss, or a failure at the expected
  load.
- Should fix: risky code without a test, real slowness, duplication, a function
  that mixes jobs, or code that should not exist.
- Nice to have: small speed-ups and shorter forms.

Number findings across groups so I can say "fix 2 and 5". Give each finding a
bold title with its `path:line` and four bullets of one or two sentences each:

2. **Orders land on the wrong day** (`billing/close_day.py:40-52`)
   - **What this is:** At midnight this job bills all orders of the day.
   - **Problem:** It reads "today" from the server clock in UTC, so an order
     placed at 00:30 in Berlin is billed on the day before.
   - **Fix:** Compute the day in the shop's time zone with
     `datetime.now(ZoneInfo("Europe/Berlin")).date()`.
   - **If we skip it:** Late orders show the wrong date, and accounting fixes
     them by hand.

End with `Verdict: Ship.` or `Verdict: fix 1 and 3 first.`, then
`Lean: -<N> lines possible.` when lean findings exist, and `Not checked:` in one
line when something mattered and could not be checked. When nothing is found,
write `What this change does:`, then `Looks good. Ship.` and one line on what
you checked.
