#!/usr/bin/env python3
"""
FA PDF Generator — Investor-grade PDF from FA markdown report.
Usage: python3 scripts/generate_fa_pdf.py <input.md> <output.pdf>
"""

import base64
import io
import logging
import os
import re
import subprocess
import sys
import tempfile
import urllib.parse
import urllib.request
from pathlib import Path

import jinja2
import requests
from bs4 import BeautifulSoup
from PIL import Image

# ── Constants ─────────────────────────────────────────────────────────────────

SCRIPT_DIR = Path(__file__).parent.resolve()
REPO_ROOT = SCRIPT_DIR.parent
TEMPLATE_PATH = SCRIPT_DIR / "templates/fa_report.html"


def _detect_chrome() -> str:
    """Resolve a Chrome / Chromium binary across macOS / Linux / Windows.

    Order of preference:
      1. ``$CHROME_PATH`` env var if set and points to an executable
      2. Common per-OS install locations
      3. ``chrome`` / ``chromium`` on ``$PATH``
    Returns the resolved path; the caller is expected to handle a missing binary.
    """
    env = os.environ.get("CHROME_PATH")
    if env and Path(env).exists():
        return env

    candidates = [
        # macOS
        "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome",
        "/Applications/Chromium.app/Contents/MacOS/Chromium",
        # Linux
        "/usr/bin/google-chrome",
        "/usr/bin/google-chrome-stable",
        "/usr/bin/chromium",
        "/usr/bin/chromium-browser",
        "/snap/bin/chromium",
        # Windows
        r"C:\Program Files\Google\Chrome\Application\chrome.exe",
        r"C:\Program Files (x86)\Google\Chrome\Application\chrome.exe",
    ]
    for path in candidates:
        if Path(path).exists():
            return path

    from shutil import which
    for name in ("google-chrome", "chrome", "chromium", "chromium-browser"):
        found = which(name)
        if found:
            return found

    return ""


def _detect_stock_universe() -> Path:
    """Resolve the stock-universe.md file.

    Order of preference:
      1. ``$STOCK_UNIVERSE_PATH`` env var
      2. ``<plugin>/skills/fa-orchestrator/references/stock-universe.md`` (standalone plugin layout)
      3. ``<cwd>/.claude/skills/fa-orchestrator/references/stock-universe.md`` (Claude Code project layout)
      4. ``<plugin>/.claude/skills/fa-orchestrator/references/stock-universe.md`` (legacy sibling layout)
    Returns the first existing candidate, or the first candidate as a non-existent fallback
    so the caller can ``read_text`` and trip its own error path.
    """
    env = os.environ.get("STOCK_UNIVERSE_PATH")
    if env:
        return Path(env)

    candidates = [
        REPO_ROOT / "fa-orchestrator/references/stock-universe.md",  # Hermes investing layout
        REPO_ROOT / "skills/fa-orchestrator/references/stock-universe.md",  # fa-plugin layout
        Path.cwd() / ".claude/skills/fa-orchestrator/references/stock-universe.md",
        REPO_ROOT / ".claude/skills/fa-orchestrator/references/stock-universe.md",
    ]
    for path in candidates:
        if path.exists():
            return path
    return candidates[0]


CHROME = _detect_chrome()
STOCK_UNIVERSE = _detect_stock_universe()

HEADSHOT_TIMEOUT = 8
IMAGE_TIMEOUT = 8
CHROME_TIMEOUT = 120
MAX_HEADSHOTS = 6
MAX_PRODUCTS = 5

BROWSER_HEADERS = {
    "User-Agent": (
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) "
        "AppleWebKit/537.36 (KHTML, like Gecko) "
        "Chrome/120.0.0.0 Safari/537.36"
    ),
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
}

RAG_CSS = {"🟢": "green", "🟡": "amber", "🔴": "red", "⬜": "na"}
PORTER_CSS = {
    "Favorable": "green", "Neutral": "amber", "Unfavorable": "red",
    "Strong": "green", "Moderate": "amber", "Weak": "red",
}
VERDICT_CSS = {"INVEST": "invest", "MONITOR": "monitor", "AVOID": "avoid"}

AVATAR_COLORS = ["#1a237e", "#2e7d32", "#6a1b9a", "#c62828", "#e65100", "#00838f"]

logging.basicConfig(level=logging.INFO, format="%(levelname)s: %(message)s")
log = logging.getLogger(__name__)


# ── SVG Avatar ────────────────────────────────────────────────────────────────

def make_initials_svg(name: str, size: int = 120) -> str:
    """Return a base64-encoded SVG data URI with initials for the given name."""
    words = [w for w in name.split() if w]
    if len(words) >= 2:
        initials = words[0][0].upper() + words[1][0].upper()
    elif words:
        initials = words[0][:2].upper()
    else:
        initials = "?"
    color = AVATAR_COLORS[hash(name) % len(AVATAR_COLORS)]
    font_size = size // 3
    svg = (
        f'<svg xmlns="http://www.w3.org/2000/svg" width="{size}" height="{size}">'
        f'<circle cx="{size//2}" cy="{size//2}" r="{size//2}" fill="{color}"/>'
        f'<text x="50%" y="50%" dominant-baseline="central" text-anchor="middle" '
        f'font-family="Georgia,serif" font-size="{font_size}" font-weight="bold" fill="white">'
        f'{initials}</text></svg>'
    )
    b64 = base64.b64encode(svg.encode()).decode()
    return f"data:image/svg+xml;base64,{b64}"


# ── Image helpers ─────────────────────────────────────────────────────────────

def image_to_data_uri(img_bytes: bytes, fmt: str = "PNG") -> str:
    """Convert raw image bytes → square-cropped, resized base64 data URI."""
    try:
        img = Image.open(io.BytesIO(img_bytes)).convert("RGBA")
        # Square crop from center
        w, h = img.size
        side = min(w, h)
        left = (w - side) // 2
        top = max(0, (h - side) // 4)  # bias toward top (faces)
        top = min(top, h - side)
        img = img.crop((left, top, left + side, top + side))
        img = img.resize((200, 200), Image.LANCZOS)
        buf = io.BytesIO()
        img.save(buf, format=fmt)
        b64 = base64.b64encode(buf.getvalue()).decode()
        mime = "image/png" if fmt == "PNG" else "image/jpeg"
        return f"data:{mime};base64,{b64}"
    except Exception as e:
        log.warning("image_to_data_uri failed: %s", e)
        return ""


def product_image_to_data_uri(img_bytes: bytes) -> str:
    """Convert product image bytes → max-height 160px data URI, preserving aspect ratio."""
    try:
        img = Image.open(io.BytesIO(img_bytes)).convert("RGBA")
        w, h = img.size
        max_h = 160
        if h > max_h:
            img = img.resize((int(w * max_h / h), max_h), Image.LANCZOS)
        buf = io.BytesIO()
        img.save(buf, format="PNG")
        b64 = base64.b64encode(buf.getvalue()).decode()
        return f"data:image/png;base64,{b64}"
    except Exception as e:
        log.warning("product_image_to_data_uri failed: %s", e)
        return ""


def fetch_bytes(url: str, timeout: int = IMAGE_TIMEOUT) -> bytes | None:
    """Fetch URL bytes with browser headers. Returns None on any error."""
    try:
        resp = requests.get(url, headers=BROWSER_HEADERS, timeout=timeout)
        if resp.status_code == 200 and resp.content:
            return resp.content
    except Exception as e:
        log.warning("fetch_bytes %s: %s", url, e)
    return None


def resolve_url(base: str, src: str) -> str:
    return urllib.parse.urljoin(base, src)


# ── Web scraping ──────────────────────────────────────────────────────────────

def fetch_html(url: str, timeout: int = HEADSHOT_TIMEOUT) -> BeautifulSoup | None:
    data = fetch_bytes(url, timeout)
    if data:
        return BeautifulSoup(data, "html.parser")
    return None


def _extract_person_from_container(container, img_tag, page_url: str) -> dict | None:
    """Extract name, title, and image from a container element. Returns dict or None."""
    src = img_tag.get("src", "")
    if not src or any(skip in src.lower() for skip in ["icon", "logo", "arrow", "bg", "banner", "sprite", "favicon"]):
        return None

    # Name extraction: try common class names first, then headings, then alt, then filename
    name = ""
    title = ""

    # Pattern A: named divs like testimonial_top_name / _info / person-name
    name_candidates = container.find_all(class_=re.compile(r"name|title|person|member", re.I))
    desi_candidates = container.find_all(class_=re.compile(r"desi|role|position|post|designation", re.I))
    if name_candidates:
        name = name_candidates[0].get_text(strip=True)
    if desi_candidates:
        title = desi_candidates[0].get_text(strip=True)

    # Pattern B: headings
    if not name:
        for h in container.find_all(["h3", "h4", "h5", "strong", "b"]):
            txt = h.get_text(strip=True)
            if txt and len(txt) > 2:
                name = txt
                break

    # Pattern C: paragraph after name
    if not title:
        for p in container.find_all("p"):
            txt = p.get_text(strip=True)
            if txt and txt != name:
                title = txt[:80]
                break

    # Fallback: alt or filename
    if not name:
        name = img_tag.get("alt", "") or Path(src).stem.replace("-", " ").replace("_", " ").title()

    abs_url = resolve_url(page_url, src)
    img_bytes = fetch_bytes(abs_url)
    if not img_bytes:
        return None
    data_uri = image_to_data_uri(img_bytes)
    if not data_uri:
        return None
    return {"name": name, "title": title, "img_data_url": data_uri, "is_fallback": False}


def scrape_headshots(website_url: str) -> list[dict]:
    """Scrape management headshots from company website. Returns list of {name, title, img_data_url}."""
    about_paths = ["/about-us.php", "/about-us", "/about", "/leadership",
                   "/team", "/management", "/our-team", "/management-team"]
    soup = None
    page_url = website_url
    for path in about_paths:
        url = website_url.rstrip("/") + path
        soup = fetch_html(url)
        if soup:
            page_url = url
            log.info("Headshots page found: %s", url)
            break

    if not soup:
        log.warning("No management page found at %s", website_url)
        return []

    results = []

    # Strategy 1: <figure> elements (semantic)
    for fig in soup.find_all("figure")[:MAX_HEADSHOTS * 2]:
        img_tag = fig.find("img")
        if not img_tag:
            continue
        item = _extract_person_from_container(fig, img_tag, page_url)
        if item:
            results.append(item)
        if len(results) >= MAX_HEADSHOTS:
            break

    # Strategy 2: divs/containers with team/person/testimonial class keywords
    if not results:
        team_keywords = re.compile(
            r"team|member|director|board|management|person|staff|leadership|testimonial|profile|bio|people",
            re.I
        )
        seen = set()
        for tag in soup.find_all(["div", "li", "article", "section"]):
            cls = " ".join(tag.get("class", []))
            if not team_keywords.search(cls):
                continue
            img_tag = tag.find("img")
            if not img_tag:
                continue
            src = img_tag.get("src", "")
            if src in seen:
                continue
            seen.add(src)
            item = _extract_person_from_container(tag, img_tag, page_url)
            if item:
                results.append(item)
            if len(results) >= MAX_HEADSHOTS:
                break

    # Strategy 3: any img with ../images/ relative path (common in PHP CMSes for person photos)
    if not results:
        seen = set()
        for img_tag in soup.find_all("img"):
            src = img_tag.get("src", "")
            if not src.startswith("../") or src in seen:
                continue
            if any(skip in src.lower() for skip in ["icon", "logo", "arrow", "bg", "banner", "social", "footer"]):
                continue
            seen.add(src)
            # Walk up parent chain to find a container with name info
            container = img_tag.parent
            for _ in range(4):
                if container and container.parent:
                    container = container.parent
                else:
                    break
            item = _extract_person_from_container(container or img_tag.parent, img_tag, page_url)
            if item:
                results.append(item)
            if len(results) >= MAX_HEADSHOTS:
                break

    log.info("Scraped %d headshots", len(results))
    return results[:MAX_HEADSHOTS]


def scrape_product_images(website_url: str) -> list[dict]:
    """Scrape product/brand logos from company homepage. Returns list of {name, img_data_url}."""
    soup = fetch_html(website_url.rstrip("/") + "/")
    if not soup:
        soup = fetch_html(website_url)
    if not soup:
        return []

    results = []
    seen_srcs = set()

    # Look for images in footer, brand sections, or product sections
    brand_keywords = {"brand", "product", "logo", "footer"}
    candidate_imgs = []

    # Find sections/divs with brand/product keywords
    for tag in soup.find_all(["section", "div", "footer", "ul"]):
        cls = " ".join(tag.get("class", [])).lower()
        tag_id = tag.get("id", "").lower()
        combined = cls + " " + tag_id
        if any(k in combined for k in brand_keywords):
            for img in tag.find_all("img"):
                candidate_imgs.append(img)

    # Also collect images where src path contains brand/product keywords
    for img in soup.find_all("img"):
        src = img.get("src", "").lower()
        if any(k in src for k in ["brand", "product", "logo1", "logo2", "logo3", "logo4", "logo5", "avvatar", "footer"]):
            candidate_imgs.append(img)

    for img_tag in candidate_imgs:
        src = img_tag.get("src", "")
        if not src or src in seen_srcs:
            continue
        # Skip tiny icons and navigation elements
        w = img_tag.get("width", "")
        if w and str(w).isdigit() and int(w) < 40:
            continue
        if any(skip in src.lower() for skip in ["icon", "arrow", "close", "menu", "search", "favicon", "sprite"]):
            continue
        seen_srcs.add(src)
        abs_url = resolve_url(website_url, src)
        img_bytes = fetch_bytes(abs_url)
        if img_bytes:
            # Skip very small files (likely icons)
            if len(img_bytes) < 800:
                continue
            data_uri = product_image_to_data_uri(img_bytes)
            if data_uri:
                name = img_tag.get("alt", "") or Path(src).stem.replace("-", " ").replace("_", " ").title()
                results.append({"name": name, "img_data_url": data_uri})
        if len(results) >= MAX_PRODUCTS:
            break

    log.info("Scraped %d product images", len(results))
    return results[:MAX_PRODUCTS]


def fetch_company_logo(website_url: str, company_name: str) -> str:
    """Try common logo paths. Returns data URI (image or SVG fallback)."""
    logo_paths = [
        "/images/logo.png", "/images/logo.jpg", "/assets/logo.png",
        "/img/logo.png", "/assets/images/logo.png", "/images/header-logo.png",
        "/wp-content/uploads/logo.png",
    ]
    for path in logo_paths:
        url = website_url.rstrip("/") + path
        img_bytes = fetch_bytes(url, timeout=5)
        if img_bytes and len(img_bytes) > 500:
            try:
                img = Image.open(io.BytesIO(img_bytes)).convert("RGBA")
                w, h = img.size
                max_dim = 300
                if max(w, h) > max_dim:
                    scale = max_dim / max(w, h)
                    img = img.resize((int(w * scale), int(h * scale)), Image.LANCZOS)
                buf = io.BytesIO()
                img.save(buf, format="PNG")
                b64 = base64.b64encode(buf.getvalue()).decode()
                log.info("Logo found at %s", url)
                return f"data:image/png;base64,{b64}"
            except Exception:
                continue
    # Fallback: SVG initials circle
    return make_initials_svg(company_name, size=150)


# ── Stock Universe lookup ──────────────────────────────────────────────────────

def load_website_url(ticker: str) -> str | None:
    """Read Website URL from stock-universe.md for the given ticker."""
    try:
        content = STOCK_UNIVERSE.read_text(encoding="utf-8")
        escaped = re.escape(ticker)
        m = re.search(
            rf"^\|\s*{escaped}\s*\|[^|]+\|[^|]+\|[^|]*\|\s*(https?://[^\s|]+)\s*\|",
            content, re.MULTILINE,
        )
        if m:
            return m.group(1).strip()
    except Exception as e:
        log.warning("load_website_url: %s", e)
    return None


# ── Markdown parsing ───────────────────────────────────────────────────────────

def strip_bold(text: str) -> str:
    return re.sub(r"\*\*(.+?)\*\*", r"\1", text).strip()


def parse_header(md: str) -> dict:
    def get(pattern):
        m = re.search(pattern, md)
        return m.group(1).strip() if m else ""

    ticker = get(r"Ticker\s*:\s*(.+)")
    return {
        "company_name": get(r"Company\s*:\s*(.+)"),
        "ticker": ticker,
        "sector": get(r"Sector\s*:\s*(.+)"),
        "date": get(r"Date\s*:\s*(\d{4}-\d{2}-\d{2})"),
        "slug": ticker.replace("NSE:", "").lower().strip(),
    }


def parse_table_rows(text: str, has_num: bool = True) -> list[dict]:
    """Parse | # | Criterion | Finding | Status | rows (or | # | Force | Assessment | Verdict |)."""
    if has_num:
        pattern = re.compile(
            r"^\|\s*(\d+)\s*\|\s*([^|]+?)\s*\|\s*([^|]+?)\s*\|\s*(🟢|🟡|🔴|⬜|Favorable|Neutral|Unfavorable|Strong|Moderate|Weak)\s*\|",
            re.MULTILINE,
        )
    else:
        pattern = re.compile(
            r"^\|\s*([^|]+?)\s*\|\s*([^|]+?)\s*\|\s*(🟢|🟡|🔴|⬜|Favorable|Neutral|Unfavorable|Strong|Moderate|Weak|Moderate-Strong)\s*\|",
            re.MULTILINE,
        )
    rows = []
    for m in pattern.finditer(text):
        if has_num:
            num, col2, col3, verdict = m.group(1), m.group(2), m.group(3), m.group(4)
        else:
            num, col2, col3, verdict = "", m.group(1), m.group(2), m.group(3)
        rag_class = RAG_CSS.get(verdict) or PORTER_CSS.get(verdict, "na")
        rows.append({
            "num": num,
            "col2": strip_bold(col2),
            "col3": strip_bold(col3)[:300],
            "verdict": verdict,
            "rag_class": rag_class,
        })
    return rows


def get_section(md: str, heading: str) -> str:
    """Extract text of a ## section."""
    parts = re.split(r"^## ", md, flags=re.MULTILINE)
    for part in parts:
        if part.strip().startswith(heading):
            return part
    return ""


def get_subsection(text: str, heading: str) -> str:
    """Extract text of a ### subsection."""
    parts = re.split(r"^### ", text, flags=re.MULTILINE)
    for part in parts:
        if part.strip().startswith(heading):
            return part
    return ""


def parse_score(text: str, total: int) -> dict:
    m = re.search(rf"Score:\s*(\d+)/{total} Green[,\s]*(\d+)?\s*Amber[,\s]*(\d+)?\s*Red(?:[,\s]*(\d+)?\s*N/A)?", text)
    if m:
        return {
            "green": int(m.group(1) or 0),
            "amber": int(m.group(2) or 0),
            "red": int(m.group(3) or 0),
            "na": int(m.group(4) or 0),
            "total": total,
        }
    return {"green": 0, "amber": 0, "red": 0, "na": 0, "total": total}


def parse_rag_verdict(text: str, patterns: list[str]) -> str:
    for p in patterns:
        m = re.search(p, text)
        if m:
            return m.group(1)
    return "🟡"


def parse_top3(md: str, heading: str) -> list[dict]:
    section = get_section(md, "OVERALL VERDICT") or md
    # Find the heading block
    m = re.search(rf"### {re.escape(heading)}\s*\n(.*?)(?=\n### |\Z)", section, re.DOTALL)
    if not m:
        return []
    block = m.group(1)
    items = re.findall(
        r"^\d+\.\s+\*\*(.+?)\*\*[:\s—–-]+(.+?)(?=^\d+\.|\Z)",
        block, re.MULTILINE | re.DOTALL,
    )
    result = []
    for title, body in items[:3]:
        body_clean = re.sub(r"\s+", " ", strip_bold(body)).strip()[:350]
        result.append({"title": strip_bold(title), "body": body_clean})
    return result


def parse_data_sources(md: str) -> list[dict]:
    section = get_section(md, "DATA SOURCES")
    rows = []
    for m in re.finditer(
        r"^\|\s*([^|*\-\s][^|]*?)\s*\|\s*([^|]+?)\s*\|\s*([^|]+?)\s*\|",
        section, re.MULTILINE,
    ):
        c1, c2, c3 = m.group(1).strip(), m.group(2).strip(), m.group(3).strip()
        if "---" in c1 or "Data Point" in c1:
            continue
        rows.append({"point": c1[:60], "source": c2[:80], "date": c3})
    return rows


def parse_industry_stage(section: str) -> dict:
    def get(p):
        m = re.search(p, section)
        return m.group(1).strip() if m else ""

    stage = get(r"\*\*Stage:\*\*\s*(.+)")
    # Map stage to CSS class
    stage_lower = stage.lower()
    if "growth" in stage_lower:
        stage_class = "stage-growth"
    elif "pioneer" in stage_lower:
        stage_class = "stage-pioneer"
    elif "decline" in stage_lower:
        stage_class = "stage-decline"
    else:
        stage_class = "stage-maturity"

    rationale_m = re.search(r"\*\*Stage Rationale:\*\*\s*(.+?)(?=\n\n|\*\*Implication|---)", section, re.DOTALL)
    impl_m = re.search(r"\*\*Implication for Company:\*\*\s*(.+?)(?=\n\n|---)", section, re.DOTALL)

    signals_block = get_subsection(section, "B1") or section
    signals = []
    for m in re.finditer(r"^\|\s*([^|*\-][^|]+?)\s*\|\s*([^|]+?)\s*\|", signals_block, re.MULTILINE):
        s, o = m.group(1).strip(), m.group(2).strip()
        if "---" in s or "Signal" in s or "Stage" in s or "Industry" in s:
            continue
        signals.append({"signal": s, "observation": o[:120]})

    return {
        "industry_name": get(r"\*\*Industry:\*\*\s*(.+)"),
        "industry_stage": stage,
        "stage_class": stage_class,
        "stage_rationale": re.sub(r"\s+", " ", strip_bold(rationale_m.group(1))).strip()[:400] if rationale_m else "",
        "stage_implication": re.sub(r"\s+", " ", strip_bold(impl_m.group(1))).strip()[:300] if impl_m else "",
        "stage_signals": signals[:5],
    }


def parse_report(md: str) -> dict:
    ctx = parse_header(md)

    # Management sections
    part_a = get_section(md, "PART A")
    a1 = get_subsection(part_a, "A1")
    a2 = get_subsection(part_a, "A2")

    ctx["integrity_rows"] = parse_table_rows(a1)
    ctx["integrity_score"] = parse_score(a1, 10)
    ctx["integrity_verdict"] = parse_rag_verdict(
        part_a, [r"Integrity.*?\|\s*(🟢|🟡|🔴)", r"Integrity Overall.*?:\s*(🟢|🟡|🔴)"]
    )

    # Key integrity concerns
    concerns_m = re.search(r"\*\*Key Integrity Concerns.*?\*\*\s*\n(.*?)(?=\n---|\n###|\Z)", a1, re.DOTALL)
    ctx["integrity_concerns"] = []
    if concerns_m:
        ctx["integrity_concerns"] = [
            strip_bold(line.lstrip("- ").strip())
            for line in concerns_m.group(1).splitlines()
            if line.strip().startswith("-")
        ][:4]

    ctx["skillset_rows"] = parse_table_rows(a2)
    ctx["skillset_score"] = parse_score(a2, 4)
    ctx["skillset_verdict"] = parse_rag_verdict(
        part_a, [r"Skillset.*?\|\s*(🟢|🟡|🔴)", r"Skillset Overall.*?:\s*(🟢|🟡|🔴)"]
    )

    # Second-gen table
    sg_m = re.search(r"Second-Gen Assessment.*?\n(.*?)(?=\n---|\n###|\Z)", part_a, re.DOTALL)
    ctx["second_gen_rows"] = parse_table_rows(sg_m.group(1), has_num=False) if sg_m else []

    # Management overall
    mgmt_overall_section = get_subsection(part_a, "Management Overall") or part_a
    ctx["mgmt_overall_verdict"] = parse_rag_verdict(
        mgmt_overall_section,
        [r"Management Overall.*?\*\*(🟢|🟡|🔴)", r"\*\*Management Overall\*\*[^|]*\|[^|]*\|\s*\*\*(🟢|🟡|🔴)"],
    )
    summary_m = re.search(r"\*\*Management Summary:\*\*\s*(.+?)(?=\n\n|---|\Z)", part_a, re.DOTALL)
    ctx["mgmt_summary"] = re.sub(r"\s+", " ", strip_bold(summary_m.group(1))).strip()[:500] if summary_m else ""

    # Industry sections
    part_b = get_section(md, "PART B")
    b1 = get_subsection(part_b, "B1")
    b2 = get_subsection(part_b, "B2")

    ctx.update(parse_industry_stage(b1 or part_b))
    ctx["forces_rows"] = parse_table_rows(b2)

    forces_summary_m = re.search(r"\*\*Industry Forces Summary:\*\*\s*(.+)", b2)
    ctx["forces_summary"] = forces_summary_m.group(1).strip() if forces_summary_m else ""

    ctx["industry_overall_verdict"] = parse_rag_verdict(
        part_b, [r"Industry Overall.*?\*\*(🟢|🟡|🔴)", r"\*\*Industry Overall\*\*[^|]*\|\s*\*\*(🟢|🟡|🔴)"]
    )

    # Overall verdict
    overall_section = get_section(md, "OVERALL VERDICT") or md
    m = re.search(r"\*\*OVERALL \(Phase 1\)\*\*\s*\|\s*\*\*(INVEST|MONITOR|AVOID)\*\*", overall_section)
    ctx["overall_verdict"] = m.group(1) if m else "MONITOR"
    ctx["verdict_class"] = VERDICT_CSS.get(ctx["overall_verdict"], "monitor")

    ctx["top3_risks"] = parse_top3(md, "Top 3 Risks")
    ctx["top3_positives"] = parse_top3(md, "Top 3 Positives")

    recommended_m = re.search(r"### Recommended Next Step\s*\n(.+?)(?=\n---|\n##|\Z)", md, re.DOTALL)
    ctx["recommended_next"] = re.sub(r"\s+", " ", strip_bold(recommended_m.group(1))).strip()[:400] if recommended_m else ""

    ctx["data_sources"] = parse_data_sources(md)

    # Scorecard cards for executive summary
    forces_count = sum(1 for r in ctx["forces_rows"] if r["rag_class"] == "green")
    forces_total = len(ctx["forces_rows"])
    ctx["scorecard_cards"] = [
        {
            "label": "Management Integrity",
            "value": ctx["integrity_verdict"],
            "sub": f"{ctx['integrity_score']['green']}G / {ctx['integrity_score']['amber']}A / {ctx['integrity_score']['red']}R",
            "rag_class": RAG_CSS.get(ctx["integrity_verdict"], "amber"),
        },
        {
            "label": "Management Skillset",
            "value": ctx["skillset_verdict"],
            "sub": f"{ctx['skillset_score']['green']}G / {ctx['skillset_score']['amber']}A / {ctx['skillset_score']['red']}R",
            "rag_class": RAG_CSS.get(ctx["skillset_verdict"], "amber"),
        },
        {
            "label": "Industry Stage",
            "value": ctx["industry_stage"],
            "sub": ctx["industry_name"][:40] if ctx.get("industry_name") else "",
            "rag_class": ctx.get("stage_class", "stage-growth").replace("stage-", ""),
        },
        {
            "label": "Industry Forces",
            "value": ctx["industry_overall_verdict"],
            "sub": f"{forces_count}/{forces_total} Forces Favorable",
            "rag_class": RAG_CSS.get(ctx["industry_overall_verdict"], "amber"),
        },
    ]

    return ctx


# ── HTML rendering ─────────────────────────────────────────────────────────────

def render_html(context: dict) -> str:
    env = jinja2.Environment(
        loader=jinja2.FileSystemLoader(str(TEMPLATE_PATH.parent)),
        autoescape=jinja2.select_autoescape(["html"]),
    )
    env.filters["strip_bold"] = strip_bold
    tmpl = env.get_template(TEMPLATE_PATH.name)
    return tmpl.render(**context)


# ── Chrome PDF ─────────────────────────────────────────────────────────────────

def html_to_pdf(html_content: str, pdf_path: Path) -> None:
    if not CHROME or not Path(CHROME).exists():
        raise FileNotFoundError(
            "Chrome / Chromium not found. Install Google Chrome or set the "
            "CHROME_PATH environment variable to the binary path."
        )

    tmp_html = None
    try:
        with tempfile.NamedTemporaryFile(suffix=".html", delete=False, mode="w", encoding="utf-8") as f:
            f.write(html_content)
            tmp_html = f.name

        result = subprocess.run(
            [
                CHROME,
                "--headless=new",
                "--no-sandbox",
                "--disable-gpu",
                "--run-all-compositor-stages-before-draw",
                "--no-pdf-header-footer",
                f"--print-to-pdf={str(pdf_path.resolve())}",
                f"file://{tmp_html}",
            ],
            capture_output=True, text=True, timeout=CHROME_TIMEOUT,
        )
        if result.returncode != 0 and not pdf_path.exists():
            raise RuntimeError(f"Chrome failed (exit {result.returncode}): {result.stderr[:400]}")
        if not pdf_path.exists():
            raise RuntimeError(f"Chrome ran but PDF not created at {pdf_path}")
        log.info("PDF written: %s (%.0f KB)", pdf_path, pdf_path.stat().st_size / 1024)
    finally:
        if tmp_html and os.path.exists(tmp_html):
            os.unlink(tmp_html)


# ── Main ───────────────────────────────────────────────────────────────────────

def main():
    if len(sys.argv) < 3:
        print("Usage: python3 generate_fa_pdf.py <input.md> <output.pdf>")
        sys.exit(1)

    md_path = Path(sys.argv[1]).resolve()
    pdf_path = Path(sys.argv[2]).resolve()

    if not md_path.exists():
        log.error("Markdown file not found: %s", md_path)
        sys.exit(1)
    if not TEMPLATE_PATH.exists():
        log.error("Template not found: %s", TEMPLATE_PATH)
        sys.exit(1)

    # 1. Parse report
    log.info("Parsing %s", md_path.name)
    md = md_path.read_text(encoding="utf-8")
    ctx = parse_report(md)
    log.info("Company: %s | Verdict: %s", ctx["company_name"], ctx["overall_verdict"])

    # 2. Image scraping
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

    # 3. Build management cards (merge headshots with SVG fallbacks)
    if headshots:
        ctx["management_cards"] = headshots
    else:
        # Generate SVG avatar cards from integrity table person names if available
        # or use generic placeholder
        default_names = ["Company Management"]
        # Try to extract person names from the report text
        name_matches = re.findall(r"(?:Chairman|Managing Director|Executive Director|CEO|MD|CFO)[^|,\n]*?([A-Z][a-z]+ [A-Z][a-z]+)", md)
        if name_matches:
            default_names = list(dict.fromkeys(name_matches))[:MAX_HEADSHOTS]
        ctx["management_cards"] = [
            {"name": n, "title": "", "img_data_url": make_initials_svg(n), "is_fallback": True}
            for n in default_names
        ]

    # 4. Render HTML
    log.info("Rendering HTML template")
    html = render_html(ctx)

    # 5. Generate PDF
    log.info("Generating PDF via Chrome headless")
    pdf_path.parent.mkdir(parents=True, exist_ok=True)
    html_to_pdf(html, pdf_path)
    print(f"PDF saved: {pdf_path}")


if __name__ == "__main__":
    main()
