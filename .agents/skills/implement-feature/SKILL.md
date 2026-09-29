---
name: implement-feature
description: Use when implementing an approved feature or bug fix with tests, architecture compliance, and a structured handoff.
---
# Implement feature
1. Read `AGENTS.md`, the product brief, architecture contract, commands, and relevant ADRs.
2. Convert the request into observable acceptance criteria; classify changes under `docs/engineering/CHANGE_POLICY.md`.
3. For protected architecture decisions, propose an ADR and stop until human approval.
4. Implement the smallest coherent change using existing conventions. Add independent tests for normal, failure, boundary, and authorization cases.
5. Update affected product, API, architecture, and operations docs in the same change.
6. Run configured checks and report actual results; never represent missing checks as passing.
7. Deliver the completion format in `docs/engineering/COMMUNICATION.md`.
