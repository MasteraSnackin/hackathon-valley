# Property Management — case 001: Bathroom leak and wall repair

> **Run assumption:** the `identity` and `route` check(s) were set aside by policy (`assumed_checks`): treated as satisfied unless a source contradicted them. Nothing was verified; every other gate (access, authority, schedule, completion, money, triage) still applied.

- **Property (as supplied, unverified):** 4 Thistlewick Rise, Larkcombe, ZZ1 1ZZ
- **Decision cutoff:** 2025-09-23T16:12:00+00:00
- **Runner status:** **settled** · execution `native_local` · sources processed 24 of 24
- **Models:** Claude `claude-opus-5` (triage effort medium); Jev `jev-1.13.0` routing
- **Commit:** `281c95a90dc8a3ddd9424b56d5decf0d9c521178` · input SHA-256 `9a9c6f50d8185ec7…`

All operational tools in this run are clearly labelled **simulated** adapters: no real tenant, landlord or contractor was contacted, nothing was paid or booked, and a simulated receipt does not prove work happened.

## What the system received

The initial report and 23 further sources, submitted one at a time in availability order; each was processed and settled before the next became visible. Full text: `input.json`.

| # | Available at | Source |
|---|---|---|
| 0 | 2025-09-04T08:10:00+00:00 | Initial report — Event 001 — Email |
| 1 | 2025-09-04T08:31:00+00:00 | Event 002 — Call from Mira Sallow (Property Manager, Northbridge Lettings) |
| 2 | 2025-09-04T09:05:00+00:00 | Event 003 — Email from Mira Sallow (Property Manager, Northbridge Lettings) |
| 3 | 2025-09-05T17:20:00+00:00 | Event 004 — Email from Orin Vale (Landlord) |
| 4 | 2025-09-07T09:15:00+00:00 | Event 005 — Email from Orin Vale (Landlord) |
| 5 | 2025-09-07T10:05:00+00:00 | Event 006 — Email from Mira Sallow (Property Manager, Northbridge Lettings) |
| 6 | 2025-09-07T11:10:00+00:00 | Event 007 — Email from Ewan Rook (Contractor, Hearthline Plumbing & Bath) |
| 7 | 2025-09-07T11:35:00+00:00 | Event 008 — Email from Mira Sallow (Property Manager, Northbridge Lettings) |
| 8 | 2025-09-08T11:30:00+00:00 | Event 009 — SMS from Mira Sallow (Property Manager, Northbridge Lettings) |
| 9 | 2025-09-10T12:20:00+00:00 | Event 010 — Call from Mira Sallow (Property Manager, Northbridge Lettings) |
| 10 | 2025-09-15T15:10:00+00:00 | Event 011 — Call from Nessa Quill (Tenant) |
| 11 | 2025-09-15T15:35:00+00:00 | Event 012 — Email from Mira Sallow (Property Manager, Northbridge Lettings) |
| 12 | 2025-09-16T07:40:00+00:00 | Event 013 — Email from Ewan Rook (Contractor, Hearthline Plumbing & Bath) |
| 13 | 2025-09-16T08:05:00+00:00 | Event 014 — Email from Mira Sallow (Property Manager, Northbridge Lettings) |
| 14 | 2025-09-18T12:00:00+00:00 | Event 015 — Note from Mira Sallow (Property Manager, Northbridge Lettings) |
| 15 | 2025-09-18T14:25:00+00:00 | Event 016 — Document from Ewan Rook (Contractor, Hearthline Plumbing & Bath) |
| 16 | 2025-09-18T14:45:00+00:00 | Event 017 — Email from Mira Sallow (Property Manager, Northbridge Lettings) |
| 17 | 2025-09-18T15:00:00+00:00 | Event 018 — Email from Orin Vale (Landlord) |
| 18 | 2025-09-18T15:12:00+00:00 | Event 019 — Email from Mira Sallow (Property Manager, Northbridge Lettings) |
| 19 | 2025-09-18T15:30:00+00:00 | Event 020 — Email from Mira Sallow (Property Manager, Northbridge Lettings) |
| 20 | 2025-09-18T15:39:00+00:00 | Event 021 — Email from Ewan Rook (Contractor, Hearthline Plumbing & Bath) |
| 21 | 2025-09-23T16:08:00+00:00 | Event 022 — Email from Mira Sallow (Property Manager, Northbridge Lettings) |
| 22 | 2025-09-23T16:12:00+00:00 | Event 023 — Email from Orin Vale (Landlord) |
| 23 | 2025-09-23T16:12:00+00:00 | Attachment bathroom-works-quotation.pdf (PDF text extraction) |

## Final decision — system case `88007831f39a`

- **Decision (policy outcome):** **WAIT**
- **Proposed next action:** `clarify` — Recurring leak from pipe behind shower, water through grout (category plumbing)
- **Next step:** Clarify before routing: Quotation still shows a single lump sum (£2,370.00 plus VAT) with no materials or labour line items, which the landlord requires before authorising.; The quotation does not state whether the recurring pipe leak behind the shower was found or will be remedied by the quoted refit scope.; Quotation lists property as 8 Wrenfold Mews, Brindlewick, ZZ1 1ZZ, not the case property 4 Thistlewick Rise, Larkcombe; confirm which property this quote covers.
- **Owner:** case manager
- **Case state:** open · policy v2

**Latest reading (claude-opus-5, medium confidence, route `clarify`):** Contractor quotation PDF (ref NBL-001-Q1, 18 September 2025) for bathroom works totalling £2,844.00 including VAT, with no materials/labour line items. The property stated on the quotation is 8 Wrenfold Mews, Brindlewick, which does not match the case property 4 Thistlewick Rise, Larkcombe.

**Why:** Quotation lacks the itemised breakdown requested and does not address the leak; property address mismatch must be resolved before routing.

### Actions taken

- `request_quote` → **succeeded** via Demo contractor (simulated adapter) — Recurring leak from pipe behind shower, water through grout
- Drafted message to tenant: **sent** (simulated channel; not sent to a real person) — “Hello Nessa, Thanks for letting us know the pipe behind the shower is leaking again and that water is coming through the grout. So we can get a clear picture, could you let us know whether water is actively escaping at the moment (for example dripping or running), and roughly how large the damaged a …”
- Drafted message to tenant: **sent** (simulated channel; not sent to a real person) — “Hello Nessa, Thanks for your patience with the leak behind the shower. So we can move things along, could you let us know which days and times over the next week or two would suit you for someone to come and take a look at the bathroom? Also, would you be happy for us to arrange access for that visi …”
- Drafted message to tenant: **sent** (simulated channel; not sent to a real person) — “Hello Nessa, Thanks for coming back to us about the leak behind the shower and for letting us know you're away this week. Could you let us know a specific date and time window that would work for the inspection, so we can confirm things properly at our end? Thanks very much, Northbridge Lettings”
- Drafted message to tenant: **awaiting_staff** (simulated channel; not sent to a real person) — “Hello Nessa, Thanks for bearing with us on the leak from the pipe behind the shower and the water coming through the grout. So we can get things lined up properly, could you let us know: 1. A specific date and time window over the next week or two that would suit you for someone to come to the bathr …”
- Drafted message to tenant: **awaiting_staff** (simulated channel; not sent to a real person) — “Hello Nessa, Thanks for your patience while we look into the leak from the pipe behind the shower. Since the bathroom was looked at, could you let us know whether you've noticed any water still coming through the grout, or any other signs of the leak since then? Thanks very much, Northbridge Letting …”
- Drafted message to tenant: **awaiting_staff** (simulated channel; not sent to a real person) — “Hello Nessa, Thanks again for your patience with the leak from the pipe behind the shower. Since the bathroom was looked at, could you let us know how things are at the moment - is water still coming through the grout, and have you noticed any change in how much or how often? Thanks very much, North …”
- Drafted message to tenant: **awaiting_staff** (simulated channel; not sent to a real person) — “Hello Nessa, Thanks again for your patience with the leak from the pipe behind the shower. Since the inspection, could you let us know how things are looking at the moment - is water still coming through the grout, and has the damaged area changed at all? Thanks very much, Northbridge Lettings”
- Clarification `triage` to tenant: closed — Clarify before routing: Extent and severity of the leak and water damage is unclear - is water actively escaping, and how large is the damaged area?
- Clarification `classification` to tenant: closed — Confirm that the category and work item match the source request.
- Clarification `access` to tenant: closed — Record consent for this visit and access method from the authorised person.
- Clarification `schedule` to tenant: closed — Confirm the active appointment with a precise date and time.
- Clarification `access` to tenant: closed — Record consent for this visit and access method from the authorised person.
- Clarification `schedule` to tenant: closed — Confirm the active appointment with a precise date and time.
- Clarification `evidence` to tenant: closed — Supply usable evidence required for this work item.
- Clarification `triage` to tenant: closed — Clarify before routing: The quoted scope is a shower/bath refit; it is not stated whether the recurring pipe leak behind the shower was found and will be remedied by this work.
- Clarification `triage` to tenant: open — Clarify before routing: Quotation has no materials or labour line items; landlord requires itemised breakdown from the contractor before authorising.; Still unstated whether the recurring pipe leak behind the shower was found and will be remedied by …

### Escalated to a person (handover)

- No open human review.

### Missing information and conflicting facts

- **issue_details** (blocks the route): Quotation still shows a single lump sum (£2,370.00 plus VAT) with no materials or labour line items, which the landlord requires before authorising.
- **issue_details** (blocks the route): The quotation does not state whether the recurring pipe leak behind the shower was found or will be remedied by the quoted refit scope.
- **location** (blocks the route): Quotation lists property as 8 Wrenfold Mews, Brindlewick, ZZ1 1ZZ, not the case property 4 Thistlewick Rise, Larkcombe; confirm which property this quote covers.
- 9 extracted claim(s) remain **unverified source assertions** (see REASONING.md); none was treated as verified authority.

## Failures

- None recorded. (Jev and Claude calls all returned; no workflow step failed.)

## Result

No approval was invented and no human response was supplied by the runner. See the decision above for the recorded end state.

Trace: `REASONING.md` (why) · `AUDIT.md` (every step, actor and tool) · `evidence.json` / `records.jsonl` (raw records) · `checkpoint-NNN.json` (state after each source; kept in the local run directory, not published).
