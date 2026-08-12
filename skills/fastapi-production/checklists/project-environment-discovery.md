# Project Environment Discovery Checklist

Run only relevant checks and record results in `.dev/environment.local.md`.

- [ ] OS and architecture
- [ ] Python version
- [ ] uv version
- [ ] Git version
- [ ] Docker CLI/runtime availability if relevant
- [ ] Podman CLI/runtime availability if relevant
- [ ] PostgreSQL client/server availability if relevant
- [ ] Redis availability if relevant
- [ ] required package-manager/network/proxy constraints
- [ ] admin/root permission constraints
- [ ] existing project `.env`/settings structure
- [ ] existing compose/service configuration
- [ ] existing local service installations

For container runtimes, distinguish installed CLI from actual runtime access.
Do not install or reconfigure system software automatically.
