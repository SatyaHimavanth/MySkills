# PostgreSQL-Specific Design

## Purpose
Use PostgreSQL capabilities deliberately while isolating database-specific code.

## Supported patterns to consider
- UUID identifiers
- JSONB for genuinely document-like fields
- ARRAY where the relationship/model requires it
- enum types when a DB-level enum is appropriate
- `ON CONFLICT` for atomic upsert behavior
- `RETURNING` for generated values
- partial/expression/composite indexes
- advisory locks when a real DB-scoped lock is appropriate

## Rules
- Prefer PostgreSQL constraints over duplicated application checks.
- Keep PostgreSQL-specific SQL in repository/database modules.
- Do not add a PostgreSQL feature merely because it exists; document why it solves the requirement.
- Test PostgreSQL-specific behavior against PostgreSQL.

## Do not overuse database-specific features

PostgreSQL-specific features are valid design choices when they solve a real requirement, but they reduce portability. Isolate them in repository/database modules and document the reason for using them.

## Upserts

Use `INSERT ... ON CONFLICT` when the business operation is an atomic insert-or-update requirement. Do not emulate it with a separate existence query plus insert/update under concurrency.

## Index selection

Choose indexes from actual access patterns. Consider:

- equality predicates
- range predicates
- sort order
- join keys
- partial conditions
- covering/index-only access

Avoid indexing every column. Indexes add write cost and storage cost and may not be useful for low-selectivity predicates.

## PostgreSQL extensions

Extensions can be valuable but are operational dependencies. If one is required, record:

- extension name/version expectation
- how it is installed in local/dev/prod
- migration implications
- backup/restore implications
- managed-PostgreSQL support

Do not assume a managed PostgreSQL service permits every extension available in self-managed PostgreSQL.
