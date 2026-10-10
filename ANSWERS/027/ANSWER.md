# Property Management — case 027: Move-out maintenance at 46 Fernwick Lane

*PREPARATION ONLY — not official Reality Test results. System-generated; not edited by hand.*

- **Property (as supplied, unverified):** 46 Fernwick Lane, Aldermead, ZZ1 1ZZ
- **Decision cutoff:** 2025-09-15T16:25:18+00:00
- **Runner status:** **interrupted** · execution `see_partial_evidence` · sources processed 18 of 19
- **Models:** Claude `claude-opus-5` (triage effort medium); Jev `jev-1.13.0` routing
- **Commit:** `26542cfa3d481aa925490db741aa4fbab8f70e3c` · input SHA-256 `b19592d3a8ee5d53…`

All operational tools in this run are clearly labelled **simulated** adapters: no real tenant, landlord or contractor was contacted, nothing was paid or booked, and a simulated receipt does not prove work happened.

## What the system received

The initial report and 18 further sources, submitted one at a time in availability order; each was processed and settled before the next became visible. Full text: `input.json`.

| # | Available at | Source |
|---|---|---|
| 0 | 2025-09-03T18:03:18+00:00 | Initial report — Event 001 — Note |
| 1 | 2025-09-03T18:10:00+00:00 | Event 002 — Update from Northbridge Lettings workflow (System) |
| 2 | 2025-09-04T17:10:01+00:00 | Event 003 — Update from Maya Chen (Property Manager, Northbridge Lettings) |
| 3 | 2025-09-04T17:20:38+00:00 | Event 004 — Update from Northbridge Lettings workflow (System) |
| 4 | 2025-09-04T17:21:00+00:00 | Event 005 — Email from Maya Chen (Property Manager, Northbridge Lettings) |
| 5 | 2025-09-07T09:35:20+00:00 | Event 006 — Email from Iris Bell (Contractor, Alderwick Property Works) |
| 6 | 2025-09-07T11:27:12+00:00 | Event 007 — Email from Maya Chen (Property Manager, Northbridge Lettings) |
| 7 | 2025-09-07T11:34:16+00:00 | Event 008 — Email from Maya Chen (Property Manager, Northbridge Lettings) |
| 8 | 2025-09-08T11:58:33+00:00 | Event 009 — Email from Maya Chen (Property Manager, Northbridge Lettings) |
| 9 | 2025-09-10T08:34:20+00:00 | Event 010 — Call from Maya Chen (Property Manager, Northbridge Lettings) |
| 10 | 2025-09-11T11:33:24+00:00 | Event 011 — Email from Maya Chen (Property Manager, Northbridge Lettings) |
| 11 | 2025-09-14T13:32:28+00:00 | Event 012 — Email from Maya Chen (Property Manager, Northbridge Lettings) |
| 12 | 2025-09-15T13:52:12+00:00 | Event 013 — Email from Iris Bell (Contractor, Alderwick Property Works) |
| 13 | 2025-09-15T13:53:34+00:00 | Event 014 — Email from Maya Chen (Property Manager, Northbridge Lettings) |
| 14 | 2025-09-15T13:54:00+00:00 | Event 015 — Update from Maya Chen (Property Manager, Northbridge Lettings) |
| 15 | 2025-09-15T16:23:44+00:00 | Event 016 — Note from Maya Chen (Property Manager, Northbridge Lettings) |
| 16 | 2025-09-15T16:25:18+00:00 | Event 017 — Call from Maya Chen (Property Manager, Northbridge Lettings) |
| 17 | 2025-09-15T16:25:18+00:00 | Attachment checkout-report.pdf (PDF text extraction) |
| 18 | 2025-09-15T16:25:18+00:00 | Attachment move-out-works-quotation.pdf (PDF text extraction) |

## Final decision — system case `d61f9da8a2bf`

- **Decision (policy outcome):** **HUMAN REVIEW**
- **Proposed next action:** `clarify` — Boiler casing taped, inspection required; non-working smoke detector (category appliance)
- **Next step:** Verify the person, property and work item mapping.
- **Owner:** case manager
- **Case state:** open · policy v1
- **Split from system case** `018889c7a1bf` as a separate issue.

**Latest reading (model, medium confidence, route `urgent_hazard`):** Checkout report attachment listing move-out damage and defects at 46 Fernwick Lane, covering joinery, flooring, fittings, water damage, carpets and services. It also records a taped boiler casing requiring inspection and a non-working smoke detector.

### Actions taken

- **No operational action was executed.** Nothing was booked, instructed, paid or sent. The system recorded readings, claims and policy assessments only.

### Escalated to a person (handover)

| Check | Owner | Rule | What the person must resolve | Evidence |
|---|---|---|---|---|
| `identity` | case manager | `require-identity` | Verify the person, property and work item mapping. | no source recorded |
| `route` | case manager | `require-route` | Verify the recipient and permitted communication route. | no source recorded |
| `triage` | case manager | `require-triage` | Claude read this as a possible urgent hazard. A case manager must take over now and apply the urgent procedure. | Split from case 018889c7a1bf: Attachment checkout-report.pdf (PDF text extraction) |

### Missing information and conflicting facts

- None recorded by the latest reading.
- 3 extracted claim(s) remain **unverified source assertions** (see REASONING.md); none was treated as verified authority.

## Final decision — system case `addab47b8335`

- **Decision (policy outcome):** **HUMAN REVIEW**
- **Proposed next action:** `request_quote` — Carpet replacement quote (stained, faded carpets) (category checkout_refurbishment)
- **Next step:** Verify the person, property and work item mapping.
- **Owner:** case manager
- **Case state:** open · policy v1
- **Split from system case** `018889c7a1bf` as a separate issue.

**Latest reading (model, medium confidence, route `request_quote`):** Property manager logs a move-out damage and defect list for 46 Fernwick Lane covering joinery, window frame, flooring, fittings, water/ceiling damage, radiators, extractor fans, decoration and carpets, with a carpet replacement quote requested. The list also includes a non-working top-floor smoke detector and a boiler casing apparently held with tape needing inspection.

### Actions taken

- **No operational action was executed.** Nothing was booked, instructed, paid or sent. The system recorded readings, claims and policy assessments only.

### Escalated to a person (handover)

| Check | Owner | Rule | What the person must resolve | Evidence |
|---|---|---|---|---|
| `identity` | case manager | `require-identity` | Verify the person, property and work item mapping. | no source recorded |
| `route` | case manager | `require-route` | Verify the recipient and permitted communication route. | no source recorded |
| `classification` | case manager | `require-classification` | Confirm that the category and work item match the source request. A verified route is required before asking externally. | Split from case 018889c7a1bf: Intake report |

### Missing information and conflicting facts

- None recorded by the latest reading.
- 1 extracted claim(s) remain **unverified source assertions** (see REASONING.md); none was treated as verified authority.

## Final decision — system case `43442048c443`

- **Decision (policy outcome):** **HUMAN REVIEW**
- **Proposed next action:** `clarify` — Non-working top-floor smoke detector and taped boiler casing (category other)
- **Next step:** Verify the person, property and work item mapping.
- **Owner:** case manager
- **Case state:** open · policy v1
- **Split from system case** `018889c7a1bf` as a separate issue.

**Latest reading (model, medium confidence, route `urgent_hazard`):** Property manager logs a move-out damage and defect list for 46 Fernwick Lane covering joinery, window frame, flooring, fittings, water/ceiling damage, radiators, extractor fans, decoration and carpets, with a carpet replacement quote requested. The list also includes a non-working top-floor smoke detector and a boiler casing apparently held with tape needing inspection.

### Actions taken

- **No operational action was executed.** Nothing was booked, instructed, paid or sent. The system recorded readings, claims and policy assessments only.

### Escalated to a person (handover)

| Check | Owner | Rule | What the person must resolve | Evidence |
|---|---|---|---|---|
| `identity` | case manager | `require-identity` | Verify the person, property and work item mapping. | no source recorded |
| `route` | case manager | `require-route` | Verify the recipient and permitted communication route. | no source recorded |
| `triage` | case manager | `require-triage` | Claude read this as a possible urgent hazard. A case manager must take over now and apply the urgent procedure. | Split from case 018889c7a1bf: Intake report |

### Missing information and conflicting facts

- None recorded by the latest reading.
- 1 extracted claim(s) remain **unverified source assertions** (see REASONING.md); none was treated as verified authority.

## Final decision — system case `018889c7a1bf`

- **Decision (policy outcome):** **HUMAN REVIEW**
- **Proposed next action:** `clarify` — Move-out damage and defect list (joinery, flooring, fittings, water damage, carpets) (category checkout_refurbishment)
- **Next step:** Verify the person, property and work item mapping.
- **Owner:** case manager
- **Case state:** open · policy v1

**Latest reading (claude-opus-5, medium confidence, route `urgent_hazard`):** Checkout report attachment listing move-out damage and defects at 46 Fernwick Lane, covering joinery, flooring, fittings, water damage, carpets and services. It also records a taped boiler casing requiring inspection and a non-working smoke detector.

**Why:** Document evidence supporting the existing checkout defect list; taped boiler casing and non-working smoke detector are possible safety hazards needing a person to review, consistent with the router decision.

### Actions taken

- **No operational action was executed.** Nothing was booked, instructed, paid or sent. The system recorded readings, claims and policy assessments only.

### Escalated to a person (handover)

| Check | Owner | Rule | What the person must resolve | Evidence |
|---|---|---|---|---|
| `identity` | case manager | `require-identity` | Verify the person, property and work item mapping. | no source recorded |
| `route` | case manager | `require-route` | Verify the recipient and permitted communication route. | no source recorded |
| `triage` | case manager | `require-triage` | Clarify before routing: The quotation gives only a single "Labour & Materials" heading with no total figure, no task-by-task prices and no stated exclusions, so the full comparable commitment including VAT cannot be esta … | Event 013 — Email from Iris Bell (Contractor, Alderwick Property Works) |

### Missing information and conflicting facts

- **issue_details** (blocks the route): Whether the carpet replacement quotation is included in the contractor's £3,865.68 quote or needs a separate quote.
- **issue_details** (blocks the route): Boiler and smoke detector safety items are not in the current quoted task list; confirm who inspects these.
- **completion**: Landlord approval of the quoted total of £3,865.68 remains outstanding.
- 8 extracted claim(s) remain **unverified source assertions** (see REASONING.md); none was treated as verified authority.

## Failures

- Runner: Batch runner process was stopped when the operator's agent session ended, after 18 of 19 sources had settled. The runner itself recorded no result for this case; this status was written afterwards by the operator to mark the interruption. Partial evidence up to checkpoint-017 is preserved; nothing after that was processed.
- The run did not settle cleanly (status `interrupted`); any recorded state is partial.

## Result

No approval was invented and no human response was supplied by the runner. The case is waiting on the person(s) listed in the handover above.

Trace: `REASONING.md` (why) · `AUDIT.md` (every step, actor and tool) · `evidence.json` / `records.jsonl` (raw records) · `checkpoint-NNN.json` (state after each source; kept in the local run directory, not published).
