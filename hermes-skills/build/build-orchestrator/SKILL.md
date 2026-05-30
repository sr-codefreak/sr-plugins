---
name: build-orchestrator
description: Use when the user says BUILD/build/let us build an idea and wants the full Hermes pipeline from idea intake to PR and deployment.
version: 1.0.0
author: S R + Hermes Agent
license: MIT
metadata:
  hermes:
    tags: [build, prd, hld, lld, kanban, ruflo, orchestration]
    related_skills: [build-prd-intake, build-hld, build-lld-tasking, build-coding-agent, build-test-agent, build-deployment-agent, kanban-orchestrator]
---

# BUILD Orchestrator

## Purpose
BUILD is the default process for every substantial software or product idea. It turns a raw idea into approved documents, Kanban tasks, implementation branches, tests, PRs, and deployment.

## Trigger
Use this skill when the user says any of: "BUILD", "build this", "new idea", "turn this into a project", "new feature", or asks to run the full pipeline.

## Pipeline
0. **Future-build proposal gate, when needed** — if the user asks to explore/prioritize many possible issues, roadmap ideas, UX improvements, or next builds, first create proposal-governance artifacts in the build-artifacts repo: persona roster, proposal lifecycle, triage/debate templates, scoring rubric, candidate proposals, and a decision matrix. Agent recommendations are advisory; explicit user approval is still required before a proposal becomes BUILD intake. See `references/future-build-proposal-governance.md`. For UI/UX friendliness requests, audit current flows read-only, run UX/product/accessibility persona debate, and capture exact current-state vs proposed flows before any implementation; see `references/ui-ux-proposal-debate-pattern.md`.
1. **PRD / questionnaire gate** — load `build-prd-intake`; ask targeted questions; write every discussion to an `.md` artifact; end with an approved PRD.
   - If the user asks to add an item as the next BUILD action and complete it only up to a named gate, run a gate-bounded continuation: verify current state, create/update artifacts only through that gate, open a build-artifacts review PR, and stop before coding or task creation. See `references/gate-bounded-build-continuation.md`.
2. **HLD gate** — load `build-hld`; use RUFLO-style subagents (`delegate_task` now; native RUFLO when installed) for architecture options, ADRs, diagrams, accepted/rejected flows, validation against PRD.
3. **LLD gate** — load `build-lld-tasking`; produce DB/API/service/test/contracts; validate against HLD + PRD; only then create implementation tasks.
4. **Task split + Kanban** — create Hermes Kanban tasks only after LLD approval. Use actual profile names from `hermes profile list`; do not invent assignees.
5. **Parallel coding + testing** — coding and test-plan agents work in parallel where safe. Each code task branches from `master`, names branch after the build, commits, runs tests on the feature branch, raises a PR to `master`, and waits for manual approval.
6. **Deployment gate** — after PR/manual approval and green tests, load `build-deployment-agent` and run deployment with rollback checks.

## Build Artifact Layout
For each build, create a local folder:

```text
.hermes/builds/<build-slug>/
  00-intake.md
  01-prd.md
  02-hld.md
  02-adr-*.md
  03-lld.md
  04-task-plan.md
  05-test-plan.md
  06-pr.md
  07-deployment.md
```

Use the same `build-slug` for folder, branches, and Kanban board/task labels.

## Build Artifact Review Repository
The user prefers review via GitHub links, not chat file attachments. For substantial BUILD runs, maintain a dedicated GitHub repository for BUILD artifacts (for example `<project>-builds`) and commit the `.hermes/builds/<build-slug>/` contents there after each gate or handoff. Send the GitHub tree/blob link for review. File attachments are a fallback only when GitHub is unavailable or explicitly requested.

### Gate-to-gate PR continuity pitfall
Review PRs may be merged by the user between gates while the local session is still on the old feature branch. Before committing the next gate's artifact, fetch and inspect the PR/branch state. If the prior review PR is merged, create a fresh branch from `origin/main` for the next gate and cherry-pick or reapply only the new gate changes; do not keep pushing to a merged review branch and assume the PR remains open. This keeps each gate reviewable as its own PR and avoids hidden commits on already-merged branches.

Recommended pattern:
1. Create or reuse a private build-artifacts repo with `gh repo create <owner>/<project>-builds --private`.
2. Mirror each build under `builds/<build-slug>/`.
3. Commit gate artifacts (`01-prd.md`, `02-hld.md`, `03-lld.md`, `04-task-plan.md`, `06-pr.md`) with clear `docs:` messages.
4. Put the build repo link at the top of `06-pr.md` and in the user-facing summary.

## Gates
- **PRD approval required before HLD.**
- **HLD approval required before LLD.**
- **LLD approval required before Kanban implementation tasks.**
- **Manual PR approval required before merge/deploy.**

If validation fails at any gate, loop back to the prior document, update the markdown artifact, and re-validate.

## RUFLO Adapter Rule
RUFLO is the preferred agent-flow layer. If a native `ruflo` command/plugin is unavailable, use Hermes `delegate_task` for short subagent reviews and Hermes Kanban profiles for durable work. Always label those runs as "RUFLO-compatible fallback" in artifacts so they can be swapped to native RUFLO later.

## First Response Shape
When starting a build, ask for or derive:
- Build name / slug
- Problem statement
- Target users
- Success metrics
- Constraints and non-goals
- Repository/path
- Deployment target
Then create `00-intake.md` and proceed with the questionnaire.

## References
- `references/hermes-build-setup-pattern.md` — session-derived recipe for installing the BUILD skill pack, specialist profiles, profile skill mirroring, Kanban board, verification checks, and RUFLO-compatible fallback.
- `references/approved-lld-to-kanban-runbook.md` — runbook for the post-LLD approval transition: record approval, generate `04-task-plan.md`, create gated Kanban tasks, dispatch ready work, and report verified task IDs.
- `references/github-build-artifacts-and-pr-handoff.md` — pattern for committing BUILD artifacts to a GitHub review repo, sending review links instead of files, and handling worker-profile GitHub auth gaps without blocking downstream tasks.
- `references/kanban-review-required-pr-unblock.md` — runbook for BUILD Kanban tasks that block as `review-required` after pushing branches/tests because worker profiles lack GitHub auth; open PRs from an authenticated orchestrator profile, complete logistics-only blockers, dispatch dependents, and preserve QA evidence/human gates.
- `references/future-build-proposal-governance.md` — pre-BUILD proposal system pattern: issue/improvement triage personas, hypothesis debate, scoring, approve/reject/park decisions, and docs-PR handoff in the build-artifacts repo.
- `references/ui-ux-proposal-debate-pattern.md` — UI/UX proposal pattern: read-only current-flow audit, UX/product/accessibility persona debate, exact current-state vs future-state flows, docs-PR handoff, and no product-code changes before approval.
- `references/approved-proposal-to-prd-handoff.md` — after a proposal/debate PR is approved/merged, create the PRD on a fresh branch from current `origin/main`, mark intake approved-for-PRD, and ask for explicit PRD gate approval before HLD.
- `references/gate-bounded-build-continuation.md` — pattern for adding the next BUILD action item and completing only through a requested gate, with docs PR handoff and no coding/task creation before approval.

## Verification Checklist
- [ ] Artifacts created under `.hermes/builds/<slug>/`
- [ ] PRD has explicit approval before HLD
- [ ] HLD validates all PRD requirements
- [ ] LLD validates all HLD decisions
- [ ] Kanban tasks exist only after LLD approval
- [ ] BUILD skills are visible to the default profile and any specialist BUILD profiles used by Kanban
- [ ] Kanban board/assignees are verified before creating tasks
- [ ] Feature branches originate from `master`
- [ ] Tests pass before PR
- [ ] PR link captured and manual approval requested
- [ ] Deployment has rollback notes

