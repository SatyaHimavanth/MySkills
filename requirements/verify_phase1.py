from pathlib import Path

ROOT = Path(__file__).resolve().parents[1] / 'skills' / 'fastapi-production'
REQUIRED = [
    "api/endpoints.shared.md",
    "api/endpoints.local_dev.md",
    "api/endpoints.prod.md",
    "api/response_contracts.shared.md",
    "api/pagination.shared.md",
    "api/openapi.shared.md",
    "api/openapi.local_dev.md",
    "api/openapi.prod.md",
    "validation/shared.md",
    "validation/local_dev.md",
    "validation/prod.md",
    "time/shared.md",
    "time/local_dev.md",
    "time/prod.md",
    "http/clients.shared.md",
    "http/clients.local_dev.md",
    "http/clients.prod.md",
    "errors/shared.md",
    "errors/local_dev.md",
    "errors/prod.md",
    "requirements/phase1_coverage.md",
]
for rel in REQUIRED:
    p = (Path(__file__).parent / rel.replace('requirements/', '')) if rel.startswith('requirements/') else (ROOT / rel)
    if not p.exists():
        raise SystemExit(f"PHASE1 FAIL: missing {rel}")
    if rel.endswith("coverage.md"):
        continue
    text = p.read_text(encoding="utf-8")
    if "# " not in text or "## " not in text or "## Rules" not in text:
        raise SystemExit(f"PHASE1 FAIL: missing required policy sections in {rel}")
print("PHASE1 PASS")
print(f"Checked {len(REQUIRED)} files")
