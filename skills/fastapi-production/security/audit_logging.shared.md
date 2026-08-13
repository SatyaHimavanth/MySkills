# Audit Logging — Shared

## Purpose
Answer "who did what, to which record, when" — distinct from `observability/shared.md`'s operational logs (latency, status, request_id), which don't preserve this by default and aren't append-only.

## Two layers, use both
- **DB-level (pgAudit)**: PostgreSQL extension logging statement-level activity through the standard log facility. Use for compliance (SOC2/PCI-DSS/HIPAA) and DBA-level accountability. Best-effort/non-transactional (not guaranteed to survive a crash the way committed data is) and cannot reliably audit superusers — restrict superuser access separately.
- **Application-level (event table)**: business-semantic trail an auditor or support engineer can actually read — "user X approved invoice Y", not raw SQL. pgAudit alone can't produce this.

## Application audit table
```text
audit_events
  id, occurred_at, actor_id, actor_type, action, resource_type, resource_id,
  tenant_id (if multi-tenant), before_state, after_state, request_id, ip_address
```
Write audit events in the same DB transaction as the business mutation (same atomicity reasoning as `database/acid.shared.md`) — an audit record that didn't actually happen is worse than none.

## Immutability
No `UPDATE`/`DELETE` grants on `audit_events` for the application role. Use a separate retention/archival job, not row deletion by request handlers.

## Forbidden
- relying on operational request logs as the audit trail
- audit event writes outside the business transaction
- application role with UPDATE/DELETE on audit_events
- logging full request/response bodies as "audit" without redacting secrets/PII
