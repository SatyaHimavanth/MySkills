from pathlib import Path

ROOT = Path(__file__).resolve().parents[1] / 'skills' / 'fastapi-production'
FILES = [
    "database/acid.shared.md",
    "database/transactions.shared.md",
    "database/concurrency.shared.md",
    "database/query_performance.shared.md",
    "database/postgresql.shared.md",
    "database/performance.local_dev.md",
    "database/performance.prod.md",
    "requirements/phase2_coverage.md",
]

required = ("#", "## Purpose")
failed = []
for rel in FILES:
    path = (Path(__file__).parent / rel.replace('requirements/', '')) if rel.startswith('requirements/') else (ROOT / rel)
    if not path.exists():
        failed.append(f"missing: {rel}")
        continue
    text = path.read_text(encoding="utf-8")
    if len(text.split()) < 180 and not rel.endswith("coverage.md"):
        failed.append(f"too shallow: {rel}")
    if "## Purpose" not in text and not rel.endswith("coverage.md"):
        failed.append(f"missing purpose: {rel}")

if failed:
    print("PHASE2 FAIL")
    print("\n".join(failed))
    raise SystemExit(1)

print("PHASE2 PASS")
print(f"Checked {len(FILES)} files")
