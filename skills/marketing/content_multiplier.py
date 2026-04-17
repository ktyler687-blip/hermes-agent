"""Content multiplier — repurposes one piece of content across all platforms."""

import json
import logging
from typing import Dict, Any

import anthropic

from brands import Brand

logger = logging.getLogger(__name__)

MULTIPLIER_SYSTEM_PROMPT = """You are an expert content repurposing strategist.
Given one piece of content, you transform it into platform-native versions
for TikTok, Pinterest, Instagram, YouTube Shorts, Twitter/X, LinkedIn, and email newsletters.
Each version must feel native to that platform — not a copy-paste.
Always return valid JSON only."""


def multiply_content(
    brand: Brand,
    source_content: str,
    source_type: str,
    client: anthropic.Anthropic,
) -> Dict[str, Any]:
    """Take one piece of content and repurpose it for all platforms."""
    prompt = f"""Repurpose this content for every platform this brand uses.

Brand: {brand.name}
Niche: {brand.niche}
Tone: {brand.tone}
Source content type: {source_type}
Source content:
---
{source_content[:1500]}
---

Return ONLY a JSON object with platform-native versions:
{{
  "source_summary": "one sentence summary of the source content",
  "repurposed": {{
    "tiktok": {{
      "hook": "scroll-stopping first line",
      "script": "15-30 second TikTok script",
      "caption": "caption + hashtags",
      "visual_direction": "what to show on screen"
    }},
    "instagram_reel": {{
      "hook": "hook text overlay",
      "script": "reel script",
      "caption": "caption + hashtags"
    }},
    "instagram_post": {{
      "caption": "long-form engaging caption",
      "image_concept": "image description",
      "hashtags": ["tag1", "tag2"]
    }},
    "pinterest": {{
      "title": "SEO pin title",
      "description": "pin description",
      "image_concept": "pin image idea"
    }},
    "youtube_short": {{
      "title": "YT short title",
      "script": "60-second script",
      "thumbnail_concept": "thumbnail description"
    }},
    "twitter_x": {{
      "tweet": "280-char tweet",
      "thread_starter": "thread opening tweet if expanded"
    }},
    "email_newsletter": {{
      "subject_line": "email subject",
      "preview_text": "preview snippet",
      "body_snippet": "2-3 paragraph email section"
    }},
    "blog_excerpt": {{
      "intro_paragraph": "blog-style intro",
      "cta": "end-of-post CTA"
    }}
  }},
  "posting_schedule": {{
    "day_1": "platform to post on day 1",
    "day_2": "platform for day 2",
    "day_3": "platform for day 3",
    "day_5": "platform for day 5",
    "day_7": "platform for day 7"
  }},
  "total_pieces_generated": 8
}}"""

    response = client.messages.create(
        model="claude-opus-4-7",
        max_tokens=3000,
        system=MULTIPLIER_SYSTEM_PROMPT,
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
