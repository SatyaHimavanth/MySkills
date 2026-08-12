from pathlib import Path

ROOT = Path(__file__).resolve().parents[1] / 'skills' / 'fastapi-production'
REQUIRED = [
    "security/api_security.shared.md",
    "security/object_authorization.shared.md",
    "security/ssrf.shared.md",
    "security/csrf.shared.md",
    "security/csrf.local_dev.md",
    "security/csrf.prod.md",
    "security/secrets.shared.md",
    "api/resource_limits.shared.md",
    "api/versioning.shared.md",
    "requirements/phase4_coverage.md",
]
REQUIRED_MARKERS = {
    "security/ssrf.shared.md": ["allowlist", "redirect", "DNS", "private", "metadata", "timeout"],
    "security/object_authorization.shared.md": ["BOLA", "property", "tenant", "mass assignment", "Forbidden"],
    "security/csrf.shared.md": ["SameSite", "Origin", "Fetch Metadata", "state-changing", "CSRF token"],
    "security/secrets.shared.md": ["SecretStr", "rotation", "production", "logs"],
    "api/resource_limits.shared.md": ["request body", "page size", "upload", "fan-out", "timeout"],
    "api/versioning.shared.md": ["version", "deprecated", "inventory", "breaking"],
}
for rel in REQUIRED:
    path = (Path(__file__).parent / rel.replace('requirements/', '')) if rel.startswith('requirements/') else (ROOT / rel)
    if not path.exists():
        raise SystemExit(f"MISSING: {rel}")
    if len(path.read_text(encoding="utf-8")) < 1000:
        raise SystemExit(f"TOO THIN: {rel}")
for rel, markers in REQUIRED_MARKERS.items():
    text = (ROOT / rel).read_text(encoding="utf-8").lower()
    for marker in markers:
        if marker.lower() not in text:
            raise SystemExit(f"MISSING CONCEPT: {rel}: {marker}")
print("PHASE4 PASS")
