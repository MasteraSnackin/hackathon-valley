# Property Management — case 010: Kitchen cabinet maintenance request

*PREPARATION ONLY — not official Reality Test results. System-generated; not edited by hand.*

- **Property (as supplied, unverified):** 42 Brackenveil Row, Oakhollow, ZZ1 1ZZ
- **Decision cutoff:** 2025-09-24T14:36:47+00:00
- **Runner status:** **settled** · execution `native_local` · sources processed 26 of 26
- **Models:** Claude `claude-opus-5` (triage effort medium); Jev `jev-1.13.0` routing
- **Commit:** `26542cfa3d481aa925490db741aa4fbab8f70e3c` · input SHA-256 `e04f41981aef65ad…`

All operational tools in this run are clearly labelled **simulated** adapters: no real tenant, landlord or contractor was contacted, nothing was paid or booked, and a simulated receipt does not prove work happened.

## What the system received

The initial report and 25 further sources, submitted one at a time in availability order; each was processed and settled before the next became visible. Full text: `input.json`.

| # | Available at | Source |
|---|---|---|
| 0 | 2025-09-04T12:08:49+00:00 | Initial report — Event 001 — Portal |
| 1 | 2025-09-04T12:31:00+00:00 | Event 002 — Email from Nia Calder (Property Manager, Northbridge Lettings) |
| 2 | 2025-09-04T14:57:45+00:00 | Event 003 — Email from Nia Calder (Property Manager, Northbridge Lettings) |
| 3 | 2025-09-06T09:07:13+00:00 | Event 004 — Email from Soren Pike (Landlord) |
| 4 | 2025-09-07T16:30:02+00:00 | Event 005 — Email from Nia Calder (Property Manager, Northbridge Lettings) |
| 5 | 2025-09-09T16:49:18+00:00 | Event 006 — Update from Nia Calder (Property Manager, Northbridge Lettings) |
| 6 | 2025-09-09T16:50:18+00:00 | Event 007 — Update from Nia Calder (Property Manager, Northbridge Lettings) |
| 7 | 2025-09-09T16:50:37+00:00 | Event 008 — Email from Nia Calder (Property Manager, Northbridge Lettings) |
| 8 | 2025-09-09T16:50:43+00:00 | Event 009 — Email from Nia Calder (Property Manager, Northbridge Lettings) |
| 9 | 2025-09-09T17:13:16+00:00 | Event 010 — Email from Elowen Marr (Tenant) |
| 10 | 2025-09-09T17:14:02+00:00 | Event 011 — Email from Nia Calder (Property Manager, Northbridge Lettings) |
| 11 | 2025-09-10T09:00:17+00:00 | Event 012 — Email from Kellan Rook (Contractor, Alderline Joinery) |
| 12 | 2025-09-10T11:13:55+00:00 | Event 013 — Email from Nia Calder (Property Manager, Northbridge Lettings) |
| 13 | 2025-09-10T11:14:46+00:00 | Event 014 — Call from Kellan Rook (Contractor, Alderline Joinery) |
| 14 | 2025-09-10T11:14:59+00:00 | Event 015 — Call from Soren Pike (Landlord) |
| 15 | 2025-09-10T15:24:27+00:00 | Event 016 — Email from Soren Pike (Landlord) |
| 16 | 2025-09-11T09:46:38+00:00 | Event 017 — Email from Nia Calder (Property Manager, Northbridge Lettings) |
| 17 | 2025-09-11T15:38:25+00:00 | Event 018 — Email from Nia Calder (Property Manager, Northbridge Lettings) |
| 18 | 2025-09-11T16:07:24+00:00 | Event 019 — Email from Kellan Rook (Contractor, Alderline Joinery) |
| 19 | 2025-09-14T07:16:51+00:00 | Event 020 — Note from Nia Calder (Property Manager, Northbridge Lettings) |
| 20 | 2025-09-17T08:01:16+00:00 | Event 021 — Note from Nia Calder (Property Manager, Northbridge Lettings) |
| 21 | 2025-09-23T13:50:19+00:00 | Event 022 — Call from Kellan Rook (Contractor, Alderline Joinery) |
| 22 | 2025-09-23T13:51:03+00:00 | Event 023 — Call from Nia Calder (Property Manager, Northbridge Lettings) |
| 23 | 2025-09-24T14:35:00+00:00 | Event 024 — Email from Kellan Rook (Contractor, Alderline Joinery) |
| 24 | 2025-09-24T14:36:03+00:00 | Event 025 — Email from Nia Calder (Property Manager, Northbridge Lettings) |
| 25 | 2025-09-24T14:36:22+00:00 | Event 026 — Note from Nia Calder (Property Manager, Northbridge Lettings) |

## Final decision — system case `538ff9876ed4`

- **Decision (policy outcome):** **HUMAN REVIEW**
- **Proposed next action:** `clarify` — Doors not closing properly (category doors_locks)
- **Next step:** Verify the person, property and work item mapping.
- **Owner:** case manager
- **Case state:** open · policy v1
- **Split from system case** `e933f68d1f88` as a separate issue.

**Latest reading (model, medium confidence, route `clarify`):** Landlord asked Northbridge Lettings to obtain a quote for replacing the kitchen-cabinet laminate, without approving the work itself. It remains unclear whether the doors that will not close are cabinet or room/external doors.

### Actions taken

- **No operational action was executed.** Nothing was booked, instructed, paid or sent. The system recorded readings, claims and policy assessments only.

### Escalated to a person (handover)

| Check | Owner | Rule | What the person must resolve | Evidence |
|---|---|---|---|---|
| `identity` | case manager | `require-identity` | Verify the person, property and work item mapping. | no source recorded |
| `route` | case manager | `require-route` | Verify the recipient and permitted communication route. | no source recorded |

### Missing information and conflicting facts

- None recorded by the latest reading.
- 1 extracted claim(s) remain **unverified source assertions** (see REASONING.md); none was treated as verified authority.

## Final decision — system case `ba67cfbe2d4c`

- **Decision (policy outcome):** **HUMAN REVIEW**
- **Proposed next action:** `clarify` — Doors not closing properly (category doors_locks)
- **Next step:** Verify the person, property and work item mapping.
- **Owner:** case manager
- **Case state:** open · policy v1
- **Split from system case** `e933f68d1f88` as a separate issue.

**Latest reading (model, medium confidence, route `clarify`):** The property manager has forwarded the tenant's report (cuts from peeling cabinet laminate, doors not closing, two dogs to secure) to the landlord and asked whether Northbridge Lettings may arrange the work. No decision, quote or appointment yet.

### Actions taken

- **No operational action was executed.** Nothing was booked, instructed, paid or sent. The system recorded readings, claims and policy assessments only.

### Escalated to a person (handover)

| Check | Owner | Rule | What the person must resolve | Evidence |
|---|---|---|---|---|
| `identity` | case manager | `require-identity` | Verify the person, property and work item mapping. | no source recorded |
| `route` | case manager | `require-route` | Verify the recipient and permitted communication route. | no source recorded |

### Missing information and conflicting facts

- None recorded by the latest reading.
- 1 extracted claim(s) remain **unverified source assertions** (see REASONING.md); none was treated as verified authority.

## Final decision — system case `f30844603a18`

- **Decision (policy outcome):** **HUMAN REVIEW**
- **Proposed next action:** `request_quote` — Doors not closing properly (category doors_locks)
- **Next step:** Verify the person, property and work item mapping.
- **Owner:** case manager
- **Case state:** open · policy v1
- **Split from system case** `e933f68d1f88` as a separate issue.

**Latest reading (model, medium confidence, route `request_quote`):** Tenant reports peeling kitchen-cabinet laminate with sharp edges that have caused multiple cuts, and several cabinet doors that will not close properly. Two dogs would need securing before any visit.

### Actions taken

- **No operational action was executed.** Nothing was booked, instructed, paid or sent. The system recorded readings, claims and policy assessments only.

### Escalated to a person (handover)

| Check | Owner | Rule | What the person must resolve | Evidence |
|---|---|---|---|---|
| `identity` | case manager | `require-identity` | Verify the person, property and work item mapping. | no source recorded |
| `route` | case manager | `require-route` | Verify the recipient and permitted communication route. | no source recorded |
| `classification` | case manager | `require-classification` | Confirm that the category and work item match the source request. A verified route is required before asking externally. | Split from case e933f68d1f88: Intake report |

### Missing information and conflicting facts

- None recorded by the latest reading.
- 1 extracted claim(s) remain **unverified source assertions** (see REASONING.md); none was treated as verified authority.

## Final decision — system case `e933f68d1f88`

- **Decision (policy outcome):** **HUMAN REVIEW**
- **Proposed next action:** `request_quote` — Peeling kitchen-cabinet laminate with sharp edges causing cuts (category other)
- **Next step:** Verify the person, property and work item mapping.
- **Owner:** case manager
- **Case state:** open · policy v1

**Latest reading (jev-1.13.0, high confidence, route `request_quote`):** Routed by Jev to request_quote. Claude did not read this message.

**Why:** Jev routed with confidence 0.90; nothing in the message needs Claude.

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
- 2 extracted claim(s) remain **unverified source assertions** (see REASONING.md); none was treated as verified authority.

## Failures

- None recorded. (Jev and Claude calls all returned; no workflow step failed.)

## Result

No approval was invented and no human response was supplied by the runner. The case is waiting on the person(s) listed in the handover above.

Trace: `REASONING.md` (why) · `AUDIT.md` (every step, actor and tool) · `evidence.json` / `records.jsonl` (raw records) · `checkpoint-NNN.json` (state after each source; kept in the local run directory, not published).
