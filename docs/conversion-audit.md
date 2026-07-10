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

## Zero-cost punch list (ranked by impact × ease)

### 1. Reorder the first 5–8 photos to sell *scale* + the *game-room* differentiator — **owner action, $0**
The photos are excellent but **sequenced wrong for a large-group listing.** The two things a group-of-12 booker needs to see fast — *"this is big enough for us"* and *"the game room in the title"* — are missing from the opening frames:

- The **game room** (pool/ping-pong/arcade) is literally in the title but buried at gallery positions **27, 35, 43**.
- The **two living rooms** (the scale shot) sit at **14, 16, 17, 26**.
- Position **3** is a dark top-down **drone aerial** — aerials underperform early and this one makes the house read *small*.
- The **first 3 photos have no captions** (`caption:""`); captions now render on Airbnb and lift click-through.

**Proposed opening order** (current gallery index → new slot, with a benefit caption):

| New slot | Use image (current order) | Caption |
|---|---|---|
| 1 (cover) | Twilight exterior — order **0** | "5BR mountain retreat · 7 min to downtown Asheville" |
| 2 | Hot tub at dusk — order **1** | "Private hot tub under the trees" |
| 3 | Great-room sectional — order **15** (or 13) | "Two living rooms — space for all 12" |
| 4 | Game room table — order **43** (or 34/26) | "Game room: pool, ping-pong & arcade" |
| 5 | Fire pit w/ 8 chairs — order **4** | "Gather around the fire pit" |
| 6 | Deck dining — order **6** / 14 | "Deck dining opening to the woods" |
| 7 | Primary suite — order **17** / 24 | "King primary suite + ensuite" |
| 8 | Drone aerial — order **2** (demoted) | "Wooded lot with fire pit & decks" |

Net effect: exterior → hot tub → **scale** → **differentiator** → group outdoor → dining → bedroom → context. Every one of the first 8 gets a caption.

### 2. Verify and tag the missing search-filter amenities — **owner action, ~$0**
The synced amenity set (`property.json`) is **missing filters this property likely qualifies for.** Each is a search *filter* — being untagged removes the listing from those filtered searches entirely (an impressions loss, not just a conversion one):

- **Self check-in / keypad** — not tagged. The guest guide implies a keypad/lock; the smart-device API is gated on this plan so it can't be confirmed here. **Verify → tag "Self check-in".** High-value filter.
- **Mountain view** — not tagged, yet the hot-tub photo shows a clear valley/ridge view and the description touts mountain views. In an Asheville search, "Mountain view" is both a filter and a draw. **Verify → tag if genuine.**
- **BBQ grill** — absent. Expected on a 12-guest house. **Verify; if present tag it, if not it's a ~$150 one-time add** (flag: trivial one-time, no recurring cost).
- *(EV charger stays gated — that's capex, and the diagnosis is occupancy not a missing amenity. Do not add now.)*

### 3. Front-load capacity in the title — **owner action, $0**
Current: `Spacious w/ Game Room + Hot Tub | Mins to Downtown` (at the 50-char Airbnb limit) — it never says **5BR** or **Sleeps 12**, the single most important qualifier for a large-group searcher scanning results. Test:
> `5BR Sleeps 12 · Game Room · Hot Tub · 7min Asheville`

Keeps the two differentiators, adds capacity, and makes "7 min to Asheville" concrete. A/B against the current title over the 90-day window.

### 4. Clear the hot-tub safety warning — **near-$0 (~$20–50)**
The live listing carries Airbnb's safety disclosure **"Pool/hot tub without a gate or lock."** That banner deters exactly the family segment this house is built for (cribs, high chair, stair gates all present). A **lockable hot-tub cover latch** removes the warning and is a real safety improvement. One-time ~$20–50, no recurring cost.

### 5. Copy hygiene + review responses — **owner action, $0**
- The description still says *"Our local co-host lives close by and is available for anything you might need."* That is **stale** — the co-host was eliminated when you took over self-management (`docs/diagnosis.md`). Replace with a responsive-self-management line; a false "co-host" claim reads as inattentive.
- The 2 Hospitable-visible reviews are **unanswered** (`response:null`, `can_respond:true`). A short host response is a free trust signal and a small ranking nudge. Make review responses part of the messaging routine.

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
