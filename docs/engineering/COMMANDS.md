# Engineering commands

**Unconfigured.** Replace each placeholder with a real command before using agents for implementation. Do not report placeholders as passed checks.

| Check | Command | Required for |
| --- | --- | --- |
| Install | `[CUSTOMIZE]` | Setup |
| Format | `[CUSTOMIZE]` | Changed source |
| Lint | `[CUSTOMIZE]` | Every PR |
| Typecheck | `[CUSTOMIZE]` | Every PR if applicable |
| Unit tests | `[CUSTOMIZE]` | Every PR |
| Integration tests | `[CUSTOMIZE]` | Relevant changes |
| E2E tests | `[CUSTOMIZE]` | Critical journeys |
| Build | `[CUSTOMIZE]` | Every PR |
| Dependency/security scan | `[CUSTOMIZE]` | Every PR |
| Smoke test | `[CUSTOMIZE]` | Before/after release |

Starter-only validation: `python3 scripts/validate_starter.py` and `python3 scripts/validate_tasks.py`. This does not replace any application checks.
