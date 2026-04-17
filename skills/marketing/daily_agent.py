#!/usr/bin/env python3
"""
AUTONOMOUS MARKETING & REVENUE AGENT — DAILY EXECUTION ENGINE
Runs daily loops across all 7 brands to generate traffic, content, and revenue.

Execution model:
    LOOP: DAILY()
      → scan_market_trends()
      → pick_top_roi(brands, 2)
      → generate_content(selected)
      → create_ads(selected)
      → optimize_pages(selected)
      → multiply_content(content)
      → decide_scaling(content, ads)
      → suggest_automation()
      → save_report()

Usage:
    python daily_agent.py              # Run once immediately
    python daily_agent.py --dry-run    # Print plan without calling API
    python daily_agent.py --brand TheFlavorCrave  # Single brand full loop
    python daily_agent.py --all        # All brands full loop
"""

import argparse
import json
import logging
import os
import sys
import time
from datetime import datetime, date
from pathlib import Path
from typing import Dict, Any, List, Optional

import anthropic

sys.path.insert(0, str(Path(__file__).parent))

from brands import BRANDS, ALL_BRAND_NAMES, Brand
from trend_scanner import scan_all_brands, pick_top_roi_brands, scan_trends_for_brand
from content_generator import generate_all_content
from ad_creator import generate_ads
from seo_optimizer import optimize_seo
from content_multiplier import multiply_content
from scaling_advisor import get_scaling_plan

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s  %(levelname)-8s  %(name)s  %(message)s",
    datefmt="%H:%M:%S",
)
logger = logging.getLogger("DailyAgent")

REPORTS_DIR = Path(__file__).parent / "reports"
STATE_FILE = Path(__file__).parent / "agent_state.json"


# ─── State Management ──────────────────────────────────────────────────────────

def load_state() -> Dict[str, Any]:
    if STATE_FILE.exists():
        with open(STATE_FILE) as f:
            return json.load(f)
    return {
        "total_runs": 0,
        "last_run": None,
        "brand_stats": {name: {"runs": 0, "last_content": None} for name in ALL_BRAND_NAMES},
        "revenue_log": [],
        "goals": {
            "monthly_target_usd": 10000,
            "current_month_usd": 0,
            "traffic_target_daily": 1000,
        },
    }


def save_state(state: Dict[str, Any]) -> None:
    STATE_FILE.parent.mkdir(parents=True, exist_ok=True)
    with open(STATE_FILE, "w") as f:
        json.dump(state, f, indent=2, default=str)


# ─── Daily Loop ────────────────────────────────────────────────────────────────

def run_daily_loop(
    client: anthropic.Anthropic,
    brand_names: Optional[List[str]] = None,
    pick_top: int = 2,
    dry_run: bool = False,
) -> Dict[str, Any]:
    """Main DAILY() execution loop."""
    run_start = datetime.utcnow()
    state = load_state()
    state["total_runs"] += 1
    state["last_run"] = run_start.isoformat()

    logger.info("━" * 70)
    logger.info("  AUTONOMOUS MARKETING AGENT — DAILY LOOP #%d", state["total_runs"])
    logger.info("  %s", run_start.strftime("%A %B %d, %Y at %H:%M UTC"))
    logger.info("━" * 70)

    if dry_run:
        logger.info("[DRY RUN] Printing plan only — no API calls.")
        return _print_dry_run_plan(brand_names or ALL_BRAND_NAMES, pick_top)

    # ── Step 1: Scan trends for all brands ──
    logger.info("\n[STEP 1] scan_market_trends() — scanning all 7 brands")
    targets = brand_names or ALL_BRAND_NAMES
    all_trend_data: Dict[str, Any] = {}
    for name in targets:
        brand = BRANDS[name]
        logger.info("  → Scanning trends: %s", name)
        try:
            all_trend_data[name] = scan_trends_for_brand(brand, client)
        except Exception as e:
            logger.warning("  ✗ Trend scan failed for %s: %s", name, e)
            all_trend_data[name] = {"error": str(e), "top_trends": []}

    # ── Step 2: Pick top ROI brands ──
    logger.info("\n[STEP 2] pick_top_roi(%d) — selecting highest opportunity brands", pick_top)
    if brand_names:
        selected_brands = brand_names
    else:
        selected_brands = pick_top_roi_brands(all_trend_data, count=pick_top)
    logger.info("  → Selected: %s", ", ".join(selected_brands))

    daily_results: Dict[str, Any] = {
        "run_id": f"daily_{run_start.strftime('%Y%m%d_%H%M%S')}",
        "timestamp": run_start.isoformat(),
        "selected_brands": selected_brands,
        "brand_campaigns": {},
    }

    for brand_name in selected_brands:
        brand = BRANDS.get(brand_name)
        if not brand:
            continue

        trend_data = all_trend_data.get(brand_name, {})
        trend_topics = [t["topic"] for t in trend_data.get("top_trends", [])]
        logger.info("\n  ╔══ %s ══╗", brand_name.upper())
        logger.info("  URL: %s", brand.url)

        campaign: Dict[str, Any] = {
            "brand": brand_name,
            "url": brand.url,
            "trends": trend_data,
            "strategy": _build_strategy(brand, trend_data),
            "selected_brands": [brand_name],
        }

        # ── Step 3: Generate content ──
        logger.info("  [STEP 3] generate_content()")
        try:
            content = generate_all_content(brand, trend_data, client)
            campaign["content"] = content
            logger.info("    ✓ %d TikTok scripts, %d Pinterest posts, 1 blog draft",
                        len(content.get("tiktok_scripts", [])),
                        len(content.get("pinterest_posts", [])))
        except Exception as e:
            logger.warning("    ✗ Content generation failed: %s", e)
            campaign["content"] = {"tiktok_scripts": [], "pinterest_posts": [], "blog_update": ""}

        # ── Step 4: Create ads ──
        logger.info("  [STEP 4] create_ads()")
        try:
            ads = generate_ads(brand, trend_topics, client)
            campaign["ads"] = {
                "primary": ads.get("primary", {}).get("headline", ""),
                "hooks": ads.get("hooks", []),
                "ctas": ads.get("ctas", []),
                "full": ads,
            }
            logger.info("    ✓ 1 primary ad, %d hooks, %d CTAs",
                        len(ads.get("hooks", [])), len(ads.get("ctas", [])))
        except Exception as e:
            logger.warning("    ✗ Ad creation failed: %s", e)
            campaign["ads"] = {"primary": "", "hooks": [], "ctas": []}

        # ── Step 5: Optimize pages (SEO) ──
        logger.info("  [STEP 5] optimize_pages()")
        try:
            seo = optimize_seo(brand, trend_topics, client)
            campaign["seo"] = seo
            quick_wins = len(seo.get("quick_wins", []))
            logger.info("    ✓ SEO plan ready — %d quick wins identified", quick_wins)
        except Exception as e:
            logger.warning("    ✗ SEO optimization failed: %s", e)
            campaign["seo"] = {}

        # ── Step 6: Multiply content ──
        logger.info("  [STEP 6] multiply_content()")
        try:
            scripts = campaign["content"].get("tiktok_scripts", [])
            if scripts:
                source = scripts[0].get("script", scripts[0].get("hook", ""))
                multiplied = multiply_content(brand, source, "tiktok_script", client)
                campaign["repurposed"] = multiplied
                total = multiplied.get("total_pieces_generated", 0)
                logger.info("    ✓ 1 piece → %d platform variants", total)
            else:
                campaign["repurposed"] = {}
                logger.info("    → Skipped (no source content)")
        except Exception as e:
            logger.warning("    ✗ Content multiplication failed: %s", e)
            campaign["repurposed"] = {}

        # ── Step 7: Decide scaling ──
        logger.info("  [STEP 7] decide_scaling()")
        try:
            scaling = get_scaling_plan(brand, campaign["content"], campaign["ads"].get("full", {}), client)
            campaign["scaling"] = scaling.get("top_scaling_moves", [])
            campaign["full_scaling"] = scaling
            revenue_win = scaling.get("revenue_opportunity", {}).get("immediate_win", "")
            logger.info("    ✓ Scaling plan ready — Revenue opportunity: %s", revenue_win[:60])
        except Exception as e:
            logger.warning("    ✗ Scaling plan failed: %s", e)
            campaign["scaling"] = []

        # ── Step 8: Suggest automation ──
        logger.info("  [STEP 8] suggest_automation()")
        automation = campaign.get("full_scaling", {}).get("automation", {})
        campaign["automation"] = automation.get("workflow_to_automate", "")
        campaign["revenue_opportunity"] = (
            campaign.get("full_scaling", {})
            .get("revenue_opportunity", {})
            .get("immediate_win", "")
        )
        if campaign["automation"]:
            logger.info("    ✓ Automate: %s", campaign["automation"][:60])

        daily_results["brand_campaigns"][brand_name] = campaign

        # Update state
        state["brand_stats"].setdefault(brand_name, {})["runs"] = (
            state["brand_stats"].get(brand_name, {}).get("runs", 0) + 1
        )
        state["brand_stats"][brand_name]["last_content"] = run_start.isoformat()

    # ── Save report ──
    run_duration = (datetime.utcnow() - run_start).total_seconds()
    daily_results["duration_seconds"] = run_duration
    daily_results["status"] = "complete"

    report_path = _save_daily_report(daily_results)
    save_state(state)

    logger.info("\n━" * 35)
    logger.info("  DAILY LOOP COMPLETE in %.1fs", run_duration)
    logger.info("  Brands processed: %s", ", ".join(selected_brands))
    logger.info("  Report: %s", report_path)
    logger.info("━" * 35)

    return daily_results


# ─── Dashboard Output ──────────────────────────────────────────────────────────

def print_dashboard(results: Dict[str, Any], state: Dict[str, Any]) -> None:
    """Print a clean terminal dashboard after the daily loop."""
    print("\n" + "█" * 70)
    print("  AUTONOMOUS MARKETING AGENT — DAILY DASHBOARD")
    print("█" * 70)
    print(f"  Run #{state['total_runs']}  |  {datetime.utcnow().strftime('%Y-%m-%d %H:%M UTC')}")
    print(f"  Brands Active: {', '.join(results.get('selected_brands', []))}")
    print()

    for brand_name, campaign in results.get("brand_campaigns", {}).items():
        brand = BRANDS.get(brand_name)
        print(f"  ┌─ {brand_name} ─ {campaign.get('url', '')}")
        print(f"  │  Strategy: {campaign.get('strategy', '')[:80]}")

        scripts = campaign.get("content", {}).get("tiktok_scripts", [])
        if scripts:
            print(f"  │  TikTok Hook: {scripts[0].get('hook', '')[:65]}")

        hooks = campaign.get("ads", {}).get("hooks", [])
        if hooks:
            print(f"  │  Top Ad Hook: {hooks[0][:65]}")

        rev = campaign.get("revenue_opportunity", "")
        if rev:
            print(f"  │  Revenue Win: {rev[:65]}")

        auto = campaign.get("automation", "")
        if auto:
            print(f"  │  Automate:    {auto[:65]}")

        scaling = campaign.get("scaling", [])
        if scaling and isinstance(scaling, list) and len(scaling) > 0:
            top = scaling[0]
            if isinstance(top, dict):
                print(f"  │  Scale Now:   {top.get('action', '')[:65]}")
        print(f"  └{'─'*60}")

    print()
    goals = state.get("goals", {})
    monthly = goals.get("monthly_target_usd", 10000)
    current = goals.get("current_month_usd", 0)
    pct = (current / monthly * 100) if monthly > 0 else 0
    bar_len = int(pct / 5)
    bar = "█" * bar_len + "░" * (20 - bar_len)
    print(f"  Revenue Goal: [{bar}] ${current:,.0f} / ${monthly:,.0f}/mo ({pct:.1f}%)")
    print("█" * 70 + "\n")


# ─── Helpers ───────────────────────────────────────────────────────────────────

def _build_strategy(brand: Brand, trend_data: Dict) -> str:
    top = trend_data.get("top_trends", [])[:2]
    topics = " + ".join(t["topic"] for t in top) if top else brand.content_pillars[0]
    gap = trend_data.get("competitor_gap", "")
    return f"Lead with '{topics}'" + (f" | Gap to fill: {gap[:50]}" if gap else "")


def _save_daily_report(results: Dict[str, Any]) -> str:
    REPORTS_DIR.mkdir(parents=True, exist_ok=True)
    ts = datetime.utcnow().strftime("%Y%m%d_%H%M%S")
    path = REPORTS_DIR / f"daily_{ts}.json"
    with open(path, "w") as f:
        json.dump(results, f, indent=2, default=str)
    return str(path)


def _print_dry_run_plan(brand_names: List[str], pick_top: int) -> Dict[str, Any]:
    print("\n[DRY RUN] DAILY EXECUTION PLAN")
    print("=" * 50)
    print(f"Step 1: scan_market_trends() for {len(brand_names)} brands")
    print(f"Step 2: pick_top_roi(n={pick_top}) — select highest opportunity brands")
    print("Step 3: generate_content() → TikTok scripts + Pinterest + Blog")
    print("Step 4: create_ads() → Primary + 5 hooks + 3 CTAs")
    print("Step 5: optimize_pages() → SEO keyword plan + quick wins")
    print("Step 6: multiply_content() → 1 piece → 8 platform variants")
    print("Step 7: decide_scaling() → budget, growth tactics, revenue paths")
    print("Step 8: suggest_automation() → top workflow to automate")
    print("\nBrands in scope:")
    for name in brand_names:
        b = BRANDS.get(name)
        if b:
            print(f"  • {b.name:25s} {b.url}")
    print("\nEstimated API cost per full loop: ~$0.30–$0.80")
    print("Estimated run time: ~3–6 minutes")
    return {"dry_run": True, "brands": brand_names}


# ─── Entry Point ───────────────────────────────────────────────────────────────

def main():
    parser = argparse.ArgumentParser(
        description="Autonomous Marketing Agent — Daily Execution Loop",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
EXECUTION MODES:
  Run once now:           python daily_agent.py
  Dry run (no API):       python daily_agent.py --dry-run
  All brands:             python daily_agent.py --all
  Single brand:           python daily_agent.py --brand TheFlavorCrave
  Pick top 3 by ROI:      python daily_agent.py --pick-top 3
  View dashboard only:    python daily_agent.py --dashboard

SCHEDULE (cron):
  Daily at 6am:           0 6 * * * cd /path/to/hermes-agent && python skills/marketing/daily_agent.py
        """,
    )
    parser.add_argument("--all", action="store_true", help="Run for all 7 brands")
    parser.add_argument("--brand", type=str, help="Run for a single brand")
    parser.add_argument("--pick-top", type=int, default=2, metavar="N",
                        help="Auto-select top N brands by ROI (default: 2)")
    parser.add_argument("--dry-run", action="store_true", help="Print plan without API calls")
    parser.add_argument("--dashboard", action="store_true", help="Print last run dashboard")
    args = parser.parse_args()

    state = load_state()

    if args.dashboard:
        if STATE_FILE.exists():
            reports = sorted(REPORTS_DIR.glob("daily_*.json")) if REPORTS_DIR.exists() else []
            last_report = {}
            if reports:
                with open(reports[-1]) as f:
                    last_report = json.load(f)
            print_dashboard(last_report, state)
        else:
            print("No runs yet. Run `python daily_agent.py` to start.")
        return

    if not args.dry_run:
        api_key = os.environ.get("ANTHROPIC_API_KEY")
        if not api_key:
            logger.error("ANTHROPIC_API_KEY not set. Export it first.")
            sys.exit(1)
        client = anthropic.Anthropic(api_key=api_key)
    else:
        client = None  # type: ignore

    brand_names: Optional[List[str]] = None
    if args.brand:
        if args.brand not in BRANDS:
            logger.error("Unknown brand: %s", args.brand)
            sys.exit(1)
        brand_names = [args.brand]
    elif args.all:
        brand_names = ALL_BRAND_NAMES

    results = run_daily_loop(
        client=client,
        brand_names=brand_names,
        pick_top=args.pick_top,
        dry_run=args.dry_run,
    )

    if not args.dry_run:
        state = load_state()
        print_dashboard(results, state)


if __name__ == "__main__":
    main()
