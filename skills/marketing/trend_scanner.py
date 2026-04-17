"""Market trend scanner — identifies trending topics per brand niche using Claude."""

import json
import logging
from typing import List, Dict, Any

import anthropic

from brands import Brand, BRANDS

logger = logging.getLogger(__name__)


TREND_SYSTEM_PROMPT = """You are a social media trend analyst with deep expertise in content marketing.
Your job is to identify the highest-ROI trending topics for a specific brand niche RIGHT NOW.
Focus on trends that are peaking (not already saturated), have strong engagement potential,
and align with the brand's voice and audience. Always return valid JSON only."""


def scan_trends_for_brand(brand: Brand, client: anthropic.Anthropic) -> Dict[str, Any]:
    """Scan and return top trending topics for a brand."""
    prompt = f"""Analyze current market trends for this brand and return a JSON object.

Brand: {brand.name}
Niche: {brand.niche}
Audience: {brand.audience}
Keywords: {', '.join(brand.keywords)}
Content Pillars: {', '.join(brand.content_pillars)}

Return ONLY valid JSON in this exact format:
{{
  "brand": "{brand.name}",
  "top_trends": [
    {{
      "topic": "trend topic name",
      "why_trending": "brief explanation",
      "content_angle": "how this brand should approach it",
      "platforms": ["TikTok", "Pinterest"],
      "urgency": "high|medium|low",
      "estimated_reach_multiplier": 2.5
    }}
  ],
  "avoid_topics": ["oversaturated topic 1", "topic 2"],
  "seasonal_opportunity": "any seasonal or time-sensitive opportunity",
  "competitor_gap": "content gap vs competitors the brand can fill"
}}

Return exactly 5 top trends, ordered by ROI potential."""

    response = client.messages.create(
        model="claude-opus-4-7",
        max_tokens=1500,
        system=TREND_SYSTEM_PROMPT,
        messages=[{"role": "user", "content": prompt}],
    )

    raw = response.content[0].text.strip()
    # Strip markdown code fences if present
    if raw.startswith("```"):
        raw = raw.split("```")[1]
        if raw.startswith("json"):
            raw = raw[4:]
    return json.loads(raw.strip())


def scan_all_brands(client: anthropic.Anthropic, brand_names: List[str] | None = None) -> Dict[str, Any]:
    """Scan trends for multiple brands and return combined results."""
    targets = brand_names or list(BRANDS.keys())
    results = {}

    for name in targets:
        brand = BRANDS.get(name)
        if not brand:
            logger.warning("Unknown brand: %s", name)
            continue
        logger.info("Scanning trends for %s...", name)
        try:
            results[name] = scan_trends_for_brand(brand, client)
        except Exception as e:
            logger.error("Trend scan failed for %s: %s", name, e)
            results[name] = {"error": str(e)}

    return results


def pick_top_roi_brands(trend_results: Dict[str, Any], count: int = 2) -> List[str]:
    """Select the top N brands by average estimated reach multiplier."""
    scores: List[tuple[str, float]] = []

    for brand_name, data in trend_results.items():
        if "error" in data:
            continue
        trends = data.get("top_trends", [])
        if not trends:
            continue
        avg_score = sum(t.get("estimated_reach_multiplier", 1.0) for t in trends) / len(trends)
        high_urgency_bonus = sum(1 for t in trends if t.get("urgency") == "high") * 0.3
        scores.append((brand_name, avg_score + high_urgency_bonus))

    scores.sort(key=lambda x: x[1], reverse=True)
    return [name for name, _ in scores[:count]]
