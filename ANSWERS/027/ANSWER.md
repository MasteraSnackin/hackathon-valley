# Property Management — case 027: Move-out maintenance at 46 Fernwick Lane

> **Run assumption:** the `identity` and `route` check(s) were set aside by policy (`assumed_checks`): treated as satisfied unless a source contradicted them. Nothing was verified; every other gate (access, authority, schedule, completion, money, triage) still applied.

- **Property (as supplied, unverified):** 46 Fernwick Lane, Aldermead, ZZ1 1ZZ
- **Decision cutoff:** 2025-09-15T16:25:18+00:00
- **Runner status:** **settled** · execution `native_local` · sources processed 19 of 19
- **Models:** Claude `claude-opus-5` (triage effort medium); Jev `jev-1.13.0` routing
- **Commit:** `281c95a90dc8a3ddd9424b56d5decf0d9c521178` · input SHA-256 `b19592d3a8ee5d53…`

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

## Final decision — system case `b9a856082df5`

- **Decision (policy outcome):** **HUMAN REVIEW**
- **Proposed next action:** `request_quote` — Stained and faded carpets - replacement quote (category other)
- **Next step:** A case manager must define a supported action for this situation.
- **Owner:** case manager
- **Case state:** open · policy v2
- **Split from system case** `a4791baab609` as a separate issue.

**Latest reading (model, medium confidence, route `request_quote`):** Checkout report PDF for 46 Fernwick Lane listing move-out defects, largely matching the quoted schedule of works. It additionally records a boiler casing apparently held with tape requiring inspection, kitchen flooring/worktop damage, missing curtain pole/curtains/bulbs and stained carpets with a replacement quotation requested.

### Actions taken

- **No operational action was executed.** Nothing was booked, instructed, paid or sent. The system recorded readings, claims and policy assessments only.

### Escalated to a person (handover)

| Check | Owner | Rule | What the person must resolve | Evidence |
|---|---|---|---|---|
| `supported` | case manager | `require-supported` | A case manager must define a supported action for this situation. | no source recorded |

### Missing information and conflicting facts

- None recorded by the latest reading.

## Final decision — system case `9ce726ac61cb`

- **Decision (policy outcome):** **HUMAN REVIEW**
- **Proposed next action:** `clarify` — Boiler casing taped, inspection required (category appliance)
- **Next step:** Claude read this as a possible urgent hazard. A case manager must take over now and apply the urgent procedure.
- **Owner:** case manager
- **Case state:** open · policy v2
- **Split from system case** `a4791baab609` as a separate issue.

**Latest reading (model, medium confidence, route `urgent_hazard`):** Checkout report PDF for 46 Fernwick Lane listing move-out defects, largely matching the quoted schedule of works. It additionally records a boiler casing apparently held with tape requiring inspection, kitchen flooring/worktop damage, missing curtain pole/curtains/bulbs and stained carpets with a replacement quotation requested.

### Actions taken

- **No operational action was executed.** Nothing was booked, instructed, paid or sent. The system recorded readings, claims and policy assessments only.

### Escalated to a person (handover)

| Check | Owner | Rule | What the person must resolve | Evidence |
|---|---|---|---|---|
| `triage` | case manager | `require-triage` | Claude read this as a possible urgent hazard. A case manager must take over now and apply the urgent procedure. | Split from case a4791baab609: Attachment checkout-report.pdf (PDF text extraction) |

### Missing information and conflicting facts

- None recorded by the latest reading.
- 2 extracted claim(s) remain **unverified source assertions** (see REASONING.md); none was treated as verified authority.

## Final decision — system case `9b8bef445795`

- **Decision (policy outcome):** **HUMAN REVIEW**
- **Proposed next action:** `request_quote` — Carpet replacement quote (category checkout_refurbishment)
- **Next step:** Verify the received source assertion. Confirm that the category and work item match the source request.
- **Owner:** case manager
- **Case state:** open · policy v2
- **Split from system case** `a4791baab609` as a separate issue.

**Latest reading (model, medium confidence, route `request_quote`):** Property manager logs a move-out schedule of damages and defects at 46 Fernwick Lane, covering joinery, window frame, decoration, flooring, missing items, carpets, radiators, extractor fans and water-damage/ceiling defects. The list also includes a non-working top-floor smoke detector and a boiler casing apparently held with tape needing inspection.

### Actions taken

- **No operational action was executed.** Nothing was booked, instructed, paid or sent. The system recorded readings, claims and policy assessments only.

### Escalated to a person (handover)

| Check | Owner | Rule | What the person must resolve | Evidence |
|---|---|---|---|---|
| `classification` | case manager | `require-classification` | Verify the received source assertion. Confirm that the category and work item match the source request. | Split from case a4791baab609: Intake report |

### Missing information and conflicting facts

- None recorded by the latest reading.
- 1 extracted claim(s) remain **unverified source assertions** (see REASONING.md); none was treated as verified authority.

## Final decision — system case `cff6dcbe178d`

- **Decision (policy outcome):** **HUMAN REVIEW**
- **Proposed next action:** `request_quote` — Water damage / ceiling defects in several rooms and warped kitchen worktop (category other)
- **Next step:** A case manager must define a supported action for this situation.
- **Owner:** case manager
- **Case state:** open · policy v2
- **Split from system case** `a4791baab609` as a separate issue.

**Latest reading (model, medium confidence, route `request_quote`):** Property manager logs a move-out schedule of damages and defects at 46 Fernwick Lane, covering joinery, window frame, decoration, flooring, missing items, carpets, radiators, extractor fans and water-damage/ceiling defects. The list also includes a non-working top-floor smoke detector and a boiler casing apparently held with tape needing inspection.

### Actions taken

- **No operational action was executed.** Nothing was booked, instructed, paid or sent. The system recorded readings, claims and policy assessments only.

### Escalated to a person (handover)

| Check | Owner | Rule | What the person must resolve | Evidence |
|---|---|---|---|---|
| `supported` | case manager | `require-supported` | A case manager must define a supported action for this situation. | no source recorded |

### Missing information and conflicting facts

- None recorded by the latest reading.

## Final decision — system case `b599635e332e`

- **Decision (policy outcome):** **HUMAN REVIEW**
- **Proposed next action:** `request_quote` — Kitchen radiator pulled away from wall and rusting radiators (category plumbing)
- **Next step:** Verify the received source assertion. Confirm that the category and work item match the source request.
- **Owner:** case manager
- **Case state:** open · policy v2
- **Split from system case** `a4791baab609` as a separate issue.

**Latest reading (model, medium confidence, route `request_quote`):** Property manager logs a move-out schedule of damages and defects at 46 Fernwick Lane, covering joinery, window frame, decoration, flooring, missing items, carpets, radiators, extractor fans and water-damage/ceiling defects. The list also includes a non-working top-floor smoke detector and a boiler casing apparently held with tape needing inspection.

### Actions taken

- **No operational action was executed.** Nothing was booked, instructed, paid or sent. The system recorded readings, claims and policy assessments only.

### Escalated to a person (handover)

| Check | Owner | Rule | What the person must resolve | Evidence |
|---|---|---|---|---|
| `classification` | case manager | `require-classification` | Verify the received source assertion. Confirm that the category and work item match the source request. | Split from case a4791baab609: Intake report |

### Missing information and conflicting facts

- None recorded by the latest reading.
- 1 extracted claim(s) remain **unverified source assertions** (see REASONING.md); none was treated as verified authority.

## Final decision — system case `518597ee00a8`

- **Decision (policy outcome):** **HUMAN REVIEW**
- **Proposed next action:** `clarify` — Boiler casing taped, inspection required (category appliance)
- **Next step:** Claude read this as a possible urgent hazard. A case manager must take over now and apply the urgent procedure.
- **Owner:** case manager
- **Case state:** open · policy v2
- **Split from system case** `a4791baab609` as a separate issue.

**Latest reading (model, medium confidence, route `urgent_hazard`):** Property manager logs a move-out schedule of damages and defects at 46 Fernwick Lane, covering joinery, window frame, decoration, flooring, missing items, carpets, radiators, extractor fans and water-damage/ceiling defects. The list also includes a non-working top-floor smoke detector and a boiler casing apparently held with tape needing inspection.

### Actions taken

- **No operational action was executed.** Nothing was booked, instructed, paid or sent. The system recorded readings, claims and policy assessments only.

### Escalated to a person (handover)

| Check | Owner | Rule | What the person must resolve | Evidence |
|---|---|---|---|---|
| `triage` | case manager | `require-triage` | Claude read this as a possible urgent hazard. A case manager must take over now and apply the urgent procedure. | Split from case a4791baab609: Intake report |

### Missing information and conflicting facts

- None recorded by the latest reading.
- 2 extracted claim(s) remain **unverified source assertions** (see REASONING.md); none was treated as verified authority.

## Final decision — system case `a1a4140a85bc`

- **Decision (policy outcome):** **HUMAN REVIEW**
- **Proposed next action:** `clarify` — Non-working top-floor smoke detector (category other)
- **Next step:** Claude read this as a possible urgent hazard. A case manager must take over now and apply the urgent procedure.
- **Owner:** case manager
- **Case state:** open · policy v2
- **Split from system case** `a4791baab609` as a separate issue.

**Latest reading (model, medium confidence, route `urgent_hazard`):** Property manager logs a move-out schedule of damages and defects at 46 Fernwick Lane, covering joinery, window frame, decoration, flooring, missing items, carpets, radiators, extractor fans and water-damage/ceiling defects. The list also includes a non-working top-floor smoke detector and a boiler casing apparently held with tape needing inspection.

### Actions taken

- **No operational action was executed.** Nothing was booked, instructed, paid or sent. The system recorded readings, claims and policy assessments only.

### Escalated to a person (handover)

| Check | Owner | Rule | What the person must resolve | Evidence |
|---|---|---|---|---|
| `triage` | case manager | `require-triage` | Claude read this as a possible urgent hazard. A case manager must take over now and apply the urgent procedure. | Split from case a4791baab609: Intake report |

### Missing information and conflicting facts

- None recorded by the latest reading.
- 1 extracted claim(s) remain **unverified source assertions** (see REASONING.md); none was treated as verified authority.

## Final decision — system case `a4791baab609`

- **Decision (policy outcome):** **WAIT**
- **Proposed next action:** `clarify` — Move-out schedule of damages and defects (category checkout_refurbishment)
- **Next step:** Clarify before routing: Checkout report items (kitchen flooring, warped worktop, boiler casing, curtain pole/curtains/bulbs, carpets) are not in the quoted scope; confirm whether the scope should be extended or separately quoted.
- **Owner:** case manager
- **Case state:** open · policy v2

**Latest reading (claude-opus-5, medium confidence, route `clarify`):** Contractor quotation NBL-027-Q1 from Alderwick Property Works for the move-out works at 46 Fernwick Lane, listing twelve tasks under a single "Labour & Materials" heading with a total of £3,865.68. No task-by-task pricing, exclusions or attendance date are given, and several checkout report items are not covered.

**Why:** Quotation document for the existing checkout refurbishment case; it cannot be instructed yet as the total exceeds the approval threshold with landlord approval outstanding, and the scope and pricing breakdown are unclear.

### Actions taken

- Drafted message to tenant: **awaiting_staff** (simulated channel; not sent to a real person) — “Hello, Thank you for your patience following the move-out at the property. We're currently going through the list of items noted at the end of the tenancy, which includes things like the staircase newel posts and bedroom door frame, marks and holes to walls, the kitchen flooring and living room lami …”
- Drafted message to tenant: **awaiting_staff** (simulated channel; not sent to a real person) — “Hello, Thank you for your patience while we work through the move-out list for the property. So that we can take the next steps correctly, could you let us know which of the listed items you consider to be your responsibility, and whether there are any you'd like to query or discuss further? A singl …”
- Drafted message to tenant: **awaiting_staff** (simulated channel; not sent to a real person) — “Hello, We're reviewing the works listed following the move-out schedule of damages and defects, which includes items such as the damaged newel post, wall damage, ceiling stain-blocking and redecoration. So that we have a clear record, could you let us know which of the listed items you consider to b …”
- Drafted message to tenant: **awaiting_staff** (simulated channel; not sent to a real person) — “Hello, Thank you for your patience while we work through the move-out schedule of damages and defects at the property. So that we have everything recorded correctly, could you please help with two quick things: 1. Could you confirm which of the items noted at the end of the tenancy you consider to b …”
- Drafted message to tenant: **awaiting_staff** (simulated channel; not sent to a real person) — “Hello, Thank you for your patience regarding the move-out works at 46 Fernwick Lane. Comparing the checkout report with the quotation received, a few items from the report don't appear in the quoted scope: the kitchen flooring damage, the warped kitchen worktop, the boiler casing, the missing curtai …”
- Clarification `triage` to tenant: closed — Clarify before routing: Whether landlord approval is actually in place for these specific move-out works, or still outstanding.; Which listed items are tenant-chargeable damage versus landlord repair, and which need quotes first.
- Clarification `triage` to tenant: closed — Clarify before routing: Landlord approval is requested but not yet given; which items are tenant-chargeable versus landlord repair remains unresolved.
- Clarification `classification` to tenant: closed — Confirm that the category and work item match the source request.
- Clarification `triage` to tenant: open — Clarify before routing: Checkout report items (kitchen flooring, warped worktop, boiler casing, curtain pole/curtains/bulbs, carpets) are not in the quoted scope; confirm whether the scope should be extended or separately quoted.

### Escalated to a person (handover)

| Check | Owner | Rule | What the person must resolve | Evidence |
|---|---|---|---|---|
| `triage` | case manager | `require-triage` | Claude read this as a possible urgent hazard. A case manager must take over now and apply the urgent procedure. | Attachment checkout-report.pdf (PDF text extraction) |

### Missing information and conflicting facts

- **issue_details** (blocks the route): Checkout report items (kitchen flooring, warped worktop, boiler casing, curtain pole/curtains/bulbs, carpets) are not in the quoted scope; confirm whether the scope should be extended or separately quoted.
- **issue_details**: The quotation gives a single "Labour & Materials" figure with no task-by-task prices, exclusions or VAT statement; confirm whether the £3,865.68 is the full comparable total including tax.
- **availability**: No attendance date is offered in the quotation; scheduling would need to be agreed after any approval.
- 7 extracted claim(s) remain **unverified source assertions** (see REASONING.md); none was treated as verified authority.

## Failures

- None recorded. (Jev and Claude calls all returned; no workflow step failed.)

## Result

No approval was invented and no human response was supplied by the runner. The case is waiting on the person(s) listed in the handover above.

Trace: `REASONING.md` (why) · `AUDIT.md` (every step, actor and tool) · `evidence.json` / `records.jsonl` (raw records) · `checkpoint-NNN.json` (state after each source; kept in the local run directory, not published).
