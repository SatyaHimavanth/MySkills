# Containers: Local Development

## Purpose

Choose Docker or Podman only after confirming that the runtime is installed, reachable, and permitted for the developer.

## Discovery

```bash
docker --version
docker info
podman --version
podman info
```

A working CLI does not prove the container engine is reachable.

## Rules

- Ask before using or installing a container runtime when availability/permission is unknown.
- Prefer the runtime already available and approved by the developer.
- Record availability and permission status in `.dev/environment.local.md`.
- Use containers for PostgreSQL/Redis/other services only when the project actually needs them.
- If containers are unavailable, evaluate native services or a compatibility-rated fallback.

## Forbidden

- automatic Docker installation
- assuming root/admin rights
- treating `docker --version` as proof the daemon is usable
