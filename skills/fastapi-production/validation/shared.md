# Input Validation and Resource Limits

## Purpose
Validate API input at the boundary and bound resource consumption before work reaches application or infrastructure layers.

## Rules
- Use Pydantic and FastAPI parameter constraints for structural validation.
- Use service/domain logic for business invariants.
- Use PostgreSQL constraints for durable data invariants.
- Bound page sizes, list lengths, string sizes, numeric ranges, upload sizes, recursion/batch sizes, and external fan-out.
- Reject malformed input early.
- Avoid catastrophic regex patterns or unbounded parsing.

## Example
```python
page_size: int = Query(20, ge=1, le=100)
name: str = Field(min_length=1, max_length=120)
tags: list[str] = Field(max_length=20)
```

## Resource-boundary review
For any endpoint ask:
- maximum body size?
- maximum list/batch size?
- maximum upload size?
- maximum downstream calls?
- timeout?
- rate limit?
- database query bound?
