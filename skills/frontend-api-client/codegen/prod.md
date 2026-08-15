# Client & Schema Generation — Production

## CI regeneration gate
Regenerate the client against a real running instance of the backend (or its committed OpenAPI spec artifact) as a pre-merge check, then diff against the checked-in generated files. A diff means the frontend's understanding of the API is stale — fail the build, don't silently deploy a mismatched client. Fits directly into `fastapi-production`'s `deployment/cicd.shared.md` gate sequence, as an additional stage alongside lint/type-check/test.

```yaml
# .gitea/workflows/ci.yml or .github/workflows/ci.yml — additional job
  api-client-drift:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - run: npm ci
      - run: npm run gen:api  # against a running backend service container, or a committed openapi.json artifact
      - run: git diff --exit-code src/api/  # fails the build if generation produced any diff
```

## Forbidden
- deploying a frontend build without having regenerated against the backend version it's actually deployed alongside
- committing generated files without a CI check that they're still current
