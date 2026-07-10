# Skyland Haven — Listing Conversion Audit

**Date:** 2026-07-10 · **Analyst window:** live listing state as of today
**Purpose:** The pricing intervention (`docs/interventions.md`) assumes the base price is already market-correct (PriceLabs base $521 ≈ recommended $522) yet occupancy trails the market by 13–18 pts. That points at **conversion** — whether searchers who see the listing actually book — as the co-primary suspect. This audit tests that hypothesis at zero cost.
**Data basis:** Hospitable API (`analysis/fetch_listing_content.py` → `data/raw/hospitable/{property,images,reviews}.json`) + live Airbnb page signals captured 2026-07-10 (`airbnb.com/rooms/907933203969939408`; JSON-LD, browser UA). PriceLabs Listing Optimizer (search-rank data) is **not on this account** — see gap below.

---

## Headline: the listing is already strong on every measurable conversion signal

The "conversion is the constraint" hypothesis is **largely NOT supported.** Everything Airbnb rewards for click-through and booking is already in place:

| Signal | Skyland (live, 2026-07-10) | Read |
|---|---|---|
| Review count | **101 reviews** | strong social proof (Hospitable only stores 2 post-connection — the public count is what matters) |
| Overall rating | **4.97 ★** | top-tier |
| Superhost | **Yes** | trust + ranking boost |
| Instant Book | **On** | max conversion + ranking |
| Capacity in data | Sleeps 12 · 5BR/3BA | matches the group-house search |
| Photos | 56, professional, twilight exteriors, styled interiors | high production quality (re-shot/re-uploaded Feb 2026) |
| Amenities | hot tub, game room, pet-friendly, cribs/high-chair/stair-gates, free parking, AC, W/D | well-stocked, family-ready |

**Conclusion:** listing quality is a *strength*, not the leak. That is itself the valuable finding — it **rules out the main alternative to the pricing thesis** and raises confidence that the live pricing intervention is aimed at the right lever. The residual occupancy gap is most plausibly **(a) search visibility/ranking** (which we cannot measure — see gap), **(b) the genuinely softer YoY market** (already priced into the conservative half-the-gap target), and **(c) price competitiveness on the margin** — i.e. it loops back to the pricing test already running.

The zero-cost conversion improvements below are still worth doing — they are cheap, they can only help, and a couple unlock **search filters (impressions)**, which is the more likely lever. But none is a smoking gun that overturns the pricing diagnosis.

---

## Zero-cost punch list — reviewed with owner 2026-07-10

Most candidate items were **checked with the owner and dismissed with cause** — which reinforces the headline that the listing is already well-optimized. Only copy hygiene + review-reply automation survive.

| # | Candidate | Verdict (owner, 2026-07-10) |
|---|---|---|
| 1 | Reorder first 5–8 photos (lead with scale + game room; demote drone aerial; add captions) | **Declined — leave as is.** Photos were arranged by the previous property manager, look good on Airbnb, and the listing converts (4.97★/101). Not worth disturbing now. |
| 2a | Tag **Self check-in** | **Already covered.** Property has a **Schlage keypad auto-updated by Airbnb**; there is no separate Airbnb amenity toggle to add. Self-check-in searchers are already served. |
| 2b | Tag **Mountain view** | **N/A — no mountain view.** Don't tag (false amenity). |
| 2c | Add/tag **BBQ grill** | **N/A — no grill.** Not adding. |
| 3 | Front-load "5BR · Sleeps 12" in title | **Not needed.** Airbnb already shows "12 guests" on the listing and surfaces it in the 12-guest capacity filter; the title slot is better spent on the game-room + hot-tub differentiators it already carries. |
| 4 | Clear "hot tub without a gate or lock" safety banner | **Effectively satisfied.** Hot tub has a **cover** and is enclosed by the **patio railings**. Low priority; owner may update the Airbnb safety-features answer if the banner persists, but no hardware needed. |
| 5 | Copy hygiene + review replies | **Kept — see below.** |

### 5 (kept). Copy hygiene + automate review replies — **owner action, $0**
- The description still says *"Our local co-host lives close by and is available for anything you might need."* That is **stale** — the co-host was eliminated when you took over self-management (`docs/diagnosis.md`). Replace with a responsive-self-management line; a false "co-host" claim reads as inattentive.
- The 2 Hospitable-visible reviews are **unanswered** (`response:null`, `can_respond:true`). Hospitable can **AI-draft the reply automatically** when a new review lands (Airbnb/Booking.com); by default it's a draft you approve/edit/send, within a 30-day window — so this becomes near-hands-off going forward. Separately, the account has **7 inactive "Review" rules** (`event:review`, "send 3 days after checkout") that auto-**leave reviews of guests** — activating one drives review reciprocity (guest reviewed → more likely to review you), which helps review velocity. Neither is on today.

---

## Measurement gap (flag, don't reflexively buy)

Whether the real leak is **search ranking/visibility** rather than per-view conversion **cannot be measured from this account.** PriceLabs' **Listing Optimizer** (search-rank by guest-count/LOS, page position, neighborhood KNN) returns *"not available for this account"* — it's a paid PriceLabs add-on. Before subscribing, the 90-day pricing gate should run: if RevPAR lifts on the price changes, ranking was not the binding constraint and the add-on isn't needed. Revisit only if the pricing test comes back flat.

## What this means for the 90-day gate (~2026-10-09)

This audit does **not** trigger a pivot away from pricing. It removes listing quality as the likely culprit, so the pricing intervention keeps its status as the primary lever. Fold the punch-list items in as cheap parallel improvements and note them on the monthly scorecard's "Listing-conversion audit" row. The kill/double-down verdict still rests on **RevPAR vs the frozen baseline.**

## Reproduce

```
python analysis/fetch_listing_content.py   # → data/raw/hospitable/{property,images,reviews}.json
```
Live Airbnb public signals (101 reviews · 4.97★ · Superhost · Instant Book · sleeps 12) were read from `airbnb.com/rooms/907933203969939408` on 2026-07-10 (Airbnb blocks unauthenticated fetches; a browser user-agent returns the embedded JSON-LD).
