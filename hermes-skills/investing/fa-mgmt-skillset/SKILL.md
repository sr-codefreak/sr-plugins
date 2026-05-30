---
name: fa-mgmt-skillset
description: This skill should be used when evaluating management competence and execution quality for an NSE stock, assessing "promoter qualification", "management experience", "second generation promoter", "capital allocation track record", "succession planning", "management execution", "growth mindset", "does management follow through", or when the fa-management sub-master skill has reached the skillset evaluation step. Applies a 4-point checklist.
version: 1.0.0
---

# FA Management Skillset — Leaf Skill

Apply the 4-point management skillset checklist. Competence analysis is distinct from integrity analysis — this section assesses whether management has the skills to execute on its stated strategy, not whether they are honest.

## Input Required

Confirm availability of:
- fa-mgmt-promoter-agent: promoter background, qualifications, generation
- fa-mgmt-news-agent: management interviews, analyst day transcripts, guidance history

Additionally, retrieve the last 3 Annual Reports' MD&A sections if not already in context (from BSE filings).

## When to Load Second-Gen Criteria

If the current MD/CEO is the founder's child (second-generation promoter), load `references/second-gen-criteria.md` for additional depth on the generational transition evaluation.

**How to identify second-gen:** The promoter agent's output will note "Generation: 2nd" if identified. Alternatively, check Annual Report's Director profile section — if the MD's surname matches the founding promoter and the founding year was >20 years ago, they are likely 2nd generation.

---

## The 4-Point Skillset Checklist

---

### Criterion 1: Qualification and Experience in Relevant Field

**What to check:**
Find the MD/CEO/key promoter's educational background and professional experience.
- Is the degree relevant? (e.g., engineering for a manufacturing company, medicine for pharma, finance/CA for NBFC)
- How many years did they work in the industry before taking leadership?
- Did they work at the current company under the previous generation, or parachute in?

**Data source:** fa-mgmt-promoter-agent (promoter profiles section)

**Sources:**
- Annual Report → Corporate Governance → Directors' Profiles
- Company website → About/Leadership page
- LinkedIn (if available)
- News profiles/interviews mentioning background

**Thresholds:**
- Relevant degree + 10+ years industry experience → 🟢
- Relevant degree OR industry experience (not both), but demonstrated learning curve → 🟡
- Unrelated background with no evident industry immersion → 🟡 to 🔴 (depends on how long they've been in the role)
- Second-gen with no clear qualification or experience before joining family business → 🟡 (apply second-gen criteria from references/)

**Note:** A founder with no formal degree but 30 years building the business from scratch is not a concern. Context matters significantly.

---

### Criterion 2: Growth Mindset — Follows Through on Plans

**What to check:**
Compare what management said they would do vs what they actually did.

**Step 1 — Extract guidance:** From the Annual Report MD&A Year N-1 (or Year N-2), identify specific forward-looking statements:
- "We plan to expand capacity by X% in FY__"
- "We are targeting revenue of ₹X cr by FY__"
- "We will launch Product Y in H1 FY__"
- "We are evaluating an acquisition in [segment]"

**Step 2 — Check actuals:** In Year N's AR or quarterly results, check whether these plans materialized.

**Classification of mindset:**
- **Growth/builder mindset**: Actively investing in new capacities, geographies, products; capex growing over time; stated plans generally executed; management learns and adapts when plans change
- **Comfort/extractor mindset**: Business in cruise control; capex flat or falling as % revenue; no new product/market initiatives; management focuses on dividend maximization rather than reinvestment

**Thresholds:**
- Consistent follow-through on specific plans + active investment → 🟢 Growth mindset
- Mixed follow-through with reasonable explanations for changes → 🟡
- Repeated commitments unmet + no reinvestment + high dividend extraction → 🔴 Comfort/extractive mindset

**Note:** Some industries (FMCG, utilities) are inherently slow-growth and dividend-focused — this is not a red flag. Judge against industry norms.

---

### Criterion 3: Capital Allocation — Long-Term, ROCE-Focused

**What to check:**
How has management deployed profits and capital over the last 5 years? Is the pattern consistent with long-term value creation?

**Capital allocation hierarchy (best to worst):**
1. Reinvestment in core business at high incremental ROCE → Best
2. Return to shareholders via dividends / buybacks → Good (if business is mature, no high-ROCE reinvestment available)
3. Adjacent expansion with clear strategic rationale → Acceptable
4. Acquisitions at reasonable valuations → Acceptable
5. Acquisitions at inflated valuations → Concern
6. Diversification into unrelated areas → Red flag
7. Inter-company loans or advances to promoter entities → Red flag

**How to assess (without financial ratios — Phase 1 only):**
- Review capex pattern in last 5 Annual Reports: is there consistent capacity investment?
- Review any large acquisitions: was the rationale stated and does it appear logical?
- Check if management returned capital during periods of low organic reinvestment opportunity (good discipline)
- Check if the company took on debt for diversification into unrelated areas

**Thresholds:**
- Disciplined, core-business-focused capex + no unrelated diversification → 🟢
- Some adjacent expansion with mixed results but logical rationale → 🟡
- Large acquisition at high valuation, unrelated diversification, or capital to promoter entities → 🔴

---

### Criterion 4: Succession Planning

**What to check:**
Is there a clear next-in-command? Is the company's fate tied to a single individual?

**Why it matters:**
Concentration of decision-making in one person (especially founder/family) creates key-person risk. If that person exits suddenly (health, legal, conflict), the company has no clear leadership path.

**How to assess:**
- Annual Report → Corporate Governance → Board composition
  - Is there a COO, Deputy MD, or Executive Director clearly positioned as next-in-line?
  - Are key management positions (CFO, CTO, CMO) held by professional non-family managers?
- Company communications → Is only one person speaking for the company (all investor presentations, all media)?
- Is the board meaningfully independent (not all family/friends)?

**Thresholds:**
- Clear professional management layer below the MD; strong board → 🟢
- Single dominant leader but competent professional management layer → 🟡 (concentration risk noted)
- Entire senior leadership is family; no visible succession path → 🔴

---

## Aggregating the Skillset Score

| Score | Verdict |
|-------|---------|
| 3–4 Green | 🟢 Strong management skillset |
| 2 Green, rest Amber | 🟡 Adequate skillset, specific gaps noted |
| Any Red, or majority Amber | 🔴 Skillset concerns |

---

## References

- **`references/second-gen-criteria.md`** — Load this when the key promoter is the founder's child (second-generation). Contains additional evaluation depth specific to generational transitions.
