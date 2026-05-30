# Kanban review-required PR unblock pattern

Use this when BUILD coding/test Kanban workers finish real work but block with `review-required` because their isolated profile cannot open or inspect GitHub PRs.

## Trigger

A worker task is `blocked` with evidence that implementation or QA completed, but the blocker is handoff/review logistics rather than unfinished work, commonly:

- branch pushed successfully
- commit hash and changed files are reported
- tests/static checks are reported
- `gh` or `GH_TOKEN` is unavailable inside the worker profile
- task asks the orchestrator/user to open a PR from a `pull/new/...` URL

Do **not** treat this as a failed implementation task if the branch and evidence exist.

## Orchestrator actions

1. Inspect the task handoff and capture:
   - branch name
   - intended base branch, especially for stacked PRs
   - commit hash
   - changed files
   - tests/checks and known caveats
2. From an authenticated profile/session, create the PR with `gh pr create`.
   - Use the worker's intended base branch for stacked slices.
   - If the worker provided only a pull/new URL, derive `--head` from that branch.
3. Comment on the blocked task with the PR URL and say the GitHub-auth blocker is resolved.
4. Complete the implementation task with a summary that preserves the worker evidence and PR URL.
5. Run `hermes kanban --board <board> dispatch` so dependent tasks promote/spawn.
6. For final QA tasks that block with `review-required` after running tests, distinguish:
   - true blockers: missing branch, missing tests, failing slice-specific checks
   - human gates: manual text-scale/screen-reader QA, accepted analyzer-warning exception, manual PR approval
   If only human gates remain, complete the QA task as `conditionally ready for human PR review`, and report the remaining gates to the user.

## Evidence to record in BUILD artifacts

Update the build artifact repo after nudging/completing tasks:

- `05-test-plan.md` with final QA evidence if the tester updated it
- `06-pr.md` with implementation PR stack, branch/commit evidence, commands/results, and human gates

Then commit/push the artifact branch and open or update the build-artifacts PR.

## Pitfalls

- Do not repeatedly unblock the same worker just to ask it to open a PR when the only blocker is missing GitHub auth in that profile.
- Do not mark a task failed solely because `gh` is unavailable in the worker profile; use an authenticated orchestrator/default profile when available.
- Do not call the work auto-merge ready just because tests passed. BUILD still requires manual PR approval, and manual mobile/accessibility QA may remain a human gate.
- For stacked PRs, base each PR on the previous slice branch, not always on `main`, unless the worker explicitly says otherwise.
