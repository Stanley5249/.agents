# Wording decisions

- **Judgment words**: "somewhat over" 400 lines, "clear boundary", "lazy", "changes the plan", "complex topics", and "when a second crate is likely" leave room for judgment on purpose. Do not replace them with a number.
- **Duplicated rules across files**: a rule may repeat in two files when the files load in different situations, such as one-line Markdown paragraphs in `documents.md` and `oxfmt.md`. Rule files cannot reference each other.
- **Reasons kept in rules**: sentences that explain why, such as the Prettier note in `zed.md` and the lockfile attributes in `setup.md`, stay because an agent follows a rule better when it knows the reason.
- **Negative statements and prohibitions**: `AGENTS.md` rewrites a statement of absence as what is true, but keeps a prohibition paired with its replacement action. The two rules cover different sentences.
