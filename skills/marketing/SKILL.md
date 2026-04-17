---
name: marketing-automation
description: AI-powered marketing automation for multi-brand social media management. Scans market trends, generates TikTok scripts, Pinterest posts, blog content, ad copy, SEO updates, and scaling recommendations across all managed brands.
version: 1.0.0
author: Hermes Agent
license: MIT
platforms: [linux, macos]
prerequisites:
  commands: [python3, uv]
  env_vars: [ANTHROPIC_API_KEY]
metadata:
  hermes:
    tags: [marketing, social-media, tiktok, pinterest, seo, ads, content, automation]
---

# Marketing Automation — Multi-Brand Social Media Manager

Full-stack marketing automation for managing and growing multiple social media brands using AI.

## Managed Brands

- **TheFlavorCrave** — Food content & recipes
- **HealthIsWealth** — Health, wellness & nutrition
- **Humming Nectar** — Natural beverages & lifestyle
- **TasteTable LA** — LA food scene & restaurant content
- **Kids Lunch Recipes** — Family & kids meal content
- **CramTools** — Productivity & study tools
- **Live Live Radio** — Music, radio & audio content

## Features

- **Market Trend Scanner** — Identifies trending topics per brand niche
- **Content Generator** — TikTok scripts, Pinterest posts, blog updates
- **Ad Creator** — Primary ads, hooks, and CTAs per brand
- **SEO Optimizer** — Keyword-optimized page/post updates
- **Content Multiplier** — Repurposes one piece across all platforms
- **Scaling Advisor** — Recommends budget & audience scaling moves
- **Automation Planner** — Suggests workflow automations

## Usage

```bash
# Run full campaign for all brands
python marketing/campaign_runner.py --all

# Run for specific brand
python marketing/campaign_runner.py --brand TheFlavorCrave

# Generate content only
python marketing/campaign_runner.py --brand HealthIsWealth --mode content

# Generate ads only
python marketing/campaign_runner.py --brand CramTools --mode ads

# Full report as JSON
python marketing/campaign_runner.py --all --output report.json
```

## Output Format

```json
{
  "selected_brands": ["TheFlavorCrave", "HealthIsWealth"],
  "strategy": "...",
  "content": {
    "tiktok_scripts": [...],
    "pinterest_posts": [...],
    "blog_update": "..."
  },
  "ads": {
    "primary": "...",
    "hooks": [...],
    "ctas": [...]
  },
  "scaling": "...",
  "automation": "...",
  "revenue_opportunity": "..."
}
```
