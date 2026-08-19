# Skyland Haven — Decision Log

Dated log of pricing and capex decisions. Newest first.

---

## 2026-08-19 — Finding: the 2026-07-10 pricing intervention was never live; 90-day gate reset

While producing the first monthly scorecard (`docs/reports/2026-07.md`), the live PriceLabs
configuration was read back for the first time since the change was logged. **The max price is
still $750.** `get_listing_data` returns `min: 332, base: 510, max: 750` (pushed
2026-08-19T01:25:24Z), and the daily feed shows the clamp directly: on 41 of the next 135
nights the model's `uncustomized_price` exceeds $750 while the pushed price sits exactly at
$750. The 2026-07-10 entry below records the raise to $1,050 as executed and live. It is not.

Separately, **July could not have measured the intervention anyway** — all 11 July room-nights
were booked between 2026-01-21 and 2026-06-11, every one before the 2026-07-10 change date.

**Decisions:**

- The **2026-10-09 gate is void.** The 90-day clock restarts from the date the settings are
  verified live, not from 2026-07-10.
- **No new intervention is selected** until the configuration matches the log. Fix the drift
  first, one variable at a time.
- **Process change:** every future "executed" entry in this log must record a *read-back
  verification* (the API/UI value observed after saving), not just the intended change. This
  entry exists because that step was missing.

**Also surfaced (not yet decided):** forward pace is running at roughly half of last year —
23 of the remaining 135 nights of 2026 on the books vs 48 at the same point last year (Oct
19% vs 58%, Dec 13% vs 48%); PriceLabs pulse is Red at 0/10/17% occupancy for the next
7/30/60 days vs market 43/37/36%. The leading hypothesis is the **4–5 night minimum stay now
enforced across Oct–Dec** against a comp set whose median booked stay is 3 nights. This is
correlation, not proven cause — the July pull did not cover October. Confirm in the PriceLabs
min-stay settings before acting on it.

- **Cost / new recurring burn:** $0.

## 2026-07-10 — Listing-conversion audit complete: conversion is NOT the leak

Ran the parallel zero-cost funnel audit (`docs/conversion-audit.md`) using the Hospitable
API (`analysis/fetch_listing_content.py`) + live Airbnb page signals. **Result:** the listing is
strong on every measurable conversion signal — **101 reviews · 4.97★ · Superhost · Instant Book
on · sleeps 12 · professional photos.** (Hospitable's store showed only 2 reviews; that is
post-connection only — the public Airbnb count is 101. Verified before concluding.)

**Decision / implication:** this **rules out listing quality** as the alternative to the pricing
thesis and *raises confidence in the live pricing intervention* — no pivot. Fold the found
zero-cost improvements in as cheap parallel work (photo reorder to lead with scale + game room;
tag missing search-filter amenities — self check-in / mountain view / BBQ grill; front-load
"5BR · Sleeps 12" in the title; ~$20–50 hot-tub cover latch to clear the safety banner; fix the
stale "local co-host" description line). 90-day verdict still rests on **RevPAR vs baseline.**

- **Cost / new recurring burn:** $0 (one optional ~$20–50 one-time cover latch; no recurring cost).
- **Measurement gap flagged:** PriceLabs **Listing Optimizer** (search-rank data) is not on this
  account — can't measure ranking/visibility. Do **not** buy the add-on until the pricing gate runs.

## 2026-07-10 — Executed: PriceLabs max price raised $750 → $1,050

First live step of the Phase 3 pricing intervention. Owner raised the PriceLabs **Max Price**
from **$750 to $1,050** (per `docs/pricelabs-settings.md` step 1) to stop the cap from throttling
peak nights (market 90th pct $900–1,100; property has booked $858–935 on peak dates). Zero
occupancy risk — PriceLabs only reaches the ceiling when demand supports it.

- **Status:** live. Remaining settings steps (low-end aggressiveness, last-minute, orphan gaps)
  still to apply.
- **90-day review clock:** effectively started; gate **~2026-10-09** against the frozen baseline.
- Watch RevPAR on peak weekends first (fastest signal from a cap raise).

## 2026-07-09 — Phase 2 diagnosis complete: loss is occupancy-driven

Classified the loss (`docs/diagnosis.md`): **primary driver = occupancy** (26–37% vs 39–62%
comp-set occupancy while ADR sits in the 5BR top quartile), **secondary = heavy fixed-cost
load** ($3,726/mo mortgage @ 6.375% + PMI). Ruled out rate, opex-cost, and structural. Trailing
11-month cash P&L −$4,974 (−$452/mo); ~breakeven excluding mortgage principal. A 2025 co-host
(~$8K/yr) drag is already eliminated by self-managing.

**Decision:** proceed to zero-cost pricing intervention; **no capex** (diagnosis is not structural
and not amenity-driven).

## 2026-07-09 — Phase 3 intervention selected: tune dynamic pricing (zero-cost)

**Decision:** re-tune the newly-live PriceLabs dynamic pricing (sync started 2026-06-03; PriceLabs
health flag RED) rather than add capex. Four moves: (1) reduce premium on winnable mid/high-demand
open nights toward market median; (2) raise the $750 max-price cap to capture peak nights (market
90th $900–1,100); (3) aggressive last-minute pricing (peak bookings land 0–2 days out); (4) loosen
min-stay on orphan gaps. Full rationale + projections in `docs/interventions.md`.

- **Cost / new recurring burn:** $0 — PriceLabs already subscribed ($19.99/mo, in opex).
- **Projected impact:** occupancy ~28% → ~38%, net ≈ +$1,350/mo → flips −$452 to ≈ +$900/mo cash.
- **Downside:** if occupancy is conversion-limited (not price), RevPAR stays flat → kill and pivot
  to the listing-quality lever.
- **Baseline frozen (Feb–Jun 2026):** occ ~28% · ADR ~$669 · RevPAR ~$188 · net cash −$452/mo.
- **90-day review: ~2026-10-09** — double down if RevPAR & net cash improve; kill/re-tune if flat.

*Note:* pricing changes above are the recommended settings; execution in PriceLabs/Airbnb is the
owner's action. This log records the decision, not a confirmed live change.
