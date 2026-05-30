# HLD Validation and Review PR Pitfalls

Use this reference when a BUILD HLD gate is being prepared after PRD approval.

## Pattern: validator failure is actionable design feedback

A coverage validator can return `FAIL` even when the HLD has a coverage matrix if the substantive screen/flow section does not describe the required behavior. Treat this as a design gap, not a paperwork issue.

Workflow:

1. Read the exact PRD requirement/NFR that failed.
2. Patch the corresponding HLD design section, not only the coverage matrix.
3. Patch the coverage row to point to the new substantive content.
4. Rerun validation.
5. Keep `Validation Result: Pass` only after the rerun passes.

Example class of gap: an empty-state requirement may say the Capture screen should guide users to start recording *and* choose/confirm AI Rules. The HLD should explicitly include both, such as:

- show the active AI Rule/default state before recording,
- if no rule exists, explain that defaults can be used or an AI Rule can be created,
- provide a secondary CTA/link to AI Rules when feasible.

## Pattern: prior gate PR may already be merged

Before pushing HLD artifacts, check whether the PRD review PR was merged. If it was:

1. Fetch origin.
2. Create a fresh branch from `origin/main` for HLD review.
3. Cherry-pick/reapply only the HLD gate changes.
4. Open a new review PR for HLD.

Do not assume the previous PR remains open just because the local branch still exists.
