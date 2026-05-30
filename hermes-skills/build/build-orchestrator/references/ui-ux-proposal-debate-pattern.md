# UI/UX Proposal Debate Pattern

Use this as a pre-BUILD pattern when the user asks to make an app more user-friendly, review a proposal, or debate UI/UX flows before implementation.

## Trigger

Apply inside the future-build proposal gate when the request is about:
- current-state vs future-state product flows,
- mobile app information architecture,
- onboarding, capture/review loops, or settings/privacy UX,
- persona debate before PRD/HLD/LLD,
- proposal artifacts rather than product-code changes.

Do **not** implement product UI code during this step unless the user has already approved the proposal and advanced through the normal BUILD gates.

## Evidence collection

Inspect the app read-only and capture exact current-state flows from source, routes, screens, labels, and empty/error states. For Flutter/mobile apps, useful targets include:
- app/router/navigation shell,
- onboarding/auth screens,
- primary capture/action screen,
- list/detail output screens,
- settings/privacy/cost screens,
- shared offline/connectivity/error widgets.

Record concrete labels and flows, not generic UX advice. Example format:

```text
Current navigation:
Recording | Requirements | Summaries | Settings

Current mental model:
Requirements -> Recording -> Upload/process -> Summaries -> Settings/cost/privacy

Proposed mental model:
I have a conversation -> I want notes/action items -> I want to find/share them later
```

## Persona debate lenses

Use three parallel lenses by default:
1. **Mobile UX Researcher** — first-run comprehension, user mental model, task success, wording.
2. **Product Designer / Information Architect** — navigation, hierarchy, build slices, visual system impact.
3. **Accessibility / Privacy Skeptic** — consent, recovery, plain language, accessibility, overpromising, trust.

Ask each persona for:
- current-state flow observed,
- friction points ranked by severity,
- proposed friendlier flow,
- what must not be changed yet,
- implementation slice recommendation,
- approval gate risks.

## Synthesis artifact shape

Create proposal artifacts in the build-artifacts repo, normally:

```text
proposals/inbox/<date>-<topic>.md
proposals/debated/<date>-<topic>.md
builds/<build-slug>/00-intake.md
```

The debated proposal should include:
- exact audited files/screens,
- current app IA and mental model,
- proposed user-friendly IA and mental model,
- flow-by-flow current vs proposed states,
- persona debate summary with disagreements,
- prioritized implementation slices,
- gates/risks before coding,
- explicit statement that product code was not modified.

## User-facing final response

Return a concise but concrete summary with:
- docs PR link,
- current-state flows,
- proposed future-state flows,
- debate outcome by persona,
- prioritized build slices/gates,
- confirmation that no product code changed.

For this user, prefer GitHub review links over chat attachments for these artifacts.
