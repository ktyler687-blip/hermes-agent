"""Ad copy generator — primary ads, scroll-stopping hooks, and CTAs per brand."""

import json
import logging
from typing import List, Dict, Any

import anthropic

from brands import Brand, BRANDS

logger = logging.getLogger(__name__)

AD_SYSTEM_PROMPT = """You are a direct-response copywriter who has written millions in profitable ad spend.
You write ads that stop the scroll, create immediate desire, and drive clicks.
Every hook must hit a pain point or curiosity gap within 3 words.
Every CTA must create urgency. Always return valid JSON only."""


def generate_ads(brand: Brand, trend_topics: List[str], client: anthropic.Anthropic) -> Dict[str, Any]:
    prompt = f"""Write high-converting ad copy for this brand for multiple platforms.

Brand: {brand.name}
Niche: {brand.niche}
Audience: {brand.audience}
Tone: {brand.tone}
Trending topics: {', '.join(trend_topics[:3])}
Revenue model: {brand.revenue_model}
CTA style: {brand.cta_style}

Return ONLY a JSON object:
{{
  "primary": {{
    "headline": "main ad headline (under 8 words, bold claim or question)",
    "body": "ad body copy (2-4 sentences, problem → solution → proof → offer)",
    "platform": "best platform for this ad",
    "format": "video/image/carousel/story",
    "audience_targeting": "who to target with this ad"
  }},
  "hooks": [
    "Hook 1 — pain point angle (under 6 words)",
    "Hook 2 — curiosity gap angle",
    "Hook 3 — social proof angle",
    "Hook 4 — contrarian/bold claim angle",
    "Hook 5 — before/after transformation angle"
  ],
  "ctas": [
    "CTA 1 — urgency-driven",
    "CTA 2 — benefit-driven",
    "CTA 3 — curiosity-driven"
  ],
  "video_ad_script": {{
    "hook_visual": "first frame visual description",
    "hook_text": "on-screen text overlay in first 2 seconds",
    "body": "15-30 second spoken script",
    "offer": "the specific offer or value prop",
    "close": "closing line + CTA"
  }},
  "retargeting_ad": {{
    "headline": "retargeting headline for warm audience",
    "body": "retargeting copy (shorter, more direct)",
    "cta": "direct retargeting CTA"
  }},
  "a_b_variants": [
    {{
      "variant": "A",
      "angle": "emotional appeal",
      "headline": "variant A headline",
      "body": "variant A body"
    }},
    {{
      "variant": "B",
      "angle": "logical/data appeal",
      "headline": "variant B headline",
      "body": "variant B body"
    }}
  ]
}}"""

    response = client.messages.create(
        model="claude-opus-4-7",
        max_tokens=2500,
        system=AD_SYSTEM_PROMPT,
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
