# Deployment — Production

## Purpose

Define the production runtime configuration, ASGI server setup, and process management for deploying FastAPI applications.

**Default scope:** the guidance below targets Tier 1 — small-team production (single region, a handful of replicas, ~100–1,000 users) per `architecture/scale_tiers.shared.md`. It applies just as well underneath Tier 2, but nothing here requires multiple regions, a CDN, or anycast DNS — those are separate, gated decisions, not part of the default production baseline.

## Rules

- Assume a reverse proxy / load balancer (Nginx, Caddy, ALB) sits in front of FastAPI.
- Assume multiple workers or replicas unless the deployment explicitly guarantees one process.
- Keep application state shared/durable outside process memory when replicas must see it.
- Use graceful shutdown and explicit dependency/request timeouts.
- Keep runtime configuration externalized via Pydantic Settings.
- Use readiness for traffic routing and liveness for process health.
- Do not use development reload mode (`--reload`).

## Uvicorn Production Configuration

```bash
# Single container with multiple workers (traditional deployment)
uvicorn myapp.main:app \
    --host 0.0.0.0 \
    --port 8000 \
    --workers 4 \
    --loop uvloop \
    --http httptools \
    --log-level info \
    --access-log \
    --timeout-keep-alive 75

# Kubernetes/ECS: single worker per container, scale via replicas
uvicorn myapp.main:app \
    --host 0.0.0.0 \
    --port 8000 \
    --workers 1 \
    --loop uvloop \
    --http httptools \
    --log-level info \
    --timeout-keep-alive 75
```

## Health Check Endpoints

```python
from fastapi import APIRouter, status
from sqlalchemy import text

health_router = APIRouter(tags=["Health"])

@health_router.get("/healthz/liveness", status_code=status.HTTP_200_OK)
async def liveness():
    """Process is alive and responding."""
    return {"status": "alive"}

@health_router.get("/healthz/readiness", status_code=status.HTTP_200_OK)
async def readiness(db: AsyncSession = Depends(get_db_session)):
    """App can reach required dependencies (DB, Redis)."""
    await db.execute(text("SELECT 1"))
    return {"status": "ready"}
```

## Topology
See `deployment/topology.shared.md` for the full multi-region version of this diagram.
```text
Client
  ↓
WAF / CDN / Reverse Proxy / Load Balancer
  ↓
FastAPI instance(s) (Uvicorn workers)
  ↓
PostgreSQL / Redis / Object Storage / Task Queues
```

## Worker / Container Rule

Container-orchestrated deployments commonly use **one Uvicorn process per container** and scale horizontally via container replicas. Single-host deployments may use multiple workers in one container. Choose based on topology and resource budgets.

## Forbidden

- assuming one worker/replica in correctness logic
- storing durable shared state in process memory
- `--reload` in production
- running Alembic migrations from every API worker process
