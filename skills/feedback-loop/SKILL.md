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
rules, approval requirements, and editing permissions.

Use the user's requested agent or model. Otherwise prefer a low-cost model
suited to the task when model selection is available. If the requested option is
unavailable, ask before substituting. When delegation is unavailable, offer a
clearly labeled self-review instead.

Use one feedback agent for small work. Split larger work into independent units
when that improves coverage. Default to at most three rounds.

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
4. Present or apply accepted corrections according to the main task's editing
   permissions. Use the revised work as the next round's version.

## Stop

Stop when a complete round produces no actionable findings, the round limit is
reached, or the user stops the loop. Resolve incomplete coverage and pending
questions, or report them explicitly rather than treating them as a clean pass.

Report the accepted changes, remaining issues, and checks performed.
