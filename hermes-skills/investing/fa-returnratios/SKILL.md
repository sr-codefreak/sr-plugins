---
name: fa-returnratios
description: This skill should be used when evaluating the return ratios of an NSE-listed company, checking "ROCE", "return on capital employed", "ROE", "return on equity", "ROA", "return on assets", "DuPont analysis", "DuPont decomposition", "capital efficiency", "asset turnover", "equity multiplier", "leverage-driven returns", "return ratio trend", "sector-relative returns", or when the fa-orchestrator has reached the return ratios analysis phase. Applies a 7-point checklist derived from Money Purse return ratio analysis framework to assign RAG verdicts.
version: 1.0.0
---

# FA Return Ratios Analysis — Leaf Skill

Analyze the return ratios (ROCE, ROE, ROA) and DuPont decomposition of an NSE-listed company using a 7-point checklist. For each criterion: state the finding with actual numbers, cite the data source, and assign a RAG verdict.

## Input Required

Before starting, confirm availability of the return ratio data packet from:
- fa-returnratios-agent: ROCE/ROE/ROA trends, DuPont components, capital employed, equity, total assets, peer comparison

If agent data is missing, note "Data unavailable — unable to verify" for affected criteria rather than assuming clean.

## Mindset

> "Margins alone tell you what percentage of revenue becomes profit. But they don't tell you how efficiently the company uses its capital to generate those profits." — Money Purse (P7→P8 transition)
>
> "If we invest in FDs we get 6-7% without risk. Mutual funds give 10-12% without effort. When we directly invest, the company should generate more than this — ROCE and ROE should be at least 13-15%." — Money Purse (P9)
>
> Example: Dixon Technologies has single-digit net margins (~3-4%) but 30-40% ROCE/ROE because of extremely high asset turnover. Without return ratios, you would wrongly dismiss Dixon as a poor business.

## Why Return Ratio Analysis Matters

1. **Margins vs Returns** — A company with high margins but poor capital efficiency is wasteful. A company with low margins but high asset turnover can deliver outstanding returns (Dixon Technologies, D-Mart).
2. **Capital allocation quality** — ROCE shows how well management deploys total capital (equity + debt). High ROCE = management is creating value.
3. **Leverage detection** — ROE can be artificially inflated by high debt. DuPont decomposition separates genuine profitability from leverage-driven returns.
4. **Sustainable compounding** — Companies with consistently high return ratios (ROCE > cost of capital) create long-term shareholder wealth. This is the single most important factor for multi-bagger identification.

## Important Caveats (apply before analysis)

1. **Banks, NBFCs & HFCs** — ROCE is less meaningful for financial companies. Since banks' primary function is providing loans, high debt is structural. ROCE will be single digits — misleading. Use ROE and ROA only. ROA for banks is typically 1-2% (normal). Compare banks only via ROE. (Money Purse P9)
2. **Cyclical businesses** — ROCE/ROE will fluctuate with commodity cycles (metals, chemicals, sugar). Use 5-year averages and judge across full cycle.
3. **Companies in capex phase** — Heavy capex temporarily depresses ROCE/ROA because the asset base grows before revenue ramps. Check if ROCE is recovering post-capex.
4. **Turn-around companies** — Companies with poor past performance but significant improvement potential due to management/strategy changes. Past return ratios may be low — judge on trajectory, not absolute level. (Money Purse P9)
5. **Same-sector comparison only** — Capital-intensive businesses (power, steel) will always have lower ROCE than asset-light (IT, FMCG). Compare only within the same sector. (Money Purse P9: "Don't compare with different industry companies")
6. **Negative equity companies** — If equity is negative (accumulated losses), ROE is meaningless. Flag and skip ROE criterion.

## The 7-Point Return Ratios Checklist

Work through each criterion in order. For each criterion:
1. State the specific numbers found
2. Apply the threshold rules below
3. Assign RAG status
4. Note the source (Screener.in URL, AR page number, etc.)

---

### Criterion 1: ROCE (Return on Capital Employed)

**Data source:** fa-returnratios-agent (ROCE trend)
**Formula:** EBIT / Capital Employed, where Capital Employed = Equity + Non-Current Liabilities

**Why EBIT (not PAT)?** (Money Purse P9) — ROCE measures return on total capital (equity + debt). Payment priority is: Debt repayment → Tax → Preferred equity → Common shareholders. Since ROCE covers capital from both lenders and equity holders, we use profit BEFORE interest and tax payments (EBIT/PBIT).

**Formula variants** (Money Purse P9): Different sources may use different denominators. If your calculation doesn't match a website's number, try:
- EBIT / (Equity + Non-Current Liabilities) — most common internationally
- EBIT / (Total Assets - Current Liabilities) — equivalent to above
- EBIT / (Equity + Long-Term Debt + Short-Term Debt)
- EBIT / Total Capital Employed

**Thresholds:** (Money Purse P9: "ideally 13-15% minimum")
- 5-year average ROCE > 15% and improving/stable -> Green
- 5-year average ROCE 10-15% -> Amber (adequate but not exceptional)
- 5-year average ROCE < 10% -> Red (poor capital efficiency)
- ROCE consistently > 20% -> strong Green (exceptional capital allocator — note this)

**Sector adjustments:**
- IT / FMCG / Consumer: Expect ROCE > 25% (asset-light). Below 15% = Red for these sectors.
- Capital-intensive (Power, Steel, Cement): ROCE > 12% is Green, 8-12% Amber, <8% Red.
- Banks/NBFCs: Skip ROCE or mark N/A — use ROE + ROA instead.

**Critical check:** ROCE must exceed the company's cost of debt (approximate from interest rate on borrowings). If ROCE < cost of debt, the company is destroying value -> Red.

**Report format:**
```
ROCE (last 5 years):
FY__: [X%] | FY__: [X%] | FY__: [X%] | FY__: [X%] | FY__: [X%]
Average (5yr): [X%]
Trend: [Improving / Stable / Declining]
ROCE vs Cost of Debt: ROCE [X%] vs Interest Rate ~[X%]
```

---

### Criterion 2: ROE (Return on Equity)

**Data source:** fa-returnratios-agent (ROE trend)
**Formula:** PAT / Shareholders' Equity

**Thresholds:**
- 5-year average ROE > 15% -> Green
- 5-year average ROE 10-15% -> Amber
- 5-year average ROE < 10% -> Red
- ROE consistently > 20% -> strong Green (note this)

**Critical cross-check with D/E ratio:**
- If ROE > 15% but D/E > 1.5 -> downgrade by one level (leverage-inflated returns)
- If ROE > 15% with D/E < 0.5 -> genuine high returns, confidence boost
- If ROE is negative due to negative PAT -> Red
- If equity is negative (accumulated losses) -> mark N/A

**Report format:**
```
ROE (last 5 years):
FY__: [X%] | FY__: [X%] | FY__: [X%] | FY__: [X%] | FY__: [X%]
Average (5yr): [X%]
D/E ratio (latest): [X]
Leverage-adjusted assessment: [Genuine / Leverage-inflated]
```

---

### Criterion 3: ROA (Return on Assets)

**Data source:** fa-returnratios-agent (ROA trend, computed)
**Formula:** PAT / Total Assets (preferred, Money Purse P9). Alternative: EBIT / Total Assets.

**Thresholds:**
- 5-year average ROA > 8% -> Green (efficient asset utilization)
- 5-year average ROA 4-8% -> Amber
- 5-year average ROA < 4% -> Red (poor asset productivity)

**Sector adjustments:**
- Asset-light (IT, consulting): Expect ROA > 15%. Below 10% = Amber for these sectors.
- Capital-intensive (Manufacturing, Power): ROA > 5% is Green, 3-5% Amber, <3% Red.
- Banks/NBFCs: ROA > 1.5% = Green, 1-1.5% = Amber, <1% = Red (banks carry massive assets).

**Report format:**
```
ROA (last 5 years):
FY__: [X%] | FY__: [X%] | FY__: [X%] | FY__: [X%] | FY__: [X%]
Average (5yr): [X%]
Sector benchmark: [sector-adjusted threshold]
```

---

### Criterion 4: DuPont Decomposition of ROE

**Data source:** fa-returnratios-agent (DuPont components)
**Formula:** ROE = Net Profit Margin × Asset Turnover × Equity Multiplier

**Components:**
- **Net Profit Margin (NPM)** = PAT / Revenue — measures pricing power & cost control
- **Asset Turnover (AT)** = Revenue / Total Assets — measures how efficiently assets generate revenue
- **Equity Multiplier (EM)** = Total Assets / Equity — measures financial leverage (higher = more debt)

**Thresholds:**
- ROE driven primarily by NPM + AT (EM < 2.0) -> Green (genuine operating returns)
- ROE driven by mix of all three with EM 2.0-3.0 -> Amber (moderate leverage contribution)
- ROE driven primarily by EM (EM > 3.0 or EM increasing while NPM/AT declining) -> Red (leverage-dependent returns — risky)

**Pattern identification:**
- High NPM, Low AT: Premium brand / pricing power model (e.g., Asian Paints)
- Low NPM, High AT: Volume/turnover model (e.g., Dixon Technologies, D-Mart)
- Both moderate: Balanced model
- Declining NPM offset by rising EM: Warning sign — company using debt to mask deteriorating profitability

**Report format:**
```
DuPont Decomposition (latest FY):
  NPM: [X%] × AT: [X]x × EM: [X]x = ROE: [X%]

DuPont 5-year trend:
FY__: NPM [X%] × AT [X]x × EM [X]x = ROE [X%]
FY__: NPM [X%] × AT [X]x × EM [X]x = ROE [X%]
...
Primary driver: [NPM / AT / EM]
Concern: [None / Leverage creep / Margin decline offset by leverage]
```

---

### Criterion 5: ROCE vs ROE Gap Analysis

**Data source:** fa-returnratios-agent (ROCE and ROE trends)
**Check:** The gap between ROCE and ROE reveals how much debt is influencing returns.

**Logic:**
- ROCE ≈ ROE (within 3 percentage points) -> Company has minimal debt influence -> Green
- ROE > ROCE by 3-8 points -> Moderate debt leverage boosting equity returns -> Amber
- ROE > ROCE by >8 points -> Heavy debt leverage -> Red (if D/E also high)
- ROCE > ROE -> Unusual — could mean tax/minority interest drag on equity returns. Investigate but not necessarily negative -> Amber (investigate)

**Thresholds:**
- Gap (ROE - ROCE) <= 3 pts for 3+ of 5 years -> Green
- Gap 3-8 pts -> Amber
- Gap > 8 pts -> Red
- Banks/NBFCs: Mark N/A (ROCE not meaningful)

**Report format:**
```
ROCE vs ROE Gap (last 5 years):
FY__: ROCE [X%], ROE [X%], Gap [X pts]
FY__: ROCE [X%], ROE [X%], Gap [X pts]
...
Average gap: [X pts]
Interpretation: [Minimal debt influence / Moderate leverage / Heavy leverage]
```

---

### Criterion 6: Return Ratio Trend (5-Year Trajectory)

**Data source:** fa-returnratios-agent (all ratio trends)
**Check:** Are return ratios improving, stable, or deteriorating over time?

**Items to verify:**
1. ROCE direction over 5 years (regression: upward/flat/downward)
2. ROE direction over 5 years
3. ROA direction over 5 years
4. Consistency — are ratios stable or erratic year-to-year?
5. Post-capex recovery — if ratios dipped due to capex, have they recovered?

**Thresholds:**
- All three ratios improving or stable above thresholds -> Green
- Mixed signals (some improving, some flat/declining) -> Amber
- All three declining or ROCE/ROE declining 3+ consecutive years -> Red

**Report format:**
```
5-Year Trend Analysis:
  ROCE: [X%] -> [X%] (FY__ to FY__) — [Improving/Stable/Declining]
  ROE:  [X%] -> [X%] (FY__ to FY__) — [Improving/Stable/Declining]
  ROA:  [X%] -> [X%] (FY__ to FY__) — [Improving/Stable/Declining]
Consistency: [Stable / Volatile / Deteriorating]
```

---

### Criterion 7: Sector-Relative Returns

**Data source:** fa-returnratios-agent (peer comparison section)
**Check:** Compare the company's return ratios against sector peers. A company with 12% ROCE in a sector where peers average 8% is strong; the same 12% in a sector averaging 25% is weak.

**Thresholds:**
- ROCE and ROE both above sector median/peer average -> Green
- One ratio above, one below median -> Amber
- Both ROCE and ROE below sector median/peer average -> Red
- If peer data unavailable -> mark N/A (do not penalize for data gap)

**Special cases (from P7 Money Purse teaching):**
- **Dixon Technologies model**: Low NPM (~3-4%) but ROCE 30-40% due to asset-light + high turnover. This is GOOD — don't penalize low margins if return ratios are high.
- **FMCG model (HUL, Asian Paints)**: High NPM + moderate AT. Both return ratios and margins are high.
- The point is: margins and return ratios together give the full picture.

**Report format:**
```
Sector Comparison:
  Company ROCE: [X%] vs Sector median: [X%] — [Above/Below/At par]
  Company ROE:  [X%] vs Sector median: [X%] — [Above/Below/At par]

Peer comparison:
  [Peer 1]: ROCE [X%], ROE [X%]
  [Peer 2]: ROCE [X%], ROE [X%]
  [Peer 3]: ROCE [X%], ROE [X%]
  [Company]: ROCE [X%], ROE [X%] — Rank: [X of Y]
```

---

## Aggregating the Return Ratios Score

After completing all 7 criteria:

1. Count: Greens, Ambers, Reds (exclude N/A from count)
2. Apply override rules:
   - ROCE < 8% average (5yr) for non-BFSI -> **Return Ratios = Red regardless** (company is destroying capital)
   - ROE artificially high (>20%) but driven by EM > 3.5 -> **flag as leverage-driven**, downgrade to Amber at best
   - All three ratios (ROCE, ROE, ROA) declining 4+ consecutive years -> **Return Ratios = Red regardless**
3. Otherwise:
   - 0 Red, <= 2 Amber -> Green (Return Ratios Strong)
   - 1 Red OR 3 Amber -> Amber (Return Ratios Adequate with Concerns)
   - 2+ Red OR 4+ Amber -> Red (Return Ratios Weak)

## Output Format

Return the analysis in this structure:

```
RETURN RATIOS ANALYSIS: [Company Name] ([Ticker])
Data as of: [FY end date]

| # | Criterion | Key Numbers | Status |
|---|-----------|-------------|--------|
| 1 | ROCE | Avg (5yr): [X%], Trend: [direction] | Green/Amber/Red |
| 2 | ROE | Avg (5yr): [X%], D/E: [X] | Green/Amber/Red |
| 3 | ROA | Avg (5yr): [X%] | Green/Amber/Red |
| 4 | DuPont Decomposition | NPM [X%] × AT [X]x × EM [X]x | Green/Amber/Red |
| 5 | ROCE vs ROE Gap | Avg gap: [X pts] | Green/Amber/Red |
| 6 | Return Ratio Trend | [Improving/Stable/Declining] | Green/Amber/Red |
| 7 | Sector-Relative Returns | vs median: [Above/Below] | Green/Amber/Red/N/A |

Return Ratios Score: [X/7 Green] (or X/6 if one N/A)
Overall Return Ratios Verdict: Green/Amber/Red

Key Return Ratio Concerns:
- [List any Red or Amber items with brief explanation]

Key Return Ratio Strengths:
- [List notable positives, e.g. consistently high ROCE compounder, genuine returns not leverage-driven]
```

## Data Sources (in priority order)

1. **Screener.in** — Primary source for ROCE, ROE, ratios, balance sheet, P&L data
2. **Moneycontrol** — Ratios section as fallback
3. **Tickertape.in** — Peer comparison, sector averages
4. **Tijori Finance** — Cross-check for return ratio calculations
5. **Company Annual Report** — Capital employed breakdown, segment-wise ROCE

Always use live data from these sources. Never use memorized or cached financial figures.
