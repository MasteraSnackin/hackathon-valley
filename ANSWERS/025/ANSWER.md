# Property Management — case 025: Kitchen tap maintenance request

*PREPARATION ONLY — not official Reality Test results. System-generated; not edited by hand.*

- **Property (as supplied, unverified):** 18 Thistlewick Row, Fenmere, ZZ1 1ZZ
- **Decision cutoff:** 2025-09-15T11:11:18+00:00
- **Runner status:** **settled** · execution `native_local` · sources processed 23 of 23
- **Models:** Claude `claude-opus-5` (triage effort medium); Jev `jev-1.13.0` routing
- **Commit:** `26542cfa3d481aa925490db741aa4fbab8f70e3c` · input SHA-256 `7ec08748e429981a…`

All operational tools in this run are clearly labelled **simulated** adapters: no real tenant, landlord or contractor was contacted, nothing was paid or booked, and a simulated receipt does not prove work happened.

## What the system received

The initial report and 22 further sources, submitted one at a time in availability order; each was processed and settled before the next became visible. Full text: `input.json`.

| # | Available at | Source |
|---|---|---|
| 0 | 2025-08-04T18:10:50+00:00 | Initial report — Event 001 — Portal |
| 1 | 2025-08-05T07:33:17+00:00 | Event 002 — Email from Tessa Wren (Property Manager, Northbridge Lettings) |
| 2 | 2025-08-05T08:52:24+00:00 | Event 003 — Email from Orin Bell (Landlord) |
| 3 | 2025-08-05T09:30:38+00:00 | Event 004 — Email from Tessa Wren (Property Manager, Northbridge Lettings) |
| 4 | 2025-08-06T09:30:26+00:00 | Event 005 — Email from Tessa Wren (Property Manager, Northbridge Lettings) |
| 5 | 2025-08-07T09:54:37+00:00 | Event 006 — Email from Tessa Wren (Property Manager, Northbridge Lettings) |
| 6 | 2025-08-07T12:01:14+00:00 | Event 007 — Email from Nia Calder (Tenant) |
| 7 | 2025-08-07T13:05:43+00:00 | Event 008 — Email from Tessa Wren (Property Manager, Northbridge Lettings) |
| 8 | 2025-08-12T12:41:48+00:00 | Event 009 — Email from Tessa Wren (Property Manager, Northbridge Lettings) |
| 9 | 2025-08-12T18:55:02+00:00 | Event 010 — Email from Nia Calder (Tenant) |
| 10 | 2025-08-12T18:56:42+00:00 | Event 011 — Email from Tessa Wren (Property Manager, Northbridge Lettings) |
| 11 | 2025-09-05T19:40:02+00:00 | Event 012 — Email from Nia Calder (Tenant) |
| 12 | 2025-09-07T09:50:37+00:00 | Event 013 — Call from Tessa Wren (Property Manager, Northbridge Lettings) |
| 13 | 2025-09-09T08:02:07+00:00 | Event 014 — Email from Ivo Fenlock (Contractor, Bracken & Vale Plumbing) |
| 14 | 2025-09-09T16:39:08+00:00 | Event 015 — Email from Nia Calder (Tenant) |
| 15 | 2025-09-09T17:09:49+00:00 | Event 016 — Email from Tessa Wren (Property Manager, Northbridge Lettings) |
| 16 | 2025-09-10T06:06:05+00:00 | Event 017 — Email from Ivo Fenlock (Contractor, Bracken & Vale Plumbing) |
| 17 | 2025-09-10T10:51:20+00:00 | Event 018 — Email from Tessa Wren (Property Manager, Northbridge Lettings) |
| 18 | 2025-09-15T10:03:43+00:00 | Event 019 — Document from Ivo Fenlock (Contractor, Bracken & Vale Plumbing) |
| 19 | 2025-09-15T11:03:41+00:00 | Event 020 — Email from Tessa Wren (Property Manager, Northbridge Lettings) |
| 20 | 2025-09-15T11:05:47+00:00 | Event 021 — Call from Tessa Wren (Property Manager, Northbridge Lettings) |
| 21 | 2025-09-15T11:11:18+00:00 | Event 022 — Document from Ivo Fenlock (Contractor, Bracken & Vale Plumbing) |
| 22 | 2025-09-15T11:11:18+00:00 | Attachment corrected-plumbing-invoice.pdf (PDF text extraction) |

## Final decision — system case `e66c7d372a8b`

- **Decision (policy outcome):** **HUMAN REVIEW**
- **Proposed next action:** `clarify` — Separate boiler matter - work done unclear (category other)
- **Next step:** Verify the person, property and work item mapping.
- **Owner:** case manager
- **Case state:** open · policy v1
- **Split from system case** `3cace1ca9243` as a separate issue.

**Latest reading (model, medium confidence, route `clarify`):** Contractor agrees to amend the invoice postcode and resend it. A separate boiler matter was mentioned; the manager will check with the relevant engineer what work was done.

### Actions taken

- **No operational action was executed.** Nothing was booked, instructed, paid or sent. The system recorded readings, claims and policy assessments only.

### Escalated to a person (handover)

| Check | Owner | Rule | What the person must resolve | Evidence |
|---|---|---|---|---|
| `identity` | case manager | `require-identity` | Verify the person, property and work item mapping. | no source recorded |
| `route` | case manager | `require-route` | Verify the recipient and permitted communication route. | no source recorded |

### Missing information and conflicting facts

- None recorded by the latest reading.

## Final decision — system case `bb642aa7ce68`

- **Decision (policy outcome):** **HUMAN REVIEW**
- **Proposed next action:** `request_quote` — Loose top kitchen drawer with snapped front brackets (category other)
- **Next step:** Verify the person, property and work item mapping.
- **Owner:** case manager
- **Case state:** open · policy v1
- **Split from system case** `3cace1ca9243` as a separate issue.

**Latest reading (model, high confidence, route `request_quote`):** Tenant chases the outstanding plumbing appointment for the leaking kitchen tap, saying no contact has been made despite availability being given. They also report a loose top kitchen drawer with apparently snapped metal front brackets and ask whether it can be repaired during the same visit.

### Actions taken

- **No operational action was executed.** Nothing was booked, instructed, paid or sent. The system recorded readings, claims and policy assessments only.

### Escalated to a person (handover)

| Check | Owner | Rule | What the person must resolve | Evidence |
|---|---|---|---|---|
| `identity` | case manager | `require-identity` | Verify the person, property and work item mapping. | no source recorded |
| `route` | case manager | `require-route` | Verify the recipient and permitted communication route. | no source recorded |
| `classification` | case manager | `require-classification` | Confirm that the category and work item match the source request. A verified route is required before asking externally. | no source recorded |
| `supported` | case manager | `require-supported` | A case manager must define a supported action for this situation. | no source recorded |

### Missing information and conflicting facts

- None recorded by the latest reading.

## Final decision — system case `3cace1ca9243`

- **Decision (policy outcome):** **HUMAN REVIEW**
- **Proposed next action:** `close_item` — Kitchen mixer tap dripping constantly; cloudy water reported (category plumbing)
- **Next step:** Verify the person, property and work item mapping.
- **Owner:** case manager
- **Case state:** open · policy v1

**Latest reading (claude-opus-5, medium confidence, route `close_item`):** Corrected invoice from Bracken & Vale Plumbing for 18 Thistlewick Row showing supply and install of one new mono kitchen sink tap, with the postcode amended. No total amount is stated in the extracted text and the cloudy water complaint is not addressed.

**Why:** Corrected invoice for completed tap installation; router decision close_item accepted, though cloudy water remains unverified.

### Actions taken

- **No operational action was executed.** Nothing was booked, instructed, paid or sent. The system recorded readings, claims and policy assessments only.

### Escalated to a person (handover)

| Check | Owner | Rule | What the person must resolve | Evidence |
|---|---|---|---|---|
| `identity` | case manager | `require-identity` | Verify the person, property and work item mapping. | no source recorded |
| `completion` | reviewer | `require-completion` | Verify completion of this work item with usable evidence. A verified route is required before asking externally. | Event 022 — Document from Ivo Fenlock (Contractor, Bracken & Vale Plumbing) |
| `commitments` | case manager | `require-commitments` | Resolve or explicitly cancel every outstanding commitment for this item. A verified route is required before asking externally. | no source recorded |
| `triage` | case manager | `require-triage` | Clarify before routing: The invoice covers the tap replacement only; it is still unconfirmed whether the reported cloudy water was investigated or resolved. A verified route is required before asking externally. | Event 022 — Document from Ivo Fenlock (Contractor, Bracken & Vale Plumbing) |

### Missing information and conflicting facts

- **completion** (blocks the route): Invoice covers the tap replacement only; it is still unconfirmed whether the reported cloudy water was investigated or resolved.
- **issue_details**: No invoice total including VAT appears in the extracted text, so the full commitment is not established.
- 7 extracted claim(s) remain **unverified source assertions** (see REASONING.md); none was treated as verified authority.

## Failures

- None recorded. (Jev and Claude calls all returned; no workflow step failed.)

## Result

No approval was invented and no human response was supplied by the runner. The case is waiting on the person(s) listed in the handover above.

Trace: `REASONING.md` (why) · `AUDIT.md` (every step, actor and tool) · `evidence.json` / `records.jsonl` (raw records) · `checkpoint-NNN.json` (state after each source; kept in the local run directory, not published).
