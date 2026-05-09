---
name: fa-industry-forces
description: This skill should be used when evaluating competitive forces for an NSE stock's industry, analyzing "competitive rivalry", "threat of new entrants", "substitute products", "supplier bargaining power", "buyer bargaining power", "entry barriers", "government protection", "Porter's five forces", "industry moat analysis", "PLI scheme benefit", "import duty protection", or when the fa-industry sub-master skill needs the forces analysis. Produces 7-point verdict with Favorable/Neutral/Unfavorable per force.
version: 1.0.0
---

# FA Industry Forces — Leaf Skill

Apply the 7-point industry forces checklist to produce a structured Favorable / Neutral / Unfavorable verdict per force. The 7 forces are Porter's 5 original forces + an Entry Barriers synthesis + India-specific Government Protection force.

## Input Required

fa-industry-research-agent findings (Porter's data section):
- Supplier concentration data
- Buyer type and concentration data
- Identified substitutes
- Entry barrier assessment
- Government schemes / protection measures
- Recent new entrants
- Competitive landscape (players + market share)

---

## The 7-Point Forces Checklist

Work through each force. State the evidence, apply thresholds, and assign Favorable / Neutral / Unfavorable.

---

### Force 1: Competitive Rivalry

**What to assess:**
- Number and relative size of competitors
- Product differentiation vs commodity
- Pricing behavior: discipline vs price wars
- Presence of large unorganized sector competing on price

**Favorable (for the company):**
- 2-3 dominant players with history of rational pricing
- Differentiated products (brand, quality, service) rather than commodity
- Industry growing faster than combined capacity additions (no need to fight for share)
- Unorganized sector declining (GST formalization ongoing)

**Neutral:**
- Moderate competition; occasional price pressure but not structural
- Mixed product portfolio (differentiated + commodity)

**Unfavorable:**
- Many players of similar scale → chronic price competition
- Pure commodity product; buyer decision = lowest price
- Overcapacity in the sector → desperate pricing
- Large unorganized sector actively competing on price

---

### Force 2: Threat of New Entrants

**What to assess:**
- Capital intensity to reach competitive scale
- Regulatory barriers (licenses, approvals)
- Brand equity and distribution network build time
- Technology or IP barriers
- Any recent large-cap or conglomerate entry announcements

**Favorable (high barriers):**
- >₹500 cr capex required to reach minimum viable scale
- Regulatory license with limited issuance (RBI, IRDAI, spectrum)
- Brand loyalty requiring 5+ years of advertising to replicate
- Distribution network depth impossible to replicate quickly (rural FMCG)
- Technology/IP protection

**Neutral:**
- Moderate capital and time to enter, but no structural impossibility
- Smaller new entrants are possible but sub-scale

**Unfavorable (low barriers):**
- Low capital requirements, no regulatory licensing
- Digital-native business model anyone can copy
- Customer switching cost is near zero
- Well-funded conglomerate or PE-backed player recently entered/announced entry

**India-specific:** Reliance, Tata, Adani entering a sector = automatic Unfavorable for Force 2. Their distribution, capital, and political access remove typical barriers.

---

### Force 3: Threat of Substitutes

**What to assess:**
- Does a fundamentally different product/service that serves the same need exist or is emerging?
- What is the timeline for substitution to become meaningful?
- How fast is customer adoption of the substitute?

**Favorable:**
- No viable substitute at comparable price/performance
- Substitute exists theoretically but has no momentum in the market
- High switching cost or infrastructure lock-in prevents substitution

**Neutral:**
- Substitute exists and is growing, but from a very small base (3-7 year horizon)
- Partial substitution (not full category replacement)

**Unfavorable:**
- Substitute is actively displacing the product NOW (volume already declining)
- Substitute has price parity and performance parity
- Generational preference shift actively underway
- Regulatory mandate driving substitution (ICE phase-out, plastic ban)

**Timeline note:** Always specify the horizon — "Unfavorable" for a 15-year horizon is a very different risk than "Unfavorable" in a 3-year horizon.

---

### Force 4: Supplier Bargaining Power

**What to assess:**
- Concentration of input suppliers
- Whether input is a commodity or specialty
- Switching cost to change supplier
- Geopolitical / China dependency risk

**Favorable (low supplier power):**
- Input is a commodity traded on exchanges (copper, aluminum, crude derivatives) — price is market-determined, not supplier-imposed
- Many competing suppliers for all key inputs
- Company is a large enough buyer to negotiate volume discounts
- Backward integration possible or already partially done

**Neutral:**
- Mix of commodity and specialty inputs; manageable price risk

**Unfavorable (high supplier power):**
- Key input has only 2-3 global suppliers (specialty APIs, certain rare metals)
- China is the dominant source for a critical input, with geopolitical risk
- High switching cost (USFDA re-approval for pharma API source change)
- Long lead times for input sourcing make spot market unavailable

---

### Force 5: Buyer Bargaining Power

**What to assess:**
- Concentration of customers
- Switching cost for buyers
- Whether buyer has alternatives readily available
- B2C vs B2B vs Government buyer mix

**Favorable (low buyer power):**
- Retail consumer (B2C): millions of individual buyers with no individual leverage
- Strong brand pull: consumers ask for the brand, retailers must stock it
- High switching cost: proprietary system, habit, or relationship lock-in
- Company's product is a small % of buyer's total spend (not worth negotiating)

**Neutral:**
- Mix of B2C and B2B; moderate concentration; some price sensitivity

**Unfavorable (high buyer power):**
- Large institutional buyers: government tenders, large infrastructure companies
- Commodity-grade product: buyer can easily switch between sellers
- Modern trade retailers (Reliance, D-Mart) negotiating hard (FMCG companies)
- Export revenue to regulated Western markets (US pharma pricing pressure)

---

### Force 6: Entry Barriers (Synthesized)

Aggregate assessment combining Forces 1-5 signals with additional barriers not captured above.

**Barrier categories:**
| Barrier Type | Present? | Strength |
|-------------|----------|---------|
| Capital intensity | Y/N | High/Medium/Low |
| Regulatory license | Y/N | High/Medium/Low |
| Brand equity | Y/N | High/Medium/Low |
| Distribution depth | Y/N | High/Medium/Low |
| Technology / IP | Y/N | High/Medium/Low |
| Geographic / Resource | Y/N | High/Medium/Low |

**Overall Entry Barrier Verdict:**
- **Strong**: 3+ barrier types at medium-to-high strength → Favorable
- **Moderate**: 1-2 barrier types → Neutral
- **Weak**: No significant barrier → Unfavorable

---

### Force 7: Government Protection / Policy

This force is unique to the Indian context. Assess the **net** impact of government policy on the company's competitive position.

**Favorable (government acting as tailwind/protector):**
- PLI (Production Linked Incentive) scheme eligibility: direct ₹ benefit for domestic production
- Import duty protection: customs duty makes foreign competition expensive (e.g., wires, some FMCG categories)
- Mandatory domestic procurement (defense, railways)
- Make-in-India / Aatmanirbhar Bharat explicit beneficiary
- RBI/IRDAI licensing as moat (financial services)
- Government infrastructure spending as demand driver (cables for power grid, cement for highways)

**Neutral:**
- Minimal direct government policy impact
- Some regulation but it applies equally to all players

**Unfavorable (government acting as headwind):**
- Price controls (DPCO for pharma, regulated tariffs for utilities)
- Government is primary buyer with long payment cycles and tender-based revenue
- Regulatory cost compliance mandates increasing
- Import duty reduction making foreign competition cheaper (periodic policy risk)
- Environmental / labor compliance mandates adding cost

**Combined net verdict:**
- Net Favorable: Tailwinds outweigh headwinds → Favorable
- Mixed or minimal: Neutral
- Net Unfavorable: Headwinds outweigh tailwinds → Unfavorable

---

## Aggregating the Forces Verdict

After completing all 7:

| Favorable Count | Verdict |
|----------------|---------|
| 5-7 Favorable | 🟢 Attractive industry structure |
| 3-4 Favorable | 🟡 Average industry structure |
| 0-2 Favorable | 🔴 Structurally challenging industry |

**Override rule:** If Force 3 (Substitutes) is Unfavorable with a <5 year horizon, or if competitive rivalry is severe with visible margin destruction, note as a **Structural Risk** regardless of overall count.

## References

- **`references/barriers-criteria.md`** — Detailed entry barrier criteria with India-specific examples, PLI scheme list, and import duty reference by sector
