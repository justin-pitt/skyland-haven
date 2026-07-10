# Phase 1 Data-Collection Checklist

Every input from the handoff spec, monthly granularity, **trailing 12 months**. Pull everything before Phase 2 diagnosis begins — per the hard rules, missing or inconsistent months get asked about, not analyzed around.

**Drop targets:**
- P&L numbers → `data/pnl/` (one CSV per month: `YYYY-MM.csv`, or a single `pnl-12mo.csv` with a month column)
- Comp evidence → `data/comps/` (screenshots named `comp<N>-YYYY-MM-DD.png`, plus `comps.md` with listing URLs)

> Airbnb note: the one export that covers most of the revenue side is the **earnings CSV**. Get it once for the full 12-month range: **airbnb.com/hosting/earnings → (filter to date range) → Get report / Export CSV**. Most revenue items below are columns in that file.

---

## Revenue side (source: Airbnb host dashboard)

- [x] **1. Gross booking revenue by month** ✅ 2026-07-08 — pulled via Hospitable API (`analysis/fetch_hospitable.py` → `analysis/build_pnl.py`), `gross_revenue` in `data/pnl/pnl-12mo-revenue.csv`. Derivations in `data/pnl/README.md`.
  - *Where:* Hosting → **Earnings** (airbnb.com/hosting/earnings). Filter by month for the summary view, or export the CSV report and sum the gross earnings column per month.
  - *Save as:* `gross_revenue` column in `data/pnl/`.

- [ ] **2. Nights booked and nights available (occupancy rate)** ⚠️ PARTIAL 2026-07-08 — `nights_booked` is solid (per-night from reservations). `nights_available` is only trustworthy from **2026-02 onward**: Hospitable's calendar shows every unreserved day before then as BLOCKED (connected ~Jan 2026, no availability backfill). **Owner homework: pull Airbnb Insights → Occupancy & rates for Jul 2025–Jan 2026** to confirm real availability/blocks; until then use `occupancy_pct_calendar_days`.
  - *Where:* Hosting → **Insights → Performance → Occupancy & rates** shows occupancy % and booked nights by month. Nights *available* needs your blocked-night count too — cross-check the **Calendar** for owner blocks/maintenance holds so the denominator is nights you actually offered, not 30.
  - *Save as:* `nights_booked`, `nights_available` columns. Note owner-blocked nights separately — they matter for the structural diagnosis.

- [x] **3. Average daily rate (ADR) by month** ✅ 2026-07-08 — computed version used: host-side accommodation revenue ÷ nights booked, cleaning fees excluded (`adr` in `data/pnl/pnl-12mo-revenue.csv`).
  - *Where:* Same Insights → Performance area ("average nightly rate"), **or** compute from the earnings CSV: accommodation revenue ÷ nights booked (excluding cleaning fees). Prefer the computed version — the dashboard figure can blend in fees. State which one you used.
  - *Save as:* `adr` column.

- [x] **4. Cleaning fees collected** ✅ 2026-07-08 — host-side cleaning-fee lines per reservation, attributed to check-in month (`cleaning_fees_collected`).
  - *Where:* Earnings CSV — per-reservation **Cleaning fee** column. Sum per month.
  - *Save as:* `cleaning_fees_collected` column.

- [x] **5. Cancellations / refund amounts** ✅ 2026-07-08 — reservation-ledger adjustments (`refunds_adjustments`: −$335.27 Dec 2025, −$100 Feb 2026) + retained cancellation payouts (`cancellation_income`: $0 in window). Caveat: resolution-center payouts outside reservations not captured.
  - *Where:* Earnings CSV — adjustment/refund rows (negative amounts), and Hosting → Earnings → **Transaction history** for anything the report labels as an adjustment. Include host-issued refunds and cancellation payouts.
  - *Save as:* `refunds_cancellations` column.

- [x] **13. Airbnb host fee percentage in effect** ✅ 2026-07-08 — `host_fee_pct` column. **It changed mid-year:** ~3% split-fee through Oct 2025, transitional Nov 2025–Feb 2026, steady **15.5% host-only** from Mar 2026 (PriceLabs also reports "Host-only fee" on file). This fee jump is a real P&L driver to examine in Phase 2.
  - *Where:* Earnings CSV — **Service fee** column ÷ gross per reservation. You're on either the split fee (~3% host side) or host-only/simplified (~15%). Confirm which, and whether it changed mid-year.
  - *Save as:* note in `data/pnl/README` or a `host_fee_pct` column.

- [ ] **14. Buncombe County occupancy tax handling** ⚠️ MOSTLY VERIFIED 2026-07-08 — reservation financials show "Accommodations Tax (Buncombe)", "General Sales and Use Tax (Buncombe)", and "General Sales and Use Tax (NC)" as guest-side lines that never touch host revenue → Airbnb collects and remits. **Owner homework: confirm listing → Pricing & availability → Taxes shows no owner-remitted local tax** (5 min).
  - *Where:* Two checks: (a) earnings CSV **Occupancy taxes** column — if populated, Airbnb is collecting/remitting; (b) your listing → **Pricing & availability → Taxes** shows which local taxes Airbnb handles vs. leaves to you. Determine whether Buncombe County occupancy tax + NC sales tax are Airbnb-remitted or owner-remitted. If owner-remitted, that's a real monthly cost line.
  - *Save as:* note + `occupancy_tax_owner_paid` column if applicable.

## Cost side (source: your records, not Airbnb)

- [x] **6. Mortgage / carrying cost** ✅ 2026-07-09 — Movement Mortgage statements (`skyland-statement-*`). **$3,687.96/mo** (through Dec-2025) → **$3,725.68/mo** (from Jan-2026, escrow reset). Balance $473,271 @ 6.375%, PMI ~$181/mo inside escrow. `mortgage_piti` in `data/pnl/pnl-12mo-costs.csv`.
  - *Where:* Loan servicer statements (principal + interest + escrow).

- [x] **7. Utilities** ✅ 2026-07-09 — from Pittnet Properties bank statements: Duke Energy (power, seasonal $160–434), Spectrum (internet $130–140), Woodfin Sanitary (water/sewer, ~bimonthly). No separate trash vendor (Woodfin covers sanitation). LTR tenant pays their own utilities → all utilities here are Skyland (owner-confirmed).
  - *Where:* Provider billing portals — sourced instead from the account debits.

- [x] **8. Cleaning cost per turnover + turnovers** ✅ 2026-07-09 — 5StrClean, ~$360/turnover. **Cleaning paid ($14,143/11mo) ≈ cleaning fees collected ($13,830)** → net ~$28/mo, washes. `cleaning` column.

- [~] **9. Supplies and consumables** ⚠️ PARTIAL 2026-07-09 — one bulk buy visible (HostGPO $1,470, Aug-2025); otherwise minimal on statements. Likely under-captured if bought on a personal card. `supplies`/`other` columns.

- [x] **10. Hot tub maintenance and chemicals** ✅ 2026-07-10 — **owner-confirmed: included in the cleaning fee** (5StrClean services the hot tub as part of each turnover). No separate cost line — it lives inside `cleaning`, which washes against cleaning fees collected.

- [~] **11. Repairs and maintenance** ⚠️ MINIMAL IN WINDOW 2026-07-09 — no major repair invoices Aug-2025→Jun-2026; closest are ambiguous `other` lines (Thumbtack, Venmo "marcus" ~$50). Confirm no large repairs were paid off-account.

- [x] **12. Insurance (STR policy) and property tax** ✅ 2026-07-10 — **escrowed** inside the mortgage (~$650/mo escrow = tax + insurance + PMI). Owner-confirmed **both STR and homeowner's insurance are carried and paid through the mortgage escrow** → no coverage gap, no separate/missing insurance cost line. (Optional refinement: `skyland-escrow-analysis-2025.pdf` splits the escrow into exact tax vs. insurance $, not needed for the diagnosis.)

## Market side (source: Airbnb search + listing editor)

- [ ] **15. Listing URL and current photo order**
  - *Where:* Listing URL is known (airbnb.com/rooms/907933203969939408). Photo order: Hosting → **Listings → your listing → Photo tour** — screenshot the first 5 photos in order (they drive click-through and are a zero-cost lever).
  - *Save as:* screenshots in `data/comps/` (`own-listing-photos-YYYY-MM-DD.png`).

- [ ] **16. Five comparable active listings** (Woodfin / North Asheville, similar bed/bath, hot tub)
  - *Where:* Airbnb search in an **incognito window** (avoids personalized results): map area Woodfin/North Asheville, filter to your bed/bath count + "Hot tub" amenity. Pick 5 active listings with review counts high enough to be credibly booked.
  - *Save as:* `data/comps/comps.md` with the 5 URLs + one-line description each.

- [ ] **17. Comp nightly rates for the next 60 days** ⚠️ PARTIAL 2026-07-08 — market-aggregate version pulled via PriceLabs MCP: `data/comps/market-daily-60d.csv` (daily 25/50/75/90th-percentile comp prices + market occupancy vs our price, 2026-07-09 → 2026-09-06), `data/comps/market-history-24mo.csv` (trailing comp-set ADR/occupancy), `data/comps/market-summary.md`. Raw source: `data/raw/pricelabs/`. **Per-listing rate screenshots for the 5 hand-picked comps (item 16) still owner homework.**
  - *Where:* Open each comp's calendar and screenshot rates across the next 60 days (grab a weekday week and a weekend in each month), **or** pull AirDNA's free Rentalizer data for the market. Screenshots preferred — per the analysis conventions, comp data needs citable sources.
  - *Save as:* `data/comps/comp<N>-rates-YYYY-MM-DD.png` per listing.

---

## Status after 2026-07-08 API pull

**Done programmatically (Hospitable + PriceLabs MCP):** 1, 3, 4, 5, 13 fully; 2, 14, 17 partially (see notes inline).

**Remaining owner homework:**
1. **Item 2 (partial):** Airbnb Insights → Occupancy & rates, Jul 2025–Jan 2026 — real availability/owner blocks (Hospitable calendar history starts ~Feb 2026).
2. **Item 6:** Mortgage / carrying cost (loan servicer statements).
3. **Item 7:** Utilities, 12 months of actuals (power, water, internet, trash).
4. **Item 8:** Cleaning cost per turnover + invoices (reconcile against checkout counts in `data/pnl/`).
5. **Item 9:** Supplies and consumables (estimate OK, flag as estimate).
6. **Item 10:** Hot tub maintenance and chemicals (keep separate from supplies).
7. **Item 11:** Repairs and maintenance, dated.
8. **Item 12:** Insurance declarations page + Buncombe property tax bill; note if the policy is actually an STR policy.
9. **Item 14 (verification only):** listing → Pricing & availability → Taxes — confirm Airbnb remits everything.
10. **Item 15:** Screenshot the first 5 photos in current order.
11. **Item 16:** Pick 5 comparable listings (URLs + one-liner into `data/comps/comps.md`).
12. **Item 17 (evidence):** Rate screenshots for those 5 comps (PriceLabs aggregates are in place as interim comp evidence).

## Done when

All 17 items checked, `data/pnl/` has 12 months of consistent numbers, and `data/comps/` has 5 sourced comps with rate evidence. Then Phase 2 (diagnosis) can start — no interventions, and especially no capex talk, before `docs/diagnosis.md` exists.
