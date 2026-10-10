# Property Management — case 003: Bathroom and kitchen maintenance

*PREPARATION ONLY — not official Reality Test results. System-generated; not edited by hand.*

- **Property (as supplied, unverified):** Flat 4, 8-12 Juniper Mews, Vellumford, ZZ1 1ZZ
- **Decision cutoff:** 2025-09-14T09:20:00+00:00
- **Runner status:** **settled** · execution `native_local` · sources processed 24 of 24
- **Models:** Claude `claude-opus-5` (triage effort medium); Jev `jev-1.13.0` routing
- **Commit:** `26542cfa3d481aa925490db741aa4fbab8f70e3c` · input SHA-256 `d7aa1749a12b1d24…`

All operational tools in this run are clearly labelled **simulated** adapters: no real tenant, landlord or contractor was contacted, nothing was paid or booked, and a simulated receipt does not prove work happened.

## What the system received

The initial report and 23 further sources, submitted one at a time in availability order; each was processed and settled before the next became visible. Full text: `input.json`.

| # | Available at | Source |
|---|---|---|
| 0 | 2025-09-03T17:43:15+00:00 | Initial report — Event 001 — Portal |
| 1 | 2025-09-03T18:05:00+00:00 | Event 002 — Email from Priya Nair (Property Manager, Northbridge Lettings) |
| 2 | 2025-09-04T08:15:00+00:00 | Event 003 — Email from Priya Nair (Property Manager, Northbridge Lettings) |
| 3 | 2025-09-04T08:32:00+00:00 | Event 004 — Email from Owen Vale (Landlord) |
| 4 | 2025-09-04T09:10:00+00:00 | Event 005 — Note from Priya Nair (Property Manager, Northbridge Lettings) |
| 5 | 2025-09-04T14:26:00+00:00 | Event 006 — Email from Priya Nair (Property Manager, Northbridge Lettings) |
| 6 | 2025-09-04T16:21:00+00:00 | Event 007 — Email from Elian Voss (Tenant) |
| 7 | 2025-09-04T16:40:00+00:00 | Event 008 — Email from Priya Nair (Property Manager, Northbridge Lettings) |
| 8 | 2025-09-04T17:05:00+00:00 | Event 009 — Email from Gareth Lune (Plumber, Copper Finch Plumbing) |
| 9 | 2025-09-04T17:20:00+00:00 | Event 010 — Email from Priya Nair (Property Manager, Northbridge Lettings) |
| 10 | 2025-09-04T17:22:00+00:00 | Event 011 — Email from Priya Nair (Property Manager, Northbridge Lettings) |
| 11 | 2025-09-05T09:00:00+00:00 | Event 012 — Email from Priya Nair (Property Manager, Northbridge Lettings) |
| 12 | 2025-09-11T09:00:00+00:00 | Event 013 — SMS from Priya Nair (Property Manager, Northbridge Lettings) |
| 13 | 2025-09-11T10:15:00+00:00 | Event 014 — Email from Gareth Lune (Plumber, Copper Finch Plumbing) |
| 14 | 2025-09-11T10:35:00+00:00 | Event 015 — Email from Gareth Lune (Plumber, Copper Finch Plumbing) |
| 15 | 2025-09-11T11:10:00+00:00 | Event 016 — Call from Gareth Lune (Plumber, Copper Finch Plumbing) |
| 16 | 2025-09-11T11:30:00+00:00 | Event 017 — Update from Priya Nair (Property Manager, Northbridge Lettings) |
| 17 | 2025-09-11T11:45:00+00:00 | Event 018 — Email from Priya Nair (Property Manager, Northbridge Lettings) |
| 18 | 2025-09-11T11:48:00+00:00 | Event 019 — SMS from Priya Nair (Property Manager, Northbridge Lettings) |
| 19 | 2025-09-12T10:55:00+00:00 | Event 020 — Call from Gareth Lune (Plumber, Copper Finch Plumbing) |
| 20 | 2025-09-12T12:20:00+00:00 | Event 021 — Note from Priya Nair (Property Manager, Northbridge Lettings) |
| 21 | 2025-09-14T09:00:00+00:00 | Event 022 — Document from Gareth Lune (Plumber, Copper Finch Plumbing) |
| 22 | 2025-09-14T09:20:00+00:00 | Event 023 — Note from Priya Nair (Property Manager, Northbridge Lettings) |
| 23 | 2025-09-14T09:20:00+00:00 | Attachment tap-works-invoice.pdf (PDF text extraction) |

## Final decision — system case `2f6fd6d24abd`

- **Decision (policy outcome):** **HUMAN REVIEW**
- **Proposed next action:** `clarify` — Bathroom basin hot tap - brass insert and chrome head fitted (category plumbing)
- **Next step:** Verify the person, property and work item mapping.
- **Owner:** case manager
- **Case state:** open · policy v1
- **Split from system case** `4f5652b4e037` as a separate issue.

**Latest reading (model, medium confidence, route `clarify`):** Contractor invoice (PDF text) for tap works states a new kitchen mixer tap was supplied and installed and a new brass insert and chrome head fitted to the bathroom basin hot tap. The invoice names a different property (Flat 4, 28 Larkspur Quay, Brindlewick) than the case property, and no price or total is shown in the extracted text.

### Actions taken

- **No operational action was executed.** Nothing was booked, instructed, paid or sent. The system recorded readings, claims and policy assessments only.

### Escalated to a person (handover)

| Check | Owner | Rule | What the person must resolve | Evidence |
|---|---|---|---|---|
| `identity` | case manager | `require-identity` | Verify the person, property and work item mapping. | no source recorded |
| `route` | case manager | `require-route` | Verify the recipient and permitted communication route. | no source recorded |

### Missing information and conflicting facts

- None recorded by the latest reading.
- 2 extracted claim(s) remain **unverified source assertions** (see REASONING.md); none was treated as verified authority.

## Final decision — system case `7f2b14d90a6e`

- **Decision (policy outcome):** **HUMAN REVIEW**
- **Proposed next action:** `request_quote` — Water ingress via bathroom vent and bedroom damp (category other)
- **Next step:** Verify the person, property and work item mapping.
- **Owner:** case manager
- **Case state:** open · policy v1
- **Split from system case** `4f5652b4e037` as a separate issue.

**Latest reading (model, medium confidence, route `request_quote`):** Northbridge Lettings forwarded the reported symptoms to Copper Finch Plumbing and asked the plumber to arrange a visit. The referral bundled both tap problems with the vent and bedroom water-ingress reports without separating them into distinct work orders.

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

## Final decision — system case `a998e581439e`

- **Decision (policy outcome):** **HUMAN REVIEW**
- **Proposed next action:** `clarify` — Check building insurance cover and review property history (category other)
- **Next step:** Verify the person, property and work item mapping.
- **Owner:** case manager
- **Case state:** open · policy v1
- **Split from system case** `4f5652b4e037` as a separate issue.

**Latest reading (model, medium confidence, route `unsupported`):** Landlord Owen Vale approves proceeding with the reported works and asks Northbridge Lettings to check possible building insurance cover and review the flat's history, noting repeated roof leaks and some severe-looking damage.

### Actions taken

- **No operational action was executed.** Nothing was booked, instructed, paid or sent. The system recorded readings, claims and policy assessments only.

### Escalated to a person (handover)

| Check | Owner | Rule | What the person must resolve | Evidence |
|---|---|---|---|---|
| `identity` | case manager | `require-identity` | Verify the person, property and work item mapping. | no source recorded |
| `route` | case manager | `require-route` | Verify the recipient and permitted communication route. | no source recorded |

### Missing information and conflicting facts

- None recorded by the latest reading.

## Final decision — system case `09e66eaadbd7`

- **Decision (policy outcome):** **HUMAN REVIEW**
- **Proposed next action:** `request_quote` — Recurring roof leak and water damage (category other)
- **Next step:** Verify the person, property and work item mapping.
- **Owner:** case manager
- **Case state:** open · policy v1
- **Split from system case** `4f5652b4e037` as a separate issue.

**Latest reading (model, medium confidence, route `request_quote`):** Landlord Owen Vale approves proceeding with the reported works and asks Northbridge Lettings to check possible building insurance cover and review the flat's history, noting repeated roof leaks and some severe-looking damage.

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

## Final decision — system case `82683767d54b`

- **Decision (policy outcome):** **HUMAN REVIEW**
- **Proposed next action:** `request_quote` — Damp patches in smaller bedroom (category other)
- **Next step:** Verify the person, property and work item mapping.
- **Owner:** case manager
- **Case state:** open · policy v1
- **Split from system case** `4f5652b4e037` as a separate issue.

**Latest reading (model, high confidence, route `request_quote`):** The property manager has forwarded the tenant's reported issues (both taps, water ingress through the bathroom vent in heavy rain, and bedroom damp) to the landlord for approval and asked whether the agency may arrange attendance. No approval, appointment or access arrangement is stated yet.

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

## Final decision — system case `f44706fcce7c`

- **Decision (policy outcome):** **HUMAN REVIEW**
- **Proposed next action:** `request_quote` — Water ingress through bathroom vent in heavy rain (category other)
- **Next step:** Verify the person, property and work item mapping.
- **Owner:** case manager
- **Case state:** open · policy v1
- **Split from system case** `4f5652b4e037` as a separate issue.

**Latest reading (model, high confidence, route `request_quote`):** The property manager has forwarded the tenant's reported issues (both taps, water ingress through the bathroom vent in heavy rain, and bedroom damp) to the landlord for approval and asked whether the agency may arrange attendance. No approval, appointment or access arrangement is stated yet.

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

## Final decision — system case `7f951bc54ff1`

- **Decision (policy outcome):** **HUMAN REVIEW**
- **Proposed next action:** `request_quote` — Bathroom hot tap hard to close (category plumbing)
- **Next step:** Verify the person, property and work item mapping.
- **Owner:** case manager
- **Case state:** open · policy v1
- **Split from system case** `4f5652b4e037` as a separate issue.

**Latest reading (model, high confidence, route `request_quote`):** The property manager has forwarded the tenant's reported issues (both taps, water ingress through the bathroom vent in heavy rain, and bedroom damp) to the landlord for approval and asked whether the agency may arrange attendance. No approval, appointment or access arrangement is stated yet.

### Actions taken

- **No operational action was executed.** Nothing was booked, instructed, paid or sent. The system recorded readings, claims and policy assessments only.

### Escalated to a person (handover)

| Check | Owner | Rule | What the person must resolve | Evidence |
|---|---|---|---|---|
| `identity` | case manager | `require-identity` | Verify the person, property and work item mapping. | no source recorded |
| `route` | case manager | `require-route` | Verify the recipient and permitted communication route. | no source recorded |

### Missing information and conflicting facts

- None recorded by the latest reading.

## Final decision — system case `f06ed8d04a66`

- **Decision (policy outcome):** **HUMAN REVIEW**
- **Proposed next action:** `request_quote` — Damp patches on smaller bedroom ceiling and wall (category other)
- **Next step:** Verify the person, property and work item mapping.
- **Owner:** case manager
- **Case state:** open · policy v1
- **Split from system case** `4f5652b4e037` as a separate issue.

**Latest reading (model, medium confidence, route `request_quote`):** Tenant Elian Voss submitted a maintenance request for Flat 4, 8-12 Juniper Mews covering four problems: a dripping kitchen tap, a bathroom hot tap that is hard to close, rainwater coming through the bathroom vent, and damp patches on the smaller bedroom ceiling and wall. No pets or access restrictions were noted.

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

## Final decision — system case `92f7c2205919`

- **Decision (policy outcome):** **HUMAN REVIEW**
- **Proposed next action:** `request_quote` — Rainwater dripping through bathroom vent (category other)
- **Next step:** Verify the person, property and work item mapping.
- **Owner:** case manager
- **Case state:** open · policy v1
- **Split from system case** `4f5652b4e037` as a separate issue.

**Latest reading (model, medium confidence, route `request_quote`):** Tenant Elian Voss submitted a maintenance request for Flat 4, 8-12 Juniper Mews covering four problems: a dripping kitchen tap, a bathroom hot tap that is hard to close, rainwater coming through the bathroom vent, and damp patches on the smaller bedroom ceiling and wall. No pets or access restrictions were noted.

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

## Final decision — system case `959b56db81a7`

- **Decision (policy outcome):** **HUMAN REVIEW**
- **Proposed next action:** `request_quote` — Bathroom hot tap hard to close (category plumbing)
- **Next step:** Verify the person, property and work item mapping.
- **Owner:** case manager
- **Case state:** open · policy v1
- **Split from system case** `4f5652b4e037` as a separate issue.

**Latest reading (model, medium confidence, route `request_quote`):** Tenant Elian Voss submitted a maintenance request for Flat 4, 8-12 Juniper Mews covering four problems: a dripping kitchen tap, a bathroom hot tap that is hard to close, rainwater coming through the bathroom vent, and damp patches on the smaller bedroom ceiling and wall. No pets or access restrictions were noted.

### Actions taken

- **No operational action was executed.** Nothing was booked, instructed, paid or sent. The system recorded readings, claims and policy assessments only.

### Escalated to a person (handover)

| Check | Owner | Rule | What the person must resolve | Evidence |
|---|---|---|---|---|
| `identity` | case manager | `require-identity` | Verify the person, property and work item mapping. | no source recorded |
| `route` | case manager | `require-route` | Verify the recipient and permitted communication route. | no source recorded |
| `classification` | case manager | `require-classification` | Confirm that the category and work item match the source request. A verified route is required before asking externally. | Split from case 4f5652b4e037: Intake report |

### Missing information and conflicting facts

- None recorded by the latest reading.
- 1 extracted claim(s) remain **unverified source assertions** (see REASONING.md); none was treated as verified authority.

## Final decision — system case `4f5652b4e037`

- **Decision (policy outcome):** **HUMAN REVIEW**
- **Proposed next action:** `clarify` — Dripping kitchen tap (category plumbing)
- **Next step:** Verify the person, property and work item mapping.
- **Owner:** case manager
- **Case state:** open · policy v1

**Latest reading (claude-opus-5, medium confidence, route `clarify`):** Contractor invoice (PDF text) for tap works states a new kitchen mixer tap was supplied and installed and a new brass insert and chrome head fitted to the bathroom basin hot tap. The invoice names a different property (Flat 4, 28 Larkspur Quay, Brindlewick) than the case property, and no price or total is shown in the extracted text.

**Why:** The invoice reports the kitchen tap work as done, which would support closing the item, but the property address on the invoice does not match the case property and no total is shown, so the completion evidence cannot be accepted without clarification.

### Actions taken

- **No operational action was executed.** Nothing was booked, instructed, paid or sent. The system recorded readings, claims and policy assessments only.

### Escalated to a person (handover)

| Check | Owner | Rule | What the person must resolve | Evidence |
|---|---|---|---|---|
| `identity` | case manager | `require-identity` | Verify the person, property and work item mapping. | no source recorded |
| `route` | case manager | `require-route` | Verify the recipient and permitted communication route. | no source recorded |
| `triage` | case manager | `require-triage` | Clarify before routing: The invoice states the property as "Flat 4, 28 Larkspur Quay, Brindlewick, ZZ1 1ZZ", which does not match the case property Flat 4, 8-12 Juniper Mews. Confirm which property was attended and wheth … | Attachment tap-works-invoice.pdf (PDF text extraction) |

### Missing information and conflicting facts

- **location** (blocks the route): The invoice states the property as "Flat 4, 28 Larkspur Quay, Brindlewick, ZZ1 1ZZ", which does not match the case property Flat 4, 8-12 Juniper Mews. Confirm which property was attended and whether the invoice has been issued against the wrong address.
- **issue_details** (blocks the route): Whether the bathroom basin hot tap work was authorised and should be recorded as its own work item remains unresolved.
- **completion**: No price or total including tax appears in the extracted invoice text; the full invoiced amount needs confirming before the item can be settled or closed.
- 18 extracted claim(s) remain **unverified source assertions** (see REASONING.md); none was treated as verified authority.

## Failures

- None recorded. (Jev and Claude calls all returned; no workflow step failed.)

## Result

No approval was invented and no human response was supplied by the runner. The case is waiting on the person(s) listed in the handover above.

Trace: `REASONING.md` (why) · `AUDIT.md` (every step, actor and tool) · `evidence.json` / `records.jsonl` (raw records) · `checkpoint-NNN.json` (state after each source; kept in the local run directory, not published).
