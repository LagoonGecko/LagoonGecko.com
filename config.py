"""All the settings for your site live here. Edit this file to change
categories, search keywords, filters and the site name."""
import os

# ---- Site identity -------------------------------------------------------
SITE_NAME = os.getenv("SITE_NAME") or "LagoonGecko"
SITE_TAGLINE = "Trending aquarium & reptile gear, sorted and price-checked daily"
SITE_URL = os.getenv("SITE_URL") or "https://lagoongecko.com"  # your live domain (sitemap + custom domain)

# ---- Contact page --------------------------------------------------------
CONTACT_EMAIL = os.getenv("CONTACT_EMAIL", "hello@yourdomain.com")  # change to your real address
# Optional free form service so visitors can message you from the site.
# Sign up at formspree.io, create a form, paste its URL here (e.g. https://formspree.io/f/abcd1234)
CONTACT_FORM_URL = os.getenv("CONTACT_FORM_URL", "")

# ---- AliExpress affiliate API (set these as secrets, never in code) ------
APP_KEY = os.getenv("ALIEXPRESS_APP_KEY")
APP_SECRET = os.getenv("ALIEXPRESS_APP_SECRET")
TRACKING_ID = os.getenv("ALIEXPRESS_TRACKING_ID")
CURRENCY = os.getenv("CURRENCY", "USD")
SHIP_TO = os.getenv("SHIP_TO", "US")  # country your visitors mostly come from
LANGUAGE = "EN"

# ---- Amazon Associates (optional second store) ---------------------------
# Your Amazon tracking ID, e.g. "lagoongecko-20". Leave empty and all Amazon
# links stay hidden. Tip: apply only once the site gets visitors, because
# Amazon needs 3 sales within 180 days of applying.
AMAZON_TAG = os.getenv("AMAZON_TAG", "")
AMAZON_DOMAIN = os.getenv("AMAZON_DOMAIN", "www.amazon.com")

# ---- Optional: AI-written product summaries ------------------------------
ANTHROPIC_API_KEY = os.getenv("ANTHROPIC_API_KEY")
AI_MODEL = os.getenv("AI_MODEL", "claude-haiku-5-5")
AI_DESCRIPTIONS_PER_RUN = 40  # caps cost per daily run

# ---- Quality filters -----------------------------------------------------
MIN_POSITIVE_FEEDBACK = 92.0  # AliExpress % positive (≈ 4.6 stars)
MIN_ORDERS = 50               # recent orders, filters out untested products
MAX_PER_CATEGORY = 24         # products shown per category page
PAGES_PER_KEYWORD = 2         # 50 products per page from the API
BUDGET_LIMIT = 20.0           # "Best under $X" page
TRENDING_COUNT = 12
TREND_WINDOW_DAYS = 7

# ---- Categories: slug -> name, group, search keywords --------------------
CATEGORIES = {
    "aquarium-filters": {
        "name": "Filters & Air Pumps", "group": "Aquarium",
        "keywords": ["aquarium filter", "aquarium air pump", "sponge filter aquarium"],
    },
    "aquarium-heaters": {
        "name": "Heaters & Thermometers", "group": "Aquarium",
        "keywords": ["aquarium heater", "aquarium thermometer digital"],
    },
    "aquarium-lighting": {
        "name": "Aquarium Lighting", "group": "Aquarium",
        "keywords": ["aquarium led light", "planted tank light"],
    },
    "aquarium-decor": {
        "name": "Decor & Plants", "group": "Aquarium",
        "keywords": ["aquarium decoration", "artificial aquarium plants", "aquarium driftwood"],
    },
    "aquarium-cleaning": {
        "name": "Cleaning & Maintenance", "group": "Aquarium",
        "keywords": ["aquarium gravel vacuum", "aquarium algae magnet cleaner", "aquascape tools"],
    },
    "betta-nano": {
        "name": "Betta & Nano Tanks", "group": "Aquarium",
        "keywords": ["betta fish tank", "betta hammock leaf", "nano aquarium"],
    },
    "reptile-heating": {
        "name": "Heat Lamps & Mats", "group": "Reptile",
        "keywords": ["reptile heat lamp", "reptile heating pad", "uvb lamp reptile"],
    },
    "reptile-hides": {
        "name": "Hides & Habitat Decor", "group": "Reptile",
        "keywords": ["reptile hide cave", "reptile hammock", "terrarium decoration"],
    },
    "reptile-feeding": {
        "name": "Feeding & Water", "group": "Reptile",
        "keywords": ["reptile feeding tongs", "reptile water dish", "reptile feeder bowl"],
    },
    "reptile-monitoring": {
        "name": "Thermostats & Hygrometers", "group": "Reptile",
        "keywords": ["reptile thermometer hygrometer", "reptile thermostat", "terrarium mister"],
    },
}
