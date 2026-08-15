# New Backend Integration Checklist

- [ ] Backend OpenAPI schema reachable (`/openapi.json`) — confirm before running codegen, not after a confusing failure
- [ ] `npx orval` run, no hand-written types for this endpoint
- [ ] `output.baseUrl` NOT set if backend paths already include a prefix (`codegen/shared.md`)
- [ ] Custom mutator signature matches `(url, RequestInit)`, not a single axios-config object (`auth/shared.md`)
- [ ] Response validated with the generated Zod schema at the boundary, not assumed from the TS type alone
- [ ] Error path handled using the backend's actual generated error shape, not a guessed one
- [ ] Mutations invalidate the matching query cache key
- [ ] 429 responses read `Retry-After` and disable retry for that long — not a silent immediate retry (`error-handling/shared.md`)
- [ ] App listens for `session-terminated` at the top level to clear state and redirect to login — not handled ad hoc per request (`auth/shared.md`, `error-handling/shared.md`)
- [ ] Tokens stored in memory/httpOnly cookie, never localStorage/sessionStorage
- [ ] CI regenerates and diffs the client (`codegen/prod.md`) before this integration ships
