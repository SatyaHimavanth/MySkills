from pathlib import Path

ROOT = Path(__file__).resolve().parents[1] / 'skills' / 'fastapi-production'
REQ_DIR = Path(__file__).resolve().parent

required = [
    "testing/shared.md",
    "testing/fixtures.shared.md",
    "testing/database.shared.md",
    "testing/api.shared.md",
    "testing/security.shared.md",
    "testing/contract.shared.md",
    "testing/concurrency.shared.md",
    "testing/e2e.shared.md",
    "testing/local_dev.md",
    "testing/prod.md",
    "testing/pyproject.toml.example",
    "requirements/phase6_coverage.md",
]

def get_path(rel: str) -> Path:
    if rel.startswith("requirements/"):
        return REQ_DIR / rel.replace("requirements/", "")
    return ROOT / rel

missing = [p for p in required if not get_path(p).exists()]
if missing:
    raise SystemExit("PHASE6 FAIL: missing files: " + ", ".join(missing))

keywords = {
    "testing/shared.md": ["pytest", "dependency_overrides", "TestClient", "AsyncClient", "parametrize", "mock"],
    "testing/fixtures.shared.md": ["fixture", "scope", "cleanup", "factory"],
    "testing/database.shared.md": ["PostgreSQL", "create_savepoint", "rollback", "migration", "concurrency"],
    "testing/api.shared.md": ["response.status_code", "response schema", "OpenAPI", "stream"],
    "testing/security.shared.md": ["authentication", "authorization", "BOLA", "CSRF", "SSRF", "rate"],
    "testing/contract.shared.md": ["OpenAPI", "breaking", "response schemas", "security"],
    "testing/concurrency.shared.md": ["idempotency", "row-lock", "optimistic", "invariant"],
    "testing/e2e.shared.md": ["E2E", "cleanup", "sandbox"],
    "testing/local_dev.md": ["uv run pytest", "PostgreSQL", "Redis"],
    "testing/prod.md": ["release", "PostgreSQL", "readiness", "rollback"],
}

for rel, terms in keywords.items():
    text = (ROOT / rel).read_text(encoding="utf-8").lower()
    absent = [term for term in terms if term.lower() not in text]
    if absent:
        raise SystemExit(f"PHASE6 FAIL: {rel} missing concepts: {absent}")

coverage = (REQ_DIR / "phase6_coverage.md").read_text(encoding="utf-8")
if coverage.count("| COMPLETE |") < 14:
    raise SystemExit("PHASE6 FAIL: incomplete coverage matrix")

print("PHASE6 PASS")
print(f"Checked {len(required)} required files")
