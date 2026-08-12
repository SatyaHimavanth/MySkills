# Database Performance — Production

## Purpose
Control latency, connection pressure, and query-plan regressions in production.

## Rules
- Monitor slow-query latency and DB connection pressure.
- Review query plans with representative production-like data before high-impact changes.
- Size indexes for actual access patterns.
- Avoid unbounded queries and expensive per-request counts.
- Recheck plans after major data-volume/schema changes.

## Query-plan operations

Use PostgreSQL `EXPLAIN`/`EXPLAIN ANALYZE` for slow-query diagnosis. Review actual row counts, execution time, buffer activity, join strategy, and estimated-vs-actual selectivity.

`ANALYZE` updates planner statistics. Large schema/data changes should trigger the normal PostgreSQL statistics/maintenance workflow rather than assuming old plans remain ideal.

## Regression prevention

For important queries, keep a representative benchmark or query-plan test where practical. Review performance after:

- major data growth
- index changes
- schema changes
- new filters/sorts
- ORM relationship changes

## Database saturation

Query performance is not only execution time. Monitor:

- active connections
- waiting connections
- transaction duration
- lock waits
- query latency
- I/O pressure

Use these signals together when diagnosing database saturation.

## Operational safety

Do not run `EXPLAIN ANALYZE` against destructive statements on production tables without a controlled procedure because `EXPLAIN ANALYZE` executes the statement. Prefer a read-only equivalent for investigation, or use a transaction that can safely be rolled back where supported and operationally appropriate.

## Index review

Before adding an index, verify the query pattern, selectivity, write overhead, storage impact, and whether an existing composite index can satisfy the access path. Before dropping an index, verify production query usage and workload evidence.
