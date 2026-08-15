# Multi-Tenant Isolation — Shared

## Purpose
Prevent tenant B from reading or writing tenant A's data. Same vulnerability class as `security/object_authorization.shared.md` (BOLA), one level up.

## Isolation models
- **Shared tables + `tenant_id` column** (default): simplest ops, cheapest, requires discipline on every query.
- **Schema-per-tenant**: stronger DB-level isolation, migration fan-out cost (N schemas to migrate).
- **Database-per-tenant**: strongest isolation, highest ops cost. Use only when compliance requires it.

Pick one per project; do not mix.

## Query-level enforcement (shared-table model)
Same rule as object authorization: filter by `tenant_id` in the query itself, never fetch-then-compare in application code.

```python
async def get_for_tenant(self, resource_id: UUID, tenant_id: UUID) -> Resource | None:
    stmt = select(Resource).where(Resource.id == resource_id, Resource.tenant_id == tenant_id)
    return (await self.session.execute(stmt)).scalar_one_or_none()
```

Every table holding tenant-scoped data needs a non-nullable `tenant_id` FK, indexed, and included in every unique constraint that must be unique per-tenant rather than globally.

## Defense in depth: RLS
For the shared-table model, enable PostgreSQL Row-Level Security as a second layer independent of application code, so a missed `WHERE tenant_id = ...` in a new endpoint doesn't silently leak data:

```sql
ALTER TABLE tasks ENABLE ROW LEVEL SECURITY;
CREATE POLICY tenant_isolation ON tasks
  USING (tenant_id = current_setting('app.current_tenant')::uuid);
```

Set `app.current_tenant` per-connection/transaction from the authenticated request context.

**This only works if the application's DB role is NOT a superuser and does NOT have `BYPASSRLS`.** Verified directly: connecting as `postgres` (superuser, `rolbypassrls = t`) returned every tenant's rows with zero filtering, even with `app.current_tenant` completely unset — the policy silently does nothing for that role, with no error, no warning, and `\d tablename` still showing RLS as enabled. This is the single most important precondition for this section and the easiest to miss, because everything *looks* correctly configured right up until a real cross-tenant leak in production. Create a dedicated non-superuser application role (`CREATE ROLE app_role LOGIN; GRANT ...` — not `BYPASSRLS`) and connect as that role, never as the migration/admin role.

**The unset-tenant-context failure mode is fail-closed either way, but by different mechanisms — prefer the strict one.** Verified both: `current_setting('app.current_tenant')` (no second argument) with the variable unset raises a hard Postgres error (`unrecognized configuration parameter`) — every query fails loudly, impossible to miss in testing. `current_setting('app.current_tenant', true)` (the "safer-looking" missing_ok variant) instead evaluates to `NULL`, and `tenant_id = NULL` is never `TRUE` in SQL, so it also returns zero rows rather than leaking — but silently, indistinguishable from "this tenant legitimately has no data," which is a worse debugging experience for the same safety outcome. Use the strict form (no `missing_ok`) so a forgotten `SET app.current_tenant` in application code fails loudly instead of quietly looking like an empty result set.

## Tenant context propagation
Resolve tenant identity once (subdomain, header, or JWT claim) at the request boundary and pass it explicitly through service/repository calls — do not re-derive it deeper in the call stack, and never trust a tenant ID supplied directly in a request body.

## Cross-cutting resources
Background jobs, cache keys, rate-limit keys, and file storage paths must all be tenant-scoped too — the same class of leak that hits a DB query can hit a Redis key (`tasks:{tenant_id}:{...}`) or an S3 prefix.

## Testing
Every endpoint needs a cross-tenant test: tenant A creates a resource, tenant B attempts to read/update/delete it by ID, must receive 404 (not 403 — don't confirm existence), same pattern as `security/object_authorization.shared.md`'s BOLA tests.

## Forbidden
- filtering by tenant in application code after an unscoped query
- trusting a client-supplied `tenant_id`
- tenant-unscoped cache keys, rate-limit keys, or storage paths
- mixing isolation models within one project without a documented reason
- connecting as a superuser or `BYPASSRLS` role while relying on RLS for isolation — verified this silently disables the policy entirely, with no error and no visual indication anything is wrong
