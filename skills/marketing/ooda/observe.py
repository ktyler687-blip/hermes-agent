"""
OODA — OBSERVE
Collects raw signals from all 7 brand sites, competitor landscape, and market environment.
Outputs a structured ObservationSet for Orient to process.
"""

import json
import logging
import sys
import urllib.request
import urllib.error
from dataclasses import dataclass, field, asdict
from datetime import datetime
from pathlib import Path
from typing import Dict, Any, List, Optional
from concurrent.futures import ThreadPoolExecutor, as_completed

sys.path.insert(0, str(Path(__file__).parent.parent))
from brands import BRANDS, ALL_BRAND_NAMES, Brand

logger = logging.getLogger("OODA.Observe")

TIMEOUT = 10  # seconds per request


@dataclass
class SiteSignal:
    brand: str
    url: str
    reachable: bool
    status_code: Optional[int]
    response_ms: Optional[float]
    content_length: Optional[int]
    title: Optional[str]
    error: Optional[str] = None


@dataclass
class TrendSignal:
    brand: str
    niche: str
    keywords: List[str]
    observed_at: str = field(default_factory=lambda: datetime.utcnow().isoformat())


@dataclass
class RevenueSignal:
    total_this_month: float
    goal: float
    pct_to_goal: float
    days_remaining: int
    daily_needed: float
    brand_breakdown: Dict[str, float]


@dataclass
class ObservationSet:
    timestamp: str
    sites: List[SiteSignal]
    trends: List[TrendSignal]
    revenue: Optional[RevenueSignal]
    raw: Dict[str, Any] = field(default_factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        return {
            "timestamp": self.timestamp,
            "sites": [asdict(s) for s in self.sites],
            "trends": [asdict(t) for t in self.trends],
            "revenue": asdict(self.revenue) if self.revenue else None,
            "raw": self.raw,
        }


# ─── Site Probe ────────────────────────────────────────────────────────────────

def _probe_site(brand: Brand) -> SiteSignal:
    if not brand.url:
        return SiteSignal(brand=brand.name, url="", reachable=False,
                          status_code=None, response_ms=None,
                          content_length=None, title=None,
                          error="no URL configured")
    start = datetime.utcnow().timestamp()
    try:
        req = urllib.request.Request(
            brand.url,
            headers={"User-Agent": "HermesMarketingAgent/2.0 (healthcheck)"},
        )
        with urllib.request.urlopen(req, timeout=TIMEOUT) as resp:
            elapsed = (datetime.utcnow().timestamp() - start) * 1000
            body = resp.read(4096).decode("utf-8", errors="ignore")
            # Parse <title>
            title = None
            if "<title>" in body.lower():
                start_idx = body.lower().index("<title>") + 7
                end_idx = body.lower().find("</title>", start_idx)
                title = body[start_idx:end_idx].strip()[:100] if end_idx > start_idx else None
            return SiteSignal(
                brand=brand.name,
                url=brand.url,
                reachable=True,
                status_code=resp.status,
                response_ms=round(elapsed, 1),
                content_length=len(body),
                title=title,
            )
    except urllib.error.HTTPError as e:
        elapsed = (datetime.utcnow().timestamp() - start) * 1000
        return SiteSignal(brand=brand.name, url=brand.url, reachable=False,
                          status_code=e.code, response_ms=round(elapsed, 1),
                          content_length=None, title=None, error=str(e))
    except Exception as e:
        return SiteSignal(brand=brand.name, url=brand.url, reachable=False,
                          status_code=None, response_ms=None,
                          content_length=None, title=None, error=str(e)[:120])


def probe_all_sites(brand_names: Optional[List[str]] = None) -> List[SiteSignal]:
    targets = brand_names or ALL_BRAND_NAMES
    signals: List[SiteSignal] = []
    with ThreadPoolExecutor(max_workers=7) as pool:
        futures = {pool.submit(_probe_site, BRANDS[n]): n for n in targets if n in BRANDS}
        for future in as_completed(futures):
            try:
                signals.append(future.result())
            except Exception as e:
                name = futures[future]
                logger.error("Probe failed for %s: %s", name, e)
    return sorted(signals, key=lambda s: s.brand)


# ─── Trend Signals ─────────────────────────────────────────────────────────────

def build_trend_signals(brand_names: Optional[List[str]] = None) -> List[TrendSignal]:
    targets = brand_names or ALL_BRAND_NAMES
    return [
        TrendSignal(
            brand=name,
            niche=BRANDS[name].niche,
            keywords=BRANDS[name].keywords,
        )
        for name in targets
        if name in BRANDS
    ]


# ─── Revenue Signal ────────────────────────────────────────────────────────────

def load_revenue_signal() -> Optional[RevenueSignal]:
    revenue_file = Path(__file__).parent.parent / "revenue_log.json"
    if not revenue_file.exists():
        return RevenueSignal(
            total_this_month=0.0, goal=10000.0, pct_to_goal=0.0,
            days_remaining=30, daily_needed=333.33,
            brand_breakdown={name: 0.0 for name in ALL_BRAND_NAMES},
        )
    from datetime import date
    with open(revenue_file) as f:
        data = json.load(f)
    today = date.today()
    month_prefix = f"{today.year:04d}-{today.month:02d}"
    entries = [e for e in data.get("entries", []) if e["date"].startswith(month_prefix)]
    total = sum(e["amount_usd"] for e in entries)
    goal = data.get("goal_monthly_usd", 10000.0)
    pct = (total / goal * 100) if goal > 0 else 0.0
    import calendar
    days_in_month = calendar.monthrange(today.year, today.month)[1]
    days_remaining = max(days_in_month - today.day, 1)
    daily_needed = (goal - total) / days_remaining
    breakdown: Dict[str, float] = {}
    for name in ALL_BRAND_NAMES:
        breakdown[name] = sum(e["amount_usd"] for e in entries if e["brand"] == name)
    return RevenueSignal(
        total_this_month=total, goal=goal, pct_to_goal=round(pct, 2),
        days_remaining=days_remaining, daily_needed=round(daily_needed, 2),
        brand_breakdown=breakdown,
    )


# ─── Main Observe ──────────────────────────────────────────────────────────────

def observe(brand_names: Optional[List[str]] = None) -> ObservationSet:
    """Run full observation pass. Returns ObservationSet."""
    logger.info("[OBSERVE] Starting observation pass...")

    logger.info("  → Probing %d brand sites...", len(brand_names or ALL_BRAND_NAMES))
    sites = probe_all_sites(brand_names)

    reachable = sum(1 for s in sites if s.reachable)
    down = [s.brand for s in sites if not s.reachable]
    logger.info("  → Sites reachable: %d/%d%s",
                reachable, len(sites),
                f"  DOWN: {', '.join(down)}" if down else "")

    logger.info("  → Building trend signals...")
    trends = build_trend_signals(brand_names)

    logger.info("  → Loading revenue signal...")
    revenue = load_revenue_signal()
    if revenue:
        logger.info("  → Revenue: $%.2f / $%.2f (%.1f%% to goal, $%.2f/day needed)",
                    revenue.total_this_month, revenue.goal,
                    revenue.pct_to_goal, revenue.daily_needed)

    obs = ObservationSet(
        timestamp=datetime.utcnow().isoformat(),
        sites=sites,
        trends=trends,
        revenue=revenue,
    )
    logger.info("[OBSERVE] Complete — %d signals collected", len(sites) + len(trends) + 1)
    return obs
