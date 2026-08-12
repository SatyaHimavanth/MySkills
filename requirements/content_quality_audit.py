from pathlib import Path
import re
import sys

ROOT = Path(__file__).resolve().parents[1] / 'skills' / 'fastapi-production'
errors = []

for path in ROOT.rglob("*.md"):
    rel = path.relative_to(ROOT).as_posix()
    text = path.read_text(encoding="utf-8", errors="ignore")
    if "cite" in text or "turn" in text and "cite" in text:
        errors.append(f"non-portable citation markup: {rel}")
    if rel.endswith(".shared.md") and "## Purpose" not in text and "## Goal" not in text:
        errors.append(f"shared policy missing Purpose/Goal: {rel}")
    if rel.endswith(".local_dev.md") and ("## Rules" not in text and "## Goal" not in text) and "## Purpose" not in text:
        errors.append(f"local policy missing Rules/Goal: {rel}")
    if rel.endswith(".prod.md") and ("## Rules" not in text and "## Goal" not in text) and "## Purpose" not in text:
        errors.append(f"prod policy missing Rules/Goal: {rel}")

# Validate SKILL.md code-like relative markdown references, ignoring glob patterns.
skill=(ROOT/"SKILL.md").read_text(encoding="utf-8")
for ref in re.findall(r"`([^`]+\.md)`", skill):
    if any(ch in ref for ch in "*[]?"):
        continue
    if not (ROOT/ref).exists():
        errors.append(f"SKILL.md missing reference: {ref}")

if errors:
    print("CONTENT QUALITY FAIL")
    for e in errors:
        print(e)
    sys.exit(1)
print("CONTENT QUALITY PASS")
print(f"Checked {len(list(ROOT.rglob('*.md')))} markdown files")
