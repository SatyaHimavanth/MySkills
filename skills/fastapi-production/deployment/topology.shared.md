# Deployment Topology — Shared

## Purpose

Keep application behavior compatible with multi-worker, multi-replica, and multi-region production deployment topologies without forcing local development environments to reproduce full production scale.

**Scope note:** the multi-region layer of this document is Tier 2 material. Most projects should launch at Tier 1 — small-team production (single region, a handful of replicas) — and only adopt the multi-region pattern below when `architecture/scale_tiers.shared.md`'s escalation gate is actually met. Read the single-process → multiple-workers → multiple-replicas progression as the default path; read the multi-region row as an optional, separately-justified step.

## Production-Shaped Principle

Local development should be production-shaped, not production-sized.

The application architecture must remain correct across:

```text
one process
  ↓
multiple workers (e.g. Uvicorn worker processes)
  ↓
multiple replicas (e.g. Kubernetes pods / ECS tasks)
  ↓
multi-region deployment (Edge CDN → Regional App Instances → DB Primary + Read Replicas)
```

## Statelessness Across Replicas & Regions

Do not keep durable shared correctness state in process memory or replica-local filesystems.

Use shared, multi-region capable state stores:

- **PostgreSQL**: Centralized primary for writes + regional asynchronous read replicas for reads
- **Redis / KeyDB**: Distributed cache, rate limiting, and session state
- **Task Queuing System**: Taskiq / Celery / SAQ for background workers
- **S3 / Cloud Storage**: Object storage for uploaded files and media

## Multi-Region Deployment Topology Pattern

```text
User / Client (Browser / Mobile)
       ↓
Edge CDN / Anycast DNS (Cloudflare / CloudFront)
       ↓
Regional Load Balancers (US-East / EU-Central / APAC)
       ↓
FastAPI Application Instances (Regional App Clusters)
   ├── Read Queries  → Regional Read Replica DB (Low latency read)
   └── Write Queries → Central Primary DB (via PgBouncer / RDS Proxy)
```

## Connection Budgeting Across Replicas & Regions

Every worker process in every container replica opens DB connections.

```text
Max Possible DB Connections = Replicas × Workers × (pool_size + max_overflow)
```

In multi-region deployments, use **PgBouncer** or **RDS Proxy** co-located with application clusters to multiplex database connections and prevent exhausting DB primary connection limits.

## Readiness vs Liveness

- **Liveness Probe**: Asserts the Python ASGI process is running and not deadlocked (`GET /healthz/liveness`).
- **Readiness Probe**: Asserts the app instance can reach mandatory dependencies like PostgreSQL and Redis (`GET /healthz/readiness`). Load balancers must remove non-ready instances from traffic routing.

## Long-Lived Connections (SSE / WebSockets)

SSE and WebSockets require explicit proxy timeout settings, client reconnect handling with backoff, and Redis Pub/Sub for multi-replica event broadcasting.

## Shutdown & Graceful Draining

On SIGTERM, app instances must stop receiving new traffic from the load balancer, complete active requests within the grace period (e.g. 30 seconds), close DB engines, and exit cleanly.

## Forbidden

- storing session state or file uploads on local container disks
- assuming all requests from the same user hit the same container instance (sticky session dependency)
- opening un-pooled database connections across WAN / multi-region links
