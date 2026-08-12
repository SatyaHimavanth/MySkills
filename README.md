# AI Agent Skills Repository

A modular collection of production-grade skills and architecture guardrails for AI coding assistants (Antigravity, Claude Code, Cursor, Copilot).

## Available Skills

| Skill Name | Path | Description |
|:---|:---|:---|
| `fastapi-production` | `skills/fastapi-production` | Architecture guardrails for building production-grade FastAPI backends with PostgreSQL, Pydantic v2, SQLAlchemy 2.0, Argon2id, and multi-region deployment. |
| *(Future Skills)* | `skills/<skill-name>` | Frontend, Design System, or AI Agent skills will be added here. |

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

## Repository Structure

```text
.
├── README.md                           # Repository documentation
├── .gitignore                          # Git ignore rules
└── skills/                             # Skills container directory
    ├── fastapi-production/             # FastAPI Backend Skill
    │   ├── SKILL.md                    # Main skill entrypoint (YAML frontmatter + rules)
    │   ├── api/                        # API route & schema policies
    │   ├── architecture/               # Layered architecture rules
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
