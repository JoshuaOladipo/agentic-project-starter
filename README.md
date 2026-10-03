# Agentic Development Framework

A versioned framework for agent-led software development that preserves human control over scope, architecture, and verification.

## Core process

1. **Describe behavior.** The human describes what a feature must do.
2. **Plan.** The agent inspects the repository and creates `tasks/active/<feature>.md`. Planning alone never authorizes coding.
3. **Authorize.** The human selects all tasks or specific task IDs.
4. **Implement.** The agent changes only authorized scope and follows `architecture/CONTRACT.yaml`.
5. **Trace.** Each task is updated with actual file paths, line ranges, useful symbols, tests, and a commit ID when available.
6. **Verify.** `Implemented` means code exists; `Verified` means required checks actually passed. Results may never be invented.
7. **Govern architecture.** Protected structural changes are blocked pending explicit approval and normally recorded in an ADR.
8. **Handoff.** The task record, not chat history, preserves completed work, remaining work, verification, blockers, and decisions.

## Installed project layout

```text
project/
├── AGENTS.md                 # project-owned entry point
├── agentic.yaml              # project-owned configuration
├── .agentic/                 # FRAMEWORK-MANAGED
│   ├── VERSION
│   ├── AGENTS.md
│   ├── skills/
│   ├── standards/
│   ├── templates/
│   └── scripts/
├── .agentic-local/           # project-owned framework overrides
├── architecture/             # project-owned
│   ├── CONTRACT.yaml
│   └── decisions/
├── tasks/                    # project-owned durable work records
│   ├── active/
│   └── completed/
├── docs/
├── src/
└── tests/
```

The ownership boundary is fundamental: **never customize `.agentic/` for one application**. Put application facts in root `AGENTS.md`, architecture files, or `.agentic-local/`. This allows `.agentic/` to be safely replaced during an upgrade.

## Install into an existing repository

Requires Python 3 and no third-party packages:

```bash
python3 cli/agentic_starter.py init /path/to/project
```

`init` installs `.agentic/` and creates missing bootstrap files. It preserves existing project-owned files. If an existing `AGENTS.md` is found, it is not overwritten; integrate a direction to read `.agentic/AGENTS.md`, `architecture/CONTRACT.yaml`, and `.agentic-local/AGENTS.md`.

Commit `.agentic/` to the application repository. That pins the exact agent rules used by each source revision.

## Planning a feature

Example human request:

> Add saved searches. Users can save, rename, delete, and execute a saved search. Generate the implementation TODO list.

The planning agent uses the `feature-planning` skill, inspects relevant code, and creates a task record. It does **not** implement code unless separately authorized.

Every task has a stable ID, purpose, dependencies, acceptance criteria, expected verification, architecture impact, and implementation-evidence fields.

## Authorizing implementation

Examples:

```text
Implement all tasks in tasks/active/saved-searches.md.
```

or:

```text
Implement TASK-002 through TASK-004 only.
```

Authorization is scoped to those tasks. Newly discovered non-trivial work is added to the plan rather than silently absorbed.

## Task states

- `Pending` — planned.
- `In progress` — currently being changed.
- `Implemented` — code exists but required verification is incomplete.
- `Verified` — required checks passed.
- `Blocked` — a dependency or decision prevents progress.
- `Completed` — verified and required documentation/recordkeeping is finished.

A checked checkbox means completed, not merely generated.

## Implementation evidence

After implementation a task should resemble:

```markdown
### TASK-003 — Consume reset token
Status: Verified

Implementation:
- `src/auth/reset.py:44-91` — `consume_reset_token()` validates and consumes one-time tokens.
- `src/api/password.py:71-109` — `reset_password()` exposes the operation.

Tests:
- `tests/auth/test_reset.py:83-151` — expiration, one-time use, invalid token, success.

Verification:
- `pytest tests/auth/test_reset.py`: passed
- Acceptance criteria: satisfied

Architecture impact:
- None; uses existing auth and persistence boundaries.

Commit:
- `abc1234`
```

Line numbers are navigation aids and can drift; symbols and commits provide more stable references. Agents must never invent any of these values.

## Architecture governance

`architecture/CONTRACT.yaml` is the structural source of truth. Routine implementation inside approved boundaries proceeds autonomously.

By default these are protected decisions: new deployable services, datastores, message brokers, external system dependencies, authentication/authorization architecture changes, cross-component data ownership changes, and bypasses of component boundaries.

An agent may analyze and propose a protected change, including drafting an ADR, but must not treat it as approved.

## ADRs

Material architectural reasoning belongs in `architecture/decisions/`. ADRs record context, decision/proposal, alternatives, consequences, affected components, status, and related tasks.

## Skills included

- `feature-planning` — feature description → repository-aware task plan.
- `task-implementation` — authorized task IDs → scoped implementation.
- `implementation-verification` — independent evidence-based verification.
- `architecture-review` — contract/boundary review and ADR escalation.
- `documentation-maintenance` — synchronize durable documentation.
- `task-handoff` — make work resumable without chat history.

## Local overrides

Use:

```text
.agentic-local/
├── AGENTS.md
└── skills/
    └── task-implementation/
        └── SKILL.md
```

Do not edit the managed copy to customize one project.

Intended precedence is: current explicit human instruction → project instructions → local overrides → project architecture/policies → framework defaults. Product-specific agent discovery varies, so root `AGENTS.md` explicitly directs agents to these sources.

## Updating

The project pins `.agentic/VERSION`; it never follows the framework repository automatically.

```bash
python3 /path/to/framework/cli/agentic_starter.py status /path/to/project
python3 /path/to/framework/cli/agentic_starter.py update /path/to/project --dry-run
python3 /path/to/framework/cli/agentic_starter.py update /path/to/project
git diff -- .agentic
```

`update` replaces **only** `.agentic/`. Review the diff, run validation/tests, then commit the upgrade, e.g.:

```text
chore(agentic): upgrade framework 0.1.0 -> 0.2.0
```

This makes changes to the rules governing coding agents explicit and auditable.

## Versioning

Use semantic versioning:

- PATCH: compatible fixes/clarifications.
- MINOR: compatible skills/capabilities.
- MAJOR: workflow/schema changes requiring migration.

Update `CHANGELOG.md` for releases; major releases should include migration instructions.

## Validation

Inside an installed project:

```bash
python3 .agentic/scripts/validate_project.py
```

This checks framework/project structure and basic task-reference integrity. It does not prove application correctness. CI should additionally run application tests, type checks, linting, security analysis, builds, and architecture checks appropriate to the technology stack.

## Communication contract

Before implementation, agents report authorized task IDs, material assumptions, blockers, and protected architecture concerns.

After implementation, agents report implemented/unimplemented tasks, verification actually performed, architecture/documentation impact, unresolved risks, and the path to the durable task record. Routine command narration is unnecessary.

## Human vs agent responsibility

The human owns product intent, protected architectural decisions, risk acceptance, verification sufficiency, and production release policy. Coding agents own implementation mechanics within authorized scope. Deterministic controls (CI, branch protection, dependency rules, security scanners) should enforce what can be enforced; prose instructions should not be the only control.

## Typical session

```text
Human: Add password reset and generate the TODO list.
Agent: Inspects repository; creates tasks/active/password-reset.md; no code changes.

Human: Implement TASK-001 through TASK-004.
Agent: Implements only those tasks, tests them, updates task evidence.

Human: Verify the implementation.
Verifier: Re-checks acceptance criteria, code, tests, architecture and references;
          corrects the task record and reports unresolved issues.
```

That loop is the central process the framework enforces.
