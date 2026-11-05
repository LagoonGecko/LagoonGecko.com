"""Trend and price-drop detection from the daily snapshots."""
import datetime as dt

import config


def product_stats(conn):
    """Return {product_id: stats} with order growth over the trend window and
    whether today's price is the lowest we've recorded."""
    today = dt.date.today()
    since = (today - dt.timedelta(days=config.TREND_WINDOW_DAYS)).isoformat()
    stats = {}
    rows = conn.execute("SELECT product_id, day, orders, price FROM snapshots ORDER BY day").fetchall()
    history = {}
    for r in rows:
        history.setdefault(r["product_id"], []).append(r)
    for pid, snaps in history.items():
        latest = snaps[-1]
        # Baseline: the last snapshot on or before the start of the window
        older = [s for s in snaps if s["day"] <= since] or snaps[:1]
        base = older[-1]
        growth = latest["orders"] - base["orders"]
        pct = growth / base["orders"] * 100 if base["orders"] else 0
        prev_prices = [s["price"] for s in snaps[:-1]]
        lowest_before = min(prev_prices) if prev_prices else None
        price_drop = lowest_before is not None and latest["price"] < lowest_before * 0.97
        stats[pid] = {
            "growth": growth, "growth_pct": pct, "days_tracked": len(snaps),
            "price_drop": price_drop,
            "was": lowest_before if price_drop else None,
        }
    return stats


def trending(products, stats, limit=None):
    limit = limit or config.TRENDING_COUNT
    scored = [p for p in products
              if stats.get(p["id"], {}).get("days_tracked", 0) >= 2
              and stats[p["id"]]["growth"] > 0]
    # Rank by % growth, but weight by absolute growth so tiny sellers don't dominate
    scored.sort(key=lambda p: stats[p["id"]]["growth_pct"] * min(stats[p["id"]]["growth"], 500),
                reverse=True)
    return scored[:limit]
