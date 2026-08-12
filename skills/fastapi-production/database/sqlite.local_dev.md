# Database: SQLite Local Development

## Use only when explicitly requested

The agent must warn the user that SQLite differs from PostgreSQL.

## Limitations to disclose

- file-based locking and concurrency limits
- fewer PostgreSQL-specific SQL features
- different transaction and isolation behavior
- weaker multi-process behavior
- limited parity for production pooling and connection management
- migration and indexing behavior that may differ from PostgreSQL

## Rules

- Use SQLite only after the user explicitly chooses it.
- Keep the application code portable so the database can be switched back to PostgreSQL later.
- Do not hide SQLite limitations behind silent defaults.
