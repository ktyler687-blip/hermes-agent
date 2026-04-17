"""Content generator — TikTok scripts, Pinterest posts, and blog updates per brand."""

import json
import logging
from typing import List, Dict, Any

import anthropic

from brands import Brand, BRANDS

logger = logging.getLogger(__name__)

CONTENT_SYSTEM_PROMPT = """You are a top-tier social media content strategist who writes
viral, platform-native content. You know exactly what hooks stop the scroll on TikTok,
what visuals perform on Pinterest, and what SEO-driven angles win on blogs.
Write like a human creator who deeply understands each brand's audience.
Always return valid JSON only — no markdown, no preamble."""


def generate_tiktok_scripts(brand: Brand, trend_topics: List[str], client: anthropic.Anthropic, count: int = 3) -> List[Dict]:
    prompt = f"""Write {count} viral TikTok video scripts for this brand.

Brand: {brand.name}
Niche: {brand.niche}
Audience: {brand.audience}
Tone: {brand.tone}
Trending topics to leverage: {', '.join(trend_topics[:3])}
Hashtags: {' '.join(brand.hashtags[:5])}

Return ONLY a JSON array of {count} scripts in this format:
[
  {{
    "title": "video concept title",
    "hook": "first 3 seconds — must stop the scroll",
    "script": "full spoken script (15-60 seconds, punchy, platform-native)",
    "visual_directions": "what to show on screen",
    "caption": "post caption with hashtags",
    "cta": "end call to action",
    "estimated_views": "low/medium/high/viral",
    "best_post_time": "Mon-Fri 6-8pm EST"
  }}
]"""

    response = client.messages.create(
        model="claude-opus-4-7",
        max_tokens=2500,
        system=CONTENT_SYSTEM_PROMPT,
        messages=[{"role": "user", "content": prompt}],
    )
    raw = _clean_json(response.content[0].text)
    return json.loads(raw)


def generate_pinterest_posts(brand: Brand, trend_topics: List[str], client: anthropic.Anthropic, count: int = 5) -> List[Dict]:
    prompt = f"""Create {count} high-converting Pinterest pins for this brand.

Brand: {brand.name}
Niche: {brand.niche}
Audience: {brand.audience}
Tone: {brand.tone}
Trending topics: {', '.join(trend_topics[:3])}
Keywords: {', '.join(brand.keywords[:5])}

Return ONLY a JSON array of {count} pins:
[
  {{
    "title": "pin title (SEO-optimized, 60-100 chars)",
    "description": "pin description (150-300 chars, keyword-rich)",
    "image_concept": "detailed description of the ideal image/graphic",
    "board": "which Pinterest board to post to",
    "keywords": ["keyword1", "keyword2"],
    "link_destination": "type of page to link to (recipe, product, blog, etc)",
    "cta_overlay": "text to overlay on the image"
  }}
]"""

    response = client.messages.create(
        model="claude-opus-4-7",
        max_tokens=2000,
        system=CONTENT_SYSTEM_PROMPT,
        messages=[{"role": "user", "content": prompt}],
    )
    raw = _clean_json(response.content[0].text)
    return json.loads(raw)


def generate_blog_update(brand: Brand, trend_topics: List[str], client: anthropic.Anthropic) -> Dict:
    prompt = f"""Write a full SEO blog post draft for this brand.

Brand: {brand.name}
Niche: {brand.niche}
Audience: {brand.audience}
Tone: {brand.tone}
Primary trend to cover: {trend_topics[0] if trend_topics else brand.content_pillars[0]}
Target keywords: {', '.join(brand.keywords[:4])}

Return ONLY a JSON object:
{{
  "title": "SEO-optimized blog post title",
  "meta_description": "155-char meta description",
  "slug": "url-friendly-slug",
  "target_keyword": "primary keyword",
  "secondary_keywords": ["kw1", "kw2", "kw3"],
  "outline": ["H2 section 1", "H2 section 2", "H2 section 3", "H2 section 4"],
  "intro": "compelling 2-paragraph introduction",
  "body": "full article body (800-1200 words, use H2/H3 headers, conversational tone)",
  "conclusion": "call-to-action conclusion paragraph",
  "internal_link_suggestions": ["related post idea 1", "related post idea 2"],
  "estimated_read_time": "X min read"
}}"""

    response = client.messages.create(
        model="claude-opus-4-7",
        max_tokens=3000,
        system=CONTENT_SYSTEM_PROMPT,
        messages=[{"role": "user", "content": prompt}],
    )
    raw = _clean_json(response.content[0].text)
    return json.loads(raw)


def generate_all_content(
    brand: Brand,
    trend_data: Dict[str, Any],
    client: anthropic.Anthropic,
) -> Dict[str, Any]:
    """Generate full content suite for a brand from trend data."""
    trend_topics = [t["topic"] for t in trend_data.get("top_trends", [])]

    logger.info("Generating TikTok scripts for %s...", brand.name)
    tiktok_scripts = generate_tiktok_scripts(brand, trend_topics, client)

    logger.info("Generating Pinterest posts for %s...", brand.name)
    pinterest_posts = generate_pinterest_posts(brand, trend_topics, client)

    logger.info("Generating blog post for %s...", brand.name)
    blog_update = generate_blog_update(brand, trend_topics, client)

    return {
        "tiktok_scripts": tiktok_scripts,
        "pinterest_posts": pinterest_posts,
        "blog_update": blog_update,
    }


def _clean_json(text: str) -> str:
    text = text.strip()
    if text.startswith("```"):
        parts = text.split("```")
        text = parts[1] if len(parts) > 1 else text
        if text.startswith("json"):
            text = text[4:]
    return text.strip()
