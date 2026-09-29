---
name: implementation-verification
description: Independently verify implemented Markdown task records against the current checkout, code locations, acceptance criteria, tests, and architecture constraints before completion or handoff.
---
# Implementation verification

1. Read the feature record, `AGENTS.md`, architecture contract, and required commands. Do not rely on the implementing agent's assertions.
2. Run `python3 scripts/validate_tasks.py <task-file>`; inspect each actual code reference and verify that file, line range, and named symbol match the claimed change.
3. Evaluate acceptance criteria and run applicable configured tests, build, scans, and architecture checks. Record commands and truthful statuses.
4. Inspect security boundaries, edge cases, documentation, and architecture/ADR consistency. Flag any checks unavailable or not run.
5. Correct stale references and mark a task `Completed` only if all completion conditions are satisfied; otherwise leave `[ ]` and record the reason.
6. Report findings with evidence, distinguishing verified behavior from inference and untested claims.
