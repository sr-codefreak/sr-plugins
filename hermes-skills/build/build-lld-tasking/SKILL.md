---
name: build-lld-tasking
description: Use during BUILD phase 3 to produce detailed design, contracts, DB/API/service specs, and split approved LLD into Kanban tasks.
version: 1.0.0
author: S R + Hermes Agent
license: MIT
metadata:
  hermes:
    tags: [build, lld, tasking, api, database, kanban]
    related_skills: [build-orchestrator, build-hld, kanban-orchestrator]
---

# BUILD LLD + Tasking

## Goal
Convert an approved HLD into a detailed, implementable LLD. Only after LLD approval, split work into Hermes Kanban tasks.

## Required LLD Sections
Write `.hermes/builds/<slug>/03-lld.md`:

```markdown
# LLD: <title>

## Status
Draft | In review | Approved

## Design Inputs
- PRD path
- HLD path
- ADR paths

## Module / Service Breakdown

## Database / Storage Design
- Tables/collections
- indexes
- migrations
- retention/privacy

## API Contracts
- endpoint/tool/function
- request schema
- response schema
- errors
- auth

## Internal Interfaces

## Sequence / State Diagrams

## Error Handling and Rejected Flows

## Observability
- logs
- metrics
- traces
- alerts

## Test Strategy
- unit
- integration
- contract
- e2e/manual

## Rollout / Compatibility

## Coverage Matrix
- HLD decision -> LLD section
- PRD requirement -> implementation unit/test
```

## Task Plan
After LLD approval, write `.hermes/builds/<slug>/04-task-plan.md` with small tasks:
- 1 task = 30-120 minutes of work
- each task has inputs, files likely touched, acceptance criteria, tests, dependencies
- independent coding and testing tasks can run in parallel

Also create `.hermes/builds/<slug>/05-test-plan.md` for the parallel tester/reviewer workstream. When approval arrives in short form (for example, `Approve proceed`), treat it as approval to update `03-lld.md` to `Approved`, create task/test artifacts, create Kanban tasks, and dispatch BUILD workers — not as approval to skip the implementation PR/manual approval gate.

## Approval Delivery
When the LLD is ready for user review, produce more than a raw markdown/docx artifact when diagrams are involved. Telegram/docx often makes Mermaid diagrams hard to inspect on mobile.

Preferred approval bundle:
1. `03-lld.md` — canonical source.
2. `<title>-LLD-for-approval.docx` — text-friendly review copy.
3. `<title>-LLD-mobile-view.html` — mobile-readable HTML with native inline SVG diagrams or simplified visual cards instead of Mermaid-only blocks.
4. `<title>-LLD-mobile-view.zip` — zip the HTML as a fallback because Telegram may not reliably deliver or preview raw HTML.

Use standalone `MEDIA:/absolute/path/to/file` lines for attachments. If the user says they did not receive the file, immediately send a `.zip` fallback and the raw file again; do not just repeat the same single attachment.

## Diagram Legibility Rule
For approval artifacts sent over Telegram, Mermaid diagrams inside docx/markdown are not enough. Include a mobile-readable HTML summary with:
- native inline SVG for key flows,
- short cards for decisions/coverage,
- minimal text around diagrams,
- a clear approval ask (`Approve LLD` or improvement notes).

## Kanban Creation Rules
- Run `hermes profile list` first; use only real profiles and their exact names. Do not assume hyphenated names; local BUILD profiles may be `buildcoder`, `buildtester`, and `builddeployer`.
- Create tasks only after LLD approval.
- Link dependencies with parent IDs at creation time.
- Assign coding tasks to the real coder profile (`buildcoder`/`build-coder` as discovered).
- Assign test-plan/review tasks to the real tester profile (`buildtester`/`build-tester` as discovered).
- Assign deployment tasks to the real deployer profile only after PR approval.
- After creation/dispatch, patch `04-task-plan.md` with the actual Kanban task IDs, assignees, and initial statuses so the tasking artifact remains the durable handoff record.

## LLD Self-Validation Before Review
Before committing or requesting approval, run a self-review against the Required LLD Sections and the approved PRD/HLD/ADRs. Do not rely on the fact that a slice is UI-only or copy-only to omit architecture sections.

Checklist:
- Every required LLD section exists, even when the answer is explicitly `No changes / N/A`.
- For UI-only/mobile IA slices, `Database / Storage Design` and `API Contracts` must still state that schemas/endpoints are unchanged and name the existing models/routes that remain stable.
- Copy and IA changes should include a presentation-only boundary: internal provider/model/API names may remain unchanged while user-facing labels change.
- Search the draft for internal or release-process language that should not surface to end users (examples: `Release gate`, `Privacy & Readiness`, `external testing`, `readiness`, raw engineering/testing labels).
- Validate the Coverage Matrix includes both implementation units and tests for each PRD/HLD requirement, not just string-search checks.

## Gate
No code changes before LLD approval.

## References
- `references/mobile-approval-artifacts.md`: Telegram/mobile approval artifact pattern using native-SVG HTML plus zip fallback when diagrams or file delivery are problematic.
- `references/lld-ui-copy-slice-validation.md`: Lessons from a UI/copy-only mobile IA LLD: keep required sections explicit, mark non-changing backend/API/storage boundaries, and scrub internal process copy before review.
- `references/post-lld-approval-tasking.md`: Post-approval sequence for marking the LLD approved, creating `04-task-plan.md`/`05-test-plan.md`, creating Kanban IDs, dispatching workers, and preserving the manual PR gate.

