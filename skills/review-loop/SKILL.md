---
name: review-loop
description:
  Review and refine any work round by round with reviewer subagents, such as a
  fast model, until a round finds little to change. Use for essays, resumes,
  application forms, documentation, rules, skills, or code. Keeps the author's
  voice and facts.
argument-hint: "[target] [reviewer agent or model]"
disable-model-invocation: true
---

# Review loop

The author owns the work. Reviewers find problems, you filter them, and the
author decides. Use supported facts and preserve the author's voice; suggest
changes to solve a concrete problem rather than to polish by preference.

## Setup

1. Read the target, earlier versions, and related files. Establish whether the
   author wants suggestions or authorizes edits. In suggestions-only mode, keep
   the target unchanged and work from a separate reference copy. Keep working
   copies and records in temporary or ignored storage when files are available,
   or as clearly labeled text in the conversation. Typos follow the same
   approval rule as other changes.
2. Build the record from `references/record.md`; references to the record also
   apply to an in-conversation record. Preserve the author's confirmed phrases
   and decisions, and record corrections. Resolve conflicting external facts
   with evidence or a question to the author before adopting a change.
3. Identify the target and any requested reviewer or model. Accept work supplied
   directly or through files, using the capabilities available in the current
   environment.
4. Choose the checks. For prose, use `references/writing.md`. Add the checks
   that other loaded skills or rules give for the target's kind or language,
   such as code review criteria or language-specific writing rules.
5. Propose the checks, the units to review, the review method and any model
   choice, and up to three rounds. Obtain approval for choices the author has
   not already approved.

## Reviewer

Choose a reviewer by capability: reading complete material, checking it against
supplied criteria and the record, and returning findings. Use a general review
role rather than a role limited to search or another unrelated task. A fast,
low-cost model is usually enough, because you filter every finding.

Treat reviewer role and model as separate choices when the environment supports
both. Honor explicit choices when available; otherwise use the environment's
defaults. Ask before substituting an unavailable requested reviewer or model.
Base any cost or quality comparison on available evidence, such as published
pricing or task-specific tests.

Use read-only permissions when the environment supports them. In every case,
instruct reviewers to return findings while keeping source material unchanged.
Instruction-only restrictions are a request, not a tool-enforced guarantee.

Without delegation, review each unit in a separate pass and report in the same
format. Identify these as self-review passes rather than independent reviews.

Give each reviewer `references/reviewer-prompt.md` filled in, with the chosen
checks and the record. Resolve bundled references relative to this skill
directory. Supply their contents directly or provide locations that the reviewer
can access; confirm that all required material is available. Give general checks
rather than sample findings, because examples can anchor a reviewer.

## Each round

- Freeze a reference copy of the current work for the round. Give every reviewer
  that same version and the current record.
- Run one reviewer per unit, such as one form field, one chapter, one file, or
  one rule. Ask before running more than that. Collect all results before
  filtering findings or changing the reference copy or record. Use the
  environment's supported mechanism to collect completed reviews. Report failed
  or incomplete units and resolve their coverage before declaring the round
  complete.
- Sort every finding: adopt, needs a fact from the author, or reject with a
  reason. Check outside claims and quoted line numbers against the work and
  relevant evidence before adopting them. When evidence is unavailable, ask the
  author or mark the claim pending. Reviewers often misread a rule or flag text
  that already follows it.
- Show adopted findings as a before-and-after table. Apply them only after
  approval, unless the author said to go ahead.
- Record rejections and decisions using the "Decided" policy in
  `references/record.md`.
- Log the round: findings, adopted, and the main reasons for rejecting.

## Stop

Stop at the approved round limit, at most three rounds, or when a complete round
adopts zero to two findings. Resolve findings awaiting author input before
counting the round's adopted changes. A complete round with every unit passing
finishes the review. Later rounds mostly reword, so more rounds cost more than
they return.
