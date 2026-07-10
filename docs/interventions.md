# Skyland Haven — Phase 3 Intervention Plan

**Date:** 2026-07-09 · **Gated by:** `docs/diagnosis.md` (primary driver = **occupancy**; secondary = fixed-cost load).
**Rule check:** zero-cost lever, no new recurring cost, capex stays gated. All projections tie to this listing's actuals (`data/pnl/`) and the comp set (`data/comps/`, PriceLabs pulse 2026-07-09).

---

## Headline recommendation: properly tune dynamic pricing (occupancy lever)

**This is the whole ballgame, and it has barely been tried.** PriceLabs only started managing this listing on **2026-06-03** (`sync_start_date`). For the entire loss window the property was manually/statically priced. PriceLabs' own health check is **RED — "fewer bookings compared to market."** So the intervention is not "turn on dynamic pricing" — it's **tune the pricing that just went live** so it competes for the nights we're currently missing.

The occupancy gap is real and measured against the *live* market:

| Month | Our occ | Market occ | Gap |
|---|---|---|---|
| Jul-2026 | 35% | 58% | −23 pts |
| Aug-2026 | 16% | 30% | −14 pts |
| Sep-2026 | 37% | 24% | **+13 pts** (we win here) |

Four specific, zero-cost moves (from the daily comp file `market-daily-60d.csv`):

1. **Cut the premium on winnable mid/high-demand open nights.** On nights with real market demand (45–60% market occ) our open price sits at the **75th percentile**, not median — e.g. 2026-07-19 we ask **$504** vs. **$401 median** at 51% market demand, and it sits empty. Pull the base/aggressiveness down so these nights price near **median ($400–500)** and actually convert. This is the occupancy play — and it's where the loss lives.
2. **Raise the $750 max-price cap.** Peak nights are capped at **$750** while the market 90th percentile runs **$900–1,100** and the property *historically booked $858–935* on those dates (see `own_booked_adr`). We are leaving **$150–350 per peak night** on the table for no reason. Pure ADR capture, zero occupancy cost.
3. **Aggressive last-minute pricing.** In peak season bookings arrive **0–2 days before stay** (PriceLabs pulse). Turn on/steepen last-minute discounts inside the 0–3 day window so unsold near-term nights clear instead of expiring empty.
4. **Loosen min-stay on orphan gaps.** Min-stay is **2 nights everywhere**; allow 1-night fills for orphan gaps in soft mid-week periods.

**Cost:** **$0 incremental.** PriceLabs is already subscribed ($19.99/mo, already in `data/pnl/` opex). No new recurring burn.

**Projected monthly impact** (deliberately conservative — closes ~half the occupancy gap, not all of it):

| | Now (Feb–Jun actual) | Target |
|---|---|---|
| Occupancy | ~28% | ~38% |
| Blended ADR | ~$669 | ~$600 (lower on soft nights, higher cap on peak) |
| Accommodation / mo (~30 nts) | ~$5,620 | ~$6,840 |
| + peak-cap capture | — | ~$400/mo |
| **Net of 15.5% Airbnb fee** | — | **≈ +$1,350/mo** |

That flips the **−$452/mo** cash position to **≈ +$900/mo** — clearing both goals (net-positive by month 6, +$300/mo by month 12). Cleaning rises with more turnovers but is offset by cleaning fees collected (it washes — see diagnosis). Slightly higher utilities/supplies at higher occupancy are immaterial versus the revenue gain.

**Payback:** immediate — no capital deployed.

**Downside case:** if the low occupancy is **not** price-driven — i.e. it's listing quality, photos, reviews, or search visibility — then cutting price on winnable nights sheds ADR without lifting occupancy and **RevPAR goes flat or down**. Two guards: (a) the comp data shows our open-night prices are only *modestly* above market on many nights, so pricing is likely *part* not *all* of the story — run the parallel check below; (b) this is a **90-day RevPAR-gated test**, not a permanent cut — kill it if RevPAR doesn't beat the baseline.

**Headwind to price in:** the market itself is **softer YoY** (Aug market 30% vs 55% last year). Some occupancy weakness is market-wide demand contraction we can't price our way out of — hence the conservative half-the-gap target.

---

## Parallel zero-cost check (supporting, not capex): listing conversion

Because our open-night prices are *not* wildly above market yet occupancy still runs at half, **price may not be the entire story**. In parallel, and at zero cost, audit the conversion funnel: first-5-photo order, listing title/summary, review score and count, and instant-book/search filters. This is a listing-quality lever (handoff Phase 3 "zero-cost first" menu), runs alongside the pricing tune, and costs nothing. Findings feed the next scorecard.

## Explicitly NOT doing yet

- **No capex.** Sauna / EV charger / pet conversion stay gated — the diagnosis is occupancy and pricing, not a missing amenity. Revisit only if the pricing test runs its course and occupancy is still capped by the listing, and only with full payback math per `CLAUDE.md`.

---

## Baseline for the 90-day kill / double-down gate

Frozen today (2026-07-09) so the intervention can be judged, per the monthly cycle:

| Metric | Baseline (Feb–Jun 2026 actual) |
|---|---|
| Occupancy | ~28% |
| ADR | ~$669 |
| RevPAR (accommodation) | ~$188 |
| Net cash / mo (trailing 11mo) | −$452 |
| Fwd occupancy (PriceLabs pulse) | Jul 35% · Aug 16% · Sep 37% |

**Review date: ~2026-10-09.** Verdict rule: **double down** if RevPAR and net cash have improved; **kill / re-tune** if RevPAR is flat-or-down despite the price changes (→ pivot effort to the listing-conversion lever).
