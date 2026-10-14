---
description:
  Audit a whole repository or a named folder for bugs, security, load, untested
  risk, slow paths, and code to delete, merge, or split. Reports only.
argument-hint: "[folder or package]"
---

Audit the repository like the senior developer who just inherited it and will be
paged when it breaks. Report findings and leave the code unchanged.

## Scope

- Audit what I name, such as a folder or a package. When I name nothing, audit
  the whole repository.
- Read the README, the build and deploy config, the dependency list, the entry
  points such as main, routes, handlers, jobs, and CLI commands, and the tests.
- Find the expected load, such as one person running a script or many users and
  processes at once, and state the load you assumed.
- Trace the main flows from where data comes in, through what is stored, to what
  goes out. Read fully the paths that handle user input, money, auth, data
  writes, background jobs, and state shared between processes.
- In a large repository, go deep where a mistake costs the most, and list the
  parts you did not read under `Not checked:`.

## Output

Write in short sentences and everyday words, and explain each technical term the
first time it appears. Start with `What this repo does:` in two or three
sentences, and the load you assumed.

Group findings under **Must fix**, **Should fix**, and **Nice to have**, most
important first, and skip empty groups:

- Must fix: a bug, a security hole, data loss, or a failure at the expected
  load.
- Should fix: risky code without a test, real slowness, duplication, a function
  that mixes jobs, or code that should not exist.
- Nice to have: small speed-ups and shorter forms.

Number findings across groups so I can say "fix 2 and 5". Report at most 20
findings, and say how many smaller ones you left out. Give each finding a bold
title with its `path:line` and four bullets of one or two sentences each:

2. **Orders land on the wrong day** (`billing/close_day.py:40-52`)
   - **What this is:** At midnight this job bills all orders of the day.
   - **Problem:** It reads "today" from the server clock in UTC, so an order
     placed at 00:30 in Berlin is billed on the day before.
   - **Fix:** Compute the day in the shop's time zone with
     `datetime.now(ZoneInfo("Europe/Berlin")).date()`.
   - **If we skip it:** Late orders show the wrong date, and accounting fixes
     them by hand.

End with:

- `Verdict:` in one line, either healthy or what to fix first.
- `Lean: -<N> lines, -<M> dependencies possible.` when lean findings exist.
- `Not checked:` with the parts you did not read or could not run.

When nothing is found, write `What this repo does:`, then
`Healthy. Nothing to fix.` and one line on what you checked.
