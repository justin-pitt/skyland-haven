<!-- Handoff prompt for the 2026-08-01 session (first monthly scorecard). Paste the block
     below as the session opener. Delete this file once 2026-07.md is produced. -->

# Next-session handoff — 2026-08-01 (first monthly scorecard)

```
You're in C:\Code\skyland-haven — the Skyland Haven profitability project (5BR Airbnb,
Woodfin/Asheville NC). Read CLAUDE.md and docs/skyland-haven-handoff.md first; the handoff
is authoritative. Honor the hard rules: zero-cost levers before capex; all analysis
reproducible from data/; flag any new recurring cost; and if a monthly P&L input is
missing or inconsistent, ASK before analyzing around it.

State as of 2026-08-01 (branch main, PRs #2–#6 merged):
- Phases 1–3 done. Diagnosis (docs/diagnosis.md): loss is OCCUPANCY-driven — occupancy ran
  ~half the comp set (26–37% vs 39–62%) while ADR sat top-quartile (~$669 vs $422 median).
  Ruled out rate, opex-cost, structural. Trailing-11mo cash P&L −$4,974 (−$452/mo).
- Conversion audit done (docs/conversion-audit.md): conversion is NOT the leak. Live listing
  is strong on every signal — 101 reviews / 4.97★ / Superhost / Instant Book / sleeps 12 /
  pro photos. This RULED OUT listing quality and STRENGTHENED the pricing thesis. Review
  automation now live (7 guest-review rotation rules active; AI review replies via Inbox;
  stale co-host description line fixed in Airbnb).
- Live intervention: PriceLabs Max Price raised $750→$1,050 on 2026-07-10. Baseline frozen
  (Feb–Jun 2026): occ ~28% · ADR ~$669 · RevPAR ~$188 · net cash −$452/mo. 90-day
  kill/double-down gate ~2026-10-09, judged on RevPAR vs baseline (docs/decisions.md).
- Pricing settings still likely UNAPPLIED (verify with owner): pricelabs-settings.md steps
  4–6 — low-end aggressiveness, last-minute discounts (0–3 day), orphan-gap min-stay. Only
  the max-price raise is confirmed live.

PRIMARY TASK THIS SESSION — first monthly scorecard (July 2026), per docs/CLAUDE.md monthly
cycle and docs/reports/_scorecard-template.md (copy to docs/reports/2026-07.md, don't edit
the template):
1. Refresh revenue: python analysis/fetch_hospitable.py && python analysis/build_pnl.py
2. Add July's cost row to data/pnl/pnl-12mo-costs.csv from the Pittnet Properties
   checking + credit statements (~/OneDrive/Documents/accounting/pittnet-properties-*.pdf;
   attribution rule + reconcile-to-statement in data/pnl/costs-README.md). If the July
   statements aren't available yet, ASK — don't estimate.
3. Rebuild P&L: python analysis/build_pnl_combined.py → read July's row + TOTAL from
   pnl-combined.csv.
4. Pull live occupancy vs market from the PriceLabs pulse
   (get_listing_health_and_recommendations) and the neighbourhood data.
5. Fill the scorecard: occupancy, ADR, RevPAR, total cost, net cash, all vs the frozen
   baseline. Note July is a PARTIAL-effect month (intervention started 2026-07-10), so read
   it as an early signal, not the verdict — watch peak-weekend RevPAR first (fastest signal
   from a cap raise). One recommendation max.

Secondary (only if time / owner wants):
- Help apply/verify PriceLabs settings steps 4–6 if still not live.
- Named comps (checklist item 16): enable a PriceLabs Market Dashboard compset or manual
  Airbnb incognito pull. Skip AirDNA.
- Direct-booking angle (existing 'direct' channel + GitHub Pages site) to cut the 15.5%
  Airbnb fee on repeat guests.

Git: Bash cwd resets to C:\Code (dubious-ownership repo) — run git as git -C /c/Code/
skyland-haven .... Never commit to main; feature branch + PR, no Claude attribution.
```
