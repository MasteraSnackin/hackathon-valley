# Property Management — case 019: Move-out maintenance at 18 Brindle Row

> **Run assumption:** the `identity` and `route` check(s) were set aside by policy (`assumed_checks`): treated as satisfied unless a source contradicted them. Nothing was verified; every other gate (access, authority, schedule, completion, money, triage) still applied.

- **Property (as supplied, unverified):** 18 Brindle Row, Larkspur Vale, ZZ1 1ZZ
- **Decision cutoff:** 2025-09-11T07:00:00+00:00
- **Runner status:** **settled** · execution `native_local` · sources processed 17 of 17
- **Models:** Claude `claude-opus-5` (triage effort medium); Jev `jev-1.13.0` routing
- **Commit:** `281c95a90dc8a3ddd9424b56d5decf0d9c521178` · input SHA-256 `c280478b4a5855ca…`

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

## Final decision — system case `4fc98fae3ee2`

- **Decision (policy outcome):** **WAIT**
- **Proposed next action:** `clarify` — Move-out remedial works (unspecified) (category checkout_refurbishment)
- **Next step:** Clarify before routing: The invoice shows a single £174.00 line and does not state whether VAT is included or itemise the individual works.; No completion evidence, visit date or access record supports the listed works; works were carried out without a quotation or recorded authorisation.
- **Owner:** case manager
- **Case state:** open · policy v2

**Latest reading (claude-opus-5, medium confidence, route `clarify`):** Attached invoice from Alder & Finch Repairs for 18 Brindle Row lists the remedial works carried out and a single line total of £174.00. No itemised pricing, VAT statement, quotation reference, payment terms or completion evidence is included.

**Why:** Scope is now listed and a £174.00 figure is given, but VAT status, itemisation and any evidence of authorised completion remain missing, so the item cannot yet be closed or paid.

### Actions taken

- `request_quote` → **succeeded** via Demo contractor (simulated adapter) — Move-out remedial works (unspecified)
- Drafted message to tenant: **awaiting_staff** (simulated channel; not sent to a real person) — “Hello, We've had a note logged about move-out remedial works at the property, but it doesn't say what's actually needed. Could you let us know what work is required (for example cleaning, repairs or redecoration) and which rooms or items are affected? Thanks very much.”
- Drafted message to tenant: **awaiting_staff** (simulated channel; not sent to a real person) — “Hello Tomas, Thanks for letting us know you moved out on 27 August and returned the keys that day dd we've noted that. So we can make sure our records are accurate, could you let us know what you understand the outstanding items at 18 Brindle Row to be dd for example any cleaning, repairs or redecor …”
- Drafted message to tenant: **awaiting_staff** (simulated channel; not sent to a real person) — “Hello, We're arranging an inspection visit at the property following your move-out, and wanted to check a couple of things with you. 1. Are you happy for the inspection to go ahead using the set of keys we hold, given you've told us you've returned yours and left the property? 2. If you'd still like …”
- Drafted message to tenant: **awaiting_staff** (simulated channel; not sent to a real person) — “Hello, Thanks for sending the paperwork through for the move-out remedial works at the property. So we can get everything matched up correctly, could you confirm the total on the invoice including VAT, and set out the scope of the work that was carried out? Many thanks.”
- Drafted message to tenant: **awaiting_staff** (simulated channel; not sent to a real person) — “Hello, Thank you for sending the invoice for the move-out remedial works at the property. So that we can process it, could you let us know what work was actually carried out, and whether the £174 total includes VAT? It would also help if you could send over anything you have from the visit, such as …”
- Clarification `triage` to tenant: closed — Clarify before routing: The note does not state what remedial works are needed (e.g. cleaning, repairs, redecoration) or which rooms/items are affected.
- Clarification `access` to tenant: closed — Record consent for this visit and access method from the authorised person.
- Clarification `schedule` to tenant: closed — Confirm the active appointment with a precise date and time.
- Clarification `triage` to tenant: open — Clarify before routing: Invoice total including VAT and the scope of works carried out are not stated in the message.

### Escalated to a person (handover)

| Check | Owner | Rule | What the person must resolve | Evidence |
|---|---|---|---|---|
| `triage` | case manager | `require-triage` | Jev routed this message to confirm_appointment, but Claude reads it as clarify: confirm_appointment is not appropriate: no visit is being arranged and the contractor states the work is already done. The next step is clar … | Event 013 — Call from Maya Chen (Property Manager, Northbridge Lettings) |

### Missing information and conflicting facts

- **issue_details** (blocks the route): The invoice shows a single £174.00 line and does not state whether VAT is included or itemise the individual works.
- **completion** (blocks the route): No completion evidence, visit date or access record supports the listed works; works were carried out without a quotation or recorded authorisation.
- 7 extracted claim(s) remain **unverified source assertions** (see REASONING.md); none was treated as verified authority.

## Failures

- None recorded. (Jev and Claude calls all returned; no workflow step failed.)

## Result

No approval was invented and no human response was supplied by the runner. The case is waiting on the person(s) listed in the handover above.

Trace: `REASONING.md` (why) · `AUDIT.md` (every step, actor and tool) · `evidence.json` / `records.jsonl` (raw records) · `checkpoint-NNN.json` (state after each source; kept in the local run directory, not published).
