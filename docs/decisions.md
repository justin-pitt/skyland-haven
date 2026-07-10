# Skyland Haven — Decision Log

Dated log of pricing and capex decisions. Newest first.

---

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
