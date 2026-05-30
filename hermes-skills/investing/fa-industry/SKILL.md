---
name: fa-industry
description: This skill should be used when analyzing the industry of an NSE-listed company, checking "industry lifecycle stage", "industry growth prospects", "competitive landscape", "market structure", "Porter's five forces", "entry barriers", "government protection in industry", "industry tailwinds", "sector outlook", or when the fa-orchestrator has reached the industry analysis phase. This is the sub-master skill that delegates to fa-industry-stage and fa-industry-forces leaf skills.
version: 1.0.0
---

# FA Industry — Sub-Master Skill

The industry sub-master coordinates two lenses of industry evaluation: where the industry is in its lifecycle (determines growth expectations) and how the competitive forces are structured (determines margin durability and moat strength).

## Framework Foundation

Industry analysis uses a combination of:
1. **Industry Lifecycle Framework** — adapted from the classical Pioneering/Growth/Maturity/Decline model, applied to Indian listed companies
2. **Porter's Five Forces** — the classic competitive analysis framework, augmented with an India-specific 6th force: Government Protection / Policy

Primary data source for Indian industry research: **IBEF.org** (India Brand Equity Foundation), which publishes free, periodically updated sector reports for most major industries.

## Two Sub-Analyses

### 1. Industry Stage
Delegated to: `fa-industry-stage` leaf skill

Classifies the industry into one of four stages:
- **Pioneering**: Market being created, high risk, high potential
- **Growth**: Rapid expansion, winners emerging, premium valuations justified
- **Maturity/Saturation**: Slow growth, consolidation, premiumization as growth lever
- **Decline**: Structural contraction, disruption underway

### 2. Industry Forces
Delegated to: `fa-industry-forces` leaf skill

Evaluates 7 forces:
1. Competitive rivalry
2. New entrants
3. Substitutes
4. Supplier bargaining power
5. Buyer bargaining power
6. Entry barriers (synthesized)
7. Government protection / policy (India-specific)

## Analysis Protocol

### Step 1: Identify Sector
Confirm the company's primary sector from the stock universe file. For diversified companies, identify the primary revenue segment.

Special handling:
- **Financial services (NBFC, insurance, payments)**: Add RBI/IRDAI/NPCI regulatory environment as an additional sub-topic under government protection
- **Pharmaceuticals**: Add DCGI, USFDA, and API import dependency as additional considerations

### Step 2: Compile Agent Findings
Organize the fa-industry-research-agent's output into:

```
INDUSTRY DATA PACKET for [Company] — [Sector]
────────────────────────────────────────────────
IBEF Data:
  - Market size: ₹X cr / $Y bn
  - Historical CAGR (5yr): Z%
  - Projected CAGR: W%
  - Key IBEF signals: [list]

Competitive Landscape:
  - Top 5 players and estimated market share
  - Pricing dynamics: [commodity/differentiated/premium]
  - Recent M&A activity: [list or "None"]

Porter's Data:
  - Key input suppliers: [names/commodities]
  - Major buyer types: [retail/B2B/government/mixed]
  - Identified substitutes: [list or "None near-term"]
  - Entry barrier assessment: [agent's view]
  - Government schemes/protection: [PLI, duties, policies]
  - Recent new entrants: [list or "None significant"]
```

### Step 3: Run Industry Stage Analysis
Load and apply the `fa-industry-stage` skill. Pass it the IBEF data and competitive landscape data. Receive a stage classification with rationale.

### Step 4: Run Industry Forces Analysis
Load and apply the `fa-industry-forces` skill. Pass it the full industry data packet. Receive 7 verdicts (Favorable/Neutral/Unfavorable per force).

### Step 5: Aggregate Industry Verdict

| Forces Favorable | Stage | Overall |
|-----------------|-------|---------|
| 5-7 Favorable | Growth or Maturity | 🟢 |
| 3-4 Favorable | Any | 🟡 |
| <3 Favorable | Any | 🔴 |
| Any stage | Decline | 🔴 (override) |

## Industry Stage vs Investment Expectation

| Stage | Typical Expectation |
|-------|-------------------|
| Pioneering | High risk, speculative; management quality + first-mover position matter most |
| Growth | Strong revenue growth; market share capture more important than margins |
| Maturity | Earnings stability; moat strength, premiumization, and cost efficiency matter |
| Decline | Avoid unless clear turnaround thesis; need exceptional management + pivot evidence |

## References

- **`references/porters-five-forces.md`** — Detailed Porter's framework adapted for Indian markets with India-specific force definitions
