"""
OODA — ORIENT
Takes the ObservationSet and builds a situational picture:
- threat matrix (site down, revenue behind, content stale)
- opportunity scores per brand
- mental model update (what changed vs last loop)
- prioritized brand list for the ACT phase
"""

import json
import logging
import sys
from dataclasses import dataclass, field, asdict
from datetime import datetime, date
from pathlib import Path
from typing import Dict, Any, List, Optional

import anthropic

sys.path.insert(0, str(Path(__file__).parent.parent))
from brands import BRANDS, ALL_BRAND_NAMES
from ooda.observe import ObservationSet, SiteSignal

logger = logging.getLogger("OODA.Orient")

ORIENT_SYSTEM = """You are a senior growth strategist and marketing intelligence analyst.
You receive raw observation data about 7 social media brands and produce a precise
situational analysis: what threats exist, what opportunities are highest-value,
and what the agent should prioritize in the next 24 hours.
Be specific, data-driven, and ruthlessly prioritized. Return valid JSON only."""

STATE_FILE = Path(__file__).parent.parent / "agent_state.json"


@dataclass
class Threat:
    brand: str
    type: str           # "site_down" | "revenue_lag" | "content_stale" | "competitor_surge"
    severity: str       # "critical" | "high" | "medium" | "low"
    detail: str
    action_required: str


@dataclass
class Opportunity:
    brand: str
    type: str           # "trending_topic" | "content_gap" | "revenue_unlock" | "platform_growth"
    score: float        # 0.0–10.0
    detail: str
    action: str
    platform: str


@dataclass
class MentalModel:
    """What we now believe to be true about the portfolio."""
    portfolio_health: str       # "healthy" | "at_risk" | "critical"
    top_priority_brand: str
    revenue_trajectory: str     # "on_track" | "behind" | "critical"
    content_velocity: str       # "high" | "medium" | "low" | "stalled"
    key_insight: str
    biggest_threat: str
    biggest_opportunity: str


@dataclass
class OrientOutput:
    timestamp: str
    threats: List[Threat]
    opportunities: List[Opportunity]
    mental_model: MentalModel
    prioritized_brands: List[str]   # ordered: highest priority first
    ai_analysis: Dict[str, Any]     # Claude's full situational read

    def to_dict(self) -> Dict[str, Any]:
        return {
            "timestamp": self.timestamp,
            "threats": [asdict(t) for t in self.threats],
            "opportunities": [asdict(o) for o in self.opportunities],
            "mental_model": asdict(self.mental_model),
            "prioritized_brands": self.prioritized_brands,
            "ai_analysis": self.ai_analysis,
        }


# ─── Rule-based threat detection ──────────────────────────────────────────────

def _detect_threats(obs: ObservationSet) -> List[Threat]:
    threats: List[Threat] = []

    # Site down threats
    for site in obs.sites:
        if not site.reachable:
            threats.append(Threat(
                brand=site.brand,
                type="site_down",
                severity="critical",
                detail=f"Site unreachable: {site.url} — {site.error or 'no response'}",
                action_required="Investigate hosting, check DNS, restore site immediately",
            ))
        elif site.response_ms and site.response_ms > 3000:
            threats.append(Threat(
                brand=site.brand,
                type="site_slow",
                severity="high",
                detail=f"Site response {site.response_ms:.0f}ms — above 3s threshold",
                action_required="Check server load, enable caching, optimize assets",
            ))

    # Revenue threats
    rev = obs.revenue
    if rev:
        if rev.pct_to_goal < 25 and rev.days_remaining < 20:
            threats.append(Threat(
                brand="PORTFOLIO",
                type="revenue_lag",
                severity="critical",
                detail=f"Only {rev.pct_to_goal:.1f}% of monthly goal with {rev.days_remaining}d left",
                action_required=f"Need ${rev.daily_needed:.2f}/day — activate paid ads immediately",
            ))
        elif rev.pct_to_goal < 50 and rev.days_remaining < 15:
            threats.append(Threat(
                brand="PORTFOLIO",
                type="revenue_lag",
                severity="high",
                detail=f"{rev.pct_to_goal:.1f}% of goal — ${rev.daily_needed:.2f}/day needed",
                action_required="Double content output on highest-converting brands",
            ))

    # Stale content threats (check last_content in state)
    if STATE_FILE.exists():
        with open(STATE_FILE) as f:
            state = json.load(f)
        today = date.today()
        for brand_name in ALL_BRAND_NAMES:
            last = state.get("brand_stats", {}).get(brand_name, {}).get("last_content")
            if last:
                last_date = datetime.fromisoformat(last).date()
                days_since = (today - last_date).days
                if days_since > 7:
                    threats.append(Threat(
                        brand=brand_name,
                        type="content_stale",
                        severity="medium" if days_since < 14 else "high",
                        detail=f"No content generated in {days_since} days",
                        action_required="Run content generation cycle immediately",
                    ))

    return threats


# ─── Rule-based opportunity scoring ───────────────────────────────────────────

def _score_opportunities(obs: ObservationSet) -> List[Opportunity]:
    opps: List[Opportunity] = []
    rev = obs.revenue

    for brand_name in ALL_BRAND_NAMES:
        brand = BRANDS[brand_name]
        brand_revenue = rev.brand_breakdown.get(brand_name, 0.0) if rev else 0.0

        # Zero-revenue brands with good sites = high opportunity
        site = next((s for s in obs.sites if s.brand == brand_name), None)
        if brand_revenue == 0 and site and site.reachable:
            opps.append(Opportunity(
                brand=brand_name,
                type="revenue_unlock",
                score=8.5,
                detail="Site live but zero revenue logged — monetization not yet activated",
                action="Generate affiliate content + add clear CTAs to site",
                platform="Blog + Pinterest",
            ))

        # Pinterest opportunity for food/kids brands
        if any(k in brand.niche.lower() for k in ["food", "recipe", "kids", "health"]):
            opps.append(Opportunity(
                brand=brand_name,
                type="platform_growth",
                score=7.5,
                detail="High-intent Pinterest audience for this niche, likely undertapped",
                action="Pin 5x daily with SEO-optimized descriptions",
                platform="Pinterest",
            ))

        # TikTok virality potential for entertainment/music/food
        if any(k in brand.niche.lower() for k in ["music", "food", "radio", "recipes"]):
            opps.append(Opportunity(
                brand=brand_name,
                type="content_gap",
                score=8.0,
                detail="Short-form video niche has strong organic reach potential",
                action="Post 2 TikToks/day using trend hooks",
                platform="TikTok",
            ))

    opps.sort(key=lambda o: o.score, reverse=True)
    return opps[:10]


# ─── Claude situational analysis ──────────────────────────────────────────────

def _run_ai_orient(obs: ObservationSet, threats: List[Threat],
                   opportunities: List[Opportunity],
                   client: anthropic.Anthropic) -> Dict[str, Any]:
    obs_summary = {
        "sites": [
            {"brand": s.brand, "reachable": s.reachable, "ms": s.response_ms, "error": s.error}
            for s in obs.sites
        ],
        "revenue": {
            "total_usd": obs.revenue.total_this_month if obs.revenue else 0,
            "goal_usd": obs.revenue.goal if obs.revenue else 10000,
            "pct_to_goal": obs.revenue.pct_to_goal if obs.revenue else 0,
            "days_remaining": obs.revenue.days_remaining if obs.revenue else 30,
            "daily_needed": obs.revenue.daily_needed if obs.revenue else 333,
        },
        "threat_count": len(threats),
        "critical_threats": [t.brand + ": " + t.detail for t in threats if t.severity == "critical"],
        "top_opportunities": [o.brand + ": " + o.detail for o in opportunities[:3]],
    }

    prompt = f"""You are the strategic intelligence layer of an autonomous marketing agent.

Current situation:
{json.dumps(obs_summary, indent=2)}

Active threats: {len(threats)} ({sum(1 for t in threats if t.severity == 'critical')} critical)
Top opportunity brands: {', '.join(o.brand for o in opportunities[:3])}

Brands managed:
{chr(10).join(f'- {name}: {BRANDS[name].niche} | {BRANDS[name].url}' for name in ALL_BRAND_NAMES)}

Return ONLY a JSON object with your situational read:
{{
  "portfolio_health": "healthy|at_risk|critical",
  "top_priority_brand": "brand name to focus on most today",
  "revenue_trajectory": "on_track|behind|critical",
  "content_velocity": "high|medium|low|stalled",
  "key_insight": "the single most important thing to know about the portfolio right now",
  "biggest_threat": "the #1 threat and why",
  "biggest_opportunity": "the #1 opportunity and why",
  "prioritized_brands": ["brand1", "brand2", "brand3", "brand4", "brand5", "brand6", "brand7"],
  "24h_focus": "in 1-2 sentences, what should the agent focus on in the next 24 hours",
  "week_focus": "in 1-2 sentences, the strategic priority for this week",
  "blind_spots": ["what we might be missing or not seeing yet"]
}}"""

    response = client.messages.create(
        model="claude-opus-4-7",
        max_tokens=1200,
        system=ORIENT_SYSTEM,
        messages=[{"role": "user", "content": prompt}],
    )
    raw = response.content[0].text.strip()
    if raw.startswith("```"):
        raw = raw.split("```")[1]
        if raw.startswith("json"):
            raw = raw[4:]
    return json.loads(raw.strip())


# ─── Main Orient ──────────────────────────────────────────────────────────────

def orient(obs: ObservationSet, client: anthropic.Anthropic) -> OrientOutput:
    """Build full situational picture from observations."""
    logger.info("[ORIENT] Building situational picture...")

    threats = _detect_threats(obs)
    logger.info("  → Threats detected: %d (%d critical)",
                len(threats), sum(1 for t in threats if t.severity == "critical"))

    opportunities = _score_opportunities(obs)
    logger.info("  → Opportunities scored: %d (top: %s @ %.1f)",
                len(opportunities),
                opportunities[0].brand if opportunities else "none",
                opportunities[0].score if opportunities else 0)

    logger.info("  → Running AI situational analysis...")
    ai = _run_ai_orient(obs, threats, opportunities, client)

    mental_model = MentalModel(
        portfolio_health=ai.get("portfolio_health", "at_risk"),
        top_priority_brand=ai.get("top_priority_brand", ALL_BRAND_NAMES[0]),
        revenue_trajectory=ai.get("revenue_trajectory", "behind"),
        content_velocity=ai.get("content_velocity", "low"),
        key_insight=ai.get("key_insight", ""),
        biggest_threat=ai.get("biggest_threat", ""),
        biggest_opportunity=ai.get("biggest_opportunity", ""),
    )

    prioritized = ai.get("prioritized_brands", ALL_BRAND_NAMES)

    logger.info("  → Portfolio health: %s | Revenue: %s",
                mental_model.portfolio_health, mental_model.revenue_trajectory)
    logger.info("  → Priority order: %s", " > ".join(prioritized[:4]))
    logger.info("  → 24h focus: %s", ai.get("24h_focus", "")[:80])
    logger.info("[ORIENT] Complete")

    return OrientOutput(
        timestamp=datetime.utcnow().isoformat(),
        threats=threats,
        opportunities=opportunities,
        mental_model=mental_model,
        prioritized_brands=prioritized,
        ai_analysis=ai,
    )
