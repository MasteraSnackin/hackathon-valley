# Property Management — case 013: Kitchen glazing maintenance request

> **Run assumption:** the `identity` and `route` check(s) were set aside by policy (`assumed_checks`): treated as satisfied unless a source contradicted them. Nothing was verified; every other gate (access, authority, schedule, completion, money, triage) still applied.

- **Property (as supplied, unverified):** 8 Brackenmere Walk, Vellumbrook, ZZ1 1ZZ
- **Decision cutoff:** 2025-09-10T10:10:00+00:00
- **Runner status:** **settled** · execution `native_local` · sources processed 25 of 25
- **Models:** Claude `claude-opus-5` (triage effort medium); Jev `jev-1.13.0` routing
- **Commit:** `281c95a90dc8a3ddd9424b56d5decf0d9c521178` · input SHA-256 `a3727fd63257ef5c…`

All operational tools in this run are clearly labelled **simulated** adapters: no real tenant, landlord or contractor was contacted, nothing was paid or booked, and a simulated receipt does not prove work happened.

## What the system received

The initial report and 24 further sources, submitted one at a time in availability order; each was processed and settled before the next became visible. Full text: `input.json`.

| # | Available at | Source |
|---|---|---|
| 0 | 2025-07-31T08:11:00+00:00 | Initial report — Event 001 — Email |
| 1 | 2025-07-31T08:30:00+00:00 | Event 002 — Email from Tamsin Rook (Property Manager, Northbridge Lettings) |
| 2 | 2025-07-31T09:09:00+00:00 | Event 003 — Email from Tamsin Rook (Property Manager, Northbridge Lettings) |
| 3 | 2025-08-03T09:11:00+00:00 | Event 004 — Email from Tamsin Rook (Property Manager, Northbridge Lettings) |
| 4 | 2025-08-04T11:48:00+00:00 | Event 005 — Note from Tamsin Rook (Property Manager, Northbridge Lettings) |
| 5 | 2025-08-04T12:23:00+00:00 | Event 006 — Email from Tamsin Rook (Property Manager, Northbridge Lettings) |
| 6 | 2025-08-05T12:04:00+00:00 | Event 007 — Email from Tamsin Rook (Property Manager, Northbridge Lettings) |
| 7 | 2025-08-06T09:29:00+00:00 | Event 008 — Email from Tamsin Rook (Property Manager, Northbridge Lettings) |
| 8 | 2025-08-11T10:34:00+00:00 | Event 009 — Email from Tamsin Rook (Property Manager, Northbridge Lettings) |
| 9 | 2025-08-11T11:05:00+00:00 | Event 010 — Email from Orren Vale (Landlord) |
| 10 | 2025-08-11T11:17:00+00:00 | Event 011 — Email from Tamsin Rook (Property Manager, Northbridge Lettings) |
| 11 | 2025-08-11T11:19:00+00:00 | Event 012 — Note from Tamsin Rook (Property Manager, Northbridge Lettings) |
| 12 | 2025-08-11T11:20:00+00:00 | Event 013 — Email from Tamsin Rook (Property Manager, Northbridge Lettings) |
| 13 | 2025-08-11T11:49:00+00:00 | Event 014 — Email from Elowen Marr (Tenant) |
| 14 | 2025-08-11T11:50:00+00:00 | Event 015 — Email from Tamsin Rook (Property Manager, Northbridge Lettings) |
| 15 | 2025-08-14T12:54:00+00:00 | Event 016 — Call from Tamsin Rook (Property Manager, Northbridge Lettings) |
| 16 | 2025-08-19T13:12:00+00:00 | Event 017 — Email from Tamsin Rook (Property Manager, Northbridge Lettings) |
| 17 | 2025-08-24T15:33:00+00:00 | Event 018 — Email from Sella Vane (Contractor, Clearfirth Glazing) |
| 18 | 2025-08-24T15:54:00+00:00 | Event 019 — Email from Tamsin Rook (Property Manager, Northbridge Lettings) |
| 19 | 2025-08-27T16:30:00+00:00 | Event 020 — Email from Tamsin Rook (Property Manager, Northbridge Lettings) |
| 20 | 2025-09-02T10:18:00+00:00 | Event 021 — Call from Tamsin Rook (Property Manager, Northbridge Lettings) |
| 21 | 2025-09-09T09:53:00+00:00 | Event 022 — Note from Tamsin Rook (Property Manager, Northbridge Lettings) |
| 22 | 2025-09-10T09:55:00+00:00 | Event 023 — Document from Tamsin Rook (Property Manager, Northbridge Lettings) |
| 23 | 2025-09-10T10:10:00+00:00 | Event 024 — Update from Tamsin Rook (Property Manager, Northbridge Lettings) |
| 24 | 2025-09-10T10:10:00+00:00 | Attachment glazing-invoice.pdf (PDF text extraction) |

## Final decision — system case `ae0260793f36`

- **Decision (policy outcome):** **WAIT**
- **Proposed next action:** `clarify` — Kitchen window: moisture between panes and water at frame (category windows)
- **Next step:** Clarify before routing: Invoice wording implies the pane was fitted but no visit report or fitting date is given; confirm whether and when the work was carried out.
- **Owner:** case manager
- **Case state:** open · policy v2

**Latest reading (claude-opus-5, high confidence, route `clarify`):** Invoice copy from Clearfirth Glazing for supply and fit of one pane of glass to the kitchen glazing at 8 Brackenmere Walk, dated 10 September 2025. No amount is shown and there is no visit report or fitting date.

**Why:** Invoice alone does not evidence completion or attendance date; clarification needed before closing.

### Actions taken

- `request_quote` → **succeeded** via Demo contractor (simulated adapter) — Kitchen window: moisture between panes and water at frame
- Drafted message to tenant: **sent** (simulated channel; not sent to a real person) — “Hello Elowen, Thanks for letting us know about the misting between the kitchen window panes and the water gathering around the frame. So we can get a clearer picture, could you let us know whether the water at the frame appears mainly after cooking or on cold mornings, or whether it seems to come in …”
- Drafted message to tenant: **awaiting_staff** (simulated channel; not sent to a real person) — “Hello Elowen, Thanks for your patience while we look into the misting between the kitchen window panes and the water gathering around the frame. So we have an up-to-date picture, could you let us know how things are at the moment - is the water still appearing around the frame, and have you noticed …”
- Drafted message to tenant: **awaiting_staff** (simulated channel; not sent to a real person) — “Hello Elowen, Thanks again for your patience about the kitchen window. So we have a full picture of what's happening, could you let us know whether the problem is limited to the misting between the panes, or whether the water at the frame and any cold or damp are still an issue too? A quick note on …”
- Drafted message to tenant: **sent** (simulated channel; not sent to a real person) — “Hello Elowen, Thanks for your patience regarding the kitchen window with the misting between the panes and the water at the frame. So we can move things along, could you let us know: 1. Which days and times over the next couple of weeks would suit you for someone to come and take a look? 2. Would yo …”
- Drafted message to tenant: **awaiting_staff** (simulated channel; not sent to a real person) — “Hello Elowen, Thanks again for your patience about the kitchen window with the misting between the panes and the water at the frame. So we have an up-to-date picture, could you let us know how the window is at the moment \u2014 in particular, whether water is still gathering at the frame as well as …”
- Drafted message to tenant: **awaiting_staff** (simulated channel; not sent to a real person) — “Hello Elowen, Thanks again for your patience with the kitchen window. So we have an up-to-date picture, could you let us know whether water is still gathering around the frame, and whether any damp or mould has appeared around the window or nearby walls since you last wrote? Thanks very much, Northb …”
- Drafted message to tenant: **sent** (simulated channel; not sent to a real person) — “Hello Elowen, Thanks again for your help with the kitchen window where the panes are misted and water gathers at the frame. So we can get things arranged, could you let us know: 1. Which two or three dates and times over the next couple of weeks would suit you best for a visit? 2. Are you happy for …”
- Drafted message to tenant: **sent** (simulated channel; not sent to a real person) — “Hello Elowen, Thanks for coming back to us with those dates for the kitchen window where the panes are misted and water gathers at the frame. Just one thing to confirm: are you happy for someone to come into the property to look at the window while you're there, and is there anything they should kno …”
- Drafted message to tenant: **awaiting_staff** (simulated channel; not sent to a real person) — “Hello Elowen, Thanks for your patience with the kitchen window where the panes are misted and water gathers at the frame. So we have an accurate picture at our end, could you let us know whether anyone has been out to the window, and if so roughly when they attended and what was done? Thanks very mu …”
- Clarification `triage` to tenant: closed — Clarify before routing: Unclear whether the water at the frame is condensation from a failed sealed unit or ingress from outside; also whether any damp or mould is already visible.
- Clarification `classification` to tenant: closed — Confirm that the category and work item match the source request.
- Clarification `triage` to tenant: closed — Clarify before routing: The contractor's price is referenced but no total including VAT, scope of works or validity is stated, so the commitment cannot be compared or instructed.; No inspection findings are recorded, so it is unclear whether the quot …
- Clarification `access` to tenant: closed — Record consent for this visit and access method from the authorised person.
- Clarification `schedule` to tenant: closed — Confirm the active appointment with a precise date and time.
- Clarification `evidence` to tenant: closed — Supply usable evidence required for this work item.
- Clarification `triage` to tenant: closed — Clarify before routing: Approval is conditional on £180 being the full total; the quote's scope and validity are still unstated, so it is unclear whether it covers the water at the frame and damp concerns as well as the misted glazing.
- Clarification `access` to tenant: closed — Record consent for this visit and access method from the authorised person.
- Clarification `schedule` to tenant: closed — Confirm the active appointment with a precise date and time.
- Clarification `triage` to tenant: open — Clarify before routing: The invoice wording implies the pane was supplied and fitted, but there is no visit report or confirmation that the work was actually carried out or when.; No appointment was ever confirmed with the tenant, so it is unclear wh …

### Escalated to a person (handover)

- No open human review.

### Missing information and conflicting facts

- **completion** (blocks the route): Invoice wording implies the pane was fitted but no visit report or fitting date is given; confirm whether and when the work was carried out.
- **issue_details**: Invoice shows no amount, so the full cost including tax is unknown.
- 4 extracted claim(s) remain **unverified source assertions** (see REASONING.md); none was treated as verified authority.

## Failures

- None recorded. (Jev and Claude calls all returned; no workflow step failed.)

## Result

No approval was invented and no human response was supplied by the runner. See the decision above for the recorded end state.

Trace: `REASONING.md` (why) · `AUDIT.md` (every step, actor and tool) · `evidence.json` / `records.jsonl` (raw records) · `checkpoint-NNN.json` (state after each source; kept in the local run directory, not published).
