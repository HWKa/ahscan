"""
Generates the static HTML page for GitHub Pages.
"""

from datetime import datetime, timezone
from scraper import copper_to_gold, copper_to_gold_float


def _profit_class(profit):
    """CSS class for profit coloring."""
    if profit is None:
        return "neutral"
    if profit > 0:
        return "positive"
    return "negative"


def _profit_str(profit, prefix="+"):
    if profit is None:
        return "N/A"
    sign = "+" if profit >= 0 else ""
    return f"{sign}{copper_to_gold(profit)}"


def render_html(analysis: dict) -> str:
    now = datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M UTC")

    exec_sum = analysis["executive_summary"]

    html = f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>Icecrown AH — Epic Gem Tracker</title>
<style>
  :root {{
    --bg: #1a1a2e; --surface: #16213e; --surface2: #0f3460;
    --accent: #e94560; --text: #eaeaea; --muted: #888;
    --positive: #4caf50; --negative: #f44336; --neutral: #aaa;
    --gold: #ffd700; --border: #2a2a4a;
  }}
  * {{ box-sizing: border-box; margin: 0; padding: 0; }}
  body {{ background: var(--bg); color: var(--text); font-family: 'Segoe UI', sans-serif; font-size: 14px; }}
  header {{ background: var(--surface2); padding: 16px 24px; border-bottom: 2px solid var(--accent); display: flex; align-items: center; gap: 16px; }}
  header h1 {{ font-size: 1.4em; color: var(--gold); }}
  header .updated {{ color: var(--muted); font-size: 0.85em; margin-left: auto; }}
  .container {{ max-width: 1600px; margin: 0 auto; padding: 16px; }}

  /* Executive Summary */
  .exec-summary {{ display: grid; grid-template-columns: 1fr 1fr; gap: 16px; margin-bottom: 24px; }}
  .exec-card {{ background: var(--surface); border: 1px solid var(--border); border-radius: 8px; padding: 16px; }}
  .exec-card h2 {{ color: var(--gold); font-size: 1.1em; margin-bottom: 12px; border-bottom: 1px solid var(--border); padding-bottom: 8px; }}
  .exec-card h3 {{ color: var(--accent); font-size: 0.9em; margin: 10px 0 6px; text-transform: uppercase; letter-spacing: 0.05em; }}
  .exec-row {{ display: flex; justify-content: space-between; align-items: center; padding: 4px 0; border-bottom: 1px solid #222; font-size: 0.88em; }}
  .exec-row:last-child {{ border-bottom: none; }}
  .exec-gem {{ color: var(--text); }}
  .exec-val {{ font-weight: 600; }}

  /* Gem sections */
  .gem-section {{ margin-bottom: 28px; }}
  .gem-header {{ background: var(--surface2); border-radius: 8px 8px 0 0; padding: 10px 16px; display: flex; align-items: center; gap: 12px; border-bottom: 2px solid var(--accent); }}
  .gem-header h2 {{ font-size: 1.05em; color: var(--gold); }}
  .gem-body {{ background: var(--surface); border: 1px solid var(--border); border-top: none; border-radius: 0 0 8px 8px; padding: 16px; }}

  /* Side-by-side faction panels */
  .faction-grid {{ display: grid; grid-template-columns: 1fr 1fr; gap: 16px; }}
  .faction-panel h3 {{ color: var(--muted); font-size: 0.8em; text-transform: uppercase; letter-spacing: 0.08em; margin-bottom: 8px; }}

  /* Transmute info */
  .transmute-info {{ background: #0d1b2a; border: 1px solid var(--border); border-radius: 6px; padding: 10px 12px; margin-bottom: 10px; font-size: 0.86em; }}
  .transmute-info .row {{ display: flex; justify-content: space-between; padding: 2px 0; }}
  .transmute-info .label {{ color: var(--muted); }}
  .transmute-info .value {{ color: var(--text); font-weight: 500; }}

  /* Tables */
  table {{ width: 100%; border-collapse: collapse; font-size: 0.84em; }}
  th {{ background: #0d1b2a; color: var(--muted); text-transform: uppercase; font-size: 0.78em; letter-spacing: 0.05em; padding: 6px 8px; text-align: left; position: sticky; top: 0; }}
  td {{ padding: 5px 8px; border-bottom: 1px solid #1e1e3a; }}
  tr:hover td {{ background: #1e2a3a; }}
  tr.best-cut td {{ background: rgba(78, 200, 80, 0.07); }}

  .positive {{ color: var(--positive); }}
  .negative {{ color: var(--negative); }}
  .neutral  {{ color: var(--neutral); }}
  .gold-val {{ color: var(--gold); }}
  .badge-best {{ background: var(--positive); color: #000; font-size: 0.7em; padding: 1px 5px; border-radius: 3px; margin-left: 4px; font-weight: 700; }}

  @media (max-width: 900px) {{
    .exec-summary, .faction-grid {{ grid-template-columns: 1fr; }}
  }}
</style>
</head>
<body>
<header>
  <h1>⚔️ Icecrown — Epic Gem JC Tracker</h1>
  <span class="updated">Last updated: {now}</span>
</header>
<div class="container">
"""

    # ── Executive Summary ──────────────────────────────────────────────────────
    html += '<div class="exec-summary">\n'
    for faction_key, faction_label, emoji in [("horde", "Horde", "🔴"), ("alli", "Alliance", "🔵")]:
        s = exec_sum[faction_key]
        html += f'<div class="exec-card">\n<h2>{emoji} {faction_label} — Executive Summary</h2>\n'

        # Transmutes worth doing
        html += '<h3>✅ Transmutes Worth Doing</h3>\n'
        if s["worthwhile_transmutes"]:
            for t in s["worthwhile_transmutes"]:
                margin_class = _profit_class(t["margin"])
                html += f'''<div class="exec-row">
  <span class="exec-gem">{t["color"]} {t["gem"]}</span>
  <span class="exec-val {margin_class}">{_profit_str(t["margin"])} profit</span>
</div>\n'''
        else:
            html += '<div class="exec-row"><span class="neutral">None currently profitable</span></div>\n'

        # Transmutes NOT worth doing
        html += '<h3>❌ Transmutes Not Worth Doing</h3>\n'
        if s["not_worthwhile_transmutes"]:
            for t in s["not_worthwhile_transmutes"]:
                html += f'''<div class="exec-row">
  <span class="exec-gem">{t["color"]} {t["gem"]}</span>
  <span class="exec-val negative">{_profit_str(t["margin"])} margin</span>
</div>\n'''
        else:
            html += '<div class="exec-row"><span class="neutral">All transmutes profitable</span></div>\n'

        # Best cuts
        html += '<h3>💎 Best Cut Per Color</h3>\n'
        for c in s["best_cuts"]:
            profit_class = _profit_class(c["profit"])
            html += f'''<div class="exec-row">
  <span class="exec-gem">{c["color"]} — {c["cut"]}</span>
  <span class="exec-val {profit_class}">{_profit_str(c["profit"])}</span>
</div>\n'''

        html += '</div>\n'  # end exec-card
    html += '</div>\n'  # end exec-summary

    # ── Per-Gem Sections ───────────────────────────────────────────────────────
    horde_groups = {g["epic_gem"]: g for g in analysis["horde"]["gem_groups"]}
    alli_groups  = {g["epic_gem"]: g for g in analysis["alli"]["gem_groups"]}

    for group_template in analysis["horde"]["gem_groups"]:
        gem_name = group_template["epic_gem"]
        color    = group_template["color"]
        h_grp    = horde_groups[gem_name]
        a_grp    = alli_groups[gem_name]

        html += f'''<div class="gem-section">
<div class="gem-header"><h2>{color} &nbsp; {gem_name}</h2></div>
<div class="gem-body">
<div class="faction-grid">
'''

        for faction_label, grp in [("🔴 Horde", h_grp), ("🔵 Alliance", a_grp)]:
            epic_price_str   = copper_to_gold(grp["epic_price"]) if grp["epic_price"] else "No data"
            xmute_cost_str   = copper_to_gold(grp["transmute_cost"]) if grp["transmute_cost"] else "No data"
            xmute_margin     = grp["transmute_margin"]
            xmute_class      = _profit_class(xmute_margin)
            xmute_margin_str = _profit_str(xmute_margin)

            html += f'<div class="faction-panel"><h3>{faction_label}</h3>\n'
            html += f'''<div class="transmute-info">
  <div class="row"><span class="label">Raw {gem_name}</span><span class="value gold-val">{epic_price_str}</span></div>
  <div class="row"><span class="label">Transmute Cost</span><span class="value">{xmute_cost_str}</span></div>
  <div class="row"><span class="label">Transmute Margin</span><span class="value {xmute_class}">{xmute_margin_str}</span></div>
'''
            # Mat breakdown
            for mat in grp["mat_breakdown"]:
                mat_total = copper_to_gold(mat["total"]) if mat["total"] else "N/A"
                html += f'  <div class="row"><span class="label">↳ {mat["qty"]}x {mat["name"]}</span><span class="value">{mat_total}</span></div>\n'
            html += '</div>\n'  # transmute-info

            # Cuts table
            html += '''<table>
<thead><tr>
  <th>Cut</th><th>Price</th><th>vs Raw</th><th>vs Transmute</th><th>Qty AH</th>
</tr></thead><tbody>\n'''

            for cut in grp["cuts"]:
                price_str = copper_to_gold(cut["price"]) if cut["price"] else "No data"
                p_raw     = cut["profit_vs_raw"]
                p_xmute   = cut["profit_vs_transmute"]
                is_best   = (cut["name"] == grp["best_cut"])
                row_class = ' class="best-cut"' if is_best else ""
                badge     = '<span class="badge-best">BEST</span>' if is_best else ""

                html += f'''<tr{row_class}>
  <td>{cut["name"]}{badge}</td>
  <td class="gold-val">{price_str}</td>
  <td class="{_profit_class(p_raw)}">{_profit_str(p_raw)}</td>
  <td class="{_profit_class(p_xmute)}">{_profit_str(p_xmute)}</td>
  <td class="neutral">{cut["qty_on_ah"] if cut["qty_on_ah"] is not None else "—"}</td>
</tr>\n'''

            html += '</tbody></table>\n'
            html += '</div>\n'  # faction-panel

        html += '</div>\n'  # faction-grid
        html += '</div>\n'  # gem-body
        html += '</div>\n'  # gem-section

    html += '</div></body></html>'
    return html


def save_html(analysis: dict, output_path: str = "docs/index.html"):
    import os
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    content = render_html(analysis)
    with open(output_path, "w", encoding="utf-8") as f:
        f.write(content)
    print(f"HTML saved to {output_path}")
