# Property Management — case 028: Move-out maintenance request

> **Run assumption:** the `identity` and `route` check(s) were set aside by policy (`assumed_checks`): treated as satisfied unless a source contradicted them. Nothing was verified; every other gate (access, authority, schedule, completion, money, triage) still applied.

- **Property (as supplied, unverified):** 42 Mallowfen Crescent, Ternwick, ZZ1 1ZZ
- **Decision cutoff:** 2025-09-18T14:50:04+00:00
- **Runner status:** **settled** · execution `native_local` · sources processed 27 of 27
- **Models:** Claude `claude-opus-5` (triage effort medium); Jev `jev-1.13.0` routing
- **Commit:** `281c95a90dc8a3ddd9424b56d5decf0d9c521178` · input SHA-256 `620be9402d7849fe…`

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

## Final decision — system case `a175fd017cf5`

- **Decision (policy outcome):** **HUMAN REVIEW**
- **Proposed next action:** `instruct_work` — Move-out works: meter cabinet hinges, nail removal and paint touch-up, sticker residue (category checkout_refurbishment)
- **Next step:** Obtain authority for this work item, provider and action.
- **Owner:** approver
- **Case state:** open · policy v2

**Latest reading (claude-opus-5, medium confidence, route `instruct_work`):** A contractor quotation from Pineglass Property Repairs (ref NBL-028-Q1, dated 10 September 2025) for the move-out works at 42 Mallowfen Crescent has been received, bundling the meter cabinet hinges, nail removal and paint touch-up, and sticker residue at £564.48. It does not state whether tax is included and provides no completion evidence for the works the landlord said were already done.

**Why:** The document is a provider quotation matching the known move-out work bundle, so the next step is instructing the contractor; however completion status and authority remain unresolved.

### Actions taken

- `clarify` → **succeeded** via Demo contractor (simulated adapter) — Move-out works: meter cabinet hinges, nail removal and paint touch-up, sticker residue
- Drafted message to tenant: **awaiting_staff** (simulated channel; not sent to a real person) — “Hello, We're getting the move-out works sorted (the meter cabinet hinges, nail removal and paint touch-up, and sticker residue) and just need a few details from you. 1. Who will be giving access for the visit, and how should the contractor get in (for example, you meeting them at the property or a k …”
- Drafted message to tenant: **awaiting_staff** (simulated channel; not sent to a real person) — “Hello, Thanks for your patience while we've been looking into the move-out works at the property - the meter cabinet hinges, the nail removal and paint touch-up, and the sticker residue. Before anything is arranged, could you let us know whether you're happy for us to go ahead with these three areas …”
- Drafted message to tenant: **awaiting_staff** (simulated channel; not sent to a real person) — “Hello, I hope you're well. I'm following up on the move-out works at the property - the meter cabinet hinges, nail removal and paint touch-up, and the sticker residue. Could you let me know whether you're happy for us to go ahead with this work at the quoted total of £564.48? Once I hear back from y …”
- Drafted message to tenant: **awaiting_staff** (simulated channel; not sent to a real person) — “Hello, Just a quick update request about the move-out works at the property (meter cabinet hinges, nail removal and paint touch-up, and sticker residue). 1. Have those works now been completed? If so, a couple of photos of the finished areas would be really helpful. 2. Is anything still outstanding …”
- Drafted message to tenant: **awaiting_staff** (simulated channel; not sent to a real person) — “Hello, Thank you for letting us know you'll be arranging the move-out works (the meter cabinet hinges, nail removal and paint touch-up, and sticker residue) with your own company. So we know how to handle things at our end, could you let us know whether you'd like us to close our job for these works …”
- Drafted message to tenant: **awaiting_staff** (simulated channel; not sent to a real person) — “Hello, Thank you for sending through the checkout report for 42 Mallowfen Crescent. The report lists the three move-out items (the electric-meter cabinet door hinges, removing the four wall nails in Bedroom 1 with paint touch-up, and removing the sticker residue from the front door), but it doesn't …”
- Drafted message to tenant: **awaiting_staff** (simulated channel; not sent to a real person) — “Hello, We're arranging the move-out works at 42 Mallowfen Crescent a" the electric-meter cabinet door hinges, the four wall nails in Bedroom 1 with paint touch-up, and the sticker residue on the front door. Could you help us with three things? 1. Are you happy for someone to enter the property for t …”
- Drafted message to tenant: **awaiting_staff** (simulated channel; not sent to a real person) — “Hello, We're following up on the move-out works at 42 Mallowfen Crescent - the meter cabinet door hinges, the four wall nails in Bedroom 1 with paint touch-up, and the sticker residue on the front door. Could you let us know whether these works have already been carried out at the property, and if s …”
- Clarification `access` to tenant: closed — Record consent for this visit and access method from the authorised person.
- Clarification `schedule` to tenant: closed — Confirm the active appointment with a precise date and time.
- Clarification `evidence` to tenant: closed — Supply usable evidence required for this work item.
- Clarification `triage` to tenant: closed — Clarify before routing: No landlord authority to proceed with the quoted spend has been recorded yet.
- Clarification `triage` to tenant: closed — Clarify before routing: Landlord approval for the £564.48 spend has been requested but not yet given; work cannot be instructed until a reply is recorded.
- Clarification `completion` to tenant: closed — Verify completion of this work item with usable evidence.
- Clarification `commitments` to staff: closed — Resolve or explicitly cancel every outstanding commitment for this item.
- Clarification `triage` to tenant: closed — Clarify before routing: Confirm whether the agency item should be formally closed/cancelled, or kept open to coordinate access for the landlord's own contractor during the cleaning visit.
- Clarification `commitments` to staff: closed — Resolve or explicitly cancel every outstanding commitment for this item.
- Clarification `triage` to tenant: closed — Clarify before routing: The checkout report only restates the requested works; it gives no completion date, photographs or invoice, so it does not evidence that the landlord-arranged works were done.
- Clarification `access` to tenant: open — Record consent for this visit and access method from the authorised person.
- Clarification `schedule` to tenant: open — Confirm the active appointment with a precise date and time.
- Clarification `evidence` to tenant: open — Supply usable evidence required for this work item.
- Clarification `triage` to tenant: open — Clarify before routing: The landlord previously stated the works were completed, but this quotation (dated 10 September 2025) gives no completion date, invoice or photographs; it is unclear whether the work has been carried out or still needs instruc …

### Escalated to a person (handover)

| Check | Owner | Rule | What the person must resolve | Evidence |
|---|---|---|---|---|
| `authority` | approver | `require-authority` | Obtain authority for this work item, provider and action. | no source recorded |
| `classification` | case manager | `require-classification` | Verify the received source assertion. Confirm that the category and work item match the source request. | Intake report |
| `total` | case manager | `require-total` | Verify the received source assertion. Establish the full comparable commitment, including tax. | Event 011 — Note from Talia Wren (Property Manager, Northbridge Lettings), Attachment provider-quotation.pdf (PDF text extraction) |

### Missing information and conflicting facts

- **completion** (blocks the route): The landlord previously stated the works were completed, but this quotation (dated 10 September 2025) gives no completion date, invoice or photographs; it is unclear whether the work has been carried out or still needs instructing.
- **issue_details** (blocks the route): No record that the landlord or agency has approved this quotation or the provider for the bundled works.
- **issue_details**: The quotation does not state whether the £564.48 includes VAT, so the full comparable commitment is not established.
- 9 extracted claim(s) remain **unverified source assertions** (see REASONING.md); none was treated as verified authority.

## Failures

- None recorded. (Jev and Claude calls all returned; no workflow step failed.)

## Result

No approval was invented and no human response was supplied by the runner. The case is waiting on the person(s) listed in the handover above.

Trace: `REASONING.md` (why) · `AUDIT.md` (every step, actor and tool) · `evidence.json` / `records.jsonl` (raw records) · `checkpoint-NNN.json` (state after each source; kept in the local run directory, not published).
