# Ponytail adaptation

Parts of this repository adapt [Ponytail](https://github.com/DietrichGebert/ponytail) by DietrichGebert under the MIT License. This document records what was adapted and every deliberate difference, so an agent can sync upstream changes or edit the adapted text without losing either.

## Source

The adaptation follows upstream commit `2961b52fc1fe6a5a87c7a959a79512e5c2f3ffe5`. `README.md` and `LICENSE` link the same commit, so update all three together.

| Upstream file                     | Local target                                                                                                       |
| --------------------------------- | ------------------------------------------------------------------------------------------------------------------ |
| `.agents/rules/ponytail.md`       | `rules/code.md`: Scope, Smallest change, the closing "Never cut" paragraph, and the non-trivial logic Tests bullet |
| `skills/ponytail-review/SKILL.md` | `skills/quality-review/SKILL.md`, and the ranking line in the `rules/code.md` Review section                       |
| `skills/ponytail-audit/SKILL.md`  | `skills/quality-review/SKILL.md`, merged with the review skill                                                     |

The other upstream skills, hooks, and plugin files are not adapted.

## Principle

Keep the adapted text as close to Ponytail as possible. A difference needs one of two reasons:

- The author decided it, and it is listed under Deliberate differences.
- The upstream wording conflicts with an existing rule, such as the writing style in `AGENTS.md`. Such a rewrite keeps the meaning, examples, and strength of the original.

Structural changes, such as moving, merging, or regrouping sections, are fine.

## Deliberate differences

`rules/code.md`:

- The sections before the adaptation, such as Compatibility, Comments, and Tests, are the author's own. Upstream text they already cover is left out.
- "Be lazy about the solution, never about the change itself" becomes "Keep the solution lazy and the change complete".
- "The shortest working diff wins" becomes "The working change with the least new code wins", which matches the upstream opening "the least new code".
- Dropped: the "lazy senior developer" persona and "The best code is the code never written", the closing lines on what was skipped, the `shortcut:` comment convention, "A house component beats a native widget", and "in one line" for comments.
- "Never cut" stays a prohibition by the author's choice.
- The Review section keeps only the ranking line. The full checklist lives in the skill.

`skills/quality-review/SKILL.md`:

- The review and audit skills are merged into one skill. Its target is whatever the user names, and mode-specific text becomes conditional, such as "for a change" or "for a folder or repository".
- The default target is the uncommitted changes, or the last commit.
- The 20-finding cap and "risky logic" apply to every target.
- `Not checked:` lists the parts that mattered and that were not read or run.
- The output starts with `What this does:`, and the verdict line covers both modes.
- The skill runs only when invoked (`disable-model-invocation`), so the description has no trigger phrases. "I" in the body means the user.
- Dropped: the `shortcut:` exemption and the audit clause "who just inherited it".

## Sync

1. List upstream changes since the pinned commit:

   ```sh
   gh api repos/DietrichGebert/ponytail/compare/<pinned commit>...HEAD --jq '.files[].filename'
   ```

2. For each changed file in the Source table, read the upstream diff and apply it to the local target, keeping the deliberate differences.
3. Compare each adapted file with upstream sentence by sentence. Every remaining difference must match an entry above or a style rule.
4. Update the pinned commit here, in `README.md`, and in `LICENSE`.

When an edit adds a new deliberate difference, record it in this document in the same commit.
