# Gate-bounded BUILD continuation pattern

Use when the user asks to add a pending issue as the next BUILD action item and says to complete it only up to a specific gate, such as PRD, HLD, LLD, tasking, or PR.

## Procedure
1. Treat the request as a BUILD continuation, not an ad-hoc fix.
2. Verify current repository, build-artifacts repo, branch, and existing artifacts before assuming prior state.
3. Create or update the build folder under the build-artifacts repository, using `builds/<build-slug>/` for review-facing artifacts when the user prefers GitHub handoffs.
4. Produce only the artifacts required up to the named gate.
5. Run coverage validation between gates:
   - PRD requirements are explicitly represented in HLD.
   - HLD decisions are explicitly represented in LLD.
   - Risks/blockers found by reviewers are folded back into the relevant docs before handoff.
6. Commit and push the docs to a review branch and open a GitHub PR for the build-artifacts repo.
7. Stop exactly at the requested gate. Do not create Kanban coding tasks, implementation branches, or product-code changes unless the user explicitly approves the next gate.

## User-facing summary
Report:
- Review PR link.
- Artifact paths created/updated.
- Key design decision(s).
- Validation evidence at a concise pass/fail level.
- The exact next approval phrase or gate needed to continue.

## Pitfalls
- Do not interpret a gate-bounded BUILD continuation as permission to code.
- When the requested gate is abbreviated (for example, `pr`), interpret it as the PR handoff gate if the surrounding BUILD context supports that reading; complete through a review PR, not deployment/merge.
- If the requested action is already implemented outside product code (for example, an existing Hermes cron job), still produce BUILD artifacts through the requested gate and capture real implementation evidence instead of inventing app/backend coding tasks.
- For cron-backed BUILD items, include the actual stored cron prompt or equivalent job contract in LLD/PR evidence, not just a summary, so reviewers can verify self-contained scheduled-run behavior.
- After creating the GitHub review PR, immediately patch the task/PR handoff artifacts with the PR URL and push a follow-up commit; do not leave `PR pending creation` / `to be filled` placeholders in the final handoff.
- Do not send attachments when GitHub review links are available; this user prefers build-artifacts PRs.
- Do not keep pushing to a review branch after its PR was merged; branch fresh from `origin/main` for the next gate.
