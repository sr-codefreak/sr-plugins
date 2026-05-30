---
name: fa-industry-stage
description: This skill should be used when classifying industry lifecycle stage, determining "pioneering stage", "growth stage", "maturity stage", "saturation stage", "decline stage", "where is this industry in its lifecycle", "industry growth rate classification", or when the fa-industry sub-master skill needs to assess the lifecycle position of a company's industry. Uses IBEF and market data.
version: 1.0.0
---

# FA Industry Stage — Leaf Skill

Classify the company's primary industry into one of four lifecycle stages and explain the investment implications.

## Primary Research Source: IBEF.org

India Brand Equity Foundation (ibef.org) publishes free sector reports for most major Indian industries. Always attempt to find and reference the most recent IBEF report for the sector.

**How to find IBEF reports:**
1. Navigate to ibef.org → Industries
2. Search by sector name (e.g., "Wires and Cables", "Paints", "Dairy", "QSR")
3. Download the latest PDF or reference the web report
4. Key data to extract: Market size (₹ cr or $ bn), historical growth rate (CAGR), projected CAGR, penetration rates, key players

If IBEF doesn't have a specific report, use:
- Industry association reports (CII, FICCI, ASSOCHAM)
- IBEF's parent sector report (e.g., "Manufacturing" if specific sub-sector is absent)
- Company's own Annual Report → Industry Overview section (usually 2-3 pages in MD&A) — note this is company-prepared and may be optimistic

## The Four Stages: Classification Criteria

---

### Stage 1: Pioneering

**Definition:** The market is being created. The product or service category has very low penetration. Business models are still being tested. Most players are losing money or just breaking even.

**Classification signals:**
- Market penetration <10% of theoretical addressable market
- Most players are startups or recently listed (last 3-5 years)
- Revenue CAGR is very high (>40%) but from a very small base
- Profitability is scarce industry-wide — investment phase dominates
- Competing business models exist — no dominant approach has won
- Institutional/VC funding is the dominant capital source
- The category barely existed 5 years ago

**India examples (as of 2026 context):**
- Electric vehicle 2-wheelers (still in early innings)
- Drone manufacturing
- Quick Commerce (10-minute delivery)
- Direct-to-consumer D2C digital-first brands

**Investment implication:**
- This is inherently speculative — the category may not reach critical mass
- Management quality and first-mover advantages matter more than current financials
- Focus on market share capture, not margins
- Be prepared for multiple funding rounds diluting equity

---

### Stage 2: Growth

**Definition:** The category has been validated. Winners are beginning to emerge. Market size is growing rapidly. Profit pools are forming. Institutional investors are increasing coverage.

**Classification signals:**
- Market penetration 10-40% of addressable market
- Industry revenue CAGR of 15-40% over last 3-5 years
- Profitable leaders emerging (though laggards may still be loss-making)
- Increasing consolidation — top 3-4 players capturing most new growth
- Sector ETFs or thematic mutual funds being created
- Media and analyst coverage expanding significantly
- IPO pipeline in the sector is active

**India examples (as of 2026 context):**
- Organized retail (despite decades, penetration still ~12% of total retail)
- Digital payments infrastructure (UPI ecosystem businesses)
- Hospital chains (private healthcare penetration still growing)
- Airport-related services
- Data center / cloud infrastructure

**Investment implication:**
- Premium valuation is justified by growth rate — don't over-focus on P/E
- Market share capture is more important than margin optimization at this stage
- Even mediocre companies in growth industries do well (don't attribute company success entirely to management)
- Key risk: paying too high a price assuming the growth phase lasts longer than it does

---

### Stage 3: Maturity / Saturation

**Definition:** The industry has reached a large size. Growth has slowed to reflect nominal GDP or slightly above. Consolidation has completed; 2-4 dominant players control most of the market. Margins are structurally stable. **Premiumization becomes the primary organic growth strategy** — moving existing customers up the value chain.

**Classification signals:**
- Market penetration >40% of addressable market
- Industry revenue CAGR of 8-15% (broadly in line with or slightly above nominal GDP)
- Consolidated market: top 3-4 players control 60%+ of revenue
- Pricing discipline has returned (the price wars of the growth/transition phase are over)
- Strong brands command meaningful premium pricing
- Capital allocation shifts toward dividends, buybacks, or adjacent expansion
- M&A activity is about strategic bolt-ons, not transformational bets

**India examples (most NSE large-caps are here):**
- FMCG (HUL, Asian Paints, Marico)
- Two-wheelers (Hero, Bajaj, TVS)
- Wires and cables (Polycab, Havells, KEI)
- Private sector banking (HDFC, ICICI, Kotak)
- Paints (Asian Paints, Berger, Kansai)

**Premiumization as growth lever:**
In maturity, organic volume growth is limited. The dominant strategy for premium incumbents is:
- Moving consumers from economy to mid-range products
- Moving mid-range consumers to premium
- Launching luxury/super-premium sub-brands
- Expanding into adjacent high-margin categories
Companies that successfully premiumize in mature industries consistently outperform the sector's overall growth rate.

**Investment implication:**
- Earnings stability and predictability = lower required return = higher justified valuation
- Strong moat (brand, distribution, cost leadership) is what separates good companies from average ones
- Management capital allocation quality matters enormously at this stage
- Watch for premiumization execution — companies successfully trading consumers up should get premium multiples

---

### Stage 4: Decline

**Definition:** The industry's structural demand is contracting. Volume is falling or flat despite pricing increases. The industry is being disrupted by a substitute, structural change in customer behavior, or regulatory phase-out.

**Classification signals:**
- Industry volumes declining year-on-year in absolute terms
- Companies shutting down capacity rather than adding
- Market leaders returning capital (high dividends, buybacks) rather than investing — signal of no growth reinvestment opportunity
- A substitute technology is actively capturing market share (not theoretical — actually happening)
- Regulatory phase-out underway (internal combustion engines, certain chemicals/plastics)
- New entrant count near zero (no one is entering a declining market)

**India examples (as of 2026 context):**
- Traditional print media and newspaper advertising
- Feature phones (voice-only mobiles)
- Landline telephone infrastructure
- Some legacy chemical categories being displaced by alternatives

**Investment implication:**
- Avoid as a long-term holding unless a specific turnaround thesis exists
- Exceptions: companies with exceptional cost structures that survive as the last man standing (can raise prices as competitors exit)
- Cash extraction thesis: declining company with zero capex needs and high FCF — value it as a bond, not a growth equity
- High risk: decline can accelerate suddenly (technology disruption is rarely linear)

---

## Classification Procedure

1. **Identify the industry** from the stock universe file.
2. **Retrieve IBEF data** (via fa-industry-research-agent findings): market size, CAGR, penetration.
3. **Check the stage signals table above** — match the data to the stage indicators.
4. **State the stage** and write a 2-3 sentence rationale explaining:
   - The specific data point(s) that determined the stage
   - Any ambiguity (some industries show mixed signals — e.g., premium sub-segment growing while mass segment is in maturity)
5. **State the investment implication** for this specific company given the stage.

## Stage Ambiguity

Some industries span two stages simultaneously:
- **Growth → Maturity transition**: Industry is structurally mature but a new sub-segment (e.g., premium, EV, digital) is in growth. Classify as "Maturity with a growth pocket" and identify the specific opportunity.
- **Maturity → Decline transition**: Volume growth has stopped but replacement demand is strong. Classify as "Late Maturity / Early Decline Watch."

When uncertain between two stages, state both and explain the tipping points.

## References

- **`references/stage-indicators.md`** — Detailed indicator checklist per stage with Indian market examples and quantitative thresholds
