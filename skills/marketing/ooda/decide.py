"""
OODA — DECIDE
Takes OrientOutput and produces an ordered ActionPlan:
a priority-ranked queue of concrete actions the ACT phase will execute.

Decision logic:
  1. Critical threats always jump to top
  2. Revenue gap urgency weights heavily
  3. Highest-score opportunities fill remaining slots
  4. Never schedule the same brand for the same action twice in one loop
  5. Budget constraints respected (free actions first if no API key)
"""

import logging
import sys
from dataclasses import dataclass, field, asdict
from datetime import datetime
from enum import Enum
from pathlib import Path
from typing import Dict, Any, List, Optional

sys.path.insert(0, str(Path(__file__).parent.parent))
from brands import BRANDS, ALL_BRAND_NAMES
from ooda.orient import OrientOutput, Threat, Opportunity

logger = logging.getLogger("OODA.Decide")


class ActionType(str, Enum):
    GENERATE_CONTENT    = "generate_content"
    CREATE_ADS          = "create_ads"
    RUN_SEO             = "run_seo"
    MULTIPLY_CONTENT    = "multiply_content"
    FULL_CAMPAIGN       = "full_campaign"
    SCALING_PLAN        = "scaling_plan"
    TREND_SCAN          = "trend_scan"
    ALERT               = "alert"           # no API — just log/notify
    REVENUE_LOG_PROMPT  = "revenue_log_prompt"


@dataclass
class Action:
    id: str
    action_type: ActionType
    brand: Optional[str]            # None = portfolio-level
    priority: int                   # 1 = highest
    reasoning: str
    estimated_impact: str           # "high" | "medium" | "low"
    estimated_cost_usd: float       # 0 = free
    kwargs: Dict[str, Any] = field(default_factory=dict)
    # Set by ACT phase:
    executed: bool = False
    result_summary: Optional[str] = None
    executed_at: Optional[str] = None

    def to_dict(self) -> Dict[str, Any]:
        d = asdict(self)
        d["action_type"] = self.action_type.value
        return d


@dataclass
class ActionPlan:
    timestamp: str
    cycle_id: str
    actions: List[Action]           # ordered by priority
    total_estimated_cost_usd: float
    decision_summary: str

    def to_dict(self) -> Dict[str, Any]:
        return {
            "timestamp": self.timestamp,
            "cycle_id": self.cycle_id,
            "actions": [a.to_dict() for a in self.actions],
            "total_estimated_cost_usd": self.total_estimated_cost_usd,
            "decision_summary": self.decision_summary,
        }

    def next_action(self) -> Optional[Action]:
        for a in self.actions:
            if not a.executed:
                return a
        return None

    def pending_count(self) -> int:
        return sum(1 for a in self.actions if not a.executed)


# ─── Decision Engine ──────────────────────────────────────────────────────────

def decide(orient_out: OrientOutput, max_actions: int = 10) -> ActionPlan:
    """Produce a prioritized ActionPlan from OrientOutput."""
    logger.info("[DECIDE] Building action plan...")

    cycle_id = datetime.utcnow().strftime("cycle_%Y%m%d_%H%M%S")
    actions: List[Action] = []
    action_counter = [0]

    def _next_id() -> str:
        action_counter[0] += 1
        return f"{cycle_id}_a{action_counter[0]:02d}"

    # ── Priority 1: Critical threats ──
    for threat in orient_out.threats:
        if threat.severity == "critical":
            if threat.type == "site_down":
                actions.append(Action(
                    id=_next_id(),
                    action_type=ActionType.ALERT,
                    brand=threat.brand,
                    priority=1,
                    reasoning=f"CRITICAL: {threat.detail}",
                    estimated_impact="high",
                    estimated_cost_usd=0.0,
                    kwargs={"message": threat.action_required, "threat": asdict(threat)},
                ))
            elif threat.type == "revenue_lag":
                # Revenue critical → push ads for top brands immediately
                for brand_name in orient_out.prioritized_brands[:2]:
                    actions.append(Action(
                        id=_next_id(),
                        action_type=ActionType.CREATE_ADS,
                        brand=brand_name,
                        priority=1,
                        reasoning=f"Revenue critical ({threat.detail}) — ads needed now",
                        estimated_impact="high",
                        estimated_cost_usd=0.15,
                        kwargs={"mode": "ads"},
                    ))

    # ── Priority 2: Top revenue opportunity brands — full campaign ──
    mm = orient_out.mental_model
    top_brand = mm.top_priority_brand
    if top_brand and top_brand in BRANDS:
        actions.append(Action(
            id=_next_id(),
            action_type=ActionType.FULL_CAMPAIGN,
            brand=top_brand,
            priority=2,
            reasoning=f"AI identified as top priority: {mm.key_insight[:80]}",
            estimated_impact="high",
            estimated_cost_usd=0.50,
            kwargs={"mode": "full"},
        ))

    # ── Priority 3: High-score opportunities ──
    seen_brand_types: set = {(top_brand, ActionType.FULL_CAMPAIGN)}
    for opp in orient_out.opportunities[:5]:
        if len(actions) >= max_actions:
            break
        action_type = _map_opportunity_to_action(opp)
        key = (opp.brand, action_type)
        if key in seen_brand_types:
            continue
        seen_brand_types.add(key)
        actions.append(Action(
            id=_next_id(),
            action_type=action_type,
            brand=opp.brand,
            priority=3,
            reasoning=f"Score {opp.score:.1f} opportunity: {opp.detail[:80]}",
            estimated_impact="medium" if opp.score < 7 else "high",
            estimated_cost_usd=_estimate_cost(action_type),
            kwargs={"platform": opp.platform, "mode": action_type.value},
        ))

    # ── Priority 4: Content for remaining prioritized brands ──
    for brand_name in orient_out.prioritized_brands:
        if len(actions) >= max_actions:
            break
        key = (brand_name, ActionType.GENERATE_CONTENT)
        if key in seen_brand_types:
            continue
        seen_brand_types.add(key)
        # Check for content staleness threat
        stale = any(t.brand == brand_name and t.type == "content_stale"
                    for t in orient_out.threats)
        actions.append(Action(
            id=_next_id(),
            action_type=ActionType.GENERATE_CONTENT,
            brand=brand_name,
            priority=4 if not stale else 2,
            reasoning="Scheduled content cycle" + (" — stale content detected" if stale else ""),
            estimated_impact="medium",
            estimated_cost_usd=0.25,
            kwargs={"mode": "content"},
        ))

    # ── Priority 5: SEO sweep on top 3 brands ──
    for brand_name in orient_out.prioritized_brands[:3]:
        if len(actions) >= max_actions:
            break
        key = (brand_name, ActionType.RUN_SEO)
        if key not in seen_brand_types:
            seen_brand_types.add(key)
            actions.append(Action(
                id=_next_id(),
                action_type=ActionType.RUN_SEO,
                brand=brand_name,
                priority=5,
                reasoning="SEO optimization for top-priority brand",
                estimated_impact="medium",
                estimated_cost_usd=0.15,
                kwargs={"mode": "seo"},
            ))

    # ── Priority 6: Scaling plan for portfolio ──
    if len(actions) < max_actions:
        actions.append(Action(
            id=_next_id(),
            action_type=ActionType.SCALING_PLAN,
            brand=orient_out.prioritized_brands[0] if orient_out.prioritized_brands else None,
            priority=6,
            reasoning="Weekly scaling & automation review",
            estimated_impact="high",
            estimated_cost_usd=0.20,
            kwargs={"mode": "scaling"},
        ))

    # Sort by priority then estimated_impact
    impact_rank = {"high": 0, "medium": 1, "low": 2}
    actions.sort(key=lambda a: (a.priority, impact_rank.get(a.estimated_impact, 1)))
    actions = actions[:max_actions]

    total_cost = sum(a.estimated_cost_usd for a in actions)

    ai_focus = orient_out.ai_analysis.get("24h_focus", "")
    decision_summary = (
        f"{len(actions)} actions planned | "
        f"Est. cost: ${total_cost:.2f} | "
        f"Top brand: {top_brand} | "
        f"Focus: {ai_focus[:80]}"
    )

    logger.info("[DECIDE] Plan: %d actions | est. $%.2f", len(actions), total_cost)
    for i, a in enumerate(actions[:5], 1):
        logger.info("  %d. [P%d] %s → %s (%s)",
                    i, a.priority, a.action_type.value,
                    a.brand or "PORTFOLIO", a.estimated_impact)

    return ActionPlan(
        timestamp=datetime.utcnow().isoformat(),
        cycle_id=cycle_id,
        actions=actions,
        total_estimated_cost_usd=total_cost,
        decision_summary=decision_summary,
    )


def _map_opportunity_to_action(opp: Opportunity) -> ActionType:
    mapping = {
        "revenue_unlock": ActionType.CREATE_ADS,
        "platform_growth": ActionType.GENERATE_CONTENT,
        "content_gap": ActionType.GENERATE_CONTENT,
        "trending_topic": ActionType.FULL_CAMPAIGN,
    }
    return mapping.get(opp.type, ActionType.GENERATE_CONTENT)


def _estimate_cost(action_type: ActionType) -> float:
    costs = {
        ActionType.FULL_CAMPAIGN: 0.50,
        ActionType.GENERATE_CONTENT: 0.25,
        ActionType.CREATE_ADS: 0.15,
        ActionType.RUN_SEO: 0.15,
        ActionType.MULTIPLY_CONTENT: 0.10,
        ActionType.SCALING_PLAN: 0.20,
        ActionType.TREND_SCAN: 0.08,
        ActionType.ALERT: 0.0,
        ActionType.REVENUE_LOG_PROMPT: 0.0,
    }
    return costs.get(action_type, 0.10)
