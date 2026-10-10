# Property Management — case 030: Maintenance report at 8 Brindlefern Walk

*PREPARATION ONLY — not official Reality Test results. System-generated; not edited by hand.*

- **Property (as supplied, unverified):** 8 Brindlefern Walk, Oakhollow, ZZ1 1ZZ
- **Decision cutoff:** 2025-09-06T18:42:00+00:00
- **Runner status:** **interrupted** · execution `see_partial_evidence` · sources processed 13 of 15
- **Models:** Claude `claude-opus-5` (triage effort medium); Jev `jev-1.13.0` routing
- **Commit:** `26542cfa3d481aa925490db741aa4fbab8f70e3c` · input SHA-256 `844a2a09984ae4c0…`

All operational tools in this run are clearly labelled **simulated** adapters: no real tenant, landlord or contractor was contacted, nothing was paid or booked, and a simulated receipt does not prove work happened.

## What the system received

The initial report and 14 further sources, submitted one at a time in availability order; each was processed and settled before the next became visible. Full text: `input.json`.

| # | Available at | Source |
|---|---|---|
| 0 | 2025-08-20T18:02:51+00:00 | Initial report — Event 001 — Portal |
| 1 | 2025-08-20T18:03:10+00:00 | Event 002 — Note from Ivo Merrick (Property Manager, Northbridge Lettings) |
| 2 | 2025-08-20T18:04:02+00:00 | Event 003 — Email from Ivo Merrick (Property Manager, Northbridge Lettings) |
| 3 | 2025-08-24T14:30:11+00:00 | Event 004 — Email from Ivo Merrick (Property Manager, Northbridge Lettings) |
| 4 | 2025-08-24T14:34:25+00:00 | Event 005 — Email from Ivo Merrick (Property Manager, Northbridge Lettings) |
| 5 | 2025-08-24T14:36:28+00:00 | Event 006 — Note from Ivo Merrick (Property Manager, Northbridge Lettings) |
| 6 | 2025-08-24T20:22:12+00:00 | Event 007 — Email from Tavian Rusk (Landlord) |
| 7 | 2025-08-24T20:22:31+00:00 | Event 008 — Email from Ivo Merrick (Property Manager, Northbridge Lettings) |
| 8 | 2025-08-24T20:22:36+00:00 | Event 009 — Email from Ivo Merrick (Property Manager, Northbridge Lettings) |
| 9 | 2025-08-24T20:23:09+00:00 | Event 010 — Email from Tavian Rusk (Landlord) |
| 10 | 2025-08-25T09:00:00+00:00 | Event 011 — Note from Ivo Merrick (Property Manager, Northbridge Lettings) |
| 11 | 2025-09-06T18:32:16+00:00 | Event 012 — Email from Tavian Rusk (Landlord) |
| 12 | 2025-09-06T18:35:00+00:00 | Event 013 — Note from Ivo Merrick (Property Manager, Northbridge Lettings) |
| 13 | 2025-09-06T18:40:11+00:00 | Event 014 — Email from Tavian Rusk (Landlord) |
| 14 | 2025-09-06T18:42:00+00:00 | Event 015 — Note from Ivo Merrick (Property Manager, Northbridge Lettings) |

## Final decision — system case `24dea22743a9`

- **Decision (policy outcome):** **HUMAN REVIEW**
- **Proposed next action:** `clarify` — Plug sockets coming away from the wall (category other)
- **Next step:** Verify the person, property and work item mapping.
- **Owner:** case manager
- **Case state:** open · policy v1
- **Split from system case** `ee907609b59c` as a separate issue.

**Latest reading (model, medium confidence, route `clarify`):** Landlord Tavian Rusk reiterates, in response to the sockets follow-up, that he will carry out the work himself and no external action is required. No completion date or evidence provided.

### Actions taken

- **No operational action was executed.** Nothing was booked, instructed, paid or sent. The system recorded readings, claims and policy assessments only.

### Escalated to a person (handover)

| Check | Owner | Rule | What the person must resolve | Evidence |
|---|---|---|---|---|
| `identity` | case manager | `require-identity` | Verify the person, property and work item mapping. | no source recorded |
| `route` | case manager | `require-route` | Verify the recipient and permitted communication route. | no source recorded |

### Missing information and conflicting facts

- None recorded by the latest reading.

## Final decision — system case `6d76c21f3a80`

- **Decision (policy outcome):** **HUMAN REVIEW**
- **Proposed next action:** `request_quote` — Plug sockets coming away from the wall (category other)
- **Next step:** Verify the person, property and work item mapping.
- **Owner:** case manager
- **Case state:** open · policy v1
- **Split from system case** `ee907609b59c` as a separate issue.

**Latest reading (model, medium confidence, route `request_quote`):** Property manager emails the landlord adding that the tenant also reported several plug sockets coming away from the wall, and asks whether these should be addressed too. No answer yet on the smoke alarm instruction.

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

## Final decision — system case `ee907609b59c`

- **Decision (policy outcome):** **HUMAN REVIEW**
- **Proposed next action:** `close_item` — Smoke alarm removed from upstairs landing ceiling (category other)
- **Next step:** Verify the person, property and work item mapping.
- **Owner:** case manager
- **Case state:** open · policy v1

**Latest reading (claude-opus-5, medium confidence, route `close_item`):** Internal note by the property manager recording the landlord's claim that the smoke alarm work was completed. No new information beyond the record.

**Why:** Internal note recording a completion claim for the current work item; close_item matches the router decision.

### Actions taken

- **No operational action was executed.** Nothing was booked, instructed, paid or sent. The system recorded readings, claims and policy assessments only.

### Escalated to a person (handover)

| Check | Owner | Rule | What the person must resolve | Evidence |
|---|---|---|---|---|
| `identity` | case manager | `require-identity` | Verify the person, property and work item mapping. | no source recorded |
| `commitments` | case manager | `require-commitments` | Resolve or explicitly cancel every outstanding commitment for this item. A verified route is required before asking externally. | no source recorded |
| `supported` | case manager | `require-supported` | A case manager must define a supported action for this situation. | no source recorded |
| `completion` | reviewer | `require-completion` | Verify completion of this work item with usable evidence. A verified route is required before asking externally. | Event 012 — Email from Tavian Rusk (Landlord), Event 013 — Note from Ivo Merrick (Property Manager, Northbridge Lettings) |

### Missing information and conflicting facts

- **completion**: No usable evidence (photo, certificate or inspection) of the smoke alarm reinstatement has been supplied; only the landlord's statement.
- 8 extracted claim(s) remain **unverified source assertions** (see REASONING.md); none was treated as verified authority.

## Failures

- Runner: Batch runner process was stopped when the operator's agent session ended, after 13 of 15 sources had settled. The runner itself recorded no result for this case; this status was written afterwards by the operator to mark the interruption. Partial evidence up to checkpoint-012 is preserved; nothing after that was processed.
- The run did not settle cleanly (status `interrupted`); any recorded state is partial.

## Result

No approval was invented and no human response was supplied by the runner. The case is waiting on the person(s) listed in the handover above.

Trace: `REASONING.md` (why) · `AUDIT.md` (every step, actor and tool) · `evidence.json` / `records.jsonl` (raw records) · `checkpoint-NNN.json` (state after each source; kept in the local run directory, not published).
