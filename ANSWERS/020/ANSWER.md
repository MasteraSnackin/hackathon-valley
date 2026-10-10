# Property Management — case 020: Kitchen socket maintenance request

*PREPARATION ONLY — not official Reality Test results. System-generated; not edited by hand.*

- **Property (as supplied, unverified):** 8 Brindlewick Row, Oakhollow, ZZ1 1ZZ
- **Decision cutoff:** 2025-04-12T16:42:00+00:00
- **Runner status:** **settled** · execution `native_local` · sources processed 25 of 25
- **Models:** Claude `claude-opus-5` (triage effort medium); Jev `jev-1.13.0` routing
- **Commit:** `26542cfa3d481aa925490db741aa4fbab8f70e3c` · input SHA-256 `dd8600fe9d916e8e…`

All operational tools in this run are clearly labelled **simulated** adapters: no real tenant, landlord or contractor was contacted, nothing was paid or booked, and a simulated receipt does not prove work happened.

## What the system received

The initial report and 24 further sources, submitted one at a time in availability order; each was processed and settled before the next became visible. Full text: `input.json`.

| # | Available at | Source |
|---|---|---|
| 0 | 2025-04-12T08:14:00+00:00 | Initial report — Event 001 — Portal |
| 1 | 2025-04-12T08:22:00+00:00 | Event 002 — Update from Northbridge Lettings workflow (System) |
| 2 | 2025-04-12T08:37:00+00:00 | Event 003 — Portal from Maya Chen (Property Manager, Northbridge Lettings) |
| 3 | 2025-04-12T08:51:00+00:00 | Event 004 — Portal from Nora Bell (Tenant) |
| 4 | 2025-04-12T09:03:00+00:00 | Event 005 — Email from Maya Chen (Property Manager, Northbridge Lettings) |
| 5 | 2025-04-12T09:18:00+00:00 | Event 006 — Email from Elliot Vane (Landlord) |
| 6 | 2025-04-12T09:26:00+00:00 | Event 007 — Portal from Maya Chen (Property Manager, Northbridge Lettings) |
| 7 | 2025-04-12T09:41:00+00:00 | Event 008 — Portal from Nora Bell (Tenant) |
| 8 | 2025-04-12T09:52:00+00:00 | Event 009 — Note from Maya Chen (Property Manager, Northbridge Lettings) |
| 9 | 2025-04-12T10:02:00+00:00 | Event 010 — Email from Elliot Vane (Landlord) |
| 10 | 2025-04-12T10:16:00+00:00 | Event 011 — Email from Rowan Pike (Handyman, Pike Property Care) |
| 11 | 2025-04-12T10:29:00+00:00 | Event 012 — Portal from Maya Chen (Property Manager, Northbridge Lettings) |
| 12 | 2025-04-12T10:46:00+00:00 | Event 013 — Portal from Nora Bell (Tenant) |
| 13 | 2025-04-12T11:03:00+00:00 | Event 014 — Email from Maya Chen (Property Manager, Northbridge Lettings) |
| 14 | 2025-04-12T11:37:00+00:00 | Event 015 — Call from Rowan Pike (Handyman, Pike Property Care) |
| 15 | 2025-04-12T11:52:00+00:00 | Event 016 — Email from Elliot Vane (Landlord) |
| 16 | 2025-04-12T12:08:00+00:00 | Event 017 — Portal from Nora Bell (Tenant) |
| 17 | 2025-04-12T12:19:00+00:00 | Event 018 — Note from Maya Chen (Property Manager, Northbridge Lettings) |
| 18 | 2025-04-12T13:06:00+00:00 | Event 019 — SMS from Rowan Pike (Handyman, Pike Property Care) |
| 19 | 2025-04-12T13:14:00+00:00 | Event 020 — Call from Maya Chen (Property Manager, Northbridge Lettings) |
| 20 | 2025-04-12T13:27:00+00:00 | Event 021 — SMS from Elliot Vane (Landlord) |
| 21 | 2025-04-12T14:11:00+00:00 | Event 022 — Portal from Nora Bell (Tenant) |
| 22 | 2025-04-12T14:24:00+00:00 | Event 023 — Email from Rowan Pike (Handyman, Pike Property Care) |
| 23 | 2025-04-12T15:02:00+00:00 | Event 024 — Email from Maya Chen (Property Manager, Northbridge Lettings) |
| 24 | 2025-04-12T16:42:00+00:00 | Event 025 — Portal from Nora Bell (Tenant) |

## Final decision — system case `613532f9953b`

- **Decision (policy outcome):** **HUMAN REVIEW**
- **Proposed next action:** `clarify` — Burning smell and warm kitchen socket (category other)
- **Next step:** Verify the person, property and work item mapping.
- **Owner:** case manager
- **Case state:** open · policy v1

**Latest reading (claude-opus-5, high confidence, route `urgent_hazard`):** Tenant Nora Bell has returned to the property and reports the faint burning smell is still noticeable near the kitchen counter. The socket has not been used, no breaker has been switched off, and no inspection has taken place; landlord authority is still outstanding.

**Why:** Persistent burning smell near an electrical socket with no inspection or isolation is a possible immediate electrical/fire hazard requiring a case manager.

### Actions taken

- **No operational action was executed.** Nothing was booked, instructed, paid or sent. The system recorded readings, claims and policy assessments only.

### Escalated to a person (handover)

| Check | Owner | Rule | What the person must resolve | Evidence |
|---|---|---|---|---|
| `identity` | case manager | `require-identity` | Verify the person, property and work item mapping. | no source recorded |
| `route` | case manager | `require-route` | Verify the recipient and permitted communication route. | no source recorded |
| `triage` | case manager | `require-triage` | Claude read this as a possible urgent hazard. A case manager must take over now and apply the urgent procedure. | Event 014 — Email from Maya Chen (Property Manager, Northbridge Lettings) |

### Missing information and conflicting facts

- **access**: Tenant is now back at the property but has not explicitly granted permission for a contractor to attend and enter.
- **issue_details**: Whether the socket is still warm, and whether the circuit should be isolated at the consumer unit, is not stated.
- 27 extracted claim(s) remain **unverified source assertions** (see REASONING.md); none was treated as verified authority.

## Failures

- None recorded. (Jev and Claude calls all returned; no workflow step failed.)

## Result

No approval was invented and no human response was supplied by the runner. The case is waiting on the person(s) listed in the handover above.

Trace: `REASONING.md` (why) · `AUDIT.md` (every step, actor and tool) · `evidence.json` / `records.jsonl` (raw records) · `checkpoint-NNN.json` (state after each source; kept in the local run directory, not published).
