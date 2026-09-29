# Agent communication contract

Keep communications concise, factual, and tied to the feature task file. Avoid narration of routine edits. Do not imply independent verification from the agent's own opinion.

## Planning response
State feature interpretation, task file path, proposed task IDs and dependencies, assumptions, architecture/security implications, and any decisions requiring approval. Explicitly state that application code was not modified during plan-only work.

## Implementation start
State authorized task IDs, prerequisites, affected components, planned checks, and any existing blocker. Do not treat a plan as permission to implement.

## During implementation
Communicate promptly on a blocker, a material requirement ambiguity, protected architecture change, security/privacy/data-loss risk, unexpected cost, or failed check that changes scope. Propose options; do not silently override the user's decision.

## Final handoff (required)

1. **Scope:** feature file path; authorized, completed, blocked, and deferred task IDs.
2. **Changes:** concise summary; affected components; task-level file:line and symbol references in the feature record.
3. **Verification:** exact commands and PASSED / FAILED / NOT RUN / UNAVAILABLE, with reasons; distinguish scaffold validation from application checks.
4. **Architecture:** compliance assessment, ADRs, and protected decisions pending.
5. **Documentation:** changed docs or explicit reason not affected.
6. **Risks and follow-up:** limitations, unverified behavior, migration/rollback notes, and next requested human decision.
7. **Revision:** commit SHA if one exists; otherwise state uncommitted.

Never claim a task is completed if required checks, acceptance criteria, or documentation remain outstanding.
