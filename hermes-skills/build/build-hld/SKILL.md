---
name: build-hld
description: Use during BUILD phase 2 to create concise HLD, ADRs, architecture diagrams, options, accepted/rejected flows, and PRD validation.
version: 1.0.0
author: S R + Hermes Agent
license: MIT
metadata:
  hermes:
    tags: [build, hld, architecture, adr, diagrams]
    related_skills: [build-orchestrator, build-prd-intake]
---

# BUILD HLD

## Goal
Create a concise but complete high-level design from the approved PRD.

## Required Sections
Write `.hermes/builds/<slug>/02-hld.md`:

```markdown
# HLD: <title>

## Status
Draft | In review | Approved

## Context

## Architecture Summary

## Current Architecture

## Proposed Architecture

## Diagrams
### System Context
```mermaid
flowchart LR
```
### Request / Event Flow
```mermaid
sequenceDiagram
```
### Component Interaction
```mermaid
flowchart TD
```

## Options Considered
### Option A: <name>
- Pros
- Cons
- Decision: Accepted/Rejected
- Reasoning

## Accepted Flows

## Rejected / Failure Flows

## ADRs
- ADR-001: ...

## Requirement Coverage Matrix
- R1 -> component/flow

## Risks and Mitigations

## Validation Result
Pass | Fail, with missing requirements
```

## ADR Template
For every major architecture decision, create `.hermes/builds/<slug>/02-adr-NNN-<topic>.md` with: Context, Decision, Options, Consequences, Rejected Alternatives.

## Subagent Pattern
Use RUFLO-compatible subagents:
- architecture options reviewer
- risk/security reviewer
- requirement coverage validator

If native RUFLO is unavailable, use `delegate_task` for these reviews.

## UX / IA / Copy Risk Review Mode
Use this when the user asks to review risks, privacy, accessibility, or test strategy for a BUILD UX slice and explicitly says not to modify files.

1. Inspect source/docs/tests directly and do not edit files. If verification tooling may update generated files/lockfiles, either avoid it or restore tracked changes and disclose the tool side effect.
2. Structure the final review into privacy/trust risks, accessibility risks, product/IA risks, and test strategy.
3. For privacy copy, flag overclaims and implementation jargon; distinguish current implemented behavior from release gates/deferred backend contracts.
4. For accessibility, check semantic labels, color-only indicators, large text scaling, tap targets, and dark-theme contrast.
5. For test strategy, recommend widget, semantics, golden/large-text, and manual VoiceOver/TalkBack checks.
6. Keep Telegram output as labeled bullets, not tables.

See `references/flutter-ux-ia-copy-risk-review.md` for a condensed checklist from a Flutter Slice 1 UX IA/copy cleanup review.

Important sequencing pitfall: do not ask the coverage validator to validate an HLD before `02-hld.md` exists. Run option/risk reviewers first, draft the HLD + ADRs, then validate the finished artifact. If a validator runs early and reports “HLD missing,” treat that as expected pre-draft feedback, not a final failure.

## Validator Feedback Loop
If the coverage validator returns `FAIL`, patch `02-hld.md` immediately, then rerun validation before asking the user for approval. Do not leave `Validation Result: Pass` in the HLD unless the most recent validation pass confirms every PRD requirement and NFR is covered. Capture the specific gap in the HLD text, not only in the coverage matrix; validators should see substantive design content for each requirement.

Common pitfall: empty/default-state requirements often include secondary guidance (for example, showing or linking to the active AI Rule/default before capture). If a matrix row claims coverage, ensure the corresponding screen/flow section explicitly includes that behavior.

## Approval Delivery
When the HLD is ready for user review, produce a viewable approval artifact in addition to markdown, preferably:

```bash
pandoc .hermes/builds/<slug>/02-hld.md -o .hermes/builds/<slug>/<title>-HLD-for-approval.docx
```

On Telegram/gateway channels, attach it with a standalone `MEDIA:/absolute/path/to/file.docx` line so the user receives the file directly. Keep the approval prompt short: `Approve HLD` or improvement notes.

### Mobile/Telegram Diagram Pitfall
If the HLD includes flow diagrams, do not rely only on Mermaid inside markdown/docx. The user may not be able to inspect those easily on mobile. Also, raw HTML may not always deliver reliably through Telegram.

For diagram-heavy HLD approvals, also create:
- `<title>-HLD-mobile-view.html` with native inline SVG diagrams and concise visual cards.
- `<title>-HLD-mobile-view.zip` as a Telegram delivery fallback.

Send both the zip and raw HTML if delivery is uncertain:

```text
MEDIA:/absolute/path/to/<title>-HLD-mobile-view.zip
MEDIA:/absolute/path/to/<title>-HLD-mobile-view.html
```

If the user says they did not receive the file, immediately send a zip fallback instead of repeating only the same raw attachment.

## Validation Checklist
Before asking for approval:
1. Confirm the approved PRD status/decision is recorded in `01-prd.md`.
2. Confirm `02-hld.md` exists under the BUILD artifact directory.
3. Confirm all ADR files referenced by the HLD exist.
4. Confirm the coverage matrix maps every approved PRD requirement and NFR.
5. Confirm `Validation Result` is `Pass`; if not, revise and re-run validation.
6. Confirm no implementation/Kanban tasks were created before LLD approval.

## Gate
HLD cannot be approved unless the coverage matrix maps every approved PRD requirement. If any requirement is missing, update HLD and re-run validation.

## References
- `references/foundation-context-hld-pattern.md`: example for foundation/context HLD, ADR set, validation order, and mobile approval artifact delivery.
- `references/hld-validation-and-review-pr-pitfalls.md`: concise runbook for fixing validator coverage failures and handling merged prior-gate PR branches before opening the HLD review PR.

## Coverage Validation Workflow
Use when the user asks to validate PRD requirement coverage for an HLD.

1. Locate the approved PRD and the HLD before judging coverage.
   - Check the project-local build path first when working inside a repo/workspace: `<workspace>/.hermes/builds/<slug>/01-prd.md` and `02-hld.md`.
   - Also check the root Hermes build path when the PRD explicitly says artifacts must live there: `~/.hermes/builds/<slug>/`.
   - If artifacts are split across these locations, call that out as an artifact-path issue.
2. Read the PRD requirements and acceptance criteria directly from `01-prd.md`; do not infer the requirement list from memory.
3. Read `02-hld.md` directly and map each PRD requirement to explicit HLD sections, components, flows, diagrams, ADRs, risks, or validation notes.
4. If `02-hld.md` is missing, return `FAIL` immediately for HLD coverage even if setup artifacts/configuration show some PRD requirements are already satisfied. Include a matrix that distinguishes:
   - evidence satisfied outside the HLD,
   - missing from the HLD,
   - artifact/path issues.
5. Verify objective acceptance criteria with tool output where practical, e.g. OpenAPI parses as 3.x, MCP config entries exist, packages import in the runtime, or Kanban tasks are absent before LLD approval.
6. Keep the final result concise and Telegram-legible: labeled bullets over markdown tables, with a clear overall `PASS` or `FAIL` and the blockers required to pass.

