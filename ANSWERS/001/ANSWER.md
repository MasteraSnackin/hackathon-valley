# Property Management — case 001: Bathroom leak and wall repair

*PREPARATION ONLY — not official Reality Test results. System-generated; not edited by hand.*

- **Property (as supplied, unverified):** 4 Thistlewick Rise, Larkcombe, ZZ1 1ZZ
- **Decision cutoff:** 2025-09-23T16:12:00+00:00
- **Runner status:** **settled** · execution `native_local` · sources processed 24 of 24
- **Models:** Claude `claude-opus-5` (triage effort medium); Jev `jev-1.13.0` routing
- **Commit:** `26542cfa3d481aa925490db741aa4fbab8f70e3c` · input SHA-256 `9a9c6f50d8185ec7…`

All operational tools in this run are clearly labelled **simulated** adapters: no real tenant, landlord or contractor was contacted, nothing was paid or booked, and a simulated receipt does not prove work happened.

## What the system received

The initial report and 23 further sources, submitted one at a time in availability order; each was processed and settled before the next became visible. Full text: `input.json`.

| # | Available at | Source |
|---|---|---|
| 0 | 2025-09-04T08:10:00+00:00 | Initial report — Event 001 — Email |
| 1 | 2025-09-04T08:31:00+00:00 | Event 002 — Call from Mira Sallow (Property Manager, Northbridge Lettings) |
| 2 | 2025-09-04T09:05:00+00:00 | Event 003 — Email from Mira Sallow (Property Manager, Northbridge Lettings) |
| 3 | 2025-09-05T17:20:00+00:00 | Event 004 — Email from Orin Vale (Landlord) |
| 4 | 2025-09-07T09:15:00+00:00 | Event 005 — Email from Orin Vale (Landlord) |
| 5 | 2025-09-07T10:05:00+00:00 | Event 006 — Email from Mira Sallow (Property Manager, Northbridge Lettings) |
| 6 | 2025-09-07T11:10:00+00:00 | Event 007 — Email from Ewan Rook (Contractor, Hearthline Plumbing & Bath) |
| 7 | 2025-09-07T11:35:00+00:00 | Event 008 — Email from Mira Sallow (Property Manager, Northbridge Lettings) |
| 8 | 2025-09-08T11:30:00+00:00 | Event 009 — SMS from Mira Sallow (Property Manager, Northbridge Lettings) |
| 9 | 2025-09-10T12:20:00+00:00 | Event 010 — Call from Mira Sallow (Property Manager, Northbridge Lettings) |
| 10 | 2025-09-15T15:10:00+00:00 | Event 011 — Call from Nessa Quill (Tenant) |
| 11 | 2025-09-15T15:35:00+00:00 | Event 012 — Email from Mira Sallow (Property Manager, Northbridge Lettings) |
| 12 | 2025-09-16T07:40:00+00:00 | Event 013 — Email from Ewan Rook (Contractor, Hearthline Plumbing & Bath) |
| 13 | 2025-09-16T08:05:00+00:00 | Event 014 — Email from Mira Sallow (Property Manager, Northbridge Lettings) |
| 14 | 2025-09-18T12:00:00+00:00 | Event 015 — Note from Mira Sallow (Property Manager, Northbridge Lettings) |
| 15 | 2025-09-18T14:25:00+00:00 | Event 016 — Document from Ewan Rook (Contractor, Hearthline Plumbing & Bath) |
| 16 | 2025-09-18T14:45:00+00:00 | Event 017 — Email from Mira Sallow (Property Manager, Northbridge Lettings) |
| 17 | 2025-09-18T15:00:00+00:00 | Event 018 — Email from Orin Vale (Landlord) |
| 18 | 2025-09-18T15:12:00+00:00 | Event 019 — Email from Mira Sallow (Property Manager, Northbridge Lettings) |
| 19 | 2025-09-18T15:30:00+00:00 | Event 020 — Email from Mira Sallow (Property Manager, Northbridge Lettings) |
| 20 | 2025-09-18T15:39:00+00:00 | Event 021 — Email from Ewan Rook (Contractor, Hearthline Plumbing & Bath) |
| 21 | 2025-09-23T16:08:00+00:00 | Event 022 — Email from Mira Sallow (Property Manager, Northbridge Lettings) |
| 22 | 2025-09-23T16:12:00+00:00 | Event 023 — Email from Orin Vale (Landlord) |
| 23 | 2025-09-23T16:12:00+00:00 | Attachment bathroom-works-quotation.pdf (PDF text extraction) |

## Final decision — system case `5c91d5582df1`

- **Decision (policy outcome):** **HUMAN REVIEW**
- **Proposed next action:** `clarify` — Recurring leak from pipe behind shower, water through grout (category plumbing)
- **Next step:** Verify the person, property and work item mapping.
- **Owner:** case manager
- **Case state:** open · policy v1

**Latest reading (claude-opus-5, medium confidence, route `clarify`):** Contractor quotation PDF (ref NBL-001-Q1) for bathroom works totalling £2,844.00 including VAT, matching the previously discussed scope. However, the property stated on the quotation is 8 Wrenfold Mews, Brindlewick, not the case property 4 Thistlewick Rise, Larkcombe.

**Why:** Quotation total matches the case figure but the property address differs, so the document cannot be relied on for authority until identity of the property is confirmed; router's clarify route accepted.

### Actions taken

- **No operational action was executed.** Nothing was booked, instructed, paid or sent. The system recorded readings, claims and policy assessments only.

### Escalated to a person (handover)

| Check | Owner | Rule | What the person must resolve | Evidence |
|---|---|---|---|---|
| `identity` | case manager | `require-identity` | Verify the person, property and work item mapping. | no source recorded |
| `route` | case manager | `require-route` | Verify the recipient and permitted communication route. | no source recorded |
| `triage` | case manager | `require-triage` | Clarify before routing: The quotation names 8 Wrenfold Mews, Brindlewick, ZZ1 1ZZ, which does not match the case property 4 Thistlewick Rise, Larkcombe. Confirm which property this quote covers. A verified route is requi … | Attachment bathroom-works-quotation.pdf (PDF text extraction) |

### Missing information and conflicting facts

- **location** (blocks the route): The quotation names 8 Wrenfold Mews, Brindlewick, ZZ1 1ZZ, which does not match the case property 4 Thistlewick Rise, Larkcombe. Confirm which property this quote covers.
- **issue_details**: The quotation shows a single line item of £2,370.00 plus VAT and does not reflect the itemized materials/labour breakdown or the 10% commission and 50% deposit the contractor mentioned. Confirm whether this is the breakdown the landlord asked for.
- 10 extracted claim(s) remain **unverified source assertions** (see REASONING.md); none was treated as verified authority.

## Failures

- None recorded. (Jev and Claude calls all returned; no workflow step failed.)

## Result

No approval was invented and no human response was supplied by the runner. The case is waiting on the person(s) listed in the handover above.

Trace: `REASONING.md` (why) · `AUDIT.md` (every step, actor and tool) · `evidence.json` / `records.jsonl` (raw records) · `checkpoint-NNN.json` (state after each source; kept in the local run directory, not published).
