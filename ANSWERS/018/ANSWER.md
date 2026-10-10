# Property Management — case 018: Kitchen maintenance report

*PREPARATION ONLY — not official Reality Test results. System-generated; not edited by hand.*

- **Property (as supplied, unverified):** 14 Mosswold Crescent, Brindlewick, ZZ1 1ZZ
- **Decision cutoff:** 2025-09-11T14:30:00+00:00
- **Runner status:** **settled** · execution `native_local` · sources processed 19 of 19
- **Models:** Claude `claude-opus-5` (triage effort medium); Jev `jev-1.13.0` routing
- **Commit:** `26542cfa3d481aa925490db741aa4fbab8f70e3c` · input SHA-256 `5ed7615b8b78b562…`

All operational tools in this run are clearly labelled **simulated** adapters: no real tenant, landlord or contractor was contacted, nothing was paid or booked, and a simulated receipt does not prove work happened.

## What the system received

The initial report and 18 further sources, submitted one at a time in availability order; each was processed and settled before the next became visible. Full text: `input.json`.

| # | Available at | Source |
|---|---|---|
| 0 | 2025-08-14T11:05:29+00:00 | Initial report — Event 001 — Portal |
| 1 | 2025-08-14T11:20:00+00:00 | Event 002 — Email from Tara Wren (Property Manager, Northbridge Lettings) |
| 2 | 2025-08-17T12:36:24+00:00 | Event 003 — Email from Tara Wren (Property Manager, Northbridge Lettings) |
| 3 | 2025-08-17T15:25:13+00:00 | Event 004 — Email from Gareth Vale (Landlord) |
| 4 | 2025-08-18T10:05:55+00:00 | Event 005 — Call from Tara Wren (Property Manager, Northbridge Lettings) |
| 5 | 2025-08-18T10:49:07+00:00 | Event 006 — Call from Gareth Vale (Landlord) |
| 6 | 2025-08-18T11:26:02+00:00 | Event 007 — Email from Tara Wren (Property Manager, Northbridge Lettings) |
| 7 | 2025-08-18T11:26:05+00:00 | Event 008 — Email from Tara Wren (Property Manager, Northbridge Lettings) |
| 8 | 2025-09-01T11:26:07+00:00 | Event 009 — Email from Tara Wren (Property Manager, Northbridge Lettings) |
| 9 | 2025-09-01T12:02:31+00:00 | Event 010 — Email from Elise Rowan (Tenant) |
| 10 | 2025-09-01T12:02:39+00:00 | Event 011 — Note from Tara Wren (Property Manager, Northbridge Lettings) |
| 11 | 2025-09-07T11:25:50+00:00 | Event 012 — Update from Northbridge Lettings workflow (System) |
| 12 | 2025-09-07T14:11:16+00:00 | Event 013 — Note from Tara Wren (Property Manager, Northbridge Lettings) |
| 13 | 2025-09-07T14:14:47+00:00 | Event 014 — Call from Tara Wren (Property Manager, Northbridge Lettings) |
| 14 | 2025-09-08T14:11:04+00:00 | Event 015 — Update from Northbridge Lettings workflow (System) |
| 15 | 2025-09-08T14:26:26+00:00 | Event 016 — Note from Tara Wren (Property Manager, Northbridge Lettings) |
| 16 | 2025-09-08T14:29:57+00:00 | Event 017 — Call from Tara Wren (Property Manager, Northbridge Lettings) |
| 17 | 2025-09-11T14:26:29+00:00 | Event 018 — Update from Northbridge Lettings workflow (System) |
| 18 | 2025-09-11T14:30:00+00:00 | Event 019 — Note from Tara Wren (Property Manager, Northbridge Lettings) |

## Final decision — system case `e4203c311563`

- **Decision (policy outcome):** **HUMAN REVIEW**
- **Proposed next action:** `clarify` — Reported maintenance (category other)
- **Next step:** Verify the person, property and work item mapping.
- **Owner:** case manager
- **Case state:** open · policy v1

**Latest reading (claude-opus-5, medium confidence, route `clarify`):** Internal note from the property manager to the maintenance coordinator recording that the tenant's latest update about the expected proofing visit has been logged. No new scope, appointment or completion details are provided.

**Why:** Administrative note with no new substantive information; scope and completion remain unresolved, so the item cannot be progressed beyond clarification.

### Actions taken

- **No operational action was executed.** Nothing was booked, instructed, paid or sent. The system recorded readings, claims and policy assessments only.

### Escalated to a person (handover)

| Check | Owner | Rule | What the person must resolve | Evidence |
|---|---|---|---|---|
| `identity` | case manager | `require-identity` | Verify the person, property and work item mapping. | no source recorded |
| `route` | case manager | `require-route` | Verify the recipient and permitted communication route. | no source recorded |
| `triage` | case manager | `require-triage` | Clarify before routing: No contractor, scope of works or target date has been given by the landlord. A verified route is required before asking externally. | Event 007 — Email from Tara Wren (Property Manager, Northbridge Lettings) |

### Missing information and conflicting facts

- **completion** (blocks the route): Still no confirmation or evidence that the proofing/sealing work has been completed.
- **issue_details** (blocks the route): Scope remains unclear - openings beneath the sink versus wall area work.
- **availability**: No rearranged appointment date or time for the missed proofing visit.
- 5 extracted claim(s) remain **unverified source assertions** (see REASONING.md); none was treated as verified authority.

## Failures

- None recorded. (Jev and Claude calls all returned; no workflow step failed.)

## Result

No approval was invented and no human response was supplied by the runner. The case is waiting on the person(s) listed in the handover above.

Trace: `REASONING.md` (why) · `AUDIT.md` (every step, actor and tool) · `evidence.json` / `records.jsonl` (raw records) · `checkpoint-NNN.json` (state after each source; kept in the local run directory, not published).
