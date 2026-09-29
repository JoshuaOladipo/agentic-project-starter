# Change classification and approval

## Routine (agent may implement and prepare PR)
Localized behavior, tests, bug fixes, documentation and refactors that preserve approved architecture, public interfaces, permissions, and data invariants. Normal PR checks and configured review rules still apply.

## Review required before merge
New external dependencies, material performance/cost impact, schema changes, new data collection, security-sensitive behavior, significant cross-component refactors. Explain impact, tests, rollback, and reviewer requirements.

## Explicit human approval before implementation of the protected decision
New service/database/queue, new cross-boundary dependency, auth architecture change, breaking public API, irreversible migration, production infrastructure changes, permission expansion, changes to agent/CI/security policy. Write a proposed ADR with alternatives and tradeoffs. Do not mark it Accepted yourself.

## Never autonomous
Production deployment or writes, deleting production data, credential rotation, bypassing branch protection, accepting risk on behalf of the owner, or approving/merging one's own protected change. Require separate, explicit authorization and independent enforcement.

## Enforcement
Branch protection, CODEOWNERS, CI and scoped credentials are the actual controls. Agent instructions and AI reviews are advisory. Do not grant an agent administrative repository permissions or production credentials.
