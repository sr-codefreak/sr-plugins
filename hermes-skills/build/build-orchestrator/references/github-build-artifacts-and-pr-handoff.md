# GitHub BUILD artifacts + PR handoff pattern

Session-derived pattern for BUILD runs where the user wants review links instead of files in chat.

## When to use

Use this when a BUILD run has reviewable markdown/doc artifacts or PR handoffs and the user expects GitHub review links.

## Pattern

1. Keep canonical working artifacts locally under:
   - `.hermes/builds/<build-slug>/`
2. Create or reuse a private GitHub review repo:
   - `<owner>/<project>-builds`
   - Example: `<owner>/<project>-builds`
3. Mirror the build folder into the repo at:
   - `builds/<build-slug>/`
4. Commit after each approved gate or handoff:
   - `docs: add <build> BUILD artifacts`
   - `docs: update <build> PR handoff`
5. Send the GitHub tree link for review instead of attaching generated files:
   - `https://github.com/<owner>/<project>-builds/tree/main/builds/<build-slug>`
6. Put the same review repo link at the top of `06-pr.md`.

## PR handoff contents

`06-pr.md` should include:

- build artifact review repo link
- every open implementation PR link
- repo, branch, commit, changed files
- local test commands and exact pass/blocker output summaries
- GitHub check/merge-state summary
- explicit manual-review gate before merge/deploy
- open pre-deploy blockers such as environment-limited Docker health checks

## Worker/profile auth pitfall

Hermes root `gh` auth may work while Kanban worker profiles still cannot see `GH_TOKEN`/`GITHUB_TOKEN` or a `gh` login. If worker PR creation blocks on auth but the orchestrator has valid GitHub auth:

1. Create/verify the PRs from the orchestrator/root profile.
2. Comment the task with the PR URL and check status.
3. Complete the task as a `review-required` handoff if implementation/tests are already done.
4. Dispatch the board so downstream gated tasks can proceed.

Do not leave completed implementation tasks stuck just because the worker profile cannot create the PR itself, provided the orchestrator can create the PR and preserve the manual review gate.

## Active unblock playbook for review-required Kanban tasks

When the user asks how to unblock completed BUILD tasks, be active: inspect the blocked task handoff, create missing PRs if root/orchestrator GitHub auth works, then complete and dispatch the gated board. Do not ask the user to manually create PRs unless both worker and orchestrator auth are unavailable.

Recommended sequence:

1. Verify root/orchestrator auth with `gh auth status` and identify the pushed branch from the task comments.
2. Create or reuse the PR with `gh pr view <branch>` then `gh pr create --base <main|master> --head <branch> ...`.
3. Check PR state/checks with `gh pr view --json url,state,mergeStateStatus,statusCheckRollup`.
4. Add a Kanban comment containing the PR URL and check status.
5. Mark the task done with a `review-required` summary, preserving the manual review gate.
6. Run one dispatcher pass so newly unblocked child tasks start.
7. Update `06-pr.md` and mirror the build artifacts repo so the user has one review link.

If a child PR includes parent-branch commits because the parent PR has not merged yet, state that clearly in the PR body and handoff instead of blocking. The manual review/merge order remains the gate.

## Durable worker-profile GitHub auth fix

For future workers, put the token in each BUILD worker profile environment and restart the gateway/dispatcher so new worker processes inherit it:

```bash
# ~/.hermes/profiles/buildcoder/.env
GH_TOKEN=...
GITHUB_TOKEN=...

# ~/.hermes/profiles/buildtester/.env
GH_TOKEN=...
GITHUB_TOKEN=...
```

Use `GH_TOKEN`/`GITHUB_TOKEN` with at least `repo` for private repos and PR creation. Add `workflow` only when workers must modify or dispatch GitHub Actions workflows.
