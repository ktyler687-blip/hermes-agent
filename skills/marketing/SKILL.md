---
name: marketing-automation
description: Autonomous AI marketing & revenue agent for 7 managed brands. Runs daily loops: trend scanning, content generation (TikTok/Pinterest/Blog), ad copy, SEO optimization, content multiplication, scaling advice, and revenue tracking. Targets $10K/month. Requires ANTHROPIC_API_KEY.
version: 2.0.0
author: Hermes Agent
license: MIT
platforms: [linux, macos]
prerequisites:
  commands: [python3]
  env_vars: [ANTHROPIC_API_KEY]
metadata:
  hermes:
    tags: [marketing, social-media, tiktok, pinterest, seo, ads, automation, revenue]
---

# Autonomous Marketing & Revenue Agent

AI-powered daily execution engine for 7 managed brands targeting **$10K/month**.

## Managed Brands

| Brand | URL | Niche |
|-------|-----|-------|
| TheFlavorCrave | https://theflavorcrave.com/ | Food & viral recipes |
| HealthIsWealth | https://healthiswealth.live/ | Health & wellness |
| Humming Nectar | https://hummingnectar-6d2kwf3s.manus.space/ | Natural beverages |
| TasteTable LA | https://tastetablela.vercel.app/ | LA food scene |
| Kids Lunch Recipes | https://kids-lunch-recipes.manus.space/ | Kids meals |
| CramTools | https://cramtools-site.vercel.app/ | Study & productivity |
| Live Live Radio | https://liveliveradio.wordpress.com/ | Music & radio |

---

## Daily Execution Loop

```
LOOP: DAILY()
  Step 1: scan_market_trends()      → top 5 trends per brand w/ ROI scores
  Step 2: pick_top_roi(n=2)         → select highest opportunity brands
  Step 3: generate_content()        → TikTok scripts + Pinterest + Blog
  Step 4: create_ads()              → primary + 5 hooks + 3 CTAs + A/B
  Step 5: optimize_pages()          → SEO keywords + quick wins + meta
  Step 6: multiply_content()        → 1 piece → 8 platform variants
  Step 7: decide_scaling()          → budget allocation + growth tactics
  Step 8: suggest_automation()      → #1 workflow to automate
  → save_report()                   → JSON report in reports/
```

---

## Quick Start

```bash
export ANTHROPIC_API_KEY=sk-ant-...

# Run daily loop now (picks top 2 brands by ROI)
python skills/marketing/daily_agent.py

# Dry run — see the plan, no API cost
python skills/marketing/daily_agent.py --dry-run

# Full loop for all 7 brands
python skills/marketing/daily_agent.py --all

# Single brand
python skills/marketing/daily_agent.py --brand TheFlavorCrave

# View dashboard from last run
python skills/marketing/daily_agent.py --dashboard

# Fine-grained campaign runner
python skills/marketing/campaign_runner.py --brand HealthIsWealth --mode content
python skills/marketing/campaign_runner.py --brand CramTools --mode ads
python skills/marketing/campaign_runner.py --all --mode seo

# Revenue tracking
python skills/marketing/revenue_tracker.py --status
python skills/marketing/revenue_tracker.py --forecast
python skills/marketing/revenue_tracker.py --log TheFlavorCrave 450.00 affiliate

# Install cron schedule (daily 6am automation)
bash skills/marketing/scheduler.sh
```

---

## Campaign Modes

| Mode | Output |
|------|--------|
| `full` | All steps |
| `content` | TikTok scripts + Pinterest posts + Blog draft |
| `ads` | Primary ad + 5 hooks + 3 CTAs + video script + A/B variants |
| `seo` | Keywords + quick wins + meta templates + featured snippets |
| `trends` | Top 5 trending topics per brand with urgency + ROI scores |
| `scaling` | Budget split + growth tactics + revenue opportunities |

---

## Files

```
skills/marketing/
├── SKILL.md              ← this file
├── brands.py             ← brand profiles + URLs
├── trend_scanner.py      ← market trend analysis
├── content_generator.py  ← TikTok, Pinterest, Blog
├── ad_creator.py         ← hooks, CTAs, ad copy
├── seo_optimizer.py      ← keyword + page optimization
├── content_multiplier.py ← 1-to-8 platform repurposing
├── scaling_advisor.py    ← budget + growth + revenue
├── daily_agent.py        ← DAILY() autonomous loop ← START HERE
├── campaign_runner.py    ← fine-grained campaign CLI
├── revenue_tracker.py    ← $10K/month goal tracker
├── scheduler.sh          ← install cron automation
└── reports/              ← daily JSON reports (auto-created)
```
