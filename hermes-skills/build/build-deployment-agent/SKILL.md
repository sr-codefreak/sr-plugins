---
name: build-deployment-agent
description: Use after BUILD PR approval to deploy safely with preflight checks, rollout, smoke tests, monitoring, and rollback plan.
version: 1.0.0
author: S R + Hermes Agent
license: MIT
metadata:
  hermes:
    tags: [build, deployment, release, rollback]
    related_skills: [build-orchestrator]
---

# BUILD Deployment Agent

## Mission
Deploy only after manual PR approval, merge readiness, and green tests.

## Deployment Artifact
Write `.hermes/builds/<slug>/07-deployment.md`:

```markdown
# Deployment: <title>

## Preflight
- approved PR
- green tests/CI
- secrets/config checked
- migrations reviewed
- rollback path ready

## Release Steps

## Smoke Tests

## Monitoring / Alerts

## Rollback Plan

## Result
Success | Rolled back | Blocked
```

## Deployment Rules
- Confirm target environment and blast radius.
- Capture exact commands and outputs.
- Run smoke tests after deploy.
- If smoke tests fail, execute rollback or block immediately.
- Report deployment status with evidence.

