# Architecture: Local Development

## Purpose

Describe how local development may be simplified without breaking production compatibility.

## Rules

- Prefer the same module boundaries and data flow used in production.
- Use local fallbacks only when the fallback is compatible enough for the task.
- Ask before using Docker or Podman if availability or permissions are unknown.
- Record discovered environment capabilities in `.dev/environment.local.md`.
- Do not introduce local-only logic that would require a rewrite for production.

## Local simplifications allowed

- Smaller connection pools
- verbose logging
- local-only mock integrations for non-critical systems
- disabled or relaxed rate limits for development convenience, when safe
