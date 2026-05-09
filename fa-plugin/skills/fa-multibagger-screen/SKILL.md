---
name: fa-multibagger-screen
description: This skill should be used when screening a stock for multi-bagger potential, checking "multi-bagger characteristics", "durable competitive edge", "moat durability", "earnings sustainability", "variant perception", "P/E re-rating potential", "low free float", "small-cap industry leader", "demerger value unlocking", "promoter holding value", "ROIC capital allocation", or when the fa-orchestrator has completed all analysis phases and needs to assess multi-bagger potential. Applies a 10-point screening checklist derived from Money Purse multi-bagger identification framework. This is a post-FA synthesis skill — it requires outputs from all preceding analysis skills.
version: 1.0.0
---

# FA Multi-bagger Screening — Synthesis Skill

Screen a stock for multi-bagger potential using a 10-point checklist that combines qualitative and quantitative characteristics. This skill runs AFTER all other FA phases are complete — it synthesizes their outputs through a multi-bagger lens.

## Input Required

This skill requires completed outputs from ALL preceding FA analysis phases:
- fa-management (integrity + skillset verdicts)
- fa-industry (stage + forces verdicts)
- fa-balancesheet (10-point verdicts)
- fa-profitloss (10-point verdicts)
- fa-cashflow (7-point verdicts)
- fa-returnratios (7-point verdicts)
- fa-valuation (7-point verdicts)

Additionally, the fa-valuation-agent data packet is needed for free float and market cap data.

If any preceding phase is missing, note "Phase not completed — unable to assess" for affected criteria.

## Mindset

> "If someone gives you the fish, you can eat only 1 time. But if you learned fishing, you can get as your own." — Money Purse (Multi-bagger video)
>
> Multi-baggers are NOT created overnight. They require:
> 1. Strong Fundamentals
> 2. Consistent Business Growth
> 3. Good and Efficient Management with prudent capital allocation
> 4. Larger Free Cash Flows
> 5. TIME and PATIENCE
>
> "Stocks that experience rapid growth solely due to speculation will also fall at a similar pace." — Money Purse

## Important Caveats

1. **Don't chase known multi-baggers** — "If everyone is aware of the competitive edges through social media, then the edge is already identified in the market. The opportunity has already passed." (Money Purse)
2. **Avoid social media euphoria** — IEX monopoly hype example: once competitors entered, stock declined. "Don't invest in stocks that already delivered multi-bagger returns."
3. **Both qualitative and quantitative matter equally** — "Usually, people give more weightage to quantitative... No, both are equally important." (Money Purse)
4. **Peter Lynch origin** — The term "multi-bagger" originated from Peter Lynch's book "One Up On Wall Street", comparing stock returns to baseball bases/bags.

## The 10-Point Multi-bagger Screening Checklist

For each criterion, use the completed FA analysis outputs. State the finding, reference which FA phase provided the data, and assign a screening verdict.

---

### Criterion 1: Durable Competitive Edge (Moat)

**Source:** fa-industry (forces analysis), fa-profitloss (margins), fa-returnratios (ROCE)

**Check:** Does the company have a durable competitive edge that competitors cannot easily replicate?

**Types of edges (Money Purse):**
- **Monopoly/Near-monopoly** business position
- **Strong Brand** — pricing power, consumer confidence (HUL example: customers pay 2-3 Rs more for branded soap)
- **Regulatory edge** — licenses, approvals, compliance barriers (Nestle example)
- **Innovation edge** — technology leadership (KPIT Technologies, Praj example)
- **Operational edge** — low-cost advantage (APL Apollo example)

**Durability check (CRITICAL):** (Money Purse)
- "In the short term, some businesses may appear strong brands, but competitors can kill in short-term"
- Big Bazaar appeared very strong → D-Mart disrupted and dominated → Big Bazaar gone
- Ask: Can a well-funded competitor replicate this edge within 3-5 years?
- If yes → edge is NOT durable → 🟡 or 🔴

**Screening verdict:**
- Durable edge that is NOT yet fully priced in by market → 🟢 (multi-bagger potential)
- Durable edge but already well-known and priced in → 🟡 (limited re-rating potential)
- No clear edge or edge is fragile/replicable → 🔴 (not a multi-bagger candidate)

---

### Criterion 2: Management Quality & Exception Assessment

**Source:** fa-management (integrity + skillset verdicts)

**Check:** Is management capable AND aligned with shareholder interests?

**Standard check:** Reference fa-management verdicts for integrity (10-point) and skillset (4-point).

**Exception rule (Money Purse — nuanced):**
- "Over a period, I learnt that initially I was strict about ignoring companies even with small mistakes. But doing business is not easy."
- Early-stage mistakes BEFORE IPO/listing are excusable IF management learned and stopped repeating them
- Promoters who didn't take salary during tough times, then took higher pay when profitable → understandable
- "If management is repeatedly making mistakes, we need to ignore it"
- "If advantages are against retail shareholders and minority shareholders, then avoid"

**When perception shifts from weak→strong management, significant returns are delivered in that gap.**

**Screening verdict:**
- Strong management + clean integrity + variant perception potential → 🟢
- Adequate management with minor flags but learning trajectory → 🟡
- Repeated integrity failures or anti-minority shareholder behavior → 🔴

---

### Criterion 3: Promoter Holding VALUE (Not Just %)

**Source:** fa-management (promoter data), fa-valuation-agent (market cap)

**Check:** Is the promoter's holding meaningful in absolute VALUE terms, not just percentage?

**The myth (Money Purse):**
- "The common myth is that if a promoter holds 75%, it's a good sign. Not at all!"
- Example: Promoter A holds 50% in a 1 lakh crore company (= Rs.50,000 cr value) AND 75% in a 1000 crore company (= Rs.750 cr value)
- Promoter will prioritize the 50% holding (50,000 cr value) over the 75% holding (750 cr value)
- "We should see how much the promoter is interested in the company"

**What to check:**
1. Calculate: Promoter Holding % × Market Cap = Promoter Holding Value
2. Check if promoter has other listed/unlisted companies with larger holdings
3. If promoter's other interests dwarf this company → lower priority risk

**Exceptions:** (Money Purse)
- Professional-run companies (ITC, L&T) with no single dominant promoter → exception, evaluate separately
- These are run by professional management, not promoter-driven

**Screening verdict:**
- Promoter holding value is their primary/largest interest → 🟢
- Promoter holding is significant but not their largest interest → 🟡
- Promoter has much larger interests elsewhere / professional-run company → 🟡 (with note)
- Very low promoter holding value or promoter clearly disengaged → 🔴

---

### Criterion 4: Sustainable Earnings Growth

**Source:** fa-profitloss (revenue growth, EPS growth), fa-industry (stage)

**Check:** Is earnings growth SUSTAINABLE, not a one-off spike?

**Sustainability test (Money Purse):**
- **Sustainable examples:** Pidilite (demand-driven consistent growth), Astral Pipes, Relaxo — "consistent earnings growth = multi-bagger returns"
- **Unsustainable examples:**
  - Nureca: COVID spike in pulse oximeter sales → earnings collapsed after COVID → stock crashed
  - Mangalam Organics: Camphor price spike → earnings spiked → camphor price fell → stock fell
- **Key question:** Is the earnings trigger structural (permanent demand shift) or cyclical/event-driven (temporary)?

**Sustainability signals:**
- Revenue CAGR > 15% for 5+ years consistently → structural growth → 🟢
- Industry in Growth stage (from fa-industry-stage) → tailwind for sustained growth → 🟢
- Earnings spike in 1-2 years from commodity price or one-off event → likely unsustainable → 🔴
- Capacity additions driving growth with demand visibility → sustainable → 🟢

**Screening verdict:**
- Consistent 5+ year earnings growth with structural demand drivers → 🟢
- Good growth but partially dependent on commodity/cycle → 🟡
- Recent spike from one-off event (COVID, commodity, regulation) → 🔴

---

### Criterion 5: Margins + Asset Turnover Moat

**Source:** fa-profitloss (margins), fa-returnratios (ROCE, ROA, DuPont)

**Check:** Does the company have BOTH margin strength AND asset efficiency?

**Money Purse insight:**
- "Don't use fixed percentage margins like 20% or 30%. Check relative to industry."
- "When there are high margins, there is high chance of competition"
- The real moat: High Asset Turnover + strong brand = competitors can't match price AND quality
- "If they have strong brand recognition, that's a killer. Even if new competition enters, they cannot offer what they offer."
- Companies with high asset turn + high volume business → higher multi-bagger chance

**Check using DuPont (from fa-returnratios Criterion 4):**
- High NPM + High AT = exceptional (rare, strongest multi-bagger signal)
- Low NPM + Very High AT = volume/efficiency model (Dixon, D-Mart type) → strong
- High NPM + Low AT = premium brand model → good but watch for competition entry
- Low NPM + Low AT = no moat → 🔴

**Screening verdict:**
- Strong margins relative to industry + high asset turnover → 🟢
- Good margins OR good asset turnover (not both) → 🟡
- Below-industry margins with no asset turnover advantage → 🔴

---

### Criterion 6: Prudent Capital Allocation (ROIC)

**Source:** fa-returnratios (ROCE), fa-cashflow (FCF), fa-balancesheet (debt)

**Check:** Does management follow prudent capital allocation policy?

**Money Purse framework:**
- "If ROIC number is strong, then it's conservative management following prudent capital allocation"
- Companies generating strong free cash flows use them for: (a) future growth, OR (b) dividends
- Negative example: Anil Ambani Group — "invested in various sectors without proper plan → collapse → shareholder wealth destroyed"

**What to check:**
1. ROCE consistently > 15% (from fa-returnratios) → capital well-deployed
2. FCF consistently positive and growing (from fa-cashflow) → cash generation strong
3. Debt is zero or manageable (from fa-balancesheet) → conservative
4. No wasteful diversification into unrelated businesses

**Screening verdict:**
- ROCE > 15% + growing FCF + low debt → 🟢 (prudent allocator)
- ROCE 10-15% + adequate FCF → 🟡
- ROCE < 10% OR consistently negative FCF OR high/rising debt → 🔴

---

### Criterion 7: Valuation Attractiveness

**Source:** fa-valuation (all 7 criteria)

**Check:** Is the stock at an attractive valuation for multi-bagger entry?

**Money Purse insight:**
- "Valuations plays very important role. To earn multi-bagger return, valuation should be attractive."
- "Valuation doesn't mean only P/E... DCF is the best thing"
- Monopoly business euphoria example: High P/E stocks fell when competition entered → investors locked in
- "After the market becomes aware of valuations, it will have already been re-rated"

**Key principle:** Identify good businesses at attractive valuations BEFORE the market re-rates them.

**Screening verdict:**
- Valuation phase verdict 🟢 (attractive across metrics) → 🟢 (multi-bagger entry zone)
- Valuation phase verdict 🟡 (fair) → 🟡 (limited multi-bagger margin)
- Valuation phase verdict 🔴 (expensive) → 🔴 (multi-bagger potential already priced in)

---

### Criterion 8: Variant Perception Potential

**Source:** All preceding phases, market sentiment assessment

**Check:** Is there a gap between current market perception and actual/improving fundamentals?

**Money Purse insight:**
- "Sometimes there will be a negative image about the management or business. But over time, as earnings increase, the perception will change."
- "When perception changes, the company undergoes P/E re-rating. We will make a lot of money on that P/E re-rating."
- Tata Elxsi example: initially negative perception → perception changed → 10-bagger return
- This is where the BIGGEST multi-bagger returns come from

**What to check:**
1. Is there currently negative sentiment about the company/management/sector?
2. Are fundamentals actually improving (earnings, margins, debt reduction)?
3. Is the negative sentiment overdone relative to improving reality?
4. Is the market ignoring early signs of turnaround?

**Screening verdict:**
- Negative perception + improving fundamentals + attractive valuation → 🟢 (high multi-bagger potential — variant perception play)
- Neutral perception + good fundamentals → 🟡 (steady compounder, not explosive)
- Positive perception already (market darling) → 🟡 (re-rating already done)
- Negative perception + deteriorating fundamentals → 🔴 (legitimately bad, not variant perception)

---

### Criterion 9: Low Free Float Catalyst

**Source:** fa-valuation-agent (market cap, outstanding shares), fa-management (promoter holding)

**Check:** Is the free float low enough to amplify returns when earnings grow?

**Money Purse insight:**
- "When free float is low and demand increases, we see exponential growth in stocks"
- Free float = shares available for daily trading (total - promoter locked - institutional locked)
- Low free float + earnings growth = "double engine edge" → exponential price growth
- **Warning:** "Low free float will play in reverse — when earnings decline and free float is low, stock falls even further"

**Thresholds:**
- Free float < 25% of total shares → very low (high amplification potential) → 🟢 (if earnings growing)
- Free float 25-40% → moderate → 🟡
- Free float > 40% → high float → less amplification effect → neutral (not negative)

**Screening verdict:**
- Low free float + strong earnings growth trajectory → 🟢 (catalyst present)
- Moderate free float → 🟡
- Low free float + declining earnings → 🔴 (amplifies downside)
- High free float → neutral, score based on other factors

---

### Criterion 10: Growth Catalysts & Triggers

**Source:** fa-industry (stage, forces), fa-profitloss (growth), company-specific research

**Check:** Are there identifiable catalysts that could drive multi-fold earnings growth?

**Catalyst types (Money Purse):**
1. **Capacity addition** — company filling existing capacity and adding new capacity with visible demand
2. **Regulatory edge** — "China Plus One" strategy, PLI scheme, import duty protection benefiting the company
3. **Acquisitions** — Minda Industries example: international acquisitions gave product edge + business growth
4. **Demerger / Value Unlocking** — small companies under large companies don't get right valuation → demerger → re-rating (Neil Bahul interview reference)
5. **Small-cap industry leader** — niche leader moving from small-cap → mid-cap → large-cap journey
6. **Product demand shift** — structural demand increase for the company's products/services

**Screening verdict:**
- 2+ clear catalysts identified with visible execution path → 🟢
- 1 catalyst with some uncertainty → 🟡
- No identifiable catalyst or catalysts are already priced in → 🔴

---

## Aggregating the Multi-bagger Score

After completing all 10 criteria:

1. Count: Greens, Ambers, Reds
2. Apply override rules:
   - If Criterion 1 (Moat) is Red → multi-bagger potential is very low regardless
   - If Criterion 4 (Earnings Sustainability) is Red → not a real multi-bagger candidate
   - If Criterion 7 (Valuation) is Red AND Criterion 8 (Variant Perception) is also Red → already priced in, no multi-bagger path
3. Otherwise:
   - 7+ Green → **Strong Multi-bagger Candidate** — high conviction
   - 5-6 Green, ≤2 Red → **Moderate Multi-bagger Potential** — needs monitoring
   - 3-4 Green → **Low Multi-bagger Potential** — may be a steady compounder but not explosive
   - <3 Green OR 4+ Red → **Not a Multi-bagger Candidate** — may still be a fine investment, just not a multi-bagger

## Output Format

```
MULTI-BAGGER SCREENING: [Company Name] ([Ticker])

| # | Criterion | Assessment | Verdict |
|---|-----------|-----------|---------|
| 1 | Durable Competitive Edge | [Type of moat, durability] | 🟢/🟡/🔴 |
| 2 | Management Quality | [Integrity + Skillset summary, exceptions if any] | 🟢/🟡/🔴 |
| 3 | Promoter Holding Value | [Value: Rs.X cr, primary interest?] | 🟢/🟡/🔴 |
| 4 | Sustainable Earnings Growth | [CAGR, sustainability drivers] | 🟢/🟡/🔴 |
| 5 | Margins + Asset Turnover Moat | [DuPont pattern, vs industry] | 🟢/🟡/🔴 |
| 6 | Prudent Capital Allocation | [ROCE, FCF, debt summary] | 🟢/🟡/🔴 |
| 7 | Valuation Attractiveness | [Valuation phase verdict] | 🟢/🟡/🔴 |
| 8 | Variant Perception | [Perception gap assessment] | 🟢/🟡/🔴 |
| 9 | Low Free Float Catalyst | [Free float %, direction] | 🟢/🟡/🔴 |
| 10 | Growth Catalysts | [Key triggers identified] | 🟢/🟡/🔴 |

Multi-bagger Score: [X/10 Green]
Multi-bagger Verdict: Strong Candidate / Moderate Potential / Low Potential / Not a Candidate

Key Multi-bagger Drivers:
- [List the strongest 🟢 factors]

Key Multi-bagger Risks:
- [List the 🔴 factors that could prevent multi-bagger returns]

Time Horizon: [Based on catalysts — estimated years for potential to play out]
```
