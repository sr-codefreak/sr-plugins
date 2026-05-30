---
name: fa-orchestrator
description: This skill should be used when the user asks to "run fundamental analysis", "analyze a stock", "FA on NSE:", "assess company quality", "check if a stock is worth investing in", "evaluate management", "analyze industry for", or when the /fa command is invoked with a stock ticker. This is the master orchestrator for the full Phase 1 fundamental analysis workflow.
version: 1.0.0
author: S R
license: MIT
metadata:
  hermes:
    tags: [investing, fundamental-analysis, nse, equities, research]
    related_skills: [fa-management, fa-industry, fa-balancesheet, fa-profitloss, fa-cashflow, fa-returnratios, fa-valuation]
---

# FA Orchestrator — Master Skill

The fundamental analysis orchestrator drives the complete Phase 1 analysis for an NSE-listed stock. It coordinates data gathering agents, delegates to domain sub-master skills, and synthesizes a structured RAG (Red/Amber/Green) investment report.

## Scope Boundary

The full FA covers:
- Management Analysis (Integrity + Skillset) — qualitative
- Industry Analysis (Lifecycle Stage + Porter's 5 Forces) — qualitative
- Balance Sheet Analysis (10-point financial health checklist) — quantitative, from live data
- Profit & Loss Analysis (10-point income statement checklist) — quantitative, from live data
- Cash Flow Analysis (7-point cash conversion & FCF checklist) — quantitative, from live data
- Return Ratios Analysis (7-point ROCE/ROE/ROA & DuPont checklist) — quantitative, from live data
- Valuation Analysis (7-point P/E, P/CF, PEG, P/S, P/B, EV/EBITDA, DCF checklist) — quantitative, from live data

## Analysis Architecture

```
fa-orchestrator (this skill)
├── fa-management sub-master
│   ├── fa-mgmt-integrity (10 criteria)
│   └── fa-mgmt-skillset (4 criteria)
├── fa-industry sub-master
│   ├── fa-industry-stage
│   └── fa-industry-forces (7 criteria)
├── fa-balancesheet (10 criteria)
├── fa-profitloss (10 criteria)
├── fa-cashflow (7 criteria)
├── fa-returnratios (7 criteria)
└── fa-valuation (7 criteria)
```

Each sub-master and leaf skill is loaded progressively — invoke them by name when reaching that analysis phase.

## Phase 1: Data Gathering

Before any analysis, launch all 9 agents **in parallel** using the Agent tool:

### Agent 1: fa-mgmt-remuneration-agent
Prompt template:
```
Analyze management remuneration and related party transactions for [Company Name] ([TICKER]).
Return structured findings: remuneration as % of PAT (last 3 years), complete RPT list with amounts, any anomalies found.
```

### Agent 2: fa-mgmt-news-agent
Prompt template:
```
Research news-based governance signals for [Company Name] ([TICKER]).
Cover: CFO/auditor changes (last 5 years), promoter pledging trend, management media appearances, any regulatory notices.
```

### Agent 3: fa-mgmt-promoter-agent
Prompt template:
```
Research promoter background and adverse records for [Company Name] ([TICKER]).
Cover: Promoter names, qualifications, experience, SEBI/legal records, Sujata Dalal/Moneylife watchlist check.
```

### Agent 4: fa-industry-research-agent
Prompt template:
```
Research industry landscape for [Company Name] ([TICKER]) in the [Sector] sector.
Cover: IBEF market data (size, CAGR), lifecycle stage signals, top 5 competitors, Porter's 5 Forces inputs (supplier/buyer power, substitutes, entry barriers, govt protection).
```

### Agent 5: fa-balancesheet-agent
Prompt template:
```
Fetch complete balance sheet data for [Company Name] ([TICKER]) from Screener.in.
Cover: 5-year balance sheet (equity, liabilities, assets), borrowing details, key ratios (D/E, current ratio), contingent liabilities, promoter pledging, goodwill & intangibles breakdown.
Use consolidated financials. Primary source: screener.in/company/[TICKER]/consolidated/
```

### Agent 6: fa-profitloss-agent
Prompt template:
```
Fetch complete profit & loss statement data for [Company Name] ([TICKER]) from Screener.in.
Cover: 5-10 year P&L (revenue, expenses breakdown, EBITDA, EBIT, PBT, PAT), margins (EBITDA%, PAT%), expense ratios, growth rates, EPS, dividend payout, exceptional items, consolidated vs standalone comparison, segment-wise revenue from annual report.
Use consolidated financials. Primary source: screener.in/company/[TICKER]/consolidated/
Also check standalone at screener.in/company/[TICKER]/ for comparison.
```

### Agent 7: fa-cashflow-agent
Prompt template:
```
Fetch complete cash flow statement data for [Company Name] ([TICKER]) from Screener.in.
Cover: 5-10 year cash flow statement (CFO, CFI, CFF), net profit for comparison, capex, D&A, working capital changes, free cash flow computation.
Use consolidated financials. Primary source: screener.in/company/[TICKER]/consolidated/
Cross-check FCF with Tijori Finance.
```

### Agent 8: fa-returnratios-agent
Prompt template:
```
Fetch complete return ratio data for [Company Name] ([TICKER]) from Screener.in.
Cover: ROCE, ROE, ROA trends (5-10 years), DuPont decomposition (NPM, Asset Turnover, Equity Multiplier), capital employed, total assets, equity, EBIT, PAT, revenue, D/E ratio, sector peer comparison (ROCE/ROE for top 3-5 peers).
Use consolidated financials. Primary source: screener.in/company/[TICKER]/consolidated/
```

### Agent 9: fa-valuation-agent
Prompt template:
```
Fetch complete valuation data for [Company Name] ([TICKER]) from Screener.in and Tijori Finance.
Cover: CMP, Market Cap, P/E (trailing), P/B, EPS trend (5-10 years), EPS CAGR (1yr/3yr/5yr), Operating Cash Flow (for P/CF), Revenue (for P/S), Book Value per Share, Total Debt & Cash (for EV), EBITDA (for EV/EBITDA), FCF trend (for DCF), sector peer comparison (P/E, P/B, P/S for 3-5 peers), historical P/E range, India 10yr Govt Bond yield.
Use consolidated financials. Primary source: screener.in/company/[TICKER]/consolidated/
Cross-check EPS growth with Tijori Finance.
```

Wait for all 9 agents to return before proceeding to Phase 2.

## Phase 2: Management Analysis

Invoke the `fa-management` sub-master skill. Pass it:
- Company name and ticker
- All findings from agents 1, 2, and 3

The sub-master will delegate to:
- `fa-mgmt-integrity` (10-point integrity checklist)
- `fa-mgmt-skillset` (4-point skillset checklist)

Collect 14 structured verdicts (criterion, evidence, RAG status).

## Phase 3: Industry Analysis

Invoke the `fa-industry` sub-master skill. Pass it:
- Company name, ticker, and sector
- All findings from agent 4

The sub-master will delegate to:
- `fa-industry-stage` (classify Pioneering / Growth / Maturity / Decline)
- `fa-industry-forces` (7-point Porter's + India forces)

Collect 8 structured verdicts (1 stage + 7 forces).

## Phase 4: Balance Sheet Analysis

Invoke the `fa-balancesheet` leaf skill directly. Pass it:
- Company name and ticker
- All findings from agent 5 (fa-balancesheet-agent)

The skill will evaluate 10 criteria:
1. Debt-to-Equity Ratio
2. Current Ratio (Liquidity)
3. Borrowing Trend
4. Equity Growth
5. Goodwill & Intangible Assets Quality
6. Contingent Liabilities
7. Capital Work-in-Progress
8. Cash Position
9. Trade Receivables & Inventory Health
10. Balance Sheet Red Flags Scan

Collect 10 structured verdicts (criterion, key numbers, RAG status).

## Phase 5: Profit & Loss Analysis

Invoke the `fa-profitloss` leaf skill directly. Pass it:
- Company name and ticker
- All findings from agent 6 (fa-profitloss-agent)

The skill will evaluate 10 criteria:
1. Revenue Growth Consistency
2. EBITDA Margin Stability & Level
3. PAT Margin & Net Profitability
4. Expense Ratio Discipline
5. Interest Coverage & Finance Cost Burden
6. Exceptional Items & One-Time Charges
7. Revenue Quality — Other Income Dependency
8. Tax Rate Consistency
9. Consolidated vs Standalone Gap
10. EPS Growth & Earnings Quality

Collect 10 structured verdicts (criterion, key numbers, RAG status).

## Phase 6: Cash Flow Analysis

Invoke the `fa-cashflow` leaf skill directly. Pass it:
- Company name and ticker
- All findings from agent 7 (fa-cashflow-agent)

The skill will evaluate 7 criteria:
1. CFO / Net Profit Ratio (Cash Conversion Quality)
2. Free Cash Flow (FCF) Trend
3. CFO Dominance (Operating vs Investing vs Financing)
4. Capex vs Depreciation (Maintenance vs Growth Capex)
5. Working Capital Impact on Cash Flow
6. Dividend / Buyback from FCF (Shareholder Returns)
7. Cash Flow Trend & Consistency

Collect 7 structured verdicts (criterion, key numbers, RAG status).

## Phase 7: Return Ratios Analysis

Invoke the `fa-returnratios` leaf skill directly. Pass it:
- Company name and ticker
- All findings from agent 8 (fa-returnratios-agent)

The skill will evaluate 7 criteria:
1. ROCE (Return on Capital Employed)
2. ROE (Return on Equity)
3. ROA (Return on Assets)
4. DuPont Decomposition of ROE
5. ROCE vs ROE Gap Analysis
6. Return Ratio Trend (5-Year Trajectory)
7. Sector-Relative Returns

Collect 7 structured verdicts (criterion, key numbers, RAG status).

## Phase 8: Valuation Analysis

Invoke the `fa-valuation` leaf skill directly. Pass it:
- Company name and ticker
- All findings from agent 9 (fa-valuation-agent)
- Key context from earlier phases: sector, cyclical/non-cyclical classification, ROE (for P/B cross-check), earnings quality verdict from cash flow phase

The skill will evaluate 7 criteria:
1. P/E Ratio Assessment
2. Price-to-Cash Flow (P/CF)
3. PEG Ratio
4. Price-to-Sales (P/S)
5. Price-to-Book (P/B)
6. EV/EBITDA
7. Intrinsic Value / DCF Assessment

Collect 7 structured verdicts (criterion, key numbers, RAG status).

**Important:** Valuation carries only 20-30% weightage (Money Purse P12). Quality analysis (Phases 2-7) carries 70-80%. A cheap stock in a bad business is still a bad investment.

## Phase 9: Multi-bagger Screening

After all analysis phases are complete, invoke the `fa-multibagger-screen` synthesis skill. Pass it:
- All verdicts from Phases 2-8 (management, industry, balance sheet, P&L, cash flow, return ratios, valuation)
- Market cap, promoter holding, free float data from agents

The skill will evaluate 10 criteria: durable competitive edge, management quality, promoter holding value, sustainable earnings growth, margins + asset turnover moat, prudent capital allocation, valuation attractiveness, variant perception potential, low free float catalyst, growth catalysts.

Collect 10 structured verdicts and a multi-bagger potential classification (Strong / Moderate / Low / Not a Candidate).

## Phase 10: Synthesis

Compile the final report using `references/output-template.md` as the scaffold (includes Part C: Balance Sheet Analysis, Part D: Profit & Loss Analysis, Part E: Cash Flow Analysis, Part F: Return Ratios Analysis, Part G: Valuation Analysis, and Part H: Multi-bagger Screening).

### RAG Assignment Rules

| Verdict | Meaning | When to assign |
|---------|---------|----------------|
| 🟢 Green | Passes | Criterion clearly met, no concerns found |
| 🟡 Amber | Caution | Minor or unconfirmed concern, needs monitoring |
| 🔴 Red | Flag | Clear red flag — criterion fails |
| ⬜ N/A | Not applicable | Data unavailable or criterion doesn't apply |

### Synthesis Rules
- A single 🔴 Red in Management Integrity is serious — highlight it prominently
- Multiple 🟡 Ambers (3+) in management = overall management concern
- Industry Decline stage + weak Porter's forces = structural headwind, flag it
- Balance Sheet 🔴 (D/E > 3 or Current Ratio < 0.5) is a hard stop — flag prominently
- Strong management + strong industry but weak balance sheet = "Monitor" (not "Invest")
- P&L Red (PAT negative 3+ years OR revenue declining 3+ years) = business fundamentally struggling — flag prominently
- Strong P&L margins but weak cash flow = potential earnings manipulation — flag as serious risk
- P&L revenue growing but EBITDA margin declining = growth without profitability — flag concern
- Cash Flow Red (CFO/Net Profit < 30%) = earnings quality concern — flag prominently
- Positive profit but consistently negative FCF = potential earnings manipulation — flag as serious risk
- Strong balance sheet + weak cash flow = "Monitor" (balance sheet may deteriorate if cash flow doesn't improve)
- Return Ratios Red (ROCE < 8% avg) = company destroying capital — flag prominently
- High ROE but driven by leverage (DuPont EM > 3.5) = fragile returns — flag as leverage risk
- Strong P&L margins but low ROCE = capital-inefficient business model — flag concern
- Low margins but high return ratios = asset-light/high-turnover model — this is POSITIVE (Dixon Technologies pattern)
- All three return ratios declining 4+ years = structural deterioration — flag prominently
- ROCE consistently > cost of debt = value creation confirmed — positive signal
- Valuation 🟢 but quality analysis (management/industry/financials) 🔴 = DO NOT invest — quality > valuation (Money Purse P12: 70-80% qualitative, 20-30% valuation)
- Valuation 🔴 but quality analysis all 🟢 = "Monitor for better entry" — good business, just expensive
- Cyclical company at low P/E = potential trap — flag prominently (P/E appears cheap at peak earnings)
- P/E 🟢 but P/CF 🔴 (divergence) = possible earnings manipulation — flag as serious risk
- PEG < 1 with consistent EPS growth = attractive growth at reasonable price — strong positive
- CMP significantly below DCF intrinsic value with strong fundamentals = high-conviction opportunity
- Combine into an Overall Verdict section: "Invest / Monitor / Avoid" with key reasons

## Output Format

See `references/output-template.md` for the exact report structure. Always end with:
- Overall Verdict (Invest / Monitor / Avoid)
- Top 3 Risks identified
- Top 3 Positives identified

## Phase 11: Save Output

After synthesis, save the report in **both Markdown and PDF** to a company-specific folder.

### Directory convention

```
company-analysis/{company-slug}/fa-phase1-{YYYY-MM-DD}.md
company-analysis/{company-slug}/fa-phase1-{YYYY-MM-DD}.pdf
```

- `{company-slug}` = lowercase ticker without the `NSE:` prefix (e.g. `NSE:POLYCAB` → `polycab`)
- `{YYYY-MM-DD}` = today's date (use the `currentDate` context variable)
- Create the directory if it does not exist

### Step-by-step

1. **Write the Markdown file** using the Write tool to `company-analysis/{company-slug}/fa-phase1-{YYYY-MM-DD}.md`

2. **Generate the PDF** by running (from the workspace that contains `company-analysis/`):
   ```bash
   python3 ~/.hermes/skills/investing/scripts/generate_fa_pdf_v2.py \
     "company-analysis/{company-slug}/fa-phase1-{YYYY-MM-DD}.md" \
     "company-analysis/{company-slug}/fa-phase1-{YYYY-MM-DD}.pdf"
   ```
   Use `generate_fa_pdf.py` instead for a shorter PDF (management + industry only). Scripts scrape website images when URLs are available, then render via Chrome headless.

3. **Confirm to the user** with paths to both files.

### Error handling

- If `beautifulsoup4` or `Pillow` or `Jinja2` is missing: `pip3 install beautifulsoup4 pillow jinja2 --break-system-packages`
- If Chrome is not found: set `CHROME_PATH` to your Chrome/Chromium binary (see investing `README.md`)
- If PDF generation fails: save only the `.md` file, inform the user. The script exits with a non-zero code on failure.

## References

- **`references/stock-universe.md`** — Template whitelist (replace with your own tickers)
- **`references/output-template.md`** — The exact Markdown report template to fill in
