---
name: feedback-loop
description: Improve work through repeated feedback from low-cost agents. Use when the user asks for an iterative feedback loop with delegated agents.
argument-hint: "[target] [agent or model]"
disable-model-invocation: true
---

# Feedback loop

You coordinate the loop and own the final judgment. Feedback agents only read and report, and you verify each finding and apply every edit.

## Setup

- Use the agent or model the user names, or a low-cost model. Ask before substituting an unavailable one, and offer a labeled self-review when delegation is unavailable.
- Give every agent, in every round, the review skill or instructions the user names. They bind the agents, not your edit permissions.
- Use one agent for small work, and split larger work into independent units. Stop after three rounds unless the user sets another limit or asks to continue until a clean round.

## Each round

1. Give the agents the current version, their scope, the applicable rules, and the findings rejected so far with reasons.
2. Ask for actionable findings only, each with a location, a concrete consequence, and a correction, and skip style preferences. Ask the agents to report what they could not check.
3. Verify each finding against the work. Reject mistaken, duplicate, speculative, and preference-only findings.
4. Apply a correction that has one clearly right form and needs no approval. Record any other accepted correction as a pending decision, and start the next round.

## Stop

Stop after a round with no actionable findings, at the round limit, when the user stops the loop, or when findings keep contradicting each other or come back after rejection. Report applied changes, pending decisions together, disagreements, and unchecked coverage, without calling incomplete coverage a clean pass.
