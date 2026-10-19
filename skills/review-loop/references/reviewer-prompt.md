# Reviewer prompt

Fill in the placeholders and send this to each reviewer, one per unit. Include
the materials as labeled text or replace each material placeholder with an
accessible location.

```text
Read these materials:
- <checks>: your checks. Apply them to the audience and context.
- <record>: verified facts, the author's confirmed phrases and decisions, and
  decided items.
- <reference copy>: the fixed version for this round.
  <Format notes, such as "line breaks inside a paragraph are wrapping"
  or "`\_` is an escaped underscore".>

Review only <unit>. Read the other units only for context.
The reader or user is <audience>. The unit serves <prompt, purpose, or
requirement>.

Return findings while keeping all supplied material unchanged. If tools are
needed, use them only to read the supplied material. Read the complete assigned
unit, checks, and record. Report any material you could not read, and mark
that review incomplete.
Report only problems with a concrete cost to the reader or user. Explain that
cost in each finding. A pattern match alone is a reason to inspect, not to
change.
Follow the record's "Decided" policy. Mark unresolved factual questions as
needing confirmation, and keep suggested changes within supported facts.

Reply in <language>. For each paragraph, rule, or function, first write
`<part> point: <one sentence>`, then one bullet per finding:

- [<check ID>] "<exact quote>": <problem> -> suggestion: "<change>"

End with `Verdict: PASS`, `Verdict: CHANGES`, `Verdict: NEEDS-INPUT`, or
`Verdict: INCOMPLETE`. Use PASS only after reading the complete assigned
material and resolving any factual questions.
```

## Variants

- Simplify pass: ask the reviewer to list every fact, number, and name in each
  part first, and to keep all of them in every change.
- Cross-document pass: give two documents, and ask only for mismatched facts,
  names, and claim strength between them.
- Fidelity pass: give an upstream source and its adaptation, and ask only for
  differences not listed in the record.
- Final proofread: ask only for typos, punctuation, and facts that contradict
  the record.
