# Property Management — case 024: End-of-occupancy property service request

*PREPARATION ONLY — not official Reality Test results. System-generated; not edited by hand.*

- **Property (as supplied, unverified):** 7 Brackenmere Walk, Vellumford, ZZ1 1ZZ
- **Decision cutoff:** 2025-09-24T16:11:00+00:00
- **Runner status:** **settled** · execution `native_local` · sources processed 23 of 23
- **Models:** Claude `claude-opus-5` (triage effort medium); Jev `jev-1.13.0` routing
- **Commit:** `26542cfa3d481aa925490db741aa4fbab8f70e3c` · input SHA-256 `e2120c251b90bb95…`

All operational tools in this run are clearly labelled **simulated** adapters: no real tenant, landlord or contractor was contacted, nothing was paid or booked, and a simulated receipt does not prove work happened.

## What the system received

The initial report and 22 further sources, submitted one at a time in availability order; each was processed and settled before the next became visible. Full text: `input.json`.

| # | Available at | Source |
|---|---|---|
| 0 | 2025-09-04T09:01:00+00:00 | Initial report — Event 001 — Portal |
| 1 | 2025-09-04T09:18:00+00:00 | Event 002 — Note from Elowen Pryce (Property Manager, Northbridge Lettings) |
| 2 | 2025-09-04T10:05:00+00:00 | Event 003 — Email from Elowen Pryce (Property Manager, Northbridge Lettings) |
| 3 | 2025-09-04T10:14:00+00:00 | Event 004 — Email from Elowen Pryce (Property Manager, Northbridge Lettings) |
| 4 | 2025-09-04T10:30:00+00:00 | Event 005 — Update from Northbridge Lettings workflow (System) |
| 5 | 2025-09-07T10:00:00+00:00 | Event 006 — Email from Elowen Pryce (Property Manager, Northbridge Lettings) |
| 6 | 2025-09-08T11:03:00+00:00 | Event 007 — Email from Perrin Holt (Contractor, Larkspan Property Care) |
| 7 | 2025-09-09T07:16:00+00:00 | Event 008 — Email from Perrin Holt (Contractor, Larkspan Property Care) |
| 8 | 2025-09-09T11:47:00+00:00 | Event 009 — Email from Elowen Pryce (Property Manager, Northbridge Lettings) |
| 9 | 2025-09-09T11:53:00+00:00 | Event 010 — Call from Elowen Pryce (Property Manager, Northbridge Lettings) |
| 10 | 2025-09-09T21:23:00+00:00 | Event 011 — Email from Perrin Holt (Contractor, Larkspan Property Care) |
| 11 | 2025-09-09T21:35:00+00:00 | Event 012 — Note from Elowen Pryce (Property Manager, Northbridge Lettings) |
| 12 | 2025-09-09T21:40:00+00:00 | Event 013 — Update from Northbridge Lettings workflow (System) |
| 13 | 2025-09-10T08:15:00+00:00 | Event 014 — Note from Elowen Pryce (Property Manager, Northbridge Lettings) |
| 14 | 2025-09-10T11:18:00+00:00 | Event 015 — Note from Elowen Pryce (Property Manager, Northbridge Lettings) |
| 15 | 2025-09-14T15:48:00+00:00 | Event 016 — Update from Northbridge Lettings workflow (System) |
| 16 | 2025-09-18T14:20:00+00:00 | Event 017 — Update from Northbridge Lettings workflow (System) |
| 17 | 2025-09-18T14:21:00+00:00 | Event 018 — Email from Elowen Pryce (Property Manager, Northbridge Lettings) |
| 18 | 2025-09-21T14:21:00+00:00 | Event 019 — Email from Elowen Pryce (Property Manager, Northbridge Lettings) |
| 19 | 2025-09-23T16:11:00+00:00 | Event 020 — Note from Elowen Pryce (Property Manager, Northbridge Lettings) |
| 20 | 2025-09-24T16:11:00+00:00 | Event 021 — Update from Northbridge Lettings workflow (System) |
| 21 | 2025-09-24T16:11:00+00:00 | Attachment checkout-report.pdf (PDF text extraction) |
| 22 | 2025-09-24T16:11:00+00:00 | Attachment property-service-quotation.pdf (PDF text extraction) |

## Final decision — system case `b3ea16b25aa6`

- **Decision (policy outcome):** **HUMAN REVIEW**
- **Proposed next action:** `close_item` — Move-out clearance of left items and final property-preparation service (category checkout_cleaning)
- **Next step:** Verify the person, property and work item mapping.
- **Owner:** case manager
- **Case state:** open · policy v1

**Latest reading (claude-opus-5, medium confidence, route `close_item`):** Contractor quotation document from Larkspan Property Care for the end-of-occupancy service at 7 Brackenmere Walk, totalling £216.00 including VAT (£180 plus £36 VAT). It sets out the included service scope only; it contains no confirmation that work was completed.

**Why:** Router set close_item for the current case; the message is a supporting quotation document confirming the £216 total, with no completion evidence.

### Actions taken

- **No operational action was executed.** Nothing was booked, instructed, paid or sent. The system recorded readings, claims and policy assessments only.

### Escalated to a person (handover)

| Check | Owner | Rule | What the person must resolve | Evidence |
|---|---|---|---|---|
| `identity` | case manager | `require-identity` | Verify the person, property and work item mapping. | no source recorded |
| `completion` | reviewer | `require-completion` | Verify completion of this work item with usable evidence. A verified route is required before asking externally. | Event 020 — Note from Elowen Pryce (Property Manager, Northbridge Lettings) |
| `commitments` | case manager | `require-commitments` | Resolve or explicitly cancel every outstanding commitment for this item. A verified route is required before asking externally. | no source recorded |
| `triage` | case manager | `require-triage` | Clarify before routing: No usable completion evidence is supplied; the only record is an internal note that work was done. Confirm completion with the contractor before closing. A verified route is required before asking … | Event 021 — Update from Northbridge Lettings workflow (System) |

### Missing information and conflicting facts

- **completion** (blocks the route): The quotation evidences price and scope only; there is still no evidence that the clearance and final preparation were completed.
- **issue_details**: The quotation covers the cleaning service but does not mention removal of the listed left items; confirm whether clearance is included in the £216.
- 8 extracted claim(s) remain **unverified source assertions** (see REASONING.md); none was treated as verified authority.

## Failures

- None recorded. (Jev and Claude calls all returned; no workflow step failed.)

## Result

No approval was invented and no human response was supplied by the runner. The case is waiting on the person(s) listed in the handover above.

Trace: `REASONING.md` (why) · `AUDIT.md` (every step, actor and tool) · `evidence.json` / `records.jsonl` (raw records) · `checkpoint-NNN.json` (state after each source; kept in the local run directory, not published).
