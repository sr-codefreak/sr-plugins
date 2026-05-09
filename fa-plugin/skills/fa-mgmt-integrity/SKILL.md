---
name: fa-mgmt-integrity
description: This skill should be used when evaluating management integrity of an NSE-listed company, checking "promoter pledging", "management remuneration percentage", "director pay", "related party transactions", "auditor resignation", "CFO resignation", "promoter fraud history", "SEBI action against promoter", "Sujata Dalal list check", "auditor fees abnormal", "management egoistic", or when the fa-management sub-master skill has reached the integrity evaluation step. Applies a 10-point checklist to assign RAG verdicts.
version: 1.0.0
---

# FA Management Integrity — Leaf Skill

Apply the 10-point management integrity checklist. For each criterion: state the finding, cite the source, and assign a RAG verdict (🟢/🟡/🔴/⬜).

## Input Required

Before starting, confirm availability of the management data packet from:
- fa-mgmt-remuneration-agent: remuneration %, RPT data
- fa-mgmt-news-agent: CFO/auditor changes, pledging, media
- fa-mgmt-promoter-agent: background, SEBI, Sujata Dalal

If any agent data is missing, note "Data unavailable — unable to verify" for affected criteria rather than assuming clean.

## The 10-Point Integrity Checklist

Work through each criterion in order. For each criterion:
1. State the specific evidence found
2. Apply the threshold rules below
3. Assign RAG status
4. Note the source URL or filing reference

---

### Criterion 1: Management Remuneration <5% of PAT

**Data source:** fa-mgmt-remuneration-agent
**Calculation:** Total director remuneration (₹ cr) ÷ PAT (₹ cr) × 100

**Thresholds:**
- <5% → 🟢
- 5–10% → 🟡 (note if PAT is temporarily depressed)
- >10% → 🔴
- Family member high-pay with vague role → 🔴 (regardless of total %)

**Note:** Use last full financial year. If PAT was unusually low (one-off write-down etc.), also calculate on a 3-year average PAT.

---

### Criterion 2: No Unjustified Family Member Salaries

**Data source:** fa-mgmt-remuneration-agent (RPT section, KMP list)
**Check:** Are promoter relatives on payroll? Are their roles and experience clearly stated?

**Thresholds:**
- No family on payroll, or family with clear relevant roles → 🟢
- Family with listed roles but unclear experience → 🟡
- Family with vague roles or disproportionate pay → 🔴

---

### Criterion 3: Related Party Transactions — No Abnormalities

**Data source:** fa-mgmt-remuneration-agent (RPT data)
**Check:** RPT/Revenue trend over 3-5 years. Pricing of transactions (arm's length?).

**Thresholds:**
- RPT stable or declining as % revenue, priced at market rates → 🟢
- RPT growing moderately but with clear audit committee documentation → 🟡
- RPT growing significantly, non-arm's-length pricing, or loans to promoter entities → 🔴

---

### Criterion 4: Promoter Clean of Criminal/Regulatory Record

**Data source:** fa-mgmt-promoter-agent (SEBI/legal records)
**Check:** SEBI enforcement orders, SFIO investigation, ED proceedings, criminal cases.

**Thresholds:**
- No adverse records found → 🟢
- Historical minor SEBI notice resolved with small penalty → 🟡
- Active SEBI/SFIO/ED/CBI proceedings → 🔴
- Promoter associated with a previously fraud-implicated company → 🔴

---

### Criterion 5: Media Appearances — Sober and Followed-Up

**Data source:** fa-mgmt-news-agent (media appearances section)
**Check:** Frequency of TV/media appearances. Do past public statements have matching follow-through?

**Thresholds:**
- Infrequent, sober, fact-based communications with demonstrated follow-through → 🟢
- Moderate media presence with mixed follow-through record → 🟡
- Frequent promotional appearances OR pattern of commitments not followed up → 🔴

---

### Criterion 6: No Share Price-Focused Statements

**Data source:** fa-mgmt-news-agent
**Check:** Management statements specifically referencing share price; vague unverifiable announcements.

**Thresholds:**
- No price-targeting statements, operational focus in communications → 🟢
- Occasional forward-looking optimism without price targets → 🟡
- Direct share price commentary, vague order/partnership announcements, price-pumping pattern → 🔴

---

### Criterion 7: No Unexplained CFO/Auditor Resignations

**Data source:** fa-mgmt-news-agent (CFO/auditor changes)
**Check:** Changes in CFO or statutory auditor in last 5 years. Reason given?

**Thresholds:**
- No changes, or changes with clear reasons (mandatory rotation, retirement) → 🟢
- One change with vague reason or coincident with bad period → 🟡
- Multiple CFO changes in 3 years, or mid-term auditor resignation without explanation → 🔴

---

### Criterion 8: Auditor Fees Proportionate to Company Size

**Data source:** fa-mgmt-remuneration-agent or direct AR lookup
**Check:** Audit fees vs revenue. Compare to approximate benchmarks.

**Benchmarks (Revenue → Expected Audit Fees):**
- <₹500 cr → ₹25–75 lakhs
- ₹500–2000 cr → ₹50–150 lakhs
- >₹2000 cr → ₹1–5 cr

**Thresholds:**
- Fees within normal range for company size → 🟢
- Fees slightly elevated (1.5–2× expected) but auditor is Big4 → 🟡
- Fees dramatically above normal without explanation → 🔴
- Fees dramatically below normal for complex company → 🟡 (insufficient scrutiny risk)

---

### Criterion 9: Management Accepts Mistakes / Non-Egoistic

**Data source:** fa-mgmt-promoter-agent + AR review (MD&A section)
**Check:** Compare AR guidance from Year N vs actual performance in Year N+1. Tone of MD&A.

**Thresholds:**
- Acknowledges specific failures with corrective actions stated → 🟢
- Generally optimistic tone but factually accurate to actual outcomes → 🟡
- Pattern of blaming external factors, dismissive of analyst concerns, never acknowledges failure → 🔴

**Note:** This requires reading the MD&A section of at least the last 3 Annual Reports. If not already done, fetch them from BSE.

---

### Criterion 10: Promoter Pledging Acceptable; Not on Sujata Dalal List

**Data source:** fa-mgmt-news-agent (pledging section) + fa-mgmt-promoter-agent (Sujata Dalal check)
**Check:** Current pledging % and trend. Moneylife/Sujata Dalal watchlist.

**Pledging thresholds:**
- 0–25% → 🟢
- 25–50% → 🟡 (assess trend and reason)
- 50–80% → 🔴
- >80% → 🔴 (critical)
- Increasing trend over 4+ quarters → bump up one level (🟢→🟡, 🟡→🔴)

**Promoter Holding VALUE check (Money Purse multi-bagger video):**
- Don't just check holding %. Calculate: Holding % × Market Cap = Promoter Holding Value
- A promoter with 50% in a Rs.1 lakh crore company (= Rs.50,000 cr value) is MORE invested than 75% in a Rs.1,000 crore company (= Rs.750 cr value)
- If promoter has other listed/unlisted companies with significantly larger holdings → this company gets lower priority → flag as 🟡
- Exception: Professional-run companies (ITC, L&T type) with no dominant single promoter → evaluate on professional management quality instead

**Sujata Dalal check:**
- Not mentioned on Moneylife → 🟢 (for this criterion)
- Mentioned negatively on Moneylife → 🔴 (document the article link)

If pledging AND Sujata Dalal flag both present → automatic 🔴 overall integrity verdict.

---

## Aggregating the Integrity Score

After completing all 10 criteria:

1. Count: Greens, Ambers, Reds
2. Apply override rule: Any 🔴 on criterion 4 (criminal/SEBI) or 10 (Sujata Dalal) → **Integrity = 🔴 regardless of other scores**
3. Otherwise:
   - 0 Red, ≤2 Amber → 🟢 Integrity Strong
   - 1 Red OR 3-4 Amber → 🟡 Integrity Acceptable with Caveats
   - 2+ Red OR 5+ Amber → 🔴 Serious Integrity Concerns

## References

- **`references/red-flags.md`** — SEBI enforcement action types, Sujata Dalal fraud list context, RPT manipulation patterns, fraud case studies
