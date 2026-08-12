from pathlib import Path

ROOT = Path(__file__).resolve().parents[1] / 'skills' / 'fastapi-production'
REQUIRED = [
    "storage/files.shared.md",
    "storage/local_dev.md",
    "storage/prod.md",
    "storage/downloads.shared.md",
    "requirements/phase5_coverage.md",
]
KEYWORDS = {
    "storage/files.shared.md": ["UploadFile", "Content-Type", "quarantine", "quota", "ObjectStorage", "signed URL", "tenant"],
    "storage/local_dev.md": ["Compatibility: PARTIAL", "docker", "podman", "LocalObjectStorage"],
    "storage/prod.md": ["signed upload URL", "quota", "scanning", "Multi-replica", "private"],
    "storage/downloads.shared.md": ["FileResponse", "StreamingResponse", "authorization", "Content-Disposition"],
}

errors = []
for rel in REQUIRED:
    p = (Path(__file__).parent / rel.replace('requirements/', '')) if rel.startswith('requirements/') else (ROOT / rel)
    if not p.exists():
        errors.append(f"missing: {rel}")
    elif p.stat().st_size < 900 and rel not in {"requirements/phase5_coverage.md"}:
        errors.append(f"too small: {rel}")

for rel, words in KEYWORDS.items():
    text = (ROOT / rel).read_text(encoding="utf-8") if (ROOT / rel).exists() else ""
    for word in words:
        if word.lower() not in text.lower():
            errors.append(f"{rel}: missing keyword {word!r}")

if errors:
    print("PHASE5 FAIL")
    for error in errors:
        print(error)
    raise SystemExit(1)

print("PHASE5 PASS")
print(f"Checked {len(REQUIRED)} required files")
