"""Daily pipeline: collect products -> write summaries -> build site.

    python run.py          # real run (needs AliExpress keys)
    python run.py --demo   # sample data, to preview the site
    (without AliExpress keys, a normal run builds the site in launch mode: no products yet)
"""
import sys

import build_site
import collect
import config
import db
import describe


def main():
    demo = "--demo" in sys.argv
    has_keys = bool(config.APP_KEY and config.APP_SECRET and config.TRACKING_ID)
    if demo:
        import demo as demo_data
        if not config.AMAZON_TAG:
            config.AMAZON_TAG = "yourtag-20"  # placeholder so the preview shows Amazon links
        conn = db.connect(db.DB_PATH.replace("tankfinds.db", "demo.db"))
        demo_data.load_demo(conn, build_site.SITE_DIR)
    elif has_keys:
        conn = db.connect()
        print("Collecting products...")
        collect.collect(conn)
    else:
        # Launch mode: no AliExpress keys yet. Publish guides, categories and info
        # pages with "coming soon" in place of products (never sample products).
        print("No AliExpress keys yet: building in launch mode (no products).")
        conn = db.connect()
    describe.describe_missing(conn)
    build_site.build(conn)


if __name__ == "__main__":
    main()
