# CI/CD Pipeline — Shared

## Purpose
Catch broken code before merge, not after deploy.

## Required pre-merge gates
Every merge to the main branch must pass, in this order (fail fast):

```text
lint/format check
  ↓
type check
  ↓
unit + api + security + database tests
  ↓
dependency vulnerability scan
  ↓
build (image/package)
```

Do not deploy from a branch that skipped these gates. Do not allow force-merge past a failing required check without an explicit, logged override.

## Test stage must use real dependencies
Per `testing/database.shared.md` and `testing/shared.md`, the pipeline's test job needs real PostgreSQL/Redis service containers, not mocks — a green CI run on mocked infra is not evidence the app works.

## Secrets in CI
Never hardcode secrets in workflow files. Use the CI platform's encrypted secrets store, scoped to the minimum jobs that need them. Never echo secret values into logs.

## Reference implementation: Gitea Actions
Gitea Actions is a self-hosted, GitHub-Actions-syntax-compatible CI/CD system built into Gitea (workflow files under `.gitea/workflows/`, ~90% syntax compatible with `.github/workflows/`, runners via `act_runner`). Good default when the project wants CI on infrastructure it controls rather than a third-party SaaS runner.

```yaml
# .gitea/workflows/ci.yml
on: [pull_request]
jobs:
  test:
    runs-on: ubuntu-latest
    services:
      postgres:
        image: postgres:16
        env: {POSTGRES_PASSWORD: postgres, POSTGRES_DB: app_test}
      redis:
        image: redis:7
    steps:
      - uses: actions/checkout@v4
      - run: uv sync --frozen
      - run: uv run alembic upgrade head
      - run: uv run pytest --cov=app
```

If the project already uses GitHub, the same workflow runs on GitHub Actions with no changes beyond the `on:`/marketplace-action availability — treat the two as interchangeable targets for this file's gates, not as competing choices to litigate per project.

## Forbidden
- merging with a failing or skipped required check
- test stage against mocked DB/Redis only
- secrets committed to workflow files or echoed into logs
- deploy job triggered directly from a push without the gate sequence above
