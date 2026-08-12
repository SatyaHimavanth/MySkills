# SLOs, SLIs, and Error Budgets — Shared

## Purpose

Turn reliability from an opinion into measurable service objectives.

Google SRE defines SLOs as target reliability levels and uses error budgets to balance reliability work against release velocity. [Certain] See the Google SRE Workbook. 

## SLI vs SLO

### SLI

A measured indicator of user-visible service behavior.

Examples:

- successful request ratio
- latency within a threshold
- freshness of asynchronous processing
- successful job completion ratio

### SLO

A target for the SLI over a defined window.

Example:

```text
99.9% of eligible API requests succeed over 28 days
95% of requests complete within 500 ms
```

Do not choose targets before deciding what users actually need.

## Good API SLIs

Availability:

```text
successful eligible requests / total eligible requests
```

Latency:

```text
requests <= threshold / eligible requests
```

Exclude deliberate client errors only when the service definition explicitly says they are not service failures. Do not casually exclude `5xx`, dependency failures, or server timeouts.

## Error budget

```text
error budget = 1 - SLO
```

For a 99.9% availability SLO over a window, the theoretical error budget is 0.1% of eligible traffic/time. Google SRE uses error budgets to decide how much change/reliability risk is acceptable. [Certain]

## Release policy

Define a policy such as:

```text
budget healthy
    → normal releases

budget materially consumed
    → additional reliability review

budget exhausted
    → restrict risky changes until recovery
```

The exact thresholds belong to the organization; the skill must not invent a universal percentage.

## Alerting

Prefer SLO/error-budget alerts over alerting on every low-level symptom.

Also alert directly on critical saturation signals:

- DB connection exhaustion
- queue backlog
- repeated readiness failures
- dependency outage
- memory exhaustion

## Per-endpoint vs service SLOs

Do not create a separate SLO for every route by default.

Start with a service-level objective, then add endpoint-specific objectives only when business criticality or failure characteristics justify them.

## Local development

Local development normally does not need formal SLO enforcement.

It should still expose the same metrics needed to validate the production SLI implementation.

## Forbidden patterns

- setting `99.999%` because it sounds professional
- defining SLOs without a user-visible SLI
- alerting on every exception
- excluding failures solely to make the SLO look healthy
- treating an SLO as a guarantee rather than an operating target
