# Skyland Haven — Loss Diagnosis (Phase 2)

**Date:** 2026-07-09 · **Analyst window:** Aug 2025 – Jun 2026 (11 months; Jul-2025 statement unavailable)
**Data basis:** Revenue = Hospitable host-side accrual (`data/pnl/pnl-12mo-revenue.csv`) + actual Airbnb cash deposits; Costs = Pittnet Properties bank/card statements, Skyland-attributed (`data/pnl/pnl-12mo-costs.csv`, every month reconciled to the penny). Comps = PriceLabs 5BR Woodfin/N-Asheville set (`data/comps/`). Reproduce: `python analysis/build_pnl_combined.py`.

---

## Verdict

> **Primary driver: OCCUPANCY.** Skyland runs at roughly **half the comp-set occupancy** (26–37% vs. 39–62%) while pricing in the **top quartile** of the 5BR market. It is over-priced into a demand hole; the empty nights, not the cost base, are what sink the low-revenue months.
>
> **Secondary driver: a heavy fixed-cost load** (6.375% / ~$473K mortgage + PMI = **$3,726/mo**) that sets a high break-even and leaves **no cushion** in any soft month.
>
> **Not** a rate problem (ADR is *above* comps), **not** an operating-cost problem (opex is lean; cleaning washes), and **not** structural (it clears comfortably at comp-level occupancy — see test below). A third factor, a **2025 co-host taking ~$8K/yr**, is real but **already eliminated** now that you self-manage.

---

## The P&L (trailing 11 months, Skyland only)

| Basis | Revenue | Cost | Net | Per month |
|---|---|---|---|---|
| **Cash** (Airbnb deposits − all cash out incl. mortgage) | $62,444 | $67,418 | **−$4,974** | **−$452** |
| **Economic** (strip out ~$561/mo mortgage *principal* = equity) | $62,444 | $61,247 | **+$1,197** | **+$109** |
| Accrual (Hospitable host-side − cost) | $70,485 | $67,418 | +$3,067 | +$279 |

Read: on the money that actually moves, Skyland **loses ~$450/mo**. Give it credit for the ~$561/mo of principal it's buying you in equity and it's **roughly break-even** — it is *treading water*, not hemorrhaging. But it never clears a return, and it drops into real cash losses every low-occupancy month: **Sep-2025 −$1,618, Jan-2026 −$3,351, Feb-2026 −$1,605**. The profit months are entirely occupancy-led (Oct −$0.7K positive, Dec +$4.9K).

**Why the two revenue rows differ:** in 2025 actual deposits ran ~$8K below accrual — matching the **$8,069 co-host payout to "Asheville Host and Realtor LLC"** on the 2025 Airbnb earnings report. In 2026 (self-managed) deposits and accrual converge (Apr matches to the dollar). So the accrual row flatters 2025; the **cash row is the honest number**.

## Cost structure — lean, and not the problem

Average monthly Skyland cost is **$6,129**, of which the **mortgage is $3,708 (60%)**. Everything else is modest and mostly variable:

- **Cleaning ≈ washes**: paid $14,143 over 11mo vs. **$13,830 cleaning fees collected** — net ~$28/mo. Not a lever.
- **Utilities** average ~$248 power (winter $322–434, summer $160–214) + ~$135 internet + ~$57 water ≈ **$440/mo**.
- **Software/pest/HOA/bookkeeping** ≈ $500/mo, some one-timers ($1,470 HostGPO bulk supplies in Aug, $685 listing photos in Oct).

There is no fat to cut that changes the outcome. **The cost side is fine; the revenue side is short.**

## Why the driver is occupancy (evidence)

| Metric | Skyland | 5BR comp set | Read |
|---|---|---|---|
| ADR (Feb–Jun 2026) | **~$670** | median $422 · 75th pct $639 · 90th $826 | **top quartile — over-priced** |
| Occupancy Mar / Apr / May / Jun 2026 | 22.6 / 36.7 / 29.0 / 26.7% | 49 / 51 / 51 / 62% | **~½ the market** |
| PriceLabs price-vs-market flag | — | — | *"your prices are above the market"* in **high *and* low** season |

The listing is trading occupancy for rate and losing the trade: at ~$670 ADR × ~27% occ ≈ **$181 RevPAR**, versus a market doing ~$422 × ~50% ≈ **$211 RevPAR**. We are leaving nights — and money — on the table to protect a premium the market isn't paying for.

## Structural test (why this is fixable, not an exit case)

At comp-level occupancy (~50%, roughly **double** today) even at a *lower*, market-competitive ADR (~$500), RevPAR rises to ~$250 (+~38%) — about **+$1,500–2,000/mo** in accommodation revenue. That clears the ~$450/mo cash gap **and** the +$300/mo month-12 target with room to spare. The property **can** carry its (heavy) nut at market occupancy → **not structural.** The mid-term-rental / exit conversation is not warranted.

The caveat is the secondary driver: because the mortgage is large and at 6.375% + PMI, break-even occupancy is high (~45%). Skyland has **no margin for error** — it must run near-market occupancy to profit. That is exactly what it is failing to do.

---

## What this licenses for Phase 3 (direction only — not yet recommendations)

- **Zero-cost first, per the rules:** the lever is **pricing/occupancy** — realign ADR toward the market (dynamic pricing) to convert the empty half of the calendar, plus min-stay/gap-night and the winter-trough months (Jan–Mar, Sep) where the losses concentrate. This is the entire ballgame.
- **Capex stays gated.** The diagnosis is occupancy, not amenity/structural — so no sauna/EV/pet-conversion math until a pricing intervention has had its run. Any capex later must still clear the payback bar in `CLAUDE.md`.

## Data caveats

1. **Jul-2025 cost row is blank** (statement not in the export) → 11-month, not 12-month, window.
2. **Cash vs. accrual** gap = 2025 co-host + payout timing (see above); use cash for P&L, accrual for ADR/occupancy trend.
3. **Pre-Feb-2026 occupancy %** denominators are unreliable (Hospitable calendar backfill) — occupancy comparisons above use Feb-2026-onward only.
4. **Unverified line items** (don't change the verdict): Bellastead HOA attribution, Thumbtack, WNC Real Estate Photo, Venmo "marcus." See `data/pnl/costs-README.md`.
