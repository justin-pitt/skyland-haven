# CLAUDE.md: Skyland Haven Profitability

Read docs/skyland-haven-handoff.md before doing anything. It is the authoritative spec. This is an analysis project, not a software project: the deliverables are diagnosis, payback math, and a monthly scorecard.

## What this is

Short-term rental in Woodfin, NC running at a net loss. Goal: net positive by month 6, +$300/month by month 12. Owner is technical; skip basics, show the math.

## Repo layout

```
skyland-haven/
  data/
    pnl/            # monthly CSVs: revenue, occupancy, ADR, costs
    comps/          # comp set rates and screenshots
  analysis/         # Python scripts or notebooks, reproducible from data/
  docs/
    skyland-haven-handoff.md
    diagnosis.md    # Phase 2 output, one page
    decisions.md    # dated log of pricing/capex decisions
    reports/        # monthly scorecards YYYY-MM.md
```

## Hard rules

- No capex recommendation before docs/diagnosis.md exists and names a primary loss driver (occupancy, rate, cost, or structural) with numbers.
- Every recommendation includes: cost, projected monthly impact, payback months, downside case. Market averages alone are not evidence; tie projections to this property's actuals and the local comp set.
- Zero-cost interventions (pricing, listing copy, photo order, min-stay, gap nights, direct booking page) always rank ahead of capex.
- Any recommendation that adds recurring cost gets flagged explicitly with the new monthly burn.
- If the diagnosis comes back structural, do not keep optimizing. Produce the mid-term rental conversion vs exit comparison instead.
- Data quality first: if a month's P&L inputs are missing or inconsistent, ask for them before analyzing around the gap.

## Analysis conventions

- All analysis reproducible: scripts read from data/, no numbers hardcoded in prose that are not traceable to a script output or a source file.
- State occupancy, ADR, and RevPAR on every scorecard so trends are comparable month to month.
- Cite sources for comp data (listing URLs, screenshot filenames in data/comps/).

## Monthly cycle

1. Owner drops the month's numbers into data/pnl/.
2. Generate docs/reports/YYYY-MM.md: scorecard vs baseline, intervention status, one recommendation maximum.
3. At each intervention's 90-day mark, render a kill or double-down verdict with numbers.
