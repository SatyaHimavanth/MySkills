# Load Balancing — Production

## Goal

Route traffic only to healthy application instances while preserving request context and application statelessness.

## Rules

- Use readiness to decide whether an instance should receive new traffic.
- Configure trusted proxy addresses explicitly.
- Preserve request/trace IDs through the proxy chain.
- Align request-body, timeout, and streaming limits across proxy and FastAPI.
- Review SSE/WebSocket upgrade and idle timeout settings.
- Do not rely on sticky sessions to compensate for local-memory state.

## Topology

```text
Client
  ↓
WAF/CDN/TLS termination
  ↓
Load balancer
  ↓
FastAPI replicas
  ↓
Shared PostgreSQL / Redis / queue / object storage
```

## Failure behavior

When readiness fails:

```text
readiness failure
  ↓
remove instance from new traffic
  ↓
drain/terminate according to policy
```
