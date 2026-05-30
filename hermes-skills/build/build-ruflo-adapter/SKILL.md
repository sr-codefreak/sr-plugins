---
name: build-ruflo-adapter
description: Use when BUILD calls for RUFLO agents/flows; maps RUFLO concepts to Hermes delegate_task and Kanban until a native RUFLO plugin is installed.
version: 1.0.0
author: S R + Hermes Agent
license: MIT
metadata:
  hermes:
    tags: [build, ruflo, agents, fallback]
    related_skills: [build-orchestrator, subagent-driven-development, kanban-orchestrator]
---

# BUILD RUFLO Adapter

## Status
No native RUFLO plugin/command was found in this Hermes installation during setup. This adapter makes the BUILD pipeline RUFLO-compatible now and easy to swap later.

## Mapping
- **RUFLO short review agent** -> Hermes `delegate_task`
- **RUFLO durable worker** -> Hermes Kanban task assigned to a specialist profile
- **RUFLO flow graph** -> Kanban dependency graph
- **RUFLO validation loop** -> document gate with validator subagent + artifact update
- **RUFLO handoff** -> markdown artifact + Kanban metadata/comment

## Required Agent Roles
- Intake/PRD agent
- HLD architect agent
- LLD designer/task splitter
- Coding agent
- Test agent
- Deployment agent
- Optional reviewer/security agent

## Setup Behavior
When the user asks to set up BUILD with RUFLO and native RUFLO is not available, do not treat that as a blocker. Complete the BUILD setup using this adapter, verify the Hermes fallback path, and clearly label the result as `RUFLO-compatible fallback` so it can be swapped to native RUFLO later.

Recommended setup checks:
- look for an existing RUFLO plugin/command;
- if absent, create/use the BUILD adapter skill;
- verify Hermes profiles and Kanban assignees instead of waiting for RUFLO;
- avoid durable negative claims such as "RUFLO cannot work" — the durable rule is the adapter mapping, not the current machine state.

## Native RUFLO Future Hook
When `ruflo` becomes available, replace fallback calls in artifacts/process notes with native RUFLO flow invocations while preserving the same phase gates and artifact paths.

