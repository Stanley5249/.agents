# Reviewer prompt

Fill in the placeholders and send this to each reviewer, one per section.
Include the materials as labeled text or replace each material placeholder with
an accessible location.

```text
Read these materials:
- <criteria>: your checks. Apply them to the audience and context.
- <facts record>: verified facts, the author's confirmed phrases, and decided
  items.
- <reference text>: the fixed version for this round.
  <Format notes, such as "line breaks inside a paragraph are wrapping"
  or "`\_` is an escaped underscore".>

Review only <section>. Read the other sections only for context.
The reader is <audience>. The section answers <prompt or purpose>.

Return findings while keeping all supplied material unchanged. If tools are
needed, use them only to read the supplied material. Read the complete assigned
section, criteria, and facts record. Report any material you could not read,
and mark that review incomplete.
Report only problems with a concrete cost to the reader. Explain that cost in
each finding; a pattern match alone is a reason to inspect, not to rewrite.
Follow the facts file's "Decided" policy. Mark unresolved factual questions as
needing confirmation, and keep suggested rewrites within supported facts.

Reply in Traditional Chinese (Taiwan). For each paragraph, first write
`<paragraph> 重點：<one sentence>`, then one bullet per finding:

- [C?] 「<exact quote>」：<problem> → 建議：「<rewrite>」

End with `結論：通過`, `結論：需修改`, `結論：待確認`, or `結論：未完成`.
Use 通過 only after reading the complete assigned material and resolving any
factual questions.
```

## Variants

- Simplify pass: ask the reviewer to list every fact, number, and name in each
  paragraph first, and to keep all of them in every rewrite.
- Cross-document pass: give two texts, and ask only for mismatched facts, names,
  and claim strength between them.
- Final proofread: ask only for typos, punctuation, and facts that contradict
  the facts file.
