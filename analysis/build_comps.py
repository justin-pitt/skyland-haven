"""Derive comp-set / market CSVs from raw PriceLabs JSON.

Inputs (data/raw/pricelabs/, both pulled 2026-07-08 via the PriceLabs MCP
server — free tier has no REST API, so raw responses are checked in as the
citable source; they contain market aggregates only, no PII):
  neighbourhood_detail.json  — get_neighbourhood_data(mode=detail,
                               include_prices=true, include_occupancy=true)
  listing_prices_60d.json    — get_listing_prices, 2026-07-09 .. 2026-09-06

Outputs (data/comps/):
  market-daily-60d.csv     — daily: our price vs market 25/50/75/90th
                             percentile prices + market occupancy, next 60 days
  market-history-24mo.csv  — trailing comp-set ADR / occupancy / booking
                             window by month (PriceLabs market history)
  market-summary.md        — bedroom-category price percentiles, monthly
                             market occupancy, insights, sources

Comp set = PriceLabs neighborhood market for this listing: 4-6 BR listings
(335 total; 81 in the 5 BR band) near Woodfin/North Asheville, source airbnb.

Usage: python analysis/build_comps.py
"""

from __future__ import annotations

import csv
import json
from datetime import date, timedelta
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent
RAW = REPO / "data" / "raw" / "pricelabs"
OUT = REPO / "data" / "comps"

WINDOW_FROM = date(2026, 7, 9)
WINDOW_TO = date(2026, 9, 6)  # 60 days


def main() -> None:
    detail = json.loads((RAW / "neighbourhood_detail.json").read_text())["data"]["data"]
    listing = json.loads((RAW / "listing_prices_60d.json").read_text())["data"]

    OUT.mkdir(parents=True, exist_ok=True)

    # --- daily 60-day market vs listing ---
    fp = detail["prices"]["future_prices"]
    occ_daily = detail["occupancy"]["daily"]
    dates = fp["stay_dates"]
    occ_dates = occ_daily["period"]
    occ_by_date = dict(zip(occ_dates, occ_daily["market_occupancy"]))
    own_price = {r["date"]: r for r in listing}

    idx = {dt: i for i, dt in enumerate(dates)}
    rows = []
    d = WINDOW_FROM
    while d <= WINDOW_TO:
        ds = d.isoformat()
        i = idx.get(ds)
        lp = own_price.get(ds, {})
        rows.append({
            "date": ds,
            "own_price": lp.get("price", ""),
            "own_booking_status": lp.get("booking_status", "") or "open",
            "own_booked_adr": lp.get("ADR") if lp.get("ADR", -1) != -1 else "",
            "min_stay": lp.get("min_stay", ""),
            "demand": lp.get("demand_desc", ""),
            "market_25pct": fp["market_25_percentile_prices"][i] if i is not None else "",
            "market_median": fp["market_price"][i] if i is not None else "",
            "market_75pct": fp["market_75_percentile_prices"][i] if i is not None else "",
            "market_90pct": fp["market_90_percentile_prices"][i] if i is not None else "",
            "market_occupancy_pct": occ_by_date.get(ds, ""),
        })
        d += timedelta(days=1)

    with (OUT / "market-daily-60d.csv").open("w", newline="") as fh:
        w = csv.DictWriter(fh, fieldnames=list(rows[0].keys()))
        w.writeheader()
        w.writerows(rows)
    print(f"wrote data/comps/market-daily-60d.csv ({len(rows)} days)")

    # --- trailing market history (comp-set ADR + occupancy by month) ---
    mh = detail["initialize_detail"]["market_history"]
    hist_rows = [
        {
            "period": p,
            "market_adr": a,
            "market_occupancy_pct": o,
            "median_booked_los": los,
            "median_booking_window_days": bw,
        }
        for p, a, o, los, bw in zip(
            mh["periods"], mh["adr"], mh["occupancy"],
            mh["median_booked_los"], mh["median_booking_window"])
    ]
    with (OUT / "market-history-24mo.csv").open("w", newline="") as fh:
        w = csv.DictWriter(fh, fieldnames=list(hist_rows[0].keys()))
        w.writeheader()
        w.writerows(hist_rows)
    print(f"wrote data/comps/market-history-24mo.csv ({len(hist_rows)} periods)")

    # --- monthly market occupancy (forward + trailing from occupancy.monthly) ---
    om = detail["occupancy"]["monthly"]
    def clean(v):
        return "—" if v is None else v

    mo_rows = [
        {"period": p, "market_occupancy_pct": clean(mo), "own_occupancy_pct": clean(oo),
         "market_occupancy_stly_pct": clean(ms)}
        for p, mo, oo, ms in zip(om["period"], om["market_occupancy"],
                                 om["occupancy"], om["market_occupancy_stly"])
    ]

    # --- summary markdown ---
    st = detail["summary_table"]
    init = detail["initialize_detail"]
    lines = [
        "# PriceLabs market summary — Woodfin / North Asheville comp set",
        "",
        f"Source: PriceLabs MCP `get_neighbourhood_data` for listing `Skyland`",
        f"(`{init['listing_id']}`, pms `{init['pms']}`), pulled 2026-07-08.",
        f"Raw JSON: `data/raw/pricelabs/neighbourhood_detail.json`.",
        f"Comp set: 4-6 BR neighborhood listings, source {init['nd_source']};",
        f"listing's own band: {init['bedrooms']}. Fee structure on file: {init['fee_structure']}.",
        "",
        "## Nightly price percentiles by bedroom category (next-365d market rates)",
        "",
        "| category | n | 25th | median | 75th | 90th |",
        "|---|---|---|---|---|---|",
    ]
    for r in st["table_data"]:
        lines.append(f"| {r['category']} | {r['count']} | ${r['25_percentile_price']} "
                     f"| ${r['50_percentile_price']} | ${r['75_percentile_price']} "
                     f"| ${r['90_percentile_price']} |")
    lines += [
        "",
        "## Monthly market occupancy (PriceLabs occupancy.monthly)",
        "",
        "| period | market occ % | own occ % | market occ STLY % |",
        "|---|---|---|---|",
    ]
    for r in mo_rows:
        lines.append(f"| {r['period']} | {r['market_occupancy_pct']} "
                     f"| {r['own_occupancy_pct']} | {r['market_occupancy_stly_pct']} |")
    lines += [
        "",
        "## PriceLabs insights (verbatim, pulled 2026-07-08)",
        "",
        "### Future prices vs market",
        "",
        detail["fp_insights"]["insight"],
        "",
        "### Occupancy / demand",
        "",
        detail["occ_insights"]["insight"],
        "",
        "## Caveats",
        "",
        "- These are market **aggregates** (percentiles over 335 comp listings),",
        "  not the 5 hand-picked comps from checklist item 16 — those still need",
        "  manual selection with listing URLs and rate screenshots.",
        "- PriceLabs market occupancy counts only listed-and-active supply.",
    ]
    (OUT / "market-summary.md").write_text("\n".join(lines))
    print("wrote data/comps/market-summary.md")


if __name__ == "__main__":
    main()
