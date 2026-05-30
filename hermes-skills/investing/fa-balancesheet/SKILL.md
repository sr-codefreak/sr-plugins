---
name: fa-balancesheet
description: This skill should be used when evaluating the balance sheet health of an NSE-listed company, checking "solvency", "liquidity", "debt to equity ratio", "current ratio", "asset quality", "goodwill percentage", "contingent liabilities", "borrowing trend", "capital work in progress", "cash position", "inventory days", "receivable days", "promoter pledging from balance sheet", or when the fa-orchestrator has reached the balance sheet analysis phase. Applies a 10-point checklist derived from Money Purse balance sheet analysis framework to assign RAG verdicts.
version: 1.0.0
---

# FA Balance Sheet Analysis — Leaf Skill

Analyze the balance sheet of an NSE-listed company using a 10-point checklist. For each criterion: state the finding with actual numbers, cite the data source, and assign a RAG verdict.

## Input Required

Before starting, confirm availability of the balance sheet data packet from:
- fa-balancesheet-agent: all balance sheet line items, ratios, borrowing details, contingent liabilities, promoter pledging

If agent data is missing, note "Data unavailable — unable to verify" for affected criteria rather than assuming clean.

## Mindset

> Adopt a detective's mindset — search for potential problems, not confirmation that the company is good. If you approach the analysis wanting to invest, confirmation bias will blind you to red flags.

## 3 Key Things Balance Sheet Reveals

1. **Solvency** — Can the company clear its loans?
2. **Liquidity** — Can it handle short-term expenses (e.g., during a downturn like COVID)?
3. **Shareholder Recovery** — If the company shuts down, will shareholders get anything back?

## Important Caveats (apply before analysis)

1. **Tangible asset book values may be understated** — Property bought years ago is at historical cost, not market value. PP&E value may be significantly higher than shown.
2. **Numbers are "As On Date"** — The balance sheet reflects the state on a specific date only. Loans may have been repaid or assets sold after that date.
3. **Banks & NBFCs have a different structure** — If the company is a Bank or NBFC, flag this and note that Deposits replace Borrowings, Advances replace Trade Receivables. Adjust analysis accordingly.

## The 10-Point Balance Sheet Checklist

Work through each criterion in order. For each criterion:
1. State the specific numbers found
2. Apply the threshold rules below
3. Assign RAG status
4. Note the source (Screener.in URL, AR page number, etc.)

---

### Criterion 1: Debt-to-Equity Ratio

**Data source:** fa-balancesheet-agent (Key Ratios section)
**Calculation:** (Long-term Borrowings + Short-term Borrowings) / Total Equity

**Thresholds:** (Money Purse P10: D/E < 1 healthy, > 2 avoid completely)
- D/E < 0.5 → 🟢 (conservatively financed)
- D/E 0.5–1.0 → 🟡 (moderate leverage, check if industry norm)
- D/E 1.0–2.0 → 🟡 (high leverage but may be acceptable for capital-intensive sectors like infra, power, real estate)
- D/E > 2.0 → 🔴 (heavily leveraged — "better to avoid completely" per Money Purse P10)
- D/E increasing over 3+ years → bump up one level (🟢→🟡, 🟡→🔴)
- D/E consistently increasing (e.g., 1→1.5→2→3) → 🔴 regardless — "exit as soon as possible" (Money Purse P10: Videocon, Jet Airways examples)

**Sector adjustments:**
- Banks/NBFCs: D/E norms are different (8-12x is normal) — lending is their business, so debt > equity is structural. Use Capital Adequacy Ratio instead if available. (Money Purse P10)
- Infrastructure/Power/Real Estate: D/E up to 2.0 is industry norm → adjust thresholds by +1.0. Note: Power sector has regular cash flows making debt servicing easier than Real Estate or Infra. (Money Purse P10)
- IT/FMCG: Should have very low D/E (<0.3) — apply stricter thresholds

**Supplementary check — Debt-to-Asset Ratio:** (Money Purse P10)
- Formula: Total Debt / Total Assets
- Shows what % of assets are financed by debt
- D/A < 0.5 → healthy (safe investment)
- D/A > 0.5 → elevated — more than half the assets are debt-financed
- D/A > 1.0 → even selling all assets won't cover liabilities → 🔴

**Report format:**
```
D/E Ratio: [X] (FY__)
Trend: FY__: [X] → FY__: [X] → FY__: [X] → FY__: [X] → FY__: [X]
Direction: [Improving / Stable / Deteriorating]
Debt-to-Asset Ratio: [X] (Total Debt Rs.[X] cr / Total Assets Rs.[X] cr)
```

---

### Criterion 2: Current Ratio & Quick Ratio (Liquidity)

**Data source:** fa-balancesheet-agent (Key Ratios section)

#### Current Ratio
**Calculation:** Total Current Assets / Total Current Liabilities

**Current assets include:** Cash, fixed deposits, mutual fund investments, quoted investments (shares of other companies), trade receivables, inventories, short-term loans & advances to subsidiaries/promoters. (Money Purse P11)

**Current liabilities include:** Overdraft (OD) facility, short-term loans (3-6 months), current maturities of long-term debt (EMIs due within 1 year), advances from customers, outstanding payables. (Money Purse P11)

**Thresholds:** (Money Purse P11: ideal range 1.33 to 3, banks use 1.33 as benchmark)
- Current Ratio 1.33–3.0 → 🟢 (healthy liquidity — ideal range per Money Purse P11)
- Current Ratio 1.0–1.33 → 🟡 (adequate but below bank benchmark)
- Current Ratio 0.75–1.0 → 🟡 (tight — acceptable ONLY for large companies that intentionally keep low cash to avoid return ratio drag; for small companies → 🔴)
- Current Ratio < 0.75 → 🔴 (liquidity risk — even for large companies, be careful per Money Purse P11)
- Current Ratio < 1.0 → 🔴 for small/mid-cap companies (current liabilities exceed current assets — company needs to raise additional debt or equity)

**Large company exception:** (Money Purse P11) Companies like Pidilite intentionally maintain current ratio 0.75-1.0 because keeping cash idle in books impacts return ratios → impacts stock performance. Don't worry about these if the company is established with long-term assets. But still be careful below 0.75.

**Current Ratio > 3.0 — Inefficiency Red Flag:** (Money Purse P11)
- Current ratio > 3 indicates **inefficient management** — 🟡 (or 🔴 if persistent)
- If CR > 3, check these 3 things:
  1. **Is cash remaining idle in the balance sheet for a long period?** → Idle cash won't generate returns
  2. **Are inventories increasing abnormally?** → Procuring inventory without matching sales
  3. **Are receivables increasing abnormally?** → Sales recorded but cash not collected (possible revenue manipulation)
- If any of these 3 cases is increasing, the company won't generate better returns because it impacts return ratios
- Money Purse P11: "Companies with CR > 3 need MORE caution than companies with CR < 3"
- Exception: Temporary cash build-up for planned acquisitions is acceptable if it normalizes

#### Quick Ratio
**Calculation:** (Total Current Assets - Inventories) / Total Current Liabilities

**Quick assets include:** Cash, fixed deposits, mutual fund investments, quoted investments, trade receivables (unless NPA), short-term loans & advances. (Money Purse P11)
**Why exclude inventory?** Inventory requires time to manufacture → sell → collect cash. Cannot be converted to cash within 1-2 months in most cases. (Money Purse P11)
**Exception:** Companies with negative cash conversion cycles (high demand, cash received before inventory purchased) — keep aside as exceptional case.

**Thresholds:** (Money Purse P11: ideal range 1 to 2.5)
- Quick Ratio 1.0–2.5 → 🟢 (healthy — assets convertible within 1-2 months cover current liabilities)
- Quick Ratio 0.75–1.0 → 🟡 (tight liquidity)
- Quick Ratio < 0.75 → 🔴 (cannot cover short-term obligations with liquid assets)
- Quick Ratio > 2.5 → 🟡 (management efficiency concern — same idle cash / receivables / inventory analysis as CR > 3)

#### Combined Liquidity Verdict
- Both CR and QR in ideal range (CR 1.33-3, QR 1-2.5) → 🟢
- One ratio outside ideal but not critical → 🟡
- Either CR < 0.75 OR QR < 0.75 → 🔴
- CR > 3 with increasing idle cash/inventory/receivables → 🔴

**Report format:**
```
Current Ratio: [X] (FY__)
Quick Ratio: [X] (FY__)
CR Trend (5yr): [X] → [X] → [X] → [X] → [X]
QR Trend (5yr): [X] → [X] → [X] → [X] → [X]
CR > 3 check (if applicable): Idle cash [Y/N], Inventory rising [Y/N], Receivables rising [Y/N]
Company size context: [Large-cap / Mid-cap / Small-cap]
```

---

### Criterion 3: Borrowing Trend (Debt Direction)

**Data source:** fa-balancesheet-agent (Borrowings Trend section)
**Check:** Is total borrowing increasing, stable, or decreasing over 5 years? Compare growth rate of borrowings vs growth rate of revenue/equity.

**Thresholds:**
- Borrowings declining or stable while revenue grows → 🟢
- Borrowings growing in line with revenue growth → 🟡
- Borrowings growing faster than revenue → 🔴
- Zero debt company → 🟢 (note as positive)

**Report format:**
```
Total Borrowings: Rs.[X] cr (FY__) vs Rs.[X] cr (FY__ 5yr ago)
Borrowing CAGR: [X%]
Revenue CAGR (same period): [X%] (fetch from Screener.in if not in agent data)
Verdict: Borrowings growing [faster/slower/in-line] than revenue
```

---

### Criterion 4: Equity Growth (Reserves & Surplus Trend)

**Data source:** fa-balancesheet-agent (Equity section)
**Check:** Is total equity (particularly Reserves & Surplus / Other Equity) growing steadily? This indicates the company is retaining and compounding profits.

**Thresholds:**
- Equity growing consistently (positive CAGR over 5 years) → 🟢
- Equity flat or erratic → 🟡
- Equity declining (accumulated losses eating into reserves) → 🔴

**Report format:**
```
Total Equity: Rs.[X] cr (FY__) vs Rs.[X] cr (FY__ 5yr ago)
Equity CAGR: [X%]
```

---

### Criterion 5: Goodwill & Intangible Assets Quality

**Data source:** fa-balancesheet-agent (Goodwill & Intangibles Check)
**Check:** How much of the asset base is intangible? High goodwill suggests the company overpaid for acquisitions. Intangibles can be written down suddenly.

**Thresholds:**
- Goodwill + Intangibles < 5% of Total Assets → 🟢 (asset base is real/tangible)
- Goodwill + Intangibles 5–15% of Total Assets → 🟡 (monitor for impairment)
- Goodwill + Intangibles > 15% of Total Assets → 🔴 (significant impairment risk)
- Goodwill + Intangibles > 50% of Total Equity → 🔴 (equity at risk if written off)

**Additional check:** Has goodwill increased significantly in recent years? → Indicates large acquisitions → check if these acquisitions are generating returns.

---

### Criterion 6: Contingent Liabilities

**Data source:** fa-balancesheet-agent (Contingent Liabilities section)
**Check:** Contingent liabilities are potential obligations that may become real. Large contingent liabilities relative to net worth are a hidden risk.

**Thresholds:**
- Contingent liabilities < 10% of net worth → 🟢
- Contingent liabilities 10–25% of net worth → 🟡 (review the nature — tax disputes are common and usually partial)
- Contingent liabilities > 25% of net worth → 🔴
- Any single contingent liability > 10% of net worth → 🟡 (concentrated risk)

**Common types (for context, not for verdict):**
- Tax demands under dispute → very common, usually resolved at 20-40% of claimed amount
- Guarantees given for subsidiaries → check if subsidiary is profitable
- Legal claims → check if material

---

### Criterion 7: Capital Work-in-Progress (CWIP)

**Data source:** fa-balancesheet-agent (Non-Current Assets)
**Check:** CWIP represents money locked in projects under construction. Persistent high CWIP without conversion to PP&E signals stalled projects or accounting manipulation.

**Thresholds:**
- CWIP < 10% of Net Fixed Assets (PP&E) → 🟢 (normal expansion)
- CWIP 10–30% of PP&E → 🟡 (significant expansion underway — check timeline)
- CWIP > 30% of PP&E → 🔴 (unusually high — is this real or parked expenses?)
- CWIP staying at similar level for 3+ years without converting to PP&E → 🔴 (stalled project red flag)

---

### Criterion 8: Cash & Cash Equivalents Position

**Data source:** fa-balancesheet-agent (Current Assets)
**Check:** Does the company have adequate cash? A company with high debt AND low cash is vulnerable.

**Assessment (qualitative, not strict thresholds):**
- Cash > Short-term Borrowings → 🟢 (can immediately clear ST debt)
- Cash covers 3+ months of operating expenses → 🟢
- Cash < Short-term Borrowings AND low current ratio → 🔴
- Cash growing steadily over 5 years → positive signal
- Cash declining while debt rises → 🔴

**Report format:**
```
Cash & Cash Equivalents: Rs.[X] cr (FY__)
Short-term Borrowings: Rs.[X] cr
Cash covers ST borrowings: [Yes/No]
```

---

### Criterion 9: Trade Receivables & Inventory Health

**Data source:** fa-balancesheet-agent (Current Assets)
**Check:** Rising receivables (money owed to the company) and inventory (unsold stock) relative to revenue can signal poor collection discipline or slowing demand.

**Thresholds (Receivable Days = Trade Receivables / Revenue × 365):**
- Receivable Days < 45 → 🟢
- Receivable Days 45–90 → 🟡
- Receivable Days > 90 → 🔴 (collection issues)
- Receivable Days increasing over 3+ years → bump one level

**Thresholds (Inventory Days = Inventory / COGS × 365, or Inventory / Revenue × 365 as proxy):**
- Inventory Days stable or declining → 🟢
- Inventory Days increasing moderately → 🟡
- Inventory Days increasing sharply (>30% rise in 3 years) → 🔴

**Note:** Revenue and COGS figures are needed from the P&L. If not available from the agent data, fetch from Screener.in directly. Use Revenue as a proxy for COGS if COGS is not available.

---

### Criterion 10: Balance Sheet Validation & Red Flags Scan

**Data source:** fa-balancesheet-agent (full report)
**Check:** Meta-level checks on the balance sheet as a whole.

**Items to verify:**
1. **Total Assets = Total Liabilities** — If they don't match in the data, flag as data quality issue
2. **Loans given by company (non-current financial assets)** — Are there significant loans to promoters/subsidiaries? (>5% of total assets → 🟡, >10% → 🔴)
3. **Other Non-Current Assets growing significantly** — Catch-all category that can hide problems
4. **Trade Payables trend** — Sharply rising trade payables may indicate the company is delaying supplier payments (cash stress)
5. **Promoter Pledging** — Already covered in Management Integrity, but cross-reference here:
   - Pledging < 25% → 🟢
   - Pledging 25–50% → 🟡
   - Pledging > 50% → 🔴

**Overall criterion verdict:**
- All sub-checks clean → 🟢
- 1-2 minor flags → 🟡
- Any significant red flag → 🔴

---

## Aggregating the Balance Sheet Score

After completing all 10 criteria:

1. Count: Greens, Ambers, Reds
2. Apply override rules:
   - D/E > 3.0 (non-BFSI company) → **Balance Sheet = 🔴 regardless**
   - Current Ratio < 0.75 → **Balance Sheet = 🔴 regardless** (Money Purse P11: even large companies need caution below 0.75)
3. Otherwise:
   - 0 Red, ≤2 Amber → 🟢 Balance Sheet Strong
   - 1 Red OR 3-4 Amber → 🟡 Balance Sheet Adequate with Concerns
   - 2+ Red OR 5+ Amber → 🔴 Balance Sheet Weak

## Output Format

Return the analysis in this structure:

```
BALANCE SHEET ANALYSIS: [Company Name] ([Ticker])
Data as of: [FY end date]

| # | Criterion | Key Numbers | Status |
|---|-----------|-------------|--------|
| 1 | Debt-to-Equity | D/E: [X], Trend: [direction] | 🟢/🟡/🔴 |
| 2 | Current & Quick Ratio (Liquidity) | CR: [X], QR: [X], CR>3 flags: [summary] | 🟢/🟡/🔴 |
| 3 | Borrowing Trend | [X] CAGR vs [X] Rev CAGR | 🟢/🟡/🔴 |
| 4 | Equity Growth | Equity CAGR: [X%] | 🟢/🟡/🔴 |
| 5 | Goodwill & Intangibles | [X%] of assets | 🟢/🟡/🔴 |
| 6 | Contingent Liabilities | [X%] of net worth | 🟢/🟡/🔴 |
| 7 | Capital Work-in-Progress | [X%] of PP&E | 🟢/🟡/🔴 |
| 8 | Cash Position | Cash: Rs.[X] cr vs ST Debt: Rs.[X] cr | 🟢/🟡/🔴 |
| 9 | Receivables & Inventory | Recv Days: [X], Inv trend: [dir] | 🟢/🟡/🔴 |
| 10 | Red Flags Scan | [Summary] | 🟢/🟡/🔴 |

Balance Sheet Score: [X/10 Green]
Overall Balance Sheet Verdict: 🟢/🟡/🔴

Key Balance Sheet Concerns:
- [List any 🔴 or 🟡 items with brief explanation]

Key Balance Sheet Strengths:
- [List notable positives]
```

## Data Sources (in priority order)

1. **Screener.in** — Primary source for 5-10 year balance sheet data, ratios
2. **BSE India** — Annual Reports, Notes to Accounts for borrowing details and contingent liabilities
3. **Moneycontrol** — Fallback for balance sheet data if Screener.in unavailable
4. **Tickertape.in** — Secondary fallback, also useful for quick ratio checks
5. **Company Investor Relations page** — Annual Reports, investor presentations

Always use live data from these sources. Never use memorized or cached financial figures.
