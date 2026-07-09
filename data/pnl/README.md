# data/pnl/ — revenue-side P&L (trailing 12 months: 2025-07 .. 2026-06)

## Files

- `pnl-12mo-revenue.csv` — one row per month. Produced by `analysis/build_pnl.py`
  from raw Hospitable API JSON in `data/raw/hospitable/` (gitignored — contains
  guest PII; regenerate with `analysis/fetch_hospitable.py`, PAT in `.env`).

Source: Hospitable public API v2 (`/reservations?include=financials`,
`/properties/{uuid}/calendar`, `/payouts`), property `Skyland`
(`8f91a20f-5c4d-4b42-aa35-f0e7812d64cf`), pulled 2026-07-08.
Cost-side lines (mortgage, utilities, cleaning invoices, etc.) are NOT here yet —
they are owner homework per `docs/data-checklist.md`.

## Column derivations

All dollar amounts are host-side USD (what the host earns), not guest-paid totals.

| column | derivation |
|---|---|
| `accommodation_revenue` | Sum of host-side per-night amounts from each accepted reservation's `accommodation_breakdown`, allocated to the month **each stay night falls in**. Reservations without a breakdown (0 in this pull) would be spread evenly across stay nights. |
| `cleaning_fees_collected` | Host-side "Cleaning fee" guest-fee line, attributed to the **check-in month**. |
| `gross_revenue` | `accommodation_revenue + cleaning_fees_collected`. Excludes Airbnb-collected taxes (pass-through, never touch the host). |
| `host_service_fees` | Absolute value of host-side "Host service fee" lines, attributed to check-in month. |
| `host_fee_pct` | `host_service_fees ÷ (accommodation + cleaning fees)` for reservations checking in that month. **Note the regime change**: ~3% (split-fee) through 2025-10, transitional Nov 2025–Feb 2026 (mix of bookings made under both models), steady 15.5% (host-only fee) from 2026-03. |
| `refunds_adjustments` | Host-side adjustment lines (negative = money returned), check-in month. |
| `cancellation_income` | Host revenue retained on cancelled reservations (cancellation payouts), check-in month. Zero across this window. |
| `nights_booked` | Accepted guest-stay reservations; each stay night (arrival .. departure−1) counted in the month it falls in. |
| `owner_blocked_nights` | Calendar days with status `BLOCKED` (not reservation-covered). **Unreliable before 2026-02 — see caveat.** |
| `nights_available` | `days_in_month − owner_blocked_nights`. Same caveat. |
| `occupancy_pct` | `nights_booked ÷ nights_available`. Same caveat. |
| `occupancy_pct_calendar_days` | `nights_booked ÷ days_in_month` — floor metric, immune to the blocked-day problem. Use this for pre-2026-02 months until block history is confirmed. |
| `adr` | `accommodation_revenue ÷ nights_booked` (cleaning fees excluded, per checklist item 3). |
| `revpar` | `accommodation_revenue ÷ nights_available` (same pre-2026-02 caveat). |
| `revpar_calendar_days` | `accommodation_revenue ÷ days_in_month`. |

## Data-quality caveats (must resolve before Phase 2)

1. **Calendar block history is not trustworthy before 2026-02.** Every
   non-reserved day from 2025-07 through 2026-01 reads `BLOCKED` with zero
   `AVAILABLE` days, then 2026-02 onward looks normal. Combined with payout
   records existing only from 2026-01-31, the likely explanation is that
   Hospitable was connected ~late Jan 2026 and did not backfill calendar
   availability (reservations did backfill). `occupancy_pct = 100%` for those
   months is an artifact. **Owner must confirm from Airbnb's own
   Insights → Occupancy & rates** what actual availability/blocks were
   pre-Feb-2026.
2. **Payout reconciliation is partial for the same reason**: payouts dated in
   the window total $30,529 vs $78,244 derived net revenue; payout records
   simply start 2026-01-31. Not treated as an inconsistency in the reservation
   data.
3. **Occupancy-tax evidence (checklist item 14):** reservation financials show
   "Accommodations Tax (Buncombe)", "General Sales and Use Tax (Buncombe)" and
   "General Sales and Use Tax (North Carolina)" as guest-side lines that never
   appear in host revenue — consistent with Airbnb collecting and remitting.
   Owner should still verify listing → Pricing & availability → Taxes shows no
   owner-remitted local tax.
4. `refunds_adjustments` only captures adjustments recorded on the reservation
   ledger; resolution-center payouts outside reservations (if any) are not in
   this pull.
