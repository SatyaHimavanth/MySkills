# Database Encryption — Shared

## Purpose
Encryption is not one control — it is several, each defending against a different threat. Choosing "encrypt the database" without naming which layer and which threat leads to either wasted effort (encrypting things a stolen laptop can't reach) or false confidence (assuming TLS covers a compromised superuser). This file inventories the layers; see `security/pii_protection.shared.md` for field-level classification and application code patterns.

## The four layers, and what each one actually stops

| Layer | Stops | Does NOT stop |
|---|---|---|
| In transit (TLS to Postgres) | Network eavesdropping, on-path tampering | A compromised DB host, a malicious query, a leaked backup |
| At rest (disk/volume) | Physical disk theft, snapshot/volume leaked outside the provider boundary | A live SQL injection, an authenticated attacker with query access, a superuser dump |
| Column/application-level (pgcrypto or app-side) | A DB read by someone with query access but not the key (rogue DBA, compromised replica, leaked dump) | Nothing once the key and ciphertext are both exposed together |
| Backups | Same as at-rest, applied to backup artifacts and their storage/transport | An attacker who already has the running DB's live access |

Naming the threat first tells you which layer to spend effort on. "We need database encryption" without a threat model usually means only layer 2 gets implemented and the team stops there, believing they're covered against layer 3.

## 1. Encryption in transit

Require TLS between the application and PostgreSQL in every environment that leaves a single trusted host:

```python
# SQLAlchemy + asyncpg: do NOT rely on ?ssl=... or ?sslmode=... in the URL — this is
# documented as unreliable through SQLAlchemy's asyncpg dialect (see sqlalchemy/sqlalchemy
# issues #5973 and discussion #10894); it can silently fail to apply, giving false confidence
# that TLS verification is active when it isn't. Pass it via connect_args instead:
engine = create_async_engine(
    "postgresql+asyncpg://user:pass@host:5432/db",
    connect_args={"ssl": "verify-full"},  # or an ssl.SSLContext for a custom CA bundle
)
```

- `sslmode=require` encrypts the wire but does not verify the server identity — vulnerable to MITM with a forged cert. Use `verify-full` (or the driver's equivalent) in prod, pinned to a known CA bundle.
- `local_dev.md`/`prod.md` in this folder define the per-environment default; do not silently downgrade to `"disable"` because a local container makes `"verify-full"` inconvenient — use `connect_args={"ssl": "require"}` locally instead of turning TLS off entirely if the local Postgres already supports it.
- This is necessary but not sufficient: it protects the network hop, not the data once it lands on disk or once a query result crosses back to the app in plaintext.

## 2. Encryption at rest (disk/volume)

This is almost always **infrastructure-provided, not application-implemented**:

- Managed Postgres (RDS, Cloud SQL, Azure Database for PostgreSQL): enable storage encryption at provisioning time — it is a provider setting, not something the FastAPI app configures. Cloud-provider provisioning itself is out of this skill's scope (see `SKILL.md` global principle 19) — hand this off to the project's cloud-provider skill, but the requirement belongs on the production-readiness checklist regardless of which skill implements it.
- Self-hosted Postgres: full-disk or volume encryption (e.g., LUKS) is an OS/ops concern, not app code.
- **Do not build application-level "at rest" encryption as a substitute for this.** It's the wrong layer for the threat (media theft) and is far more expensive than flipping a provider flag.

## 3. Column/application-level encryption

This is the layer application code actually implements. See `security/pii_protection.shared.md` for the two sub-types and when to use each:

- Standard-sensitivity PII → `pgcrypto` (DB does encrypt/decrypt, still trusts the DB with plaintext transiently)
- Highest-sensitivity data (SSNs, payment data, health records) → application-side envelope encryption before the row ever reaches Postgres

Do not duplicate that logic here — read that file when implementing column encryption. This file covers the layer selection; that file covers the implementation.

## 4. Backup encryption

A correctly encrypted live database with unencrypted backups is a common gap — the backup is a full copy of the same sensitive data, often shipped to a separate storage location with separate access controls.

- Backups must be encrypted in transit (during the dump/copy) and at rest (in the storage location), independent of whether the live DB uses provider-managed at-rest encryption — some backup pipelines export to a different medium (object storage, offsite replica) that needs its own encryption setting.
- Column-level ciphertext (layer 3) stays ciphertext in a backup as long as the encryption key is stored and rotated separately from the backup itself — never bundle the key with the backup artifact.
- Cross-reference `operations/disaster_recovery.shared.md`, which lists encryption as one of the required attributes of a backup strategy alongside frequency, retention, and access control — that file defines the backup *policy*; this file defines *which layer* satisfies the encryption line item.

## 5. Per-user key encryption (crypto-shredding) for right-to-erasure

This is a distinct pattern from layer 3, not a variant of it: layer 3 asks "is this column readable by a rogue DB session"; this asks "when a user is deleted, how do we make their data unrecoverable — including in every backup — without rewriting or selectively editing those backups." `security/pii_protection.shared.md` names the general problem (backups "age out," you "cannot selectively edit an existing backup"); this is the specific technique that makes that limitation acceptable.

**Mechanism.** Give each user their own data-encryption key (DEK), stored wrapped (envelope-encrypted by a root KEK in the KMS) in a keys table/keystore that is logically and operationally separate from the data table it protects. Encrypt that user's rows with their DEK. To erase the user, destroy the DEK (delete the keystore row, or delete/schedule-deletion of the corresponding KMS key). Every copy of their ciphertext — live table, replica, and every existing backup — becomes permanently unreadable the instant the key is gone, with no need to touch the backups themselves.

```python
# Erasure: destroy the key, not (only) the row
async def erase_user(user_id: UUID, session: AsyncSession, kms: KmsClient) -> None:
    await kms.schedule_key_deletion(key_alias=f"user-dek/{user_id}")
    await session.execute(delete(UserKey).where(UserKey.user_id == user_id))
    await session.execute(delete(User).where(User.id == user_id))  # still delete live rows per policy
    await session.commit()
```

**Why this solves the backup problem, and where it doesn't.** Crypto-shredding neutralizes ciphertext sitting in a backup without editing the backup — but only for data that was actually encrypted under the destroyed key before it was backed up. It does nothing for copies of the plaintext that exist outside this pattern: search indices, analytics warehouses/CDC pipelines, log lines, exported CSVs, third-party processors, or caches. Treat "identify every place plaintext could have leaked to" as a required step of adopting this pattern, not an edge case — the technique is only as complete as the inventory behind it.

**Deactivation is not deletion.** Do not destroy a user's key on deactivation/suspension — that's a reversible state and key destruction is not. Crypto-shred only on an erasure request or a policy-defined hard-delete, and keep deactivated-but-not-deleted accounts on normal key custody (app-held, per below) so reactivation doesn't require key recovery that no longer exists.

**Key custody: app-held vs. user-held.** Two different trust models, not two implementations of the same thing:

| | App-held key (KMS-managed) | User-held key |
|---|---|---|
| Where the key lives | App's KMS/secrets manager | User's device/password manager; app never stores it, or stores only a copy the user can revoke |
| App can decrypt without the user present | Yes | No — app must receive the key (e.g., from a request header, or derived from a passphrase at login) to decrypt |
| Erasure mechanism | App deletes the DEK from its own KMS | App deletes its stored copy (if any); user's independently-held copy is outside the app's control by design |
| Cost | Low friction, normal queries/background jobs work | High friction — password reset or lost key means the app cannot recover that user's data either; no background processing on the data without the user's session supplying the key |
| Right-to-erasure story | "We deleted the key" | "We deleted our copy; you retain whatever copy you kept" — offer to export the key/data to the user at account closure *before* the app-side copy is destroyed, since that's the last moment the app can hand it over |

Default to app-held per-user keys for most products — it gets you crypto-shredding without breaking every feature that touches user data server-side. Reach for user-held keys only when the product explicitly promises "we cannot read your data without you" (client-side/end-to-end designs) — that promise has to be true everywhere (no plaintext copies in logs, search, or analytics), not just at the point of erasure, or it's a false guarantee.

## Key management (applies to layers 2–5)

- Never hardcode or store encryption keys alongside the data they protect. Keys live in a KMS/secrets manager — see `security/secrets.shared.md`.
- Use envelope encryption for application-level keys: a per-record or per-tenant data key, itself wrapped by a root key in the KMS. One static application-wide key is listed as forbidden in `security/pii_protection.shared.md` for the same reason it's forbidden here — a single key compromise decrypts everything, and you cannot rotate it without re-encrypting the entire dataset.
- In a multi-tenant system (see `database/multi_tenancy.shared.md`), prefer tenant-scoped data keys over a single shared key so a key compromise or a tenant offboarding/erasure request is scoped to that tenant, not global.
- Define a key rotation cadence and a re-encryption path before you need one under incident pressure, not after.

## Choosing layers by use case

| Use case | Layers required |
|---|---|
| Internal admin tool, no regulated data, single trusted network | In transit only |
| Standard SaaS app storing user PII (name, email, address) | In transit + at rest (provider) + column-level via pgcrypto for anything queried as sensitive |
| Payment data, SSNs, health records (HIPAA/PCI-adjacent) | All four layers, with application-side envelope encryption (not pgcrypto alone) for layer 3 |
| Multi-tenant SaaS with enterprise/regulated tenants | All four layers + tenant-scoped data keys, so per-tenant key rotation and erasure are possible without touching other tenants |
| Disaster-recovery/backup pipeline for any of the above | Backup encryption matching or exceeding the live DB's layer 3 guarantee — a backup is not exempt because the source table was encrypted |
| Large user base with deletion/deactivation requests where backups can't practically be edited per-erasure | Per-user DEKs (layer 5) so erasure = key destruction; app-held keys unless the product specifically promises the app cannot read user data, in which case user-held keys with a documented export-at-closure flow |

## Forbidden
- Treating TLS-in-transit as satisfying a "we encrypt sensitive data" requirement — it does not cover data at rest or a compromised DB session.
- Treating provider-managed at-rest encryption as sufficient for data that needs to survive a compromised superuser or leaked dump — that requires layer 3.
- Shipping unencrypted backups of a database whose live tables are encrypted.
- One static, unrotatable key shared across all tenants/records at any layer.
- Building custom at-rest (disk-level) encryption in application code instead of using the provider's setting.
- Destroying a user's DEK on deactivation/suspension instead of on actual erasure — deactivation must stay reversible.
- Calling erasure complete after key destruction without having inventoried plaintext copies outside the encrypted table (search, analytics, logs, exports, processors).
- Claiming a "user-held key" / "we can't read your data" design while any plaintext copy exists server-side outside the user's control.
