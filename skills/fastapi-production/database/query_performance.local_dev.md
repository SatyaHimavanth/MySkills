# Database Performance — Local Development

## Purpose
Keep local query optimization meaningful without pretending local data size equals production.

## Rules
- Use representative data when testing query plans.
- Prefer local PostgreSQL for integration/performance diagnosis.
- Small local pools are fine, but query shape should remain production-compatible.
- Run `EXPLAIN` for suspected slow queries.
- Do not use SQLite to prove PostgreSQL query-plan or locking behavior.

## Representative testing

Small local datasets can hide planner and index problems. For meaningful performance work, create representative row counts/distributions and run `ANALYZE` before comparing plans.

## Safety

`EXPLAIN ANALYZE` executes the statement. Do not use it against mutating statements casually; use a transaction and roll back when a safe analysis is required.

## Query profiling

When diagnosing a slow endpoint, separate:

```text
API latency
  ├── serialization
  ├── DB connection acquisition
  ├── query execution
  ├── external calls
  └── application processing
```

Do not call a query slow merely because the endpoint is slow. Instrument the boundaries first.

## Pooling

Local pool sizes can be small. They should still exercise the same SQLAlchemy pooling architecture as production unless the user explicitly chose a different local topology.
