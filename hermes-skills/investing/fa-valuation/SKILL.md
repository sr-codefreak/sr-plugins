---
name: fa-valuation
description: This skill should be used when evaluating the valuation of an NSE-listed company, checking "P/E ratio", "price to earnings", "price to cash flow", "P/CF ratio", "PEG ratio", "price earnings growth", "price to sales", "P/S ratio", "price to book", "P/B ratio", "EV/EBITDA", "enterprise value to EBITDA", "intrinsic value", "DCF", "discounted cash flow", "is the stock cheap or expensive", "valuation attractive", "fair value", or when the fa-orchestrator has reached the valuation analysis phase. Applies a 7-point checklist derived from Money Purse valuation framework to assign RAG verdicts.
version: 1.0.0
---

# FA Valuation Analysis — Leaf Skill

Analyze the valuation of an NSE-listed company using a 7-point checklist. For each criterion: state the finding with actual numbers, cite the data source, and assign a RAG verdict.

## Input Required

Before starting, confirm availability of the valuation data packet from:
- fa-valuation-agent: P/E, P/CF, PEG, P/S, P/B, EV/EBITDA, intrinsic value inputs, sector peers, historical P/E range

If agent data is missing, note "Data unavailable — unable to verify" for affected criteria rather than assuming clean.

## Mindset

> "70-80% of weightage should be on qualitative aspects (business model, management, industry, financials). Only 20-30% of weightage is for valuations." — Money Purse P12
>
> "If you just rely on valuation parameters, you may become a good valuer, not a good investor. You won't be able to invest in new age businesses like Amazon, Apple, Google." — Money Purse P12
>
> Valuations are the LAST step — only apply after Phase 1 qualitative + financial analysis confirms the business is worth investing in. A cheap stock in a bad business is still a bad investment.

## Important Caveats (apply before analysis)

1. **Same-sector comparison ONLY** — Never compare P/E of an FMCG stock with a Pharma stock. Compare Dabur with HUL, not Dabur with Dr. Reddy's. (Money Purse P12: "we should not compare stocks of companies in different sectors")
2. **Cyclical company trap** — P/E of cyclical companies (metals, chemicals, sugar, commodities) appears LOW at peak earnings. Buying at low P/E = buying at peak = trap. Use P/S, EV/EBITDA, or normalized earnings instead. (Money Purse P12)
3. **Earnings manipulation risk** — Fraudulent managements can inflate earnings, making P/E appear low. Always cross-check with P/CF (cash flows are harder to manipulate). (Money Purse P12)
4. **P/E doesn't consider balance sheet quality** — A company taking on massive debt to boost profits will show low P/E but has hidden risk. (Money Purse P12: "P/E don't consider the Quality of earnings")
5. **Banks/NBFCs** — Use P/B as primary metric (not P/E or EV/EBITDA). P/E can be misleading due to provisions and NPA cycles. (Money Purse P13 fragments)
6. **Growth assumptions in PEG are just estimates** — Past growth may not continue. If the company can't grow as calculated, PEG-based decisions will be wrong. (Money Purse P12: "There is no absolute certainty that growth of company will exactly match")
7. **Loss-making / early-stage companies** — P/E is meaningless for negative earnings. Use P/S, EV/Revenue, or DCF with projected cash flows.

## The 7-Point Valuation Checklist

Work through each criterion in order. For each criterion:
1. State the specific numbers found
2. Apply the threshold rules below
3. Assign RAG status
4. Note the source (Screener.in URL, Tijori Finance, etc.)

---

### Criterion 1: P/E Ratio Assessment

**Data source:** fa-valuation-agent (P/E section)
**Formula:** Current Market Price / Earnings Per Share (TTM)
**EPS Formula:** Net Income / Total Outstanding Shares (Money Purse P12: demonstrated with Tata Elxsi on BSE — 113 cr profit / 6.23 cr shares = 18.21 EPS)

**Thresholds (per book, Money Purse P12):**
- P/E < 12 → extremely oversold / very cheap
- P/E 12–15 → very attractive zone
- P/E 15–20 → attractive zone
- P/E 20–25 → expensive zone
- P/E > 25 → overbought zone

**But these are GUIDELINES, not hard rules.** Context matters:
- High-growth companies (>20% EPS CAGR) can justify P/E > 25
- Mature/slow-growth companies with P/E > 25 → genuinely expensive
- Cyclical companies at low P/E → may be a TRAP (peak earnings)

**RAG Verdict Logic:**
- P/E below historical 5-year median AND below sector median → 🟢 (attractively valued)
- P/E near historical median, within sector range → 🟡 (fairly valued)
- P/E above historical 5-year high OR significantly above sector median → 🔴 (expensive)
- P/E negative (loss-making) → ⬜ N/A (use P/S and EV/EBITDA instead)
- Cyclical company at low P/E with peak earnings → 🟡 or 🔴 (flag the trap)

**Report format:**
```
Trailing P/E: [X]
Sector median P/E: [X]
Historical 5yr P/E: Median [X], Low [X], High [X]
Current vs historical: [Below median / At median / Above median]
Current vs sector: [Below / At / Above sector median]
Cyclical check: [Yes/No — if yes, flag peak earnings risk]
```

---

### Criterion 2: Price-to-Cash Flow (P/CF)

**Data source:** fa-valuation-agent (P/CF section)
**Formula:** Current Market Price / Cash Flow per Share
**Cash Flow per Share:** Operating Cash Flow / Outstanding Shares (Money Purse P12)

**Why P/CF matters:** (Money Purse P12) P/CF addresses the "quality of earnings" challenge in P/E. It checks whether the company is genuinely generating profits or merely reflecting them in financial statements. "It is not an easy task to manipulate the Cashflows."

**Thresholds:**
- P/CF < 10 → 🟢 (cheap relative to cash generation)
- P/CF 10–20 → 🟡 (fairly valued)
- P/CF 20–30 → 🟡 (expensive — check if justified by growth)
- P/CF > 30 → 🔴 (very expensive relative to cash generation)
- P/CF negative (negative OCF) → 🔴 (company not generating operating cash)

**Cross-check with P/E:**
- P/E low but P/CF high → earnings may be inflated (cash not supporting profit claims) → flag concern
- P/E high but P/CF low → strong cash generation despite accounting adjustments → less concerning
- Both P/E and P/CF low → genuinely cheap → 🟢

**Sector comparison:** Compare P/CF within industry — lower is better relative to peers.

**Report format:**
```
P/CF Ratio: [X]
OCF per Share: Rs.[X]
P/E vs P/CF comparison: P/E [X] vs P/CF [X]
P/CF vs sector peers: [Below / At / Above peer average]
Earnings quality signal: [Consistent / Divergent — flag if P/E and P/CF tell different stories]
```

---

### Criterion 3: PEG Ratio

**Data source:** fa-valuation-agent (PEG section)
**Formula:** P/E / EPS Growth Rate (CAGR) (Money Purse P12)

**Growth rate selection:** (Money Purse P12)
- If 1-year EPS growth is abnormal (>100% like Tata Elxsi's 142%, or negative), do NOT use it — "1 year growth can create impact on 2 year"
- Prefer 3-year or 5-year EPS CAGR to reduce error rate
- If company delivers consistent growth, 3-year is sufficient
- Source: Tijori Finance → Financials → Growth table, or Screener.in profit growth

**Thresholds:** (Money Purse P12)
- PEG < 1 → 🟢 (attractive — stock is cheap relative to growth, per Money Purse P12)
- PEG = 1 → 🟡 (fairly valued — price reflects growth)
- PEG 1.0–1.5 → 🟡 (slightly expensive but acceptable in practice per Money Purse P12: "in most cases we cannot get stocks less than 1")
- PEG 1.5–1.75 → 🟡 (upper bound of acceptable per Money Purse P12)
- PEG > 1.75 → 🔴 (expensive — growth doesn't justify the premium)
- PEG negative (negative growth or negative earnings) → ⬜ N/A

**Caveats:**
- Growth is an ASSUMPTION. "There is no absolute certainty that growth will match exactly as calculated." (Money Purse P12)
- If using past growth for a company entering a structural slowdown, PEG will be misleadingly low
- Cross-reference with industry growth rate — company growth should be at or above industry

**Report format:**
```
P/E: [X]
EPS CAGR (3yr): [X%]
EPS CAGR (5yr): [X%]
PEG (3yr basis): [X]
PEG (5yr basis): [X]
Growth assumption risk: [Low / Medium / High — based on consistency of past growth]
```

---

### Criterion 4: Price-to-Sales (P/S) Ratio

**Data source:** fa-valuation-agent (P/S section)
**Formula:** Market Capitalization / Revenue (or CMP / Revenue per Share)
(Money Purse P13: demonstrated with Golem International — Market Cap 1596 cr / Revenue 524 cr = P/S 3.05)

**When P/S is most useful:**
- Loss-making companies (P/E is meaningless)
- Cyclical companies (earnings are volatile, revenue is more stable)
- High-growth companies burning cash but growing revenue rapidly
- Companies with temporarily depressed margins

**Thresholds (general — highly sector-dependent):**
- P/S < 1.0 → 🟢 (cheap — paying less than 1x revenue)
- P/S 1.0–3.0 → 🟡 (moderate — acceptable for profitable companies)
- P/S 3.0–8.0 → 🟡 (expensive — only justified for high-margin, high-growth)
- P/S > 8.0 → 🔴 (very expensive — needs exceptional growth to justify)

**Sector context is critical:**
- IT services: P/S 3-6 is normal (high margins)
- FMCG: P/S 5-10 is normal (brand premium, high margins)
- Manufacturing / Commodities: P/S > 2 is expensive (low margins)
- Banks/NBFCs: P/S is less meaningful — use P/B instead

**RAG Verdict:** Compare to sector peers rather than absolute thresholds.
- Below sector median P/S → 🟢
- At sector median → 🟡
- Above sector median → 🔴

**Report format:**
```
P/S Ratio: [X] (Market Cap Rs.[X] cr / Revenue Rs.[X] cr)
Sector peers P/S: [Peer 1]: [X], [Peer 2]: [X], [Peer 3]: [X]
vs sector median: [Below / At / Above]
Company net margin: [X%] — margin justifies P/S? [Yes / No]
```

---

### Criterion 5: Price-to-Book (P/B) Ratio

**Data source:** fa-valuation-agent (P/B section)
**Formula:** Current Market Price / Book Value per Share

**When P/B is most useful:** (Money Purse P13 context: banks, NBFCs, asset-like businesses)
- Banks & NBFCs (primary valuation metric — earnings are volatile due to provisions/NPAs)
- Asset-heavy businesses (real estate, manufacturing, infrastructure)
- Companies with significant tangible assets on the balance sheet

**Thresholds (general):**
- P/B < 1.0 → 🟢 (trading below book value — but check why! Could be value trap)
- P/B 1.0–3.0 → 🟡 (moderate premium to book value)
- P/B 3.0–5.0 → 🟡 (high premium — needs strong ROE to justify)
- P/B > 5.0 → 🔴 (very high premium — only justified for exceptional ROE companies)

**P/B and ROE linkage:**
- High P/B is justified ONLY if ROE is high — a company earning 25% ROE deserves higher P/B than one earning 10%
- P/B > 3 with ROE < 15% → 🔴 (overvalued)
- P/B < 1.5 with ROE > 20% → 🟢 (attractively valued)

**Banking-specific thresholds:**
- P/B < 1.0 → potentially distressed or NPA-heavy → investigate
- P/B 1.0–2.0 → normal range for good banks
- P/B 2.0–3.5 → premium bank (HDFC Bank, Kotak type)
- P/B > 3.5 → expensive even for best banks

**Report format:**
```
P/B Ratio: [X]
Book Value per Share: Rs.[X]
ROE (latest): [X%] — P/B justified by ROE? [Yes / No]
Sector peers P/B: [Peer 1]: [X], [Peer 2]: [X], [Peer 3]: [X]
Banking/NBFC context: [If applicable — NPA quality, provision coverage]
```

---

### Criterion 6: EV/EBITDA

**Data source:** fa-valuation-agent (EV/EBITDA section)
**Formula:**
- Enterprise Value (EV) = Market Cap + Total Debt - Cash & Cash Equivalents
- EV/EBITDA = Enterprise Value / EBITDA

**Why EV/EBITDA:** EV/EBITDA is superior to P/E for comparing companies with different capital structures because:
- It includes debt (unlike market cap alone)
- It uses EBITDA (pre-interest, pre-tax, pre-depreciation) — removes accounting differences
- Makes levered and unlevered companies comparable

**Thresholds (general — sector-dependent):**
- EV/EBITDA < 8 → 🟢 (cheap)
- EV/EBITDA 8–15 → 🟡 (fairly valued)
- EV/EBITDA 15–25 → 🟡 (expensive — needs growth justification)
- EV/EBITDA > 25 → 🔴 (very expensive)

**Sector adjustments:**
- Capital-intensive (Power, Infra): EV/EBITDA < 10 is normal
- IT / Tech: EV/EBITDA 15-25 is normal
- FMCG / Consumer: EV/EBITDA 20-40 is common (brand premium)
- Banks/NBFCs: EV/EBITDA is not applicable — skip or mark N/A

**RAG Verdict:** Compare to sector peers.
- Below sector median → 🟢
- At sector median → 🟡
- Above sector median → 🔴

**Report format:**
```
EV: Rs.[X] cr (MCap [X] + Debt [X] - Cash [X])
EBITDA: Rs.[X] cr
EV/EBITDA: [X]
Sector peers: [Peer 1]: [X], [Peer 2]: [X], [Peer 3]: [X]
vs sector median: [Below / At / Above]
```

---

### Criterion 7: Intrinsic Value / DCF Assessment

**Data source:** fa-valuation-agent (DCF inputs section)
**Framework:** Simplified DCF based on Free Cash Flow (Money Purse P14: "What is Intrinsic Value of a Stock", Warren Buffett reference)

**Simplified DCF Calculation:**
1. Take average FCF of last 3-5 years (or latest if growing consistently)
2. Project FCF growth for next 10 years using conservative growth rate:
   - Use lower of: (a) past 5-year FCF CAGR, (b) past 5-year revenue CAGR, (c) industry growth rate
   - Cap growth rate at 15% for conservatism (even if past growth was higher)
3. Terminal growth rate: 3-4% (long-term GDP growth proxy)
4. Discount rate: Risk-free rate (10yr Govt Bond) + Equity Risk Premium (5-6%) ≈ typically 11-13%
5. Intrinsic Value per Share = PV of projected FCFs + PV of Terminal Value / Outstanding Shares

**Thresholds:**
- CMP < 70% of Intrinsic Value → 🟢 (significant margin of safety)
- CMP 70-100% of Intrinsic Value → 🟡 (near fair value — limited margin of safety)
- CMP > 100% of Intrinsic Value → 🔴 (overvalued relative to DCF)
- FCF negative or erratic → ⬜ N/A (DCF not reliable; note and skip)

**Caveats:**
- DCF is highly sensitive to growth rate and discount rate assumptions — small changes create large swings in intrinsic value
- Present the intrinsic value as a RANGE (optimistic, base, conservative scenarios) rather than a single number
- If FCF is inconsistent, DCF is unreliable — note this limitation
- For high-growth companies, DCF will vary wildly based on terminal growth assumptions

**Report format:**
```
DCF Inputs:
  Avg FCF (3yr): Rs.[X] cr
  Growth rate assumed: [X%] (based on [rationale])
  Discount rate: [X%] (RFR [X%] + ERP [X%])
  Terminal growth: [X%]

Intrinsic Value per Share:
  Conservative (growth -2%): Rs.[X]
  Base case: Rs.[X]
  Optimistic (growth +2%): Rs.[X]

CMP: Rs.[X]
CMP as % of Base Intrinsic Value: [X%]
Margin of Safety: [X%] (positive = undervalued)
```

---

## Aggregating the Valuation Score

After completing all 7 criteria:

1. Count: Greens, Ambers, Reds (exclude N/A from count)
2. Apply override rules:
   - If company is a cyclical at peak earnings with low P/E → do NOT give overall Green (trap risk)
   - If P/E is Green but P/CF tells a different story (divergence) → downgrade to Amber at best
   - If intrinsic value shows >30% overvaluation AND most relative metrics (P/E, P/S, EV/EBITDA) are above sector → 🔴 regardless
3. Otherwise:
   - 0 Red, ≤ 2 Amber → 🟢 Valuation Attractive
   - 1 Red OR 3 Amber → 🟡 Valuation Fair / Mixed
   - 2+ Red OR 4+ Amber → 🔴 Valuation Expensive

## Output Format

Return the analysis in this structure:

```
VALUATION ANALYSIS: [Company Name] ([Ticker])
Data as of: [Date]
CMP: Rs.[X] | Market Cap: Rs.[X] cr

| # | Criterion | Key Numbers | Status |
|---|-----------|-------------|--------|
| 1 | P/E Ratio | Trailing P/E: [X], Sector median: [X] | 🟢/🟡/🔴/⬜ |
| 2 | Price-to-Cash Flow | P/CF: [X] | 🟢/🟡/🔴 |
| 3 | PEG Ratio | PEG (3yr): [X], EPS CAGR: [X%] | 🟢/🟡/🔴/⬜ |
| 4 | Price-to-Sales | P/S: [X], vs sector: [position] | 🟢/🟡/🔴 |
| 5 | Price-to-Book | P/B: [X], ROE: [X%] | 🟢/🟡/🔴 |
| 6 | EV/EBITDA | EV/EBITDA: [X], vs sector: [position] | 🟢/🟡/🔴/⬜ |
| 7 | Intrinsic Value / DCF | CMP vs IV: [X%], Margin of Safety: [X%] | 🟢/🟡/🔴/⬜ |

Valuation Score: [X/7 Green] (or X/N if some N/A)
Overall Valuation Verdict: 🟢/🟡/🔴

Key Valuation Concerns:
- [List any 🔴 or 🟡 items with brief explanation]

Key Valuation Strengths:
- [List notable positives, e.g. trading below intrinsic value, PEG < 1, below sector median on all metrics]

Valuation Context:
- Reminder: Valuation carries only 20-30% weightage. A cheap stock in a bad business is still bad.
- Phase 1 Quality Check: [Reference management, industry, financial health verdicts from earlier phases]
```

## Data Sources (in priority order)

1. **Screener.in** — Primary source for P/E, P/B, EPS, revenue, balance sheet data, peer comparison
2. **Tijori Finance** — EPS CAGR growth rates, financial metrics
3. **Moneycontrol** — Fallback for valuation ratios, historical P/E
4. **Tickertape.in** — Peer comparison, sector averages
5. **BSE/NSE website** — Outstanding shares, market cap, latest price
6. **RBI / Bond yield sites** — Risk-free rate for DCF

Always use live data from these sources. Never use memorized or cached financial figures.
