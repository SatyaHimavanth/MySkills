# Time — Local Development

## Purpose

Make local tests deterministic and keep time behavior compatible with production.

## Rules

- Use the same timezone/serialization policy as production.
- Run local tests in UTC by default unless a test explicitly targets a user timezone.
- Inject/freeze application time in business-logic tests rather than relying on wall-clock sleeps.
- Add explicit tests for DST transitions where the domain depends on local schedules.
- Never depend on the developer machine's local timezone implicitly.

## Example

```text
Clock dependency → fixed test instant
```
