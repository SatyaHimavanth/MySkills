# Database Query Performance

## Purpose
Prevent slow or unbounded SQLAlchemy queries and N+1 loading.

## Rules
- Filter/order/page in PostgreSQL, not in Python, for large datasets.
- Return only required columns when payload size matters.
- Inspect relationship loading explicitly.
- Use `selectinload` for many collection-loading cases when appropriate.
- Use `joinedload` deliberately and understand result de-duplication requirements.
- Use `raiseload` during development for relationships that must not trigger hidden lazy SQL.
- Avoid N+1 query patterns.
- Measure before optimizing.

## EXPLAIN
For slow PostgreSQL queries use:
```sql
EXPLAIN (ANALYZE, BUFFERS)
SELECT ...;
```
Do not optimize from query text alone; inspect actual plans and representative data.

## Relationship loading

SQLAlchemy documents `selectinload()` as a SELECT-IN eager-loading strategy and `joinedload()` as joined eager loading. Choose based on relationship cardinality and query shape. If joined eager loading is used for collections, account for result de-duplication as required by SQLAlchemy's current API.

## Statistics

PostgreSQL's planner depends on table statistics. `ANALYZE` updates planner statistics. Query-plan investigations should therefore use representative data and reasonably fresh statistics rather than a tiny empty local database.
