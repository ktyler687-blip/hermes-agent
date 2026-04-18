---
name: pokemon-card-scanner
description: >
  Identify and value collectible trading cards and sports cards from photos.
  Extracts card name, set, number, rarity, condition, and current market price using
  vision analysis and web search, then displays results in a modern popup UI.
  Supports Pokemon TCG, Magic: The Gathering, Yu-Gi-Oh!, and sports cards
  (Baseball, Basketball, Football, Hockey, Soccer, UFC, Golf, etc.).
version: 2.0.0
author: Hermes Agent
license: MIT
metadata:
  hermes:
    tags: [Gaming, Pokemon, TCG, Cards, Vision, Collectibles, Magic, Yu-Gi-Oh, Sports Cards, Baseball, Basketball, Football, Valuation, Popup UI]
    category: gaming
    related_skills: [pokemon-player]
    requires_tools: [vision_analyze]
---

# Card Scanner — Pokemon, TCG & Sports Cards

Identify any collectible card from a photo, assess its condition, look up market value, and display results in a beautiful popup UI.

## When to Use

- User says "scan my card", "identify this card", "what's this card worth", "scan my sports card"
- User uploads or pastes a photo of any collectible card
- User asks about card rarity, condition, set, print run, or price
- User wants to appraise a collection
- User asks "is this card fake?", "is this real?", "is this authentic?"
- User mentions any of: Pokemon, Magic, Yu-Gi-Oh!, baseball card, rookie card, Prizm, Topps, Panini, Upper Deck, Bowman, Refractor

## Step 1: Get the Card Image

Accept the card image in any of these formats:
- A URL pasted by the user (http/https)
- A local file path (e.g. `/home/user/card.jpg`)
- An already-analyzed image — if vision pre-processing already ran, use that description AND call `vision_analyze` again with the targeted prompt below for higher accuracy

If no image has been provided, ask:
> "Please share a clear photo of the card — front face, well-lit, in focus, flat on a neutral background."

## Step 2: Analyze the Card with Vision

Call `vision_analyze` with the image URL/path and this full structured prompt:

```
This is a collectible trading card or sports card. Extract ALL of the following with maximum precision:

━━━ CARD GAME / SPORT ━━━
What type of card is this?
- Trading Card Game: Pokemon TCG, Magic: The Gathering, Yu-Gi-Oh!, other TCG
- Sports Card: Baseball, Basketball, Football, Hockey, Soccer, UFC, Golf, Tennis, Wrestling, other sport

━━━ CARD IDENTITY ━━━
- Full card name (player name for sports, character name for TCG)
- Set/product name (e.g. "2023 Topps Chrome", "Scarlet & Violet — 151")
- Card number / collector number (e.g. 025/165, RC-45)
- Year of production / print run year
- Edition or variation (1st Edition, Shadowless, Unlimited, Rookie Card, Short Print, SSP)
- Language (English, Japanese, Korean, Spanish, etc.)
- Brand/manufacturer (Topps, Panini, Upper Deck, Bowman, Fleer, Donruss, Score, Select, etc.)

━━━ POKEMON TCG SPECIFICS (if Pokemon) ━━━
- Pokemon name, type(s), and HP
- Rarity symbol: circle=common, diamond=uncommon, star=rare, 2-star=ultra rare, crown=secret rare
- Energy cost and attack names + damage
- Illustrator name (bottom-right corner)
- Holographic / special treatment: base holo, reverse holo, full-art, rainbow rare, gold rare, trainer gallery, alt-art, illustration rare

━━━ MAGIC: THE GATHERING SPECIFICS (if MTG) ━━━
- Mana cost and card type (Creature, Instant, Sorcery, etc.)
- Rarity symbol (C/U/R/M)
- Set symbol and collector number
- Foil treatment (regular foil, borderless, extended art, showcase, etched)
- Power/Toughness if creature

━━━ YU-GI-OH! SPECIFICS (if YGO) ━━━
- Card type (Monster/Spell/Trap), Attribute, Level/Rank
- ATK / DEF values
- Rarity (Common, Rare, Super, Ultra, Secret, Starlight, etc.)
- Edition (1st Edition, Unlimited)
- Set code (e.g. LOB-EN005)

━━━ SPORTS CARD SPECIFICS (if sports) ━━━
- Player full name
- Team and position
- Sport (Baseball, Basketball, Football, Hockey, Soccer, etc.)
- Year / Season
- Is this a Rookie Card (RC)?
- Card number and parallel variation (base, Refractor, Prizm, Gold, Red, Blue, etc.)
- Serial number if present (e.g. /25, /10, /1 — one-of-ones)
- Autograph present? (on-card auto or sticker auto)
- Patch / memorabilia embedded?
- Grading slab present? If yes: grading company (PSA/BGS/SGC/CGC), grade number, certification number

━━━ CONDITION ASSESSMENT ━━━
Rate on the standard scale:
- Gem Mint (GM/10): Flawless — only used by PSA/BGS
- Mint (M/9): Near perfect, microscopic flaws only
- Near Mint (NM/8): Minimal handling wear, no creases
- Lightly Played (LP/7): Minor edge wear, slight scratches
- Moderately Played (MP/6): Noticeable wear, light creasing
- Heavily Played (HP/5): Significant wear, creases, marks
- Damaged (D/1-4): Major damage affecting playability/display

List any visible flaws: scratches, edge whitening, creases, print defects, centering issues, surface marks, ink smudges.
Estimate centering ratio if visible (e.g. 60/40, 55/45).

━━━ AUTHENTICITY ━━━
Flag anything unusual vs. an authentic card:
- Off-center or blurry printing
- Incorrect font or font weight
- Wrong card stock texture or thickness appearance
- Missing or incorrect holographic pattern
- Color saturation or ink bleed issues
- Incorrect card back design
- Rosette pattern anomalies (a key counterfeit indicator)
```

## Step 3: Look Up Market Value

After identification, use `web_search` to find current prices.

**For Pokemon/TCG cards:**
```
"[card name]" "[set name]" "[card number]" "[treatment]" price site:tcgplayer.com OR pricecharting.com
```

**For sports cards:**
```
"[year] [brand] [player name]" "[parallel/variation]" "[serial number if any]" price eBay sold OR PSA OR 130point.com
```

Look for:
- **TCGPlayer** — best for Pokemon/MTG/YGO market prices
- **PriceCharting** — historical trends for all card types
- **PWCC / Goldin / eBay Sold Listings** — real transaction prices for sports cards
- **PSA Population Report** — how rare is this grade for graded cards
- **130point.com / Market Movers** — sports card market data

Report: low / market / high price range, and note graded vs. raw card price difference.

## Step 4: Display Results with Popup UI

After collecting all data, run the popup script to show results in a beautiful browser window.

### Build the JSON payload

Assemble the card data into this JSON structure:

```json
{
  "game": "Pokemon TCG",
  "name": "Charizard",
  "set": "Base Set",
  "number": "4/102",
  "rarity": "Holo Rare",
  "treatment": "Shadowless Holo",
  "language": "English",
  "edition": "1st Edition",
  "condition": "NM",
  "condition_notes": "Minor edge whitening on back, 60/40 centering front.",
  "image_url": "<original URL or local path the user provided>",
  "details": {
    "HP": "120",
    "Type": "Fire",
    "Attacks": "Fire Spin 100",
    "Illustrator": "Mitsuhiro Arita"
  },
  "prices": [
    {"condition": "NM",  "price": "$8,500"},
    {"condition": "LP",  "price": "$5,200"},
    {"condition": "MP",  "price": "$2,800"}
  ],
  "price_source": "TCGPlayer / PriceCharting",
  "authenticity": "Authentic — all security features present.",
  "notes": "Shadowless 1st Edition Charizard — among the most iconic cards in the hobby."
}
```

**Sports card example:**
```json
{
  "game": "Basketball",
  "name": "LeBron James",
  "set": "2003-04 Topps Chrome",
  "number": "111",
  "rarity": "Refractor",
  "treatment": "Refractor /500",
  "language": "English",
  "edition": "Rookie Card",
  "condition": "NM",
  "condition_notes": "Sharp corners, no visible scratches. Clean surface.",
  "image_url": "<url or path>",
  "details": {
    "Team": "Cleveland Cavaliers",
    "Position": "Small Forward",
    "Year": "2003-04",
    "Serial": "/500"
  },
  "prices": [
    {"condition": "PSA 10",  "price": "$28,000"},
    {"condition": "PSA 9",   "price": "$8,500"},
    {"condition": "Raw NM",  "price": "$4,200"}
  ],
  "price_source": "eBay Sold Listings / PWCC",
  "authenticity": "Authentic — consistent with genuine Topps Chrome refractor stock.",
  "notes": "LeBron Rookie Refractor — one of the cornerstone modern sports cards."
}
```

### Run the popup script

```bash
cd <path to this skill's scripts directory>
python3 card_popup.py '<json_string>'
```

The script will:
1. Generate a modern self-contained HTML page with the card data
2. Open it automatically in the default browser
3. Print the path to the saved HTML file

After running, tell the user: *"Your card scan results are open in the browser!"*

### Also display a text summary in chat

Show a clean summary in the conversation as well:

```
## [Card Name] — [Set] #[Number]
**Game/Sport:** [type] · **Rarity:** [rarity] · **Condition:** [condition]
**Market Value (NM):** [price] · Source: [source]
[authenticity line]
```

## Handling Multiple Cards

Process each card image individually with separate `vision_analyze` calls. Run the popup once per card (multiple browser tabs). After all cards, summarize:
- Total cards scanned
- Total estimated collection value
- Highest-value card

## Pitfalls

- **Blurry or dark images**: Ask for a better photo before proceeding — misidentification on low-quality images leads to wrong values.
- **Back of card only**: Ask for the front — the back alone cannot identify a specific card.
- **Cropped images**: Set symbols, card numbers, and rarity markers are at the edges — always ask for a full card photo.
- **Fakes and reprints**: If authenticity flags are raised, be transparent and recommend professional grading (PSA, BGS, CGC, SGC) before any purchase or sale.
- **Prices fluctuate daily**: Always note that prices are estimates based on recent data, not guaranteed offers.
- **Graded slabs (PSA/BGS/SGC/CGC)**: Identify the grading company, grade, and cert number from the label; search for that specific graded pop/price.
- **Japanese / non-English cards**: Values differ significantly from English — specify language in the search query.
- **Serial-numbered cards**: Always note the exact serial number (e.g., /10) — it dramatically affects value.
- **1/1 one-of-one cards**: These are auction-only items; provide recent comparable auction results, not a fixed price.
- **Sticker autos vs. on-card autos**: On-card autos are worth significantly more — the popup `details` field should note which type.
- **Popup won't open**: If `xdg-open` fails (headless environment), tell the user the path to the HTML file so they can open it manually.
