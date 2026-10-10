# Property Management — case 013: Kitchen glazing maintenance request

*PREPARATION ONLY — not official Reality Test results. System-generated; not edited by hand.*

- **Property (as supplied, unverified):** 8 Brackenmere Walk, Vellumbrook, ZZ1 1ZZ
- **Decision cutoff:** 2025-09-10T10:10:00+00:00
- **Runner status:** **settled** · execution `native_local` · sources processed 25 of 25
- **Models:** Claude `claude-opus-5` (triage effort medium); Jev `jev-1.13.0` routing
- **Commit:** `26542cfa3d481aa925490db741aa4fbab8f70e3c` · input SHA-256 `a3727fd63257ef5c…`

All operational tools in this run are clearly labelled **simulated** adapters: no real tenant, landlord or contractor was contacted, nothing was paid or booked, and a simulated receipt does not prove work happened.

## What the system received

The initial report and 24 further sources, submitted one at a time in availability order; each was processed and settled before the next became visible. Full text: `input.json`.

| # | Available at | Source |
|---|---|---|
| 0 | 2025-07-31T08:11:00+00:00 | Initial report — Event 001 — Email |
| 1 | 2025-07-31T08:30:00+00:00 | Event 002 — Email from Tamsin Rook (Property Manager, Northbridge Lettings) |
| 2 | 2025-07-31T09:09:00+00:00 | Event 003 — Email from Tamsin Rook (Property Manager, Northbridge Lettings) |
| 3 | 2025-08-03T09:11:00+00:00 | Event 004 — Email from Tamsin Rook (Property Manager, Northbridge Lettings) |
| 4 | 2025-08-04T11:48:00+00:00 | Event 005 — Note from Tamsin Rook (Property Manager, Northbridge Lettings) |
| 5 | 2025-08-04T12:23:00+00:00 | Event 006 — Email from Tamsin Rook (Property Manager, Northbridge Lettings) |
| 6 | 2025-08-05T12:04:00+00:00 | Event 007 — Email from Tamsin Rook (Property Manager, Northbridge Lettings) |
| 7 | 2025-08-06T09:29:00+00:00 | Event 008 — Email from Tamsin Rook (Property Manager, Northbridge Lettings) |
| 8 | 2025-08-11T10:34:00+00:00 | Event 009 — Email from Tamsin Rook (Property Manager, Northbridge Lettings) |
| 9 | 2025-08-11T11:05:00+00:00 | Event 010 — Email from Orren Vale (Landlord) |
| 10 | 2025-08-11T11:17:00+00:00 | Event 011 — Email from Tamsin Rook (Property Manager, Northbridge Lettings) |
| 11 | 2025-08-11T11:19:00+00:00 | Event 012 — Note from Tamsin Rook (Property Manager, Northbridge Lettings) |
| 12 | 2025-08-11T11:20:00+00:00 | Event 013 — Email from Tamsin Rook (Property Manager, Northbridge Lettings) |
| 13 | 2025-08-11T11:49:00+00:00 | Event 014 — Email from Elowen Marr (Tenant) |
| 14 | 2025-08-11T11:50:00+00:00 | Event 015 — Email from Tamsin Rook (Property Manager, Northbridge Lettings) |
| 15 | 2025-08-14T12:54:00+00:00 | Event 016 — Call from Tamsin Rook (Property Manager, Northbridge Lettings) |
| 16 | 2025-08-19T13:12:00+00:00 | Event 017 — Email from Tamsin Rook (Property Manager, Northbridge Lettings) |
| 17 | 2025-08-24T15:33:00+00:00 | Event 018 — Email from Sella Vane (Contractor, Clearfirth Glazing) |
| 18 | 2025-08-24T15:54:00+00:00 | Event 019 — Email from Tamsin Rook (Property Manager, Northbridge Lettings) |
| 19 | 2025-08-27T16:30:00+00:00 | Event 020 — Email from Tamsin Rook (Property Manager, Northbridge Lettings) |
| 20 | 2025-09-02T10:18:00+00:00 | Event 021 — Call from Tamsin Rook (Property Manager, Northbridge Lettings) |
| 21 | 2025-09-09T09:53:00+00:00 | Event 022 — Note from Tamsin Rook (Property Manager, Northbridge Lettings) |
| 22 | 2025-09-10T09:55:00+00:00 | Event 023 — Document from Tamsin Rook (Property Manager, Northbridge Lettings) |
| 23 | 2025-09-10T10:10:00+00:00 | Event 024 — Update from Tamsin Rook (Property Manager, Northbridge Lettings) |
| 24 | 2025-09-10T10:10:00+00:00 | Attachment glazing-invoice.pdf (PDF text extraction) |

## Final decision — system case `c1a71272813b`

- **Decision (policy outcome):** **HUMAN REVIEW**
- **Proposed next action:** `confirm_appointment` — Kitchen window: misted sealed unit and water around frame (category windows)
- **Next step:** Verify the person, property and work item mapping.
- **Owner:** case manager
- **Case state:** open · policy v1

**Latest reading (claude-opus-5, low confidence, route `confirm_appointment`):** Invoice copy from Clearfirth Glazing for supplying and fitting one pane of glass to the kitchen glazing at 8 Brackenmere Walk, dated 10 September 2025. No amount is shown and there is still no visit report or appointment confirmation.

**Why:** Router chose confirm_appointment; the invoice alone does not evidence completion and no appointment is recorded, so the visit/fitting still needs confirming.

### Actions taken

- **No operational action was executed.** Nothing was booked, instructed, paid or sent. The system recorded readings, claims and policy assessments only.

### Escalated to a person (handover)

| Check | Owner | Rule | What the person must resolve | Evidence |
|---|---|---|---|---|
| `identity` | case manager | `require-identity` | Verify the person, property and work item mapping. | no source recorded |
| `route` | case manager | `require-route` | Verify the recipient and permitted communication route. | no source recorded |
| `access` | access officer | `require-access` | Record consent for this visit and access method from the authorised person. A verified route is required before asking externally. | no source recorded |
| `authority` | approver | `require-authority` | Obtain authority for this work item, provider and action. | no source recorded |
| `schedule` | case manager | `require-schedule` | Confirm the active appointment with a precise date and time. A verified route is required before asking externally. | no source recorded |
| `triage` | case manager | `require-triage` | Clarify before routing: The status change implies a visit occurred, but there is no visit report or completion evidence; confirm whether any attendance actually took place. A verified route is required before asking exte … | Event 022 — Note from Tamsin Rook (Property Manager, Northbridge Lettings) |

### Missing information and conflicting facts

- **completion** (blocks the route): The invoice describes fitting glass but there is no visit report or appointment confirmation; confirm whether the work was actually carried out and on what date.
- **issue_details**: The invoice shows no amount, so the full cost including tax is unknown.
- 5 extracted claim(s) remain **unverified source assertions** (see REASONING.md); none was treated as verified authority.

## Failures

- None recorded. (Jev and Claude calls all returned; no workflow step failed.)

## Result

No approval was invented and no human response was supplied by the runner. The case is waiting on the person(s) listed in the handover above.

Trace: `REASONING.md` (why) · `AUDIT.md` (every step, actor and tool) · `evidence.json` / `records.jsonl` (raw records) · `checkpoint-NNN.json` (state after each source; kept in the local run directory, not published).
