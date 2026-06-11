"""
Main entry point. Run this script to:
1. Fetch all item prices (Horde + Alliance, in parallel)
2. Run profit analysis
3. Generate static HTML page (docs/index.html for GitHub Pages)
4. Send email report

Usage:
    python main.py              # full run (html + email)
    python main.py --html-only  # skip email
    python main.py --dry-run    # print analysis, no files written
"""

import argparse
import logging
import sys
import time

from items import GEM_GROUPS, TRANSMUTE_MATS
from scraper import fetch_all_items
from analysis import build_analysis
from render_html import save_html
from render_email import render_email
from mailer import send_email

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    handlers=[logging.StreamHandler(sys.stdout)]
)
logger = logging.getLogger(__name__)


def collect_all_item_ids() -> list[int]:
    """Build the complete list of item IDs we need to fetch."""
    ids = set()

    for group in GEM_GROUPS:
        # Epic gem itself
        ids.add(group["epic_gem_id"])
        # Transmute mats
        for mat_name, qty in group["transmute_mats"]:
            ids.add(TRANSMUTE_MATS[mat_name])
        # All cuts
        for cut_name, cut_id in group["cuts"].items():
            ids.add(cut_id)

    return sorted(ids)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--html-only", action="store_true", help="Skip email send")
    parser.add_argument("--dry-run",   action="store_true", help="Print only, write nothing")
    args = parser.parse_args()

    all_ids = collect_all_item_ids()
    logger.info(f"Fetching {len(all_ids)} unique items × 2 factions = {len(all_ids)*2} pages...")

    t0 = time.time()

    logger.info("Fetching Horde prices (faction=0)...")
    prices_horde = fetch_all_items(all_ids, faction=0, max_workers=8)

    logger.info("Fetching Alliance prices (faction=1)...")
    prices_alli  = fetch_all_items(all_ids, faction=1, max_workers=8)

    elapsed = time.time() - t0
    logger.info(f"Fetch complete in {elapsed:.1f}s")

    logger.info("Running analysis...")
    analysis = build_analysis(prices_horde, prices_alli)

    # ── Print executive summary to console ────────────────────────────────────
    for faction_key in ("horde", "alli"):
        s = analysis["executive_summary"][faction_key]
        print(f"\n{'='*50}")
        print(f"  {s['faction'].upper()} SUMMARY")
        print(f"{'='*50}")

        print("\n✅ TRANSMUTES WORTH DOING:")
        for t in s["worthwhile_transmutes"]:
            print(f"  {t['color']} {t['gem']:20s} margin: {t['margin_gold']}")

        print("\n❌ TRANSMUTES NOT WORTH IT:")
        for t in s["not_worthwhile_transmutes"]:
            print(f"  {t['color']} {t['gem']:20s} margin: {t['margin_gold']}")

        print("\n💎 BEST CUT PER COLOR:")
        for c in s["best_cuts"]:
            print(f"  {c['color']} {c['cut']:35s} profit: {c['profit_gold']}")

    if args.dry_run:
        logger.info("Dry run — not writing files.")
        return

    # ── Write HTML ─────────────────────────────────────────────────────────────
    save_html(analysis, output_path="docs/index.html")

    # ── Send Email ─────────────────────────────────────────────────────────────
    if not args.html_only:
        logger.info("Generating email body...")
        email_body = render_email(analysis)
        send_email(email_body)
    else:
        logger.info("--html-only set, skipping email.")


if __name__ == "__main__":
    main()
