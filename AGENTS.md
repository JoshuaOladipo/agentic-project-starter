# Agent operating contract — canonical repository instructions

Read this file at the start of every session. `agent.md`, `CLAUDE.md`, and `.github/copilot-instructions.md` point here; this is the source of truth. Read `README.md`, `docs/product/PRODUCT.md`, `architecture/CONTRACT.yaml`, `docs/engineering/CHANGE_POLICY.md`, `docs/engineering/COMMANDS.md`, and the relevant task record before acting. Load applicable `.agents/skills/*/SKILL.md`. More local instructions may add restrictions but must not weaken these rules.

## Authority and mandatory feature workflow
1. **Plan only when asked to plan.** Turn the user's feature description into a Markdown record at `tasks/active/<feature-slug>.md` using `tasks/templates/FEATURE.md`. Inspect existing code first. Include stable task IDs, dependencies, acceptance criteria, test plan, architectural impact, and approval needs. Do not modify application code during planning.
2. **Implement only authorized tasks.** The user may authorize all tasks or a named subset. Do not interpret plan approval as authorization to merge, deploy, or implement unrelated tasks. Update the task record as work proceeds; never silently expand scope.
3. **Verify before completing.** For each task, report changed code symbols, actual repository-relative paths and current line ranges, test paths and results, and commit hash if one exists. Mark `[x]` only after acceptance criteria, required verification, and documentation are complete. Otherwise leave `[ ]` with an explicit status and reason.
4. **Handoff.** Report implemented IDs, deferred IDs, verification results, architecture impact, outstanding risks, and decisions required. Follow `docs/engineering/COMMUNICATION.md`.
5. **Resume safely.** On a new session, re-read the feature record and verify its references against the current checkout; do not assume previously reported status or line numbers are still accurate.

## Code and architecture standards
- Prefer existing patterns, simple cohesive modules, minimal changes, and existing dependencies. Avoid speculative abstractions and unrelated refactors.
- Preserve public interfaces unless a breaking change is approved. Validate untrusted input, enforce authorization server-side, handle errors explicitly, and never expose secrets or sensitive data in code, logs, prompts, or task records.
- Use safe, reversible migrations where possible. Protect transactional invariants. Bound retries, timeouts, concurrency, and third-party costs.
- Add meaningful unit, integration, and end-to-end tests for relevant behavior and failure modes. Do not weaken tests or disable checks to make a change pass.
- Follow `architecture/CONTRACT.yaml` and approved ADRs. Identify component boundaries, dependency changes, data flows, and operational impact during planning. An approved ADR and contract update must precede protected architectural implementation.
- Treat source and CI output as evidence; agent opinions and self-reported success are not independent verification.

## Documentation requirements
Keep task records, product behavior docs, API/schema docs, architecture diagrams/contract, ADRs, runbooks, and setup instructions consistent with the code. State explicitly when a category is unaffected. Do not claim documentation or references were updated unless they were.

## Permissions and escalation
The agent may inspect, plan, edit approved scope, run local checks, and prepare commits/PRs in an isolated environment. No implicit permission to merge, deploy, access production, alter credentials, change billing, destroy data, or modify governance/security policy. Stop and request approval for new services/stores/queues, cross-component dependencies, authentication or authorization design, breaking APIs, irreversible migrations, permission expansion, production changes, and other protected changes listed in `docs/engineering/CHANGE_POLICY.md`.

## Verification and communication
Run configured checks in `docs/engineering/COMMANDS.md`. Distinguish PASSED, FAILED, NOT RUN, and UNAVAILABLE; include commands and evidence. Never report placeholder checks as passed. Give a concise plan before nontrivial work, communicate promptly when blocked or a material risk appears, and avoid routine edit-by-edit narration. See `docs/engineering/COMMUNICATION.md`.
