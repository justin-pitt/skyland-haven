# Phase 1 Data Collection — Report

**Date:** 2026-07-08
**Property:** Skyland Haven — 39 West Skyland Circle, Woodfin, NC 28804
(5BR/3BA, sleeps 12, hot tub + game room). Airbnb listing
[907933203969939408](https://airbnb.com/rooms/907933203969939408).
**Scope:** Programmatic pull of every Phase 1 input the connected APIs can
supply. **Phase 2 diagnosis is deliberately NOT started** — real data gaps
remain (see below), and per the project hard rules those get asked about, not
analyzed around.

---

## What was collected

All outputs are reproducible from `data/` via the scripts in `analysis/`.

### Revenue side — Hospitable API (trailing 12 months, 2025-07 .. 2026-06)

- **Script:** `analysis/fetch_hospitable.py` (reads PAT from `.env`) →
  `analysis/build_pnl.py`
- **Raw:** `data/raw/hospitable/` (gitignored — contains guest PII)
- **Output:** `data/pnl/pnl-12mo-revenue.csv`, one row per month
- **Column derivations:** documented in `data/pnl/README.md`

Pulled: 69 reservations (with full host-side financials), 20 payouts,
41 transactions, 12 months of calendar. Derived monthly: gross revenue,
accommodation revenue (allocated per stay-night from Airbnb's own per-date
`accommodation_breakdown`), cleaning fees collected, refunds/adjustments,
cancellation income, nights booked, nights available, occupancy %, ADR
(accommodation ÷ nights booked, fees excluded), RevPAR, and effective Airbnb
host-fee %.

**The 12-month revenue picture (host-side USD):**

| month | gross rev | acc. rev | cleaning | host fee % | nights booked | ADR | occ % (avail) | occ % (cal days) |
|---|---|---|---|---|---|---|---|---|
| 2025-07 | 7,978 | 6,828 | 1,150 | 2.74 | 12 | 569.00 | 100.0* | 38.7 |
| 2025-08 | 7,557 | 6,407 | 1,150 | 2.89 | 10 | 640.70 | 100.0* | 32.3 |
| 2025-09 | 2,392 | 1,892 | 500 | 3.00 | 4 | 473.00 | 100.0* | 13.3 |
| 2025-10 | 11,231 | 9,036 | 2,195 | 2.89 | 17 | 531.53 | 100.0* | 54.8 |
| 2025-11 | 7,549 | 6,452 | 1,097 | 5.81 | 9 | 716.89 | 100.0* | 30.0 |
| 2025-12 | 10,413 | 8,904 | 1,509 | 6.66 | 14 | 636.00 | 100.0* | 45.2 |
| 2026-01 | 4,460 | 3,636 | 824 | 15.97 | 7 | 519.43 | 100.0* | 22.6 |
| 2026-02 | 4,320 | 3,548 | 772 | 7.24 | 7 | 506.86 | 25.9 | 25.0 |
| 2026-03 | 6,201 | 4,965 | 1,236 | 15.50 | 7 | 709.29 | 22.6 | 22.6 |
| 2026-04 | 8,590 | 6,942 | 1,648 | 15.50 | 11 | 631.09 | 36.7 | 36.7 |
| 2026-05 | 8,063 | 6,415 | 1,648 | 15.50 | 9 | 712.78 | 29.0 | 29.0 |
| 2026-06 | 7,545 | 6,294 | 1,251 | 15.50 | 8 | 786.75 | 26.7 | 26.7 |

`*` = artifact. The availability denominator is unreliable before 2026-02
(see gap #1). Use the `occ % (cal days)` column — nights booked ÷ days in
month — for those earlier months. **Window totals: 115 nights booked,
$86,299 gross.**

### Market side — PriceLabs (via MCP connector)

- **Script:** `analysis/build_comps.py`
- **Raw:** `data/raw/pricelabs/` (market aggregates only, no PII — committed
  as citable comp evidence)
- **Outputs:**
  - `data/comps/market-daily-60d.csv` — our price vs comp-set 25/50/75/90th
    percentile prices + market occupancy, daily, 2026-07-09 → 2026-09-06
  - `data/comps/market-history-24mo.csv` — trailing 24 months comp-set ADR,
    occupancy, median booked LOS, booking window
  - `data/comps/market-summary.md` — bedroom-band price percentiles +
    PriceLabs seasonal/demand insights (verbatim)

**Comp-set nightly price percentiles (next-365d market rates):**

| category | n | 25th | median | 75th | 90th |
|---|---|---|---|---|---|
| 4 BR | 197 | $256 | $346 | $471 | $655 |
| 5 BR | 81 | $350 | $422 | $639 | $826 |
| 6 BR | 57 | $511 | $714 | $1,001 | $1,176 |
| All | 335 | $287 | $408 | $616 | $862 |

---

## Signals recorded (NOT a diagnosis)

These are flagged for Phase 2, not classified — the cost side does not exist
yet, so no loss-driver call can be made.

1. **Airbnb host fee changed regime mid-year.** ~3% split-fee through
   Oct 2025 → transitional Nov 2025–Feb 2026 → steady **15.5% host-only**
   from Mar 2026. On ~$8.6K gross that is roughly $1,070/mo in host fees vs
   ~$260/mo under the old model — a real recurring P&L change to model.
2. **Occupancy is running below the comp set while ADR runs above it.**
   Feb–Jun 2026 own occupancy 22–37% vs comp-set 39–62% (market-history CSV),
   with own ADR $506–787 vs 5BR market median $422. Consistent with a
   price-position/occupancy question — but not diagnosed until costs land.
3. **Occupancy tax looks Airbnb-remitted.** Buncombe Accommodations Tax,
   Buncombe Sales/Use Tax, and NC Sales/Use Tax appear only as guest-side
   lines that never touch host revenue. One owner verification remains
   (item 14).

---

## Data gaps blocking Phase 2 (owner homework)

Tracked in `docs/data-checklist.md`. Summary:

1. **Availability history Jul 2025 – Jan 2026 (item 2, partial).** Hospitable
   connected ~late Jan 2026 and did not backfill calendar blocks or payouts,
   so every unreserved day before Feb 2026 reads BLOCKED and pre-Feb
   occupancy-vs-available is an artifact. Pull Airbnb Insights → Occupancy &
   rates for those months to get true availability/owner blocks.
2. **Entire cost side (items 6–12):** mortgage/carrying cost, utilities
   actuals (12 mo), cleaning cost per turnover + invoices, supplies, hot tub
   maintenance/chemicals, repairs, insurance (STR policy?) + property tax.
3. **Tax verification (item 14):** confirm listing → Pricing & availability →
   Taxes shows nothing owner-remitted.
4. **Comp evidence (items 15–17):** first-5-photos screenshot, 5 hand-picked
   comps into `data/comps/comps.md`, and their rate screenshots. PriceLabs
   aggregates stand in as interim comp evidence but the hand-picked set is
   still required by the spec.

**Phase 2 can start once the cost-side numbers land in `data/pnl/`.**

---

## Reproducibility

```
python analysis/fetch_hospitable.py   # raw Hospitable JSON (needs .env PAT)
python analysis/build_pnl.py          # -> data/pnl/pnl-12mo-revenue.csv
python analysis/build_comps.py        # -> data/comps/*  (from data/raw/pricelabs/)
```

PriceLabs raw JSON was captured via the MCP connector (free tier has no REST
API); the responses are checked in under `data/raw/pricelabs/` so
`build_comps.py` runs without re-hitting the connector.
