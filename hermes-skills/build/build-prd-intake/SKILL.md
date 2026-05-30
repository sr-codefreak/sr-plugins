---
name: build-prd-intake
description: Use during BUILD phase 1 to question the user, capture requirements, and produce an approved PRD markdown artifact.
version: 1.0.0
author: S R + Hermes Agent
license: MIT
metadata:
  hermes:
    tags: [build, prd, requirements, questionnaire]
    related_skills: [build-orchestrator]
---

# BUILD PRD Intake

## Goal
Turn a rough idea into a crisp PRD by asking enough questions to understand the requirement deeply. Store every meaningful discussion and decision in markdown.

## Question Bank
Ask only what is relevant, but cover these dimensions before approval:

1. **Problem** — What pain are we solving? Why now? What happens if we do nothing?
2. **Users** — Who uses it? Admin vs end user? Telegram/CLI/web/API?
3. **Current workflow** — What exists today? What repo/path/system is involved?
4. **Desired workflow** — Happy path, alternate path, failure path.
5. **Scope** — Must-have, should-have, nice-to-have, explicit non-goals.
6. **Data** — Inputs, outputs, persistence, privacy, retention, ownership.
7. **Integrations** — Hermes tools, gateway, Kanban, cron, GitHub, DBs, external APIs.
8. **Quality attributes** — latency, reliability, security, observability, scale, cost.
9. **Acceptance criteria** — concrete checks, examples, and demo script.
10. **Deployment** — environment, secrets, rollback, monitoring.

## Artifact Template
Write/update `.hermes/builds/<slug>/01-prd.md`:

```markdown
# PRD: <title>

## Status
Draft | In review | Approved

## Problem

## Goals

## Non-goals

## Users / Personas

## Requirements
### Functional
- R1: ...
### Non-functional
- NFR1: ...

## User Flows
### Happy Path
### Edge / Rejected Flows

## Data & Integrations

## Acceptance Criteria
- AC1: Given..., when..., then...

## Open Questions

## Decision Log
- YYYY-MM-DD: ...
```

## Approved Proposal Handoff
When the PRD comes from a previously debated/approved proposal:

1. Treat proposal approval as approval to draft the PRD, not automatic PRD approval unless the user explicitly says so.
2. Set the proposal/intake artifact to approved-for-PRD and create `01-prd.md` with `Status: In review`.
3. Preserve the debate outputs as PRD defaults: chosen terminology, deferred options, non-goals, slice boundaries, privacy/accessibility constraints, and open decisions.
4. Ask for a focused PRD gate response: `Approve PRD`, `Revise PRD`, or `Approve with changes`.
5. Only after explicit PRD approval should the BUILD pipeline proceed to HLD.

## Gate
Do not move to HLD until the PRD says `Status: Approved` or the user explicitly approves in chat.

