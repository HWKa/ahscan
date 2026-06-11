"""
Scraper for ah.nerfed.net — parses server-rendered HTML item pages.
Returns prices in COPPER. Use copper_to_gold() for display.
"""

import re
import time
import logging
from concurrent.futures import ThreadPoolExecutor, as_completed

import requests
from bs4 import BeautifulSoup

REALM = 15
BASE_URL = "https://ah.nerfed.net/item/index"
SESSION = requests.Session()
SESSION.headers.update({
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36",
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8",
    "Accept-Language": "en-US,en;q=0.9",
    "Accept-Encoding": "gzip, deflate, br",
    "Connection": "keep-alive",
})

def _init_session():
    """Hit the homepage once to get session cookies, then set Referer."""
    try:
        resp = SESSION.get("https://ah.nerfed.net/", timeout=10)
        SESSION.headers["Referer"] = "https://ah.nerfed.net/"
    except Exception:
        pass

_init_session()

logger = logging.getLogger(__name__)


def copper_to_gold(copper: int) -> str:
    """Convert raw copper integer to '123g 45s 67c' display string."""
    if copper is None:
        return "N/A"
    g = copper // 10000
    s = (copper % 10000) // 100
    c = copper % 100
    parts = []
    if g:
        parts.append(f"{g}g")
    if s:
        parts.append(f"{s}s")
    if c or not parts:
        parts.append(f"{c}c")
    return " ".join(parts)


def copper_to_gold_float(copper: int) -> float:
    """Convert copper to fractional gold for sorting / arithmetic."""
    if copper is None:
        return 0.0
    return copper / 10000.0


def fetch_item(item_id: int, faction: int, retries: int = 3) -> dict:
    """
    Fetch one item page and return a dict with price fields.
    All monetary values are in copper (int) or None if unavailable.
    """
    url = BASE_URL
    params = {"id": item_id, "realm": REALM, "faction": faction}

    for attempt in range(retries):
        try:
            resp = SESSION.get(url, params=params, timeout=15)
            resp.raise_for_status()
            return _parse_item_page(resp.text, item_id, faction)
        except Exception as e:
            if attempt < retries - 1:
                time.sleep(2 ** attempt)
            else:
                logger.warning(f"Failed to fetch item {item_id} faction {faction}: {e}")
                return _empty_result(item_id, faction)


def _parse_item_page(html: str, item_id: int, faction: int) -> dict:
    soup = BeautifulSoup(html, "html.parser")

    result = {
        "item_id": item_id,
        "faction": faction,
        "name": None,
        "fetched_at": None,
        "qty_on_ah": None,
        "min_buyout": None,
        "avg_buyout": None,
        "median_buyout": None,
        "min_bid": None,
        "avg_bid": None,
        "median_bid": None,
        "cost_price": None,   # site's calculated crafting cost
    }

    # Item name from h1/title area
    title_tag = soup.find("title")
    if title_tag:
        m = re.match(r"^(.+?) Price Analysis", title_tag.text)
        if m:
            result["name"] = m.group(1).strip()

    # Parse the stats table — rows are label | value pairs
    label_map = {
        "Data Fetched at":       "fetched_at",
        "Quantity On AH":        "qty_on_ah",
        "Minimum Buyout Price":  "min_buyout",
        "Average Buyout Price":  "avg_buyout",
        "Median Buyout Price":   "median_buyout",
        "Minimum Bid Price":     "min_bid",
        "Average Bid Price":     "avg_bid",
        "Median Bid Price":      "median_bid",
        "Cost Price":            "cost_price",
    }

    for row in soup.select("table tr"):
        cells = row.find_all(["td", "th"])
        if len(cells) == 2:
            label = cells[0].get_text(strip=True)
            value = cells[1].get_text(strip=True)
            key = label_map.get(label)
            if key:
                if key == "fetched_at":
                    result[key] = value
                elif key == "qty_on_ah":
                    try:
                        result[key] = int(value)
                    except ValueError:
                        result[key] = 0
                else:
                    # Copper values — plain integers on the site
                    try:
                        result[key] = int(re.sub(r"[^\d]", "", value)) if value else None
                    except ValueError:
                        result[key] = None

    return result


def _empty_result(item_id: int, faction: int) -> dict:
    return {
        "item_id": item_id, "faction": faction,
        "name": f"Item #{item_id}", "fetched_at": None,
        "qty_on_ah": None,
        "min_buyout": None, "avg_buyout": None, "median_buyout": None,
        "min_bid": None,    "avg_bid": None,    "median_bid": None,
        "cost_price": None,
    }


def fetch_all_items(item_ids: list[int], faction: int, max_workers: int = 8) -> dict[int, dict]:
    """
    Fetch multiple items in parallel.
    Returns dict keyed by item_id.
    """
    results = {}
    with ThreadPoolExecutor(max_workers=max_workers) as executor:
        future_to_id = {
            executor.submit(fetch_item, iid, faction): iid
            for iid in item_ids
        }
        for future in as_completed(future_to_id):
            iid = future_to_id[future]
            results[iid] = future.result()
            # polite delay - random small sleep handled per-thread implicitly
    return results
