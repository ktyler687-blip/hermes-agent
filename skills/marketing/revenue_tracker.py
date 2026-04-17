#!/usr/bin/env python3
"""
Revenue Tracker — Log, monitor, and forecast revenue across all 7 brands.
Tracks actuals vs $10K/month goal and computes brand-level breakdowns.

Usage:
    python revenue_tracker.py --log TheFlavorCrave 450.00 "affiliate"
    python revenue_tracker.py --status
    python revenue_tracker.py --forecast
    python revenue_tracker.py --breakdown
"""

import argparse
import json
from datetime import datetime, date
from pathlib import Path
from typing import Dict, Any, List

from brands import ALL_BRAND_NAMES, BRANDS

STATE_FILE = Path(__file__).parent / "agent_state.json"
REVENUE_FILE = Path(__file__).parent / "revenue_log.json"

MONTHLY_GOAL = 10_000.00


def load_revenue_log() -> Dict[str, Any]:
    if REVENUE_FILE.exists():
        with open(REVENUE_FILE) as f:
            return json.load(f)
    return {"entries": [], "goal_monthly_usd": MONTHLY_GOAL}


def save_revenue_log(log: Dict[str, Any]) -> None:
    with open(REVENUE_FILE, "w") as f:
        json.dump(log, f, indent=2, default=str)


def log_revenue(brand: str, amount: float, source: str) -> None:
    if brand not in BRANDS:
        print(f"Unknown brand: {brand}. Use one of: {', '.join(ALL_BRAND_NAMES)}")
        return
    log = load_revenue_log()
    entry = {
        "date": date.today().isoformat(),
        "brand": brand,
        "amount_usd": amount,
        "source": source,
        "logged_at": datetime.utcnow().isoformat(),
    }
    log["entries"].append(entry)
    save_revenue_log(log)
    print(f"✓ Logged ${amount:.2f} from {brand} ({source})")


def get_monthly_total(log: Dict[str, Any], year: int, month: int) -> float:
    return sum(
        e["amount_usd"]
        for e in log["entries"]
        if e["date"].startswith(f"{year:04d}-{month:02d}")
    )


def get_brand_total(log: Dict[str, Any], brand: str, year: int, month: int) -> float:
    return sum(
        e["amount_usd"]
        for e in log["entries"]
        if e["brand"] == brand and e["date"].startswith(f"{year:04d}-{month:02d}")
    )


def print_status() -> None:
    log = load_revenue_log()
    today = date.today()
    monthly = get_monthly_total(log, today.year, today.month)
    goal = log.get("goal_monthly_usd", MONTHLY_GOAL)
    pct = (monthly / goal * 100) if goal > 0 else 0
    remaining = goal - monthly
    days_in_month = 31
    day_of_month = today.day
    daily_needed = remaining / max(days_in_month - day_of_month, 1)

    bar_len = int(pct / 5)
    bar = "█" * bar_len + "░" * (20 - bar_len)

    print("\n" + "═" * 55)
    print("  REVENUE STATUS — " + today.strftime("%B %Y"))
    print("═" * 55)
    print(f"  Goal:      ${goal:>10,.2f}/month")
    print(f"  Earned:    ${monthly:>10,.2f}  [{bar}] {pct:.1f}%")
    print(f"  Remaining: ${remaining:>10,.2f}")
    print(f"  Daily need: ${daily_needed:>9,.2f}/day to hit goal")
    print()
    print("  By Brand:")
    for name in ALL_BRAND_NAMES:
        brand_total = get_brand_total(log, name, today.year, today.month)
        if brand_total > 0:
            print(f"    {name:25s} ${brand_total:,.2f}")
    print("═" * 55 + "\n")


def print_forecast() -> None:
    log = load_revenue_log()
    today = date.today()
    monthly = get_monthly_total(log, today.year, today.month)
    daily_avg = monthly / max(today.day, 1)
    projected = daily_avg * 30
    goal = log.get("goal_monthly_usd", MONTHLY_GOAL)

    print("\n" + "═" * 55)
    print("  30-DAY REVENUE FORECAST")
    print("═" * 55)
    print(f"  Current daily avg: ${daily_avg:.2f}/day")
    print(f"  Projected 30-day:  ${projected:,.2f}")
    print(f"  Monthly goal:      ${goal:,.2f}")
    gap = goal - projected
    if gap > 0:
        print(f"  Gap to close:      ${gap:,.2f}  ← needs {gap/30:.2f}/day more")
    else:
        print(f"  Surplus:           ${abs(gap):,.2f} ahead of goal  ✓")
    print("═" * 55 + "\n")


def print_breakdown() -> None:
    log = load_revenue_log()
    today = date.today()
    print("\n" + "═" * 55)
    print("  BRAND REVENUE BREAKDOWN — ALL TIME")
    print("═" * 55)
    totals: List[tuple] = []
    for name in ALL_BRAND_NAMES:
        total = sum(e["amount_usd"] for e in log["entries"] if e["brand"] == name)
        totals.append((name, total))
    totals.sort(key=lambda x: x[1], reverse=True)
    grand_total = sum(t for _, t in totals)
    for name, total in totals:
        pct = (total / grand_total * 100) if grand_total > 0 else 0
        bar = "█" * int(pct / 5) + "░" * (20 - int(pct / 5))
        print(f"  {name:25s} ${total:>8,.2f}  [{bar}] {pct:.1f}%")
    print(f"\n  {'TOTAL':25s} ${grand_total:>8,.2f}")
    print("═" * 55 + "\n")


def main():
    parser = argparse.ArgumentParser(description="Revenue Tracker for all managed brands")
    parser.add_argument("--log", nargs=3, metavar=("BRAND", "AMOUNT", "SOURCE"),
                        help='Log revenue: --log TheFlavorCrave 450.00 "affiliate"')
    parser.add_argument("--status", action="store_true", help="Show current month status vs goal")
    parser.add_argument("--forecast", action="store_true", help="Show 30-day revenue forecast")
    parser.add_argument("--breakdown", action="store_true", help="All-time brand breakdown")
    parser.add_argument("--set-goal", type=float, metavar="AMOUNT",
                        help="Set monthly revenue goal in USD")
    args = parser.parse_args()

    if args.set_goal:
        log = load_revenue_log()
        log["goal_monthly_usd"] = args.set_goal
        save_revenue_log(log)
        print(f"✓ Monthly goal set to ${args.set_goal:,.2f}")

    if args.log:
        log_revenue(args.log[0], float(args.log[1]), args.log[2])

    if args.status:
        print_status()

    if args.forecast:
        print_forecast()

    if args.breakdown:
        print_breakdown()

    if not any([args.log, args.status, args.forecast, args.breakdown, args.set_goal]):
        print_status()
        print_forecast()


if __name__ == "__main__":
    main()
