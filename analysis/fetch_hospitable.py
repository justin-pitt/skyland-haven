"""Fetch raw Hospitable data for the Skyland property (trailing 12 months).

Reads HOSPITABLE_API_TOKEN / HOSPITABLE_API_BASE from the repo-root .env
(never committed) and writes raw JSON responses to data/raw/hospitable/.
No derivation happens here — see build_pnl.py for the monthly CSV logic.

Window: the trailing 12 full months set by WINDOW_START/WINDOW_END below
(roll both forward by one each month). Reservations are fetched with a
check-in range widened on both sides so stays that straddle the window
edges are captured; build_pnl.py allocates nights to calendar months.

Usage: python analysis/fetch_hospitable.py
"""

from __future__ import annotations

import json
import sys
import time
import urllib.parse
import urllib.request
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent
RAW_DIR = REPO / "data" / "raw" / "hospitable"

PROPERTY_UUID = "8f91a20f-5c4d-4b42-aa35-f0e7812d64cf"  # "Skyland"

# Analysis window (full months), widened for reservation fetch.
WINDOW_START = "2025-08-01"
WINDOW_END = "2026-07-31"
# Reservations are pulled well beyond the analysis window on BOTH sides: back far
# enough that stays straddling the window start are captured, and forward far enough
# to capture FUTURE on-books (needed for booking-pace / pickup analysis). build_pnl.py
# filters to MONTHS, so a wide pull costs nothing there.
RES_FETCH_START = "2025-06-01"
RES_FETCH_END = "2027-12-31"


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
    url = f"{BASE}{path}{qs}"
    req = urllib.request.Request(url, headers={
        "Authorization": f"Bearer {TOKEN}",
        "Accept": "application/json",
    })
    with urllib.request.urlopen(req) as resp:
        return json.load(resp)


def get_paginated(path: str, params: dict) -> list[dict]:
    """Follow `meta.current_page`/`meta.last_page` pagination, return all rows."""
    rows: list[dict] = []
    page = 1
    while True:
        payload = get(path, {**params, "page": page, "per_page": 100})
        rows.extend(payload.get("data", []))
        meta = payload.get("meta", {})
        last = meta.get("last_page") or meta.get("lastPage") or 1
        print(f"  {path} page {page}/{last} -> {len(payload.get('data', []))} rows")
        if page >= last:
            return rows
        page += 1
        time.sleep(0.5)  # stay well under rate limits


def save(name: str, obj) -> None:
    RAW_DIR.mkdir(parents=True, exist_ok=True)
    out = RAW_DIR / name
    out.write_text(json.dumps(obj, indent=2))
    print(f"  wrote {out.relative_to(REPO)}")


def month_edges() -> list[tuple[str, str]]:
    """First/last day of each month in the analysis window."""
    edges = []
    y, m = int(WINDOW_START[:4]), int(WINDOW_START[5:7])
    while f"{y}-{m:02d}" <= WINDOW_END[:7]:
        import calendar
        last = calendar.monthrange(y, m)[1]
        edges.append((f"{y}-{m:02d}-01", f"{y}-{m:02d}-{last:02d}"))
        y, m = (y + 1, 1) if m == 12 else (y, m + 1)
    return edges


def main() -> None:
    print("reservations (accepted + cancelled, with financials)...")
    reservations = get_paginated("/reservations", {
        "properties[]": PROPERTY_UUID,
        "start_date": RES_FETCH_START,
        "end_date": RES_FETCH_END,
        "date_query": "checkin",
        "include": "financials",
    })
    save("reservations.json", reservations)

    print("payouts...")
    payouts = get_paginated("/payouts", {})
    save("payouts.json", payouts)

    print("transactions...")
    transactions = get_paginated("/transactions", {})
    save("transactions.json", transactions)

    print("calendar, month by month...")
    cal_months = {}
    for start, end in month_edges():
        try:
            payload = get(f"/properties/{PROPERTY_UUID}/calendar",
                          {"start_date": start, "end_date": end})
            cal_months[start[:7]] = payload.get("data", payload)
            print(f"  {start[:7]} ok")
        except Exception as e:  # historical months may not be served
            cal_months[start[:7]] = {"error": str(e)}
            print(f"  {start[:7]} FAILED: {e}")
        time.sleep(0.5)
    save("calendar.json", cal_months)

    print("done")


if __name__ == "__main__":
    sys.exit(main())
