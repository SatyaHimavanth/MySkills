# Containers — Production

## Purpose

Define lightweight, secure, reproducible, multi-stage Docker container image builds for FastAPI applications using `uv`.

## Rules

- Use multi-stage builds to separate dependency building from the final runtime image.
- Use official `ghcr.io/astral-sh/uv` images for fast dependency installation.
- Run as a non-root user (`appuser`) in production containers.
- Do not include build tooling, compilers, git, or source cache in the final runtime container.
- Use `uv sync --frozen --no-dev --no-editable` for reproducible locked builds.
- Execute application processes directly (`exec`) to handle SIGTERM/SIGINT signals properly.
- Maintain a `.dockerignore` excluding `.env`, `.git`, `tests/`, `__pycache__`, and `.venv` — required even with selective `COPY`, since it's the backstop against secrets/dev files reaching the build context at all.

## Production Multi-Stage Dockerfile (`uv` + FastAPI)

```dockerfile
# --- Stage 1: Build virtual environment ---
FROM ghcr.io/astral-sh/uv:0.6-python3.12-bookworm-slim AS builder

WORKDIR /app

# Copy dependency definition files first for layer caching
COPY pyproject.toml uv.lock ./

# Install dependencies into virtualenv without dev dependencies
RUN --mount=type=cache,target=/root/.cache/uv \
    uv sync --frozen --no-dev --no-editable

# --- Stage 2: Production runtime image ---
FROM python:3.12-slim-bookworm AS runner

# Create non-root user
RUN groupadd -r appgroup && useradd -r -g appgroup -u 10001 appuser

WORKDIR /app

# Copy virtualenv and application code from builder — copy explicitly, not `COPY . /app`,
# which would also pull in .env, .git, tests/, and anything else not excluded by .dockerignore.
COPY --from=builder /app/.venv /app/.venv
COPY app /app/app
COPY alembic /app/alembic
COPY alembic.ini /app/alembic.ini

# Set PATH to use virtualenv
ENV PATH="/app/.venv/bin:$PATH" \
    PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1

USER appuser

EXPOSE 8000

# Exec form for proper SIGTERM signal forwarding
CMD ["uvicorn", "myapp.main:app", "--host", "0.0.0.0", "--port", "8000", "--workers", "4"]
```

## Security & Image Optimization

- **Base Image**: Use official Debian `slim` or `distroless` images.
- **Signal Handling**: Use array form `CMD ["uvicorn", ...]` so PID 1 receives SIGTERM and triggers FastAPI lifespan shutdown cleanly.
- **Read-Only Root Filesystem**: Configure container orchestrator (Kubernetes/ECS) to enforce read-only root filesystems where practical.

## Forbidden

- running containers as `root` in production
- installing dev dependencies (`pytest`, `mypy`) in production container images
- shell form `CMD uvicorn myapp.main:app` (blocks SIGTERM signal propagation)
- `COPY . /app` with no `.dockerignore` — risks shipping `.env`, `.git`, or test fixtures into the image
