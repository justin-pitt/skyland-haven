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

**Current PriceLabs settings (pulled 2026-07-09):** min **$350** · base **$521** · max **$750**; PriceLabs' *recommended* base is **$522** — i.e. **the base is right, don't cut it.** Occupancy still trails across every window (next-7 43% vs 57% market · next-30 33% vs 51% · next-60 27% vs 40%). So the moves are about the *cap*, the *curve*, and *conversion* — not the base level:

1. **Raise the $750 max-price cap** → ~**$1,000–1,100**. This is the highest-confidence, zero-risk win. Peak nights command a market 90th percentile of **$900–1,100** and the property *historically booked $858–935* on those dates (`own_booked_adr`), yet the cap chokes them at $750 — **$150–350/peak-night left on the table**. PriceLabs only prices up when demand supports it, so raising the ceiling has no occupancy cost.
2. **Let soft nights ride lower via aggressiveness, not the base.** Unbooked far-out and low-demand mid-week nights stall near **$500** when the median is ~$400 (e.g. 2026-07-19: our **$504** vs **$401 median**, empty). The **$350 floor already allows** deeper discounting — increase pricing aggressiveness / steepen the occupancy-based curve so low-occupancy dates slide toward **$350–420** as they approach.
3. **Aggressive last-minute pricing.** In peak season bookings arrive **0–2 days before stay** (PriceLabs pulse). Turn on/steepen last-minute discounts inside the 0–3 day window so unsold near-term nights clear instead of expiring empty.
4. **Loosen min-stay on orphan gaps.** Min-stay is **2 nights everywhere**; allow 1-night fills for orphan gaps in soft mid-week periods.

Step-by-step settings (current → target, where to click) are in `docs/pricelabs-settings.md`.

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

## Parallel zero-cost check — listing conversion (now co-primary, not just supporting)

The live settings sharpen this: PriceLabs says the **base price is already market-correct** ($521 vs recommended $522), yet occupancy still trails the market by 13–18 points. When price is right and bookings still don't come, the suspect is **conversion** — how many searchers who see the listing actually book. So this is not a side quest; audit the funnel at zero cost: first-5-photo order, title/summary, **review score and count**, amenity tags/search filters, and instant-book. If conversion is the true constraint, no amount of price-tuning fixes it — which is exactly what the 90-day gate is designed to reveal. Findings feed the next scorecard.

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
