<!-- Handoff prompt for the next session. Paste the block below as the session opener.
     Delete this file once 2026-08.md is produced. -->

# Next-session handoff — 2026-09-01 (August scorecard)

```
You're in C:\Code\skyland-haven — the Skyland Haven profitability project (5BR Airbnb,
Woodfin/Asheville NC). Read CLAUDE.md and docs/skyland-haven-handoff.md first; the handoff
is authoritative. Honor the hard rules: zero-cost levers before capex; all analysis
reproducible from data/; flag any new recurring cost; and if a monthly P&L input is
missing or inconsistent, ASK before analyzing around it.

State as of 2026-08-19 (branch main; July scorecard merged):

- Diagnosis unchanged and reinforced: the loss is OCCUPANCY-driven (docs/diagnosis.md).
  Conversion was ruled out as the leak (docs/conversion-audit.md).
- THE BIG ONE (docs/reports/2026-07.md, docs/decisions.md 2026-08-19): the pricing
  intervention logged as executed on 2026-07-10 was NEVER LIVE. PriceLabs max price is
  still $750, not $1,050. The 2026-10-09 gate is void; the 90-day clock restarts from the
  date the settings are verified. Every "executed" decision-log entry must now record a
  read-back verification, not just the intended change.
- July 2026 revenue was strong (occ 35.5%, ADR $868.45, RevPAR $308.16 vs baseline
  28.0% / $669.35 / $187.00) but measures NOTHING about the intervention: all 11 July
  nights were booked 2026-01-21 .. 2026-06-11, all pre-change.
- Forward pace is the real problem: 23 of the remaining 135 nights of 2026 on the books vs
  48 at the same point last year (Oct 19% vs 58%, Dec 13% vs 48%). PriceLabs pulse Red:
  0/10/17% occupancy next 7/30/60 days vs market 43/37/36%.
- Leading (UNPROVEN) hypothesis: the 4-5 night minimum stay now enforced across Oct-Dec,
  against a comp set whose median booked stay is 3 nights. Confirm in PriceLabs settings
  before acting.

OPEN ITEMS CARRIED IN — resolve these first:
1. JULY 2026 COST ROW IS STILL BLANK if the statements had not arrived. Check
   ~/OneDrive/Documents/accounting/pittnet-properties-{checking,credit}-JUL-2026.pdf. If
   present, fill data/pnl/pnl-12mo-costs.csv (attribution rule + reconcile-to-statement in
   data/pnl/costs-README.md), rerun python analysis/build_pnl_combined.py, and backfill the
   pending cells in docs/reports/2026-07.md. If still absent, ASK — do not estimate.
2. Did the owner apply + VERIFY max price $1,050? Read it back with PriceLabs
   get_listing_data and confirm max: 1050 before crediting it. Log the read-back value.
3. Were the Oct-Dec min-stays confirmed/changed? One variable at a time.

PRIMARY TASK — August scorecard (docs/reports/_scorecard-template.md -> 2026-08.md):
1. Roll the window: bump WINDOW_START/WINDOW_END one month in analysis/build_pnl.py and
   analysis/fetch_hospitable.py (now 2025-08..2026-07 -> 2025-09..2026-08).
2. python analysis/fetch_hospitable.py && python analysis/build_pnl.py
3. Add August's cost row (and July's, if it landed) to data/pnl/pnl-12mo-costs.csv.
4. python analysis/build_pnl_combined.py
5. Fresh PriceLabs pull -> transcribe to data/raw/pricelabs/forward_prices_<DATE>.csv
   (format + provenance in that directory's README), update the MIN_PRICE/MAX_PRICE
   constants in analysis/build_forward_pace.py to the values get_listing_data returns,
   then python analysis/build_forward_pace.py.
6. Refresh the market history pull — data/comps/market-history-24mo.csv currently ends
   Jun 2026, so there is no market occupancy figure to compare recent months against.
7. Fill the scorecard. One recommendation maximum. Judge on RevPAR AND pace vs STLY, not
   ADR alone — ADR is what looked good in July while pace was collapsing.

Git: Bash cwd resets to C:\Code (dubious-ownership repo) — run git as
git -C /c/Code/skyland-haven .... Never commit to main; feature branch + PR, no Claude
attribution.
```
