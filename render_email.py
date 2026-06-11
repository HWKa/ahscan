"""
Generates an HTML email body from the analysis dict.
Designed for Gmail/Outlook compatibility (inline styles, table layout).
"""

from datetime import datetime, timezone
from scraper import copper_to_gold


def _profit_color(profit):
    if profit is None:
        return "#888"
    return "#4caf50" if profit >= 0 else "#f44336"


def _ps(profit):
    if profit is None:
        return "N/A"
    sign = "+" if profit >= 0 else ""
    return f"{sign}{copper_to_gold(profit)}"


def render_email(analysis: dict) -> str:
    now = datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M UTC")

    rows = []
    rows.append(f"""
<html><body style="margin:0;padding:0;background:#1a1a2e;font-family:Arial,sans-serif;color:#eaeaea;">
<table width="100%" cellpadding="0" cellspacing="0" style="max-width:900px;margin:0 auto;">
<tr><td style="background:#0f3460;padding:16px 20px;border-bottom:2px solid #e94560;">
  <h1 style="margin:0;color:#ffd700;font-size:1.3em;">⚔️ Icecrown AH — Epic Gem Report</h1>
  <p style="margin:4px 0 0;color:#888;font-size:0.82em;">{now}</p>
</td></tr>
""")

    # ── Executive Summary ─────────────────────────────────────────────────────
    exec_sum = analysis["executive_summary"]

    rows.append("""<tr><td style="padding:16px 20px;">
<table width="100%" cellspacing="0" cellpadding="0"><tr>""")

    for faction_key, faction_label, emoji in [("horde", "Horde", "🔴"), ("alli", "Alliance", "🔵")]:
        s = exec_sum[faction_key]
        rows.append(f"""<td width="50%" valign="top" style="padding:0 8px 0 0;">
<table width="100%" cellpadding="6" cellspacing="0" style="background:#16213e;border-radius:6px;border:1px solid #2a2a4a;">
<tr><td colspan="2" style="background:#0f3460;padding:8px 12px;border-radius:6px 6px 0 0;">
  <strong style="color:#ffd700;">{emoji} {faction_label} Summary</strong>
</td></tr>
<tr><td colspan="2" style="padding:4px 12px;color:#e94560;font-size:0.8em;font-weight:bold;text-transform:uppercase;letter-spacing:0.05em;">
  ✅ Transmutes Worth Doing
</td></tr>""")
        if s["worthwhile_transmutes"]:
            for t in s["worthwhile_transmutes"]:
                c = _profit_color(t["margin"])
                rows.append(f"""<tr>
  <td style="padding:3px 12px;font-size:0.86em;">{t["color"]} {t["gem"]}</td>
  <td style="padding:3px 12px;color:{c};font-size:0.86em;text-align:right;font-weight:600;">{_ps(t["margin"])}</td>
</tr>""")
        else:
            rows.append('<tr><td colspan="2" style="padding:3px 12px;color:#888;font-size:0.85em;">None currently profitable</td></tr>')

        rows.append("""<tr><td colspan="2" style="padding:4px 12px;color:#e94560;font-size:0.8em;font-weight:bold;text-transform:uppercase;letter-spacing:0.05em;">
  💎 Best Cut Per Color
</td></tr>""")
        for c_item in s["best_cuts"]:
            c = _profit_color(c_item["profit"])
            rows.append(f"""<tr>
  <td style="padding:3px 12px;font-size:0.84em;">{c_item["color"]} — {c_item["cut"]}</td>
  <td style="padding:3px 12px;color:{c};font-size:0.84em;text-align:right;font-weight:600;">{_ps(c_item["profit"])}</td>
</tr>""")

        rows.append("</table></td>")

    rows.append("</tr></table></td></tr>")

    # ── Per-Gem Detail ─────────────────────────────────────────────────────────
    horde_groups = {g["epic_gem"]: g for g in analysis["horde"]["gem_groups"]}
    alli_groups  = {g["epic_gem"]: g for g in analysis["alli"]["gem_groups"]}

    for gem_template in analysis["horde"]["gem_groups"]:
        gem_name = gem_template["epic_gem"]
        color    = gem_template["color"]
        h_grp    = horde_groups[gem_name]
        a_grp    = alli_groups[gem_name]

        rows.append(f"""<tr><td style="padding:12px 20px 0;">
<table width="100%" cellpadding="0" cellspacing="0">
<tr><td style="background:#0f3460;padding:8px 12px;border-radius:6px 6px 0 0;border-bottom:2px solid #e94560;">
  <strong style="color:#ffd700;">{color} &nbsp; {gem_name}</strong>
</td></tr>
<tr><td style="background:#16213e;border:1px solid #2a2a4a;border-top:none;border-radius:0 0 6px 6px;padding:12px;">
<table width="100%" cellpadding="0" cellspacing="0"><tr>""")

        for faction_label, grp in [("🔴 Horde", h_grp), ("🔵 Alliance", a_grp)]:
            ep   = copper_to_gold(grp["epic_price"]) if grp["epic_price"] else "N/A"
            xm   = copper_to_gold(grp["transmute_cost"]) if grp["transmute_cost"] else "N/A"
            xmm  = grp["transmute_margin"]
            xmmc = _profit_color(xmm)

            rows.append(f"""<td width="50%" valign="top" style="padding:0 6px;">
<p style="color:#888;font-size:0.78em;text-transform:uppercase;font-weight:bold;margin:0 0 6px;">{faction_label}</p>
<table width="100%" cellpadding="3" cellspacing="0" style="background:#0d1b2a;border-radius:4px;margin-bottom:8px;font-size:0.83em;">
  <tr><td style="color:#888;">Raw {gem_name}</td><td style="color:#ffd700;text-align:right;">{ep}</td></tr>
  <tr><td style="color:#888;">Transmute cost</td><td style="text-align:right;">{xm}</td></tr>
  <tr><td style="color:#888;">Transmute margin</td><td style="color:{xmmc};text-align:right;font-weight:bold;">{_ps(xmm)}</td></tr>
</table>
<table width="100%" cellpadding="3" cellspacing="0" style="font-size:0.82em;">
<thead><tr style="background:#0d1b2a;">
  <th style="text-align:left;color:#666;font-weight:normal;padding:4px 6px;">Cut</th>
  <th style="text-align:right;color:#666;font-weight:normal;padding:4px 6px;">Price</th>
  <th style="text-align:right;color:#666;font-weight:normal;padding:4px 6px;">vs Raw</th>
  <th style="text-align:right;color:#666;font-weight:normal;padding:4px 6px;">vs Xmute</th>
</tr></thead><tbody>""")

            for cut in grp["cuts"][:10]:  # email: top 10 cuts per gem to keep manageable
                is_best = (cut["name"] == grp["best_cut"])
                name_str = f'<strong>{cut["name"]} ★</strong>' if is_best else cut["name"]
                p_raw   = _ps(cut["profit_vs_raw"])
                p_xmute = _ps(cut["profit_vs_transmute"])
                c_raw   = _profit_color(cut["profit_vs_raw"])
                c_xmute = _profit_color(cut["profit_vs_transmute"])
                price_str = copper_to_gold(cut["price"]) if cut["price"] else "N/A"
                bg = "background:#0e2010;" if is_best else ""
                rows.append(f"""<tr style="{bg}">
  <td style="padding:3px 6px;">{name_str}</td>
  <td style="text-align:right;color:#ffd700;padding:3px 6px;">{price_str}</td>
  <td style="text-align:right;color:{c_raw};padding:3px 6px;">{p_raw}</td>
  <td style="text-align:right;color:{c_xmute};padding:3px 6px;">{p_xmute}</td>
</tr>""")

            rows.append("</tbody></table></td>")

        rows.append("</tr></table></td></tr></table></td></tr>")

    rows.append("</table></body></html>")
    return "\n".join(rows)
