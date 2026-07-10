"""Combine the revenue-side and cost-side CSVs into a monthly Skyland P&L.

Reads:
  data/pnl/pnl-12mo-revenue.csv  (accrual revenue, from build_pnl.py)
  data/pnl/pnl-12mo-costs.csv    (cost side + actual Airbnb cash deposits)

Writes:
  data/pnl/pnl-combined.csv      (one row per month + a TOTAL row)
and prints the same table.

Two revenue bases are reported (see data/pnl/costs-README.md caveat #2):
  - accrual  = gross_revenue - host_service_fees + refunds_adjustments  (Hospitable host-side)
  - cash     = airbnb_deposits_cash                                     (what actually banked)

Two cost bases:
  - cash economic outlay incl. mortgage principal = skyland_cost_total
  - economic expense = skyland_cost_total - mortgage_principal_est      (principal is equity, not an expense)

Usage: python analysis/build_pnl_combined.py
"""

from __future__ import annotations

import csv
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent
PNL = REPO / "data" / "pnl"


def f(x: str) -> float:
    return float(x) if x not in (None, "") else 0.0


def load(name: str) -> dict[str, dict]:
    with open(PNL / name, newline="") as fh:
        return {row["month"]: row for row in csv.DictReader(fh)}


def main() -> None:
    rev = load("pnl-12mo-revenue.csv")
    cost = load("pnl-12mo-costs.csv")
    months = sorted(set(rev) | set(cost))

    cols = [
        "month", "accrual_net_rev", "cash_rev", "cost_total",
        "principal", "net_cash", "net_cash_economic", "net_accrual",
    ]
    rows = []
    tot = {c: 0.0 for c in cols[1:]}
    covered = 0

    for m in months:
        r, c = rev.get(m, {}), cost.get(m, {})
        if not c or c.get("skyland_cost_total", "") == "":
            # cost row missing (e.g. 2025-07) — report revenue only, exclude from totals
            accrual = f(r.get("gross_revenue")) - f(r.get("host_service_fees")) + f(r.get("refunds_adjustments"))
            rows.append({"month": m, "accrual_net_rev": round(accrual, 2), "cash_rev": None,
                         "cost_total": None, "principal": None, "net_cash": None,
                         "net_cash_economic": None, "net_accrual": None})
            continue

        accrual = f(r.get("gross_revenue")) - f(r.get("host_service_fees")) + f(r.get("refunds_adjustments"))
        cash_rev = f(c["airbnb_deposits_cash"])
        cost_total = f(c["skyland_cost_total"])
        principal = f(c["mortgage_principal_est"])
        econ_cost = cost_total - principal

        row = {
            "month": m,
            "accrual_net_rev": round(accrual, 2),
            "cash_rev": round(cash_rev, 2),
            "cost_total": round(cost_total, 2),
            "principal": round(principal, 2),
            "net_cash": round(cash_rev - cost_total, 2),
            "net_cash_economic": round(cash_rev - econ_cost, 2),
            "net_accrual": round(accrual - cost_total, 2),
        }
        rows.append(row)
        for k in cols[1:]:
            tot[k] += row[k]
        covered += 1

    total_row = {"month": f"TOTAL ({covered}mo)", **{k: round(tot[k], 2) for k in cols[1:]}}
    rows.append(total_row)

    with open(PNL / "pnl-combined.csv", "w", newline="") as fh:
        w = csv.DictWriter(fh, fieldnames=cols)
        w.writeheader()
        for row in rows:
            w.writerow({k: ("" if row.get(k) is None else row.get(k, "")) for k in cols})

    widths = {c: max(len(c), 14) for c in cols}
    print("  ".join(c.rjust(widths[c]) for c in cols))
    for row in rows:
        print("  ".join(("" if row.get(c) is None else str(row.get(c, ""))).rjust(widths[c]) for c in cols))


if __name__ == "__main__":
    main()
