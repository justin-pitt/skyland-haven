"""Forward-looking pace + price-clamp analysis from the PriceLabs daily pull.

Reads:
  data/raw/pricelabs/forward_prices_<DATE>.csv  (PriceLabs MCP get_listing_prices,
                                                 transcribed PII-free; see that dir's README)

Answers three questions the monthly scorecard needs and the revenue CSV cannot:
  1. Is the price ceiling (max) or floor (min) binding, and what does it cost?
     `uncustomized_price` is what PriceLabs' model wants; `price` is what it may
     actually push after the listing's min/max clamp. Divergence = a binding limit.
  2. How does on-the-books pace compare with the same time last year (STLY)?
  3. What min-stay is being enforced, by month?

Writes data/pnl/forward-pace.csv and prints the summary.

Usage: python analysis/build_forward_pace.py [path-to-csv]
"""

from __future__ import annotations

import csv
import sys
from collections import defaultdict
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent
DEFAULT_SRC = REPO / "data" / "raw" / "pricelabs" / "forward_prices_2026-08-19.csv"

# Listing-level limits in PriceLabs at pull time (get_listing_data: min/base/max).
# Update alongside a new pull; the clamp math is meaningless if these drift.
MIN_PRICE = 332
MAX_PRICE = 750


def num(x: str) -> float:
    try:
        return float(x)
    except (TypeError, ValueError):
        return -1.0


def booked(status: str) -> bool:
    return status.strip().startswith("Booked")


def main() -> None:
    src = Path(sys.argv[1]) if len(sys.argv) > 1 else DEFAULT_SRC
    rows = list(csv.DictReader(src.open()))
    print(f"source: {src.relative_to(REPO)}  ({len(rows)} nights, "
          f"{rows[0]['date']} .. {rows[-1]['date']})")
    print(f"listing limits at pull: min ${MIN_PRICE} / max ${MAX_PRICE}\n")

    months = defaultdict(lambda: defaultdict(float))
    ceil_loss = 0.0
    floor_gap = 0.0

    for r in rows:
        m = r["date"][:7]
        want = num(r["uncustomized_price"])
        got = num(r["price"])
        is_booked = booked(r["booking_status"])
        was_booked_stly = booked(r["booking_status_STLY"])

        s = months[m]
        s["nights"] += 1
        s["booked"] += 1 if is_booked else 0
        s["booked_stly"] += 1 if was_booked_stly else 0
        s["min_stay_sum"] += num(r["min_stay"])

        # Ceiling binding: model wants more than the cap allows.
        if want > MAX_PRICE:
            s["ceil_days"] += 1
            gap = want - MAX_PRICE
            s["ceil_gap"] += gap
            # Only unbooked nights are still recoverable by raising the cap;
            # booked nights already sold at the capped rate (revenue forgone).
            ceil_loss += gap
            if not is_booked:
                s["ceil_gap_open"] += gap

        # Floor binding: model wants to discount below the min price.
        if want < MIN_PRICE and want > 0:
            s["floor_days"] += 1
            s["floor_gap"] += MIN_PRICE - want
            floor_gap += MIN_PRICE - want

    hdr = (f"{'month':<9}{'nights':>7}{'booked':>8}{'occ%':>7}{'STLY':>6}{'STLY%':>7}"
           f"{'ceil_d':>8}{'ceil_$':>9}{'floor_d':>9}{'avg_minstay':>13}")
    print(hdr)
    print("-" * len(hdr))
    out_rows = []
    for m in sorted(months):
        s = months[m]
        n = s["nights"]
        occ = 100 * s["booked"] / n
        occ_stly = 100 * s["booked_stly"] / n
        avg_ms = s["min_stay_sum"] / n
        print(f"{m:<9}{int(n):>7}{int(s['booked']):>8}{occ:>6.0f}%"
              f"{int(s['booked_stly']):>6}{occ_stly:>6.0f}%"
              f"{int(s['ceil_days']):>8}{s['ceil_gap']:>9,.0f}"
              f"{int(s['floor_days']):>9}{avg_ms:>13.1f}")
        out_rows.append({
            "month": m,
            "nights_in_window": int(n),
            "booked_now": int(s["booked"]),
            "occupancy_pct_onbooks": round(occ, 1),
            "booked_same_time_last_year": int(s["booked_stly"]),
            "occupancy_pct_stly": round(occ_stly, 1),
            "ceiling_bound_nights": int(s["ceil_days"]),
            "ceiling_gap_total": round(s["ceil_gap"], 2),
            "ceiling_gap_open_nights": round(s["ceil_gap_open"], 2),
            "floor_bound_nights": int(s["floor_days"]),
            "floor_gap_total": round(s["floor_gap"], 2),
            "avg_min_stay": round(avg_ms, 2),
        })

    tot_n = sum(m["nights"] for m in months.values())
    tot_b = sum(m["booked"] for m in months.values())
    tot_s = sum(m["booked_stly"] for m in months.values())
    tot_open = sum(m["ceil_gap_open"] for m in months.values())
    print("-" * len(hdr))
    print(f"{'TOTAL':<9}{int(tot_n):>7}{int(tot_b):>8}{100*tot_b/tot_n:>6.0f}%"
          f"{int(tot_s):>6}{100*tot_s/tot_n:>6.0f}%")

    print(f"\nceiling (${MAX_PRICE}) binds on {sum(int(m['ceil_days']) for m in months.values())} "
          f"of {int(tot_n)} nights; total gap to model price ${ceil_loss:,.0f}")
    print(f"  of which still OPEN (recoverable by raising the cap): ${tot_open:,.0f}")
    print(f"floor (${MIN_PRICE}) binds on {sum(int(m['floor_days']) for m in months.values())} "
          f"nights; model wants ${floor_gap:,.0f} lower in aggregate")

    out = REPO / "data" / "pnl" / "forward-pace.csv"
    with out.open("w", newline="") as fh:
        w = csv.DictWriter(fh, fieldnames=list(out_rows[0].keys()))
        w.writeheader()
        w.writerows(out_rows)
    print(f"\nwrote {out.relative_to(REPO)}")


if __name__ == "__main__":
    main()
