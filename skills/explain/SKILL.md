---
name: explain
description: Teach a codebase concept through concrete representations, ASCII diagrams, and prediction questions over several turns. Use when the user asks for a guided lesson or to be quizzed on a concept, type, or API, not for a one-off explanation.
---

# Explain a codebase concept

Ask which concept to explain when the user has not named one.

## Setup

Establish the user's starting knowledge, desired depth, and pace. Reuse preferences already given. Default to representation-level depth and one concept per turn when the user leaves these choices to you.

Read the relevant source and schemas before teaching. Cite `file:line` for code-specific claims. Distinguish observed behavior from inferred design intent.

## Teaching loop

For each concept:

1. Explain the problem the concept solves.
2. Draw an ASCII picture of the representation or behavior.
3. Show the underlying data shape and its invariants through a concrete example. Use the storage or wire format when relevant, otherwise the in-memory types.
4. Connect the example to an API the user knows, when useful.
5. Trace how the project's types, constructors, and conversions implement the example.
6. Ask two or three prediction questions using concrete inputs, including an edge case.

At the agreed pace, pause for answers before introducing more concepts.

## Feedback

State which answers are correct or partly correct, then explain any corrections using concrete values and the relevant source. Focus on the missing reasoning.

Propose the next concept with a brief reason and let the user choose. Choose the next concept yourself when the user delegates that decision.

## Lesson detours

Answer side questions directly using source evidence, then offer to return to the lesson.
