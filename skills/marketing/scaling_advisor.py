"""Scaling advisor — recommends budget allocation, audience scaling, and automation."""

import json
import logging
from typing import Dict, Any, List

import anthropic

from brands import Brand

logger = logging.getLogger(__name__)

SCALING_SYSTEM_PROMPT = """You are a growth marketing strategist with expertise in scaling
social media brands from 0 to 6-figure revenue. You give concrete, actionable scaling
recommendations with specific numbers, timelines, and tools. Always return valid JSON only."""


def get_scaling_plan(
    brand: Brand,
    content_data: Dict[str, Any],
    ads_data: Dict[str, Any],
    client: anthropic.Anthropic,
) -> Dict[str, Any]:
    prompt = f"""Create a scaling plan for this brand based on recent content and ad strategy.

Brand: {brand.name}
Niche: {brand.niche}
Revenue model: {brand.revenue_model}
Site: {brand.url}
Platforms: {', '.join(brand.platforms)}

Content generated: {len(content_data.get('tiktok_scripts', []))} TikTok scripts, {len(content_data.get('pinterest_posts', []))} Pinterest posts
Ad strategy: {ads_data.get('primary', {}).get('format', 'mixed')} format

Return ONLY a JSON object:
{{
  "current_stage": "launch/growth/scale/optimize",
  "30_day_goal": "specific measurable goal for next 30 days",
  "90_day_goal": "specific measurable goal for 90 days",
  "budget_allocation": {{
    "total_monthly_budget_suggested": "$X",
    "paid_ads": "X% — $X/month",
    "content_creation": "X% — $X/month",
    "tools_software": "X% — $X/month",
    "influencer_collab": "X% — $X/month"
  }},
  "top_scaling_moves": [
    {{
      "action": "specific action",
      "platform": "which platform",
      "expected_result": "measurable outcome",
      "timeline": "X days/weeks",
      "cost": "free/$X/month"
    }}
  ],
  "audience_growth_strategy": {{
    "primary_channel": "channel to focus on first",
    "growth_tactics": ["tactic 1", "tactic 2", "tactic 3"],
    "target_followers_30d": "X",
    "target_followers_90d": "X"
  }},
  "revenue_opportunity": {{
    "immediate_win": "quickest path to first/next $1k",
    "medium_term": "path to $5k/month in 90 days",
    "long_term": "path to $10k+/month in 6 months",
    "best_monetization": "top recommended monetization method for this brand"
  }},
  "automation": {{
    "recommended_tools": [
      {{
        "tool": "tool name",
        "use_case": "what to automate",
        "cost": "free/$X/month",
        "priority": "high/medium/low"
      }}
    ],
    "workflow_to_automate": "describe the #1 workflow to automate first",
    "time_saved_per_week": "estimated hours saved"
  }},
  "risk_flags": ["any risks or pitfalls to avoid"],
  "quick_wins_this_week": ["action 1", "action 2", "action 3"]
}}"""

    response = client.messages.create(
        model="claude-opus-4-7",
        max_tokens=2500,
        system=SCALING_SYSTEM_PROMPT,
        messages=[{"role": "user", "content": prompt}],
    )
    raw = _clean_json(response.content[0].text)
    return json.loads(raw)


def _clean_json(text: str) -> str:
    text = text.strip()
    if text.startswith("```"):
        parts = text.split("```")
        text = parts[1] if len(parts) > 1 else text
        if text.startswith("json"):
            text = text[4:]
    return text.strip()
