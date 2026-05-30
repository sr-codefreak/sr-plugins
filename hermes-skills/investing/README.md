# Investing — Fundamental analysis (Hermes)

Hermes skill pack for Phase 1 fundamental analysis on NSE-listed stocks.

## Skills

| Skill | Role |
| ----- | ---- |
| `fa-orchestrator` | Master workflow — coordinates agents and synthesis |
| `fa-management`, `fa-mgmt-integrity`, `fa-mgmt-skillset` | Management quality |
| `fa-industry`, `fa-industry-stage`, `fa-industry-forces` | Industry structure |
| `fa-balancesheet`, `fa-profitloss`, `fa-cashflow`, `fa-returnratios` | Financial statements |
| `fa-valuation`, `fa-multibagger-screen` | Valuation and screening |

## Trigger phrases

- "run fundamental analysis on NSE:EXAMPLE1"
- "FA on &lt;ticker&gt;"
- "assess management quality of …"

## PDF generation

Dependencies: Python 3.10+, `beautifulsoup4`, `pillow`, `jinja2`, `requests`, Chrome/Chromium.

```bash
pip3 install beautifulsoup4 pillow jinja2 requests
export CHROME_PATH="/path/to/chrome"   # if auto-detect fails
```

```bash
python3 ~/.hermes/skills/investing/scripts/generate_fa_pdf_v2.py report.md report.pdf
```

## Customisation

Replace `fa-orchestrator/references/stock-universe.md` with your own ticker list, or set `STOCK_UNIVERSE_PATH` to an external file.

## Disclaimer

Not investment advice. Verify all outputs against audited filings. See repo [DISCLAIMER.md](../../DISCLAIMER.md).
