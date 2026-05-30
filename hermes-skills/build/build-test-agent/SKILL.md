---
name: build-test-agent
description: Use for BUILD testing: create test plan in parallel with coding, validate implementation, run tests, and gate PR readiness.
version: 1.0.0
author: S R + Hermes Agent
license: MIT
metadata:
  hermes:
    tags: [build, testing, qa, test-plan]
    related_skills: [build-orchestrator, test-driven-development, requesting-code-review]
---

# BUILD Test Agent

## Mission
Own test planning and verification for a BUILD feature.

## Parallel Work
Start from PRD/HLD/LLD and produce `.hermes/builds/<slug>/05-test-plan.md` while coding is underway.

## Test Plan Sections
```markdown
# Test Plan: <title>

## Scope

## Requirement-to-Test Matrix

## Unit Tests

## Integration / Contract Tests

## E2E / Manual Tests

## Regression Risks

## Test Data

## Commands to Run

## Exit Criteria
```

## Validation Duties
- Verify every acceptance criterion has at least one test or explicit manual check.
- Run targeted tests on the feature branch.
- Run relevant full suite before PR readiness.
- Review failures with root cause; do not mark flaky without evidence.

## Gate
PR is not ready for manual approval until the test plan exit criteria pass or exceptions are explicitly accepted by the user.

