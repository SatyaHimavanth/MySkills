# Architecture Selection and Complexity Budget — Shared

## Purpose

Keep local development simple without creating a second architecture that must be redesigned for production. Select the smallest architecture that satisfies the settled requirements, then preserve interfaces and correctness semantics so production can add scale or stronger infrastructure without rewriting application logic.

## Core rule

Use **production-shaped semantics, not production-sized infrastructure**.

A local application does not need every production component. It does need the same important contracts, invariants, authorization boundaries, transaction rules, failure semantics, and resource ownership model that production will rely on.

Optimize for:

1. minimal required components now
2. explicit extension seams for components that may be needed later
3. low migration cost from local to production
4. no premature distributed infrastructure

Do not add a dependency, service, queue, cache, abstraction, or deployment component only because production systems sometimes use it.

## Complexity budget

For every new infrastructure component, identify the concrete requirement that makes it necessary.

| Requirement | Start with | Escalate when |
|---|---|---|
| API | one FastAPI process | deployment scale or availability requires multiple workers/replicas |
| Database | PostgreSQL | workload or topology requires additional replicas/partitioning/region strategy |
| Cache | no cache | measured latency/load or a clear cache requirement justifies it |
| Shared cache/rate-limit state | local memory (`PARTIAL`) | multiple workers/replicas must coordinate |
| Background work | direct request path | work is too slow, retryable, failure-isolated, or durable |
| Durable jobs | queue + worker | only when job durability/throughput requires it |
| Transactional event publication | direct publish after commit | DB commit and event publication must be atomic from the business perspective |
| Object storage | local filesystem (`PARTIAL`) | multiple replicas, durability, scale, or external access requires shared storage |
| Service decomposition | modular monolith | independent deployment/scaling/failure boundaries are actually required |
| Distributed tracing/metrics | local console/exporter | production operations need cross-service correlation or durable telemetry |

These are **default starting points**, not hard limits. A different initial choice is valid when requirements, constraints, or an existing platform make it cheaper or safer.

## Escalation test

Before introducing production-grade infrastructure locally, answer all three:

- **Requirement:** What concrete user, workload, reliability, security, or deployment requirement needs it?
- **Semantics:** What application behavior must remain unchanged when the component is replaced or scaled?
- **Promotion path:** How will the local implementation become the production implementation without changing business logic or API contracts?

If the first answer is weak, do not add the component.

If the second or third answer is unclear, introduce or improve the interface/contract before introducing infrastructure.

## Preferred architecture shape

For a typical greenfield service, prefer:

```text
API / transport
    ↓
application services
    ↓
domain rules
    ↓
repositories / infrastructure interfaces
    ↓
PostgreSQL + minimal required infrastructure
```

Keep framework and infrastructure concerns near their boundaries. Do not create layers that have no current responsibility.

A modular monolith is the default starting point unless the requirements explicitly demand separate deployable units.

## Interfaces worth preserving

Create a small interface/seam only when the component is a realistic production replacement point:

- configuration
- object storage
- cache
- outbound integrations
- background jobs
- identity provider
- clock/time source when deterministic testing requires it

Do not create interfaces for every class merely to make the code “enterprise-ready”.

## Local fallbacks

Use the repository's `FULL` / `PARTIAL` / `MOCK` classification:

- `FULL`: semantics sufficiently match the production implementation for the feature being tested
- `PARTIAL`: useful for local development but cannot prove production/distributed behavior
- `MOCK`: isolated unit-test substitute

A `PARTIAL` fallback must preserve the application-facing contract so promotion is configuration/infrastructure work rather than a business-logic rewrite.

## Evidence before escalation

Prefer measured evidence or an explicit requirement over speculative scaling.

Examples:

- Add Redis because the application needs shared state across replicas, not because “production should use Redis”.
- Add a queue because a job must survive process restarts or be retried independently, not because the endpoint is asynchronous.
- Add a circuit breaker because a specific dependency failure mode justifies one, not because every HTTP call needs one.
- Add service decomposition because teams, deployment cadence, scaling, or failure isolation require it, not because the codebase is large.

## Production promotion checklist

Before calling local development production-ready, confirm:

- application contracts are unchanged
- configuration values/secrets are environment supplied
- local-only fallbacks are identified and their limitations are known
- persistence semantics are proven against PostgreSQL
- authorization and tenant boundaries remain intact
- durable state is not trapped in process-local memory or replica-local disk
- timeouts/retries/idempotency are unchanged in meaning
- health/readiness behavior matches the deployment topology
- background work has an explicit durability model
- external dependencies have an explicit failure/degradation policy
- production infrastructure replaces adapters/configuration, not business rules

## Anti-patterns

Avoid:

- adding Redis, Kafka, Celery, Kubernetes, or microservices without a concrete requirement
- creating a “local mode” with different API/database/security semantics
- adding abstraction layers that have no replacement point
- using mocks to claim production behavior has been tested
- scaling architecture before measuring or identifying the constraint
- making local development so different from production that promotion becomes a rewrite

## Decision output

For greenfield or materially changing work, record a short architecture decision in the implementation plan/ADR:

```text
Baseline:
Why this is the smallest sufficient architecture:
Future production seam(s):
What would trigger escalation:
What remains PARTIAL locally:
```

This should be concise. The goal is to make future promotion predictable, not to create documentation overhead.
