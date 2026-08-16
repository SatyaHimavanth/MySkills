# Project Scoping — Shared

## Purpose

Do not start a greenfield build (or a materially ambiguous feature) on an unresolved design. Settle the user-facing goal, boundaries, constraints, and success conditions before implementation, while avoiding unnecessary ceremony for small, clear changes.

The purpose of this gate is to prevent expensive wrong assumptions—not to force a heavyweight planning process onto every task.

## When this applies

- A new project with no existing codebase to inspect.
- A feature broad enough that reasonable implementations would differ significantly.
- An architectural change with unresolved product or domain decisions.
- A request where missing requirements could materially change the data model, auth model, API contract, deployment shape, or failure behavior.

Does **not** apply to a well-specified endpoint, bugfix, refactor, or small change where the relevant behavior is already clear from the request and repository.

## Preferred: `grill-me` / `grilling`

When the upstream `grill-me` skill is installed and the task needs a real design interview, route the user through it before implementation. The current upstream workflow is dependency-ordered and asks **one question at a time**, with a recommended answer, while instructing the agent to inspect the codebase instead of asking questions the code can answer. Do not replace it with a parallel batch questionnaire. Source: https://github.com/mattpocock/skills/blob/main/skills/productivity/grill-me/SKILL.md

The engineering skill should not duplicate the grilling mechanism. Its responsibility is the gate around it:

1. determine whether the task actually needs the interview
2. let `grill-me` / `grilling` resolve the design branches
3. do not implement until the interview reaches shared understanding
4. translate the settled answers into a concise project/implementation brief
5. use that brief to select the smallest sufficient architecture via `architecture/complexity.shared.md`

`grill-me` is not a reason to ask questions that the repository, existing configuration, or documentation can answer.

## Minimum information required before greenfield implementation

The implementation brief must be clear on:

1. **Goal** — what the system does and for whom.
2. **Scope boundaries** — what is included and explicitly excluded.
3. **Core domain/data** — important entities and relationships in the user's terms.
4. **Auth/authorization** — who can do what, including tenant/resource boundaries when applicable.
5. **Constraints** — compliance, deployment restrictions, existing infrastructure, deadline, budget, portability, or platform constraints.
6. **Success criteria** — what must work for the first usable release.
7. **Non-goals** — related capabilities intentionally deferred.

Implementation details that can be safely inferred from the codebase, framework, or agreed project conventions should not be turned into user questions.

## Complexity gate

After scope is settled, choose the **smallest sufficient architecture**.

Record:

```text
Baseline:
Why it is sufficient now:
Future production seam(s):
Escalation trigger(s):
Local PARTIAL behavior:
```

Do not add Redis, queues, object storage, service decomposition, distributed locks, multi-region deployment, or other infrastructure unless a concrete requirement justifies it.

## Completion gate

Before implementation begins, the agent should be able to answer:

- What are we building?
- What are we not building?
- What are the important data/security boundaries?
- What constraints must not be violated?
- What is the smallest architecture that satisfies the current requirements?
- What production capability is intentionally deferred?
- What concrete event/requirement would trigger that escalation?

If any answer would materially change the design, the scope is not settled.

## Forbidden

- starting a greenfield implementation on an unresolved material requirement
- inventing infrastructure requirements because they are common in production
- asking the user questions that repository inspection can answer
- dumping a wall of unrelated questions instead of using the grilling workflow when it is available
- re-running a full scoping interview for a small, already-clear change
- treating a settled scope as permission to over-engineer future capabilities
