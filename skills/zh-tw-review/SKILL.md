---
name: zh-tw-review
description:
  Review and refine Traditional Chinese (Taiwan) writing round by round, using
  reviewer subagents when available. Use for essays, resumes, application forms,
  reports, or documentation. Keeps the author's voice and facts.
argument-hint: "[file] [reviewer agent or model]"
disable-model-invocation: true
---

# Review Taiwanese Chinese writing

The author owns the text. Reviewers find problems, you filter them, and the
author decides. Use supported facts and preserve the author's voice; suggest
rewrites to solve a concrete reader problem rather than to polish by preference.

## Setup

1. Read the draft, earlier versions, and related files. Establish whether the
   author wants suggestions or authorizes edits. In suggestions-only mode, keep
   the draft unchanged and work from a separate reference copy. Keep working
   copies and records in temporary or ignored storage when files are available,
   or as clearly labeled text in the conversation. Typos follow the same
   approval rule as other changes.
2. Build the facts record from `references/facts.md`; references to the facts
   file also apply to an in-conversation record. Preserve the author's confirmed
   phrases and record corrections. Resolve conflicting external facts with
   evidence or a question to the author before adopting a rewrite.
3. Identify the input text and any requested reviewer or model. Accept text
   supplied directly or through files, using the capabilities available in the
   current environment.
4. Propose the checks from `references/criteria.md`, the sections to review, the
   review method and any model choice, and up to three rounds. Obtain approval
   for choices the author has not already approved.

## Reviewer

Choose a reviewer by capability: reading complete prose, checking it against
supplied criteria and facts, and returning findings. Use a general review role
rather than a role limited to search or another unrelated task.

Treat reviewer role and model as separate choices when the environment supports
both. Honor explicit choices when available; otherwise use the environment's
defaults. Ask before substituting an unavailable requested reviewer or model.
Base any cost or quality comparison on available evidence, such as published
pricing or task-specific tests.

Use read-only permissions when the environment supports them. In every case,
instruct reviewers to return findings while keeping source material unchanged.
Instruction-only restrictions are a request, not a tool-enforced guarantee.

Without delegation, review each section in a separate pass and report in the
same format. Identify these as self-review passes rather than independent
reviews.

Give each reviewer `references/reviewer-prompt.md` filled in, with
`references/criteria.md` and the facts file. Resolve bundled references relative
to this skill directory. Supply their contents directly or provide locations
that the reviewer can access; confirm that all required material is available.
Give general checks rather than sample findings, because examples can anchor a
reviewer.

## Each round

- Freeze a reference copy of the current text for the round. Give every reviewer
  that same version and the current facts file.
- Run one reviewer per section, such as one form field or one chapter. Ask
  before running more than that. Collect all results before filtering findings
  or changing the reference text or facts file. Use the environment's supported
  mechanism to collect completed reviews. Report failed or incomplete sections
  and resolve their coverage before declaring the round complete.
- Sort every finding: adopt, needs a fact from the author, or reject with a
  reason. Check outside claims against relevant evidence before adopting them.
  When evidence is unavailable, ask the author or mark the claim pending.
  Reviewers often misread a rule, such as asking to delete the space between
  Chinese and Latin text.
- Show adopted findings as a before-and-after table. Apply them only after
  approval, unless the author said to go ahead.
- Record rejections and decisions using the "Decided" policy in
  `references/facts.md`.
- Log the round: findings, adopted, and the main reasons for rejecting.

## Stop

Stop at the approved round limit, at most three rounds, or when a complete round
adopts zero to two findings. Resolve findings awaiting author input before
counting the round's adopted changes. A complete round with every section
passing finishes the review. Later rounds mostly reword, so more rounds cost
more than they return.
