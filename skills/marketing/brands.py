"""Brand profiles for all managed social media properties."""

from dataclasses import dataclass, field
from typing import List, Dict

@dataclass
class Brand:
    name: str
    niche: str
    audience: str
    tone: str
    platforms: List[str]
    keywords: List[str]
    content_pillars: List[str]
    hashtags: List[str]
    cta_style: str
    revenue_model: str
    url: str = ""
    competitors: List[str] = field(default_factory=list)

BRANDS: Dict[str, Brand] = {
    "TheFlavorCrave": Brand(
        name="TheFlavorCrave",
        niche="Food content, viral recipes, restaurant trends",
        audience="Foodies aged 18-45, home cooks, food lovers",
        tone="Exciting, mouth-watering, conversational, trend-aware",
        platforms=["TikTok", "Pinterest", "Instagram", "Blog"],
        keywords=["viral recipes", "easy dinner ideas", "food trends 2025", "quick meals", "comfort food"],
        content_pillars=["Viral Recipes", "Restaurant Reviews", "Food Hacks", "Trending Dishes", "Meal Prep"],
        hashtags=["#TheFlavorCrave", "#FoodTok", "#RecipeOfTheDay", "#FoodLover", "#EasyRecipes", "#Foodie"],
        cta_style="Save this recipe + follow for daily food inspo",
        revenue_model="Affiliate links, brand partnerships, recipe ebook",
        url="https://theflavorcrave.com/",
        competitors=["TastyFood", "Delish", "BuzzFeedFood"],
    ),
    "HealthIsWealth": Brand(
        name="HealthIsWealth",
        niche="Health, wellness, nutrition, fitness lifestyle",
        audience="Health-conscious adults 25-50, wellness seekers",
        tone="Motivational, educational, empowering, science-backed",
        platforms=["TikTok", "Pinterest", "Instagram", "Blog", "YouTube"],
        keywords=["healthy lifestyle", "wellness tips", "nutrition facts", "weight loss", "mental health", "gut health"],
        content_pillars=["Nutrition Tips", "Wellness Habits", "Mental Health", "Fitness Basics", "Healthy Recipes"],
        hashtags=["#HealthIsWealth", "#WellnessJourney", "#HealthyLiving", "#NutritionTips", "#MindBodySoul"],
        cta_style="Follow for daily wellness tips that actually work",
        revenue_model="Digital wellness programs, supplements affiliation, coaching",
        url="https://healthiswealth.live/",
        competitors=["Well+Good", "MindBodyGreen", "Healthline"],
    ),
    "HummingNectar": Brand(
        name="Humming Nectar",
        niche="Natural beverages, herbal drinks, clean lifestyle",
        audience="Health-conscious millennials, natural product enthusiasts",
        tone="Calm, earthy, aspirational, aesthetic, wholesome",
        platforms=["TikTok", "Pinterest", "Instagram", "Blog"],
        keywords=["herbal drinks", "natural beverages", "clean living", "functional drinks", "wellness drinks"],
        content_pillars=["Drink Recipes", "Ingredient Spotlights", "Lifestyle Aesthetic", "DIY Brews", "Wellness Rituals"],
        hashtags=["#HummingNectar", "#NaturalDrinks", "#HerbalTea", "#CleanLiving", "#DrinkWell"],
        cta_style="Sip better, live better — follow for daily drink inspo",
        revenue_model="Product sales, brand partnerships, affiliate",
        url="https://hummingnectar-6d2kwf3s.manus.space/",
        competitors=["Olipop", "Poppi", "Rebbl"],
    ),
    "TasteTableLA": Brand(
        name="TasteTable LA",
        niche="LA food scene, restaurant reviews, local eats",
        audience="LA locals and tourists aged 21-45, food explorers",
        tone="Hip, local, insider, enthusiastic, place-based",
        platforms=["TikTok", "Instagram", "Pinterest", "Blog"],
        keywords=["LA restaurants", "best food in Los Angeles", "LA eats", "hidden gems LA", "LA foodie"],
        content_pillars=["Restaurant Reviews", "Hidden Gems", "LA Food Trends", "Neighborhood Guides", "Chef Spotlights"],
        hashtags=["#TasteTableLA", "#LAFoodie", "#LosAngelesEats", "#LARestaurants", "#EatLA"],
        cta_style="Follow to eat your way through LA like a local",
        revenue_model="Restaurant partnerships, sponsored posts, LA food guide ebook",
        url="https://tastetablela.vercel.app/",
        competitors=["Eater LA", "LA Weekly Food", "Infatuation LA"],
    ),
    "KidsLunchRecipes": Brand(
        name="Kids Lunch Recipes",
        niche="Kid-friendly meals, school lunches, family cooking",
        audience="Parents aged 28-45, caregivers, educators",
        tone="Warm, practical, encouraging, simple, family-focused",
        platforms=["Pinterest", "TikTok", "Instagram", "Blog"],
        keywords=["kids lunch ideas", "school lunch recipes", "picky eater tips", "healthy kids meals", "easy lunchbox"],
        content_pillars=["Lunchbox Ideas", "Picky Eater Solutions", "Quick Family Dinners", "Snack Ideas", "Meal Prep for Kids"],
        hashtags=["#KidsLunchRecipes", "#LunchboxIdeas", "#KidFriendlyFood", "#SchoolLunch", "#MomLife"],
        cta_style="Save this for tomorrow's lunchbox — follow for daily kid meal ideas",
        revenue_model="Pinterest affiliate, meal plan subscription, cookbooks",
        url="https://kids-lunch-recipes.manus.space/",
        competitors=["Weelicious", "Super Healthy Kids", "Yummy Toddler Food"],
    ),
    "CramTools": Brand(
        name="CramTools",
        niche="Study tools, productivity, student life, learning hacks",
        audience="Students aged 14-28, lifelong learners, productivity enthusiasts",
        tone="Energetic, practical, smart, meme-aware, motivational",
        platforms=["TikTok", "Pinterest", "YouTube", "Blog", "Instagram"],
        keywords=["study tips", "productivity tools", "best study apps", "how to study", "focus tips", "college hacks"],
        content_pillars=["Study Tips", "App Reviews", "Productivity Hacks", "Exam Prep", "Focus Techniques"],
        hashtags=["#CramTools", "#StudyTok", "#StudyWithMe", "#ProductivityTips", "#StudentLife"],
        cta_style="Follow for study hacks that actually save your GPA",
        revenue_model="Affiliate (apps, tools), digital study guides, sponsorships",
        url="https://cramtools-site.vercel.app/",
        competitors=["Thomas Frank", "Study MD", "Mike and Matty"],
    ),
    "LiveLiveRadio": Brand(
        name="Live Live Radio",
        niche="Music discovery, radio culture, audio content, live performances",
        audience="Music lovers aged 18-40, audiophiles, culture enthusiasts",
        tone="Vibrant, cultural, passionate, eclectic, community-driven",
        platforms=["TikTok", "Instagram", "Pinterest", "Blog", "Spotify"],
        keywords=["music discovery", "live radio", "underground music", "new music", "radio culture", "playlist"],
        content_pillars=["Music Discovery", "Artist Spotlights", "Playlist Curation", "Radio Culture", "Live Session Clips"],
        hashtags=["#LiveLiveRadio", "#MusicDiscovery", "#NewMusic", "#RadioVibes", "#MusicTok"],
        cta_style="Tune in + follow for music that moves you",
        revenue_model="Sponsorships, merchandise, event partnerships, Patreon",
        url="https://liveliveradio.wordpress.com/",
        competitors=["NTS Radio", "Poolside FM", "SiriusXM Digital"],
    ),
}

ALL_BRAND_NAMES = list(BRANDS.keys())
