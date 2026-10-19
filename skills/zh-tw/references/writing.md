# Taiwanese Chinese writing

Checks for Traditional Chinese (Taiwan) text. Apply them when writing Chinese
text, and give them to reviewers alongside other checks. Report only real
problems, and treat patterns as clues to judge in context.

- Z1 Taiwan usage and grammar: wording used in Taiwan, correct collocations,
  clear subjects, and one name for one concept.
- Z2 Translationese structure: phrasing that obscures meaning or reads
  unnaturally in Taiwan usage. Check vague pronouns, passive constructions, and
  English clause frames such as 當……的時候, 對於……而言, and 作為一個. Words such
  as 它, 這, 被, and 當 also occur naturally, so report the specific ambiguity
  or awkwardness.
- Z3 Modifiers: long relative clauses placed before a noun, stacked 的, 地
  adverbs and stacked intensifiers such as 非常地, and dummy verbs such as 進行
  or 作出 before an action noun. Prefer splitting the clause or using the verb
  directly.
- Z4 Names: technical names stay in their original form, such as Rust or
  lockfile, instead of a forced translation.
- Z5 Punctuation: full-width punctuation in Chinese, no full-width semicolons,
  and a half-width space between Chinese and Latin text or numbers. Reviewers
  often misread this rule and ask to delete that space.

Reviewers reply in Traditional Chinese (Taiwan) when the text is Chinese.
