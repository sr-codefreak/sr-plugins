# Mobile approval artifacts for BUILD LLD

Use this pattern when an LLD contains diagrams and the approval channel is Telegram/mobile.

## Problem observed
- DOCX/Markdown artifacts can hide or render Mermaid diagrams poorly on mobile.
- Raw HTML attachments may not always arrive or preview reliably in Telegram.
- Re-sending the same single artifact is not enough when the user says they did not receive it.

## Recommended outputs
Create all of these in the build artifact directory:

1. `03-lld.md` — canonical source.
2. `AI-...-LLD-for-approval.docx` — text-friendly review copy.
3. `AI-...-LLD-for-approval.html` — full pandoc HTML if useful.
4. `AI-...-LLD-mobile-view.html` — concise mobile-readable review artifact.
5. `AI-...-LLD-mobile-view.zip` — zipped HTML fallback for Telegram delivery.

## Mobile HTML shape
- Inline CSS; no external assets.
- Native inline SVG diagrams instead of Mermaid-only blocks.
- Cards for requirements, decisions, protected rules, and validation results.
- Short approval section at the end.

## Verification
Before sending:

```bash
python3 - <<'PY'
from html.parser import HTMLParser
from pathlib import Path
p = Path('<build-slug>-LLD-mobile-view.html')
HTMLParser().feed(p.read_text())
print('mobile_html_parse=ok')
PY
zip -q -j <build-slug>-LLD-mobile-view.zip <build-slug>-LLD-mobile-view.html
stat -f '%N %z bytes' <build-slug>-LLD-mobile-view.html <build-slug>-LLD-mobile-view.zip
```

## Telegram delivery pattern
Send both:

```text
MEDIA:/absolute/path/to/AI-...-LLD-mobile-view.zip
MEDIA:/absolute/path/to/AI-...-LLD-mobile-view.html
```

If the user reports non-delivery, send the zip first, then the raw file again.
