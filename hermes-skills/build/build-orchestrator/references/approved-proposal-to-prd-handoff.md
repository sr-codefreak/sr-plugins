# Approved Proposal to PRD Handoff

Use this when a future-build proposal/debate artifact has been approved and the user says to proceed with the BUILD pipeline.

## Durable pattern

1. Treat the user's approval as approval to enter the BUILD pipeline, not as automatic PRD approval unless they explicitly say the PRD itself is approved.
2. Update the proposal/intake status to show it is approved for PRD.
3. Draft `builds/<slug>/01-prd.md` from the approved proposal/debate artifacts.
4. Carry forward proposal defaults explicitly, including:
   - chosen product terminology,
   - deferred alternatives,
   - slice boundaries,
   - non-goals,
   - privacy/accessibility constraints,
   - open decisions that need gate approval.
5. Push the PRD as a new review handoff and ask for the PRD gate decision before HLD.

## Git branch hygiene after proposal PRs

If the proposal/debate PR has already been merged, do **not** keep appending new BUILD-gate commits to the same stale feature branch. Instead:

```bash
git fetch origin
git checkout -B build/<slug>-prd origin/main
# apply/copy the PRD changes
git diff --check
git add builds/<slug>/00-intake.md builds/<slug>/01-prd.md
git commit -m 'docs: add <slug> PRD'
git push -u origin build/<slug>-prd
```

Why: proposal PR branches may still exist locally/remotely after merge, but the review PR is closed. New gate artifacts need a fresh branch from current `origin/main` so GitHub creates a clean PR for the next gate.

## PR body shape

Include:

- Summary of changed artifacts.
- Gate status: `PRD is in review; after user approval proceed to HLD`.
- Verification: `git diff --check`.
- Link to the source proposal/debate artifacts when useful.

## Pitfalls

- Do not skip PRD review just because the proposal was approved. BUILD gates remain: proposal approval -> PRD draft -> explicit PRD approval -> HLD.
- Do not claim product-code work has started while still in the build-artifacts repo.
- If the implementation repo path is not a git repo at the expected root, record it as an open implementation-discovery item for HLD/LLD instead of blocking PRD drafting.
