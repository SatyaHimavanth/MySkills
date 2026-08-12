from pathlib import Path
import re

ROOT = Path(__file__).resolve().parents[1] / 'skills' / 'fastapi-production'
SKILL = ROOT / "SKILL.md"

text = SKILL.read_text(encoding="utf-8")
refs: set[str] = set()
for line in text.splitlines():
    for value in re.findall(r"`([^`]+)`", line):
        for item in value.split(","):
            item = item.strip()
            if item.endswith(".md") or item.endswith(".py"):
                refs.add(item)

missing = sorted(path for path in refs if not (ROOT / path).exists())
if missing:
    print("Missing SKILL.md references:")
    for path in missing:
        print(f"  - {path}")
    raise SystemExit(1)

# Minimum substantive-file guard. Environment delta files may remain concise,
# but shared policy files should not collapse into one-line routers.
shared_files = sorted(ROOT.rglob("*.shared.md"))
small_shared = []
for path in shared_files:
    words = len(path.read_text(encoding="utf-8").split())
    if words < 80:
        small_shared.append((words, str(path.relative_to(ROOT))))

if small_shared:
    print("Shared files under 80 words:")
    for words, path in small_shared:
        print(f"  {words:>3} {path}")
    raise SystemExit(1)

print(f"Skill files: {sum(1 for p in ROOT.rglob('*') if p.is_file())}")
print(f"SKILL.md references checked: {len(refs)}")
print(f"Shared policy files checked: {len(shared_files)}")
print("All SKILL.md references resolve and shared policy files are substantive.")
