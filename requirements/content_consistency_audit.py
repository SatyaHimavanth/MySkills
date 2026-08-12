from pathlib import Path
import re
import sys

ROOT = Path(__file__).resolve().parents[1] / 'skills' / 'fastapi-production'
errors=[]
files=list(ROOT.rglob('*.md'))
text='\n'.join(p.read_text(encoding='utf-8',errors='ignore') for p in files)

# Explicit contradictions we never want in a completed skill.
patterns=[
    (r'(?i)(?<!not )(?<!never )(?:use|treat) SQLite (?:as|by) default', 'SQLite is described as a default'),
    (r'(?i)(?<!not )(?<!never )SQLite is the default', 'SQLite is described as the default'),
    (r'(?i)BackgroundTasks.{0,80}(?:is|are) (?:a |an )?(?:durable|reliable|persistent|guaranteed)', 'BackgroundTasks is described as durable'),
]
for pat,msg in patterns:
    for m in re.finditer(pat,text,re.S):
        snippet=text[max(0,m.start()-100):m.end()+150].replace('\n',' ')
        if re.search(r'(?i)\b(not|never|do not|is not)\b[^.]{0,100}sqlite|sqlite[^.]{0,100}\b(not|never|do not|is not)\b', snippet):
            continue
        errors.append(f'{msg}: {snippet}')

# Positive production anti-patterns in prose/code.
for p in files:
    t=p.read_text(encoding='utf-8',errors='ignore')
    checks=[
        (r'(?i)production.{0,80}--reload', 'production --reload claim'),
        (r'(?i)production.{0,80}\.env as (?:the )?source', 'production .env source claim'),
        (r'(?i)create (?:a )?new (?:Redis|AsyncClient|httpx\.AsyncClient|Engine) (?:on )?every request', 'per-request infrastructure client claim'),
    ]
    for pat,msg in checks:
        for m in re.finditer(pat,t,re.S):
            snippet=t[max(0,m.start()-60):m.end()+100].replace('\n',' ')
            if re.search(r'(?i)do not|never|avoid|bad|forbidden|unsafe', snippet):
                continue
            errors.append(f'{msg}: {p.relative_to(ROOT)}: {snippet}')

# No stale internal citation markup.
for p in files:
    t=p.read_text(encoding='utf-8',errors='ignore')
    if 'cite' in t:
        errors.append(f'non-portable citation markup: {p.relative_to(ROOT)}')

# SKILL references.
skill=(ROOT/'SKILL.md').read_text(encoding='utf-8')
for ref in re.findall(r'`([^`]+\.md)`',skill):
    if any(c in ref for c in '*[]?'):
        continue
    if not (ROOT/ref).exists():
        errors.append(f'SKILL.md missing file: {ref}')

if errors:
    print('CONTENT CONSISTENCY FAIL')
    for e in errors:
        print(e)
    sys.exit(1)
print('CONTENT CONSISTENCY PASS')
print(f'Checked {len(files)} markdown files')
