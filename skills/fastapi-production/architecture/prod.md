# Architecture: Production

## Purpose

Keep production implementation constraints explicit.

## Rules

- Prefer stateless application processes.
- Assume multiple workers or replicas may exist.
- Expect externalized state for database, cache, queue, file storage, and secrets.
- Require readiness/health signaling suitable for orchestration or load balancers.
- Keep implementation compatible with deployable environments that may terminate and restart processes.

## Production influences on local development

- Avoid process-local shared state for anything that must survive multiple workers.
- Avoid cache/session logic that depends on one process.
- Design for explicit timeouts and graceful shutdown.
