"""Short product summaries. Uses Claude if ANTHROPIC_API_KEY is set,
otherwise a simple template. Each product is only described once."""
import config


def _template(p, cat):
    return (f"A popular pick in {cat['name'].lower()}, with {p['orders']:,} recent orders "
            f"and {p['rating']:.0f}% positive feedback.")


def _ai(client, p, cat):
    prompt = (
        "Write a 1-2 sentence, plain-English summary for a product card on an aquarium and "
        "reptile gear website. Say what it's for and who it suits. No hype, no prices, no "
        "claims you can't see in the title.\n"
        f"Category: {cat['name']}\nProduct title: {p['title']}"
    )
    msg = client.messages.create(model=config.AI_MODEL, max_tokens=120,
                                 messages=[{"role": "user", "content": prompt}])
    return msg.content[0].text.strip()


def describe_missing(conn):
    rows = conn.execute("SELECT * FROM products WHERE description IS NULL OR description=''").fetchall()
    client = None
    if config.ANTHROPIC_API_KEY:
        try:
            import anthropic
            client = anthropic.Anthropic(api_key=config.ANTHROPIC_API_KEY)
        except ImportError:
            print("  anthropic package not installed, using templates")
    ai_used = 0
    for r in rows:
        p, cat = dict(r), config.CATEGORIES.get(r["category"], {"name": "aquarium gear"})
        text = None
        if client and ai_used < config.AI_DESCRIPTIONS_PER_RUN:
            try:
                text = _ai(client, p, cat)
                ai_used += 1
            except Exception as e:
                print(f"  AI description failed ({e}), using template")
        if text:  # templates aren't stored, so they refresh with new order counts
            conn.execute("UPDATE products SET description=? WHERE id=?", (text, r["id"]))
    conn.commit()
    if ai_used:
        print(f"Wrote {ai_used} AI summaries")


def text_for(p, cat):
    return p.get("description") or _template(p, cat)
