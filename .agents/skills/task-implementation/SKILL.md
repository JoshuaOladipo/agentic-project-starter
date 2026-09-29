---
name: task-implementation
description: Implement only the user-authorized task IDs from an existing Markdown feature record, maintain status, tests, documentation, and exact implementation references.
---
# Task implementation

1. Read `AGENTS.md`, the feature record, architecture contract, relevant ADRs, and engineering commands.
2. Confirm authorized task IDs (all or explicit subset); check dependencies. Stop for unapproved prerequisites or protected architectural changes.
3. Set selected tasks `In progress` and implement only approved scope, following existing patterns and adding tests.
4. Update each task to `Implemented` when code exists; capture actual file:line and symbol references from the current checkout, test paths, and truthful revision status.
5. Run required configured checks and record exact commands and results. Update documentation and architecture records when applicable. Set `Verified` only after required checks pass and acceptance is demonstrated.
6. Set `[x]` and `Completed` only when acceptance, required checks, documentation, and traceability are complete. Otherwise retain `[ ]` and explain the blocker.
7. Run `python3 scripts/validate_tasks.py <task-file>`; hand off completed/deferred IDs, code references, risks, and decisions.
