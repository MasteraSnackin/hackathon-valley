# Property Management — case 006: Solar generation readings

*PREPARATION ONLY — not official Reality Test results. System-generated; not edited by hand.*

- **Property (as supplied, unverified):** 14 Brindlefern Walk, Larkmere, ZZ1 1ZZ
- **Decision cutoff:** 2025-09-18T17:42:00+00:00
- **Runner status:** **settled** · execution `native_local` · sources processed 17 of 17
- **Models:** Claude `claude-opus-5` (triage effort medium); Jev `jev-1.13.0` routing
- **Commit:** `26542cfa3d481aa925490db741aa4fbab8f70e3c` · input SHA-256 `7effc3b79ac36a3d…`

All operational tools in this run are clearly labelled **simulated** adapters: no real tenant, landlord or contractor was contacted, nothing was paid or booked, and a simulated receipt does not prove work happened.

## What the system received

The initial report and 16 further sources, submitted one at a time in availability order; each was processed and settled before the next became visible. Full text: `input.json`.

| # | Available at | Source |
|---|---|---|
| 0 | 2025-09-03T09:10:00+00:00 | Initial report — Event 001 — Call |
| 1 | 2025-09-03T09:26:00+00:00 | Event 002 — Note from Maya Chen (Property Manager, Northbridge Lettings) |
| 2 | 2025-09-03T09:31:00+00:00 | Event 003 — Update from Northbridge Lettings workflow (System) |
| 3 | 2025-09-03T09:44:00+00:00 | Event 004 — Email from Northbridge Lettings workflow (System) |
| 4 | 2025-09-03T11:18:00+00:00 | Event 005 — Note from Maya Chen (Property Manager, Northbridge Lettings) |
| 5 | 2025-09-03T11:36:00+00:00 | Event 006 — Email from Maya Chen (Property Manager, Northbridge Lettings) |
| 6 | 2025-09-03T13:05:00+00:00 | Event 007 — Update from Maya Chen (Property Manager, Northbridge Lettings) |
| 7 | 2025-09-03T13:20:00+00:00 | Event 008 — Note from Maya Chen (Property Manager, Northbridge Lettings) |
| 8 | 2025-09-08T10:15:00+00:00 | Event 009 — Update from Northbridge Lettings workflow (System) |
| 9 | 2025-09-09T09:40:00+00:00 | Event 010 — Email from Maya Chen (Property Manager, Northbridge Lettings) |
| 10 | 2025-09-09T09:52:00+00:00 | Event 011 — Note from Maya Chen (Property Manager, Northbridge Lettings) |
| 11 | 2025-09-14T10:05:00+00:00 | Event 012 — Update from Northbridge Lettings workflow (System) |
| 12 | 2025-09-14T10:35:00+00:00 | Event 013 — Email from Maya Chen (Property Manager, Northbridge Lettings) |
| 13 | 2025-09-14T10:38:00+00:00 | Event 014 — SMS from Maya Chen (Property Manager, Northbridge Lettings) |
| 14 | 2025-09-17T10:40:00+00:00 | Event 015 — Update from Northbridge Lettings workflow (System) |
| 15 | 2025-09-18T14:42:00+00:00 | Event 016 — Email from Maya Chen (Property Manager, Northbridge Lettings) |
| 16 | 2025-09-18T17:42:00+00:00 | Event 017 — Email from Ivo Mercer (Tenant) |

## Final decision — system case `f33754f31e7c`

- **Decision (policy outcome):** **HUMAN REVIEW**
- **Proposed next action:** `clarify` — Request for solar generation readings (category other)
- **Next step:** Verify the person, property and work item mapping.
- **Owner:** case manager
- **Case state:** open · policy v1

**Latest reading (claude-opus-5, medium confidence, route `clarify`):** Tenant Ivo Mercer replied that the solar generation readings were already supplied around two weeks ago, stating his wife phoned and emailed the office. No figures or image were included in this reply.

**Why:** Reply asserts prior supply but provides no readings or evidence; clarification needed before closing, matching router decision.

### Actions taken

- **No operational action was executed.** Nothing was booked, instructed, paid or sent. The system recorded readings, claims and policy assessments only.

### Escalated to a person (handover)

| Check | Owner | Rule | What the person must resolve | Evidence |
|---|---|---|---|---|
| `identity` | case manager | `require-identity` | Verify the person, property and work item mapping. | no source recorded |
| `route` | case manager | `require-route` | Verify the recipient and permitted communication route. | no source recorded |
| `triage` | case manager | `require-triage` | Clarify before routing: Unclear what readings are wanted (period, format) and whether the desk holds or can obtain solar generation data; no maintenance action identified. A verified route is required before asking exter … | Intake report |

### Missing information and conflicting facts

- **issue_details** (blocks the route): Tenant says readings were already sent via phone/email by his wife, but no figures or photo are in this reply; search inbox/call logs or ask for the reading to be resent.
- **completion** (blocks the route): Confirm whether the earlier submission satisfies the landlord's request so the item can be closed.

## Failures

- None recorded. (Jev and Claude calls all returned; no workflow step failed.)

## Result

No approval was invented and no human response was supplied by the runner. The case is waiting on the person(s) listed in the handover above.

Trace: `REASONING.md` (why) · `AUDIT.md` (every step, actor and tool) · `evidence.json` / `records.jsonl` (raw records) · `checkpoint-NNN.json` (state after each source; kept in the local run directory, not published).
