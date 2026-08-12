# Disaster Recovery — Shared

## Purpose

Define how data and service state can be restored after data loss, infrastructure failure, or region/host failure.

## Recovery objectives

### RPO — Recovery Point Objective

Maximum acceptable data loss measured in time.

Example:

```text
RPO = 15 minutes
```

### RTO — Recovery Time Objective

Maximum acceptable time to restore service.

Example:

```text
RTO = 60 minutes
```

Do not choose RPO/RTO numbers without product/business input.

## PostgreSQL backup model

PostgreSQL documents three broad backup approaches:

- SQL dumps
- filesystem-level backups
- continuous archiving/PITR

Continuous WAL archiving plus a base backup can support point-in-time recovery and warm standby patterns. [Certain] See PostgreSQL backup/PITR documentation. 

## Backup policy

Define:

- what is backed up
- frequency
- retention
- encryption
- storage location
- cross-region/zone strategy when required
- access control
- restore verification

## Restore testing

A backup that has never been restored is not proven recovery capability.

Regularly test:

```text
backup
  ↓
restore
  ↓
migrations / compatibility
  ↓
application startup
  ↓
readiness
  ↓
critical workflow
```

## Database recovery

For PostgreSQL PITR, preserve the base backup plus the required continuous WAL archive sequence. [Certain]

Do not confuse `pg_dump` with continuous WAL-based recovery; PostgreSQL documents these as distinct backup approaches.

## Object storage recovery

Define:

- object versioning where useful
- retention/deletion protection
- cross-region replication when required
- metadata/database consistency

## Redis recovery

Determine whether Redis contains:

```text
reconstructable cache
```

or:

```text
authoritative/durable state
```

Cache loss may be acceptable. Durable job/session state may not be.

## Secrets recovery

Document how credentials are recreated/rotated after a disaster.

Do not store recovery credentials inside application repositories.

## Recovery validation

After restore:

- verify schema version
- verify migrations
- verify critical indexes/constraints
- verify application configuration
- verify readiness
- verify authentication
- verify critical user workflow

## Forbidden patterns

- calling a backup policy complete without restore tests
- storing backups only on the same host as the primary database
- treating cache snapshots as guaranteed recovery for authoritative data
- undocumented RPO/RTO assumptions
