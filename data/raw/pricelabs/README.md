# data/raw/pricelabs/ — PriceLabs pulls

Market and own-listing pricing data from PriceLabs. **No guest PII**, so unlike
`data/raw/hospitable/` this directory is committed as comp/pricing evidence.

## Why these are transcribed rather than fetched by a script

PriceLabs' free tier gives **MCP access only** — the REST API is a paid add-on
(see `.env.example`). So there is no `fetch_pricelabs.py` equivalent to
`fetch_hospitable.py`: the data arrives through the MCP tools in a session and is
written here so downstream analysis is reproducible from the repo.

When refreshing, pull with the same tools and overwrite/date-stamp a new file:

| File | Source tool |
|---|---|
| `forward_prices_<DATE>.csv` | `get_listing_prices` (date_from/date_to) |
| `listing_prices_60d.json` | `get_listing_prices`, earlier pull |
| `neighbourhood_detail.json` | `get_neighbourhood_data` |

Listing-level settings (`min` / `base` / `max`) come from `get_listing_data` and are
**not** in these files — they are recorded in the scorecard and mirrored as constants
in `analysis/build_forward_pace.py`. Update those constants whenever a new price pull
is transcribed, or the clamp math is wrong.

## forward_prices_<DATE>.csv columns

Straight from the `get_listing_prices` payload, one row per night.

| column | meaning |
|---|---|
| `price` | rate PriceLabs actually pushes, **after** the listing min/max clamp |
| `user_price` | rate including any manual customization; `-1` on booked nights |
| `uncustomized_price` | what the PriceLabs model wants **before** the clamp. `uncustomized_price > max` means the ceiling is binding and costing money; `< min` means the floor is blocking a discount. |
| `min_stay` | minimum nights enforced for that date |
| `booking_status` / `booking_status_STLY` | booked state now vs the same point last year — the pace comparison |
| `ADR` / `ADR_STLY` | realized nightly rate on booked nights, this year vs last |
| `booked_date` | when a booked night was sold — use this to test whether a stay predates an intervention |
| `demand_desc` | PriceLabs demand band for the date |

## Pull log

- **2026-08-19** — `forward_prices_2026-08-19.csv`, 135 nights (2026-08-19 .. 2026-12-31).
  Listing settings at pull: **min $332 / base $510 / max $750**. This pull is what surfaced
  the finding that the logged 2026-07-10 max-price raise to $1,050 was never applied
  (`docs/decisions.md`, 2026-08-19).
