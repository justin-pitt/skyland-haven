# Skyland Haven Profitability: Project Handoff Spec

**Goal:** Take the Woodfin, NC Airbnb from net loss to consistent monthly profit. Diagnose the loss driver first, then deploy capital only against the lever the numbers point to.

**Owner context:** Property is an existing asset with a hot tub, a GitHub Pages guest manual, printable signage, and QR codes already built. Capital available for improvements ($5-10K range) if justified. Owner does not want a new sales/customer motion, so all recommendations must work within Airbnb's existing distribution.

**Claude Project instructions to set:** No capex recommendations until the loss-driver diagnosis is complete. Every recommendation must include payback math against actual P&L numbers, not market averages alone. Flag any recommendation that adds recurring cost.

---

## Phase 1: Data gathering (owner homework)

Pull 12 months of the following, monthly granularity:

Revenue side:
- Gross booking revenue (Airbnb payout reports)
- Nights booked and nights available (occupancy rate)
- Average daily rate by month
- Cleaning fees collected
- Cancellation/refund amounts

Cost side:
- Mortgage or carrying cost allocated to the property
- Utilities (power, water, internet, trash)
- Cleaning cost per turnover and turnovers per month
- Supplies and consumables
- Hot tub maintenance and chemicals
- Repairs and maintenance
- Insurance (STR policy) and property tax
- Airbnb host fee percentage in effect
- Buncombe County occupancy tax handling (remitted by Airbnb or owner)

Market side:
- Listing URL and current photo order
- 5 comparable active listings in Woodfin/North Asheville (similar bed/bath, hot tub)
- Their nightly rates for the next 60 days (owner screenshots or AirDNA free data)

## Phase 2: Diagnosis

Classify the loss into one primary driver:

1. Occupancy problem: occupancy materially below comp set. Levers: pricing strategy, listing quality, photos, amenities, minimum-stay settings, instant book.
2. Rate problem: occupancy fine but ADR below comps. Levers: repricing, amenity-based ADR lift, seasonal pricing.
3. Cost problem: revenue in line with comps but cost structure eats it. Levers: cleaning cost renegotiation, utility audit, insurance requote, refinance question (out of scope for this project, flag only).
4. Structural problem: even at comp-level occupancy and ADR the property cannot clear carrying cost. Different conversation: mid-term rental conversion (travel nurses, Mission Hospital proximity), or exit analysis.

Deliverable: one-page diagnosis with the numbers, stating the primary and secondary driver.

## Phase 3: Interventions, gated by diagnosis

Zero-cost first, regardless of driver:
- Dynamic pricing: PriceLabs or Wheelhouse trial, or manual seasonal repricing against comp calendar.
- Listing copy rewrite and photo reorder (first 5 photos drive click-through).
- Review response templates and automated guest messaging flows.
- Minimum-stay and gap-night optimization.
- Direct booking page on the existing GitHub Pages site for repeat guests, cutting the Airbnb fee on returns.

Capex, only if diagnosis supports it:
- Sauna ($4-8K): ADR lift play. Justify with comp-set ADR delta for sauna listings in the Asheville market.
- EV charger ($1-2K): search filter unlock. Occupancy play.
- Pet-friendly conversion (minimal cost, higher cleaning/wear): booking pool expansion. Occupancy play.
- Each requires: cost, projected monthly impact, payback months, and downside case.

## Phase 4: Tracking

Monthly scorecard in the project: occupancy, ADR, RevPAR, total cost, net. Compare against the diagnosis baseline. Kill or double down on interventions at 90 days.

## Success metric

Net positive by month 6, +$300/month or better by month 12. If Phase 2 returns a structural problem, success is redefined as a decision (convert to mid-term or exit) backed by numbers, not continued bleeding.
