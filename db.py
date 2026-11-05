"""Small SQLite store: one row per product, plus a daily snapshot of
orders and price so we can spot trends and price drops over time."""
import os
import sqlite3

DB_PATH = os.path.join(os.path.dirname(__file__), "data", "tankfinds.db")

SCHEMA = """
CREATE TABLE IF NOT EXISTS products (
    id TEXT PRIMARY KEY,
    title TEXT, image TEXT, url TEXT, category TEXT,
    price REAL, original_price REAL, rating REAL, orders INTEGER,
    commission REAL, description TEXT,
    first_seen TEXT, last_seen TEXT
);
CREATE TABLE IF NOT EXISTS snapshots (
    product_id TEXT, day TEXT, orders INTEGER, price REAL,
    PRIMARY KEY (product_id, day)
);
"""


def connect(path=DB_PATH):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    conn = sqlite3.connect(path)
    conn.row_factory = sqlite3.Row
    conn.executescript(SCHEMA)
    return conn


def upsert_product(conn, p, day):
    """Insert or refresh a product. A product keeps the first category it was
    found in, so it never appears twice on the site."""
    existing = conn.execute("SELECT category, description, first_seen FROM products WHERE id=?",
                            (p["id"],)).fetchone()
    if existing:
        conn.execute(
            """UPDATE products SET title=?, image=?, url=?, price=?, original_price=?,
               rating=?, orders=?, commission=?, last_seen=? WHERE id=?""",
            (p["title"], p["image"], p["url"], p["price"], p["original_price"],
             p["rating"], p["orders"], p["commission"], day, p["id"]))
    else:
        conn.execute(
            """INSERT INTO products (id, title, image, url, category, price, original_price,
               rating, orders, commission, description, first_seen, last_seen)
               VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?)""",
            (p["id"], p["title"], p["image"], p["url"], p["category"], p["price"],
             p["original_price"], p["rating"], p["orders"], p["commission"],
             p.get("description"), day, day))
    conn.execute("INSERT OR REPLACE INTO snapshots (product_id, day, orders, price) VALUES (?,?,?,?)",
                 (p["id"], day, p["orders"], p["price"]))
