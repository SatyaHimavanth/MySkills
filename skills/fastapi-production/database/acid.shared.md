# ACID and Transaction Correctness

## Purpose
Use PostgreSQL transaction semantics intentionally instead of relying on application guesses.

## Atomicity
A business operation that must succeed or fail together belongs in one transaction.

## Consistency
Enforce durable invariants with primary keys, unique constraints, foreign keys, check constraints, and not-null rules.

## Isolation
PostgreSQL supports Read Committed, Repeatable Read, and Serializable isolation levels. Use the weakest level that satisfies the business invariant and design for serialization/deadlock failures when stronger isolation is used.

## Durability
Do not equate a local test filesystem with production durability. Follow the deployment database's durability/backup policy.

## Example
```text
create order
 + reserve stock
 + create audit record
 = one DB transaction
```

External services are not automatically part of the same atomic transaction.

## Failure and retry implications

Serializable transactions and some stronger concurrency operations can fail because another transaction committed an incompatible result. The application must catch only the known retryable class, roll back, and retry the complete idempotent unit of work with bounded backoff.

## Application invariant rule

Use database constraints for invariants that must survive concurrent requests. An application-only pre-check such as `SELECT ... WHERE email = ?` followed by `INSERT` is not sufficient protection against concurrent duplicates; use a unique constraint and translate the resulting constraint violation into the API contract.
