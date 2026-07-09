"""Derive monthly revenue-side P&L from raw Hospitable JSON.

Reads data/raw/hospitable/*.json (produced by fetch_hospitable.py) and writes:
  data/pnl/pnl-12mo-revenue.csv  — one row per month, 2025-07 .. 2026-06
  (column derivations documented in data/pnl/README.md)

Attribution rules (documented in the README):
- Accommodation revenue: allocated to the month of each stay night using the
  host-side `accommodation_breakdown` per-date amounts; if a reservation lacks
  a breakdown, its host accommodation total is spread evenly across stay nights.
- Cleaning fees, host service fees, adjustments: attributed to check-in month.
- Nights booked: accepted guest-stay reservations, each stay night counted in
  the month it falls in (arrival date .. departure date - 1).
- Nights available: days in month minus owner/manual BLOCKED days from the
  property calendar (RESERVED days are counted as available-and-sold).
- Cancelled reservations contribute no nights; any retained payout on a
  cancelled reservation is reported in `cancellation_income`.

Usage: python analysis/build_pnl.py
"""

from __future__ import annotations

import csv
import json
from collections import defaultdict
from datetime import date, timedelta
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent
RAW = REPO / "data" / "raw" / "hospitable"
OUT = REPO / "data" / "pnl"

MONTHS = [f"2025-{m:02d}" for m in range(7, 13)] + [f"2026-{m:02d}" for m in range(1, 7)]


def d(amount_cents) -> float:
    return round((amount_cents or 0) / 100, 2)


def stay_nights(res) -> list[date]:
    a = date.fromisoformat(res["arrival_date"][:10])
    dep = date.fromisoformat(res["departure_date"][:10])
    return [a + timedelta(days=i) for i in range((dep - a).days)]


def main() -> None:
    reservations = json.loads((RAW / "reservations.json").read_text())
    calendar = json.loads((RAW / "calendar.json").read_text())
    payouts = json.loads((RAW / "payouts.json").read_text())

    acc_rev = defaultdict(float)      # accommodation $ per month (per-night allocation)
    nights = defaultdict(int)         # booked nights per month
    cleaning = defaultdict(float)     # cleaning fees per check-in month
    host_fees = defaultdict(float)    # host service fees (positive $) per check-in month
    fee_base = defaultdict(float)     # accommodation+cleaning per check-in month (fee denominator)
    adjustments = defaultdict(float)  # host adjustments (refunds etc.) per check-in month
    cancel_income = defaultdict(float)

    n_no_breakdown = 0
    for r in reservations:
        status = r["reservation_status"]["current"]["category"]
        fin = r["financials"]["host"]
        cin_month = r["arrival_date"][:7]

        if status == "cancelled":
            if fin["revenue"]["amount"]:
                if cin_month in MONTHS:
                    cancel_income[cin_month] += d(fin["revenue"]["amount"])
            continue
        if status != "accepted" or r.get("stay_type") != "guest_stay":
            continue

        # accommodation: per-night allocation
        breakdown = fin.get("accommodation_breakdown")
        if breakdown:
            for row in breakdown:
                m = row["label"][:7]
                if m in MONTHS:
                    acc_rev[m] += d(row["amount"])
        else:
            n_no_breakdown += 1
            nts = stay_nights(r)
            if nts:
                per = (fin["accommodation"]["amount"] or 0) / len(nts)
                for n in nts:
                    m = n.strftime("%Y-%m")
                    if m in MONTHS:
                        acc_rev[m] += d(per)

        for n in stay_nights(r):
            m = n.strftime("%Y-%m")
            if m in MONTHS:
                nights[m] += 1

        if cin_month in MONTHS:
            for fee in fin.get("guest_fees", []):
                if "cleaning" in fee["label"].lower():
                    cleaning[cin_month] += d(fee["amount"])
            for fee in fin.get("host_fees", []):
                host_fees[cin_month] += abs(d(fee["amount"]))
            for adj in fin.get("adjustments", []):
                adjustments[cin_month] += d(adj["amount"])
            fee_base[cin_month] += d(fin["accommodation"]["amount"]) + sum(
                d(f["amount"]) for f in fin.get("guest_fees", [])
                if "cleaning" in f["label"].lower())

    # calendar: owner blocks + sanity distribution of day states
    blocked = defaultdict(int)
    day_states = defaultdict(lambda: defaultdict(int))
    for m, days in calendar.items():
        if isinstance(days, dict) and "error" in days:
            print(f"WARNING: no calendar for {m}: {days['error']}")
            continue
        if isinstance(days, dict):
            days = days.get("days", [])
        for day in days:
            reason = day["status"]["reason"]
            day_states[m][reason] += 1
            if reason == "BLOCKED":
                blocked[m] += 1

    print("calendar day states per month (sanity check):")
    for m in MONTHS:
        print(f"  {m}: {dict(day_states[m])}")
    if n_no_breakdown:
        print(f"note: {n_no_breakdown} reservations lacked accommodation_breakdown; spread evenly")

    rows = []
    for m in MONTHS:
        y, mo = int(m[:4]), int(m[5:7])
        import calendar as cal_mod
        dim = cal_mod.monthrange(y, mo)[1]
        avail = dim - blocked[m]
        gross = round(acc_rev[m] + cleaning[m], 2)
        adr = round(acc_rev[m] / nights[m], 2) if nights[m] else 0
        occ = round(100 * nights[m] / avail, 1) if avail else 0
        revpar = round(acc_rev[m] / avail, 2) if avail else 0
        fee_pct = round(100 * host_fees[m] / fee_base[m], 2) if fee_base[m] else None
        rows.append({
            "month": m,
            "gross_revenue": gross,
            "accommodation_revenue": round(acc_rev[m], 2),
            "cleaning_fees_collected": round(cleaning[m], 2),
            "host_service_fees": round(host_fees[m], 2),
            "host_fee_pct": fee_pct if fee_pct is not None else "",
            "refunds_adjustments": round(adjustments[m], 2),
            "cancellation_income": round(cancel_income[m], 2),
            "nights_booked": nights[m],
            "days_in_month": dim,
            "owner_blocked_nights": blocked[m],
            "nights_available": avail,
            "occupancy_pct": occ,
            "occupancy_pct_calendar_days": round(100 * nights[m] / dim, 1),
            "adr": adr,
            "revpar": revpar,
            "revpar_calendar_days": round(acc_rev[m] / dim, 2),
        })

    OUT.mkdir(parents=True, exist_ok=True)
    out_file = OUT / "pnl-12mo-revenue.csv"
    with out_file.open("w", newline="") as fh:
        w = csv.DictWriter(fh, fieldnames=list(rows[0].keys()))
        w.writeheader()
        w.writerows(rows)
    print(f"wrote {out_file.relative_to(REPO)}")

    # reconciliation: payouts in window vs derived net revenue
    po_total = sum((p["amount"]["amount"] or 0) for p in payouts
                   if p["date"][:7] in MONTHS) / 100
    derived_net = sum(r["gross_revenue"] - r["host_service_fees"]
                      + r["refunds_adjustments"] + r["cancellation_income"] for r in rows)
    po_dates = sorted(p["date"][:10] for p in payouts)
    print(f"payout records span {po_dates[0]} .. {po_dates[-1]} ({len(payouts)} payouts)")
    print(f"payouts dated in window: ${po_total:,.2f}")
    print(f"derived net revenue (gross - host fees + adj + cancel income): ${derived_net:,.2f}")

    tot_nights = sum(r["nights_booked"] for r in rows)
    tot_gross = sum(r["gross_revenue"] for r in rows)
    print(f"window totals: {tot_nights} nights, ${tot_gross:,.2f} gross")


if __name__ == "__main__":
    main()
