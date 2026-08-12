# Validation — Local Development

## Purpose
Keep validation identical to production while allowing easier test data.

## Rules
- Use the same Pydantic constraints locally.
- Do not remove validation just because the frontend is still under development.
- Development-only limits may be higher only if they do not hide production failures.
- Run negative validation tests locally.

## Examples
Keep validation active while developing request handlers. If a test needs invalid data, construct it intentionally in the test rather than weakening the model.

## Production parity
The goal is to keep the same schema and validation behavior locally. Environment differences belong in configuration/resource limits, not in the meaning of the API contract.
