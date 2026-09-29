---
name: incident-investigation
description: Use when investigating production errors, performance regressions, data-integrity issues, security alerts, or unexpected costs without making unapproved production changes.
---
# Incident investigation
1. Establish impact and timeline using available telemetry; minimize access to sensitive data.
2. Preserve evidence and distinguish observed facts from hypotheses. Correlate release versions, traces, logs, metrics, and architectural dependencies.
3. Suggest safe mitigations and rollback options; do not execute production writes or deployments without explicit authorization.
4. Identify tests, alerts, documentation, and architecture changes that would prevent recurrence.
5. Record findings in `docs/templates/INCIDENT.md` and escalate security or data-loss risks immediately.
