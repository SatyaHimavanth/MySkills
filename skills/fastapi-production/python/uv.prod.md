# uv — Production

## Purpose

Make production Python environments reproducible from committed project metadata and the lockfile.

## Rules

- Commit `pyproject.toml` and `uv.lock`.
- Prefer `uv sync --locked` in CI/release workflows when the lockfile must not change.
- Use `--frozen` only when the workflow intentionally wants the lockfile to be the sole resolution source without checking project metadata.
- Do not include development dependency groups in production unless the deployment explicitly needs them.
- Keep production runtime dependencies in `[project].dependencies`.

## Example

```bash
uv sync --locked --no-dev
```

Verify the exact production command against the project's chosen group/extra strategy.

## Forbidden

- ad-hoc `pip install` as the production dependency workflow
- silently modifying `uv.lock` during release
