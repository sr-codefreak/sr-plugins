# Stock Universe — Your Portfolio Tickers

> This file is a **user-customised whitelist** of NSE tickers you want to run FA on.
> Copy this template, fill in your own holdings, and save it as `stock-universe.md`
> alongside this file. The orchestrator will still run FA for any NSE ticker not
> listed here (it just won't have your own metadata to draw from).
>
> **Heads-up:** the example tickers below are for illustration only. They are
> **not stock recommendations**. Replace them with your own list before using.

## Tradeable NSE Securities (FA Applicable)

| Ticker         | Company Name                        | Sector                      | Notes      | Website URL                    |
| -------------- | ----------------------------------- | --------------------------- | ---------- | ------------------------------ |
| NSE:POLYCAB    | Polycab India Ltd                   | Wires & Cables              |            | https://www.polycab.com        |
| NSE:ASIANPAINT | Asian Paints Ltd                    | Paints & Coatings           |            | https://www.asianpaints.com    |
| NSE:HEROMOTOCO | Hero MotoCorp Ltd                   | Two-Wheelers                |            | https://www.heromotocorp.com   |

## Special Cases — FA Not Applicable

| Ticker       | Type                        | Reason                                                                                               |
| ------------ | --------------------------- | ---------------------------------------------------------------------------------------------------- |
| NSE:GOLDBEES | Gold ETF (Nippon Gold BeES) | ETF tracks gold price; no operating management or competitive industry to analyze. Skip FA entirely. |
| CASH         | Cash holding                | Not a security. Skip.                                                                                |

## Notes for Analysis

- **Small-caps**: Data availability may be limited. Rely more on Annual Reports and less on third-party databases. Flag if key data is unavailable.
- **Recent IPOs**: Limited historical data — note the shorter track record in reports; do not penalize heavily for missing 5-year trends.
- **NBFCs**: Industry analysis should include RBI regulatory environment as a key government protection / risk factor.

## Columns

- **Ticker** — NSE symbol with `NSE:` prefix
- **Company Name** — Full registered name
- **Sector** — Free-text industry classification
- **Notes** — Anything you want the orchestrator to keep in mind (e.g. "Recent IPO", "Small-cap")
- **Website URL** — Used by `scripts/generate_fa_pdf.py` to scrape headshots, products, and the company logo for the PDF report. Leave empty to skip image scraping.
