---
name: frontend-api-client
description: Guardrails for TypeScript frontends consuming a typed backend (e.g. FastAPI). Generates a client and runtime validators from the backend's own OpenAPI schema instead of hand-writing request/response types, so contract drift becomes a build error, not a runtime bug.
---

# Frontend API Client — Overview

## Core principle
The backend's OpenAPI schema (e.g. FastAPI's auto-generated `/openapi.json`) is the single source of truth for request/response shapes. Never hand-write TypeScript interfaces or fetch calls describing a backend contract that already has a machine-readable schema — generate from it. This mirrors `fastapi-production`'s own "shared invariant, not duplicated logic" principle, applied across the frontend/backend boundary instead of within one codebase.

Every pattern below was run end-to-end against a real FastAPI backend (real PostgreSQL/Redis, no mocks) before being written down. Three real integration bugs were caught doing that — all are called out explicitly in the relevant files, because they're the mistakes most likely to repeat: a `baseUrl` double-prefix (`codegen/shared.md`), a mutator signature mismatch that silently turned every write into a GET (`codegen/shared.md`, `auth/shared.md`), and a terminal refresh failure that left dead tokens in memory with no app-level signal (`auth/shared.md`).

## Required agent workflow

```text
IDENTIFY the backend's OpenAPI schema URL (e.g. http://localhost:8000/openapi.json)
  ↓
READ codegen/shared.md — generate client + zod schemas, do not hand-write types
  ↓
READ auth/shared.md — token storage and refresh interceptor
  ↓
READ validation/shared.md — when/where to apply zod validation
  ↓
READ error-handling/shared.md — read the backend's actual error shape, don't guess it
  ↓
READ data-fetching/shared.md — TanStack Query usage with the generated hooks
  ↓
CHECK checklists/new-integration.md before wiring a new endpoint
```

## Routing table

| Capability | Files |
|---|---|
| Client/schema generation | `codegen/shared.md`, `codegen/local_dev.md`, `codegen/prod.md` |
| Runtime validation | `validation/shared.md` |
| Auth token handling | `auth/shared.md` |
| Error handling | `error-handling/shared.md` |
| Data fetching / caching | `data-fetching/shared.md` |
| New integration checklist | `checklists/new-integration.md` |

## Global principles
- Generated files (`src/api/client.ts`, `src/api/client.zod.ts` or equivalent) are build artifacts. Never hand-edit them; a hand-edit is silently overwritten on the next regeneration and gives no error when it happens.
- Regenerate in CI (`codegen/prod.md`) so a backend contract change becomes a merge-blocking diff, not a silent frontend bug discovered by a user.
- Types alone are a compile-time guarantee, not a runtime one. A malformed response (backend bug, proxy mangling JSON) still reaches the frontend as `any`-shaped data unless something validates it at the boundary — that's what `validation/shared.md` is for.
