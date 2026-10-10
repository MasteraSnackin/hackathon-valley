# Property Management — case 023: Heating maintenance at 7 Larkspur Fold

*PREPARATION ONLY — not official Reality Test results. System-generated; not edited by hand.*

- **Property (as supplied, unverified):** 7 Larkspur Fold, Orvane Heath, ZZ1 1ZZ
- **Decision cutoff:** 2025-02-12T16:35:00+00:00
- **Runner status:** **settled** · execution `native_local` · sources processed 25 of 25
- **Models:** Claude `claude-opus-5` (triage effort medium); Jev `jev-1.13.0` routing
- **Commit:** `26542cfa3d481aa925490db741aa4fbab8f70e3c` · input SHA-256 `716258e3d16deb28…`

All operational tools in this run are clearly labelled **simulated** adapters: no real tenant, landlord or contractor was contacted, nothing was paid or booked, and a simulated receipt does not prove work happened.

## What the system received

The initial report and 24 further sources, submitted one at a time in availability order; each was processed and settled before the next became visible. Full text: `input.json`.

| # | Available at | Source |
|---|---|---|
| 0 | 2025-02-03T08:14:00+00:00 | Initial report — Event 001 — Portal |
| 1 | 2025-02-03T08:41:00+00:00 | Event 002 — Update from Ivo Merrick (Property Manager, Northbridge Lettings) |
| 2 | 2025-02-03T09:12:00+00:00 | Event 003 — Portal from Tessa Vane (Tenant) |
| 3 | 2025-02-03T10:05:00+00:00 | Event 004 — Email from Ivo Merrick (Property Manager, Northbridge Lettings) |
| 4 | 2025-02-03T12:22:00+00:00 | Event 005 — Email from Soren Dallow (Landlord) |
| 5 | 2025-02-04T09:18:00+00:00 | Event 006 — Email from Ivo Merrick (Property Manager, Northbridge Lettings) |
| 6 | 2025-02-04T10:03:00+00:00 | Event 007 — Email from Petra Quill (Contractor, Copper Finch Mechanical) |
| 7 | 2025-02-05T14:32:00+00:00 | Event 008 — Update from Petra Quill (Contractor, Copper Finch Mechanical) |
| 8 | 2025-02-05T14:54:00+00:00 | Event 009 — Email from Petra Quill (Contractor, Copper Finch Mechanical) |
| 9 | 2025-02-05T15:21:00+00:00 | Event 010 — Email from Ivo Merrick (Property Manager, Northbridge Lettings) |
| 10 | 2025-02-06T07:56:00+00:00 | Event 011 — SMS from Tessa Vane (Tenant) |
| 11 | 2025-02-06T10:38:00+00:00 | Event 012 — Email from Soren Dallow (Landlord) |
| 12 | 2025-02-06T13:17:00+00:00 | Event 013 — Portal from Ivo Merrick (Property Manager, Northbridge Lettings) |
| 13 | 2025-02-06T14:06:00+00:00 | Event 014 — Portal from Tessa Vane (Tenant) |
| 14 | 2025-02-07T09:24:00+00:00 | Event 015 — Email from Ivo Merrick (Property Manager, Northbridge Lettings) |
| 15 | 2025-02-07T13:47:00+00:00 | Event 016 — Email from Petra Quill (Contractor, Copper Finch Mechanical) |
| 16 | 2025-02-10T09:52:00+00:00 | Event 017 — Email from Petra Quill (Contractor, Copper Finch Mechanical) |
| 17 | 2025-02-10T10:26:00+00:00 | Event 018 — Document from Petra Quill (Contractor, Copper Finch Mechanical) |
| 18 | 2025-02-10T11:11:00+00:00 | Event 019 — Note from Ivo Merrick (Property Manager, Northbridge Lettings) |
| 19 | 2025-02-10T15:08:00+00:00 | Event 020 — Portal from Tessa Vane (Tenant) |
| 20 | 2025-02-11T09:16:00+00:00 | Event 021 — Email from Ivo Merrick (Property Manager, Northbridge Lettings) |
| 21 | 2025-02-12T11:42:00+00:00 | Event 022 — Email from Petra Quill (Contractor, Copper Finch Mechanical) |
| 22 | 2025-02-12T16:35:00+00:00 | Event 023 — Email from Ivo Merrick (Property Manager, Northbridge Lettings) |
| 23 | 2025-02-12T16:35:00+00:00 | Attachment invoice-NBL-CFM-250210-A.pdf (PDF text extraction) |
| 24 | 2025-02-12T16:35:00+00:00 | Attachment invoice-NBL-CFM-250210-B.pdf (PDF text extraction) |

## Final decision — system case `fea0d65b5f72`

- **Decision (policy outcome):** **HUMAN REVIEW**
- **Proposed next action:** `clarify` — Radiator heating cutting out intermittently (category other)
- **Next step:** Verify the person, property and work item mapping.
- **Owner:** case manager
- **Case state:** open · policy v1

**Latest reading (claude-opus-5, medium confidence, route `clarify`):** Second Copper Finch Mechanical invoice (NBL-CFM-250210-B) for the same 5 February service date, totalling £372.00 including VAT, covering actuator supply and replacement plus diagnosis and testing. It does not state whether it supersedes the £138.00 invoice, and no authorisation or completion evidence is provided.

**Why:** Billing document raising unresolved duplicate-invoice, authority and completion questions; cannot be actioned until the record position is clarified.

### Actions taken

- **No operational action was executed.** Nothing was booked, instructed, paid or sent. The system recorded readings, claims and policy assessments only.

### Escalated to a person (handover)

| Check | Owner | Rule | What the person must resolve | Evidence |
|---|---|---|---|---|
| `identity` | case manager | `require-identity` | Verify the person, property and work item mapping. | no source recorded |
| `route` | case manager | `require-route` | Verify the recipient and permitted communication route. | no source recorded |
| `triage` | case manager | `require-triage` | Clarify before routing: Contractor has not confirmed whether a repair alternative to replacement is possible, parts availability, or an itemised estimate breakdown including whether diagnosis is credited. A verified rout … | Event 016 — Email from Petra Quill (Contractor, Copper Finch Mechanical) |

### Missing information and conflicting facts

- **issue_details** (blocks the route): This invoice covers the same 5 February service date as invoice NBL-CFM-250210-A (£138.00); it is not stated whether it supersedes that record or is separate chargeable work.
- **completion** (blocks the route): No completion evidence, parts record or attendance proof for the actuator replacement is supplied, and the tenant reports heating still intermittent.
- **issue_details** (blocks the route): No written landlord authorisation on file for actuator replacement; authority for the £372.00 spend is unconfirmed.
- 15 extracted claim(s) remain **unverified source assertions** (see REASONING.md); none was treated as verified authority.

## Failures

- None recorded. (Jev and Claude calls all returned; no workflow step failed.)

## Result

No approval was invented and no human response was supplied by the runner. The case is waiting on the person(s) listed in the handover above.

Trace: `REASONING.md` (why) · `AUDIT.md` (every step, actor and tool) · `evidence.json` / `records.jsonl` (raw records) · `checkpoint-NNN.json` (state after each source; kept in the local run directory, not published).
