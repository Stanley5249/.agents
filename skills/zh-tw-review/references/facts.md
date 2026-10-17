# Facts file

Build this record at setup as a temporary or ignored file, or as labeled text
when file storage is unavailable. Every reviewer reads it. Each line is one
short fact with its source and status, so a reviewer can match a sentence
against it. Treat draft claims as author-provided claims until evidence or
confirmation establishes their status.

## Layout

```markdown
# Facts

Record factual claims from the text here. A missing entry is a question for the
coordinating reviewer to check, rather than evidence that the claim is false.

## Context

- Audience, purpose, length guide, and the prompt or question for each section.
- Draft claims awaiting confirmation or evidence, explicitly marked pending.

## Verified

- Facts checked against evidence such as the repo or public records, each with
  its source and relevant date or number.

## Confirmed by the author

- The author's confirmed phrases and claims, such as habits and motives, with
  their confirmation source. Accept these as the author's account; return any
  conflicting external evidence to the coordinating reviewer.

## Corrections

- Corrections from the author, newest first. These replace earlier statements of
  the author's account. Check conflicting external evidence before adopting a
  factual rewrite.

## Decided

- Preserve the author's settled wording and direction until the author reopens
  them.
- Record rejected factual or consistency findings with the reason and affected
  text. Revisit them only when new evidence or a relevant text change affects
  that reason, and explain what changed.
```

## Upkeep

- Add a correction the moment the author gives it, and remove the line it
  replaces.
- After each round, move rejected findings into "Decided" with a short reason.
