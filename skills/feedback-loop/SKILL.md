---
name: feedback-loop
description:
  Improve work through repeated feedback from low-cost agents. Use when the user
  asks for an iterative feedback loop with delegated agents.
argument-hint: "[target] [agent or model]"
disable-model-invocation: true
---

# Feedback loop

You coordinate the loop and own the final judgment. Low-cost feedback agents
find potential problems; you verify their findings before acting.

## Setup

Identify the target, scope, and applicable instructions. Follow the main task's
rules and approval requirements.

When the user names a review skill or instructions, give them to every feedback
agent in every round. They bind the feedback agents and leave your edit
permissions unchanged.

Use the user's requested agent or model. Otherwise prefer a low-cost model
suited to the task when model selection is available. If the requested option is
unavailable, ask before substituting. When delegation is unavailable, offer a
clearly labeled self-review instead.

Use one feedback agent for small work. Split larger work into independent units
when that improves coverage. Default to at most three rounds, unless the user
sets another limit or asks to continue until a clean round.

## Permissions

Feedback agents only read. You apply every edit.

Apply an accepted correction without asking when it has one clearly right form
and the applicable rules require no approval for it. Record every other accepted
correction as a pending decision, leave that part unchanged, and continue.

## Each round

1. Give feedback agents the same current version, their assigned scope, relevant
   instructions, and context needed to judge the work. Include earlier rejected
   findings and their reasons to prevent repeated suggestions.
2. Ask feedback agents to keep the work unchanged and return only actionable
   findings. Each finding needs a location, concrete consequence, and suggested
   correction. Permit investigation allowed by the main task, and require agents
   to report coverage and verification limits.
3. Verify each finding against the work and applicable rules. Reject mistaken,
   duplicate, and preference-only suggestions. Keep unresolved questions
   separate from accepted findings.
4. Apply safe corrections and record pending decisions as defined in
   Permissions, then start the next round without waiting for approval. Use the
   revised work as the next round's version, and include pending decisions so
   agents skip them.

## Stop

Stop when a complete round produces no actionable findings, the round limit is
reached, or the user stops the loop. Resolve incomplete coverage and pending
questions, or report them explicitly rather than treating them as a clean pass.

Report the applied changes, pending decisions, remaining issues, and checks
performed. Present all pending decisions together so the user can approve them
in one pass.
