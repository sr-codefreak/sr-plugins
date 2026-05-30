# Future Build Proposal Governance Pattern

Use this pattern when the user asks to explore/prioritize many possible product issues or future builds before starting implementation.

## When to use

Trigger before normal PRD intake when the request is about:
- exploring all issues/improvements,
- prioritizing next builds,
- creating proposal folders or roadmap governance,
- running multiple personas to triage/debate hypotheses,
- approving/rejecting/parking future builds.

This is a pre-BUILD governance layer. It decides **what is worth turning into a BUILD**. It does not authorize coding.

## Recommended artifact layout in the build-artifacts repo

```text
proposals/
  inbox/
  triage/
  debated/
  approved/
  rejected/
  parked/
governance/
  persona-roster.md
  lifecycle.md
  scoring-rubric.md
templates/
  proposal.md
  triage-review.md
  debate-round.md
  decision.md
decision-records/
  FBDR-0001-<topic>.md
builds/<build-slug>/
  00-intake.md
```

Use `FBDR` for Future Build Decision Records so roadmap/product decisions stay distinct from architecture ADRs.

## Persona triage pattern

Run short, evidence-oriented persona reviews before synthesis. Useful default personas:
- Product Lead: roadmap coherence and final recommendation.
- User Research Lead: workflow pain, user value, UX friction.
- Bug / Reliability Research Lead: defects, broken contracts, CI/test gaps, operational risk.
- Architecture Lead: cross-repo boundaries and contracts.
- Security / Privacy Lead: PII, consent, retention, deletion, secrets, access control.
- Cost / Budget Lead: LLM/transcription/storage/cloud spend.
- Delivery / Test Lead: BUILD readiness, acceptance criteria, task slicing.
- Product Skeptic: counterarguments, overbuilding checks, smaller alternatives.
- Data / Memory Lead: retrieval, correction, source attribution, stale-memory risk.
- Integration Lead: client apps, CLI, webhooks, GitHub, external APIs.

For speed, start with three parallel lenses when the request is broad:
1. User Research Lead
2. Bug / Reliability Research Lead
3. Product Lead

Then synthesize into a decision matrix.

## Debate / scoring mechanics

Each candidate should have:
- hypothesis: `If <change>, then <measurable outcome>, because <reason>`
- arguments for
- arguments against
- counterfactuals: do nothing, manual workaround, smaller build
- risk review: privacy/security, reliability, cost, delivery, product/UX
- smallest validating build
- recommendation: approve, reject, park, research spike, or fast-track

Suggested weighted rubric:
- User Value: 25%
- Strategic Fit: 15%
- Evidence Strength: 10%
- Delivery Feasibility: 15%
- Risk-Adjusted Confidence: 15%
- Cost Efficiency: 10%
- Learning Value: 10%

Decision bands:
- 4.2-5.0: strong approve candidate
- 3.5-4.19: approve if capacity exists or strategically urgent
- 2.8-3.49: park or run research spike
- 2.0-2.79: reject unless mandatory
- <2.0: reject

## Gate discipline

- Agent recommendation is not user approval.
- Moving a proposal to approved requires explicit user approval.
- Proposal approval authorizes BUILD intake only.
- Implementation still requires approved PRD, HLD, and LLD.
- Do not create implementation Kanban tasks until LLD approval.

## Practical GitHub handoff

For substantial proposal-governance work:
1. Create/update artifacts in the build-artifacts repo, not chat attachments.
2. Open a docs PR for review.
3. Include the PR link and a concise next-build ranking in the user-facing summary.
4. Keep parked/rejected proposals as first-class artifacts so the rationale is not lost.
