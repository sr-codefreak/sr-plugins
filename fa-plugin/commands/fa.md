---
description: Run Fundamental Analysis on an NSE stock — covers Management Integrity (10 points), Management Skillset (4 points), Industry Stage, Porter's 5 Forces + India-specific government protection, Balance Sheet Health (10 points), P&L Health (10 points), Cash Flow Health (7 points), Return Ratios (7 points — ROCE, ROE, ROA, DuPont), and Valuation (7 points — P/E, P/CF, PEG, P/S, P/B, EV/EBITDA, DCF). Covers qualitative, financial statement, return ratio, and valuation analysis.
argument-hint: <NSE:TICKER>
allowed-tools: [WebSearch, WebFetch, Agent, TodoWrite, Write, Bash]
---

# /fa — Fundamental Analysis

## Argument Parsing

Accept `$ARGUMENTS` in any of these formats and normalize to `NSE:TICKER`:
- `NSE:POLYCAB` → use as-is
- `POLYCAB` → prefix with `NSE:`
- `polycab` → uppercase and prefix with `NSE:`

If no argument is provided, display:
```
Usage: /fa <NSE:TICKER>
Example: /fa NSE:POLYCAB

Available tickers in your portfolio:
  NSE:POLYCAB   Polycab India Ltd
  NSE:FIEMIND   Fiem Industries Ltd
  NSE:ASIANPAINT Asian Paints Ltd
  ... (see the fa-orchestrator skill's references/stock-universe.md for the full list)
```
Then stop.

## Stock Universe Validation

Load the `fa-orchestrator` skill and read its `references/stock-universe.md` to look up the ticker.

- If the ticker is marked `N/A` (GOLDBEES, CASH), respond: "NSE:GOLDBEES is a Gold ETF — management and industry analysis is not applicable. Fundamental analysis is designed for operating businesses."
- If the ticker is unknown (not in the list), warn the user but proceed: "NSE:XXXX is not in your tracked portfolio, but proceeding with analysis."
- Extract the company display name and sector for use throughout the analysis.

## Analysis Scope

This command runs the complete Fundamental Analysis:
- **Management Analysis**: Integrity (10 criteria) + Skillset (4 criteria)
- **Industry Analysis**: Lifecycle Stage + Porter's 5 Forces (7 criteria)
- **Balance Sheet Analysis**: 10-point financial health checklist (solvency, liquidity, asset quality)
- **P&L Analysis**: 10-point income statement checklist (revenue growth, EBITDA margin, expense discipline, EPS)
- **Cash Flow Analysis**: 7-point cash conversion & FCF checklist (CFO quality, FCF trend, cash dominance)
- **Return Ratios Analysis**: 7-point ROCE/ROE/ROA checklist (DuPont decomposition, gap analysis, sector peers)
- **Valuation Analysis**: 7-point valuation checklist (P/E, P/CF, PEG, P/S, P/B, EV/EBITDA, DCF intrinsic value)
- **Multi-bagger Screening**: 10-point synthesis checklist (moat durability, earnings sustainability, variant perception, free float, catalysts)

Display at the start:
```
═══════════════════════════════════════════════════
  FUNDAMENTAL ANALYSIS: [Company Name] ([TICKER])
  Date: [today's date]
  Scope: Full FA (Quality + Valuation)
═══════════════════════════════════════════════════
```

## Execution Workflow

Follow the fa-orchestrator skill for the full workflow:

**Phase 1 — Data Gathering (parallel)**
Launch all 9 research agents simultaneously:
1. `fa-mgmt-remuneration-agent` — director pay %, related party transactions
2. `fa-mgmt-news-agent` — CFO/auditor changes, pledging news, media appearances
3. `fa-mgmt-promoter-agent` — promoter background, SEBI records, Sujata Dalal check
4. `fa-industry-research-agent` — IBEF industry data, competitive landscape, Porter's inputs
5. `fa-balancesheet-agent` — balance sheet data from Screener.in, ratios, borrowings, contingent liabilities
6. `fa-profitloss-agent` — P&L data from Screener.in, revenue/EBITDA/PAT margins, expense ratios, EPS, segments
7. `fa-cashflow-agent` — cash flow statement data from Screener.in, FCF, CFO/CFI/CFF trends, net profit comparison
8. `fa-returnratios-agent` — ROCE/ROE/ROA trends, DuPont components, capital employed, sector peer comparison
9. `fa-valuation-agent` — P/E, P/CF, PEG, P/S, P/B, EV/EBITDA, DCF inputs, EPS CAGR, sector peer valuations, historical P/E range

**Phase 2 — Management Analysis**
Using agent findings, run management analysis guided by fa-management skill → fa-mgmt-integrity (10 points) + fa-mgmt-skillset (4 points).

**Phase 3 — Industry Analysis**
Using agent findings, run industry analysis guided by fa-industry skill → fa-industry-stage + fa-industry-forces (7 points).

**Phase 4 — Balance Sheet Analysis**
Using agent findings, run balance sheet analysis guided by fa-balancesheet skill (10 points: solvency, liquidity, asset quality).

**Phase 5 — P&L Analysis**
Using agent findings, run P&L analysis guided by fa-profitloss skill (10 points: revenue growth, EBITDA margin, PAT margin, expense discipline, interest coverage, exceptional items, revenue quality, tax rate, consol vs standalone, EPS growth).

**Phase 6 — Cash Flow Analysis**
Using agent findings, run cash flow analysis guided by fa-cashflow skill (7 points: CFO/NP ratio, FCF trend, CFO dominance, capex vs D&A, working capital impact, shareholder returns, consistency).

**Phase 7 — Return Ratios Analysis**
Using agent findings, run return ratios analysis guided by fa-returnratios skill (7 points: ROCE, ROE, ROA, DuPont decomposition, ROCE vs ROE gap, trend, sector-relative).

**Phase 8 — Valuation Analysis**
Using agent findings + context from earlier phases (sector, cyclicality, ROE, earnings quality), run valuation analysis guided by fa-valuation skill (7 points: P/E, P/CF, PEG, P/S, P/B, EV/EBITDA, DCF intrinsic value). Remember: valuation = 20-30% weightage only.

**Phase 9 — Multi-bagger Screening**
Using all preceding phase outputs, run multi-bagger screening guided by fa-multibagger-screen skill (10 points: moat durability, management quality, promoter holding value, earnings sustainability, margins + asset turnover, capital allocation, valuation, variant perception, free float, catalysts).

**Phase 10 — Synthesis**
Compile the final report using the template in the `fa-orchestrator` skill's `references/output-template.md`.

**Phase 11 — Save Output**
Save the report to `company-analysis/{ticker-slug}/fa-{YYYY-MM-DD}.{md,pdf}` following the instructions in the `fa-orchestrator` SKILL.md Phase 11 section.
- `{ticker-slug}` = lowercase ticker without `NSE:` prefix (e.g. `NSE:POLYCAB` → `polycab`)
- Write the Markdown file first, then generate the PDF with `pandoc --pdf-engine=weasyprint`
- Confirm to the user with the saved file paths

## Progress Tracking

Use TodoWrite to track progress:
- [ ] Phase 1: Data gathering (9 agents)
- [ ] Phase 2: Management integrity (10 criteria)
- [ ] Phase 3: Management skillset (4 criteria)
- [ ] Phase 4: Industry stage
- [ ] Phase 5: Industry forces (7 criteria)
- [ ] Phase 6: Balance sheet analysis (10 criteria)
- [ ] Phase 7: P&L analysis (10 criteria)
- [ ] Phase 8: Cash flow analysis (7 criteria)
- [ ] Phase 9: Return ratios analysis (7 criteria)
- [ ] Phase 10: Valuation analysis (7 criteria)
- [ ] Phase 11: Synthesis and report
- [ ] Phase 12: Save MD + PDF to company-analysis/
