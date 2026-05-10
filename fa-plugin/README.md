# fa-plugin

Phase 1 Fundamental Analysis for NSE-listed stocks, packaged as a
[Claude Code](https://docs.claude.com/en/docs/claude-code/overview) /
Cowork plugin.

> [!CAUTION]
> **Not investment advice. Output may be wrong.**
> This plugin runs an LLM over public financial data and produces a research
> report. It does **not** give investment, legal, or tax advice. The author
> is not a SEBI-registered Investment Adviser. Verify everything against the
> company's audited filings before acting on any output. Read the full
> [DISCLAIMER](../DISCLAIMER.md) before use.

## What it does

Runs a full qualitative + quantitative Phase 1 analysis on an NSE ticker:

- **Management** — Integrity (10 criteria) + Skillset (4 criteria)
- **Industry** — Lifecycle stage + Porter's 5 Forces with India-specific government-protection lens (8 criteria)
- **Balance Sheet** — 10-point financial-health checklist
- **P&L** — 10-point income-statement checklist
- **Cash Flow** — 7-point cash-conversion & FCF checklist
- **Return Ratios** — 7-point ROCE / ROE / ROA checklist with DuPont decomposition

Output is a RAG-rated (Red / Amber / Green) report saved to
`company-analysis/{ticker-slug}/fa-phase1-{YYYY-MM-DD}.md` and rendered as
a 6-page PDF.

Phase 2 (P/E, DCF, PEG, valuation verdict) is out of scope for this plugin.

## How to invoke

In Cowork or Claude Code, any of these will trigger the orchestrator skill:

- `run fundamental analysis on POLYCAB`
- `analyze NSE:FIEMIND`
- `assess management quality of Asian Paints`
- `/fa NSE:POLYCAB` (legacy slash command, also supported)

The skill normalizes the ticker (`polycab` → `NSE:POLYCAB`) and validates it
against `skills/fa-orchestrator/references/stock-universe.md` (which you
customise — the version in this repo is a stub example, not stock advice).

## Install

### Claude Code

```bash
/plugin install https://github.com/sr-codefreak/sr-plugins/tree/main/fa-plugin
```

Or install from the **sr-plugins** marketplace (same repo, [`marketplace.json`](../.claude-plugin/marketplace.json)):

```bash
/plugin marketplace add sr-codefreak/sr-plugins
/plugin install fa-plugin@sr-plugins
```

Or clone and install locally:

```bash
git clone https://github.com/sr-codefreak/sr-plugins.git
/plugin install ./sr-plugins/fa-plugin
```

### Cowork

1. **Customize** in the left sidebar.
2. **Add plugin** → paste the plugin's GitHub URL.
3. Restart the session if prompted.

## Dependencies (PDF generation only)

The orchestrator's "save output" step shells out to
`scripts/generate_fa_pdf.py`, which needs:

- **Python 3.10+** with these packages:
  ```bash
  pip3 install beautifulsoup4 pillow jinja2 requests
  ```
- **Google Chrome or Chromium** for headless PDF rendering. The script
  auto-detects common install locations on macOS / Linux / Windows. If yours
  isn't found, point it at the binary explicitly:
  ```bash
  export CHROME_PATH="/path/to/your/chrome-binary"
  ```

If a dependency is missing, the orchestrator falls back to saving only the
Markdown report and tells you what's missing.

## Configuration

| Env var               | Purpose                                                                  |
| --------------------- | ------------------------------------------------------------------------ |
| `CHROME_PATH`         | Override Chrome / Chromium binary location for PDF rendering.            |
| `STOCK_UNIVERSE_PATH` | Override the path to your customised `stock-universe.md` whitelist.      |

## Customising the stock universe

`skills/fa-orchestrator/references/stock-universe.md` ships as a generic
**template with example tickers** — these are not recommendations, just
illustrations of the file format.

Replace it with your own holdings, or keep your real list outside the repo
and point `STOCK_UNIVERSE_PATH` at it. The orchestrator will still run FA on
any NSE ticker that isn't in the list (it just won't have your own metadata
to lean on).

## Layout

```
fa-plugin/
├── .claude-plugin/plugin.json     # manifest
├── commands/fa.md                 # /fa slash command
├── skills/                        # 11 skills (orchestrator + sub-masters + leaves)
│   ├── fa-orchestrator/           # master entry point
│   ├── fa-management/, fa-mgmt-integrity/, fa-mgmt-skillset/
│   ├── fa-industry/, fa-industry-stage/, fa-industry-forces/
│   └── fa-balancesheet/, fa-profitloss/, fa-cashflow/, fa-returnratios/
├── agents/                        # parallel research subagents
└── scripts/
    ├── generate_fa_pdf.py         # Markdown → 6-page PDF renderer
    └── templates/fa_report.html
```

## Methodology credits

The criteria draw on publicly available frameworks. None of these authors
endorse this plugin or bear any responsibility for it.

- Michael E. Porter — *Competitive Strategy* (Five Forces).
- Vijay Malik — Stock investing & behavioural-analysis frameworks
  (https://www.drvijaymalik.com).
- Standard accounting / valuation literature (DuPont decomposition, FCF, ROCE).

## License

[MIT](../LICENSE) — © 2026 Sai Rajesh. The software is provided **AS IS,
without warranty of any kind**. See LICENSE for the full text.

## Full disclaimer

See [`DISCLAIMER.md`](../DISCLAIMER.md) at the root of the repository for
the full set of "this is not investment advice" caveats. Short version:

- Outputs are research aids, not recommendations.
- LLM output can be wrong; verify against audited filings.
- Past performance does not predict future returns.
- The author has no SEBI RIA registration and no fiduciary duty to you.
- Use at your own risk.
