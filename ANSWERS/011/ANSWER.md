# Property Management — case 011: Kitchen ceiling leak inspection at 16 Brindlewick Mews

*PREPARATION ONLY — not official Reality Test results. System-generated; not edited by hand.*

- **Property (as supplied, unverified):** 16 Brindlewick Mews, Fenbarrow, ZZ1 1ZZ
- **Decision cutoff:** 2025-06-13T15:26:00+00:00
- **Runner status:** **settled** · execution `native_local` · sources processed 24 of 24
- **Models:** Claude `claude-opus-5` (triage effort medium); Jev `jev-1.13.0` routing
- **Commit:** `26542cfa3d481aa925490db741aa4fbab8f70e3c` · input SHA-256 `c2ff5e68f67f5d9e…`

All operational tools in this run are clearly labelled **simulated** adapters: no real tenant, landlord or contractor was contacted, nothing was paid or booked, and a simulated receipt does not prove work happened.

## What the system received

The initial report and 23 further sources, submitted one at a time in availability order; each was processed and settled before the next became visible. Full text: `input.json`.

| # | Available at | Source |
|---|---|---|
| 0 | 2025-06-10T08:12:00+00:00 | Initial report — Event 001 — Portal |
| 1 | 2025-06-10T08:39:00+00:00 | Event 002 — Update from Mara Voss (Property Manager, Northbridge Lettings) |
| 2 | 2025-06-10T09:17:00+00:00 | Event 003 — Portal from Iven Rell (Tenant) |
| 3 | 2025-06-10T09:42:00+00:00 | Event 004 — Note from Mara Voss (Property Manager, Northbridge Lettings) |
| 4 | 2025-06-10T10:21:00+00:00 | Event 005 — Email from Mara Voss (Property Manager, Northbridge Lettings) |
| 5 | 2025-06-10T13:06:00+00:00 | Event 006 — Email from Bren Talwick (Building Manager, Alderwake Court) |
| 6 | 2025-06-10T14:18:00+00:00 | Event 007 — Call from Mara Voss (Property Manager, Northbridge Lettings) |
| 7 | 2025-06-10T15:02:00+00:00 | Event 008 — Email from Mara Voss (Property Manager, Northbridge Lettings) |
| 8 | 2025-06-11T11:18:00+00:00 | Event 009 — Note from Kellan Orve (Contractor, Mossbarrow Pipe Services) |
| 9 | 2025-06-11T11:46:00+00:00 | Event 010 — SMS from Iven Rell (Tenant) |
| 10 | 2025-06-11T14:12:00+00:00 | Event 011 — Email from Kellan Orve (Contractor, Mossbarrow Pipe Services) |
| 11 | 2025-06-11T16:05:00+00:00 | Event 012 — Email from Mara Voss (Property Manager, Northbridge Lettings) |
| 12 | 2025-06-12T08:44:00+00:00 | Event 013 — Email from Ossa Fenlow (Landlord) |
| 13 | 2025-06-12T09:26:00+00:00 | Event 014 — Email from Mara Voss (Property Manager, Northbridge Lettings) |
| 14 | 2025-06-12T10:03:00+00:00 | Event 015 — Email from Kellan Orve (Contractor, Mossbarrow Pipe Services) |
| 15 | 2025-06-12T10:36:00+00:00 | Event 016 — Call from Mara Voss (Property Manager, Northbridge Lettings) |
| 16 | 2025-06-13T10:42:00+00:00 | Event 017 — Call from Kellan Orve (Contractor, Mossbarrow Pipe Services) |
| 17 | 2025-06-13T10:51:00+00:00 | Event 018 — Call from Mara Voss (Property Manager, Northbridge Lettings) |
| 18 | 2025-06-13T11:09:00+00:00 | Event 019 — Portal from Mara Voss (Property Manager, Northbridge Lettings) |
| 19 | 2025-06-13T11:27:00+00:00 | Event 020 — Portal from Iven Rell (Tenant) |
| 20 | 2025-06-13T11:34:00+00:00 | Event 021 — Email from Mara Voss (Property Manager, Northbridge Lettings) |
| 21 | 2025-06-13T12:14:00+00:00 | Event 022 — Email from Ossa Fenlow (Landlord) |
| 22 | 2025-06-13T13:48:00+00:00 | Event 023 — Note from Kellan Orve (Contractor, Mossbarrow Pipe Services) |
| 23 | 2025-06-13T15:26:00+00:00 | Event 024 — Update from Mara Voss (Property Manager, Northbridge Lettings) |

## Final decision — system case `015374d273d2`

- **Decision (policy outcome):** **HUMAN REVIEW**
- **Proposed next action:** `request_quote` — Damp patch and leak above kitchen sink ceiling (category plumbing)
- **Next step:** Verify the person, property and work item mapping.
- **Owner:** case manager
- **Case state:** open · policy v1

**Latest reading (claude-opus-5, medium confidence, route `request_quote`):** Mara Voss updates the landlord that the pipe repair is still needed and the leak recurs when the tap is used, but the contractor has stopped because the ceiling lining is unidentified with no survey on file. She asks the landlord to decide whether further assessment or repair scope can be authorised; no cost or appointment agreed.

**Why:** Ongoing defect with no priceable scope; contractor cannot quote until the lining is identified, so the item stays at quote/assessment stage pending landlord decision.

### Actions taken

- **No operational action was executed.** Nothing was booked, instructed, paid or sent. The system recorded readings, claims and policy assessments only.

### Escalated to a person (handover)

| Check | Owner | Rule | What the person must resolve | Evidence |
|---|---|---|---|---|
| `identity` | case manager | `require-identity` | Verify the person, property and work item mapping. | no source recorded |
| `route` | case manager | `require-route` | Verify the recipient and permitted communication route. | no source recorded |
| `classification` | case manager | `require-classification` | Confirm that the category and work item match the source request. A verified route is required before asking externally. | Intake report |
| `triage` | case manager | `require-triage` | Clarify before routing: No records exist identifying the ceiling lining; a case manager must decide whether a specialist survey is required before the authorised plumbing scope can continue. A verified route is required … | Event 022 — Email from Ossa Fenlow (Landlord) |

### Missing information and conflicting facts

- **issue_details** (blocks the route): The ceiling lining remains unidentified with no survey on file; a case manager must decide whether a specialist survey is commissioned before plumbing work continues.
- **completion**: No authority, cost or appointment is agreed for further assessment or repair scope; awaiting landlord decision.
- 11 extracted claim(s) remain **unverified source assertions** (see REASONING.md); none was treated as verified authority.

## Failures

- None recorded. (Jev and Claude calls all returned; no workflow step failed.)

## Result

No approval was invented and no human response was supplied by the runner. The case is waiting on the person(s) listed in the handover above.

Trace: `REASONING.md` (why) · `AUDIT.md` (every step, actor and tool) · `evidence.json` / `records.jsonl` (raw records) · `checkpoint-NNN.json` (state after each source; kept in the local run directory, not published).
