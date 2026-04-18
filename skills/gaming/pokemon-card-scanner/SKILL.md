---
name: pokemon-card-scanner
description: >
  Identify and value Pokemon cards (and other collectible trading cards) from photos.
  Extracts card name, set, number, rarity, condition, and current market price using
  vision analysis and web search. Supports Pokemon TCG, Magic: The Gathering,
  Yu-Gi-Oh!, and other collectible card games.
version: 1.0.0
author: Hermes Agent
license: MIT
metadata:
  hermes:
    tags: [Gaming, Pokemon, TCG, Cards, Vision, Collectibles, Magic, Yu-Gi-Oh, Valuation]
    category: gaming
    related_skills: [pokemon-player]
    requires_tools: [vision_analyze]
---

# Pokemon Card Scanner

Identify collectible trading cards from photos and look up their current market value.

## When to Use

- User says "scan my card", "identify this card", "what's this card worth"
- User uploads or pastes a photo of a Pokemon, Magic, Yu-Gi-Oh!, or other TCG card
- User asks about card rarity, condition, set, or price
- User wants to catalog or appraise their card collection
- User asks "is this card fake/counterfeit?"

## Procedure

### Step 1: Get the Card Image

Accept the card image in any of these formats:
- A URL the user pastes (http/https)
- A local file path (e.g. `/home/user/card.jpg`)
- An already-analyzed image — if the user pasted an image into the chat, vision pre-processing may have already run; use the injected description AND call `vision_analyze` again with the targeted prompt below for higher accuracy

If no image has been provided, ask: "Please share a clear photo of the card — front face, well-lit, in focus."

### Step 2: Analyze the Card with Vision

Call `vision_analyze` with the image and the following structured prompt:

```
This is a collectible trading card. Please identify and extract ALL of the following:

CARD GAME: Which TCG is this? (Pokemon, Magic: The Gathering, Yu-Gi-Oh!, other)

CARD IDENTITY:
- Full card name (exactly as printed)
- Set name and set symbol description
- Card/collector number (e.g. 025/165)
- Edition or print run (1st Edition, Shadowless, Unlimited, etc.)
- Language (English, Japanese, Korean, etc.)

POKEMON TCG SPECIFICS (if applicable):
- Pokemon type(s) and HP
- Rarity symbol (circle=common, diamond=uncommon, star=rare, double-star=ultra rare, crown=secret rare, etc.)
- Energy cost and attack names
- Illustrator name (bottom of card)
- Holographic or special treatment (holo, reverse holo, full-art, rainbow, gold, etc.)

MAGIC: THE GATHERING SPECIFICS (if applicable):
- Mana cost and card type
- Rarity (C/U/R/M symbol)
- Set symbol and collector number
- Foil treatment

YU-GI-OH! SPECIFICS (if applicable):
- Card type (Monster/Spell/Trap), ATK/DEF
- Rarity (Common, Rare, Ultra Rare, Secret Rare, etc.)
- Edition (1st Edition, Unlimited)

CONDITION ASSESSMENT:
Rate the card condition on the standard scale:
- Mint (M): Perfect, no flaws
- Near Mint (NM): Nearly perfect, minimal handling
- Lightly Played (LP): Minor wear, slight scratches
- Moderately Played (MP): Noticeable wear, creases
- Heavily Played (HP): Significant damage
- Damaged (D): Major damage affecting playability
Point out any visible flaws (scratches, bends, whitening, ink marks).

AUTHENTICITY FLAGS:
Note anything that looks unusual vs. an authentic card: off-center printing, incorrect font, wrong texture pattern, color saturation issues, missing holographic pattern, incorrect card back.
```

### Step 3: Look Up Market Value (Optional but Recommended)

If the card was successfully identified, use `web_search` to find its current price:

Search query: `"[card name]" "[set name]" "[card number]" price TCGPlayer OR PriceCharting OR eBay sold 2025`

Look for:
- **TCGPlayer** market price (most reliable for Pokemon/MTG in US)
- **CardMarket** for European prices
- **PriceCharting** for historical trends
- **eBay completed/sold listings** for real transaction prices

Report the price range (low / market / high) and note if the condition affects value significantly.

### Step 4: Report Results

Present findings in this structure:

```
## Card Identified: [Card Name]

**Game:** [TCG Name]
**Set:** [Set Name] · #[Number]
**Rarity:** [Rarity] · [Treatment]
**Language:** [Language] · [Edition]

### Details
[Key stats — HP/attacks for Pokemon, mana cost/type for MTG, ATK/DEF for YGO]
**Illustrator:** [Name] *(Pokemon only)*

### Condition: [Grade]
[Brief description of visible condition. List any specific flaws noted.]

### Estimated Market Value
| Condition | Price (USD) |
|-----------|-------------|
| NM        | $XX.XX      |
| LP        | $XX.XX      |
| MP        | $XX.XX      |
*Source: [TCGPlayer / PriceCharting / eBay — as of [date]]*

### Notes
[Any authenticity concerns, notable variants, or additional context]
```

## Handling Multiple Cards

If the user shares multiple card images:
- Process each card individually with a separate `vision_analyze` call
- Summarize with a total estimated collection value at the end

## Pitfalls

- **Blurry or dark images**: Ask for a better photo before proceeding — low-quality images lead to misidentification. Request: flat on a neutral background, good lighting, no glare, camera directly above.
- **Back of card only**: Politely ask for the front — the back alone cannot identify a specific card.
- **Cropped images**: Set symbols, card numbers, and rarity indicators are often at the edges; a full-card photo is needed.
- **Fakes**: If authenticity flags are raised, be clear about uncertainty and recommend professional grading (PSA, BGS, CGC) before purchase or sale.
- **Prices vary widely**: Always note that card prices fluctuate daily. The price is an estimate, not a guaranteed offer.
- **Graded cards (PSA/BGS slabs)**: If the card is inside a grading slab, identify the grading company, grade number, and cert number shown, then search for that specific graded card's value.
- **Japanese cards**: Values differ significantly from English printings — search specifically for Japanese prices on sites like YYT or TCGPlayer Japan.
