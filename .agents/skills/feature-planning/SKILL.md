---
name: feature-planning
description: Convert a user's feature description into a scoped Markdown TODO feature record with stable task IDs, acceptance criteria, dependencies, tests, and architecture impact; use for planning-only requests.
---
# Feature planning

1. Read `AGENTS.md`, product docs, architecture contract/ADRs, existing code, and relevant tests.
2. Resolve material ambiguities or record assumptions; identify affected components and protected decisions.
3. Create `tasks/active/<feature-slug>.md` from `tasks/templates/FEATURE.md` with stable task IDs, checkbox tasks, dependencies, observable acceptance criteria, planned areas, test strategy, docs, and architecture impact.
4. Set `Scope authorization: Not authorized for implementation`; leave all task checkboxes unchecked and status `Pending` or `Blocked` as appropriate.
5. Run `python3 scripts/validate_tasks.py <task-file>` and report validation result. Do not change application code during planning.
6. Summarize task IDs, dependencies, risks, and decisions needing user approval.
