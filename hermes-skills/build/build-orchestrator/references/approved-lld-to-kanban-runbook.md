# Approved LLD → Kanban Runbook

Use this reference when the user approves an LLD and the BUILD pipeline needs to move into implementation.

## Durable pattern
1. **Record approval in artifacts**
   - Update `.hermes/builds/<slug>/03-lld.md` with explicit approval status/date/context.
   - Do not proceed from memory alone; the markdown artifact is the source of truth.
2. **Create `04-task-plan.md`**
   - Derive implementation tasks from the approved LLD, not directly from the original idea.
   - Include task IDs, scope, dependencies, expected assignee/profile, acceptance criteria, verification command(s), and artifact paths.
3. **Discover live Hermes/Kanban state**
   - Verify actual profile names before assigning tasks.
   - Verify Kanban board and task-create syntax before creating tasks.
   - Do not invent profiles, boards, or command flags.
4. **Create a gated dependency graph**
   - Backend/schema foundation tasks usually go first.
   - Contract tests and app-alignment review should wait on schema/API foundation tasks.
   - Final integration/PR task should wait on all coding and testing tasks.
5. **Dispatch only ready tasks**
   - After task creation, dispatch the Kanban board so immediately-ready coding and testing work starts.
   - Confirm spawned worker count and workdirs.
6. **Report operational handles**
   - Return artifact paths, board name, task IDs, statuses, dependencies, and spawned workers.

## Example task graph shape
- T1 coder: foundational backend/OpenAPI/schema hardening
- T2 coder/test: backend route/OpenAPI contract coverage; waits for T1
- T3 coder: backend/worker async contract or integration seam
- T4 tester/reviewer: app/backend API alignment; waits for T1
- T5 coder: reproducibility/tooling hardening
- T6 tester: local readiness verification
- T7 tester/integrator: integration review + PR preparation; waits for T1–T6

## Pitfalls
- Do not create implementation Kanban tasks before LLD approval.
- Do not leave the user with only a plan after approval; create the task artifacts and queue runnable work.
- Do not report success until board state has been verified after dispatch.
