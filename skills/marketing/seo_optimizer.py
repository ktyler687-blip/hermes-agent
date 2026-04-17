"""SEO optimizer — keyword analysis, page optimization recommendations, and meta updates."""

import json
import logging
from typing import List, Dict, Any

import anthropic

from brands import Brand

logger = logging.getLogger(__name__)

SEO_SYSTEM_PROMPT = """You are a technical SEO expert who specializes in content-driven organic growth.
You analyze brand niches and return actionable SEO recommendations that drive real traffic.
Focus on low-competition, high-intent keywords. Always return valid JSON only."""


def optimize_seo(brand: Brand, trend_topics: List[str], client: anthropic.Anthropic) -> Dict[str, Any]:
    prompt = f"""Generate a complete SEO optimization plan for this brand.

Brand: {brand.name}
Niche: {brand.niche}
Audience: {brand.audience}
Current keywords: {', '.join(brand.keywords)}
Trending topics: {', '.join(trend_topics[:4])}
Platforms: {', '.join(brand.platforms)}

Return ONLY a JSON object:
{{
  "primary_keyword_strategy": {{
    "head_term": "main keyword to own",
    "monthly_search_volume": "estimated searches/month",
    "difficulty": "low/medium/high",
    "rationale": "why this keyword"
  }},
  "long_tail_keywords": [
    {{
      "keyword": "exact long-tail phrase",
      "intent": "informational/commercial/transactional",
      "monthly_volume": "estimated",
      "content_type": "blog/video/product page"
    }}
  ],
  "quick_wins": [
    {{
      "action": "specific SEO action to take",
      "page_type": "home/blog/product/social",
      "impact": "high/medium/low",
      "effort": "low/medium/high",
      "example": "concrete example of implementation"
    }}
  ],
  "content_gap_keywords": ["keyword 1", "keyword 2", "keyword 3"],
  "meta_templates": {{
    "title_formula": "formula for page titles",
    "description_formula": "formula for meta descriptions",
    "example_title": "example title using the formula",
    "example_description": "example meta description"
  }},
  "internal_linking_strategy": "recommendation for internal link structure",
  "featured_snippet_opportunities": [
    {{
      "query": "question likely to trigger featured snippet",
      "answer_format": "paragraph/list/table",
      "draft_answer": "50-word answer optimized for snippet"
    }}
  ],
  "local_seo": "any local SEO recommendations if applicable",
  "monthly_content_plan": [
    "Month 1 priority keyword/topic",
    "Month 2 priority keyword/topic",
    "Month 3 priority keyword/topic"
  ]
}}

Include exactly 8 long-tail keywords and 5 quick wins."""

    response = client.messages.create(
        model="claude-opus-4-7",
        max_tokens=2500,
        system=SEO_SYSTEM_PROMPT,
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
