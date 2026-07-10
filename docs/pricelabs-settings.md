# PriceLabs settings — Skyland (execution checklist)

Concrete settings changes for the Phase 3 pricing intervention (`docs/interventions.md`).
Owner action, in the PriceLabs dashboard for listing **Skyland** (Woodfin, NC; connected via
Hostaway/smartbnb; also syncs to a direct-booking channel). Settings and market data pulled
**2026-07-09**. UI labels may differ slightly by PriceLabs version — the *intent* of each step is
what matters.

Open PriceLabs → **Listings → Skyland → Pricing / Customize**.

| # | Setting | Current | Change to | Why |
|---|---|---|---|---|
| 1 | **Max Price** | **$750** | **$1,050** | Highest-confidence win, zero occupancy risk. Peak market 90th pct is $900–1,100 and Skyland *has booked $858–935* on peak dates — the $750 cap is throttling those nights. PriceLabs only reaches the ceiling when demand supports it. |
| 2 | **Base Price** | **$521** | **leave (~$521)** | PriceLabs' own recommended base is **$522** — the base is already market-correct. **Do not cut it.** |
| 3 | **Min Price** | **$350** | **leave ($350)** | Sits at the 5BR 25th percentile — an appropriate floor. The problem isn't that the floor is too high; it's that the curve doesn't ride *down* to it (step 4). |
| 4 | **Pricing aggressiveness / occupancy-based adjustment** | curve stalls soft nights near ~$500 | **more aggressive on the low end** | Far-out and low-demand mid-week nights price ~$500 while market median is ~$400 and they sit empty (e.g. 07-19: $504 vs $401). Increase aggressiveness (or lower the occupancy-based-adjustment %s for low occupancy / far horizons) so unbooked soft dates slide toward **$380–420** as they approach. The $350 floor already permits this. |
| 5 | **Last-Minute discount** | verify | enable/steepen **0–3 day** window (~ −15% to −25%) | Peak-season bookings land **0–2 days before stay** — near-term empty nights should clear, not expire. |
| 6 | **Min-stay / Orphan gaps** | 2 nights everywhere | allow **1-night** orphan-gap fills; reduce gap min-stay to 1 | Recover single-night holes between bookings in soft periods. |
| 7 | **Sync / push** | push enabled, last push 2026-07-09 | confirm auto-push **on** after edits | So the new curve actually reaches Airbnb + the direct channel. |

## After you change it

1. **Push prices** (or wait for the daily auto-push) and spot-check the Airbnb calendar: peak weekends should now exceed $750; soft mid-week nights should be lower than before.
2. **Do not also tune the base or min** — changing three things at once makes the 90-day test unreadable. This intervention is: **raise cap + steepen low-end aggressiveness + last-minute + orphan gaps.**
3. **Freeze the baseline** (already recorded in `docs/decisions.md`) and let it run to the **~2026-10-09** review.

## What this does NOT address

Base pricing is already market-correct, so if occupancy stays 13–18 pts below market after this, the
constraint is **conversion, not price** — run the listing-quality audit in `docs/interventions.md`
(photos, title, reviews, filters). That's the other half of the 90-day verdict.
