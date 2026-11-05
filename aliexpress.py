"""AliExpress Affiliate API client (aliexpress.affiliate.product.query).

Every product link it returns already contains your tracking ID, so any
purchase made through it is credited to you."""
import hashlib
import hmac
import time

import requests

import config

API_URL = "https://api-sg.aliexpress.com/sync"


def _sign(params, secret):
    # Sort parameters, join as key+value, HMAC-SHA256 with the app secret.
    base = "".join(f"{k}{params[k]}" for k in sorted(params))
    return hmac.new(secret.encode(), base.encode(), hashlib.sha256).hexdigest().upper()


def _call(method, **biz):
    params = {
        "app_key": config.APP_KEY,
        "method": method,
        "sign_method": "sha256",
        "timestamp": str(int(time.time() * 1000)),
        "format": "json",
        "v": "2.0",
        **{k: str(v) for k, v in biz.items() if v is not None},
    }
    params["sign"] = _sign(params, config.APP_SECRET)
    r = requests.post(API_URL, data=params, timeout=30)
    r.raise_for_status()
    data = r.json()
    if "error_response" in data:
        raise RuntimeError(f"AliExpress API error: {data['error_response']}")
    return data


def _num(value, default=0.0):
    try:
        return float(str(value).replace("%", "").replace(",", ""))
    except (TypeError, ValueError):
        return default


def search(keyword, page=1, page_size=50):
    """Return a list of clean product dicts for one keyword, best sellers first."""
    data = _call(
        "aliexpress.affiliate.product.query",
        keywords=keyword, page_no=page, page_size=page_size,
        sort="LAST_VOLUME_DESC", target_currency=config.CURRENCY,
        target_language=config.LANGUAGE, ship_to_country=config.SHIP_TO,
        tracking_id=config.TRACKING_ID,
    )
    result = (data.get("aliexpress_affiliate_product_query_response", {})
                  .get("resp_result", {}).get("result", {}))
    raw = (result.get("products") or {}).get("product") or []
    products = []
    for item in raw:
        url = item.get("promotion_link")
        if not url:
            continue  # not in the affiliate program, no commission possible
        price = _num(item.get("target_sale_price") or item.get("sale_price"))
        products.append({
            "id": str(item.get("product_id")),
            "title": item.get("product_title", "").strip(),
            "image": item.get("product_main_image_url", ""),
            "url": url,
            "price": price,
            "original_price": _num(item.get("target_original_price"), price),
            "rating": _num(item.get("evaluate_rate")),
            "orders": int(_num(item.get("lastest_volume"))),
            "commission": _num(item.get("commission_rate")),
        })
    return products
