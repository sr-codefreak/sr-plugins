---
name: fa-cashflow
description: This skill should be used when evaluating the cash flow health of an NSE-listed company, checking "operating cash flow quality", "free cash flow", "FCF", "FCFF", "FCFE", "cash flow from operations", "CFO to net profit ratio", "capex coverage", "cash conversion", "profit to cash conversion", "cash flow dominance", "working capital cash impact", "Warren Buffett free cash flow", or when the fa-orchestrator has reached the cash flow analysis phase. Applies a 7-point checklist derived from Money Purse cash flow analysis framework to assign RAG verdicts.
version: 1.0.0
---

# FA Cash Flow Analysis — Leaf Skill

Analyze the cash flow statement of an NSE-listed company using a 7-point checklist. For each criterion: state the finding with actual numbers, cite the data source, and assign a RAG verdict.

## Input Required

Before starting, confirm availability of the cash flow data packet from:
- fa-cashflow-agent: CFO/CFI/CFF trends, net profit, capex, FCF, D&A, revenue, working capital changes

If agent data is missing, note "Data unavailable — unable to verify" for affected criteria rather than assuming clean.

## Mindset

> "The company you work for provides you with a salary slip. Does providing a salary slip alone suffice, or do they need to deposit money in your account? Obviously they need to deposit money." — Money Purse
>
> Similarly, a company showing profit in P&L must actually generate cash. If they don't, the profit is hollow. Warren Buffett says: focus on the cash flow statement more than the P&L — specifically Free Cash Flow.

## Why Cash Flow Analysis Matters

1. **Credit-based business risk** — Companies doing 70-80% business on credit face higher bad debt risk
2. **Profit manipulation detection** — Promoters can inflate P&L profits to boost share price; cash flow is harder to fake
3. **Tax on unreceived income** — Company pays tax on declared profit even if cash hasn't arrived
4. **True earnings quality** — At least 70-80% of net profit should convert to operating cash flow

## Important Caveats (apply before analysis)

1. **One bad FCF year is not conclusive** — Pending payments from previous years may clear next year (e.g., Tata Elxsi: negative FCF in 2013, then Rs.172 Cr FCF the next year). Look at multi-year trends.
2. **Banks, NBFCs & HFCs have different cash flow structure** — Advances are operating, Deposits are financing. Flag this and note that standard thresholds don't apply directly.
3. **Capex-heavy growth phase** — A company investing heavily for future growth will have lower/negative FCF temporarily. Check if capex is generating revenue growth in subsequent years.

## The 7-Point Cash Flow Checklist

Work through each criterion in order. For each criterion:
1. State the specific numbers found
2. Apply the threshold rules below
3. Assign RAG status
4. Note the source (Screener.in URL, AR page number, etc.)

---

### Criterion 1: CFO / Net Profit Ratio (Cash Conversion Quality)

**Data source:** fa-cashflow-agent (CFO trend + Net Profit trend)
**Calculation:** (Cash Flow from Operating Activities / Net Profit) x 100, averaged over last 3-5 years

**Thresholds:**
- Average CFO/Net Profit >= 80% -> Green (strong cash conversion)
- Average CFO/Net Profit 50-80% -> Amber (moderate — investigate working capital)
- Average CFO/Net Profit < 50% -> Red (poor cash conversion — profit quality suspect)
- CFO consistently negative while net profit is positive -> Red (major red flag — potential earnings manipulation)

**Sector adjustments:**
- Infrastructure/Real Estate/EPC: Cash conversion cycles are longer — 50-70% may be acceptable -> adjust thresholds by -20%
- IT/FMCG: Should have very high cash conversion (>90%) — apply stricter thresholds

**Report format:**
```
CFO / Net Profit ratio (last 5 years):
FY__: [X%] | FY__: [X%] | FY__: [X%] | FY__: [X%] | FY__: [X%]
Average (3yr): [X%]
Average (5yr): [X%]
```

---

### Criterion 2: Free Cash Flow (FCF) Trend

**Data source:** fa-cashflow-agent (FCFF computed section)
**Calculation:** FCFF = CFO - Capex

**Thresholds:**
- FCF positive in 4+ of last 5 years -> Green (consistent cash generator)
- FCF positive in 3 of last 5 years -> Amber (inconsistent — check capex cycle)
- FCF positive in <= 2 of last 5 years -> Red (chronic cash consumer)
- FCF growing over 5 years -> positive signal (note even if already Green)

**Additional checks:**
- If FCF is negative due to large capex in growth phase, check if revenue/profit grew in subsequent years — if yes, downgrade severity by one level
- Cumulative FCF over 5 years should be positive -> if negative, bump up one level

**Report format:**
```
FCFF (CFO - Capex) last 5 years:
FY__: Rs.[X] cr | FY__: Rs.[X] cr | FY__: Rs.[X] cr | FY__: Rs.[X] cr | FY__: Rs.[X] cr
Cumulative 5yr FCF: Rs.[X] cr
Positive years: [X] of 5
```

---

### Criterion 3: CFO Dominance (Operating vs Investing vs Financing)

**Data source:** fa-cashflow-agent (CFO/CFI/CFF trends)
**Check:** In a healthy company, CFO should be the primary source of cash. If CFI or CFF consistently exceeds CFO, the company is relying on asset sales or debt rather than operations.

**Thresholds:**
- CFO is the largest positive component in 4+ of last 5 years -> Green
- CFO is the largest positive component in 3 of last 5 years -> Amber
- CFI or CFF frequently larger than CFO -> Red (company funding operations through investments or debt)

**Patterns to flag:**
- CFO negative + CFF positive = funding operations through borrowing -> Red
- CFO negative + CFI positive = selling assets to fund operations -> Red
- CFO positive + CFI negative + CFF negative = ideal pattern (earn from operations, invest for growth, repay debt) -> Green

**Report format:**
```
Cash flow dominance (last 5 years):
FY__: CFO [X] | CFI [X] | CFF [X] — Dominant: [CFO/CFI/CFF]
FY__: CFO [X] | CFI [X] | CFF [X] — Dominant: [CFO/CFI/CFF]
...
Ideal pattern (CFO+, CFI-, CFF-) count: [X] of 5 years
```

---

### Criterion 4: Capex vs Depreciation (Maintenance vs Growth Capex)

**Data source:** fa-cashflow-agent (Capex trend + D&A trend)
**Check:** If capex roughly equals D&A, the company is only maintaining existing assets (maintenance capex). Growth capex = Capex - D&A. Healthy growing companies should have capex > D&A.

**Thresholds:**
- Capex > 1.5x D&A consistently -> Green (investing for growth beyond replacement)
- Capex ~ 1.0-1.5x D&A -> Amber (mostly maintenance, limited growth investment)
- Capex < D&A -> Red if declining company; Amber if asset-light model (IT, services)

**Sector adjustments:**
- Asset-light businesses (IT, consulting, fintech): Low capex/D&A ratio is normal -> do not penalize
- Capital-intensive (manufacturing, infra, power): Capex should be well above D&A during growth phase

**Report format:**
```
Capex vs D&A (last 5 years):
FY__: Capex Rs.[X] cr / D&A Rs.[X] cr = [X]x
FY__: Capex Rs.[X] cr / D&A Rs.[X] cr = [X]x
...
Average ratio: [X]x
Growth Capex (Capex - D&A) latest FY: Rs.[X] cr
```

---

### Criterion 5: Working Capital Impact on Cash Flow

**Data source:** fa-cashflow-agent (CFO breakdown — working capital changes)
**Check:** Large working capital increases (rising receivables, rising inventory) eat into cash flow. This is how companies can show profit but have no cash.

**Thresholds:**
- Working capital changes < 20% of CFO (positive or negative) -> Green (stable)
- Working capital changes 20-50% of CFO -> Amber (significant WC swings)
- Working capital changes > 50% of CFO or consistently negative -> Red (WC is consuming cash)
- Receivables growing faster than revenue for 3+ years -> bump up one level (collection issues)

**Report format:**
```
Working capital impact on CFO (latest FY):
  Change in Receivables: Rs.[X] cr
  Change in Inventory: Rs.[X] cr
  Change in Payables: Rs.[X] cr
  Net Working Capital Change: Rs.[X] cr
  As % of pre-WC CFO: [X%]
```

---

### Criterion 6: Dividend / Buyback from FCF (Shareholder Returns)

**Data source:** fa-cashflow-agent (CFF breakdown — dividends paid, buybacks)
**Check:** Are shareholder returns (dividends + buybacks) funded from free cash flow, or is the company borrowing to pay dividends?

**Thresholds:**
- Dividends + Buybacks < FCF -> Green (returns funded from free cash)
- Dividends + Buybacks > FCF but < CFO -> Amber (returns partially funded by reduced investment)
- Dividends + Buybacks > CFO or paid while FCF is negative -> Red (borrowing to pay shareholders)
- No dividends or buybacks -> N/A (note whether company is in growth phase or cash-strapped)

**Report format:**
```
Shareholder returns vs FCF (latest FY):
  Dividends paid: Rs.[X] cr
  Buybacks: Rs.[X] cr
  Total returns: Rs.[X] cr
  FCF: Rs.[X] cr
  Returns as % of FCF: [X%]
```

---

### Criterion 7: Cash Flow Trend & Consistency

**Data source:** fa-cashflow-agent (all trends)
**Check:** Meta-level check — is the overall cash flow picture improving, stable, or deteriorating?

**Items to verify:**
1. **CFO trend direction** — Is CFO growing, flat, or declining over 5 years?
2. **FCF trend direction** — Same check for free cash flow
3. **Cash balance trajectory** — Is the company accumulating or burning cash?
4. **Cumulative net cash flow** — Sum of (CFO + CFI + CFF) over 5 years: positive = cash generating, negative = cash consuming
5. **Consistency** — Erratic year-to-year swings are worse than steady growth or steady decline

**Overall criterion verdict:**
- CFO and FCF both growing + cumulative positive -> Green
- Mixed signals (CFO growing but FCF erratic) -> Amber
- CFO declining or FCF consistently negative -> Red

---

## Aggregating the Cash Flow Score

After completing all 7 criteria:

1. Count: Greens, Ambers, Reds (exclude N/A from count)
2. Apply override rules:
   - CFO/Net Profit < 30% average (3yr) for non-BFSI -> **Cash Flow = Red regardless**
   - Cumulative 5yr FCF deeply negative (> -50% of current market cap) -> **Cash Flow = Red regardless**
3. Otherwise:
   - 0 Red, <= 2 Amber -> Green (Cash Flow Strong)
   - 1 Red OR 3 Amber -> Amber (Cash Flow Adequate with Concerns)
   - 2+ Red OR 4+ Amber -> Red (Cash Flow Weak)

## Output Format

Return the analysis in this structure:

```
CASH FLOW ANALYSIS: [Company Name] ([Ticker])
Data as of: [FY end date]

| # | Criterion | Key Numbers | Status |
|---|-----------|-------------|--------|
| 1 | CFO/Net Profit Ratio | Avg: [X%] (3yr) | Green/Amber/Red |
| 2 | Free Cash Flow Trend | [X] of 5 yrs positive, Cumul: Rs.[X] cr | Green/Amber/Red |
| 3 | CFO Dominance | Ideal pattern: [X] of 5 yrs | Green/Amber/Red |
| 4 | Capex vs D&A | Avg ratio: [X]x | Green/Amber/Red |
| 5 | Working Capital Impact | WC as % of CFO: [X%] | Green/Amber/Red |
| 6 | Shareholder Returns vs FCF | Returns: [X%] of FCF | Green/Amber/Red/N/A |
| 7 | Cash Flow Trend & Consistency | [Summary] | Green/Amber/Red |

Cash Flow Score: [X/7 Green] (or X/6 if one N/A)
Overall Cash Flow Verdict: Green/Amber/Red

Key Cash Flow Concerns:
- [List any Red or Amber items with brief explanation]

Key Cash Flow Strengths:
- [List notable positives, e.g. consistent FCF generator, strong cash conversion]
```

## Data Sources (in priority order)

1. **Screener.in** — Primary source for 5-10 year cash flow data, P&L data
2. **Tijori Finance** — Cross-check for FCF numbers (may have slight mismatches)
3. **BSE India** — Annual Reports for detailed cash flow statement breakdown
4. **Moneycontrol** — Fallback for cash flow data if Screener.in unavailable
5. **Company Investor Relations page** — Annual Reports, investor presentations

Always use live data from these sources. Never use memorized or cached financial figures.
