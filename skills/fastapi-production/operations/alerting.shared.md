# Alerting — Shared

## Purpose

Produce actionable alerts that indicate user impact, imminent saturation, or operational failure.

## Alert categories

### Page

Immediate human action is required.

Examples:

- severe sustained availability loss
- database unavailable
- widespread readiness failure
- rapidly exhausting error budget

### Ticket/async attention

Important but not urgent.

Examples:

- elevated dependency latency
- increasing queue backlog
- repeated non-critical job failures

### Dashboard only

Useful context without requiring action.

Examples:

- cache hit rate
- normal request volume
- expected retry rate

## Alert design

Every alert should answer:

```text
What is wrong?
Why does it matter?
How severe is it?
What service is affected?
What should the operator inspect first?
```

## Avoid alert floods

Do not alert independently on dozens of low-level symptoms when one higher-level SLO alert gives a better signal.

Group correlated dependency failures.

## Recommended signals

- SLO/error budget burn
- 5xx ratio
- p95/p99 latency
- readiness failures
- DB pool exhaustion
- queue depth/age
- dependency failure rate
- memory/CPU saturation
- per-endpoint request rate deviating sharply from its own recent baseline (not an absolute count — a login endpoint jumping 50x its normal rate is the leading indicator for `operations/runbooks.shared.md`'s credential-stuffing runbook, and fires before CPU saturation does, which is a lagging signal by the time it pages)

## Alert labels

Keep labels low-cardinality.

Avoid user IDs, request IDs, raw URLs, exception strings, and arbitrary query parameters as metric labels.

## Runbook link

Every actionable production alert should point to the relevant runbook.

Example:

```text
ALERT: APIHighErrorRate
Runbook: docs/runbooks/api-high-error-rate.md
```

## Forbidden patterns

- alerts with no owner
- alerts with no action
- paging on every warning log
- alert conditions based only on absolute traffic counts
- alert labels with unbounded cardinality
