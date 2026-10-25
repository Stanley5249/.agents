# Repository decisions

- **Amend without asking**: `workflow.md` lets an agent amend local commits on a non-default branch, because only unpublished history changes. This is not a destructive change under the approval list in `AGENTS.md`.
- **Commit scope in this repository**: `CONTRIBUTING.md` overrides the `agents` scope in `workflow.md` on purpose.
- **Project `CLAUDE.md`**: `setup.md` deletes it, including an import-only file, because Claude Code reads `AGENTS.md`.
- **CI calls tools directly**: `setup.md` keeps CI independent of the justfile, so the local gate and CI can fail for different reasons.
