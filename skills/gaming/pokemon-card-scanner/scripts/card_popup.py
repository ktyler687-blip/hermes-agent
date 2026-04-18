#!/usr/bin/env python3
"""
Card Scanner Popup UI
Generates a modern HTML popup displaying card scan results and opens it in the browser.

Usage:
    python3 card_popup.py '<json_string>'
    echo '<json_string>' | python3 card_popup.py

JSON schema:
{
  "game":       "Pokemon TCG" | "Magic: The Gathering" | "Yu-Gi-Oh!" | "Sports" | ...,
  "name":       "Charizard",
  "set":        "Base Set",
  "number":     "4/102",
  "rarity":     "Holo Rare",
  "treatment":  "Shadowless Holo",
  "language":   "English",
  "edition":    "1st Edition",
  "condition":  "NM",
  "condition_notes": "Minor edge whitening on back.",
  "image_url":  "https://... or /local/path/to/image.jpg",
  "details":    {"HP": "120", "Type": "Fire", "Attacks": "Fire Spin 100"},
  "prices": [
    {"condition": "NM",  "price": "$8,500"},
    {"condition": "LP",  "price": "$5,200"},
    {"condition": "MP",  "price": "$2,800"}
  ],
  "price_source": "TCGPlayer",
  "authenticity": "Authentic — all security features present.",
  "notes": "Shadowless 1st Edition Charizard — one of the most iconic cards."
}
"""
import sys
import json
import os
import tempfile
import webbrowser
from pathlib import Path
from datetime import date

# ──────────────────────────────────────────────────────────────────────────────
# Condition badge colors
# ──────────────────────────────────────────────────────────────────────────────
CONDITION_COLORS = {
    "M":   ("#22c55e", "#dcfce7"),
    "NM":  ("#16a34a", "#dcfce7"),
    "LP":  ("#84cc16", "#f7fee7"),
    "MP":  ("#eab308", "#fefce8"),
    "HP":  ("#f97316", "#fff7ed"),
    "D":   ("#ef4444", "#fef2f2"),
}

# ──────────────────────────────────────────────────────────────────────────────
# Game accent colors  (gradient start, gradient end, accent)
# ──────────────────────────────────────────────────────────────────────────────
GAME_THEMES = {
    "pokemon tcg":              ("#ef4444", "#3b82f6", "#facc15"),
    "magic: the gathering":     ("#7c3aed", "#1e40af", "#a78bfa"),
    "yu-gi-oh!":                ("#b45309", "#92400e", "#fbbf24"),
    "sports":                   ("#1d4ed8", "#0f172a", "#38bdf8"),
    "baseball":                 ("#dc2626", "#1e3a5f", "#60a5fa"),
    "basketball":               ("#ea580c", "#1c1917", "#fdba74"),
    "football":                 ("#166534", "#14532d", "#4ade80"),
    "hockey":                   ("#0369a1", "#0c4a6e", "#38bdf8"),
    "soccer":                   ("#15803d", "#14532d", "#86efac"),
    "default":                  ("#6366f1", "#1e1b4b", "#a5b4fc"),
}


def get_theme(game: str):
    key = game.lower().strip()
    for k, v in GAME_THEMES.items():
        if k in key:
            return v
    return GAME_THEMES["default"]


def condition_badge(cond: str) -> str:
    cond_key = cond.upper().split()[0] if cond else "NM"
    color, bg = CONDITION_COLORS.get(cond_key, ("#6b7280", "#f3f4f6"))
    return f'<span class="badge" style="background:{bg};color:{color};border:1.5px solid {color}">{cond}</span>'


def price_rows(prices: list) -> str:
    if not prices:
        return '<tr><td colspan="2" style="color:#6b7280;text-align:center">No pricing data</td></tr>'
    rows = []
    for i, p in enumerate(prices):
        bg = "#f8fafc" if i % 2 == 0 else "#ffffff"
        cond = p.get("condition", "—")
        price = p.get("price", "—")
        cond_key = cond.upper().split()[0]
        color, badge_bg = CONDITION_COLORS.get(cond_key, ("#6b7280", "#f3f4f6"))
        rows.append(
            f'<tr style="background:{bg}">'
            f'<td><span class="badge" style="background:{badge_bg};color:{color};border:1.5px solid {color};font-size:0.75rem">{cond}</span></td>'
            f'<td style="font-weight:700;color:#0f172a;text-align:right">{price}</td>'
            f"</tr>"
        )
    return "\n".join(rows)


def detail_chips(details: dict) -> str:
    chips = []
    for k, v in details.items():
        chips.append(
            f'<div class="chip"><span class="chip-label">{k}</span>'
            f'<span class="chip-value">{v}</span></div>'
        )
    return "\n".join(chips)


def image_tag(image_url: str) -> str:
    if not image_url:
        return '<div class="card-img-placeholder"><span>📷</span><p>No image</p></div>'
    # local file → convert to file:// URI
    if not image_url.startswith("http"):
        p = Path(image_url).resolve()
        image_url = p.as_uri()
    return (
        f'<img src="{image_url}" alt="Card image" class="card-img" '
        f'onerror="this.style.display=\'none\';this.nextElementSibling.style.display=\'flex\'">'
        f'<div class="card-img-placeholder" style="display:none"><span>📷</span><p>Image unavailable</p></div>'
    )


def render_html(data: dict) -> str:
    game = data.get("game", "Trading Card")
    grad_start, grad_end, accent = get_theme(game)
    today = date.today().strftime("%B %d, %Y")

    name        = data.get("name", "Unknown Card")
    card_set    = data.get("set", "—")
    number      = data.get("number", "")
    rarity      = data.get("rarity", "—")
    treatment   = data.get("treatment", "")
    language    = data.get("language", "English")
    edition     = data.get("edition", "")
    condition   = data.get("condition", "—")
    cond_notes  = data.get("condition_notes", "")
    image_url   = data.get("image_url", "")
    details     = data.get("details", {})
    prices      = data.get("prices", [])
    price_src   = data.get("price_source", "")
    authenticity = data.get("authenticity", "")
    notes       = data.get("notes", "")

    set_line = card_set
    if number:
        set_line += f" · #{number}"

    meta_chips = []
    if language and language != "English":
        meta_chips.append(f'<span class="meta-chip">{language}</span>')
    if edition:
        meta_chips.append(f'<span class="meta-chip">{edition}</span>')
    if treatment:
        meta_chips.append(f'<span class="meta-chip">{treatment}</span>')
    meta_line = " ".join(meta_chips)

    auth_block = ""
    if authenticity:
        icon = "✅" if "authentic" in authenticity.lower() else "⚠️"
        auth_color = "#16a34a" if "authentic" in authenticity.lower() else "#d97706"
        auth_block = f"""
        <div class="auth-block" style="border-color:{auth_color};background:{auth_color}11">
          <span style="font-size:1.1rem">{icon}</span>
          <span style="color:{auth_color};font-weight:600">{authenticity}</span>
        </div>"""

    notes_block = ""
    if notes:
        notes_block = f"""
        <div class="notes-block">
          <div class="section-label">📝 Notes</div>
          <p style="margin:0;color:#334155;line-height:1.6">{notes}</p>
        </div>"""

    price_source_line = f'<p class="price-source">Source: {price_src} · {today}</p>' if price_src else f'<p class="price-source">{today}</p>'

    return f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>{name} — Card Scanner</title>
<style>
  *, *::before, *::after {{ box-sizing: border-box; margin: 0; padding: 0; }}

  body {{
    font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
    background: #0f172a;
    min-height: 100vh;
    display: flex;
    align-items: center;
    justify-content: center;
    padding: 2rem 1rem;
    background-image:
      radial-gradient(ellipse 80% 60% at 20% -10%, {grad_start}33 0%, transparent 60%),
      radial-gradient(ellipse 60% 50% at 80% 110%, {grad_end}44 0%, transparent 60%);
  }}

  .popup {{
    background: #ffffff;
    border-radius: 24px;
    box-shadow: 0 32px 80px rgba(0,0,0,0.45), 0 0 0 1px rgba(255,255,255,0.08);
    max-width: 780px;
    width: 100%;
    overflow: hidden;
    animation: slideUp 0.4s cubic-bezier(0.16,1,0.3,1) both;
  }}

  @keyframes slideUp {{
    from {{ opacity:0; transform:translateY(32px) scale(0.97); }}
    to   {{ opacity:1; transform:translateY(0)    scale(1);    }}
  }}

  /* ── Header bar ─────────────────────────────────────────── */
  .header {{
    background: linear-gradient(135deg, {grad_start}, {grad_end});
    padding: 1.5rem 2rem;
    display: flex;
    align-items: center;
    gap: 1rem;
    position: relative;
    overflow: hidden;
  }}
  .header::before {{
    content: '';
    position: absolute; inset: 0;
    background: url("data:image/svg+xml,%3Csvg width='60' height='60' viewBox='0 0 60 60' xmlns='http://www.w3.org/2000/svg'%3E%3Cg fill='none' fill-rule='evenodd'%3E%3Cg fill='%23ffffff' fill-opacity='0.04'%3E%3Cpath d='M36 34v-4h-2v4h-4v2h4v4h2v-4h4v-2h-4zm0-30V0h-2v4h-4v2h4v4h2V6h4V4h-4zM6 34v-4H4v4H0v2h4v4h2v-4h4v-2H6zM6 4V0H4v4H0v2h4v4h2V6h4V4H6z'/%3E%3C/g%3E%3C/g%3E%3C/svg%3E");
  }}
  .header-icon {{
    font-size: 2.5rem;
    filter: drop-shadow(0 2px 8px rgba(0,0,0,0.3));
    position: relative;
    z-index:1;
  }}
  .header-text {{ position: relative; z-index:1; }}
  .header-game {{
    font-size: 0.72rem;
    font-weight: 700;
    letter-spacing: 0.12em;
    text-transform: uppercase;
    color: {accent};
    margin-bottom: 0.15rem;
  }}
  .header-title {{
    font-size: 1.6rem;
    font-weight: 800;
    color: #ffffff;
    line-height: 1.2;
    text-shadow: 0 2px 8px rgba(0,0,0,0.25);
  }}
  .header-sub {{
    font-size: 0.82rem;
    color: rgba(255,255,255,0.75);
    margin-top: 0.2rem;
  }}

  /* ── Body layout ────────────────────────────────────────── */
  .body {{ display: flex; gap: 0; }}

  /* ── Image panel ────────────────────────────────────────── */
  .image-panel {{
    width: 220px;
    flex-shrink: 0;
    background: #f1f5f9;
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: center;
    padding: 1.5rem 1rem;
    border-right: 1px solid #e2e8f0;
    position: relative;
  }}
  .card-img {{
    width: 100%;
    max-width: 180px;
    border-radius: 12px;
    box-shadow: 0 8px 32px rgba(0,0,0,0.18), 0 0 0 2px {accent}55;
    transition: transform 0.3s ease;
    display: block;
  }}
  .card-img:hover {{ transform: scale(1.04) rotate(-1deg); }}
  .card-img-placeholder {{
    width: 160px; height: 220px;
    background: #e2e8f0;
    border-radius: 12px;
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: center;
    color: #94a3b8;
    font-size: 2.5rem;
    gap: 0.5rem;
  }}
  .card-img-placeholder p {{ font-size: 0.75rem; }}

  .condition-panel {{
    margin-top: 1rem;
    text-align: center;
    width: 100%;
  }}
  .condition-label {{
    font-size: 0.65rem;
    font-weight: 700;
    letter-spacing: 0.1em;
    text-transform: uppercase;
    color: #94a3b8;
    margin-bottom: 0.35rem;
  }}

  /* ── Info panel ─────────────────────────────────────────── */
  .info-panel {{
    flex: 1;
    padding: 1.5rem;
    display: flex;
    flex-direction: column;
    gap: 1.1rem;
  }}

  .section-label {{
    font-size: 0.65rem;
    font-weight: 700;
    letter-spacing: 0.12em;
    text-transform: uppercase;
    color: #94a3b8;
    margin-bottom: 0.5rem;
  }}

  /* ── Rarity + meta ─────────────────────────────────────── */
  .rarity-row {{
    display: flex;
    flex-wrap: wrap;
    align-items: center;
    gap: 0.4rem;
  }}
  .rarity-pill {{
    background: linear-gradient(135deg, {grad_start}22, {grad_end}22);
    border: 1.5px solid {grad_start}55;
    color: {grad_start};
    font-size: 0.78rem;
    font-weight: 700;
    padding: 0.25rem 0.7rem;
    border-radius: 999px;
  }}
  .meta-chip {{
    background: #f1f5f9;
    border: 1px solid #e2e8f0;
    color: #475569;
    font-size: 0.72rem;
    font-weight: 600;
    padding: 0.2rem 0.6rem;
    border-radius: 999px;
  }}

  /* ── Detail chips ───────────────────────────────────────── */
  .chips-grid {{
    display: flex;
    flex-wrap: wrap;
    gap: 0.5rem;
  }}
  .chip {{
    background: #f8fafc;
    border: 1px solid #e2e8f0;
    border-radius: 10px;
    padding: 0.35rem 0.75rem;
    display: flex;
    flex-direction: column;
    min-width: 80px;
  }}
  .chip-label {{
    font-size: 0.62rem;
    font-weight: 700;
    letter-spacing: 0.08em;
    text-transform: uppercase;
    color: #94a3b8;
  }}
  .chip-value {{
    font-size: 0.85rem;
    font-weight: 600;
    color: #0f172a;
    margin-top: 0.1rem;
  }}

  /* ── Badge ──────────────────────────────────────────────── */
  .badge {{
    font-size: 0.78rem;
    font-weight: 700;
    padding: 0.25rem 0.7rem;
    border-radius: 999px;
    display: inline-block;
  }}

  /* ── Price table ────────────────────────────────────────── */
  .price-table-wrap {{
    background: #f8fafc;
    border: 1px solid #e2e8f0;
    border-radius: 14px;
    overflow: hidden;
  }}
  .price-table-wrap table {{
    width: 100%;
    border-collapse: collapse;
    font-size: 0.85rem;
  }}
  .price-table-wrap td {{
    padding: 0.6rem 1rem;
    border-bottom: 1px solid #f1f5f9;
  }}
  .price-table-wrap tr:last-child td {{ border-bottom: none; }}
  .price-source {{
    font-size: 0.7rem;
    color: #94a3b8;
    text-align: right;
    margin-top: 0.35rem;
    padding-right: 0.5rem;
  }}

  /* ── Auth block ─────────────────────────────────────────── */
  .auth-block {{
    display: flex;
    align-items: center;
    gap: 0.6rem;
    border: 1.5px solid;
    border-radius: 12px;
    padding: 0.65rem 1rem;
    font-size: 0.85rem;
  }}

  /* ── Notes block ────────────────────────────────────────── */
  .notes-block {{
    background: #fffbeb;
    border: 1px solid #fde68a;
    border-radius: 12px;
    padding: 0.75rem 1rem;
  }}

  /* ── Footer ─────────────────────────────────────────────── */
  .footer {{
    background: #f8fafc;
    border-top: 1px solid #e2e8f0;
    padding: 0.75rem 2rem;
    display: flex;
    align-items: center;
    justify-content: space-between;
  }}
  .footer-brand {{
    font-size: 0.72rem;
    font-weight: 700;
    color: #94a3b8;
    letter-spacing: 0.08em;
    text-transform: uppercase;
  }}
  .footer-accent {{ color: {accent}; }}
  .footer-date {{ font-size: 0.72rem; color: #cbd5e1; }}

  @media (max-width: 580px) {{
    .body {{ flex-direction: column; }}
    .image-panel {{ width: 100%; border-right: none; border-bottom: 1px solid #e2e8f0; flex-direction: row; gap: 1rem; padding: 1rem; }}
    .card-img {{ max-width: 120px; }}
  }}
</style>
</head>
<body>
<div class="popup">

  <!-- Header -->
  <div class="header">
    <div class="header-icon">🃏</div>
    <div class="header-text">
      <div class="header-game">{game}</div>
      <div class="header-title">{name}</div>
      <div class="header-sub">{set_line}</div>
    </div>
  </div>

  <!-- Body -->
  <div class="body">

    <!-- Left: Image + Condition -->
    <div class="image-panel">
      {image_tag(image_url)}
      <div class="condition-panel">
        <div class="condition-label">Condition</div>
        {condition_badge(condition)}
        {"<p style='font-size:0.7rem;color:#64748b;margin-top:0.4rem;line-height:1.4'>" + cond_notes + "</p>" if cond_notes else ""}
      </div>
    </div>

    <!-- Right: Info -->
    <div class="info-panel">

      <!-- Rarity row -->
      <div>
        <div class="section-label">Rarity &amp; Treatment</div>
        <div class="rarity-row">
          <span class="rarity-pill">{rarity}</span>
          {meta_line}
        </div>
      </div>

      <!-- Details chips -->
      {"<div><div class='section-label'>Card Details</div><div class='chips-grid'>" + detail_chips(details) + "</div></div>" if details else ""}

      <!-- Authenticity -->
      {auth_block}

      <!-- Price table -->
      <div>
        <div class="section-label">Market Value</div>
        <div class="price-table-wrap">
          <table>
            <tbody>
              {price_rows(prices)}
            </tbody>
          </table>
        </div>
        {price_source_line}
      </div>

      <!-- Notes -->
      {notes_block}

    </div>
  </div>

  <!-- Footer -->
  <div class="footer">
    <span class="footer-brand">Hermes <span class="footer-accent">Card Scanner</span></span>
    <span class="footer-date">{today}</span>
  </div>

</div>
</body>
</html>"""


def main():
    raw = ""
    if len(sys.argv) > 1:
        raw = " ".join(sys.argv[1:])
    elif not sys.stdin.isatty():
        raw = sys.stdin.read().strip()

    if not raw:
        print("Usage: python3 card_popup.py '<json_string>'", file=sys.stderr)
        sys.exit(1)

    try:
        data = json.loads(raw)
    except json.JSONDecodeError as e:
        print(f"Error: invalid JSON — {e}", file=sys.stderr)
        sys.exit(1)

    html = render_html(data)

    # Write to a temp file so the browser can open it
    fd, path = tempfile.mkstemp(suffix=".html", prefix="card_scan_")
    with os.fdopen(fd, "w", encoding="utf-8") as f:
        f.write(html)

    print(f"Card popup saved: {path}")

    # Open in browser
    opened = webbrowser.open(f"file://{path}")
    if not opened:
        # Fallback: try xdg-open
        os.system(f"xdg-open '{path}' &>/dev/null &")

    return path


if __name__ == "__main__":
    main()
