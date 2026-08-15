# Load & Performance Testing — Shared

## Purpose
Correctness tests (`testing/*.shared.md`) prove the app behaves right for one request. They don't prove it survives 500 concurrent ones — a different failure class (connection pool exhaustion, N+1 queries only visible under concurrency, rate limiter/cache contention).

## Default: Locust
Python-native, no new language for a project already on `uv`/pytest — reuses real auth/token logic instead of reimplementing it in another language.

```python
import itertools
from locust import HttpUser, task, between

user_counter = itertools.count(1)

class ApiUser(HttpUser):
    wait_time = between(1, 3)

    def on_start(self):
        # One distinct account per virtual user, not one shared login. Verified: sharing a
        # single login across all simulated users collides with the per-username rate limit
        # (security/ratelimiting.shared.md) — 30/35 logins failed with 429 in testing, looking
        # like a capacity problem when it was actually the rate limiter correctly treating
        # concurrent logins to one account as credential stuffing. Fixed by seeding N distinct
        # accounts and giving each virtual user its own: 0/152 failures, real numbers.
        n = next(user_counter)
        r = self.client.post("/api/v1/auth/login", json={"email": f"loadtest{n}@example.com", "password": "..."})
        self.token = r.json()["access_token"]

    @task
    def list_tasks(self):
        self.client.get("/api/v1/tasks", headers={"Authorization": f"Bearer {self.token}"})
```
Run against a production-shaped environment (real Postgres/Redis, per `testing/database.shared.md` — not SQLite/mocks) — start at expected peak concurrent users + ~20-30% headroom, increase until degradation to find the actual ceiling.

## Alternative: k6
Prefer k6 when the goal is a CI-gated pass/fail threshold on every change (`deployment/cicd.shared.md`) rather than exploratory Python-scripted scenarios — its `thresholds` config fails the build declaratively; Locust needs custom glue for the same result. Both are legitimate; don't run both by default, pick one per project.

## What to watch, not just requests/sec
DB pool exhaustion (`database/pooling.shared.md`'s budget under real concurrency, not just at rest), p99 latency (not just average — a slow tail hides behind a good mean), and error rate climbing before throughput plateaus (the actual capacity ceiling, not the point requests/sec stops increasing).

## Forbidden
- load testing against SQLite/mocked DB or Redis — numbers won't transfer to production
- treating average latency alone as sufficient — a good mean can hide a bad p99
- running load tests only once, pre-launch, with no regression baseline going forward
- one shared login/account across all virtual users on a rate-limited auth endpoint — verified this produces false failures indistinguishable from a real capacity problem
