"""Demo mode: fills the database with SAMPLE products (not real listings)
and 14 days of history, so you can see the full site working before your
AliExpress API keys are approved. Real runs never use this."""
import datetime as dt
import os
import random

import config
import db

SAMPLES = {
    "aquarium-filters": ["Ultra-Quiet Sponge Filter", "3-in-1 Internal Filter Pump", "Hang-On-Back Waterfall Filter",
                         "Silent Air Pump Dual Outlet", "Biochemical Double Sponge Filter", "Canister Filter Media Kit"],
    "aquarium-heaters": ["Adjustable Submersible Heater 100W", "LED Digital Aquarium Thermometer",
                         "Mini Betta Heater 10W", "Titanium Heater with Controller", "Stick-On Tank Thermometer Strip"],
    "aquarium-lighting": ["Full-Spectrum Planted Tank LED", "Clip-On Nano Aquarium Light", "RGB Sunrise Timer LED Bar",
                          "Waterproof Submersible LED Strip", "Extendable Brackets LED Light"],
    "aquarium-decor": ["Natural Spider Driftwood", "Silk Artificial Plant Set 10pcs", "Resin Shipwreck Ornament",
                       "Lava Rock Cave Hideout", "Moss Ball 5-Pack", "Floating Betta Log"],
    "aquarium-cleaning": ["Siphon Gravel Vacuum Kit", "Floating Algae Magnet Cleaner", "Stainless Aquascape Tool Set",
                          "Long-Handle Algae Scraper", "Fish Net Fine Mesh 2-Pack"],
    "betta-nano": ["Betta Hammock Leaf Bed", "5L Desktop Nano Tank Kit", "Betta Mirror Exercise Toy",
                   "Self-Cleaning Mini Aquarium", "Floating Betta Hideout Log"],
    "reptile-heating": ["Ceramic Heat Emitter 100W", "Under-Tank Heating Mat", "UVB 5.0 Reptile Bulb",
                        "Basking Lamp Dome Fixture", "Infrared Night Heat Bulb"],
    "reptile-hides": ["Resin Rock Reptile Cave", "Bearded Dragon Hammock", "Leopard Gecko Moist Hide",
                      "Bendable Jungle Vine 2m", "Cork Bark Tunnel Hide", "Terrarium Background 3D"],
    "reptile-feeding": ["Stainless Steel Feeding Tongs 2pc", "Escape-Proof Worm Dish", "Rock-Look Water Bowl",
                        "Suction Cup Gecko Feeder Ledge", "Ceramic Food Dish Set"],
    "reptile-monitoring": ["Digital Thermometer Hygrometer", "Reptile Thermostat Controller",
                           "Automatic Terrarium Mister", "Dual-Probe Temperature Gauge", "Humidity Fogger Mini"],
}

COLORS = {"Aquarium": ("#3fb8b0", "#10302b"), "Reptile": ("#7fae4a", "#1a2c1a")}


def _placeholder_image(out_dir, pid, label, group):
    fg, bg = COLORS[group]
    os.makedirs(out_dir, exist_ok=True)
    svg = f"""<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 400 400">
<rect width="400" height="400" fill="{bg}"/>
<circle cx="200" cy="170" r="70" fill="none" stroke="{fg}" stroke-width="10"/>
<path d="M150 170 q50 -60 100 0 q-50 60 -100 0z" fill="{fg}" opacity=".35"/>
<text x="200" y="300" font-family="sans-serif" font-size="22" fill="{fg}" text-anchor="middle">SAMPLE</text>
<text x="200" y="330" font-family="sans-serif" font-size="16" fill="{fg}" text-anchor="middle">{label[:30]}</text>
</svg>"""
    with open(os.path.join(out_dir, f"{pid}.svg"), "w") as f:
        f.write(svg)
    return f"img/demo/{pid}.svg"


def load_demo(conn, site_dir, days=14):
    rng = random.Random(42)
    today = dt.date.today()
    img_dir = os.path.join(site_dir, "img", "demo")
    n = 0
    for slug, names in SAMPLES.items():
        group = config.CATEGORIES[slug]["group"]
        for name in names:
            n += 1
            pid = f"demo{n:03d}"
            base_orders = rng.randint(80, 4000)
            growth = rng.choice([0.0, 0.002, 0.005, 0.01, 0.03, 0.06])  # some products take off
            price = round(rng.uniform(1.5, 45), 2)
            image = _placeholder_image(img_dir, pid, name, group)
            for back in range(days, -1, -1):
                day = (today - dt.timedelta(days=back)).isoformat()
                orders = int(base_orders * (1 + growth) ** (days - back))
                day_price = price if back > 2 or rng.random() > 0.15 else round(price * 0.8, 2)
                db.upsert_product(conn, {
                    "id": pid, "title": f"{name} (sample product)", "image": image,
                    "url": "#demo-link", "category": slug, "price": day_price,
                    "original_price": round(price * rng.uniform(1.3, 2.2), 2),
                    "rating": round(rng.uniform(92, 99.5), 1), "orders": orders,
                    "commission": rng.choice([3, 7, 9]),
                }, day)
    conn.commit()
    print(f"Loaded {n} SAMPLE products with {days} days of history (demo mode)")
