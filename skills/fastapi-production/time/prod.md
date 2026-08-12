# Time — Production

## Purpose

Make persisted timestamps and distributed scheduling deterministic across hosts, containers, and geographically distributed deployment regions.

## Rules

- Persist and transmit all timestamp instants in UTC with ISO-8601 formatting.
- Synchronize system clocks across all application servers and background workers using NTP (e.g. Chrony or systemd-timesyncd).
- Monitor NTP clock synchronization offset (`chronyc tracking`) on production hosts.
- Configure token verification dependencies with an explicit clock skew tolerance (`leeway=10`) to absorb minor regional NTP drift.
- Use IANA timezone identifiers (e.g. `"Europe/London"`, `"Asia/Tokyo"`) for business-local schedule definitions.
- Make scheduler timezone configuration explicit in task queues (Taskiq, Celery, APScheduler).
- Do not rely on host-local timezone settings or system environment timezone variables.

## Multi-Region Clock Drift Safety

When API workers in Region A communicate with Database servers in Region B:
- App servers must not assume their system clock is perfectly identical to the DB primary clock.
- Audit timestamps (`created_at`, `updated_at`) must be assigned by PostgreSQL (`server_default=func.now()`).

## Forbidden

- fixed numeric offsets (e.g. `+05:30`) as hardcoded timezone identifiers in code instead of IANA names
- host-local timezone assumptions (`datetime.now()`)
- naive UTC objects (`datetime.utcnow()`)
