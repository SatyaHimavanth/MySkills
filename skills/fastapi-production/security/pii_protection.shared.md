# PII Protection at Rest — Shared

## Purpose
Protect PII sitting in application tables — distinct from `security/secrets.shared.md` (credentials) and `security/passwords.shared.md` (auth hashes).

## Classify before encrypting
Not all PII needs the same treatment. Classify fields (name/email vs. SSN/government ID/health data) and apply encryption proportional to sensitivity — encrypting everything makes normal queries (search, join, sort) impossible without justification.

## Standard PII: pgcrypto
PostgreSQL's `pgcrypto` extension provides column-level encryption without adding infrastructure:
```sql
-- write
UPDATE users SET ssn = pgp_sym_encrypt('123-45-6789', :key);
-- read
SELECT pgp_sym_decrypt(ssn, :key) FROM users WHERE id = :id;
```
Encrypted columns can't be indexed for equality/range search directly. Don't encrypt a column you need to `WHERE`/`JOIN` on without a separate deterministic-hash lookup column, and don't pretend that hash column is itself encrypted.

## Highest sensitivity: encrypt before it reaches Postgres
For SSNs, payment data, health records: encrypt in the application before `INSERT`, so the DB only ever stores ciphertext and never sees plaintext, even from a superuser or a compromised replica. Use envelope encryption — a data key per record/tenant, itself encrypted by a root key held in a KMS/secrets manager (see `security/secrets.shared.md`), not one static application-wide key.

## Right to erasure (GDPR/CCPA)
A deletion request must cascade correctly through: primary tables (FK cascade or explicit delete), soft-delete flags (a `deleted_at` flag is not erasure), audit event `before_state`/`after_state` snapshots (see `security/audit_logging.shared.md` — redact or key-shred, don't leave plaintext PII in an immutable audit trail forever), and backups (define a backup retention window after which old backups age out; you cannot selectively edit an existing backup).

## Forbidden
- one static encryption key for all records/tenants
- encrypted columns queried via a full-table decrypt-and-scan in application code
- treating a soft-delete flag as satisfying an erasure request
- PII in audit `before_state`/`after_state` with no redaction/expiry plan
