# Phase 2 Coverage

| Requirement | Files | Status |
|---|---|---|
| ACID / transactions / isolation | `database/acid.shared.md`, `database/transactions.shared.md` | COMPLETE |
| Concurrency control | `database/concurrency.shared.md` | COMPLETE |
| Optimistic/pessimistic locking | `database/concurrency.shared.md`, `database/acid.shared.md` | COMPLETE |
| Query performance / N+1 | `database/query_performance.shared.md` | COMPLETE |
| EXPLAIN/query-plan workflow | `database/query_performance.shared.md`, `database/query_performance.local_dev.md`, `database/query_performance.prod.md` | COMPLETE |
| Index design | `database/query_performance.shared.md`, `database/postgresql.shared.md` | COMPLETE |
| PostgreSQL-specific types/features | `database/postgresql.shared.md` | COMPLETE |
| Local/prod performance behavior | `database/query_performance.local_dev.md`, `database/query_performance.prod.md` | COMPLETE |

## Verification requirements

A Phase 2 audit must confirm that all referenced files exist and each policy contains purpose, rules, examples, and forbidden patterns or an equivalent validation section.
