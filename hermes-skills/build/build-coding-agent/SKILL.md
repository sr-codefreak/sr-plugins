---
name: build-coding-agent
description: "Use for BUILD implementation tasks: branch from default branch, implement with tests, commit, push, and raise PR for manual approval."
version: 1.0.1
author: S R + Hermes Agent
license: MIT
metadata:
  hermes:
    tags: [build, coding, branch, github, implementation]
    related_skills: [build-orchestrator, test-driven-development, github-pr-workflow]
---

# BUILD Coding Agent

## Mission
Implement one Kanban task from the approved LLD without expanding scope.

## Branching Standard
1. Start from repo root.
2. Ensure clean tree.
3. Detect the repository default branch (`gh repo view --json defaultBranchRef -q .defaultBranchRef.name` or `git remote show origin`) instead of assuming `master`.
4. Checkout the default branch and pull latest.
5. Create branch: `build/<build-slug>/<task-slug>`.
6. Implement only the task scope.
7. Write/update tests.
8. Run targeted tests and relevant full/regression tests.
9. Commit with conventional message.
10. Push branch and create PR to the default branch.
11. Record PR URL in `.hermes/builds/<slug>/06-pr.md` or Kanban metadata.

## Implementation Rules
- When the user asks to “fix” a concrete bug, the expected deliverable is product-code implementation PR(s), not another build-artifact-only PR. If PRD/HLD/LLD artifacts already exist, use them as context and proceed to code unless the user explicitly asks to stop at a design gate.
- Follow the LLD contracts exactly.
- If LLD is wrong/missing, block and ask for design revision; do not improvise major architecture.
- Prefer TDD for behavior changes: failing test -> implementation -> passing test.
- Include migration/rollback notes for DB changes.
- For async processing/status bugs, preserve the invariant that records must not enter a processing state until the durable payload exists and the worker task has been successfully queued. See `references/async-processing-finalization.md`.
- Never merge to the default branch yourself; manual approval is required.

## Handoff
Report:
- changed files
- tests run and results
- branch name
- PR URL
- risks/open items
