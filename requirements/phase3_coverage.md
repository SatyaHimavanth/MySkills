# Phase 3 Coverage

| Requirement | Primary file(s) | Local | Production | Verification |
|---|---|---:|---:|---|
| Idempotency | `async/idempotency.shared.md` | `async/local_dev.md` | `async/prod.md` | PASS |
| Durable background jobs | `async/jobs.shared.md` | `async/local_dev.md` | `async/prod.md` | PASS |
| Application lifespan/resource ownership | `reliability/lifespan.shared.md` | `reliability/lifespan.local_dev.md` | `reliability/lifespan.prod.md` | PASS |
| Outbound HTTP clients/retries | `http/clients.shared.md` | `async/local_dev.md` | `async/prod.md` | PASS |
| Streaming/SSE/WebSockets | `streaming/shared.md` | `async/local_dev.md` | `async/prod.md` | PASS |
