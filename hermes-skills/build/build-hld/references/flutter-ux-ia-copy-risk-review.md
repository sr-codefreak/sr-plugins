# Flutter UX IA/copy risk review notes

Use for BUILD/HLD review passes where the request is to review Flutter Slice UX, IA, trust/privacy copy, accessibility, and test strategy without modifying files.

## Review workflow
1. Respect explicit `do not modify files`: inspect only. If verification tooling may mutate generated files or lockfiles, avoid it unless necessary; if it does mutate tracked files, restore them and call out what happened.
2. Ground the review in source files, not memory. Prioritize onboarding, recording-mode entry points, schedule creation/editing, settings/privacy surfaces, theme, and existing tests/docs.
3. Treat static policy metadata as evidence of intent, not proof of implemented UX. Verify whether privacy/consent text is actually present at the point of action.
4. Separate findings into: privacy/trust risks, accessibility risks, product/IA risks, and test strategy.
5. Keep Telegram output legible with labeled bullets; avoid tables.

## Privacy/copy checks
- Avoid overclaims such as “secure”, “private”, “fully controlled”, “deleted everywhere”, “never uploaded”, or “encrypted” unless backed by implemented behavior.
- For scheduled/continuous recording, check for point-of-action disclosure: what starts recording, when it can run in background, how the user stops/disables it, and that they need permission to record.
- Flag implementation jargon in user-facing copy: backend, API, Hive, release gate, foreground service, chunk, retention contract, etc.
- Do not let copy promise delete/export/retention controls if backend/API contracts are deferred or absent.

## Accessibility checks
- Recording controls need semantic labels for start/stop/pause/resume; visible adjacent text is not enough for assistive tech.
- Custom visualizations and color state (waveforms, badges, active chips) need textual/semantic equivalents.
- Validate large text scale risks on onboarding, mode selector, schedule editor, and settings.
- Check 44x44 tap target risk for compact segmented controls, chips, switches, icon-only buttons, and destructive actions.
- Validate contrast in dark theme, especially muted secondary text, disabled/inactive chips, warning/error states.

## Test strategy patterns
- Widget tests: onboarding copy, recording mode helper/disclosure copy, schedule editor consent copy, settings copy without implementation jargon.
- Semantics tests: record/stop/pause/resume, schedule toggle/delete, mode selector.
- Golden or screenshot tests: dark theme and large text scale for onboarding, recording, schedule editor, settings.
- Manual QA: first-run onboarding, Manual/Continuous/Scheduled switching, schedule create/edit/delete, recording lifecycle, offline messaging, VoiceOver/TalkBack traversal.

## Verification caveat
When running `flutter test`/`flutter analyze`, report real output. If failures are caused by unrelated or untracked template files (for example a default `test/widget_test.dart` referencing `MyApp` while the app class is named differently), call that out separately from the review findings.