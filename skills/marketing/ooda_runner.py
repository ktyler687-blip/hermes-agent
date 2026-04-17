#!/usr/bin/env python3
"""
OODA LOOP ORCHESTRATOR — L99 AUTONOMOUS MARKETING AGENT
Observe → Orient → Decide → Act → repeat

Runs continuously or as a single pass. Each cycle:
  OBSERVE  — probe all 7 brand sites + revenue state + trend signals
  ORIENT   — threat detection + opportunity scoring + AI situational read
  DECIDE   — priority-ranked action queue (respects budget + threats)
  ACT      — executes every action, saves JSON execution log

Usage:
  python ooda_runner.py                    # single pass (default)
  python ooda_runner.py --loop             # continuous loop (interval: 6h)
  python ooda_runner.py --interval 3600    # loop every 1 hour
  python ooda_runner.py --dry-run          # observe + orient + decide, no API actions
  python ooda_runner.py --brand TheFlavorCrave  # single brand focus
  python ooda_runner.py --status           # print last cycle status
  python ooda_runner.py --max-actions 5    # cap action count per cycle
"""

import argparse
import json
import logging
import os
import signal
import sys
import time
from datetime import datetime
from pathlib import Path
from typing import Optional, List

import anthropic

sys.path.insert(0, str(Path(__file__).parent))

from brands import BRANDS, ALL_BRAND_NAMES
from ooda.observe import observe, ObservationSet
from ooda.orient import orient, OrientOutput
from ooda.decide import decide, ActionPlan
from ooda.act import act, ExecutionLog

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s  %(levelname)-8s  %(name)s  %(message)s",
    datefmt="%H:%M:%S",
)
logger = logging.getLogger("OODA")

REPORTS_DIR = Path(__file__).parent / "reports"
STATE_FILE = Path(__file__).parent / "agent_state.json"
CYCLE_LOG = Path(__file__).parent / "ooda_cycles.json"

_running = True


def _handle_sigint(sig, frame):
    global _running
    logger.info("\n[OODA] Received interrupt — finishing current cycle then stopping...")
    _running = False


signal.signal(signal.SIGINT, _handle_sigint)


# ─── Single OODA Cycle ────────────────────────────────────────────────────────

def run_cycle(
    client: anthropic.Anthropic,
    brand_names: Optional[List[str]] = None,
    max_actions: int = 10,
    dry_run: bool = False,
    cycle_num: int = 1,
) -> dict:
    cycle_start = datetime.utcnow()

    _print_cycle_header(cycle_num, cycle_start)

    # ── OBSERVE ──
    obs: ObservationSet = observe(brand_names)

    # ── ORIENT ──
    orient_out: OrientOutput = orient(obs, client)

    # ── DECIDE ──
    plan: ActionPlan = decide(orient_out, max_actions=max_actions)

    _print_plan_summary(plan, orient_out)

    if dry_run:
        logger.info("[DRY RUN] Skipping ACT phase.")
        _save_cycle_log(cycle_num, cycle_start, obs, orient_out, plan, None)
        return {"dry_run": True, "plan": plan.to_dict()}

    # ── ACT ──
    execution: ExecutionLog = act(plan, client)

    duration = (datetime.utcnow() - cycle_start).total_seconds()
    _save_cycle_log(cycle_num, cycle_start, obs, orient_out, plan, execution)
    _print_cycle_summary(cycle_num, duration, plan, execution, orient_out)

    return {
        "cycle": cycle_num,
        "duration_s": duration,
        "succeeded": execution.actions_succeeded,
        "failed": execution.actions_failed,
        "report": execution.report_path,
    }


# ─── Continuous Loop ──────────────────────────────────────────────────────────

def run_loop(
    client: anthropic.Anthropic,
    interval_seconds: int = 21600,   # 6 hours default
    brand_names: Optional[List[str]] = None,
    max_actions: int = 10,
    dry_run: bool = False,
) -> None:
    logger.info("=" * 70)
    logger.info("  OODA CONTINUOUS LOOP — interval: %ds (%.1fh)",
                interval_seconds, interval_seconds / 3600)
    logger.info("  Ctrl+C to stop gracefully after current cycle")
    logger.info("=" * 70)

    cycle_num = _load_last_cycle_num() + 1

    while _running:
        try:
            run_cycle(client, brand_names=brand_names, max_actions=max_actions,
                      dry_run=dry_run, cycle_num=cycle_num)
            cycle_num += 1
        except Exception as e:
            logger.error("Cycle %d failed: %s", cycle_num, e)
            logger.info("Backing off 60s before retry...")
            time.sleep(60)
            cycle_num += 1
            continue

        if not _running:
            break

        next_run = datetime.utcnow().timestamp() + interval_seconds
        logger.info("[OODA] Next cycle in %ds at %s",
                    interval_seconds,
                    datetime.utcfromtimestamp(next_run).strftime("%H:%M:%S UTC"))

        # Sleep in small increments so Ctrl+C works
        elapsed = 0
        while elapsed < interval_seconds and _running:
            time.sleep(min(10, interval_seconds - elapsed))
            elapsed += 10

    logger.info("[OODA] Loop stopped. Total cycles run: %d", cycle_num - 1)


# ─── Status ───────────────────────────────────────────────────────────────────

def print_status() -> None:
    if not CYCLE_LOG.exists():
        print("No OODA cycles logged yet. Run: python ooda_runner.py")
        return

    with open(CYCLE_LOG) as f:
        cycles = json.load(f)

    if not cycles:
        print("No cycles found.")
        return

    last = cycles[-1]
    print("\n" + "█" * 65)
    print("  OODA STATUS — LAST CYCLE")
    print("█" * 65)
    print(f"  Cycle #:     {last.get('cycle_num', '?')}")
    print(f"  Started:     {last.get('started_at', '?')}")
    print(f"  Duration:    {last.get('duration_s', 0):.1f}s")
    print(f"  Health:      {last.get('portfolio_health', '?')}")
    print(f"  Revenue:     {last.get('revenue_trajectory', '?')}")
    print(f"  Insight:     {last.get('key_insight', '')[:70]}")
    print(f"  24h Focus:   {last.get('24h_focus', '')[:70]}")
    print(f"  Actions:     {last.get('actions_succeeded', 0)}/{last.get('actions_total', 0)} succeeded")
    print(f"  Threats:     {last.get('threats_critical', 0)} critical, {last.get('threats_total', 0)} total")
    print(f"  Report:      {last.get('report_path', 'N/A')}")
    print("█" * 65)
    print(f"\n  Total cycles: {len(cycles)}")
    print(f"  Run: python ooda_runner.py --status\n")


# ─── Helpers ──────────────────────────────────────────────────────────────────

def _print_cycle_header(cycle_num: int, start: datetime) -> None:
    logger.info("")
    logger.info("▓" * 70)
    logger.info("  OODA CYCLE #%d — %s", cycle_num, start.strftime("%a %b %d %H:%M:%S UTC"))
    logger.info("  Observe → Orient → Decide → Act")
    logger.info("▓" * 70)


def _print_plan_summary(plan: ActionPlan, orient_out: OrientOutput) -> None:
    mm = orient_out.mental_model
    ai = orient_out.ai_analysis
    logger.info("")
    logger.info("  ┌─ SITUATIONAL PICTURE ─────────────────────────────────────────┐")
    logger.info("  │ Health:      %-55s│", mm.portfolio_health.upper())
    logger.info("  │ Revenue:     %-55s│", mm.revenue_trajectory.upper())
    logger.info("  │ Top Brand:   %-55s│", mm.top_priority_brand)
    logger.info("  │ Insight:     %-55s│", mm.key_insight[:55])
    logger.info("  │ 24h Focus:   %-55s│", ai.get("24h_focus", "")[:55])
    logger.info("  │ Actions:     %-55s│", f"{plan.pending_count()} queued | est. ${plan.total_estimated_cost_usd:.2f}")
    logger.info("  └───────────────────────────────────────────────────────────────┘")
    logger.info("")


def _print_cycle_summary(cycle_num: int, duration: float, plan: ActionPlan,
                          execution: ExecutionLog, orient_out: OrientOutput) -> None:
    logger.info("")
    logger.info("▓" * 70)
    logger.info("  CYCLE #%d COMPLETE — %.1fs", cycle_num, duration)
    logger.info("  ✓ %d/%d actions succeeded | ✗ %d failed",
                execution.actions_succeeded, execution.actions_total, execution.actions_failed)
    logger.info("  Report: %s", execution.report_path)
    logger.info("▓" * 70)
    logger.info("")


def _save_cycle_log(cycle_num: int, start: datetime, obs: ObservationSet,
                    orient_out: OrientOutput, plan: ActionPlan,
                    execution: Optional[ExecutionLog]) -> None:
    cycles = []
    if CYCLE_LOG.exists():
        with open(CYCLE_LOG) as f:
            cycles = json.load(f)

    mm = orient_out.mental_model
    ai = orient_out.ai_analysis
    entry = {
        "cycle_num": cycle_num,
        "started_at": start.isoformat(),
        "duration_s": (datetime.utcnow() - start).total_seconds(),
        "portfolio_health": mm.portfolio_health,
        "revenue_trajectory": mm.revenue_trajectory,
        "content_velocity": mm.content_velocity,
        "key_insight": mm.key_insight,
        "24h_focus": ai.get("24h_focus", ""),
        "biggest_opportunity": mm.biggest_opportunity,
        "biggest_threat": mm.biggest_threat,
        "threats_total": len(orient_out.threats),
        "threats_critical": sum(1 for t in orient_out.threats if t.severity == "critical"),
        "actions_total": len(plan.actions),
        "actions_succeeded": execution.actions_succeeded if execution else 0,
        "actions_failed": execution.actions_failed if execution else 0,
        "report_path": execution.report_path if execution else "",
        "sites_down": [s.brand for s in obs.sites if not s.reachable],
        "prioritized_brands": orient_out.prioritized_brands,
    }
    cycles.append(entry)
    # Keep last 100 cycles
    cycles = cycles[-100:]
    with open(CYCLE_LOG, "w") as f:
        json.dump(cycles, f, indent=2, default=str)


def _load_last_cycle_num() -> int:
    if CYCLE_LOG.exists():
        with open(CYCLE_LOG) as f:
            cycles = json.load(f)
        if cycles:
            return cycles[-1].get("cycle_num", 0)
    return 0


# ─── Entry Point ──────────────────────────────────────────────────────────────

def main():
    parser = argparse.ArgumentParser(
        description="OODA Loop — Autonomous Marketing Agent (L99)",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
OODA LOOP: Observe → Orient → Decide → Act

  Single pass:              python ooda_runner.py
  Continuous (every 6h):    python ooda_runner.py --loop
  Custom interval (1h):     python ooda_runner.py --loop --interval 3600
  Dry run (no execution):   python ooda_runner.py --dry-run
  Focus on one brand:       python ooda_runner.py --brand TheFlavorCrave
  Limit actions:            python ooda_runner.py --max-actions 3
  View last cycle status:   python ooda_runner.py --status
  All brands continuous:    python ooda_runner.py --all --loop

BRANDS: TheFlavorCrave | HealthIsWealth | HummingNectar | TasteTableLA
        KidsLunchRecipes | CramTools | LiveLiveRadio
        """,
    )
    parser.add_argument("--loop", action="store_true", help="Run continuously")
    parser.add_argument("--interval", type=int, default=21600,
                        help="Loop interval in seconds (default: 21600 = 6h)")
    parser.add_argument("--brand", type=str, help="Focus on a single brand")
    parser.add_argument("--all", action="store_true", help="Run for all 7 brands")
    parser.add_argument("--dry-run", action="store_true",
                        help="Observe + Orient + Decide only, no ACT API calls")
    parser.add_argument("--max-actions", type=int, default=10,
                        help="Max actions per cycle (default: 10)")
    parser.add_argument("--status", action="store_true", help="Print last cycle status")
    args = parser.parse_args()

    if args.status:
        print_status()
        return

    api_key = os.environ.get("ANTHROPIC_API_KEY")
    if not api_key:
        logger.error("ANTHROPIC_API_KEY not set.")
        sys.exit(1)

    client = anthropic.Anthropic(api_key=api_key)

    brand_names: Optional[List[str]] = None
    if args.brand:
        if args.brand not in BRANDS:
            logger.error("Unknown brand: %s", args.brand)
            sys.exit(1)
        brand_names = [args.brand]
    elif args.all:
        brand_names = ALL_BRAND_NAMES
    # default: None → auto-select via Orient

    if args.loop:
        run_loop(
            client,
            interval_seconds=args.interval,
            brand_names=brand_names,
            max_actions=args.max_actions,
            dry_run=args.dry_run,
        )
    else:
        cycle_num = _load_last_cycle_num() + 1
        run_cycle(
            client,
            brand_names=brand_names,
            max_actions=args.max_actions,
            dry_run=args.dry_run,
            cycle_num=cycle_num,
        )


if __name__ == "__main__":
    main()
