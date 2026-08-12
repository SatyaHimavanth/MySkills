# uv Package and Project Management

## Purpose
Use one reproducible Python project workflow.

## Dependency fields
- `[project].dependencies` → required runtime dependencies
- `[project.optional-dependencies]` → optional application extras
- `[dependency-groups]` → local development tooling/groups

uv currently documents these as distinct dependency mechanisms and supports `uv add`, `uv remove`, and group/extra flags.

## Workflow
```bash
uv add fastapi
uv add sqlalchemy
uv add --dev pytest
uv add --optional redis redis
uv sync
uv run pytest
uv lock
```

## Locking
Commit `uv.lock` for applications. Use `uv run --locked` or equivalent locked CI behavior when the environment must fail rather than mutate the lockfile. uv documents `--locked` as refusing to update an out-of-date lockfile.

## Rules
- Inspect `pyproject.toml`, `uv.lock`, and `.python-version` before changing dependencies.
- Do not mix routine `pip install` workflows with the project workflow.
- Keep optional application integrations out of mandatory runtime dependencies when they are genuinely optional.

## Sources

- https://docs.astral.sh/uv/concepts/projects/dependencies/
- https://docs.astral.sh/uv/concepts/projects/sync/

