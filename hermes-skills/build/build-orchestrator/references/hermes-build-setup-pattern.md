# Hermes BUILD Setup Pattern

Session-derived setup pattern for turning a BUILD process idea into a reusable Hermes workflow.

## When this reference applies
Use when the user wants a reusable multi-phase BUILD pipeline for software or product ideas, especially when they ask for skills, plugin-like behavior, specialist agents/profiles, and Kanban execution.

## Durable setup pattern
1. **Create class-level BUILD skills**, not one-off idea skills:
   - `build-orchestrator`
   - `build-prd-intake`
   - `build-hld`
   - `build-lld-tasking`
   - `build-coding-agent`
   - `build-test-agent`
   - `build-deployment-agent`
   - `build-ruflo-adapter`
2. **Create specialist Hermes profiles** that match the durable roles:
   - `buildprd`
   - `buildhld`
   - `buildlld`
   - `buildcoder`
   - `buildtester`
   - `builddeployer`
3. **Mirror BUILD skills into each profile** so Kanban-spawned profile workers can load the same BUILD process without relying on the default profile's skill directory.
4. **Customize each profile's `SOUL.md`** with its phase responsibility and the universal BUILD gates.
5. **Create a dedicated Kanban board** such as `build`, separate from project-specific boards.
6. **Write a human-readable overview artifact** such as `~/.hermes/builds/BUILD-PIPELINE.md` with architecture, gates, roles, and first-run instructions.
7. **Verify, don't assume**:
   - default profile sees the BUILD skills;
   - every BUILD profile sees the BUILD skills;
   - profiles appear in `hermes profile list` / Kanban assignees;
   - the Kanban board exists and is empty/ready.

## RUFLO-compatible fallback pattern
If the user asks for RUFLO but native RUFLO is not present, do not block the setup. Install the process with a RUFLO-compatible adapter:

- short review agents -> Hermes `delegate_task`;
- durable workers -> Hermes Kanban tasks assigned to specialist profiles;
- flow graph -> Kanban dependency graph;
- validation loops -> markdown gate + validator subagent + artifact update.

Phrase this as "RUFLO-compatible fallback until native RUFLO is installed," not as a permanent limitation.

## Final handoff shape
The user-facing summary should include:
- skills installed;
- profiles/agents created;
- Kanban board name;
- artifact path;
- architecture diagram;
- phase-by-phase flow;
- RUFLO status/fallback;
- first command/message to start a build, e.g. `BUILD <idea>`.
