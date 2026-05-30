# BUILD Skill Pack

Installed local skill pack for S R's standard idea-to-production process.

## Skills
- build-orchestrator
- build-prd-intake
- build-hld
- build-lld-tasking
- build-coding-agent
- build-test-agent
- build-deployment-agent
- build-ruflo-adapter

## Canonical flow
Idea -> questionnaire/PRD -> HLD/ADR/diagrams -> LLD/contracts/tasks -> Hermes Kanban -> code + test -> PR -> manual approval -> deploy.

RUFLO note: native RUFLO was not found during setup, so the skill pack uses a RUFLO-compatible fallback via Hermes delegate_task and Kanban profiles.
