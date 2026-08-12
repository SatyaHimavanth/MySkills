# File Storage — Local Development

## Purpose

Make local file development simple without creating an application architecture that must be rewritten for object storage in production.

## Default local backend

Use a configurable `LocalObjectStorage` implementation when object-storage-specific behavior is not part of the feature.

```text
Compatibility: PARTIAL
```

Example:

```env
APP_STORAGE__BACKEND=local
APP_STORAGE__ROOT_DIR=./var/storage
APP_STORAGE__MAX_FILE_SIZE_BYTES=104857600
```

## Local directory layout

```text
var/
├── storage/
├── quarantine/
└── tmp/
```

Keep these directories outside the Python package and source-controlled files.

Add them to `.gitignore`.

## When to use a real object-storage-compatible service

Use a real S3-compatible/local object store when developing:

- presigned URLs
- multipart uploads
- object metadata semantics
- bucket policies
- versioning
- provider-specific headers
- direct browser-to-object-storage upload flows

A local filesystem does not reproduce those semantics.

## Container decision

Before requiring a local object-storage container:

```bash
docker --version
docker info
podman --version
podman info
```

If containers are unavailable, do not silently install them. Continue with `LocalObjectStorage` where the feature allows it, or ask for an approved alternative when object-storage semantics are essential.

## Local upload validation

Do not disable security validation merely because files are local.

Keep:

- allowed extensions
- size limits
- generated keys
- ownership checks

## Test data

Do not store real user files in the repository.

Use deterministic fixtures under:

```text
tests/fixtures/files/
```

Fixtures should be small and safe.
