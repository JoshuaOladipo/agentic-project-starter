---
name: architecture-review
description: Use when planning or reviewing structural changes, component dependencies, new services, databases, public interfaces, or architectural drift.
---
# Architecture review
1. Compare `architecture/CONTRACT.yaml`, `architecture/README.md`, relevant ADRs, and the actual implementation.
2. Map affected components, dependencies, interfaces, data ownership, trust boundaries, operational consequences and alternatives.
3. Separate verified findings from assumptions; identify contract violations and missing evidence.
4. For protected changes, draft `docs/templates/ADR.md` with options, tradeoffs, migration and rollback; leave status Proposed.
5. Do not approve your own ADR or modify policy to accommodate a violation. Escalate for explicit human approval.
6. After approval, ensure contract, diagrams, tests and implementation agree; report any remaining drift.
