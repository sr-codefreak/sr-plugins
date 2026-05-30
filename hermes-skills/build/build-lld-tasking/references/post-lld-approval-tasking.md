# Post-LLD Approval Tasking Pattern

Use this when the user approves an LLD with language like `Approve proceed`.

## Durable sequence
1. Treat approval as the gate opening for tasking, not for code changes in the current agent session.
2. Update `03-lld.md` status to `Approved` and add an approval log/date if the artifact has one.
3. Create or update:
   - `04-task-plan.md` — implementation slices, dependencies, acceptance criteria, and Kanban IDs once known.
   - `05-test-plan.md` — independent tester/reviewer workstream, verification commands, PR review duties.
4. Run a whitespace/diff sanity check before commit (`git diff --check` in the build-artifacts repo).
5. Commit and push tasking artifacts on their own build-artifacts branch/PR before or immediately after dispatching workers, so review handoff links are durable.
6. Create Kanban tasks only after LLD approval. Create dependency-linked child tasks at creation time when possible.
7. Dispatch coding and testing workers in parallel only after task artifacts exist.
8. Patch `04-task-plan.md` with the actual Kanban task IDs and current status after creation/dispatch.
9. Report: build-artifacts PR link, task IDs, assignees, and which tasks are running.

## Profile naming pitfall
Do not infer profile names from role labels. Run `hermes profile list` and use the actual profile names. In this environment the BUILD profiles may be `buildcoder`, `buildtester`, and `builddeployer` rather than hyphenated names.

## Gate discipline
Post-LLD approval opens task planning and worker dispatch. Implementation still needs a feature branch, tests, implementation PR, tester verification, and manual PR approval before deployment.
