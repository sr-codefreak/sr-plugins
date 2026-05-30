#!/usr/bin/env python3
"""
FA PDF Generator V2 — extends V1 with Parts C-H + Overall Verdict coverage.

V1 covered: Cover, Exec Summary, Mgmt People, Mgmt Tables (A1+A2), Industry (B1+B2), Data Sources.
V2 adds: Financial Health Dashboard, Balance Sheet (C), P&L (D), Cash Flow (E),
         Return Ratios (F), Valuation (G), Multi-bagger Screening (H), Final Verdict.

Usage: python3 scripts/generate_fa_pdf_v2.py <input.md> <output.pdf>
"""

import logging
import re
import sys
from pathlib import Path

# Reuse all V1 helpers (parsers, image scraping, Chrome PDF, etc.)
from generate_fa_pdf import (
    RAG_CSS,
    SCRIPT_DIR,
    fetch_company_logo,
    html_to_pdf,
    load_website_url,
    log,
    make_initials_svg,
    parse_report as parse_v1_report,
    parse_score,
    parse_table_rows,
    scrape_headshots,
    scrape_product_images,
    strip_bold,
    MAX_HEADSHOTS,
)

import jinja2

TEMPLATE_PATH = SCRIPT_DIR / "templates/fa_report_v2.html"


# ── Section helpers ────────────────────────────────────────────────────────────

def get_section(md: str, heading: str) -> str:
    parts = re.split(r"^## ", md, flags=re.MULTILINE)
    for part in parts:
        if part.strip().startswith(heading):
            return part
    return ""


def get_subsection(text: str, heading: str) -> str:
    parts = re.split(r"^### ", text, flags=re.MULTILINE)
    for part in parts:
        if part.strip().startswith(heading):
            return part
    return ""


def parse_data_meta(text: str) -> dict:
    """Extract '**Data as of:** ...' and '**Source:** ...' lines from a section."""
    date_m = re.search(r"\*\*Data as of:\*\*\s*(.+)", text)
    src_m = re.search(r"\*\*Source:\*\*\s*(.+)", text)
    return {
        "data_date": date_m.group(1).strip() if date_m else "",
        "data_source": src_m.group(1).strip() if src_m else "",
    }


def parse_callout_items(text: str, heading_pattern: str, limit: int = 6) -> list:
    """Find a `**Key X Concerns/Strengths:**` block and return its bulleted items."""
    m = re.search(
        rf"\*\*{heading_pattern}\*\*\s*\n(.*?)(?=\n\*\*|\n###|\n---|\Z)",
        text, re.DOTALL,
    )
    if not m:
        return []
    items = []
    for line in m.group(1).splitlines():
        s = line.strip()
        if s.startswith("-"):
            items.append(strip_bold(s.lstrip("-").strip())[:280])
    return items[:limit]


def parse_dimension_rows(text: str, overall_label: str) -> dict:
    """
    Parse the trailing 3-col dimension table that ends with the **<Section> Overall** row.

    Returns dict with rows: list[{name, score, verdict}], overall_score, overall_verdict.
    """
    # Find the table block — it appears after `### <Section> Overall`
    block_m = re.search(
        rf"### {re.escape(overall_label)}\s*\n(.*?)(?=\n---|\n##|\Z)",
        text, re.DOTALL,
    )
    block = block_m.group(1) if block_m else text

    rows = []
    overall_score = ""
    overall_verdict = "🟡"

    for m in re.finditer(
        r"^\|\s*([^|*\-][^|]+?|\*\*[^|]+?\*\*)\s*\|\s*([^|]+?)\s*\|\s*(.+?)\s*\|",
        block, re.MULTILINE,
    ):
        name, score, verdict = m.group(1).strip(), m.group(2).strip(), m.group(3).strip()
        if "Dimension" in name or "---" in name:
            continue
        is_overall = name.startswith("**") and "Overall" in name
        clean_name = strip_bold(name)
        clean_verdict = strip_bold(verdict)
        if is_overall:
            overall_score = score
            # Try to extract just the emoji from the verdict cell
            v_emoji = re.search(r"(🟢|🟡|🔴|⬜)", clean_verdict)
            overall_verdict = v_emoji.group(1) if v_emoji else clean_verdict
        else:
            v_emoji = re.search(r"(🟢|🟡|🔴|⬜)", clean_verdict)
            rows.append({
                "name": clean_name,
                "score": score[:80],
                "verdict": v_emoji.group(1) if v_emoji else clean_verdict,
            })
    return {
        "rows": rows,
        "overall_score": overall_score,
        "overall_verdict": overall_verdict,
    }


def parse_financial_section(md: str, part_letter: str, sub_id: str,
                            total_points: int, label: str,
                            concerns_heading: str, strengths_heading: str,
                            overall_label: str) -> dict:
    """Generic parser for Parts C, D, E, F (and base for G)."""
    section = get_section(md, f"PART {part_letter}")
    sub = get_subsection(section, sub_id) or section

    meta = parse_data_meta(section)
    rows = parse_table_rows(sub)
    score = parse_score(sub, total_points)
    concerns = parse_callout_items(sub, concerns_heading)
    strengths = parse_callout_items(sub, strengths_heading)

    dim_data = parse_dimension_rows(section, overall_label)

    return {
        "data_date": meta["data_date"],
        "data_source": meta["data_source"],
        "rows": rows,
        "score": score,
        "concerns": concerns,
        "strengths": strengths,
        "dimensions": dim_data["rows"],
        "overall_score": dim_data["overall_score"] or f"{score['green']}/{total_points}",
        "overall_verdict": dim_data["overall_verdict"],
    }


def parse_valuation(md: str) -> dict:
    """Part G — Valuation. Extends financial_section with CMP, market cap, banner, multiples."""
    section = get_section(md, "PART G")
    base = parse_financial_section(
        md, "G", "G1", 7, "Valuation",
        "Key Valuation Concerns", "Key Valuation Strengths", "Valuation Overall",
    )

    # Header line: `**CMP:** Rs.7,808 | **Market Cap:** Rs.66,591 cr`
    cmp_m = re.search(r"\*\*CMP:\*\*\s*(?:Rs\.?|₹)?\s*([\d,]+)", section)
    mc_m = re.search(r"\*\*Market Cap:\*\*\s*(?:Rs\.?|₹)?\s*([\d,]+)", section)
    base["cmp"] = cmp_m.group(1).strip() if cmp_m else ""
    base["market_cap"] = mc_m.group(1).strip() if mc_m else ""

    # Pull the first 4 multiples from the rows for the highlight grid
    multiples = []
    multiple_keys = [
        ("P/E Ratio",      r"P/E:?\s*([\d.,]+x?)",       r"sector(?:\s*median)?\s*P/E:?\s*~?([\d.,]+x?)"),
        ("P/B Ratio",      r"P/B:?\s*([\d.,]+x?)",       r"peer[s]?:?[^.]*?([\d.,]+x?)"),
        ("EV/EBITDA",      r"EV/EBITDA:?\s*([\d.,]+x?)", r"sector:?[^.]*?([\d.,]+x?)"),
        ("Price/Sales",    r"P/S:?\s*([\d.,]+x?)",       r"peer[s]?:?[^.]*?([\d.,]+x?)"),
    ]
    for label, val_re, peer_re in multiple_keys:
        for r in base["rows"]:
            blob = r["col2"] + " " + r["col3"]
            vm = re.search(val_re, blob)
            if vm:
                pm = re.search(peer_re, blob, re.IGNORECASE)
                multiples.append({
                    "label": label,
                    "value": vm.group(1),
                    "peer": f"peer ~{pm.group(1)}" if pm else "",
                })
                break
    base["multiples"] = multiples[:4]

    # Banner: did all metrics flash red?
    if base["score"]["red"] >= 5:
        base["banner_text"] = "Stock is priced for perfection — extremely expensive on every measure"
        base["banner_sub"] = f"{base['score']['red']} of {base['score']['red'] + base['score']['amber'] + base['score']['green']} valuation criteria are Red"
    elif base["score"]["green"] >= 5:
        base["banner_text"] = "Valuation looks reasonable across most measures"
        base["banner_sub"] = ""
    else:
        base["banner_text"] = ""
        base["banner_sub"] = ""

    # Context callout — pull from "Valuation Context:" block
    ctx_m = re.search(
        r"\*\*Valuation Context:\*\*\s*\n(.*?)(?=\n\*\*|\n###|\n---|\Z)",
        section, re.DOTALL,
    )
    base["context"] = []
    if ctx_m:
        for line in ctx_m.group(1).splitlines():
            s = line.strip()
            if s.startswith("-"):
                base["context"].append(strip_bold(s.lstrip("-").strip())[:260])
        base["context"] = base["context"][:5]

    return base


def parse_multibagger(md: str) -> dict:
    """Part H — Multi-bagger Screening (10-point + drivers/risks + verdict + horizon)."""
    section = get_section(md, "PART H")
    sub = get_subsection(section, "H1") or section

    rows = parse_table_rows(sub)
    score = parse_score(sub, 10)

    # Verdict text & candidate flag
    v_m = re.search(r"\*\*Multi-bagger Verdict:\*\*\s*(.+)", sub)
    verdict_text = v_m.group(1).strip().rstrip("*") if v_m else ""
    is_candidate = bool(re.search(r"\bcandidate\b", verdict_text, re.IGNORECASE)) \
                   and not re.search(r"\bnot\b.*\bcandidate\b", verdict_text, re.IGNORECASE)

    drivers = parse_callout_items(sub, "Key Multi-bagger Drivers")
    risks = parse_callout_items(sub, "Key Multi-bagger Risks")

    th_m = re.search(r"\*\*Time Horizon:\*\*\s*(.+)", sub)
    time_horizon = th_m.group(1).strip().rstrip("*") if th_m else ""

    return {
        "rows": rows,
        "score": score,
        "verdict_text": verdict_text or ("Multi-bagger Candidate" if is_candidate else "Not a Multi-bagger Candidate"),
        "is_candidate": is_candidate,
        "drivers": drivers,
        "risks": risks,
        "time_horizon": time_horizon,
    }


def parse_overall_verdict_v2(md: str) -> dict:
    """
    Parse the OVERALL VERDICT section's summary table:
      | Dimension | Verdict |
      ... 10 dimension rows ...
      | **OVERALL** | **MONITOR** |
    Plus: Top 3 Risks, Top 3 Positives, Recommended Next Step, Entry Triggers.
    """
    section = get_section(md, "OVERALL VERDICT")

    rows = []
    overall_text = "MONITOR"
    overall_emoji = ""

    table_m = re.search(
        r"\|\s*Dimension\s*\|\s*Verdict\s*\|.*?\n((?:\|.*?\n)+)",
        section, re.DOTALL | re.IGNORECASE,
    )
    if table_m:
        for line in table_m.group(1).splitlines():
            cells = [c.strip() for c in line.strip().strip("|").split("|")]
            if len(cells) < 2 or "---" in cells[0]:
                continue
            name, verdict = cells[0], cells[1]
            is_overall = name.startswith("**") and "OVERALL" in name.upper()
            clean_name = strip_bold(name)
            clean_verdict = strip_bold(verdict)
            if is_overall:
                v_word = re.search(r"(INVEST|MONITOR|AVOID)", clean_verdict, re.IGNORECASE)
                if v_word:
                    overall_text = v_word.group(1).upper()
                e = re.search(r"(🟢|🟡|🔴)", clean_verdict)
                overall_emoji = e.group(1) if e else ""
            else:
                # split detail vs verdict emoji
                e = re.search(r"(🟢|🟡|🔴|⬜)", clean_verdict)
                emoji = e.group(1) if e else ""
                detail = re.sub(r"^[🟢🟡🔴⬜]\s*", "", clean_verdict).strip()
                detail = re.sub(r"^\(|\)$", "", detail)
                rows.append({
                    "name": clean_name,
                    "detail": detail[:200],
                    "verdict": emoji or clean_verdict,
                })

    # Entry triggers
    et_m = re.search(
        r"\*\*Entry triggers to watch for:\*\*\s*\n(.*?)(?=\n\n|\n\*\*|\n##|\n---|\Z)",
        section, re.DOTALL | re.IGNORECASE,
    )
    entry_triggers = []
    if et_m:
        for line in et_m.group(1).splitlines():
            s = line.strip()
            if s.startswith("-"):
                entry_triggers.append(strip_bold(s.lstrip("-").strip())[:260])
        entry_triggers = entry_triggers[:6]

    return {
        "overall_dimensions": rows,
        "overall_verdict": overall_text,
        "overall_verdict_emoji": overall_emoji,
        "entry_triggers": entry_triggers,
    }


# ── Compose extra V2 context ───────────────────────────────────────────────────

def build_financial_pillars(ctx: dict) -> list:
    """Five-up summary cards for the Financial Health dashboard page."""
    pillars = []
    spec = [
        ("C", "Balance Sheet", ctx["balance_sheet"], 10),
        ("D", "P&L",           ctx["pnl"],           10),
        ("E", "Cash Flow",     ctx["cashflow"],       7),
        ("F", "Returns",       ctx["returns"],        7),
        ("G", "Valuation",     ctx["valuation"],      7),
    ]
    for letter, name, sec, total in spec:
        rag = RAG_CSS.get(sec["overall_verdict"], "amber")
        rag_dz = {"green": "good", "amber": "warn", "red": "bad"}.get(rag, "warn")
        green = sec["score"]["green"]
        amber = sec["score"]["amber"]
        red = sec["score"]["red"]
        pillars.append({
            "letter": letter,
            "name": name,
            "score_display": f"{green}/{total}",
            "rag_class": rag,
            "rag_class_dz": rag_dz,
            "verdict": sec["overall_verdict"],
            "tagline": f"{green}G · {amber}A · {red}R",
        })
    return pillars


def build_v2_scorecards(ctx: dict) -> list:
    """8-up scorecard for Executive Summary: 4 qualitative + 4 financial."""
    cards = list(ctx.get("scorecard_cards", []))[:4]  # mgmt-int, mgmt-skill, ind-stage, ind-forces

    fin_specs = [
        ("Balance Sheet", ctx["balance_sheet"], 10),
        ("P&L Health",    ctx["pnl"],           10),
        ("Cash Flow",     ctx["cashflow"],       7),
        ("Valuation",     ctx["valuation"],      7),
    ]
    for label, sec, total in fin_specs:
        cards.append({
            "label": label,
            "value": sec["overall_verdict"],
            "sub": f"{sec['score']['green']}/{total} G · {sec['score']['amber']}A · {sec['score']['red']}R",
            "rag_class": RAG_CSS.get(sec["overall_verdict"], "amber"),
            "rag_class_dz": {"green": "good", "amber": "warn", "red": "bad"}.get(RAG_CSS.get(sec["overall_verdict"], "amber"), "warn"),
        })
    return cards


def build_headline_stats(md: str, ctx: dict) -> list:
    """A row of 4 marquee stats for the Financial dashboard page."""
    stats = []

    def find(pattern, default=""):
        m = re.search(pattern, md)
        return m.group(1).strip() if m else default

    revenue = find(r"Revenue:?\s*Rs\.?([\d,]+\s*cr)")
    de = find(r"D/E:?\s*([\d.]+)")
    roce = find(r"ROCE:?\s*([\d.]+%)")
    pe = find(r"(?:Trailing\s*)?P/E:?\s*([\d.]+x?)")
    ebitda_margin = find(r"EBITDA\s*Margin[^:]*:?\s*([\d.]+%)")

    if revenue: stats.append({"label": "Revenue (FY25)",   "value": revenue, "sub": "", "rag_class": "green"})
    if de:      stats.append({"label": "Debt / Equity",    "value": de,      "sub": "Virtually debt-free" if float(de or 0) < 0.1 else "", "rag_class": "green" if float(de or 0) < 0.5 else "amber"})
    if ebitda_margin: stats.append({"label": "EBITDA Margin", "value": ebitda_margin, "sub": "", "rag_class": "green"})
    if roce:    stats.append({"label": "ROCE",             "value": roce,    "sub": "", "rag_class": "green" if float(roce.rstrip('%') or 0) >= 15 else "amber"})
    if pe and len(stats) < 4:  stats.append({"label": "P/E (TTM)", "value": pe, "sub": "", "rag_class": "red" if float(pe.rstrip('x') or 0) > 50 else "green"})

    # Add Dezerv RAG class mapping
    _map = {"green": "good", "amber": "warn", "red": "bad"}
    for s in stats:
        s["rag_class_dz"] = _map.get(s.get("rag_class", "green"), "good")

    return stats[:4]


# ── Main parse pipeline ────────────────────────────────────────────────────────

def parse_report_v2(md: str) -> dict:
    ctx = parse_v1_report(md)

    # Parts C-H
    ctx["balance_sheet"] = parse_financial_section(
        md, "C", "C1", 10, "Balance Sheet",
        "Key Balance Sheet Concerns", "Key Balance Sheet Strengths",
        "Balance Sheet Overall",
    )
    ctx["pnl"] = parse_financial_section(
        md, "D", "D1", 10, "P&L",
        "Key P&L Concerns", "Key P&L Strengths",
        "P&L Overall",
    )
    ctx["cashflow"] = parse_financial_section(
        md, "E", "E1", 7, "Cash Flow",
        "Key Cash Flow Concerns", "Key Cash Flow Strengths",
        "Cash Flow Overall",
    )
    ctx["returns"] = parse_financial_section(
        md, "F", "F1", 7, "Return Ratios",
        "Key Return Ratio Concerns", "Key Return Ratio Strengths",
        "Return Ratios Overall",
    )
    ctx["valuation"] = parse_valuation(md)
    ctx["multibagger"] = parse_multibagger(md)

    # Overall verdict (extends/overrides V1's overall_verdict if richer)
    ov = parse_overall_verdict_v2(md)
    ctx["overall_dimensions"] = ov["overall_dimensions"]
    ctx["entry_triggers"] = ov["entry_triggers"]
    if ov["overall_verdict"]:
        ctx["overall_verdict"] = ov["overall_verdict"]
        ctx["verdict_class"] = {"INVEST": "invest", "MONITOR": "monitor", "AVOID": "avoid"}.get(ov["overall_verdict"], "monitor")

    # Derived: financial pillars + 8-up scorecards + headline stats
    ctx["financial_pillars"] = build_financial_pillars(ctx)
    ctx["scorecard_cards"]   = build_v2_scorecards(ctx)
    ctx["financial_headline_stats"] = build_headline_stats(md, ctx)

    # Short summary line for the financial dashboard
    g_count = sum(1 for p in ctx["financial_pillars"] if p["verdict"] == "🟢")
    r_count = sum(1 for p in ctx["financial_pillars"] if p["verdict"] == "🔴")
    a_count = sum(1 for p in ctx["financial_pillars"] if p["verdict"] == "🟡")
    ctx["financial_summary"] = (
        f"Across the five financial pillars, the company shows "
        f"{g_count} Green / {a_count} Amber / {r_count} Red verdicts. "
    )
    if r_count == 0 and g_count >= 4:
        ctx["financial_summary"] += "Financial fundamentals are broadly strong; investment risk lies elsewhere (valuation, governance)."
    elif r_count >= 2:
        ctx["financial_summary"] += "Multiple financial pillars carry serious concerns — verify each section carefully."
    else:
        ctx["financial_summary"] += "Financials are mixed; strengths and concerns balance out across pillars."

    # Overall summary (one-liner for the verdict page)
    ctx["overall_summary"] = (
        f"Final verdict based on management, industry, financials, valuation, and multi-bagger screening."
    )

    return ctx


# ── Render & write ─────────────────────────────────────────────────────────────

def render_html(context: dict) -> str:
    env = jinja2.Environment(
        loader=jinja2.FileSystemLoader(str(TEMPLATE_PATH.parent)),
        autoescape=jinja2.select_autoescape(["html"]),
    )
    env.filters["strip_bold"] = strip_bold
    tmpl = env.get_template(TEMPLATE_PATH.name)
    return tmpl.render(**context)


def main():
    if len(sys.argv) < 3:
        print("Usage: python3 generate_fa_pdf_v2.py <input.md> <output.pdf>")
        sys.exit(1)

    md_path = Path(sys.argv[1]).resolve()
    pdf_path = Path(sys.argv[2]).resolve()

    if not md_path.exists():
        log.error("Markdown file not found: %s", md_path)
        sys.exit(1)
    if not TEMPLATE_PATH.exists():
        log.error("Template not found: %s", TEMPLATE_PATH)
        sys.exit(1)

    log.info("Parsing %s", md_path.name)
    md = md_path.read_text(encoding="utf-8")
    ctx = parse_report_v2(md)
    log.info("Company: %s | Verdict: %s", ctx["company_name"], ctx["overall_verdict"])

    # Image scraping (same as V1)
    website_url = load_website_url(ctx["ticker"])
    if website_url:
        log.info("Website: %s", website_url)
        ctx["company_logo"] = fetch_company_logo(website_url, ctx["company_name"])
        headshots = scrape_headshots(website_url)
        ctx["product_images"] = scrape_product_images(website_url)
    else:
        log.warning("No website URL for %s — using SVG fallbacks", ctx["ticker"])
        ctx["company_logo"] = make_initials_svg(ctx["company_name"], size=150)
        headshots = []
        ctx["product_images"] = []

    if headshots:
        ctx["management_cards"] = headshots
    else:
        default_names = ["Company Management"]
        name_matches = re.findall(
            r"(?:Chairman|Managing Director|Executive Director|CEO|MD|CFO)[^|,\n]*?([A-Z][a-z]+ [A-Z][a-z]+)",
            md,
        )
        if name_matches:
            default_names = list(dict.fromkeys(name_matches))[:MAX_HEADSHOTS]
        ctx["management_cards"] = [
            {"name": n, "title": "", "img_data_url": make_initials_svg(n), "is_fallback": True}
            for n in default_names
        ]

    log.info("Rendering V2 HTML template")
    html = render_html(ctx)

    log.info("Generating PDF via Chrome headless")
    pdf_path.parent.mkdir(parents=True, exist_ok=True)
    html_to_pdf(html, pdf_path)
    print(f"PDF saved: {pdf_path}")


if __name__ == "__main__":
    main()
