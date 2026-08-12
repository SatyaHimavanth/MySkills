from pathlib import Path

ROOT = Path(__file__).resolve().parents[1] / 'skills' / 'fastapi-production'
REQUIRED = {
    "reliability/degradation.shared.md": ["graceful degradation", "timeouts", "fallbacks", "load shedding"],
    "reliability/circuit_breakers.shared.md": ["circuit breaker", "closed", "open", "half-open", "metrics"],
    "operations/slo.shared.md": ["SLI", "SLO", "error budget", "release policy"],
    "operations/alerting.shared.md": ["page", "dashboard", "runbook", "error budget"],
    "deployment/rollback.shared.md": ["rollback", "expand-and-contract", "canary", "forward-fix"],
    "operations/disaster_recovery.shared.md": ["RPO", "RTO", "PITR", "restore"],
    "operations/runbooks.shared.md": ["Symptoms", "Impact", "Mitigation", "Recovery", "Escalation"],
    "operations/local_dev.md": ["Local", "Redis", "graceful degradation"],
    "operations/prod.md": ["SLOs/SLIs", "rollback", "backup/restore", "runbook"],
}

errors = []
for rel, terms in REQUIRED.items():
    path = (Path(__file__).parent / rel.replace('requirements/', '')) if rel.startswith('requirements/') else (ROOT / rel)
    if not path.exists():
        errors.append(f"missing: {rel}")
        continue
    text = path.read_text(encoding="utf-8")
    low = text.lower()
    for term in terms:
        if term.lower() not in low:
            errors.append(f"{rel}: missing concept {term!r}")

if errors:
    print("PHASE7 FAIL")
    for e in errors:
        print(e)
    raise SystemExit(1)

print(f"PHASE7 PASS\nChecked {len(REQUIRED)} files")
