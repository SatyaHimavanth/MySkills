# Scale Tiers — Shared

## Purpose

Most projects using this skill follow one growth path: build and validate locally, launch to a small internal/beta audience, then — only if that audience actually grows — expand to more regions or worldwide. This file makes that path an explicit, named set of tiers so an agent never jumps straight from "local laptop" reasoning to "global multi-region" infrastructure (or the reverse: never leaves small-team production accidentally coupled to single-process assumptions that would make later scaling a rewrite).

This file governs **application-level scale decisions only** (process count, replica count, database topology, cache/session sharing, CDN usage). It does not cover cloud-provider provisioning (VPC, IAM, managed service setup, autoscaling group configuration, DNS/anycast setup) — that belongs to the relevant cloud-provider skill (AWS, GCP, Azure, etc.). See "Boundary with cloud-provider skills" below.

## The three tiers

| | Tier 0 — Local Dev | Tier 1 — Small-Team Production (default launch target) | Tier 2 — Regional / Global Scale |
|---|---|---|---|
| Audience | 1 developer / CI | ~100–1,000 authenticated users, one internal org | Public, growing beyond one region's comfortable latency/capacity |
| Tenancy | Single-tenant | **Single-tenant by default** — one internal org per deployment. Do not add `tenant_id` columns, RLS policies, or tenant-context middleware unless the project actually serves multiple orgs from one deployment; see `database/multi_tenancy.shared.md` | Single- or multi-tenant, decided by the actual business requirement, not by scale alone |
| Process topology | 1 FastAPI process | 1 FastAPI app, 2+ replicas/workers behind a single load balancer, single region | Multiple regions, each with its own replica set |
| Database | Local PostgreSQL (or SQLite only if explicitly chosen) | Single managed PostgreSQL primary (+ optional single read replica if measured read load justifies it), one region | Primary + regional async read replicas, `database/multi_region.shared.md` applies in full |
| Cache/session state | In-memory (`PARTIAL`) is acceptable for solo dev | Shared Redis **required** the moment there is more than one replica — see `architecture/complexity.shared.md`'s escalation test | Same shared Redis pattern, now potentially region-local with cross-region invalidation strategy |
| CDN / edge / anycast DNS | Not applicable | Not required — a single regional load balancer is sufficient for 100–1,000 users | Introduce when latency to distant users or edge caching of static assets is a measured problem |
| Object storage | Local filesystem (`PARTIAL`) is acceptable | Shared object storage (S3-compatible) — required once there is more than one replica, regardless of user count | Same interface; may add regional buckets/replication |
| Observability | Console logs | Structured JSON logs + basic metrics + alerting on the one thing that would page someone (`operations/*.shared.md`) | Add cross-region trace correlation only when cross-service/cross-region debugging is actually needed |

**Tier 1 is the default production target for this skill, not Tier 2.** A project with 100–1,000 internal users does not need a CDN, anycast DNS, multi-region database replicas, or PgBouncer/RDS Proxy connection multiplexing across regions. Building those in anyway is exactly the "adding infrastructure speculatively" anti-pattern in `architecture/complexity.shared.md`. Read `deployment/topology.shared.md` and `database/multi_region.shared.md` as **Tier 2 reference material**, not as the shape every production deployment must take.

## Why Tier 0 → Tier 1 should be a small diff

Because Tier 0 already uses PostgreSQL, Pydantic Settings, the same layered architecture, and the same API/auth contracts as Tier 1 (per `architecture/complexity.shared.md`), promoting from local dev to small-team production should change:

- infrastructure wiring (managed Postgres URL, Redis URL, object storage credentials) via `configuration/shared.md`
- replica count (1 → 2+) and the load balancer in front of them
- secrets source (`.env` → secret manager, per `security/secrets.shared.md`)
- TLS termination and CORS origin allowlist (`security/cors.prod.md`)

It should **not** change: route handlers, service-layer business logic, database schema/query semantics, or the API contract. If a promotion requires touching those, the local architecture skipped a required seam — treat it as a defect in the local build, not a normal cost of shipping.

## Tier 1 → Tier 2 escalation gate

Do not add multi-region infrastructure because "production should be global." Escalate only when a concrete signal exists:

- measured latency complaints from users in a distant region
- a compliance/data-residency requirement naming a specific region
- sustained load that a single region's replica count cannot absorb even after vertical scaling and read-replica addition
- a business requirement to serve two or more named regions from day one (in which case, scope this at the project-scoping stage, not mid-flight)

When one of these is real, apply `database/multi_region.shared.md` and `deployment/topology.shared.md` in full, and re-run the escalation test in `architecture/complexity.shared.md` for each new component (CDN, read replicas, cross-region cache, PgBouncer/RDS Proxy) individually — do not adopt the whole multi-region topology as a bundle when only one piece (e.g., a CDN for static assets) is actually justified.

## Boundary with cloud-provider skills

This skill defines what the application needs at each tier (replica count, shared state requirements, health-check contracts, connection budgets). It deliberately does not prescribe:

- which cloud provider to use
- how to provision managed PostgreSQL/Redis/object storage (RDS vs Cloud SQL vs self-managed, IAM roles, VPC layout)
- autoscaling group / Kubernetes cluster setup
- DNS, anycast, or CDN provider configuration

Hand those off to the project's cloud-provider skill (AWS, GCP, etc.) once the tier and its concrete infrastructure requirements (from the table above) are known. Passing "we need shared Redis reachable from 2 replicas in one region" to a cloud skill is a Tier 1 request; passing "we need regional read replicas behind anycast DNS in 3 regions" is a Tier 2 request. Getting the tier right first prevents the cloud-provider skill from over- or under-provisioning.

## Forbidden

- defaulting new projects to Tier 2 topology because `deployment/prod.md` mentions replicas and load balancers
- introducing CDN, multi-region DB replicas, or cross-region cache invalidation without one of the Tier 2 triggers above
- adding multi-tenant data-isolation (`tenant_id` columns, RLS, tenant-context middleware) to a Tier 1 single-org deployment without an actual second tenant to isolate
- leaving Tier 1 production on a single replica with in-memory cache/session state (this breaks the moment a second replica is added for availability, and availability — not global scale — is why Tier 1 needs 2+ replicas in the first place)
- treating Tier 0 → Tier 1 promotion as an excuse to change API contracts, database schema conventions, or business logic
