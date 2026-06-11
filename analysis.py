"""
Analysis logic: combines raw price data into profit calculations,
transmute ROI, and per-color summaries for both factions.
"""

from items import GEM_GROUPS, TRANSMUTE_MATS
from scraper import copper_to_gold, copper_to_gold_float


def build_analysis(prices_horde: dict, prices_alli: dict) -> dict:
    """
    prices_horde / prices_alli: {item_id: price_dict} from scraper.fetch_all_items()
    Returns a structured analysis dict used by both HTML and email renderers.
    """
    analysis = {
        "horde": _analyze_faction(prices_horde, faction_label="Horde"),
        "alli":  _analyze_faction(prices_alli,  faction_label="Alliance"),
    }
    analysis["executive_summary"] = _executive_summary(analysis)
    return analysis


def _get_median_buyout(prices: dict, item_id: int) -> int | None:
    """Safely get median buyout in copper."""
    data = prices.get(item_id)
    if not data:
        return None
    return data.get("median_buyout")


def _analyze_faction(prices: dict, faction_label: str) -> dict:
    result = {"faction": faction_label, "gem_groups": []}

    for group in GEM_GROUPS:
        epic_id   = group["epic_gem_id"]
        epic_name = group["epic_gem"]
        epic_price = _get_median_buyout(prices, epic_id)

        # Transmute cost = sum of mat prices
        transmute_cost = _calc_transmute_cost(prices, group["transmute_mats"])
        transmute_margin = None
        if transmute_cost is not None and epic_price is not None:
            transmute_margin = epic_price - transmute_cost

        # Mat breakdown for display
        mat_breakdown = []
        for mat_name, qty in group["transmute_mats"]:
            mat_id    = TRANSMUTE_MATS[mat_name]
            mat_price = _get_median_buyout(prices, mat_id)
            mat_breakdown.append({
                "name":       mat_name,
                "qty":        qty,
                "unit_price": mat_price,
                "total":      (mat_price * qty) if mat_price else None,
            })

        # Cuts analysis
        cuts = []
        best_cut = None
        best_cut_profit = None

        for cut_name, cut_id in group["cuts"].items():
            cut_price = _get_median_buyout(prices, cut_id)
            cut_data  = prices.get(cut_id, {})

            # Profit vs raw epic gem
            profit_vs_raw = None
            if cut_price is not None and epic_price is not None:
                profit_vs_raw = cut_price - epic_price

            # Profit vs transmute cost
            profit_vs_transmute = None
            if cut_price is not None and transmute_cost is not None:
                profit_vs_transmute = cut_price - transmute_cost

            cuts.append({
                "name":                 cut_name,
                "item_id":              cut_id,
                "price":                cut_price,
                "qty_on_ah":            cut_data.get("qty_on_ah"),
                "profit_vs_raw":        profit_vs_raw,
                "profit_vs_transmute":  profit_vs_transmute,
                "fetched_at":           cut_data.get("fetched_at"),
            })

            if profit_vs_raw is not None:
                if best_cut_profit is None or profit_vs_raw > best_cut_profit:
                    best_cut_profit = profit_vs_raw
                    best_cut = cut_name

        # Sort cuts by profit_vs_raw descending (None last)
        cuts.sort(key=lambda x: x["profit_vs_raw"] if x["profit_vs_raw"] is not None else -999999, reverse=True)

        result["gem_groups"].append({
            "color":              group["color"],
            "epic_gem":           epic_name,
            "epic_gem_id":        epic_id,
            "epic_price":         epic_price,
            "epic_data":          prices.get(epic_id, {}),
            "transmute_cost":     transmute_cost,
            "transmute_margin":   transmute_margin,
            "mat_breakdown":      mat_breakdown,
            "cuts":               cuts,
            "best_cut":           best_cut,
            "best_cut_profit":    best_cut_profit,
        })

    return result


def _calc_transmute_cost(prices: dict, mat_list: list) -> int | None:
    """Sum of (qty * median_buyout) for each material. Returns None if any price missing."""
    total = 0
    for mat_name, qty in mat_list:
        mat_id = TRANSMUTE_MATS[mat_name]
        price  = _get_median_buyout(prices, mat_id)
        if price is None:
            return None
        total += price * qty
    return total


def _executive_summary(analysis: dict) -> dict:
    """
    Build per-faction executive summary:
    - Which transmutes are worth doing (positive margin)
    - Best cut per gem color
    """
    summary = {}
    for faction_key in ("horde", "alli"):
        faction_data = analysis[faction_key]
        faction_label = faction_data["faction"]

        worthwhile_transmutes = []
        not_worthwhile_transmutes = []
        best_cuts = []

        for grp in faction_data["gem_groups"]:
            gem = grp["epic_gem"]
            color = grp["color"]

            # Transmute assessment
            margin = grp["transmute_margin"]
            if margin is not None:
                entry = {
                    "gem":            gem,
                    "color":          color,
                    "margin":         margin,
                    "margin_gold":    copper_to_gold(margin),
                    "epic_price":     grp["epic_price"],
                    "transmute_cost": grp["transmute_cost"],
                }
                if margin > 0:
                    worthwhile_transmutes.append(entry)
                else:
                    not_worthwhile_transmutes.append(entry)

            # Best cut
            if grp["best_cut"] and grp["best_cut_profit"] is not None:
                best_cuts.append({
                    "gem":          gem,
                    "color":        color,
                    "cut":          grp["best_cut"],
                    "profit":       grp["best_cut_profit"],
                    "profit_gold":  copper_to_gold(grp["best_cut_profit"]),
                })

        # Sort by descending margin / profit
        worthwhile_transmutes.sort(key=lambda x: x["margin"], reverse=True)
        not_worthwhile_transmutes.sort(key=lambda x: x["margin"], reverse=True)
        best_cuts.sort(key=lambda x: x["profit"], reverse=True)

        summary[faction_key] = {
            "faction":                    faction_label,
            "worthwhile_transmutes":      worthwhile_transmutes,
            "not_worthwhile_transmutes":  not_worthwhile_transmutes,
            "best_cuts":                  best_cuts,
        }

    return summary
