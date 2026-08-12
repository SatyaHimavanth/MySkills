# Validation — Production

## Purpose
Prevent malformed or resource-exhausting requests from reaching expensive code paths.

## Rules
- Enforce hard request/body/upload bounds.
- Enforce pagination limits.
- Validate URLs and external targets before network access.
- Bound downstream fan-out and timeouts.
- Combine validation with rate limiting and authorization for sensitive business flows.

## Dependency protection
Validation is one part of resource protection. Combine bounded input with rate limits, explicit downstream timeouts, and authorization. Do not rely on validation alone to prevent abuse.

## Verification
Production-like tests should cover maximum allowed values, malformed requests, oversized batches/uploads, and rejected out-of-range parameters before release.
