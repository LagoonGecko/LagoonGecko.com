"""Daily product collection: search every keyword, keep only well-rated
products with real sales, and store today's snapshot."""
import datetime as dt

import aliexpress
import config
import db


def passes_filters(p):
    return (p["rating"] >= config.MIN_POSITIVE_FEEDBACK
            and p["orders"] >= config.MIN_ORDERS
            and p["price"] > 0 and p["title"])


def collect(conn, day=None):
    day = day or dt.date.today().isoformat()
    kept = 0
    for slug, cat in config.CATEGORIES.items():
        for kw in cat["keywords"]:
            for page in range(1, config.PAGES_PER_KEYWORD + 1):
                try:
                    results = aliexpress.search(kw, page=page)
                except Exception as e:  # one bad keyword shouldn't stop the run
                    print(f"  ! {kw} p{page}: {e}")
                    break
                for p in results:
                    if passes_filters(p):
                        p["category"] = slug
                        db.upsert_product(conn, p, day)
                        kept += 1
                if len(results) < 50:
                    break
        conn.commit()
        print(f"  {cat['name']}: done")
    print(f"Collected {kept} qualifying product listings")
