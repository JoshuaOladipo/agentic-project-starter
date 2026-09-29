# Agentic Project Starter — task-driven, architecture-controlled development

This repository is a **starter for projects built primarily by coding agents**. The human describes features and selects what to build. The agent translates those features into a durable Markdown TODO list, implements only authorized tasks, verifies the work, and annotates each task with the exact code locations that changed. Architecture and engineering rules constrain the agent; significant decisions remain with the human.

**This is a governance scaffold, not an application.** It contains no application runtime, stack-specific tests, deployed dashboard, or autonomous enforcement of GitHub approvals. Customize the architecture contract, commands, and CI before trusting autonomous changes. A passing starter validator proves structure and task-record syntax, not software correctness.

## 1. Operating model and responsibilities

| Role | Responsible for | Not automatically authorized to do |
| --- | --- | --- |
| Human/product owner | Describe desired behavior; approve task plan/subset; approve protected architectural decisions; accept residual risks | Manually code every feature |
| Planning agent | Inspect repository; turn feature request into scoped, ordered tasks with acceptance criteria and test plans | Change application code during plan-only requests |
| Coding agent | Implement authorized task IDs, test, document, and update task evidence | Expand scope, merge, deploy, or bypass approval gates |
| Architecture guardian | Compare changes to architecture contract, ADRs, and dependency rules; surface violations | Approve its own exceptions |
| Quality/operations checks | Independently run tests, scans, and production monitoring where configured | Treat agent assertions as proof |

The roles can run in one coding tool or multiple tools. Independence is provided by separate deterministic checks and enforced repository permissions, not merely by naming a second AI agent.

## 2. Quick start (new repository)

1. Copy the contents of this starter into the repository root; commit the baseline. Keep hidden directories such as `.agents/` and `.github/`.
2. Fill in `docs/product/PRODUCT.md` with the application's purpose, users, major workflows, and non-goals.
3. Define the actual components, paths, dependencies, and ownership in `architecture/CONTRACT.yaml`; change `status: uninitialized` only after doing so. Document the design in `architecture/README.md`.
4. Replace **every** `[CUSTOMIZE]` in `docs/engineering/COMMANDS.md` with real stack-specific commands; wire them into required CI jobs. Add real dependency/architecture checks and secret/security scanning. The included CI only validates the scaffold.
5. Configure `.github/CODEOWNERS` and branch rulesets to require human review and checks for protected paths; adapt `.github/PULL_REQUEST_TEMPLATE/default.md` to your team.
6. Read `AGENTS.md` and check your coding tool actually loads it and discovers `.agents/skills/`. If it does not, explicitly point the agent to `AGENTS.md` and the relevant `SKILL.md` at the start of a session. `agent.md` is a compatibility pointer, not a separate policy.
7. Run `python3 scripts/validate_starter.py` to validate the scaffold. Run `python3 scripts/validate_tasks.py` after adding task records.
8. Start with the planning prompt below. **Do not grant production access to the coding agent by default.**

## 3. The required feature-to-code workflow

The task file is the durable source of truth for a feature's plan, progress, and verification evidence. Each feature has its own file under `tasks/active/`. The human can ask for the entire plan or only particular task IDs to be implemented.

### Stage A — Describe the feature

Explain the desired user behavior and any constraints. For example:

> Add password reset: users can request a time-limited reset link, use it once, and receive confirmation. Do not change our existing authentication provider.

The agent inspects existing code, tests, product documentation, and architecture before planning. It asks questions only where ambiguity materially changes behavior, risk, or design.

### Stage B — Plan (no application code changes)

Ask:

> Read `AGENTS.md`. Plan the password-reset feature only. Create `tasks/active/password-reset.md` using `tasks/templates/FEATURE.md`. Break the work into stable, ordered Markdown checkbox tasks with acceptance criteria, dependencies, expected code areas, tests, documentation, and architectural impact. Do not implement yet.

The resulting plan includes a feature-level objective and acceptance criteria plus task IDs such as `AUTH-001`, `AUTH-002`. **Expected paths in a plan are predictions, not implementation evidence.** The plan identifies any protected architectural decision before work begins. Review it and request edits if necessary.

### Stage C — Authorize all or a subset

Ask either:

> Implement all approved tasks in `tasks/active/password-reset.md`. Update the task file as you work. Stop if you encounter a protected architectural decision.

or:

> Implement only `AUTH-001` and `AUTH-002` in `tasks/active/password-reset.md`. Do not implement the remaining tasks. Update the task record with verification evidence and actual file/line references.

Plan approval and implementation authorization are separate. An agent must not implement tasks merely because they appear in the file. A selected task may require prerequisite tasks; the agent must disclose missing dependencies and request authorization rather than silently expanding scope.

### Stage D — Implement and maintain the record

For each authorized task, move its `Status` through `Pending` → `In progress` → `Implemented` → `Verified` → `Completed`. Use `Blocked` when a decision or dependency prevents progress. Keep `[ ]` until completion; `[x]` means all acceptance criteria, required checks, and documentation are satisfied.

The agent edits only approved scope, follows architecture and code standards, adds relevant tests, and updates the task file with actual code symbols and repository-relative paths. If an implementation reveals additional work, add a proposed task marked `Pending` and ask before executing it when it changes approved scope.

### Stage E — Verify independently

Run configured format/lint/typecheck/tests/build/scans as applicable. Record **the exact command and result** for each task. Distinguish `PASSED`, `FAILED`, `NOT RUN`, and `UNAVAILABLE`; never mark a placeholder or unexecuted command as passed. Verify behavioral acceptance criteria rather than relying solely on tests written by the same agent. The architecture guardian checks contract and ADR compliance; CI and branch protection should enforce deterministic checks.

### Stage F — Update traceability and hand off

Every implemented task must include:

- **Implementation:** repository-relative file path, current line range, and function/class/symbol or description.
- **Tests:** test file paths and relevant ranges; exact test commands and results.
- **Revision:** commit SHA when committed, otherwise `uncommitted` and current working-tree context. Never invent a hash.
- **Architecture:** affected components, compliance result, and ADR link if required.
- **Documentation:** changed paths or explicit `not affected` with rationale.
- **Outstanding:** risks, limitations, and next steps.

Example (illustrative; these paths and line numbers are not real):

```markdown
- [x] AUTH-001: Add reset-token validation
  - Status: Completed
  - Acceptance: expired and reused tokens are rejected
  - Implementation: `src/auth/reset.py:18-79` (`validate_reset_token`)
  - Tests: `tests/auth/test_reset.py:12-91`
  - Verification: `pytest tests/auth/test_reset.py` — PASSED
  - Revision: `a1b2c3d` (example only)
  - Architecture: existing auth component; no protected change
  - Documentation: `docs/product/PRODUCT.md` updated
```

Line numbers are **snapshot references**: they can shift after later edits. The agent should derive them from the current checkout after editing (e.g., `nl -ba`, editor navigation, or symbol search), not guess them. A commit SHA pins a historical snapshot; use a commit permalink when sharing across machines. `scripts/validate_tasks.py` checks syntax, path existence, and line-range bounds, but does not prove that the referenced lines implement the requirement. Recheck references when resuming work or before final handoff.

### Stage G — Review, merge, and archive

The human reviews the task record and follows code references. A pull request links the feature record and summarizes verified tasks, deferred work, tests, and architecture decisions. Merge only after configured required checks and human approval. After merge, move the feature file from `tasks/active/` to `tasks/completed/`, update its revision references if necessary, and keep it as an audit trail. Moving a file does not itself authorize deployment.

## 4. Task record contract

Use `tasks/templates/FEATURE.md` for every feature. Keep task IDs stable even when reordering. A task includes `Status`, `Acceptance`, `Dependencies`, `Implementation`, `Tests`, `Verification`, `Revision`, `Architecture`, and `Documentation`. Use `none`, `pending`, or `not affected` explicitly when appropriate; do not omit fields. A feature can contain completed and pending tasks simultaneously. `tasks/active/` holds in-progress feature records; `tasks/completed/` holds features whose authorized scope is finished and reviewed. See `docs/engineering/TASK_WORKFLOW.md` for status rules, scope changes, and edge cases.

## 5. Architecture and approval policy

`architecture/CONTRACT.yaml` declares intended components and dependencies. `architecture/README.md` explains design and data flows. Significant decisions are recorded as ADRs in `architecture/decisions/`. The agent must stop before implementing protected changes such as new services, databases, queues, cross-component dependencies, auth design changes, breaking public APIs, irreversible migrations, or changes to governance/security controls. An approved ADR and updated contract must precede implementation. See `docs/engineering/CHANGE_POLICY.md`.

A YAML contract is **not self-enforcing**. Configure stack-specific dependency tests, CI gates, protected branches, and CODEOWNERS. The included validator checks required metadata, not actual code dependencies or human approval.

## 6. Communication protocol

The agent communicates at meaningful boundaries rather than narrating each edit. At planning: summarize feature interpretation, proposed task IDs, assumptions, risks, and approval needs. At implementation start: state authorized IDs and prerequisites. During work: report blockers or newly discovered architecture/security/data-loss/cost risks promptly. At handoff: report completed/deferred IDs, actual code references, verification results, documentation, architecture impact, and decisions needed. Never claim tests passed unless run; never imply AI review is independent evidence. Full format: `docs/engineering/COMMUNICATION.md`.

## 7. Files and how they fit together

```text
AGENTS.md                         Canonical agent instructions
agent.md / CLAUDE.md              Compatibility pointers
.agents/skills/*/SKILL.md         Planning, implementation, verification, review, handoff
architecture/CONTRACT.yaml        Intended component/dependency contract
architecture/README.md           Architecture narrative and diagrams
architecture/decisions/          Approved/proposed ADRs
docs/product/PRODUCT.md           Product context and requirements
docs/engineering/                Commands, change policy, communication, task lifecycle
docs/operations/OBSERVABILITY.md  Reliability, security, cost, and data-integrity guidance
tasks/templates/FEATURE.md        Mandatory feature/task record format
tasks/active/                     Active feature records
tasks/completed/                  Archived feature records
scripts/validate_starter.py       Scaffold validator
scripts/validate_tasks.py         Task-record/reference validator
.github/workflows/governance.yml  Scaffold validation CI; extend with real gates
.github/CODEOWNERS                Example review ownership; customize
```

## 8. Using different agents and continuing across sessions

The repository's persistent state is the feature record, code, tests, ADRs, and Git history—not an agent's chat context. A new agent must read `AGENTS.md`, the relevant task file, and the architecture contract, then inspect the current checkout before continuing. Do not trust a prior agent's line numbers without revalidation. The `SKILL.md` format uses a skill folder with YAML `name` and `description`; different clients may require additional discovery configuration. The canonical instructions remain in `AGENTS.md` regardless of client.

## 9. What is and is not enforced out of the box

**Included:** explicit written policies, skills, templates, task syntax/reference validator, scaffold CI, sample ownership and PR template. **Not included:** application-specific lint/test/build/security commands, real dependency boundary enforcement, approval automation, production observability, automatic semantic verification, or guaranteed agent obedience. Configure these before relying on autonomous merging or deployment. Run `python3 scripts/validate_starter.py` and `python3 scripts/validate_tasks.py` locally and in CI.

## 10. Common failure cases

- **Agent marks a task done before tests:** leave `[ ]`, set `Implemented`, and record missing/failed checks.
- **A planned file does not exist:** planned paths are expectations; only implementation references must point to actual files.
- **Line numbers become stale:** regenerate from the current checkout; include the commit SHA for historical lookup.
- **A subset depends on unapproved tasks:** stop and request approval for prerequisites.
- **A task needs a new service or dependency boundary:** propose an ADR and wait for approval.
- **A check cannot run:** report `UNAVAILABLE` or `NOT RUN`, not `PASSED`; do not mark complete if it is required.
- **The agent changes the task plan mid-implementation:** document the proposal; do not silently implement work outside the authorized IDs.
- **CI passes the starter checks:** that proves the scaffold and record structure, not feature correctness or architectural compliance.

## 11. Useful commands

```bash
python3 scripts/validate_starter.py
python3 scripts/validate_tasks.py
python3 scripts/validate_tasks.py tasks/active/password-reset.md
```

Application-specific commands belong in `docs/engineering/COMMANDS.md` and your CI configuration. See `docs/engineering/TASK_WORKFLOW.md` for the detailed lifecycle and `docs/engineering/COMMUNICATION.md` for exact handoff requirements.
