# Property Management — case 019: Move-out maintenance at 18 Brindle Row

*PREPARATION ONLY — not official Reality Test results. System-generated; not edited by hand.*

- **Property (as supplied, unverified):** 18 Brindle Row, Larkspur Vale, ZZ1 1ZZ
- **Decision cutoff:** 2025-09-11T07:00:00+00:00
- **Runner status:** **settled** · execution `native_local` · sources processed 17 of 17
- **Models:** Claude `claude-opus-5` (triage effort medium); Jev `jev-1.13.0` routing
- **Commit:** `26542cfa3d481aa925490db741aa4fbab8f70e3c` · input SHA-256 `c280478b4a5855ca…`

All operational tools in this run are clearly labelled **simulated** adapters: no real tenant, landlord or contractor was contacted, nothing was paid or booked, and a simulated receipt does not prove work happened.

## What the system received

The initial report and 16 further sources, submitted one at a time in availability order; each was processed and settled before the next became visible. Full text: `input.json`.

| # | Available at | Source |
|---|---|---|
| 0 | 2025-09-04T13:25:54+00:00 | Initial report — Event 001 — Note |
| 1 | 2025-09-04T13:26:00+00:00 | Event 002 — Email from Maya Chen (Property Manager, Northbridge Lettings) |
| 2 | 2025-09-04T13:51:20+00:00 | Event 003 — Email from Tomas Venn (Former Tenant) |
| 3 | 2025-09-04T15:16:19+00:00 | Event 004 — Note from Maya Chen (Property Manager, Northbridge Lettings) |
| 4 | 2025-09-07T09:44:04+00:00 | Event 005 — Email from Ivo Marlow (Landlord) |
| 5 | 2025-09-07T09:44:16+00:00 | Event 006 — Note from Maya Chen (Property Manager, Northbridge Lettings) |
| 6 | 2025-09-07T10:51:49+00:00 | Event 007 — Note from Maya Chen (Property Manager, Northbridge Lettings) |
| 7 | 2025-09-07T10:53:09+00:00 | Event 008 — Email from Maya Chen (Property Manager, Northbridge Lettings) |
| 8 | 2025-09-07T10:53:16+00:00 | Event 009 — Email from Maya Chen (Property Manager, Northbridge Lettings) |
| 9 | 2025-09-08T10:51:52+00:00 | Event 010 — Email from Maya Chen (Property Manager, Northbridge Lettings) |
| 10 | 2025-09-10T10:51:40+00:00 | Event 011 — Note from Maya Chen (Property Manager, Northbridge Lettings) |
| 11 | 2025-09-10T11:57:57+00:00 | Event 012 — Note from Maya Chen (Property Manager, Northbridge Lettings) |
| 12 | 2025-09-10T12:00:48+00:00 | Event 013 — Call from Maya Chen (Property Manager, Northbridge Lettings) |
| 13 | 2025-09-11T06:57:15+00:00 | Event 014 — Email from Rowan Pike (Contractor, Alder & Finch Repairs) |
| 14 | 2025-09-11T06:57:30+00:00 | Event 015 — Note from Maya Chen (Property Manager, Northbridge Lettings) |
| 15 | 2025-09-11T06:58:16+00:00 | Event 016 — Document from Rowan Pike (Contractor, Alder & Finch Repairs) |
| 16 | 2025-09-11T07:00:00+00:00 | Attachment remedial-works-invoice.pdf (PDF text extraction) |

## Final decision — system case `0cd731bfdf25`

- **Decision (policy outcome):** **HUMAN REVIEW**
- **Proposed next action:** `clarify` — Move-out remedial works (unspecified) (category checkout_refurbishment)
- **Next step:** Verify the person, property and work item mapping.
- **Owner:** case manager
- **Case state:** open · policy v1

**Latest reading (claude-opus-5, high confidence, route `clarify`):** Invoice document from Alder & Finch Repairs (ref NBL-019-INV-11, 11 September 2025) for 18 Brindle Row, listing six remedial work items as completed with a single total of £174.00. No itemised pricing, VAT statement, quotation or separate completion evidence is included.

**Why:** Invoice asserts completed works and a total, but without itemised pricing, VAT position, authority for apparent variations or any completion evidence; the item cannot be closed or approved until these are clarified.

### Actions taken

- **No operational action was executed.** Nothing was booked, instructed, paid or sent. The system recorded readings, claims and policy assessments only.

### Escalated to a person (handover)

| Check | Owner | Rule | What the person must resolve | Evidence |
|---|---|---|---|---|
| `identity` | case manager | `require-identity` | Verify the person, property and work item mapping. | no source recorded |
| `route` | case manager | `require-route` | Verify the recipient and permitted communication route. | no source recorded |
| `triage` | case manager | `require-triage` | Clarify before routing: Contractor states the works are finished, but no evidence, scope or invoice is on file yet; what was actually done is unknown.; Agreed scope and price were never established, and no written author … | Event 013 — Call from Maya Chen (Property Manager, Northbridge Lettings) |

### Missing information and conflicting facts

- **completion** (blocks the route): The invoice gives a single lump sum of £174.00 with no itemised prices and no statement of whether VAT is included, so the full comparable commitment cannot be established.
- **completion** (blocks the route): No completion evidence, photographs, visit narrative or appointment record supports that the listed items were carried out.
- **issue_details** (blocks the route): Several invoiced items (new Venetian blind supply and install, front-gate hinge, toilet seat) may be variations outside the original scope; no quotation, prior approval or authorising person is identified.
- **access**: The document does not say when or how the contractor gained access to the property or who authorised entry.
- 7 extracted claim(s) remain **unverified source assertions** (see REASONING.md); none was treated as verified authority.

## Failures

- None recorded. (Jev and Claude calls all returned; no workflow step failed.)

## Result

No approval was invented and no human response was supplied by the runner. The case is waiting on the person(s) listed in the handover above.

Trace: `REASONING.md` (why) · `AUDIT.md` (every step, actor and tool) · `evidence.json` / `records.jsonl` (raw records) · `checkpoint-NNN.json` (state after each source; kept in the local run directory, not published).
