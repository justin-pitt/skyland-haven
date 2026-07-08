# Phase 1 Data-Collection Checklist

Every input from the handoff spec, monthly granularity, **trailing 12 months**. Pull everything before Phase 2 diagnosis begins — per the hard rules, missing or inconsistent months get asked about, not analyzed around.

**Drop targets:**
- P&L numbers → `data/pnl/` (one CSV per month: `YYYY-MM.csv`, or a single `pnl-12mo.csv` with a month column)
- Comp evidence → `data/comps/` (screenshots named `comp<N>-YYYY-MM-DD.png`, plus `comps.md` with listing URLs)

> Airbnb note: the one export that covers most of the revenue side is the **earnings CSV**. Get it once for the full 12-month range: **airbnb.com/hosting/earnings → (filter to date range) → Get report / Export CSV**. Most revenue items below are columns in that file.

---

## Revenue side (source: Airbnb host dashboard)

- [ ] **1. Gross booking revenue by month**
  - *Where:* Hosting → **Earnings** (airbnb.com/hosting/earnings). Filter by month for the summary view, or export the CSV report and sum the gross earnings column per month.
  - *Save as:* `gross_revenue` column in `data/pnl/`.

- [ ] **2. Nights booked and nights available (occupancy rate)**
  - *Where:* Hosting → **Insights → Performance → Occupancy & rates** shows occupancy % and booked nights by month. Nights *available* needs your blocked-night count too — cross-check the **Calendar** for owner blocks/maintenance holds so the denominator is nights you actually offered, not 30.
  - *Save as:* `nights_booked`, `nights_available` columns. Note owner-blocked nights separately — they matter for the structural diagnosis.

- [ ] **3. Average daily rate (ADR) by month**
  - *Where:* Same Insights → Performance area ("average nightly rate"), **or** compute from the earnings CSV: accommodation revenue ÷ nights booked (excluding cleaning fees). Prefer the computed version — the dashboard figure can blend in fees. State which one you used.
  - *Save as:* `adr` column.

- [ ] **4. Cleaning fees collected**
  - *Where:* Earnings CSV — per-reservation **Cleaning fee** column. Sum per month.
  - *Save as:* `cleaning_fees_collected` column.

- [ ] **5. Cancellations / refund amounts**
  - *Where:* Earnings CSV — adjustment/refund rows (negative amounts), and Hosting → Earnings → **Transaction history** for anything the report labels as an adjustment. Include host-issued refunds and cancellation payouts.
  - *Save as:* `refunds_cancellations` column.

- [ ] **13. Airbnb host fee percentage in effect**
  - *Where:* Earnings CSV — **Service fee** column ÷ gross per reservation. You're on either the split fee (~3% host side) or host-only/simplified (~15%). Confirm which, and whether it changed mid-year.
  - *Save as:* note in `data/pnl/README` or a `host_fee_pct` column.

- [ ] **14. Buncombe County occupancy tax handling**
  - *Where:* Two checks: (a) earnings CSV **Occupancy taxes** column — if populated, Airbnb is collecting/remitting; (b) your listing → **Pricing & availability → Taxes** shows which local taxes Airbnb handles vs. leaves to you. Determine whether Buncombe County occupancy tax + NC sales tax are Airbnb-remitted or owner-remitted. If owner-remitted, that's a real monthly cost line.
  - *Save as:* note + `occupancy_tax_owner_paid` column if applicable.

## Cost side (source: your records, not Airbnb)

- [ ] **6. Mortgage / carrying cost allocated to the property**
  - *Where:* Loan servicer statements (principal + interest + escrow). If no mortgage, use the agreed carrying-cost allocation and document the assumption.

- [ ] **7. Utilities** — power, water, internet, trash
  - *Where:* Provider billing portals (12 months each). Power will be seasonal in Woodfin — get actuals per month, not an average.

- [ ] **8. Cleaning cost per turnover + turnovers per month**
  - *Where:* Cleaner invoices or payment app history (Venmo/Zelle/etc.). Turnover count = number of checkouts, which you can pull from the earnings CSV reservation rows — reconcile the two.

- [ ] **9. Supplies and consumables**
  - *Where:* Receipts / card statements (Amazon, Costco, etc.). A reasonable monthly estimate is acceptable here if receipts are scattered — flag it as an estimate.

- [ ] **10. Hot tub maintenance and chemicals**
  - *Where:* Receipts (chemicals, filters) + any service visits. Keep separate from general supplies — it's a candidate cost lever and an amenity we may lean on for ADR.

- [ ] **11. Repairs and maintenance**
  - *Where:* Invoices/receipts, dated. One-time items should stay identifiable so they don't distort a single month's picture.

- [ ] **12. Insurance (STR policy) and property tax**
  - *Where:* Policy declarations page (annual premium ÷ 12) + Buncombe County property tax bill (tax.buncombecounty.org for the bill amount). Note whether the policy is actually an STR policy or homeowner's.

## Market side (source: Airbnb search + listing editor)

- [ ] **15. Listing URL and current photo order**
  - *Where:* Listing URL is known (airbnb.com/rooms/907933203969939408). Photo order: Hosting → **Listings → your listing → Photo tour** — screenshot the first 5 photos in order (they drive click-through and are a zero-cost lever).
  - *Save as:* screenshots in `data/comps/` (`own-listing-photos-YYYY-MM-DD.png`).

- [ ] **16. Five comparable active listings** (Woodfin / North Asheville, similar bed/bath, hot tub)
  - *Where:* Airbnb search in an **incognito window** (avoids personalized results): map area Woodfin/North Asheville, filter to your bed/bath count + "Hot tub" amenity. Pick 5 active listings with review counts high enough to be credibly booked.
  - *Save as:* `data/comps/comps.md` with the 5 URLs + one-line description each.

- [ ] **17. Comp nightly rates for the next 60 days**
  - *Where:* Open each comp's calendar and screenshot rates across the next 60 days (grab a weekday week and a weekend in each month), **or** pull AirDNA's free Rentalizer data for the market. Screenshots preferred — per the analysis conventions, comp data needs citable sources.
  - *Save as:* `data/comps/comp<N>-rates-YYYY-MM-DD.png` per listing.

---

## Done when

All 17 items checked, `data/pnl/` has 12 months of consistent numbers, and `data/comps/` has 5 sourced comps with rate evidence. Then Phase 2 (diagnosis) can start — no interventions, and especially no capex talk, before `docs/diagnosis.md` exists.
