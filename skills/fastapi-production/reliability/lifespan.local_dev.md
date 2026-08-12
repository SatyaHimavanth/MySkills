# Lifespan — Local Development

## Purpose

Use the real application lifespan locally while keeping infrastructure smaller.

## Rules

- Use the same resource ownership model as production.
- Start PostgreSQL/Redis/HTTP clients only when the selected feature requires them.
- Use console logging for startup/cleanup diagnostics.
- Fail clearly when a required dependency is absent.
- Do not silently replace PostgreSQL or Redis with incompatible fallbacks.

## Verification

Run startup/shutdown tests locally and inspect for unclosed clients, engines, sessions, or tasks.

## Test cases

Exercise successful startup, missing required dependencies, cleanup after shutdown, and repeated test application creation. The goal is to detect leaked HTTP clients, Redis connections, DB engines, background tasks, and open resources.

## Container/runtime interaction

If local dependencies are containerized, lifespan startup should report a clear connectivity error when the service is unavailable rather than silently switching to a different backend.
