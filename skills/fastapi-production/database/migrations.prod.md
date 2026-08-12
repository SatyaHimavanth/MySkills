# Database Migrations — Production

## Purpose
Execute database schema changes as a controlled release step.

## Rules
- Run approved migrations as a deployment stage/job.
- Do not have every API replica independently run migrations by default.
- Validate compatibility with both old and new application versions during rolling deployment.
- Review destructive/large migrations for lock and data-loss risk.
- Use backups/snapshots according to the platform's recovery policy before destructive changes.
- Verify database readiness after migration before routing traffic to incompatible application versions.
