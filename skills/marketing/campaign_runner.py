#!/usr/bin/env python3
"""
Marketing Campaign Orchestrator
Runs full AI-powered marketing campaigns for all managed brands.

Usage:
    python campaign_runner.py --all
    python campaign_runner.py --brand TheFlavorCrave
    python campaign_runner.py --brand HealthIsWealth --mode content
    python campaign_runner.py --all --output report.json
    python campaign_runner.py --list-brands
"""

import argparse
import json
import logging
import os
import sys
from datetime import datetime
from pathlib import Path
from typing import List, Dict, Any, Optional

import anthropic

# Allow running from this directory
sys.path.insert(0, str(Path(__file__).parent))

from brands import BRANDS, ALL_BRAND_NAMES, Brand
from trend_scanner import scan_trends_for_brand, scan_all_brands, pick_top_roi_brands
from content_generator import generate_all_content
from ad_creator import generate_ads
from seo_optimizer import optimize_seo
from scaling_advisor import get_scaling_plan

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s  %(levelname)-8s  %(message)s",
    datefmt="%H:%M:%S",
)
logger = logging.getLogger(__name__)

MODES = ["full", "content", "ads", "seo", "trends", "scaling"]


def run_campaign_for_brand(
    brand: Brand,
    client: anthropic.Anthropic,
    mode: str = "full",
) -> Dict[str, Any]:
    """Run a full or partial marketing campaign for one brand."""
    logger.info("=" * 60)
    logger.info("Running %s campaign for: %s", mode.upper(), brand.name)
    logger.info("Site: %s", brand.url or "N/A")
    logger.info("=" * 60)

    result: Dict[str, Any] = {
        "brand": brand.name,
        "url": brand.url,
        "mode": mode,
        "timestamp": datetime.utcnow().isoformat(),
        "selected_brands": [brand.name],
        "strategy": "",
        "content": {"tiktok_scripts": [], "pinterest_posts": [], "blog_update": ""},
        "ads": {"primary": "", "hooks": [], "ctas": []},
        "seo": {},
        "scaling": "",
        "automation": "",
        "revenue_opportunity": "",
    }

    # 1. Trend scan (always needed for other modules)
    trend_data: Dict[str, Any] = {}
    if mode in ("full", "trends", "content", "ads", "seo", "scaling"):
        logger.info("[1/5] Scanning market trends...")
        trend_data = scan_trends_for_brand(brand, client)
        result["strategy"] = _build_strategy_summary(brand, trend_data)

    if mode == "trends":
        result["trends"] = trend_data
        return result

    trend_topics = [t["topic"] for t in trend_data.get("top_trends", [])]

    # 2. Content generation
    if mode in ("full", "content"):
        logger.info("[2/5] Generating content...")
        content = generate_all_content(brand, trend_data, client)
        result["content"] = content

    # 3. Ad copy
    if mode in ("full", "ads"):
        logger.info("[3/5] Generating ad copy...")
        ads = generate_ads(brand, trend_topics, client)
        result["ads"] = {
            "primary": ads.get("primary", {}).get("headline", ""),
            "hooks": ads.get("hooks", []),
            "ctas": ads.get("ctas", []),
            "full_ads": ads,
        }

    # 4. SEO optimization
    if mode in ("full", "seo"):
        logger.info("[4/5] Generating SEO plan...")
        seo = optimize_seo(brand, trend_topics, client)
        result["seo"] = seo

    # 5. Scaling + automation advice
    if mode in ("full", "scaling"):
        logger.info("[5/5] Building scaling plan...")
        scaling = get_scaling_plan(
            brand,
            result["content"],
            result.get("ads", {}).get("full_ads", {}),
            client,
        )
        result["scaling"] = scaling.get("top_scaling_moves", [])
        result["automation"] = scaling.get("automation", {}).get("workflow_to_automate", "")
        result["revenue_opportunity"] = scaling.get("revenue_opportunity", {}).get("immediate_win", "")
        result["full_scaling"] = scaling

    logger.info("Campaign complete for %s", brand.name)
    return result


def run_all_brands(
    client: anthropic.Anthropic,
    mode: str = "full",
    pick_top: Optional[int] = None,
) -> Dict[str, Any]:
    """Run campaigns for all brands, optionally picking only top ROI brands."""
    logger.info("Scanning trends for all brands to identify top opportunities...")

    if pick_top:
        trend_results = scan_all_brands(client)
        selected = pick_top_roi_brands(trend_results, count=pick_top)
        logger.info("Top %d brands by ROI: %s", pick_top, ", ".join(selected))
    else:
        selected = ALL_BRAND_NAMES

    all_results = {}
    for brand_name in selected:
        brand = BRANDS[brand_name]
        try:
            all_results[brand_name] = run_campaign_for_brand(brand, client, mode)
        except Exception as e:
            logger.error("Campaign failed for %s: %s", brand_name, e)
            all_results[brand_name] = {"brand": brand_name, "error": str(e)}

    return {
        "campaign_run": datetime.utcnow().isoformat(),
        "mode": mode,
        "brands_processed": selected,
        "results": all_results,
    }


def _build_strategy_summary(brand: Brand, trend_data: Dict) -> str:
    top = trend_data.get("top_trends", [])[:2]
    topics = " and ".join(t["topic"] for t in top) if top else brand.content_pillars[0]
    gap = trend_data.get("competitor_gap", "")
    seasonal = trend_data.get("seasonal_opportunity", "")
    parts = [f"Focus on {topics} to maximize reach."]
    if gap:
        parts.append(f"Exploit competitor gap: {gap}.")
    if seasonal:
        parts.append(f"Seasonal opportunity: {seasonal}.")
    return " ".join(parts)


def save_report(data: Dict, output_path: str) -> None:
    Path(output_path).parent.mkdir(parents=True, exist_ok=True)
    with open(output_path, "w") as f:
        json.dump(data, f, indent=2, default=str)
    logger.info("Report saved to %s", output_path)


def print_summary(result: Dict) -> None:
    """Print a human-readable campaign summary to stdout."""
    print("\n" + "=" * 70)
    print(f"  CAMPAIGN REPORT: {result.get('brand', 'All Brands')}")
    print("=" * 70)

    if "results" in result:
        # Multi-brand report
        for brand_name, data in result["results"].items():
            print(f"\n{'─'*40}")
            print(f"  {brand_name}")
            print(f"  Site: {data.get('url', 'N/A')}")
            if "error" in data:
                print(f"  ERROR: {data['error']}")
            else:
                print(f"  Strategy: {data.get('strategy', '')[:120]}...")
                rev = data.get("revenue_opportunity", "")
                if rev:
                    print(f"  Revenue Opportunity: {rev[:100]}")
    else:
        # Single brand report
        print(f"\nBrand:    {result.get('brand')}")
        print(f"URL:      {result.get('url', 'N/A')}")
        print(f"Strategy: {result.get('strategy', '')}")
        content = result.get("content", {})
        scripts = content.get("tiktok_scripts", [])
        if scripts:
            print(f"\nTikTok Scripts Generated: {len(scripts)}")
            print(f"  Top Hook: {scripts[0].get('hook', '')[:80]}")
        ads = result.get("ads", {})
        hooks = ads.get("hooks", [])
        if hooks:
            print(f"\nAd Hooks: {len(hooks)}")
            print(f"  Top Hook: {hooks[0][:80]}")
        rev = result.get("revenue_opportunity", "")
        if rev:
            print(f"\nRevenue Opportunity: {rev}")
        auto = result.get("automation", "")
        if auto:
            print(f"\nAutomation Priority: {auto[:120]}")

    print("\n" + "=" * 70 + "\n")


def main():
    parser = argparse.ArgumentParser(
        description="AI Marketing Campaign Runner for all managed brands",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python campaign_runner.py --all
  python campaign_runner.py --all --pick-top 2
  python campaign_runner.py --brand TheFlavorCrave
  python campaign_runner.py --brand HealthIsWealth --mode content
  python campaign_runner.py --all --mode ads --output ads_report.json
  python campaign_runner.py --list-brands
        """,
    )
    parser.add_argument("--all", action="store_true", help="Run for all brands")
    parser.add_argument("--brand", type=str, help="Run for a specific brand")
    parser.add_argument(
        "--mode",
        choices=MODES,
        default="full",
        help="Campaign mode (default: full)",
    )
    parser.add_argument(
        "--pick-top",
        type=int,
        metavar="N",
        help="Auto-select top N brands by ROI from trend scan",
    )
    parser.add_argument("--output", type=str, help="Save JSON report to file")
    parser.add_argument("--list-brands", action="store_true", help="List all managed brands")
    args = parser.parse_args()

    if args.list_brands:
        print("\nManaged Brands:")
        for name, brand in BRANDS.items():
            print(f"  • {brand.name:25s} {brand.url}")
        return

    api_key = os.environ.get("ANTHROPIC_API_KEY")
    if not api_key:
        logger.error("ANTHROPIC_API_KEY environment variable not set.")
        sys.exit(1)

    client = anthropic.Anthropic(api_key=api_key)

    if args.all:
        result = run_all_brands(client, mode=args.mode, pick_top=args.pick_top)
    elif args.brand:
        brand = BRANDS.get(args.brand)
        if not brand:
            logger.error("Unknown brand: %s. Use --list-brands to see options.", args.brand)
            sys.exit(1)
        result = run_campaign_for_brand(brand, client, mode=args.mode)
    else:
        parser.print_help()
        sys.exit(0)

    print_summary(result)

    if args.output:
        save_report(result, args.output)
    else:
        timestamp = datetime.utcnow().strftime("%Y%m%d_%H%M%S")
        brand_slug = args.brand.lower().replace(" ", "_") if args.brand else "all_brands"
        default_output = f"reports/{brand_slug}_{args.mode}_{timestamp}.json"
        save_report(result, default_output)


if __name__ == "__main__":
    main()
