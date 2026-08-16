from pathlib import Path

ROOT = Path(__file__).resolve().parents[1] / 'skills' / 'fastapi-production'
FILES = [
    "async/idempotency.shared.md",
    "async/jobs.shared.md",
    "async/local_dev.md",
    "async/prod.md",
    "reliability/lifespan.shared.md",
    "reliability/lifespan.local_dev.md",
    "reliability/lifespan.prod.md",
    "http/clients.shared.md",
    "streaming/shared.md",
    "requirements/phase3_coverage.md",
]
REQUIRED = {
    "async/idempotency.shared.md": ["Idempotency-Key", "409", "transaction", "concurrent"],
    "async/jobs.shared.md": ["BackgroundTasks", "outbox", "retry", "idempotent", "delivery"],
    "reliability/lifespan.shared.md": ["lifespan", "shutdown", "request-scoped", "testing"],
    "http/clients.shared.md": ["httpx", "timeout", "retry", "idempotency", "response validation"],
    "streaming/shared.md": ["StreamingResponse", "SSE", "WebSocket", "disconnect", "backpressure"],
}

for rel in FILES:
    p = (Path(__file__).parent / rel.replace('requirements/', '')) if rel.startswith('requirements/') else (ROOT / rel)
    if not p.exists():
        raise SystemExit(f"MISSING: {rel}")
    text = p.read_text(encoding="utf-8")
    if len(text.split()) < 120 and rel not in {"requirements/phase3_coverage.md"}:
        raise SystemExit(f"TOO SHALLOW: {rel}")
    for term in REQUIRED.get(rel, []):
        if term.lower() not in text.lower():
            raise SystemExit(f"MISSING CONTENT: {rel}: {term}")

print("PHASE3 PASS")
