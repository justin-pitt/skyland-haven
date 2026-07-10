"""Fetch Skyland listing *content* for the conversion audit (docs/conversion-audit.md).

Distinct from fetch_hospitable.py (which pulls reservations/payouts/transactions/
calendar for the P&L). This pulls the marketing surface a searcher sees:

  - property.json  : title/public_name, summary, description, amenities, capacity,
                     room_details, house_rules, channel listings (+ details include)
  - images.json    : the ordered photo gallery (order + captions)
  - reviews.json   : reviews stored in Hospitable (NOTE: post-connection only —
                     the *live* Airbnb public count is far higher; see below)

Reads HOSPITABLE_API_TOKEN / HOSPITABLE_API_BASE from the repo-root .env
(never committed). Writes raw JSON to data/raw/hospitable/.

Public-review-count caveat: Hospitable only stores reviews collected after the
account connected the channel. The authoritative *public* review count/rating is
on the live Airbnb page (rooms/<platform_id>). As of 2026-07-10 the live listing
showed 101 reviews / 4.97 stars / Superhost / Instant Book — captured in the audit,
not fetchable here because Airbnb blocks automated fetches without a browser UA.

Usage: python analysis/fetch_listing_content.py
"""

from __future__ import annotations

import json
import sys
import urllib.parse
import urllib.request
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent
RAW_DIR = REPO / "data" / "raw" / "hospitable"

PROPERTY_UUID = "8f91a20f-5c4d-4b42-aa35-f0e7812d64cf"  # "Skyland"


def load_env() -> dict[str, str]:
    env: dict[str, str] = {}
    for line in (REPO / ".env").read_text().splitlines():
        line = line.strip()
        if line and not line.startswith("#") and "=" in line:
            k, v = line.split("=", 1)
            env[k.strip()] = v.strip()
    return env


ENV = load_env()
BASE = ENV.get("HOSPITABLE_API_BASE", "https://public.api.hospitable.com/v2")
TOKEN = ENV["HOSPITABLE_API_TOKEN"]


def get(path: str, params: dict | None = None) -> dict:
    qs = f"?{urllib.parse.urlencode(params, doseq=True)}" if params else ""
    req = urllib.request.Request(f"{BASE}{path}{qs}", headers={
        "Authorization": f"Bearer {TOKEN}",
        "Accept": "application/json",
    })
    with urllib.request.urlopen(req) as resp:
        return json.load(resp)


def save(name: str, obj) -> None:
    RAW_DIR.mkdir(parents=True, exist_ok=True)
    out = RAW_DIR / name
    out.write_text(json.dumps(obj, indent=2))
    print(f"  wrote {out.relative_to(REPO)}")


def main() -> None:
    print("property (details + listings)...")
    prop = get(f"/properties/{PROPERTY_UUID}",
               {"include": "details,listings"})
    save("property.json", prop.get("data", prop))

    print("images (ordered gallery)...")
    images = get(f"/properties/{PROPERTY_UUID}/images")
    save("images.json", images.get("data", images))

    print("reviews (Hospitable store — post-connection only)...")
    reviews = get(f"/properties/{PROPERTY_UUID}/reviews", {"per_page": 100})
    save("reviews.json", reviews.get("data", reviews))

    print("done")


if __name__ == "__main__":
    sys.exit(main())
