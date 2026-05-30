# LLD validation for UI/copy-only slices

Session-derived guidance for BUILD Phase 3 when the implementation is mostly mobile IA, UX labels, or presentation copy rather than backend logic.

## Problem pattern
A UI-only LLD can look complete while silently skipping required architecture sections because the backend/API/storage are not changing. Reviewers and downstream coding/test agents still need those sections to know the boundary.

## Durable fix
Include every required LLD section and make non-changes explicit:

- `Database / Storage Design`: state `No database/schema/storage changes` and list the existing persisted objects that remain unchanged.
- `API Contracts`: state `No endpoint/request/response/auth changes` and list existing API surfaces/providers that must remain compatible.
- `Module / Service Breakdown`: separate presentation modules/copy constants from unchanged domain models and data providers.
- `Internal Interfaces`: define any copy facade/constants surface, even if it is just a constants class/file.
- `Rollout / Compatibility`: call out that existing routes, provider names, API contracts, and stored data remain stable.

## Copy scrub checklist
Before approval, search the LLD and proposed UI strings for internal process language that should not appear in product UX:

- Release gate
- Privacy & Readiness
- external testing
- readiness
- raw engineering/testing labels
- backend/contract jargon in user-visible copy

If a term appears only in the LLD as a developer note, label it clearly as non-user-facing.

## Validation approach
Use two review passes:

1. Structural pass: compare the LLD headings against the skill's Required LLD Sections and fail if any are missing.
2. Coverage/copy pass: compare each PRD/HLD/ADR requirement to an implementation unit and test, and inspect user-visible copy for internal language.

Do not make the validation too narrow. A simple string-search for renamed tabs is insufficient; validate boundaries, non-goals, and test coverage as well.
