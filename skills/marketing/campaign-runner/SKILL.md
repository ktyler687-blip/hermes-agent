---
name: campaign-runner
description: Run AI-powered marketing campaigns for any or all 7 managed brands. Generates trend analysis, TikTok scripts, Pinterest posts, blog content, ad copy (hooks/CTAs), SEO plans, scaling advice, and automation recommendations. Requires ANTHROPIC_API_KEY.
version: 1.0.0
author: Hermes Agent
license: MIT
platforms: [linux, macos]
prerequisites:
  commands: [python3, uv]
  env_vars: [ANTHROPIC_API_KEY]
metadata:
  hermes:
    tags: [marketing, campaigns, content, ads, seo, tiktok, pinterest]
---

# Campaign Runner

AI-powered marketing campaign generator using Claude Opus.

## Quick Start

```bash
export ANTHROPIC_API_KEY=your_key_here

# Full campaign for all 7 brands
python skills/marketing/campaign_runner.py --all

# Auto-pick top 2 brands by ROI opportunity
python skills/marketing/campaign_runner.py --all --pick-top 2

# Full campaign for one brand
python skills/marketing/campaign_runner.py --brand TheFlavorCrave

# Content only (TikTok + Pinterest + Blog)
python skills/marketing/campaign_runner.py --brand HealthIsWealth --mode content

# Ads only
python skills/marketing/campaign_runner.py --brand CramTools --mode ads

# SEO plan only
python skills/marketing/campaign_runner.py --brand KidsLunchRecipes --mode seo

# Trend scan only
python skills/marketing/campaign_runner.py --all --mode trends

# Save to custom output file
python skills/marketing/campaign_runner.py --brand TasteTableLA --output my_report.json
```

## Campaign Modes

| Mode | What it generates |
|------|------------------|
| `full` | Everything: trends + content + ads + SEO + scaling |
| `content` | TikTok scripts, Pinterest posts, blog update |
| `ads` | Primary ad, 5 hooks, 3 CTAs, video script, A/B variants |
| `seo` | Keywords, quick wins, meta templates, featured snippet targets |
| `trends` | Top 5 trending topics per brand with urgency scores |
| `scaling` | Budget allocation, growth tactics, revenue opportunities |

## Output

Reports are saved as JSON to `reports/` by default.
The JSON shape matches:

```json
{
  "selected_brands": ["TheFlavorCrave"],
  "strategy": "...",
  "content": {
    "tiktok_scripts": [...],
    "pinterest_posts": [...],
    "blog_update": {...}
  },
  "ads": {
    "primary": "headline",
    "hooks": [...],
    "ctas": [...]
  },
  "scaling": [...],
  "automation": "...",
  "revenue_opportunity": "..."
}
```
