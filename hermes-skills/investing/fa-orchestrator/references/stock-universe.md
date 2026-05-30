# Stock Universe — Template

> User-customised whitelist of NSE tickers for fundamental analysis.
> Copy this template, fill in your own tickers, and save as `stock-universe.md`.
> The orchestrator still runs FA for any NSE ticker not listed here.
>
> **The example rows below are placeholders only — not recommendations.**

## Tradeable NSE Securities (FA Applicable)

| Ticker       | Company Name      | Sector          | Notes              | Website URL        |
| ------------ | ----------------- | --------------- | ------------------ | ------------------ |
| NSE:EXAMPLE1 | Example Co Ltd    | Example Sector  | Template row only  | https://example.com |
| NSE:EXAMPLE2 | Another Example Ltd | Example Sector | Template row only |                    |

## Special Cases — FA Not Applicable

| Ticker       | Type        | Reason                                                                 |
| ------------ | ----------- | ---------------------------------------------------------------------- |
| NSE:GOLDBEES | Gold ETF    | ETF tracks gold; no operating management or industry to analyze. Skip. |
| CASH         | Cash holding | Not a security. Skip.                                                 |

## Notes for Analysis

- **Small-caps**: Data may be limited — prefer annual reports; flag missing data.
- **Recent IPOs**: Shorter history — note limited track record; do not over-penalize.
- **NBFCs**: Include RBI / regulatory context in industry analysis.

## Columns

- **Ticker** — NSE symbol with `NSE:` prefix
- **Company Name** — Registered name
- **Sector** — Industry classification
- **Notes** — Context for the orchestrator (e.g. "Recent IPO", "Small-cap")
- **Website URL** — Used by PDF scripts for logo/headshot scraping; leave empty to skip
