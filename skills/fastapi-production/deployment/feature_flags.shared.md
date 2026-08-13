# Feature Flags — Shared

## Purpose
`deployment/rollback.shared.md` already champions expand-and-contract for schema changes — decouple the risky step from the deploy. Feature flags are the same idea applied to code paths: ship code disabled, enable independently of deploy, kill instantly without a rollback deploy if it misbehaves.

## Default: config-driven, no new infra
For most projects, a flag is a boolean in Settings, evaluated in code — no new service:

```python
class FeatureFlags(BaseModel):
    new_pricing_engine: bool = False

# usage
if settings.flags.new_pricing_engine:
    ...
```
Sufficient for on/off per-environment rollout. Insufficient for per-user targeting, percentage rollout, or a non-engineer toggling flags without a deploy — that's the signal to move up, not a reason to build it yourself.

## Scale-up: Unleash
Self-hosted, open source, real Python SDK, when per-user/percentage targeting or a UI for non-engineers is actually needed. Real ongoing cost, not free to add: expect meaningful integration time per service plus regular maintenance (DB backups, SDK version bumps, its own uptime to monitor) — same "measure before adding infrastructure" reasoning as `async/outbox.shared.md`'s CDC step. Don't add this pre-emptively.

```python
from UnleashClient import UnleashClient

client = UnleashClient(url=settings.unleash.url, app_name="api")
client.initialize_client()

if client.is_enabled("new-pricing-engine", fallback_function=lambda ctx: False):
    ...
```
Always provide a fallback — a flag service being unreachable must degrade to a known-safe default, not fail the request.

## Testing
Every flag needs both states tested (`testing/api.shared.md`), not just the default — a flag flipped in prod with only the off-path ever tested is a live production experiment.

## Lifecycle
A flag is temporary scaffolding, not permanent config. Remove the flag and the dead code path once a rollout is complete and stable — an accumulating pile of stale flags is its own maintenance/testing-matrix burden.

## Forbidden
- a flag with no fallback behavior when the flag source is unreachable
- shipping and forgetting — no owner/removal plan for a temporary rollout flag
- adding Unleash (or similar) before a config boolean is actually insufficient
