# data/pnl/pnl-12mo-costs.csv — Skyland cost side

Monthly Skyland-attributed operating costs, extracted from the **Pittnet Properties**
business account (Navy Federal Credit Union, access no. on file). One row per month,
aligned to the revenue CSV window (2025-08 .. 2026-07).

All dollar figures are **actual cash outlays** transcribed from the monthly checking +
credit-card statements. Every month was reconciled line-by-line to the statement's own
total-debits / total-new-charges figure (exact match, $0.00 variance) before entry.

## Source documents (NOT committed — PII)

Raw statements live in `~/OneDrive/Documents/accounting/pittnet-properties-{checking,credit}-<MON>-<YEAR>.pdf`
and the Movement Mortgage statements `skyland-statement-<MON>-<YEAR>.pdf`. They contain
account numbers, addresses, and third-party names; **this repo is public, so they are not
committed.** Figures below are the PII-free extraction. Regenerate by re-reading those
statements and re-applying the attribution rules in this file.

## Attribution rule (owner-confirmed 2026-07-09)

The Pittnet Properties account is **commingled** across two properties: **Skyland** (the
short-term/Airbnb rental this analysis covers) and a **long-term rental (LTR)** whose
mortgage is serviced by Pennymac. Owner confirmed:

- **Movement mortgage** (`Movement Mtg Pmt`, ~$3,688 in 2025 / $3,725.68 in 2026) = **Skyland**. Kept.
- **All utilities** (Duke Energy = power, Spectrum = internet, Woodfin Sanitary = water/sewer) = **Skyland** — the LTR tenant pays their own utilities. Kept.
- **Pennymac mortgage** (~$1,358/mo) = **LTR**. Excluded.
- **"United FCU Statesville" deposits** (~$1,250–1,460) = **LTR cash rent**. Excluded (not Skyland revenue).
- `Transfer To Credit Card`, inter-account transfers, and owner capital injections = internal money movement. Excluded (the card's own charges are itemized separately, so counting the transfer too would double-count).

## Columns

| column | meaning |
|---|---|
| `mortgage_piti` | Movement mortgage debit (principal + interest + escrow). $3,687.96 through Dec-2025, $3,725.68 from Jan-2026 (escrow reset at the 2026 escrow analysis). |
| `mortgage_principal_est` | Est. principal portion of PITI (~$561/mo, from the Movement statement: $3,725.68 = $561.43 P + $2,514.25 I + $650.00 escrow). Used to compute the *economic* P&L, since principal is equity build, not an expense. Escrow (tax+insurance+PMI) is inside `mortgage_piti`, not broken out. |
| `power` | Duke Energy. Strongly seasonal (winter $322–434, summer $160–214). |
| `internet` | Spectrum ($129.99 in 2025, $140.00 in 2026). |
| `water` | Woodfin Sanitary (water/sewer). Billed irregularly (~every other month). |
| `cleaning` | 5StrClean turnover cleaning (sum of all 5StrClean charges hitting that month across checking + card). |
| `pest` | Pestmaster ($40/mo). |
| `hoa` | Bellastead HOA. **See caveat #3.** |
| `accounting` | R&T Accounting bookkeeping (irregular, $225–450). |
| `software` | Hospitable + PriceLabs + Intuit QuickBooks + Google Workspace + OpenAI/ChatGPT. |
| `supplies` | Bulk consumables/furnishings (HostGPO $1,470.19 in Aug-2025 — one-time). |
| `other` | Misc/ambiguous: Thumbtack, WNC Real Estate Photo, Venmo (handyman), NSF fees. **See caveat #4.** |
| `skyland_cost_total` | Sum of all Skyland cost columns = total cash out attributable to Skyland that month. |
| `airbnb_deposits_cash` | **Revenue, not cost.** Actual Airbnb payout deposits into the account that month (ground-truth cash). Differs from the accrual revenue in `pnl-12mo-revenue.csv` — see caveat #2. |

## Caveats (read before using)

1. **2026-07 is missing (open).** The July-2026 checking and credit statements are not
   yet in `~/OneDrive/Documents/accounting/` (latest is JUN-2026), so the row is blank and
   July net cash is not computed — see `docs/reports/2026-07.md`. Per `CLAUDE.md` no
   estimate has been substituted. Fill this row when the statements land.
   *(The previously-missing 2025-07 row dropped out of the window when it rolled forward on
   2026-08-19, so the trailing-year totals in `docs/diagnosis.md` remain an 11-month window
   — Aug-2025 .. Jun-2026 — until the July-2026 row is filled.)*
2. **Cash deposits ≠ accrual revenue.** `airbnb_deposits_cash` (what actually landed in
   the bank) runs materially **below** the Hospitable host-side accrual in
   `pnl-12mo-revenue.csv` during 2025 — e.g. Aug-2025 banked $4,125 vs. $7,339 accrual.
   The gap tracks the **~$8,069 co-host payout to "Asheville Host and Realtor LLC"** on
   the 2025 Airbnb earnings report plus payout timing. In 2026 (owner self-managing) the
   two agree (Apr-2026 matches to the dollar). Use **cash deposits** for the "is it losing
   money" P&L; use **accrual** for ADR/occupancy/RevPAR trend.
3. **Bellastead HOA is unverified.** First appears Mar-2026 ($459.02, then $275, $154.50).
   Attributed to Skyland by default; owner to confirm it isn't the LTR's HOA.
4. **`other` holds one-time / ambiguous items** to confirm: Thumbtack ($169.12 ×1 Feb, ×2 Mar —
   handyman lead-gen or advertising?), WNC Real Estate Photo ($685.07 Oct — listing photos vs.
   the owner's separate realtor business?), Venmo "marcus" ($50 Aug & Jun — recurring handyman?),
   and two $29 NSF fees (Apr). `supplies` HostGPO ($1,470 Aug) is a one-time bulk buy. None
   change the diagnosis, but they inflate individual months.
5. **Cleaning ≈ washes.** Cleaning paid ($14,143 over 11 mo) ≈ cleaning fees collected in
   revenue ($13,830). Cleaning is not a loss driver. **Hot-tub service is included in the
   cleaning fee** (owner-confirmed 2026-07-10, 5StrClean services it per turnover) — there is
   no separate hot-tub cost line.
