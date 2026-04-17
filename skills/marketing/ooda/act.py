"""
OODA — ACT
Executes the ActionPlan produced by Decide.
Dispatches each action to the appropriate campaign module,
records results, updates state, and returns an ExecutionLog.
"""

import json
import logging
import sys
from dataclasses import dataclass, asdict
from datetime import datetime
from pathlib import Path
from typing import Dict, Any, List, Optional

import anthropic

sys.path.insert(0, str(Path(__file__).parent.parent))
from brands import BRANDS
from ooda.decide import ActionPlan, Action, ActionType

logger = logging.getLogger("OODA.Act")

STATE_FILE = Path(__file__).parent.parent / "agent_state.json"
REPORTS_DIR = Path(__file__).parent.parent / "reports"


@dataclass
class ActionResult:
    action_id: str
    action_type: str
    brand: Optional[str]
    success: bool
    summary: str
    output: Dict[str, Any]
    duration_ms: float
    error: Optional[str] = None


@dataclass
class ExecutionLog:
    cycle_id: str
    started_at: str
    completed_at: str
    actions_total: int
    actions_succeeded: int
    actions_failed: int
    results: List[ActionResult]
    report_path: str

    def to_dict(self) -> Dict[str, Any]:
        return {
            "cycle_id": self.cycle_id,
            "started_at": self.started_at,
            "completed_at": self.completed_at,
            "actions_total": self.actions_total,
            "actions_succeeded": self.actions_succeeded,
            "actions_failed": self.actions_failed,
            "results": [asdict(r) for r in self.results],
            "report_path": self.report_path,
        }


# ─── Action Dispatchers ────────────────────────────────────────────────────────

def _dispatch(action: Action, client: anthropic.Anthropic) -> ActionResult:
    """Route action to the correct module and return result."""
    start = datetime.utcnow().timestamp()

    try:
        if action.action_type == ActionType.ALERT:
            return _act_alert(action, start)

        brand = BRANDS.get(action.brand) if action.brand else None

        if action.action_type == ActionType.FULL_CAMPAIGN:
            return _act_full_campaign(action, brand, client, start)
        elif action.action_type == ActionType.GENERATE_CONTENT:
            return _act_content(action, brand, client, start)
        elif action.action_type == ActionType.CREATE_ADS:
            return _act_ads(action, brand, client, start)
        elif action.action_type == ActionType.RUN_SEO:
            return _act_seo(action, brand, client, start)
        elif action.action_type == ActionType.MULTIPLY_CONTENT:
            return _act_multiply(action, brand, client, start)
        elif action.action_type == ActionType.SCALING_PLAN:
            return _act_scaling(action, brand, client, start)
        elif action.action_type == ActionType.TREND_SCAN:
            return _act_trends(action, brand, client, start)
        elif action.action_type == ActionType.REVENUE_LOG_PROMPT:
            return _act_revenue_prompt(action, start)
        else:
            raise ValueError(f"Unknown action type: {action.action_type}")

    except Exception as e:
        ms = (datetime.utcnow().timestamp() - start) * 1000
        logger.error("  ✗ Action %s failed: %s", action.id, e)
        return ActionResult(
            action_id=action.id,
            action_type=action.action_type.value,
            brand=action.brand,
            success=False,
            summary=f"Failed: {str(e)[:120]}",
            output={},
            duration_ms=round(ms, 1),
            error=str(e),
        )


def _act_alert(action: Action, start: float) -> ActionResult:
    msg = action.kwargs.get("message", "")
    logger.warning("  ⚠  ALERT [%s]: %s", action.brand or "PORTFOLIO", msg)
    ms = (datetime.utcnow().timestamp() - start) * 1000
    return ActionResult(
        action_id=action.id, action_type=action.action_type.value,
        brand=action.brand, success=True,
        summary=f"Alert logged: {msg[:80]}", output={"alert": msg}, duration_ms=round(ms, 1),
    )


def _act_full_campaign(action, brand, client, start) -> ActionResult:
    from trend_scanner import scan_trends_for_brand
    from content_generator import generate_all_content
    from ad_creator import generate_ads
    from seo_optimizer import optimize_seo
    from scaling_advisor import get_scaling_plan

    trend_data = scan_trends_for_brand(brand, client)
    content = generate_all_content(brand, trend_data, client)
    trend_topics = [t["topic"] for t in trend_data.get("top_trends", [])]
    ads = generate_ads(brand, trend_topics, client)
    seo = optimize_seo(brand, trend_topics, client)
    scaling = get_scaling_plan(brand, content, ads, client)

    _update_brand_state(brand.name)
    ms = (datetime.utcnow().timestamp() - start) * 1000
    scripts = len(content.get("tiktok_scripts", []))
    pins = len(content.get("pinterest_posts", []))
    hooks = len(ads.get("hooks", []))
    rev_win = scaling.get("revenue_opportunity", {}).get("immediate_win", "")
    return ActionResult(
        action_id=action.id, action_type=action.action_type.value,
        brand=brand.name, success=True,
        summary=f"{scripts} TikTok scripts, {pins} Pinterest pins, {hooks} hooks | Rev: {rev_win[:60]}",
        output={"content": content, "ads": ads, "seo": seo, "scaling": scaling},
        duration_ms=round(ms, 1),
    )


def _act_content(action, brand, client, start) -> ActionResult:
    from trend_scanner import scan_trends_for_brand
    from content_generator import generate_all_content

    trend_data = scan_trends_for_brand(brand, client)
    content = generate_all_content(brand, trend_data, client)
    _update_brand_state(brand.name)
    ms = (datetime.utcnow().timestamp() - start) * 1000
    scripts = len(content.get("tiktok_scripts", []))
    pins = len(content.get("pinterest_posts", []))
    return ActionResult(
        action_id=action.id, action_type=action.action_type.value,
        brand=brand.name, success=True,
        summary=f"{scripts} TikTok scripts + {pins} Pinterest pins + 1 blog draft",
        output=content, duration_ms=round(ms, 1),
    )


def _act_ads(action, brand, client, start) -> ActionResult:
    from trend_scanner import scan_trends_for_brand
    from ad_creator import generate_ads

    trend_data = scan_trends_for_brand(brand, client)
    trend_topics = [t["topic"] for t in trend_data.get("top_trends", [])]
    ads = generate_ads(brand, trend_topics, client)
    ms = (datetime.utcnow().timestamp() - start) * 1000
    hooks = ads.get("hooks", [])
    return ActionResult(
        action_id=action.id, action_type=action.action_type.value,
        brand=brand.name, success=True,
        summary=f"Primary: {ads.get('primary',{}).get('headline','')[:60]} | {len(hooks)} hooks",
        output=ads, duration_ms=round(ms, 1),
    )


def _act_seo(action, brand, client, start) -> ActionResult:
    from trend_scanner import scan_trends_for_brand
    from seo_optimizer import optimize_seo

    trend_data = scan_trends_for_brand(brand, client)
    trend_topics = [t["topic"] for t in trend_data.get("top_trends", [])]
    seo = optimize_seo(brand, trend_topics, client)
    ms = (datetime.utcnow().timestamp() - start) * 1000
    head_term = seo.get("primary_keyword_strategy", {}).get("head_term", "")
    quick_wins = len(seo.get("quick_wins", []))
    return ActionResult(
        action_id=action.id, action_type=action.action_type.value,
        brand=brand.name, success=True,
        summary=f"Head term: '{head_term}' | {quick_wins} quick wins",
        output=seo, duration_ms=round(ms, 1),
    )


def _act_multiply(action, brand, client, start) -> ActionResult:
    from content_multiplier import multiply_content

    source = action.kwargs.get("source_content", f"Latest content from {brand.name}")
    result = multiply_content(brand, source, "tiktok_script", client)
    ms = (datetime.utcnow().timestamp() - start) * 1000
    total = result.get("total_pieces_generated", 0)
    return ActionResult(
        action_id=action.id, action_type=action.action_type.value,
        brand=brand.name, success=True,
        summary=f"1 piece → {total} platform variants generated",
        output=result, duration_ms=round(ms, 1),
    )


def _act_scaling(action, brand, client, start) -> ActionResult:
    from trend_scanner import scan_trends_for_brand
    from scaling_advisor import get_scaling_plan

    if not brand:
        from brands import BRANDS, ALL_BRAND_NAMES
        brand = BRANDS[ALL_BRAND_NAMES[0]]
    trend_data = scan_trends_for_brand(brand, client)
    scaling = get_scaling_plan(brand, {}, {}, client)
    ms = (datetime.utcnow().timestamp() - start) * 1000
    immediate = scaling.get("revenue_opportunity", {}).get("immediate_win", "")
    return ActionResult(
        action_id=action.id, action_type=action.action_type.value,
        brand=brand.name, success=True,
        summary=f"Scaling plan ready | Immediate win: {immediate[:60]}",
        output=scaling, duration_ms=round(ms, 1),
    )


def _act_trends(action, brand, client, start) -> ActionResult:
    from trend_scanner import scan_trends_for_brand

    result = scan_trends_for_brand(brand, client)
    ms = (datetime.utcnow().timestamp() - start) * 1000
    top = [t["topic"] for t in result.get("top_trends", [])[:3]]
    return ActionResult(
        action_id=action.id, action_type=action.action_type.value,
        brand=brand.name, success=True,
        summary=f"Top trends: {', '.join(top)}",
        output=result, duration_ms=round(ms, 1),
    )


def _act_revenue_prompt(action, start) -> ActionResult:
    ms = (datetime.utcnow().timestamp() - start) * 1000
    return ActionResult(
        action_id=action.id, action_type=action.action_type.value,
        brand=action.brand, success=True,
        summary="Revenue logging prompt — check revenue_tracker.py --status",
        output={}, duration_ms=round(ms, 1),
    )


# ─── Main Act ─────────────────────────────────────────────────────────────────

def act(plan: ActionPlan, client: anthropic.Anthropic) -> ExecutionLog:
    """Execute all actions in the plan and return an ExecutionLog."""
    logger.info("[ACT] Executing %d actions for cycle %s", len(plan.actions), plan.cycle_id)
    started_at = datetime.utcnow().isoformat()
    results: List[ActionResult] = []

    for i, action in enumerate(plan.actions, 1):
        logger.info("  [%d/%d] %s → %s (P%d)",
                    i, len(plan.actions), action.action_type.value,
                    action.brand or "PORTFOLIO", action.priority)
        result = _dispatch(action, client)
        action.executed = True
        action.result_summary = result.summary
        action.executed_at = datetime.utcnow().isoformat()
        results.append(result)

        status = "✓" if result.success else "✗"
        logger.info("    %s %s (%.0fms)", status, result.summary[:70], result.duration_ms)

    succeeded = sum(1 for r in results if r.success)
    failed = sum(1 for r in results if not r.success)
    completed_at = datetime.utcnow().isoformat()

    # Save execution log
    REPORTS_DIR.mkdir(parents=True, exist_ok=True)
    ts = datetime.utcnow().strftime("%Y%m%d_%H%M%S")
    report_path = str(REPORTS_DIR / f"ooda_{plan.cycle_id}_{ts}.json")
    log = ExecutionLog(
        cycle_id=plan.cycle_id,
        started_at=started_at,
        completed_at=completed_at,
        actions_total=len(plan.actions),
        actions_succeeded=succeeded,
        actions_failed=failed,
        results=results,
        report_path=report_path,
    )
    full_report = {
        "plan": plan.to_dict(),
        "execution": log.to_dict(),
    }
    with open(report_path, "w") as f:
        json.dump(full_report, f, indent=2, default=str)

    logger.info("[ACT] Complete — %d/%d succeeded | Report: %s",
                succeeded, len(plan.actions), report_path)
    return log


# ─── State helpers ─────────────────────────────────────────────────────────────

def _update_brand_state(brand_name: str) -> None:
    state: Dict[str, Any] = {}
    if STATE_FILE.exists():
        with open(STATE_FILE) as f:
            state = json.load(f)
    state.setdefault("brand_stats", {}).setdefault(brand_name, {})
    state["brand_stats"][brand_name]["last_content"] = datetime.utcnow().isoformat()
    state["brand_stats"][brand_name]["runs"] = (
        state["brand_stats"][brand_name].get("runs", 0) + 1
    )
    with open(STATE_FILE, "w") as f:
        json.dump(state, f, indent=2, default=str)
