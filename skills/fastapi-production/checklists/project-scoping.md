# Project Scoping — Shared

## Purpose
Don't start a greenfield build (or a feature with genuinely unclear scope) on an ambiguous request. Settle goal, boundaries, and constraints first — the cost of an hour of scoping is far lower than the cost of implementing the wrong thing.

## When this applies
- A new project with no existing codebase to inspect.
- A feature request broad enough that reasonable implementations would differ significantly (auth model, data model, what's explicitly out of scope).

Does **not** apply to a well-specified single endpoint/bugfix in an existing project — `checklists/new-endpoint.md` already covers that, and re-scoping a small, clear change adds friction without value.

## Preferred: `grill-me` / `grilling`
If the [`grill-me`](https://github.com/mattpocock/skills) plugin is installed, use it (`/grill-me` or `/grilling`) before starting implementation. It runs a structured, round-based interview — mapping decisions as a tree, asking every question whose prerequisites are settled in one round, recommending an answer for each, and waiting for the user before the next round — until scope is fully settled. This skill deliberately does not reimplement that mechanism inline; it's a separate, independently maintained tool with its own update cycle. Don't vendor a copy of it here.

## Fallback, if not installed
Cover at minimum, in one round, before writing code:
1. **Goal** — what does this system do, for whom, one sentence.
2. **Scope boundaries** — what's explicitly out of scope for this pass.
3. **Data/domain** — the core entities and their relationships, in the user's terms.
4. **Auth model** — who can do what (ties directly into `security/object_authorization.shared.md` / `database/multi_tenancy.shared.md` if multi-tenant).
5. **Non-negotiable constraints** — compliance, existing infra, deadline-driven cuts.
6. **Explicit non-goals** — what looks related but isn't being built now.

Ask these as one batch, recommend a default for each, then implement — don't ask one question, wait, ask the next; that's what `grilling` is for if the project actually needs that depth.

## Forbidden
- starting a greenfield implementation on an unscoped one-line request
- re-running a full scoping interview for a small, already-clear change
