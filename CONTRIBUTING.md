# Contributing to sr-plugins

Thanks for considering a contribution. This repo is a small collection of
Claude Code / Cowork plugins, each living in its own folder
(`sr-plugins/<plugin-name>/`).

## Before you open a PR

1. **Read the [DISCLAIMER](./DISCLAIMER.md).** Anything you contribute is
   covered by the same "research / educational, not advice" framing.
2. **Don't commit personal data.** No real portfolios, no API keys, no
   absolute paths to your home folder, no scraped content from gated sources.
   The repo's `.gitignore` covers the most common slip-ups (your real
   `stock-universe.md`, `company-analysis/` outputs, `.DS_Store`, `.env`,
   credentials) — please double-check `git status` before pushing.
3. **Check your output is reproducible.** If you change a skill prompt or
   a scoring rule, run the orchestrator end-to-end on at least one example
   ticker and eyeball the resulting report.

## How to propose a change

- **Bug fix or small tweak** — open a PR directly with a short description.
- **New criterion / scoring rule / phase** — open an issue first so we can
  agree on the methodology before you spend time wiring it up.
- **New plugin** — add a sibling folder under `sr-plugins/<your-plugin-name>/`
  with its own `.claude-plugin/plugin.json` and `README.md`. Follow the
  layout `fa-plugin/` uses.

## Style

- Markdown skills / agents: keep prompts terse and rule-based; prefer
  checklists over prose.
- Python scripts: target Python 3.10+, type-hint public functions, keep
  external deps minimal (the existing pin is `beautifulsoup4`, `pillow`,
  `jinja2`, `requests`).
- Shell scripts (if any): `bash`, `set -euo pipefail`, no GNU-only flags
  unless guarded.
- Comments should explain **why**, not narrate the code.

## Methodology changes

This is a finance tool. Changes that affect ratings, scoring, or
recommendations need to be defensible:

- Cite the source (book, paper, framework author) where possible.
- Explain why the new rule is more accurate / less prone to false positives.
- Update the relevant `references/*.md` file alongside the `SKILL.md`.

## Licensing

By submitting a PR you agree your contribution is licensed under the
[MIT License](./LICENSE) used by the rest of the repo.
