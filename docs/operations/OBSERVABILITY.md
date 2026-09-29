# Observability and operations baseline

Before production release, configure ownership, actionable alerts, dashboards, on-call/escalation and a tested rollback procedure.

## Signals
- Reliability: availability, errors, failed critical transactions, job failures.
- Performance: P50/P95/P99 latency, traffic, saturation, slow queries.
- Security: authentication anomalies, authorization denials, dependency findings and secret alerts.
- Data integrity: domain invariants, reconciliation failures, migration and backup/restore status.
- Costs: cloud/API/model spend, cost per transaction and budget anomalies.
- Product: critical journey completion, frontend failures and feature adoption.

Instrument structured logs, metrics and traces with correlation IDs; scrub secrets and personal data. Set service-specific SLOs and alert thresholds. Document incident response and post-incident follow-up.
