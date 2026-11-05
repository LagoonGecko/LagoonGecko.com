"""Turns the database into a fast static website in ./site"""
import datetime as dt
import html
import os
import shutil

import config
import describe
import guides
import trends

SITE_DIR = os.path.join(os.path.dirname(__file__), "site")
ASSETS = os.path.join(os.path.dirname(__file__), "assets")
e = html.escape


def money(v, whole=False):
    if whole and float(v).is_integer():
        return f"${v:,.0f}" if config.CURRENCY == "USD" else f"{v:,.0f} {config.CURRENCY}"
    return f"${v:,.2f}" if config.CURRENCY == "USD" else f"{v:,.2f} {config.CURRENCY}"


def short(title, n=70):
    title = " ".join(title.split())
    return title if len(title) <= n else title[: n - 1].rsplit(" ", 1)[0] + "…"


def amazon_url(query):
    """Amazon search link carrying your Associates tag (empty if no tag set)."""
    if not config.AMAZON_TAG:
        return ""
    from urllib.parse import quote_plus
    return f"https://{config.AMAZON_DOMAIN}/s?k={quote_plus(query)}&tag={quote_plus(config.AMAZON_TAG)}"


def amazon_query(title):
    import re
    t = re.sub(r"\(.*?\)|\[.*?\]", " ", title)
    words = [w for w in re.findall(r"[A-Za-z][A-Za-z\-]+", t) if len(w) > 1][:6]
    return " ".join(words)


def amazon_link(query, label="Compare on Amazon", cls="alt"):
    url = amazon_url(query)
    return (f'<a class="{cls}" href="{e(url)}" target="_blank" rel="sponsored nofollow noopener">{e(label)} →</a>'
            if url else "")


def card(p, stats):
    s = stats.get(p["id"], {})
    cat = config.CATEGORIES.get(p["category"], {"name": ""})
    badges = []
    if s.get("growth_pct", 0) >= 15 and s.get("growth", 0) > 0:
        badges.append(f'<span class="badge hot">▲ {s["growth_pct"]:.0f}% this week</span>')
    if s.get("price_drop"):
        badges.append(f'<span class="badge drop">Price drop · was {money(s["was"])}</span>')
    old = (f'<s>{money(p["original_price"])}</s>'
           if p["original_price"] and p["original_price"] > p["price"] * 1.05 else "")
    return f"""<article class="card {cat.get('group', 'Aquarium').lower()}" data-price="{p['price']}" data-orders="{p['orders']}" data-growth="{s.get('growth_pct', 0):.1f}">
  <a class="img" href="{e(p['url'])}" target="_blank" rel="sponsored nofollow noopener"><img src="{e(p['image'])}" alt="{e(short(p['title'], 100))}" loading="lazy"></a>
  <div class="body">
    <div class="badges">{''.join(badges)}</div>
    <h3>{e(short(p['title']))}</h3>
    <p class="desc">{e(describe.text_for(p, cat))}</p>
    <div class="meta"><span>★ {p['rating']:.0f}% positive</span><span>{p['orders']:,} orders</span></div>
    <div class="buy"><span class="price">{money(p['price'])} {old}</span>
      <a class="btn" href="{e(p['url'])}" target="_blank" rel="sponsored nofollow noopener">View deal</a></div>
    {amazon_link(amazon_query(p['title']))}
  </div>
</article>"""


LOGO = """<svg viewBox="0 0 40 40" aria-hidden="true">
<circle cx="20" cy="20" r="19" fill="none" stroke="#ffb500" stroke-width="1.6"/>
<g fill="#ffb500"><ellipse cx="20" cy="17" rx="4.2" ry="7"/><circle cx="20" cy="8.5" r="3.4"/>
<path d="M20 23c-1 4 2 6 5 6.5c-2.6-1.6-3.4-3.4-2.8-6.5z"/>
<path d="M16.4 13.5l-5 -2.6l-.8 1.4l4.6 2.8z M23.6 13.5l5 -2.6l.8 1.4l-4.6 2.8z M16.6 20.5l-5.2 2.2l.6 1.5l5.2 -1.8z M23.4 20.5l5.2 2.2l-.6 1.5l-5.2 -1.8z"/></g>
<path d="M7 31c3-2 5-2 8 0s5 2 8 0s5-2 8 0" fill="none" stroke="#ffb500" stroke-width="1.8" stroke-linecap="round"/></svg>"""


def wordmark():
    name = config.SITE_NAME
    if name.lower().startswith("lagoon") and len(name) > 6:
        return f'<span class="wm"><small>{e(name[:6].lower())}</small>{e(name[6:].lower())}</span>'
    return f'<span class="wm">{e(name)}</span>'


def sechead(eyebrow, title, sid="", lead=""):
    idattr = f' id="{sid}"' if sid else ""
    return (f'<div class="sechead"{idattr}><span class="eyebrow">{e(eyebrow)}</span><h2>{e(title)}</h2>'
            + (f'<p class="lead">{e(lead)}</p>' if lead else "") + "</div>")


def pagehead(eyebrow, title, lead="", bg="river", extra=""):
    return (f'<div class="pagehead band {bg}"><div class="inner"><span class="eyebrow">{e(eyebrow)}</span><h1>{e(title)}</h1>'
            + (f'<p class="lead">{e(lead)}</p>' if lead else "") + extra + "</div></div>")


ICONS = {
    "Aquarium": """<svg viewBox="0 0 48 48" aria-hidden="true"><path d="M6 24c6-8 14-11 22-9c4 1 7 4 9 9c-2 5-5 8-9 9c-8 2-16-1-22-9z" fill="none" stroke="currentColor" stroke-width="2.4" stroke-linejoin="round"/><path d="M37 24l7-6v12z" fill="none" stroke="currentColor" stroke-width="2.4" stroke-linejoin="round"/><circle cx="14" cy="22" r="1.8" fill="currentColor"/><path d="M22 17c2 4 2 10 0 14" fill="none" stroke="currentColor" stroke-width="2"/></svg>""",
    "Reptile": """<svg viewBox="0 0 48 48" aria-hidden="true"><path d="M24 4c10 6 14 16 6 30c-2 3-4 6-6 10c-2-4-4-7-6-10C10 20 14 10 24 4z" fill="none" stroke="currentColor" stroke-width="2.4" stroke-linejoin="round"/><path d="M24 8v34M24 16l-6-4M24 16l6-4M24 24l-8-5M24 24l8-5M24 32l-7-4M24 32l7-4" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round"/></svg>""",
}

WAVE = """<svg class="wave" viewBox="0 0 1440 60" preserveAspectRatio="none" aria-hidden="true"><path d="M0 30 C 120 0 240 60 360 30 S 600 0 720 30 S 960 60 1080 30 S 1320 0 1440 30 V60 H0z" fill="currentColor"/></svg>"""

HERO_SCENE = """<svg class="scene" viewBox="0 0 1200 520" preserveAspectRatio="xMidYMax slice" aria-hidden="true">
<defs><linearGradient id="sky" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#0b1712"/><stop offset=".55" stop-color="#173322"/><stop offset="1" stop-color="#21402a"/></linearGradient>
<linearGradient id="water" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#12403d"/><stop offset="1" stop-color="#071816"/></linearGradient>
<radialGradient id="glow" cx=".72" cy=".22" r=".35"><stop offset="0" stop-color="#ffb500" stop-opacity=".28"/><stop offset="1" stop-color="#ffb500" stop-opacity="0"/></radialGradient></defs>
<rect width="1200" height="520" fill="url(#sky)"/><rect width="1200" height="520" fill="url(#glow)"/>
<circle cx="865" cy="120" r="46" fill="#ffcf5c" opacity=".9"/>
<path d="M0 320 L120 260 L230 290 L340 210 L440 265 L540 235 L640 280 L760 215 L850 250 L960 225 L1080 275 L1200 245 L1200 360 L0 360z" fill="#13291c"/>
<path d="M0 345 Q80 300 160 335 Q230 292 320 338 Q400 305 480 345 Q570 312 650 348 Q760 308 860 346 Q960 312 1060 344 Q1130 320 1200 338 L1200 372 L0 372z" fill="#0d1f15"/>
<g fill="#08140e">
<path d="M70 372 C80 290 70 230 48 180 C92 214 108 280 104 372z"/><path d="M48 182 C14 166 -12 190 -24 214 C10 196 28 192 48 182z"/>
<path d="M52 176 C70 128 116 116 150 132 C116 140 82 152 52 176z"/><path d="M50 182 C82 172 128 186 150 216 C116 200 82 192 50 182z"/>
<path d="M1130 372 C1124 300 1142 236 1166 186 C1120 218 1096 286 1098 372z"/><path d="M1164 188 C1190 148 1232 152 1250 172 C1214 168 1190 174 1164 188z"/>
<path d="M1162 186 C1144 142 1096 130 1066 144 C1102 150 1132 164 1162 186z"/><path d="M1166 190 C1132 186 1090 204 1072 236 C1108 218 1138 204 1166 190z"/>
<path d="M240 372 q12 -52 -8 -92 q28 34 22 92z"/><path d="M990 372 q-10 -58 12 -100 q-28 38 -20 100z"/>
<path d="M300 372 q30 -40 70 -36 q-40 8 -60 36z"/><path d="M900 372 q-30 -40 -70 -36 q40 8 60 36z"/>
</g>
<path d="M0 370 Q50 362 100 370 T200 370 T300 370 T400 370 T500 370 T600 370 T700 370 T800 370 T900 370 T1000 370 T1100 370 T1200 370 L1200 520 L0 520z" fill="url(#water)"/>
<path d="M760 386 h120 M700 400 h70 M820 404 h90" stroke="#ffcf5c" stroke-width="3" stroke-linecap="round" opacity=".35"/>
<g fill="#ffcf5c" opacity=".22"><circle cx="300" cy="450" r="4"/><circle cx="310" cy="430" r="2.5"/><circle cx="302" cy="414" r="1.8"/>
<circle cx="980" cy="470" r="3.5"/><circle cx="988" cy="450" r="2.2"/></g>
<g fill="#04100d" opacity=".95"><path d="M560 450 q18 -10 36 0 q-18 10 -36 0z M596 450 l10 -7 v14z"/><path d="M620 470 q14 -8 28 0 q-14 8 -28 0z M648 470 l8 -5 v10z"/>
<path d="M530 476 q12 -7 24 0 q-12 7 -24 0z M554 476 l7 -5 v10z"/></g>
<g stroke="#0e3a2a" stroke-width="5" fill="none" stroke-linecap="round"><path d="M120 520 q-14 -40 4 -80 q-16 -24 0 -50"/><path d="M150 520 q12 -36 -4 -66"/>
<path d="M1060 520 q14 -44 -6 -86 q14 -20 0 -44"/><path d="M1090 520 q-10 -30 6 -58"/></g>
</svg>"""


AMAZON_NOTE = " As an Amazon Associate we earn from qualifying purchases."

INFO_PAGES = [("about.html", "About us"), ("faq.html", "How it works & FAQ"),
              ("contact.html", "Contact us"), ("disclosure.html", "Affiliate disclosure")]


def guide_slider():
    n = len(guides.GUIDES)
    slides = "".join(
        f'<a class="gs-slide{" active" if i == 0 else ""}" href="{g["slug"]}.html" tabindex="{0 if i == 0 else -1}" '
        f'aria-hidden="{"false" if i == 0 else "true"}"><span class="gs-thumb {g["bg"]}"></span>'
        f'<span class="gs-body"><span class="eyebrow">{e(g["eyebrow"])}</span><b>{e(g["title"])}</b>'
        f'<span class="gs-teaser">{e(g["teaser"])}</span><span class="gmeta">Read guide · {g["minutes"]} min →</span></span></a>'
        for i, g in enumerate(guides.GUIDES))
    dots = "".join(f'<button class="gs-dot{" active" if i == 0 else ""}" type="button" aria-label="Show guide {i + 1}"></button>'
                   for i in range(n))
    return f"""<div class="gslider" aria-roledescription="carousel" aria-label="Buying guides">
<div class="gs-head"><span>Field guides</span><a href="guides.html">See all</a></div>
<div class="gs-slides">{slides}</div>
<div class="gs-nav"><button class="gs-arrow gs-prev" type="button" aria-label="Previous guide"><svg viewBox="0 0 24 24"><path d="M15 5l-7 7 7 7"/></svg></button>
<div class="gs-dots">{dots}</div>
<button class="gs-arrow gs-next" type="button" aria-label="Next guide"><svg viewBox="0 0 24 24"><path d="M9 5l7 7-7 7"/></svg></button></div></div>"""


def layout(title, body, description="", page_class=""):
    groups = {}
    for slug, c in config.CATEGORIES.items():
        groups.setdefault(c["group"], []).append(f'<a href="{slug}.html">{e(c["name"])}</a>')
    nav = "".join(f'<div class="navgroup"><b>{e(g)}</b>{"".join(links)}</div>' for g, links in groups.items())
    zone = {"Aquarium": "Deep water · Aquarium", "Reptile": "Jungle · Reptile"}
    menu_cols = "".join(
        f'<div class="mcol {g.lower()}"><b>{e(zone.get(g, g))}</b>{"".join(links)}</div>'
        for g, links in groups.items())
    menu_cols += f"""<div class="mcol"><b>Explore</b><a href="index.html#trending">Trending this week</a>
<a href="index.html#price-drops">Price drops</a><a href="guides.html">Buying guides</a><a href="budget.html">Best under {money(config.BUDGET_LIMIT, True)}</a></div>
<div class="mcol"><b>Info</b>{"".join(f'<a href="{u}">{e(t)}</a>' for u, t in INFO_PAGES)}</div>"""
    updated = dt.date.today().strftime("%d %B %Y")
    return f"""<!DOCTYPE html>
<html lang="en"><head><meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>{e(title)}</title><meta name="description" content="{e(description or config.SITE_TAGLINE)}">
<link rel="preconnect" href="https://fonts.googleapis.com"><link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=DM+Serif+Display&family=Manrope:wght@400;500;600;700;800&display=swap" rel="stylesheet">
<link rel="icon" href="img/bg/favicon.svg" type="image/svg+xml">
<link rel="stylesheet" href="style.css"></head>
<body class="{page_class}">
<header class="top"><div class="topnote">We earn a small commission when you buy through our links, at no extra cost to you.</div><div class="wrap">
  <a class="logo" href="index.html"><img src="img/bg/logo.svg" alt="{e(config.SITE_NAME)}" width="190" height="78"></a>
  <nav><a class="hide-sm" href="guides.html">Guides</a><a class="hide-sm" href="index.html#trending">Trending</a><a class="hide-sm" href="budget.html">Under {money(config.BUDGET_LIMIT, True)}</a>
    <div class="menu"><button class="menubtn" type="button" aria-expanded="false" aria-controls="menupanel">Explore
      <svg viewBox="0 0 12 8" aria-hidden="true"><path d="M1 1l5 5 5-5" fill="none" stroke="currentColor" stroke-width="2"/></svg></button>
      <div class="menupanel" id="menupanel" hidden>{menu_cols}</div></div>
  </nav>
</div></header>
<main class="wrap">{body}</main>
<footer><div class="footwave">{WAVE}</div><div class="wrap">
  <a class="logo" href="index.html"><img src="img/bg/logo.svg" alt="{e(config.SITE_NAME)}" width="190" height="78"></a>
  <div class="footnav">{nav}</div>
  <p>Prices and order counts update daily (last update {updated}) and can change on AliExpress.
  {e(config.SITE_NAME)} is a participant in the AliExpress affiliate program.{AMAZON_NOTE if config.AMAZON_TAG else ""}
  {" · ".join(f'<a href="{u}">{e(t)}</a>' for u, t in INFO_PAGES)}</p>
</div></footer>
<script src="site.js"></script>
</body></html>"""


def grid(products, stats, sortable=False):
    controls = ("""<div class="sortbar">Sort by <select id="sort">
<option value="orders">Most popular</option><option value="growth">Trending</option>
<option value="price">Lowest price</option></select></div>""" if sortable else "")
    return controls + '<div class="grid">' + "".join(card(p, stats) for p in products) + "</div>"


def write(name, content):
    with open(os.path.join(SITE_DIR, name), "w", encoding="utf-8") as f:
        f.write(content)


def build_info_pages():
    name = e(config.SITE_NAME)
    email = e(config.CONTACT_EMAIL)

    write("about.html", layout(f"About us | {config.SITE_NAME}", f"""{pagehead("Who we are", "About us")}
<p>{name} is a field guide to the best gear for creatures of the lagoon and the jungle. We help fishkeepers and
reptile owners find well-rated aquarium and terrarium gear at good prices, without scrolling through thousands
of listings.</p>
<h2>What we do</h2>
<p>Every day we scan thousands of AliExpress listings across {len(config.CATEGORIES)} categories. We only show products
with at least {config.MIN_POSITIVE_FEEDBACK:.0f}% positive feedback and {config.MIN_ORDERS}+ recent orders, and we track
their prices and sales so you can see what's trending and when prices drop.</p>
<h2>What we don't do</h2>
<p>We don't sell products ourselves, handle orders or ship anything. When you click "View deal" you buy directly from
the seller on AliExpress, under AliExpress's buyer protection.</p>
<p><a href="contact.html">Get in touch</a> · <a href="faq.html">Read the FAQ</a></p>"""))

    faqs = [
        ("Do you sell these products?",
         "No. We find and compare products. You buy directly from the seller on AliExpress, and your order, payment, "
         "shipping and returns are handled by AliExpress."),
        ("How do you choose which products to show?",
         f"Every day we search AliExpress for aquarium and reptile gear and keep only products with at least "
         f"{config.MIN_POSITIVE_FEEDBACK:.0f}% positive feedback and {config.MIN_ORDERS}+ recent orders. They're then "
         "ranked by popularity, and you can sort each category by price."),
        ("What does \"Trending this week\" mean?",
         "These are products whose recent orders have grown the fastest over the past 7 days."),
        ("What is a \"Price drop\"?",
         "The product is cheaper today than any price we've recorded for it before."),
        ("Are the prices on your site accurate?",
         "We update prices every day, but sellers can change them at any time. Always check the final price, "
         "shipping cost and delivery time on AliExpress before you buy."),
        ("How long does shipping take?",
         "It depends on the seller and your country. The delivery estimate is shown on the AliExpress product page."),
        ("I have a problem with my order. Who do I contact?",
         "Please contact the seller through your AliExpress account, or open a dispute with AliExpress buyer "
         "protection. We can't see or change orders."),
        ("Does it cost me more to buy through your links?",
         "No. You pay the same price. AliExpress pays us a small commission, which keeps this site running."),
    ]
    items = "".join(f'<details class="faq"><summary>{e(q)}</summary><p>{e(a)}</p></details>' for q, a in faqs)
    write("faq.html", layout(f"How it works & FAQ | {config.SITE_NAME}",
                             pagehead('Field notes', 'How it works & FAQ', 'Quick answers to common questions.') + items + ''
                             f'<p>Still have a question? <a href="contact.html">Contact us</a>.</p>'))

    if config.CONTACT_FORM_URL:
        form = f"""<form class="contact" action="{e(config.CONTACT_FORM_URL)}" method="POST">
<label>Your name<input name="name" required></label>
<label>Your email<input type="email" name="email" required></label>
<label>Message<textarea name="message" rows="6" required></textarea></label>
<button class="btn" type="submit">Send message</button></form>"""
    else:
        form = ""
    write("contact.html", layout(f"Contact us | {config.SITE_NAME}", f"""{pagehead("Send a signal", "Contact us", "Product suggestions, partnership ideas or feedback on the site: we'd love to hear from you.")}
<div class="contactbox"><b>Email</b><p><a href="mailto:{email}">{email}</a></p>
<p class="small">We usually reply within 1–2 business days.</p></div>
{form}
<div class="note"><b>Questions about an order?</b> We don't handle orders. Please contact the seller through your
AliExpress account, or see our <a href="faq.html">FAQ</a>.</div>"""))

    write("disclosure.html", layout(f"Affiliate disclosure | {config.SITE_NAME}", f"""{pagehead("The fine print", "Affiliate disclosure")}
<p>{name} is a participant in the AliExpress affiliate program. Links on this site are affiliate links: if you click
one and buy something, we may earn a commission. This costs you nothing extra.</p>
{"<p>" + name + " is also a participant in the Amazon Services LLC Associates Program. As an Amazon Associate we earn from qualifying purchases.</p>" if config.AMAZON_TAG else ""}
<p>Commissions don't change which products we show. Products are selected and ranked automatically by their ratings,
recent sales and price.</p>
<h2>Prices and availability</h2>
<p>Prices, stock, shipping and delivery times are set by AliExpress sellers and can change at any time. The price on
AliExpress at checkout is the one that applies.</p>"""))


def guide_cards(items):
    return '<div class="guides">' + "".join(
        f'<a class="gcard {g["bg"]}" href="{g["slug"]}.html"><span class="eyebrow">{e(g["eyebrow"])}</span>'
        f'<b>{e(g["title"])}</b><p>{e(g["teaser"])}</p><span class="gmeta">{g["minutes"]} min read →</span></a>'
        for g in items) + "</div>"


def top_pick(by_cat, slug, stats, budget=False, match=None):
    items = by_cat.get(slug, [])
    if match:
        items = [p for p in items if any(m in p["title"].lower() for m in match)] or items
    if budget:
        items = [p for p in items if p["price"] <= config.BUDGET_LIMIT] or items
    return max(items, key=lambda p: (p["rating"] >= 95, p["orders"]), default=None)


def kit_row(k, by_cat, stats, budget):
    cat = config.CATEGORIES.get(k["category"]) if k["category"] else None
    pick = top_pick(by_cat, k["category"], stats, budget, k.get("match")) if cat else None
    if pick and budget and pick["price"] > config.BUDGET_LIMIT:
        pick = None  # never show an over-budget pick in a budget guide
    links = []
    if cat:
        links.append(f'<a class="alt" href="{k["category"]}.html">See all {e(cat["name"].lower())} →</a>')
    links.append(amazon_link(k["amazon"], "Find it on Amazon"))
    links = " ".join(l for l in links if l) or '<span class="alt">Available at most pet stores.</span>'
    pick_html = ""
    if pick:
        pick_html = f"""<div class="pick"><span class="eyebrow">Top pick today</span>
<a class="pimg" href="{e(pick['url'])}" target="_blank" rel="sponsored nofollow noopener"><img src="{e(pick['image'])}" alt="" loading="lazy"></a>
<div class="pinfo"><b>{e(short(pick['title'], 56))}</b><span>★ {pick['rating']:.0f}% · {pick['orders']:,} orders</span>
<div class="buy"><span class="price">{money(pick['price'])}</span><a class="btn" href="{e(pick['url'])}" target="_blank" rel="sponsored nofollow noopener">View deal</a></div></div></div>"""
    return f"""<div class="kitrow"><div class="kitinfo"><h3>{e(k['item'])}</h3><p>{e(k['why'])}</p><div class="kitlinks">{links}</div></div>{pick_html}</div>"""


def build_guides(by_cat, stats):
    for g in guides.GUIDES:
        budget = "budget" in g["slug"]
        facts = "".join(f'<div><span>{e(a)}</span><b>{e(v)}</b></div>' for a, v in g["facts"])
        sections = "".join(f'<h2>{e(h)}</h2>' + "".join(f"<p>{e(p)}</p>" for p in ps) for h, ps in g["sections"])
        kit = "".join(kit_row(k, by_cat, stats, budget) for k in g["kit"])
        others = [o for o in guides.GUIDES if o["slug"] != g["slug"]][:3]
        body = (pagehead(g["eyebrow"], g["title"], g["intro"], bg=g["bg"])
                + f'<article class="guide"><div class="facts">{facts}</div>{sections}'
                + f'<h2 id="kit">The kit list</h2><p>Picks update every day based on ratings, sales and price.</p>{kit}'
                + '<p class="small">Always check a species-specific care sheet, and your vet if you have concerns. '
                  'Prices and availability can change.</p></article>'
                + sechead("Keep exploring", "More field guides") + guide_cards(others))
        write(f'{g["slug"]}.html', layout(f'{g["title"]} | {config.SITE_NAME}', body, g["teaser"]))
    write("guides.html", layout(f"Buying guides | {config.SITE_NAME}",
          pagehead("Field guides", "Buying guides", "Straightforward setup guides and kit lists for fishkeepers "
                   "and reptile keepers, with picks that update every day.") + guide_cards(guides.GUIDES)))


def build(conn):
    os.makedirs(SITE_DIR, exist_ok=True)
    cutoff = (dt.date.today() - dt.timedelta(days=3)).isoformat()  # drop listings that vanished
    products = [dict(r) for r in conn.execute(
        "SELECT * FROM products WHERE last_seen >= ? ORDER BY orders DESC", (cutoff,))]
    stats = trends.product_stats(conn)
    by_cat = {}
    for p in products:
        by_cat.setdefault(p["category"], []).append(p)

    # Category pages
    for slug, c in config.CATEGORIES.items():
        items = by_cat.get(slug, [])[: config.MAX_PER_CATEGORY]
        zone = "Deep water · Aquarium" if c["group"] == "Aquarium" else "Jungle · Reptile"
        body = (pagehead(zone, c["name"], f'The best-selling, best-rated {c["name"].lower()} on AliExpress right now, checked daily.',
                         bg="underwater" if c["group"] == "Aquarium" else "jungle",
                         extra=amazon_link(c["keywords"][0], f'Also browse {c["name"].lower()} on Amazon', "btn ghost"))
                + (grid(items, stats, sortable=True) if items else ('<div class="soon"><b>Our scouts are out gathering the best picks.</b><p>Products for this category are on their way. '
                    'In the meantime, take a look at our <a href="guides.html">buying guides</a>.</p></div>')))
        write(f"{slug}.html", layout(f'{c["name"]} | {config.SITE_NAME}', body,
                                     f'Top-rated {c["group"].lower()} {c["name"].lower()} sorted by popularity and price.'))

    # Home page
    hot = trends.trending(products, stats)
    drops = [p for p in products if stats.get(p["id"], {}).get("price_drop")][:8]
    tiles = "".join(
        f'<a class="tile {c["group"].lower()}" href="{slug}.html"><span class="pic"><img src="img/bg/cat-{slug}.webp" alt="" loading="lazy"></span><b>{e(c["name"])}</b>'
        f'<span>{(str(len(by_cat[slug])) + " picks") if by_cat.get(slug) else "Coming soon"} · {"Deep water" if c["group"] == "Aquarium" else "Jungle"}</span></a>'
        for slug, c in config.CATEGORIES.items())
    body = f"""<section class="hero photo"><div class="wrap copy"><div class="herotext">
<span class="eyebrow">Aquarium &amp; reptile gear · checked daily</span>
<h1>Welcome to the lagoon, keeper</h1>
<p>Every day we wade through thousands of aquarium and reptile products and only bring back the ones with great ratings, real sales and fair prices.</p>
<a class="btn big" href="#territory">Start exploring</a></div>{guide_slider()}</div>{WAVE}</section>
<section class="band jungle"><div class="inner">{sechead("Pick your habitat", "Where are we heading?", "territory")}<div class="tiles">{tiles}</div></div></section>
{sechead("Fresh sightings", "Trending this week", "trending", "Products whose orders are growing fastest right now.")}
{grid(hot, stats) if hot else '<div class="soon"><b>Fresh sightings coming soon.</b><p>Once our daily scan starts, the products growing fastest will appear here.</p></div>'}
{('<section class="band underwater"><div class="inner">' + sechead("Rare finds", "Price drops", "price-drops", "Cheaper today than any price we have recorded.") + grid(drops, stats) + '</div></section>') if drops else ''}
{sechead("Field guides", "Set it up right", "guides", "Simple setup guides with kit lists that update every day.")}
{guide_cards(guides.GUIDES[:4])}
<p class="center"><a class="btn ghost" href="guides.html">All buying guides</a></p>
<section class="cta band river"><div class="inner"><span class="eyebrow">On a budget?</span><h2>Great gear under {money(config.BUDGET_LIMIT, True)}</h2>
<p>Popular, well-rated picks that keep your tank happy and your wallet happier.</p>
<a class="btn big" href="budget.html">See budget picks</a></div></section>"""
    write("index.html", layout(f"{config.SITE_NAME} | Trending Aquarium & Reptile Gear", body, page_class="home"))

    # Budget page
    cheap = sorted([p for p in products if p["price"] <= config.BUDGET_LIMIT],
                   key=lambda p: -p["orders"])[:48]
    write("budget.html", layout(
        f"Best aquarium & reptile gear under {money(config.BUDGET_LIMIT, True)} | {config.SITE_NAME}",
        pagehead("Budget expedition", f"Best under {money(config.BUDGET_LIMIT, True)}", "Popular, well-rated gear that won't break the bank.")
        + (grid(cheap, stats, sortable=True) if cheap else '<div class="soon"><b>Budget picks are on their way.</b>'
           '<p>Once our daily scan starts, the best-rated gear under ' + money(config.BUDGET_LIMIT, True) + ' will appear here.</p></div>')))

    build_info_pages()
    build_guides(by_cat, stats)

    # Static assets
    for name in ("style.css", "site.js"):
        with open(os.path.join(ASSETS, name), encoding="utf-8") as src:
            write(name, src.read())
    os.makedirs(os.path.join(SITE_DIR, "img", "bg"), exist_ok=True)
    with open(os.path.join(SITE_DIR, "img", "bg", "favicon.svg"), "w") as fav:
        fav.write(LOGO.replace('<svg ', '<svg xmlns="http://www.w3.org/2000/svg" ', 1).replace('fill="none" stroke="#ffb500"', 'fill="#0c1813" stroke="#ffb500"'))
    for name in os.listdir(os.path.join(ASSETS, "img")):
        shutil.copy(os.path.join(ASSETS, "img", name), os.path.join(SITE_DIR, "img", "bg", name))

    # SEO files
    pages = (["index.html", "budget.html", "guides.html"] + [u for u, _ in INFO_PAGES]
             + [g["slug"] + ".html" for g in guides.GUIDES]
             + [f"{s}.html" for s in config.CATEGORIES])
    if config.SITE_URL:
        from urllib.parse import urlparse
        host = urlparse(config.SITE_URL).netloc
        if host and not host.endswith("github.io"):
            write("CNAME", host + "\n")
    write("robots.txt", "User-agent: *\nAllow: /\n"
          + (f"Sitemap: {config.SITE_URL.rstrip('/')}/sitemap.xml\n" if config.SITE_URL else ""))
    if config.SITE_URL:
        urls = "".join(f"<url><loc>{config.SITE_URL.rstrip('/')}/{p}</loc></url>" for p in pages)
        write("sitemap.xml", f'<?xml version="1.0" encoding="UTF-8"?><urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">{urls}</urlset>')
    print(f"Built {len(pages)} pages with {len(products)} products, {len(hot)} trending, {len(drops)} price drops")
