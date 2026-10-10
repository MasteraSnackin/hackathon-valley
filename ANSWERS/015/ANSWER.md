# Property Management — case 015: Vacant Property Preparation

*PREPARATION ONLY — not official Reality Test results. System-generated; not edited by hand.*

- **Property (as supplied, unverified):** 18 Thistlevaunt Lane, Orvelune, ZZ1 1ZZ
- **Decision cutoff:** 2025-09-25T08:34:11+00:00
- **Runner status:** **settled** · execution `native_local` · sources processed 23 of 23
- **Models:** Claude `claude-opus-5` (triage effort medium); Jev `jev-1.13.0` routing
- **Commit:** `26542cfa3d481aa925490db741aa4fbab8f70e3c` · input SHA-256 `d5cae21c4bb3d30b…`

All operational tools in this run are clearly labelled **simulated** adapters: no real tenant, landlord or contractor was contacted, nothing was paid or booked, and a simulated receipt does not prove work happened.

## What the system received

The initial report and 22 further sources, submitted one at a time in availability order; each was processed and settled before the next became visible. Full text: `input.json`.

| # | Available at | Source |
|---|---|---|
| 0 | 2025-09-03T18:04:18+00:00 | Initial report — Event 001 — Note |
| 1 | 2025-09-04T17:20:08+00:00 | Event 002 — Email from Mira Venn (Property Manager, Northbridge Lettings) |
| 2 | 2025-09-04T17:27:48+00:00 | Event 003 — Email from Mira Venn (Property Manager, Northbridge Lettings) |
| 3 | 2025-09-07T09:59:05+00:00 | Event 004 — Email from Elian Wren (Contractor, Brindlewick Turnover Services) |
| 4 | 2025-09-07T11:33:00+00:00 | Event 005 — Email from Mira Venn (Property Manager, Northbridge Lettings) |
| 5 | 2025-09-08T13:25:03+00:00 | Event 006 — Email from Elian Wren (Contractor, Brindlewick Turnover Services) |
| 6 | 2025-09-08T13:26:14+00:00 | Event 007 — Email from Mira Venn (Property Manager, Northbridge Lettings) |
| 7 | 2025-09-08T15:45:30+00:00 | Event 008 — Email from Nessa Quill (Landlord, Property Owner) |
| 8 | 2025-09-08T15:46:20+00:00 | Event 009 — Email from Mira Venn (Property Manager, Northbridge Lettings) |
| 9 | 2025-09-08T16:43:12+00:00 | Event 010 — Email from Nessa Quill (Landlord, Property Owner) |
| 10 | 2025-09-10T10:27:45+00:00 | Event 011 — Email from Mira Venn (Property Manager, Northbridge Lettings) |
| 11 | 2025-09-10T10:54:32+00:00 | Event 012 — Email from Mira Venn (Property Manager, Northbridge Lettings) |
| 12 | 2025-09-10T11:07:05+00:00 | Event 013 — Email from Elian Wren (Contractor, Brindlewick Turnover Services) |
| 13 | 2025-09-15T17:08:05+00:00 | Event 014 — Email from Elian Wren (Contractor, Brindlewick Turnover Services) |
| 14 | 2025-09-16T07:31:55+00:00 | Event 015 — Email from Mira Venn (Property Manager, Northbridge Lettings) |
| 15 | 2025-09-17T15:38:24+00:00 | Event 016 — Update from Nessa Quill (Landlord, Property Owner) |
| 16 | 2025-09-17T16:19:33+00:00 | Event 017 — Email from Mira Venn (Property Manager, Northbridge Lettings) |
| 17 | 2025-09-18T16:27:18+00:00 | Event 018 — Note from Tovan Rusk (Maintenance Coordinator, Northbridge Lettings) |
| 18 | 2025-09-21T17:41:01+00:00 | Event 019 — Call from Mira Venn (Property Manager, Northbridge Lettings) |
| 19 | 2025-09-22T08:27:47+00:00 | Event 020 — Note from Tovan Rusk (Maintenance Coordinator, Northbridge Lettings) |
| 20 | 2025-09-25T08:34:11+00:00 | Event 021 — Update from Mira Venn (Property Manager, Northbridge Lettings) |
| 21 | 2025-09-25T08:34:11+00:00 | Attachment move-out-inspection-report.pdf (PDF text extraction) |
| 22 | 2025-09-25T08:34:11+00:00 | Attachment property-preparation-quotation.pdf (PDF text extraction) |

## Final decision — system case `51f093b54cd9`

- **Decision (policy outcome):** **HUMAN REVIEW**
- **Proposed next action:** `clarify` — Rear garden weeding, grass cutting and tidy (category garden)
- **Next step:** Verify the person, property and work item mapping.
- **Owner:** case manager
- **Case state:** open · policy v1
- **Split from system case** `680c8f82e05f` as a separate issue.

**Latest reading (model, medium confidence, route `clarify`):** Contractor quotation NBL-015-Q1 from Brindlewick Turnover Services for property preparation at 18 Thistlevaunt Lane, totalling £665.00. Scope includes oven/extractor degreasing, limescale treatment, rubbish removal, carpet shampooing and rear garden tidying; no visit date is given.

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

## Final decision — system case `4d948ac1bf18`

- **Decision (policy outcome):** **HUMAN REVIEW**
- **Proposed next action:** `request_quote` — Rear garden clearance including bagged dog waste and disturbed soil (category garden)
- **Next step:** Verify the person, property and work item mapping.
- **Owner:** case manager
- **Case state:** open · policy v1
- **Split from system case** `680c8f82e05f` as a separate issue.

**Latest reading (model, medium confidence, route `request_quote`):** An extracted move-out inspection report for 18 Thistlevaunt Lane lists the post-tenancy preparation items: kitchen/oven/extractor degreasing, bathroom and en-suite limescale removal and waste removal, matching the current checkout clean item. It also records rear garden clearance (including bagged dog waste) and disturbed soil, which are not part of the current work item.

### Actions taken

- **No operational action was executed.** Nothing was booked, instructed, paid or sent. The system recorded readings, claims and policy assessments only.

### Escalated to a person (handover)

| Check | Owner | Rule | What the person must resolve | Evidence |
|---|---|---|---|---|
| `identity` | case manager | `require-identity` | Verify the person, property and work item mapping. | no source recorded |
| `route` | case manager | `require-route` | Verify the recipient and permitted communication route. | no source recorded |
| `classification` | case manager | `require-classification` | Confirm that the category and work item match the source request. A verified route is required before asking externally. | Split from case 680c8f82e05f: Attachment move-out-inspection-report.pdf (PDF text extraction) |

### Missing information and conflicting facts

- None recorded by the latest reading.
- 1 extracted claim(s) remain **unverified source assertions** (see REASONING.md); none was treated as verified authority.

## Final decision — system case `2745b724fbe3`

- **Decision (policy outcome):** **HUMAN REVIEW**
- **Proposed next action:** `clarify` — Separate major maintenance works outstanding at property (category other)
- **Next step:** Verify the person, property and work item mapping.
- **Owner:** case manager
- **Case state:** open · policy v1
- **Split from system case** `680c8f82e05f` as a separate issue.

**Latest reading (model, medium confidence, route `clarify`):** Mira Venn tells the contractor the checkout clean remains on hold because separate major maintenance is outstanding. A prospective tenant wants to move in on 28 September, and landlord approval of the separate maintenance quote had not been received.

### Actions taken

- **No operational action was executed.** Nothing was booked, instructed, paid or sent. The system recorded readings, claims and policy assessments only.

### Escalated to a person (handover)

| Check | Owner | Rule | What the person must resolve | Evidence |
|---|---|---|---|---|
| `identity` | case manager | `require-identity` | Verify the person, property and work item mapping. | no source recorded |
| `route` | case manager | `require-route` | Verify the recipient and permitted communication route. | no source recorded |

### Missing information and conflicting facts

- None recorded by the latest reading.

## Final decision — system case `4ca85da308ff`

- **Decision (policy outcome):** **HUMAN REVIEW**
- **Proposed next action:** `request_quote` — Rear garden clearance including bagged dog waste (category garden)
- **Next step:** Verify the person, property and work item mapping.
- **Owner:** case manager
- **Case state:** open · policy v1
- **Split from system case** `680c8f82e05f` as a separate issue.

**Latest reading (model, high confidence, route `request_quote`):** Mira Venn has asked contractor Brindlewick Turnover Services for a price and earliest availability for the post-tenancy cleaning, waste removal and garden clearance. She states the property is vacant and keys can be collected from the Northbridge Lettings office.

### Actions taken

- **No operational action was executed.** Nothing was booked, instructed, paid or sent. The system recorded readings, claims and policy assessments only.

### Escalated to a person (handover)

| Check | Owner | Rule | What the person must resolve | Evidence |
|---|---|---|---|---|
| `identity` | case manager | `require-identity` | Verify the person, property and work item mapping. | no source recorded |
| `route` | case manager | `require-route` | Verify the recipient and permitted communication route. | no source recorded |

### Missing information and conflicting facts

- None recorded by the latest reading.

## Final decision — system case `9f3574a409ac`

- **Decision (policy outcome):** **HUMAN REVIEW**
- **Proposed next action:** `clarify` — Soil disturbed by digging in garden - scope unclear (category inspection)
- **Next step:** Verify the person, property and work item mapping.
- **Owner:** case manager
- **Case state:** open · policy v1
- **Split from system case** `680c8f82e05f` as a separate issue.

**Latest reading (model, medium confidence, route `clarify`):** Property Manager logs post-move-out works at a vacant property: cleaning of kitchen, oven, extractor, bathroom and en-suite limescale, removal of waste left in the kitchen, and rear garden clearance including bagged dog waste. Inspection notes also mention disturbed soil from digging.

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

## Final decision — system case `6db6e1b9fd6f`

- **Decision (policy outcome):** **HUMAN REVIEW**
- **Proposed next action:** `request_quote` — Rear garden clearance including bagged dog waste (category garden)
- **Next step:** Verify the person, property and work item mapping.
- **Owner:** case manager
- **Case state:** open · policy v1
- **Split from system case** `680c8f82e05f` as a separate issue.

**Latest reading (model, medium confidence, route `request_quote`):** Property Manager logs post-move-out works at a vacant property: cleaning of kitchen, oven, extractor, bathroom and en-suite limescale, removal of waste left in the kitchen, and rear garden clearance including bagged dog waste. Inspection notes also mention disturbed soil from digging.

### Actions taken

- **No operational action was executed.** Nothing was booked, instructed, paid or sent. The system recorded readings, claims and policy assessments only.

### Escalated to a person (handover)

| Check | Owner | Rule | What the person must resolve | Evidence |
|---|---|---|---|---|
| `identity` | case manager | `require-identity` | Verify the person, property and work item mapping. | no source recorded |
| `route` | case manager | `require-route` | Verify the recipient and permitted communication route. | no source recorded |
| `classification` | case manager | `require-classification` | Confirm that the category and work item match the source request. A verified route is required before asking externally. | Split from case 680c8f82e05f: Intake report |

### Missing information and conflicting facts

- None recorded by the latest reading.
- 1 extracted claim(s) remain **unverified source assertions** (see REASONING.md); none was treated as verified authority.

## Final decision — system case `680c8f82e05f`

- **Decision (policy outcome):** **HUMAN REVIEW**
- **Proposed next action:** `confirm_appointment` — Checkout clean: kitchen, oven, extractor, bathroom/en-suite limescale, waste removal (category checkout_cleaning)
- **Next step:** Verify the person, property and work item mapping.
- **Owner:** case manager
- **Case state:** open · policy v1

**Latest reading (claude-opus-5, medium confidence, route `confirm_appointment`):** Contractor quotation NBL-015-Q1 from Brindlewick Turnover Services for property preparation at 18 Thistlevaunt Lane, totalling £665.00. Scope includes oven/extractor degreasing, limescale treatment, rubbish removal, carpet shampooing and rear garden tidying; no visit date is given.

**Why:** Router route retained for the current case item; message is a contractor quotation document adding price information to the known checkout job and does not propose a date.

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
| `triage` | case manager | `require-triage` | Clarify before routing: Is the rear garden clearance and disturbed soil to be handled as a separate work item, or added to the existing checkout scope with the same contractor? A verified route is required before asking … | Attachment move-out-inspection-report.pdf (PDF text extraction) |

### Missing information and conflicting facts

- **issue_details** (blocks the route): Quote adds carpet shampooing and garden tidying beyond the recorded checkout scope, and omits the disturbed soil and bagged dog waste noted in the inspection report. Confirm whether the garden work is part of this item or a separate work item.
- **issue_details**: The quoted £665.00 does not state whether VAT is included; the full comparable commitment including tax needs confirming.
- **availability**: No proposed visit date or time is given, so the outstanding scheduling request remains unanswered.
- 8 extracted claim(s) remain **unverified source assertions** (see REASONING.md); none was treated as verified authority.

## Failures

- None recorded. (Jev and Claude calls all returned; no workflow step failed.)

## Result

No approval was invented and no human response was supplied by the runner. The case is waiting on the person(s) listed in the handover above.

Trace: `REASONING.md` (why) · `AUDIT.md` (every step, actor and tool) · `evidence.json` / `records.jsonl` (raw records) · `checkpoint-NNN.json` (state after each source; kept in the local run directory, not published).
