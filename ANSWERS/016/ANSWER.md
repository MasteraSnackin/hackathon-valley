# Property Management — case 016: Smoke alarm maintenance request

*PREPARATION ONLY — not official Reality Test results. System-generated; not edited by hand.*

- **Property (as supplied, unverified):** 26 Tallowmere Close, Fenbarrow, ZZ1 1ZZ
- **Decision cutoff:** 2025-09-22T08:48:00+00:00
- **Runner status:** **settled** · execution `native_local` · sources processed 17 of 17
- **Models:** Claude `claude-opus-5` (triage effort medium); Jev `jev-1.13.0` routing
- **Commit:** `26542cfa3d481aa925490db741aa4fbab8f70e3c` · input SHA-256 `12d8ad65d5297132…`

All operational tools in this run are clearly labelled **simulated** adapters: no real tenant, landlord or contractor was contacted, nothing was paid or booked, and a simulated receipt does not prove work happened.

## What the system received

The initial report and 16 further sources, submitted one at a time in availability order; each was processed and settled before the next became visible. Full text: `input.json`.

| # | Available at | Source |
|---|---|---|
| 0 | 2025-08-07T09:58:12+00:00 | Initial report — Event 001 — Portal |
| 1 | 2025-08-07T10:21:14+00:00 | Event 002 — Email from Maya Chen (Property Manager, Northbridge Lettings) |
| 2 | 2025-08-07T11:24:38+00:00 | Event 003 — Email from Maya Chen (Property Manager, Northbridge Lettings) |
| 3 | 2025-08-07T16:14:57+00:00 | Event 004 — Email from Ronan Vale (Landlord) |
| 4 | 2025-08-07T16:55:25+00:00 | Event 005 — Email from Maya Chen (Property Manager, Northbridge Lettings) |
| 5 | 2025-08-07T16:55:33+00:00 | Event 006 — Email from Maya Chen (Property Manager, Northbridge Lettings) |
| 6 | 2025-08-12T05:55:15+00:00 | Event 007 — Email from Ronan Vale (Landlord) |
| 7 | 2025-08-24T08:01:00+00:00 | Event 008 — Email from Maya Chen (Property Manager, Northbridge Lettings) |
| 8 | 2025-08-27T09:25:40+00:00 | Event 009 — Call from Maya Chen (Property Manager, Northbridge Lettings) |
| 9 | 2025-09-02T15:50:40+00:00 | Event 010 — Call from Maya Chen (Property Manager, Northbridge Lettings) |
| 10 | 2025-09-07T16:50:26+00:00 | Event 011 — Call from Maya Chen (Property Manager, Northbridge Lettings) |
| 11 | 2025-09-07T16:57:08+00:00 | Event 012 — Email from Elise Rowan (Tenant) |
| 12 | 2025-09-11T13:12:26+00:00 | Event 013 — Email from Elise Rowan (Tenant) |
| 13 | 2025-09-11T17:40:27+00:00 | Event 014 — Note from Maya Chen (Property Manager, Northbridge Lettings) |
| 14 | 2025-09-20T10:15:00+00:00 | Event 015 — Call from Elise Rowan (Tenant) |
| 15 | 2025-09-20T11:02:00+00:00 | Event 016 — Note from Maya Chen (Property Manager, Northbridge Lettings) |
| 16 | 2025-09-22T08:48:00+00:00 | Event 017 — Update from Maya Chen (Property Manager, Northbridge Lettings) |

## Final decision — system case `2bfd5a655809`

- **Decision (policy outcome):** **HUMAN REVIEW**
- **Proposed next action:** `clarify` — Smoke alarm detached from ceiling (category other)
- **Next step:** Verify the person, property and work item mapping.
- **Owner:** case manager
- **Case state:** open · policy v1

**Latest reading (claude-opus-5, medium confidence, route `clarify`):** Internal status update from the property manager stating that NBL-016 is pending review. No new maintenance information about the detached smoke alarm.

**Why:** Message is a bare internal status note adding no actionable detail, so the case remains awaiting clarification on alarm completion.

### Actions taken

- **No operational action was executed.** Nothing was booked, instructed, paid or sent. The system recorded readings, claims and policy assessments only.

### Escalated to a person (handover)

| Check | Owner | Rule | What the person must resolve | Evidence |
|---|---|---|---|---|
| `identity` | case manager | `require-identity` | Verify the person, property and work item mapping. | no source recorded |
| `route` | case manager | `require-route` | Verify the recipient and permitted communication route. | no source recorded |
| `triage` | case manager | `require-triage` | Claude read this as a possible urgent hazard. A case manager must take over now and apply the urgent procedure. | Intake report |

### Missing information and conflicting facts

- **completion** (blocks the route): Still no evidence that the smoke alarm has been refitted and tested; confirmation needed.
- **access**: Identity and purpose of the unannounced visitor remain unverified, and no access arrangement is confirmed.
- 19 extracted claim(s) remain **unverified source assertions** (see REASONING.md); none was treated as verified authority.

## Failures

- None recorded. (Jev and Claude calls all returned; no workflow step failed.)

## Result

No approval was invented and no human response was supplied by the runner. The case is waiting on the person(s) listed in the handover above.

Trace: `REASONING.md` (why) · `AUDIT.md` (every step, actor and tool) · `evidence.json` / `records.jsonl` (raw records) · `checkpoint-NNN.json` (state after each source; kept in the local run directory, not published).
