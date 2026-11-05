"""Buying guides. Each kit item links to the matching category, shows the
current top pick from the daily data, and (if set up) an Amazon search.

To add a guide, copy one block below and edit it. `category` must be a slug
from config.CATEGORIES (or None), `amazon` is the Amazon search phrase, and
`match` (optional) lists words the top pick's title should contain."""

GUIDES = [
    {
        "slug": "guide-betta-tank-setup",
        "title": "Beginner betta tank setup",
        "eyebrow": "Deep water · Starter guide",
        "bg": "underwater",
        "teaser": "Everything a betta needs to thrive, and what to skip, for a healthy first tank.",
        "minutes": 5,
        "intro": ("Bettas are often sold as fish that can live in a bowl, but they do far better in a small, "
                  "heated, filtered tank. The good news: a proper betta setup is simple and affordable."),
        "facts": [("Tank size", "5 gallons (19 L) or more"), ("Water temperature", "76–82°F (24–28°C)"),
                  ("Filter", "Gentle flow only"), ("Before adding fish", "Cycle the tank first")],
        "sections": [
            ("Pick the right tank", [
                "Aim for at least 5 gallons (about 19 litres). A bigger volume of water keeps temperature and water "
                "quality more stable, which means fewer problems for you and a healthier fish.",
                "Choose a tank with a lid. Bettas can jump, and a lid also reduces evaporation.",
            ]),
            ("Keep the water warm and gently filtered", [
                "Bettas are tropical fish, so a heater isn't optional in most homes. Use an adjustable heater and a "
                "thermometer so you can see the temperature at a glance.",
                "Bettas have long fins and don't like strong currents. A sponge filter, or a filter with an "
                "adjustable flow, is ideal.",
            ]),
            ("Add places to rest and hide", [
                "Bettas love resting near the surface. A floating 'hammock' leaf, live or silk plants, and a cave or "
                "piece of driftwood give them places to explore and hide. Avoid sharp plastic decorations that can "
                "tear fins.",
            ]),
            ("Cycle the tank before your betta moves in", [
                "A new tank needs time to grow the beneficial bacteria that break down waste. Run the filter for "
                "a few weeks first (see our guide to cycling a new aquarium), and always use a water conditioner "
                "when adding tap water.",
            ]),
        ],
        "kit": [
            {"item": "Nano tank (5 gal+)", "match": ["tank","aquarium kit"], "why": "Stable water and room to swim.", "category": "betta-nano", "amazon": "5 gallon betta tank kit"},
            {"item": "Adjustable heater", "match": ["heater"], "why": "Keeps water in the 76–82°F range.", "category": "aquarium-heaters", "amazon": "adjustable aquarium heater 50w"},
            {"item": "Sponge filter", "match": ["sponge"], "why": "Cleans the water without strong current.", "category": "aquarium-filters", "amazon": "sponge filter air pump small aquarium"},
            {"item": "Plants & hammock leaf", "match": ["hammock","plant","leaf","moss"], "why": "Resting spots and hiding places.", "category": "aquarium-decor", "amazon": "betta hammock leaf"},
            {"item": "Gentle LED light", "match": ["light","led"], "why": "Shows off colours and keeps plants growing.", "category": "aquarium-lighting", "amazon": "nano aquarium led light"},
        ],
    },
    {
        "slug": "guide-cycle-new-aquarium",
        "title": "How to cycle a new aquarium",
        "eyebrow": "Deep water · Essentials",
        "bg": "underwater",
        "teaser": "The step most beginners skip, and the reason most first fish get sick.",
        "minutes": 6,
        "intro": ("Fish produce ammonia, which is toxic. In an established tank, beneficial bacteria turn ammonia into "
                  "nitrite and then into far less harmful nitrate. 'Cycling' means growing those bacteria before you "
                  "add fish."),
        "facts": [("Typical time", "4–8 weeks"), ("Done when", "Ammonia & nitrite read 0"),
                  ("You'll need", "Liquid test kit"), ("Then", "Add fish slowly")],
        "sections": [
            ("Set up everything first", [
                "Fill the tank, add a water conditioner, and run the filter and heater as normal. The bacteria live "
                "mostly in the filter media and substrate, so the filter must run the whole time.",
            ]),
            ("Feed the bacteria", [
                "In a fishless cycle you add a small, measured source of ammonia (bottled aquarium ammonia or a pinch "
                "of fish food) so the bacteria have something to grow on. Bottled 'starter bacteria' products can "
                "speed this up.",
            ]),
            ("Test, don't guess", [
                "Test the water every few days. You'll see ammonia rise, then nitrite rise as ammonia falls, then "
                "nitrite fall as nitrate appears. When ammonia and nitrite both read zero within a day of adding "
                "ammonia, the tank is cycled.",
                "Liquid test kits are more accurate than strips and last much longer.",
            ]),
            ("Add fish gradually", [
                "Do a partial water change to lower nitrate, then add a few fish at a time so the bacteria can keep up. "
                "Keep testing for the first few weeks.",
            ]),
        ],
        "kit": [
            {"item": "Filter", "match": ["filter"], "why": "Home for the beneficial bacteria.", "category": "aquarium-filters", "amazon": "aquarium filter"},
            {"item": "Heater & thermometer", "match": ["heater"], "why": "Bacteria grow faster in warm water.", "category": "aquarium-heaters", "amazon": "aquarium heater thermometer"},
            {"item": "Gravel vacuum", "match": ["vacuum","siphon"], "why": "For the water changes once fish are in.", "category": "aquarium-cleaning", "amazon": "aquarium gravel vacuum siphon"},
            {"item": "Liquid test kit", "why": "Tells you exactly when the cycle is done.", "category": None, "amazon": "aquarium master test kit liquid"},
            {"item": "Water conditioner", "why": "Removes chlorine from tap water.", "category": None, "amazon": "aquarium water conditioner"},
        ],
    },
    {
        "slug": "guide-leopard-gecko-starter-kit",
        "title": "Leopard gecko starter kit",
        "eyebrow": "Jungle · Starter guide",
        "bg": "jungle",
        "teaser": "The complete checklist for a happy leopard gecko, from heat to hides.",
        "minutes": 6,
        "intro": ("Leopard geckos are one of the friendliest reptiles for beginners. They're hardy and calm, but they "
                  "depend completely on you for the right warmth, hiding spots and nutrition."),
        "facts": [("Enclosure", "40 gal / 36×18×18 in (90×45×45 cm)+"), ("Warm side surface", "88–92°F (31–33°C)"),
                  ("Cool side", "Mid-70s °F (around 24°C)"), ("Hides", "At least 3, incl. a humid hide")],
        "sections": [
            ("Give them room", [
                "Modern care guides recommend at least a 40-gallon (about 90 × 45 × 45 cm) enclosure for an adult. "
                "More floor space means a better temperature gradient and more room to explore.",
            ]),
            ("Heat with a gradient, and always use a thermostat", [
                "Leopard geckos regulate their temperature by moving between warm and cool areas. Heat one end of the "
                "enclosure with a heat mat or an overhead heat source, and leave the other end cooler.",
                "Every heat source should run through a thermostat. It stops overheating and is the single most "
                "important safety item in the setup. Check temperatures with a digital thermometer.",
            ]),
            ("Three hides, minimum", [
                "Provide a warm hide, a cool hide, and a humid hide (a hide with damp moss inside) to help them shed. "
                "Add climbing branches and plants for enrichment.",
            ]),
            ("Lighting and feeding", [
                "A day/night light cycle helps, and many keepers now add low-level UVB. Feed live insects and dust "
                "them with a calcium supplement. Use shallow dishes so insects can't escape, and keep a water dish "
                "available at all times.",
            ]),
        ],
        "kit": [
            {"item": "Heat mat or lamp", "match": ["heat mat","heating","heat emitter","heat lamp","ceramic"], "why": "Creates the warm side of the gradient.", "category": "reptile-heating", "amazon": "reptile heat mat leopard gecko"},
            {"item": "Thermostat & thermometer", "match": ["thermostat"], "why": "Prevents overheating, the #1 safety item.", "category": "reptile-monitoring", "amazon": "reptile thermostat"},
            {"item": "Hides (warm, cool, humid)", "match": ["hide","cave"], "why": "Security and healthy shedding.", "category": "reptile-hides", "amazon": "reptile hide cave"},
            {"item": "Feeding dish & water bowl", "match": ["dish","bowl","feeder"], "why": "Escape-proof insects and fresh water.", "category": "reptile-feeding", "amazon": "reptile food dish escape proof"},
            {"item": "Calcium supplement", "why": "Dust insects for strong bones.", "category": None, "amazon": "reptile calcium with d3"},
        ],
    },
    {
        "slug": "guide-bearded-dragon-setup",
        "title": "Bearded dragon setup checklist",
        "eyebrow": "Jungle · Starter guide",
        "bg": "jungle",
        "teaser": "Bearded dragons need serious heat and UVB. Here's how to get it right first time.",
        "minutes": 6,
        "intro": ("Bearded dragons are curious, interactive and great for beginners, but they have bigger setup "
                  "needs than most reptiles, especially for heat and UVB lighting."),
        "facts": [("Adult enclosure", "4×2×2 ft (120×60×60 cm)"), ("Basking spot", "Around 100–110°F (38–43°C)"),
                  ("Cool side", "75–85°F (24–29°C)"), ("UVB", "Strong linear tube, replaced on schedule")],
        "sections": [
            ("Plan for adult size", [
                "A baby dragon grows fast. An adult needs an enclosure of around 4 × 2 × 2 ft (120 × 60 × 60 cm), so "
                "buying that size from the start saves money.",
            ]),
            ("A hot basking spot and a cool retreat", [
                "Dragons need a hot basking spot at one end and a cooler area at the other. Use a basking lamp on a "
                "dimming thermostat and check the basking surface with a digital thermometer.",
                "Babies and juveniles usually need a slightly lower basking temperature than adults. Check a "
                "species-specific care sheet for your dragon's age.",
            ]),
            ("UVB is not optional", [
                "Bearded dragons need strong UVB to absorb calcium. A linear UVB tube in a reflector, running about "
                "12–14 hours a day, is the standard. UVB output fades over time, so replace bulbs as the "
                "manufacturer recommends, even if they still glow.",
            ]),
            ("Decor and feeding", [
                "Add a sturdy basking platform, a hide, and branches to climb. Feed a mix of live insects and fresh "
                "greens, and dust insects with calcium.",
            ]),
        ],
        "kit": [
            {"item": "Basking lamp & fixture", "match": ["basking","dome","lamp"], "why": "The hot spot they need to digest.", "category": "reptile-heating", "amazon": "reptile basking lamp dome"},
            {"item": "Thermostat & thermometer", "match": ["thermostat"], "why": "Keeps the basking spot in range.", "category": "reptile-monitoring", "amazon": "dimming thermostat reptile"},
            {"item": "Hide & basking platform", "match": ["hide","cave","platform","hammock"], "why": "Somewhere to bask and somewhere to retreat.", "category": "reptile-hides", "amazon": "bearded dragon basking platform"},
            {"item": "Food & water dishes", "match": ["dish","bowl"], "why": "Shallow, easy-to-clean bowls.", "category": "reptile-feeding", "amazon": "reptile feeding dish"},
            {"item": "Linear UVB tube", "why": "Essential for healthy bones.", "category": None, "amazon": "t5 ho uvb reptile 10.0"},
        ],
    },
    {
        "slug": "guide-budget-upgrades-under-20",
        "title": "Best tank upgrades under $20",
        "eyebrow": "Budget expedition",
        "bg": "river",
        "teaser": "Small, cheap upgrades that make a real difference to any tank or terrarium.",
        "minutes": 4,
        "intro": ("You don't need to spend a lot to improve your setup. These inexpensive upgrades make tank "
                  "maintenance easier and your animals happier."),
        "facts": [("Budget", "Under $20 each"), ("Best for", "Aquariums & terrariums"),
                  ("Biggest impact", "Thermometer & cleaning tools"), ("Updated", "Daily prices")],
        "sections": [
            ("Measure before you guess", [
                "A cheap digital thermometer (and a hygrometer for reptiles) is the most useful upgrade you can buy. "
                "Most problems start with temperatures or humidity being off without anyone noticing.",
            ]),
            ("Make maintenance quicker", [
                "A gravel vacuum and an algae magnet turn a dreaded chore into a ten-minute job, which means you'll "
                "actually do it regularly.",
            ]),
            ("Add enrichment", [
                "Live or silk plants, driftwood, a new hide or a hammock give fish and reptiles more places to explore "
                "and feel secure. Swap decor around occasionally to keep things interesting.",
            ]),
        ],
        "kit": [
            {"item": "Digital thermometer / hygrometer", "match": ["hygrometer","thermometer"], "why": "Spot problems before they start.", "category": "reptile-monitoring", "amazon": "digital thermometer hygrometer reptile"},
            {"item": "Gravel vacuum or algae magnet", "match": ["vacuum","magnet","scraper"], "why": "Faster, easier cleaning.", "category": "aquarium-cleaning", "amazon": "aquarium algae magnet cleaner"},
            {"item": "Plants & driftwood", "match": ["driftwood","plant","moss"], "why": "Instant enrichment and a natural look.", "category": "aquarium-decor", "amazon": "aquarium driftwood"},
            {"item": "A new hide", "match": ["hide","cave"], "why": "More security for shy reptiles.", "category": "reptile-hides", "amazon": "reptile hide cave"},
        ],
    },
]
