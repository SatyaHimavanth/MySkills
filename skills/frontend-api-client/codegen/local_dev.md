# Client & Schema Generation — Local Development

## Regeneration
Regenerate whenever the backend's routes/schemas change — this is a local dev-loop step, not a one-time setup step. Add an npm script:
```json
{ "scripts": { "gen:api": "orval" } }
```
Run it after pulling backend changes, before assuming a type error is a frontend bug — it might just be a stale generated client.

## Pointing at a local backend
`input` in `orval.config.ts` should point at the actual running local backend (e.g. `http://127.0.0.1:8000/openapi.json` — matches `deployment/local_dev.md` in `fastapi-production`). If the backend isn't running, codegen fails at the network call, not with a misleading schema error — check the backend is up first.
