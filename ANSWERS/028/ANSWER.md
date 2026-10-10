# Property Management — case 028: Move-out maintenance request

*PREPARATION ONLY — not official Reality Test results. System-generated; not edited by hand.*

- **Property (as supplied, unverified):** 42 Mallowfen Crescent, Ternwick, ZZ1 1ZZ
- **Decision cutoff:** 2025-09-18T14:50:04+00:00
- **Runner status:** **interrupted** · execution `see_partial_evidence` · sources processed 17 of 27
- **Models:** Claude `claude-opus-5` (triage effort medium); Jev `jev-1.13.0` routing
- **Commit:** `26542cfa3d481aa925490db741aa4fbab8f70e3c` · input SHA-256 `620be9402d7849fe…`

All operational tools in this run are clearly labelled **simulated** adapters: no real tenant, landlord or contractor was contacted, nothing was paid or booked, and a simulated receipt does not prove work happened.

## What the system received

The initial report and 26 further sources, submitted one at a time in availability order; each was processed and settled before the next became visible. Full text: `input.json`.

| # | Available at | Source |
|---|---|---|
| 0 | 2025-09-04T10:50:28+00:00 | Initial report — Event 001 — Note |
| 1 | 2025-09-04T11:03:00+00:00 | Event 002 — Note from Talia Wren (Property Manager, Northbridge Lettings) |
| 2 | 2025-09-04T17:18:42+00:00 | Event 003 — Email from Talia Wren (Property Manager, Northbridge Lettings) |
| 3 | 2025-09-04T17:18:59+00:00 | Event 004 — Email from Talia Wren (Property Manager, Northbridge Lettings) |
| 4 | 2025-09-04T17:25:54+00:00 | Event 005 — Email from Talia Wren (Property Manager, Northbridge Lettings) |
| 5 | 2025-09-07T17:18:42+00:00 | Event 006 — Email from Talia Wren (Property Manager, Northbridge Lettings) |
| 6 | 2025-09-08T17:18:26+00:00 | Event 007 — Update from Oren Pell (Maintenance Coordinator, Northbridge Lettings) |
| 7 | 2025-09-09T08:57:58+00:00 | Event 008 — Email from Talia Wren (Property Manager, Northbridge Lettings) |
| 8 | 2025-09-09T09:01:17+00:00 | Event 009 — Call from Talia Wren (Property Manager, Northbridge Lettings) |
| 9 | 2025-09-09T09:05:00+00:00 | Event 010 — Note from Talia Wren (Property Manager, Northbridge Lettings) |
| 10 | 2025-09-10T15:29:25+00:00 | Event 011 — Note from Talia Wren (Property Manager, Northbridge Lettings) |
| 11 | 2025-09-10T15:30:11+00:00 | Event 012 — Email from Talia Wren (Property Manager, Northbridge Lettings) |
| 12 | 2025-09-10T15:57:41+00:00 | Event 013 — Note from Talia Wren (Property Manager, Northbridge Lettings) |
| 13 | 2025-09-10T16:00:19+00:00 | Event 014 — Call from Talia Wren (Property Manager, Northbridge Lettings) |
| 14 | 2025-09-11T16:20:40+00:00 | Event 015 — Email from Talia Wren (Property Manager, Northbridge Lettings) |
| 15 | 2025-09-11T16:21:23+00:00 | Event 016 — Note from Talia Wren (Property Manager, Northbridge Lettings) |
| 16 | 2025-09-13T07:59:11+00:00 | Event 017 — Email from Elowen Quill (Landlord, private owner) |
| 17 | 2025-09-14T11:58:04+00:00 | Event 018 — Note from Talia Wren (Property Manager, Northbridge Lettings) |
| 18 | 2025-09-14T11:58:20+00:00 | Event 019 — Email from Talia Wren (Property Manager, Northbridge Lettings) |
| 19 | 2025-09-14T11:58:29+00:00 | Event 020 — Email from Talia Wren (Property Manager, Northbridge Lettings) |
| 20 | 2025-09-18T05:45:11+00:00 | Event 021 — Email from Elowen Quill (Landlord, private owner) |
| 21 | 2025-09-18T08:21:35+00:00 | Event 022 — Update from Oren Pell (Maintenance Coordinator, Northbridge Lettings) |
| 22 | 2025-09-18T08:46:00+00:00 | Event 023 — Email from Talia Wren (Property Manager, Northbridge Lettings) |
| 23 | 2025-09-18T14:49:44+00:00 | Event 024 — Update from Oren Pell (Maintenance Coordinator, Northbridge Lettings) |
| 24 | 2025-09-18T14:50:04+00:00 | Event 025 — Note from Talia Wren (Property Manager, Northbridge Lettings) |
| 25 | 2025-09-18T14:50:04+00:00 | Attachment checkout-report.pdf (PDF text extraction) |
| 26 | 2025-09-18T14:50:04+00:00 | Attachment provider-quotation.pdf (PDF text extraction) |

## Final decision — system case `0d3eb95fa947`

- **Decision (policy outcome):** **HUMAN REVIEW**
- **Proposed next action:** `request_quote` — Remove sticker residue from front door (category checkout_cleaning)
- **Next step:** Verify the person, property and work item mapping.
- **Owner:** case manager
- **Case state:** open · policy v1
- **Split from system case** `1c6fcba54ae6` as a separate issue.

**Latest reading (model, medium confidence, route `request_quote`):** Property manager opens case NBL-028 for move-out works at a vacant property: electric meter cabinet door hinges, nail removal and paint touch-up in Bedroom 1, and sticker residue on the front door. An internal note states landlord approval was already given for the move-out works.

### Actions taken

- **No operational action was executed.** Nothing was booked, instructed, paid or sent. The system recorded readings, claims and policy assessments only.

### Escalated to a person (handover)

| Check | Owner | Rule | What the person must resolve | Evidence |
|---|---|---|---|---|
| `identity` | case manager | `require-identity` | Verify the person, property and work item mapping. | no source recorded |
| `route` | case manager | `require-route` | Verify the recipient and permitted communication route. | no source recorded |
| `classification` | case manager | `require-classification` | Confirm that the category and work item match the source request. A verified route is required before asking externally. | Split from case 1c6fcba54ae6: Intake report |

### Missing information and conflicting facts

- None recorded by the latest reading.
- 1 extracted claim(s) remain **unverified source assertions** (see REASONING.md); none was treated as verified authority.

## Final decision — system case `4c619fd9cebe`

- **Decision (policy outcome):** **HUMAN REVIEW**
- **Proposed next action:** `request_quote` — Remove four wall nails in Bedroom 1 and touch up paint (category checkout_refurbishment)
- **Next step:** Verify the person, property and work item mapping.
- **Owner:** case manager
- **Case state:** open · policy v1
- **Split from system case** `1c6fcba54ae6` as a separate issue.

**Latest reading (model, medium confidence, route `request_quote`):** Property manager opens case NBL-028 for move-out works at a vacant property: electric meter cabinet door hinges, nail removal and paint touch-up in Bedroom 1, and sticker residue on the front door. An internal note states landlord approval was already given for the move-out works.

### Actions taken

- **No operational action was executed.** Nothing was booked, instructed, paid or sent. The system recorded readings, claims and policy assessments only.

### Escalated to a person (handover)

| Check | Owner | Rule | What the person must resolve | Evidence |
|---|---|---|---|---|
| `identity` | case manager | `require-identity` | Verify the person, property and work item mapping. | no source recorded |
| `route` | case manager | `require-route` | Verify the recipient and permitted communication route. | no source recorded |
| `classification` | case manager | `require-classification` | Confirm that the category and work item match the source request. A verified route is required before asking externally. | Split from case 1c6fcba54ae6: Intake report |

### Missing information and conflicting facts

- None recorded by the latest reading.
- 1 extracted claim(s) remain **unverified source assertions** (see REASONING.md); none was treated as verified authority.

## Final decision — system case `1c6fcba54ae6`

- **Decision (policy outcome):** **HUMAN REVIEW**
- **Proposed next action:** `confirm_appointment` — Electric meter cabinet door hinges repair or replacement (category doors_locks)
- **Next step:** Verify the person, property and work item mapping.
- **Owner:** case manager
- **Case state:** open · policy v1

**Latest reading (claude-opus-5, medium confidence, route `confirm_appointment`):** The landlord declined the agency provider's £564.48 quote and says she will arrange her own company to carry out the work on Wednesday morning, during the cleaning visit.

**Why:** Landlord rejects agency quote and proposes own contractor on Wednesday morning; router chose confirm_appointment and the message is largely about arranging that visit, though authority decline is the key fact.

### Actions taken

- **No operational action was executed.** Nothing was booked, instructed, paid or sent. The system recorded readings, claims and policy assessments only.

### Escalated to a person (handover)

| Check | Owner | Rule | What the person must resolve | Evidence |
|---|---|---|---|---|
| `identity` | case manager | `require-identity` | Verify the person, property and work item mapping. | no source recorded |
| `route` | case manager | `require-route` | Verify the recipient and permitted communication route. | no source recorded |
| `access` | access officer | `require-access` | Record consent for this visit and access method from the authorised person. A verified route is required before asking externally. | no source recorded |
| `authority` | approver | `require-authority` | Obtain authority for this work item, provider and action. | no source recorded |
| `schedule` | case manager | `require-schedule` | Confirm the active appointment with a precise date and time. A verified route is required before asking externally. | no source recorded |
| `triage` | case manager | `require-triage` | Clarify before routing: Unclear whether the landlord's own company covers all three bundled areas or only part, and whether the agency item should now be closed. A verified route is required before asking externally. | Event 017 — Email from Elowen Quill (Landlord, private owner) |

### Missing information and conflicting facts

- **issue_details** (blocks the route): Unclear whether the landlord's own company covers all three bundled areas or only part, and whether the agency item should now be closed.
- **availability**: "Wednesday morning" has no date or time window; the appointment with the landlord's own company is not confirmed with the desk.
- **access**: No explicit consent or access arrangement stated for the landlord's own contractor to enter, and overlap with the cleaning visit needs checking.
- 5 extracted claim(s) remain **unverified source assertions** (see REASONING.md); none was treated as verified authority.

## Failures

- Runner: Batch runner process was stopped when the operator's agent session ended, after 17 of 27 sources had settled. The runner itself recorded no result for this case; this status was written afterwards by the operator to mark the interruption. Partial evidence up to checkpoint-016 is preserved; nothing after that was processed.
- The run did not settle cleanly (status `interrupted`); any recorded state is partial.

## Result

No approval was invented and no human response was supplied by the runner. The case is waiting on the person(s) listed in the handover above.

Trace: `REASONING.md` (why) · `AUDIT.md` (every step, actor and tool) · `evidence.json` / `records.jsonl` (raw records) · `checkpoint-NNN.json` (state after each source; kept in the local run directory, not published).
