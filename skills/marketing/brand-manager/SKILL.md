---
name: brand-manager
description: View and update brand profiles for all 7 managed social media properties. Shows brand URLs, niches, keywords, content pillars, and revenue models.
version: 1.0.0
author: Hermes Agent
license: MIT
platforms: [linux, macos]
prerequisites:
  commands: [python3]
metadata:
  hermes:
    tags: [marketing, brands, management]
---

# Brand Manager

View and manage profiles for all 7 brands.

## List All Brands

```bash
python skills/marketing/campaign_runner.py --list-brands
```

## Brands

| Brand | URL | Niche |
|-------|-----|-------|
| TheFlavorCrave | https://theflavorcrave.com/ | Food & viral recipes |
| HealthIsWealth | https://healthiswealth.live/ | Health & wellness |
| Humming Nectar | https://hummingnectar-6d2kwf3s.manus.space/ | Natural beverages |
| TasteTable LA | https://tastetablela.vercel.app/ | LA food scene |
| Kids Lunch Recipes | https://kids-lunch-recipes.manus.space/ | Kids meals |
| CramTools | https://cramtools-site.vercel.app/ | Study & productivity |
| Live Live Radio | https://liveliveradio.wordpress.com/ | Music & radio |

To modify brand profiles, edit `skills/marketing/brands.py`.
