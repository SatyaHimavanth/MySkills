# Final Content and Consistency Audit

Date: 2026-08-16

## Results

The current authoritative tree was inspected for:

- broken or stale `SKILL.md` references
- missing requirement files
- shared/local/prod structural completeness
- internal/non-portable citation markup
- contradictory SQLite/PostgreSQL defaults
- durable-vs-in-process background-job confusion
- reload/production contradictions

## Follow-up pass (same date)

A second review found and corrected:

- Duplicate outbound-HTTP-client policy folders (`http/` and `http_client/`) covering the same content. `http_client/` removed; `http/clients.shared.md` is now the single source. All internal references updated.
- Stale path references across `requirements/*.md` and `verify_phase3.py` pointing to nonexistent files (`database/performance.local_dev.md` / `.prod.md` instead of `database/query_performance.*`, `middleware.shared.md` instead of `middleware/shared.md`, and the now-removed `http_client/shared.md`). All corrected to the actual file paths.
- `full_file_audit.md` incorrectly listed `.dev/environment.local.md` as a tracked release file with fabricated byte/line counts. It is a runtime artifact the coding agent creates in the consumer's project, not a shipped file — the row was removed and a note added explaining why.
- Missing scale-tier guidance: the skill's `prod.md`/`topology.shared.md`/`multi_region.shared.md` files presented single-region and multi-region production as one undifferentiated path, with no explicit default or escalation gate between them. Added `architecture/scale_tiers.shared.md` defining Tier 1 (small-team production, ~100–1,000 users, single region — the default) and Tier 2 (regional/global, gated on a concrete trigger), wired into `SKILL.md`'s workflow/routing/principles, `checklists/production-readiness.md`, and cross-referenced from the topology and multi-region files so they're read as Tier 2 material rather than the default shape.
- Added an explicit scope boundary against cloud-provider skills (AWS/GCP/etc.): this skill defines application-level tier requirements; cloud provisioning is deferred to the relevant cloud skill.

## Follow-up pass 2 (same date)

Confirmed with the project owner: Tier 1 (small-team production) is single-tenant — one internal org per deployment. Updated `architecture/scale_tiers.shared.md` to state this as the explicit default (was previously ambiguous, hedging between "one org or a small set of orgs"), added it to the tier table and the Forbidden list, added a matching scope note to `database/multi_tenancy.shared.md` marking multi-tenancy as opt-in rather than default, and tightened the corresponding line in `checklists/production-readiness.md` so it points at the default instead of a bare "if applicable."

## Follow-up pass 3 (same date) — built and tested a real app against both skills

Built a real FastAPI app (auth: register/login, Argon2id + JWT, layered architecture, domain exceptions, in-process rate limiting, health/readiness) and a real frontend client generated with Orval against the live `/openapi.json`, per `frontend-api-client`'s documented workflow. Ran the full stack end-to-end (pytest against the backend; a live Node script exercising the generated TS client against the running server, not mocks). Four real defects/gaps surfaced and were fixed in both the app and the skill docs:

1. **OpenAPI schema omits custom exception-handler status codes** (the highest-impact finding). A `@app.exception_handler(DomainError)` returning 409/401/429 is correct at runtime but those codes never appeared in `/openapi.json` — confirmed by inspecting the live schema before and after. This silently broke `frontend-api-client`'s core promise (generated types catch contract drift): the generated error type for `/auth/register` was `HTTPValidationError` only, no compile-time signal that a 409 could happen. Fixed by declaring `responses=` per route; re-ran `npx orval` and confirmed the generated union became `ErrorResponseSchema | HTTPValidationError`. Documented in `api/response_contracts.shared.md` and mirrored in `frontend-api-client/codegen/shared.md` + `error-handling/shared.md`.
2. **Argon2id hashing blocks the event loop if not offloaded.** Measured hash time directly (~150ms). `security/passwords.shared.md` documented the CPU-DoS angle but never said to offload via `run_in_threadpool`. Added, with the caveat that offloading fixes responsiveness, not throughput (still CPU-core-bound).
3. **Rate-limiter DI gap breaks its own required tests.** `testing/security.shared.md` requires testing "independent principals" and "reset/expiry" for rate limits, but nothing said the limiter needs to be behind a `Depends` provider to make that resettable. Hit this directly: a bare module-level limiter leaked state across test functions in the same process. Fixed by adding the provider pattern to `security/ratelimiting.shared.md`/`.local_dev.md`, plus a verified gotcha (a test override that constructs a new instance per call silently defeats the limiter — the count never accumulates).
4. **Example dev JWT secret too short.** The documented `development-only-secret` placeholder (23 bytes) trips PyJWT's `InsecureKeyLengthWarning` for HS256 (32-byte minimum) — confirmed via the actual warning in test output. Fixed the example and added a Forbidden entry in `security/authentication.local_dev.md`.

All four fixes were verified working (not just written) before being committed to the skill files: reran the affected pytest suite and/or `npx orval` after each fix and confirmed the expected before/after change.

## Corrections

- per-request infrastructure-client anti-patterns
- stale historical counts in coverage/audit files
- Added the missing middleware, networking, CORS, security-header, cache, pooling, topology, authentication local/prod, rate-limit local/prod, and checklist files referenced by the requirement matrix.
- Replaced the root `SKILL.md` with a complete routing index for all implemented capability areas.
- Updated the requirements matrix to current file paths.
- Removed non-portable citation markup from skill files and added durable source URLs.
- Strengthened previously shallow shared policies.

## Gates

Run all gates before packaging:

```bash
python requirements/verify_coverage.py
python requirements/verify_phase1.py
python requirements/verify_phase2.py
python requirements/verify_phase3.py
python requirements/verify_phase4.py
python requirements/verify_phase5.py
python requirements/verify_phase6.py
python requirements/verify_phase7.py
python requirements/content_quality_audit.py
```

The gate should be supplemented by human review of security-critical architecture before deploying a generated backend.


## Architecture-quality upgrade

- Added `architecture/complexity.shared.md` as the explicit complexity-budget and local-to-production promotion gate.
- Greenfield/materially ambiguous work now resolves scope before implementation and then selects the smallest sufficient architecture.
- The `grill-me` integration now follows the upstream one-question-at-a-time interview model and avoids duplicating its interrogation mechanism.
- Clarified that production-shaped means semantic/contract parity, not production-sized local infrastructure.
- Added escalation triggers for Redis, queues, object storage, service decomposition, and distributed topology to reduce premature infrastructure.
- Corrected the Phase 2 verifier's stale query-performance paths.
- Corrected several version-sensitive documentation claims identified during the external fact-check.
