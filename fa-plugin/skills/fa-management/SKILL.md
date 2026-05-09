---
name: fa-management
description: This skill should be used when evaluating the management quality of an NSE stock, assessing "management integrity", "promoter quality", "management remuneration", "director background", "capital allocation track record", "management red flags", or when the fa-orchestrator has reached the management analysis phase. This is the sub-master skill that delegates to fa-mgmt-integrity and fa-mgmt-skillset leaf skills.
version: 1.0.0
---

# FA Management — Sub-Master Skill

The management sub-master coordinates the two pillars of management evaluation: Integrity (character, ethics, governance) and Skillset (competence, execution, strategy). Both are equally important — a skilled but dishonest management is dangerous; an honest but incompetent management destroys value slowly.

## Framework Origin

The management analysis framework is primarily derived from **Dr. Vijay Malik's** value investing methodology. Dr. Malik is one of India's most respected independent equity analysts. His framework focuses on identifying and avoiding management red flags before any financial analysis. See `references/vijay-malik-framework.md` for the full expanded framework.

## Two Sub-Analyses

### 1. Management Integrity (10 criteria)
Delegated to: `fa-mgmt-integrity` leaf skill

Covers ethical and governance standards:
- Remuneration structure
- Related party transactions
- Promoter track record (criminal/regulatory)
- Communication integrity (media, statements)
- Personnel changes (CFO, auditors)
- Pledging and Sujata Dalal watchlist

**Data needed from agents:**
- Agent 1 (remuneration) findings: pay %, RPT data, trend
- Agent 2 (news) findings: CFO/auditor changes, pledging, media
- Agent 3 (promoter) findings: background, SEBI records, Sujata Dalal

### 2. Management Skillset (4 criteria)
Delegated to: `fa-mgmt-skillset` leaf skill

Covers competence and execution:
- Qualifications and sector experience
- Growth mindset and execution follow-through
- Capital allocation discipline
- Succession planning

**Data needed from agents:**
- Agent 3 (promoter) findings: background, qualifications
- Agent 2 (news) findings: management interviews, analyst day transcripts

## Analysis Protocol

### Step 1: Compile Agent Findings
Organize the three management agent outputs into a structured data packet:

```
MANAGEMENT DATA PACKET for [Company] ([Ticker])
────────────────────────────────────────────────
Remuneration Data (Agent 1):
  - Director pay total: ₹X cr
  - PAT: ₹Y cr
  - Pay as % PAT: Z%
  - RPT summary: [list]
  - Anomalies: [list or "None found"]

News / Events Data (Agent 2):
  - CFO changes: [date, reason if available]
  - Auditor changes: [date, reason]
  - Pledging: X% as of [date], trend: [stable/increasing/decreasing]
  - Media appearances: [assessment]
  - Regulatory notices: [list or "None found"]

Promoter Data (Agent 3):
  - Key promoters: [Name, Generation, Qualification, Experience]
  - SEBI/legal records: [findings or "None found"]
  - Sujata Dalal / Moneylife flag: [Yes/No + link if Yes]
```

### Step 2: Run Integrity Analysis
Load and apply the `fa-mgmt-integrity` skill checklist (10 criteria) using the data packet above. Assign 🟢/🟡/🔴 for each criterion.

### Step 3: Run Skillset Analysis
Load and apply the `fa-mgmt-skillset` skill checklist (4 criteria). For second-generation promoters, also load `fa-mgmt-skillset/references/second-gen-criteria.md`.

### Step 4: Aggregate Management Verdict

| Score | Overall Verdict |
|-------|----------------|
| 0 Red flags, ≤2 Amber | 🟢 Strong management |
| 1 Red flag OR 3-4 Amber | 🟡 Acceptable with caveats |
| 2+ Red flags OR 5+ Amber | 🔴 Serious management concerns |

A single 🔴 in Integrity (especially criteria 4 — criminal record, or 10 — Sujata Dalal) automatically elevates the overall Management verdict to 🔴 regardless of other scores.

## Key Principles

- **Never skip integrity analysis** in favor of compelling financials. Bad management with good numbers is a time bomb (Satyam, DHFL).
- **Weight integrity above skillset.** A moderately skilled honest management is better than a highly skilled dishonest one.
- **Second-generation transitions** require special scrutiny. The founding generation's success does not automatically transfer to their children.
- **Data limitations are not the same as clean record.** If data on a small-cap promoter's background is unavailable, note "Unable to verify" rather than marking 🟢.

## References

- **`references/vijay-malik-framework.md`** — Complete Dr. Vijay Malik management analysis framework with expanded explanations for each criterion
