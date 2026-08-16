# AI Agent Skills Repository

A modular collection of production-grade skills and architecture guardrails for AI coding assistants (Antigravity, Claude Code, Cursor, Copilot).

## Available Skills

| Skill Name | Path | Description |
|:---|:---|:---|
| `fastapi-production` | `skills/fastapi-production` | Architecture guardrails for building production-grade FastAPI backends with PostgreSQL, Pydantic v2, SQLAlchemy 2.0, and Argon2id. Defaults to a small-team production target (single region, ~100–1,000 users) with an explicit, gated path to regional/global scale — see `architecture/scale_tiers.shared.md`. Cloud provisioning (AWS/GCP/etc.) is intentionally out of scope; pair with your cloud provider's skill for that layer. |
| `frontend-api-client` | `skills/frontend-api-client` | Generates a typed TypeScript client + Zod runtime validators from a backend's OpenAPI schema (verified against FastAPI) instead of hand-written request/response types, so backend contract drift becomes a build error. |
| *(Future Skills)* | `skills/<skill-name>` | Design System or AI Agent skills will be added here. |

---

## Installation via CLI (`npx skills`)

### 1. Install All Skills from this Repository
To pull all skills in this repository into your AI agent environment:

```bash
npx skills add SatyaHimavanth/MySkills
```

### 2. Install Only a Specific Skill
To pull only the `fastapi-production` backend skill:

```bash
npx skills add SatyaHimavanth/MySkills fastapi-production
```

---

## Manual Installation

To install a skill manually into your local AI workspace:

1. **For Workspace Scope**: Copy `skills/fastapi-production/` into your project's `.agents/skills/` directory:
   ```bash
   cp -r skills/fastapi-production/ .agents/skills/fastapi-production/
   ```
2. **For Global Scope**: Copy `skills/fastapi-production/` into your global config directory:
   ```bash
   cp -r skills/fastapi-production/ ~/.gemini/config/skills/fastapi-production/
   ```

---

## Maintainer tooling

The top-level `requirements/` directory holds this repository's own coverage matrices and audit scripts, used to verify that each skill's files stay internally consistent as they change. It is not part of any individual skill and is not installed by `npx skills add <repo> <skill-name>`; it only matters if you're contributing to this repository.

## Repository Structure

```text
.
├── README.md                           # Repository documentation
├── .gitignore                          # Git ignore rules
└── skills/                             # Skills container directory
    ├── fastapi-production/             # FastAPI Backend Skill
    │   ├── SKILL.md                    # Main skill entrypoint (YAML frontmatter + rules)
    │   ├── api/                        # API route & schema policies
    │   ├── architecture/               # Layered architecture rules + scale_tiers.shared.md (Tier 1 small-team vs Tier 2 regional/global)
    │   ├── async/                      # Job queues & async handling
    │   ├── cache/                      # Redis caching policies
    │   ├── configuration/              # Pydantic Settings v2
    │   ├── database/                   # PostgreSQL, SQLAlchemy 2.0 & Multi-Region
    │   ├── deployment/                 # Production topology & container rules
    │   ├── errors/                     # AppError & exception handlers
    │   ├── http/                       # Outbound HTTP client policies
    │   ├── infrastructure/             # Docker multi-stage builds
    │   ├── middleware/                 # ASGI middleware policies
    │   ├── observability/              # Structlog JSON logging
    │   ├── reliability/                # Lifespan resource management
    │   ├── security/                   # Auth, Argon2id, JWT, Rate Limiting, SSRF
    │   ├── storage/                    # S3 / Object storage
    │   ├── testing/                    # Pytest strategy & markers
    │   └── time/                       # UTC & multi-region NTP handling
    │
    └── (Future Skills Go Here)         # e.g., frontend-production, design-system
```

---

## Adding a New Skill to this Repository

To add a new skill in the future (e.g. `frontend-production`):

1. Create a new subfolder in `skills/`:
   ```bash
   mkdir -p skills/frontend-production
   ```
2. Add a `SKILL.md` inside `skills/frontend-production/` with YAML frontmatter:
   ```markdown
   ---
   name: frontend-production
   description: Modern React/Next.js frontend design system and performance guardrails.
   ---
   ```
3. Commit and push to GitHub. Users can then pull it via:
   ```bash
   npx skills add SatyaHimavanth/MySkills frontend-production
   ```
