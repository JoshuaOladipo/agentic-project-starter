# Task lifecycle and evidence rules

`tasks/templates/FEATURE.md` is mandatory for feature work. Planning and implementation are separate requests. A feature plan is not authorization to implement. The user authorizes all tasks or specific stable IDs; agents may not silently execute unapproved prerequisites or newly proposed tasks.

## Status and checkbox semantics

| Status | Checkbox | Meaning |
| --- | --- | --- |
| Pending | `[ ]` | Planned but not started |
| In progress | `[ ]` | Agent is editing authorized scope |
| Implemented | `[ ]` | Code exists; verification incomplete |
| Verified | `[ ]` | Required checks passed; documentation/handoff may remain |
| Blocked | `[ ]` | Approval, prerequisite, or failed/unavailable required check prevents completion |
| Completed | `[x]` | Acceptance, required verification, documentation, and traceability all satisfied |

Never use `[x]` for a partial implementation. An incomplete feature may contain completed tasks. A blocked task should state the blocker and who can resolve it. If the plan changes, retain IDs; add new IDs instead of reusing old ones. Record deferrals explicitly.

## Required task fields

Each task needs `Status`, `Acceptance`, `Dependencies`, `Planned areas`, `Implementation`, `Tests`, `Verification`, `Revision`, `Architecture`, `Documentation`, and `Outstanding`. For implemented tasks, use actual repo-relative implementation paths with line ranges and symbol/description; test paths and exact executed commands; and commit SHA if available. For planning, use `pending` and mark paths as expected, not verified. `Revision: uncommitted` is truthful before a commit exists. Avoid embedding secrets, personal data, or production payloads in task records.

## Evidence rules

Capture line numbers after edits, using current checkout output. Verify file exists and line range covers relevant code. If later edits shift lines, refresh references before handoff. The task validator checks file existence and bounds, not semantic relevance. A commit SHA supports historical traceability, but an uncommitted working tree has no stable snapshot. Never fabricate results or hashes. Record check status as PASSED, FAILED, NOT RUN, or UNAVAILABLE with the command and a short reason.

## Protected decisions and scope changes

If implementation needs an unapproved architectural decision, write a proposed ADR, set affected tasks to `Blocked`, and request approval. If new tasks are discovered, propose them in the task file and request authorization when they expand scope. No approval is implied by a task appearing in the file. Agent may fix incidental in-scope defects needed for an authorized task, but must disclose them.

## Closing a feature

A feature is ready to archive only when the authorized scope is complete or explicit deferrals are accepted, task evidence is current, the PR passes required checks, and human review/merge has occurred. Move its record to `tasks/completed/` and retain it as an audit trail. Archival does not imply deployment.
