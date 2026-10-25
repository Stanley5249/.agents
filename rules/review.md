# Review

How to review work, and how to write a review prompt for another agent.

## Prompt

- Name the scope exactly: the files, commits, or diff to read, and what to leave
  out.
- State the intent the work must meet, and the rules to check, by file and
  section.
- Ask for verification with tools before a finding, such as a search, a test, or
  a build, and for each finding to quote the text it is about verbatim.
- Ask only for findings that change behavior, correctness, or maintainability,
  ranked by impact, and set an output length the reader can act on.
- Keep the review read-only, and say so.

## Findings

- Check each finding against the code before acting on it. A reviewer can cite
  the wrong line or misread intent.
- Say which findings you did not take, and why.
- Rank findings in this order: correct, safe, holds under load, tested, fast,
  lean.
