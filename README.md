# LagoonGecko: automated aquarium & reptile affiliate site

Every day this project:

1. **Collects** best-selling aquarium and reptile products from AliExpress (about 50 search keywords across 10 categories).
2. **Filters** them: only 92%+ positive feedback, 50+ recent orders, and an affiliate link.
3. **Tracks** orders and price for each product every day, then flags **Trending** products (orders growing fastest) and **Price drops** (cheapest price ever recorded).
4. **Writes** a short summary for each product (AI if you add a Claude API key, otherwise a template).
5. **Builds and publishes** the website: home page, 10 category pages with sorting, a "Best under $20" page, and an affiliate disclosure page.

Every "View deal" button is your affiliate link, so you earn commission on purchases.

---

## Preview it now (no keys needed)

```bash
pip install -r requirements.txt
python run.py --demo
```
Then open `site/index.html` in your browser. Demo mode uses **sample** products so you can see how the site works.

---

## Go live on lagoongecko.com: step by step

You can go live **before** your AliExpress keys are approved. Without keys the site runs in
**launch mode**: guides, categories and info pages go live, with "coming soon" where products will appear
(it never shows sample products). Products switch on automatically on the first daily run after you add the keys.

### 1. Put the project on GitHub (free, ~5 min)
1. Create a free account at **github.com** and click **New repository**. Name it `lagoongecko`.
   Make it **Public** (free GitHub Pages hosting needs a public repo on the free plan).
2. On the new repo page click **uploading an existing file** and drag in **everything inside this folder**,
   including the hidden `.github` folder (on Mac press Cmd+Shift+. to show hidden files). Click **Commit changes**.

### 2. Turn on hosting with your domain
1. In the repo: **Settings → Pages → Source: GitHub Actions**.
2. Same page, **Custom domain**: type `lagoongecko.com` and click **Save**.
3. **Actions** tab → **Daily update** → **Run workflow**. Wait ~2 minutes for the green tick.

### 3. Point lagoongecko.com at GitHub (DNS)
In the place you bought the domain, open its **DNS settings** and set these records
(delete any existing A record for `@` and CNAME for `www` first):

| Type | Name / Host | Value |
|---|---|---|
| A | @ | 185.199.108.153 |
| A | @ | 185.199.109.153 |
| A | @ | 185.199.110.153 |
| A | @ | 185.199.111.153 |
| CNAME | www | `YOUR-GITHUB-USERNAME.github.io` |

**Bought it through Shopify?** Shopify admin → **Settings → Domains** → click `lagoongecko.com` →
**Domain settings → Edit DNS settings**, then replace Shopify's A record and `www` CNAME with the records above.
(It is currently attached to your Shopify store, so this points it at the new site instead.)

DNS changes take from a few minutes up to 24 hours. Then go back to **Settings → Pages**, wait for the
domain check to pass, and tick **Enforce HTTPS**.

### 4. Add your keys when they're ready
**Settings → Secrets and variables → Actions**.

**Secrets** tab:
| Name | Value |
|---|---|
| `ALIEXPRESS_APP_KEY` | your App Key |
| `ALIEXPRESS_APP_SECRET` | your App Secret |
| `ALIEXPRESS_TRACKING_ID` | your Tracking ID |
| `ANTHROPIC_API_KEY` | optional, for AI product summaries |

To get the AliExpress keys: sign up at **portals.aliexpress.com**, create a Tracking ID, then register at
**openservice.aliexpress.com** and create an Affiliate API app.

**Variables** tab (same page), optional:
| Name | Value |
|---|---|
| `CONTACT_EMAIL` | the email shown on the Contact page |
| `CONTACT_FORM_URL` | optional Formspree form link |
| `AMAZON_TAG` | your Amazon Associates tracking ID, e.g. `lagoongecko-20` (see below) |

## Adding Amazon (second store)

Every product card gets a "Compare on Amazon" link, each category page gets an "Also browse on Amazon" button,
and every guide kit item gets a "Find it on Amazon" link. They only appear once `AMAZON_TAG` is set.

**Timing matters:** Amazon gives new affiliates 180 days from applying to make 3 qualifying sales, or the
account is closed. So apply at **affiliate-program.amazon.com** once the site is getting regular visitors,
then add your tracking ID as the `AMAZON_TAG` variable. The site adds Amazon's required disclosure automatically.

## Buying guides

Guides live in **`guides.py`**: setup advice plus a kit list. Each kit item shows today's best matching
product from your data (so picks stay fresh), a link to the category, and an Amazon link. To add a guide,
copy one block, change the text, and it appears on the Guides page, the home page and the sitemap.

## Customising

Everything is in **`config.py`**:
- `CATEGORIES`: add, remove or rename categories and their search keywords.
- `MIN_POSITIVE_FEEDBACK`, `MIN_ORDERS`: how strict the quality filter is.
- `SHIP_TO`: the country your visitors are in (affects prices and availability).
- `BUDGET_LIMIT`: the "Best under $X" page.
- `CONTACT_EMAIL`: the email shown on the Contact us page. **Change this before going live.**
- `CONTACT_FORM_URL`: optional. Sign up free at formspree.io, create a form and paste its URL here to add a message form to the Contact page.

Colours and layout are in `assets/style.css`, and the menu and sorting script is `assets/site.js`.

## Good to know
- **Trending needs history.** "Trending" and "Price drops" start showing after the site has run for a few days.
- **Order counts** come from AliExpress's recent-sales figure, so "▲ 40% this week" means that figure grew 40% over 7 days.
- **Add your own content.** Google ranks sites that add real value higher than pure product lists. Add a few guides (e.g. "Beginner betta tank setup") as extra pages over time.
- **Check the first real run.** If the first live run shows an API error, check that your API app is approved for the `aliexpress.affiliate.product.query` method.

## Files
| File | What it does |
|---|---|
| `run.py` | Runs the whole daily pipeline |
| `config.py` | All settings |
| `aliexpress.py` | Talks to the AliExpress affiliate API |
| `collect.py` | Searches keywords, filters and stores products |
| `trends.py` | Works out trending products and price drops |
| `describe.py` | Writes product summaries |
| `build_site.py` | Builds the website |
| `demo.py` | Sample data for previewing |
| `.github/workflows/daily.yml` | The daily schedule and publishing |
