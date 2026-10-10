# Property Management — case 009: Bedroom Window Maintenance Request

> **Run assumption:** the `identity` and `route` check(s) were set aside by policy (`assumed_checks`): treated as satisfied unless a source contradicted them. Nothing was verified; every other gate (access, authority, schedule, completion, money, triage) still applied.

- **Property (as supplied, unverified):** 24 Bramblewick Lane, Alderfen, ZZ1 1ZZ
- **Decision cutoff:** 2025-09-10T18:20:00+00:00
- **Runner status:** **settled** · execution `native_local` · sources processed 21 of 21
- **Models:** Claude `claude-opus-5` (triage effort medium); Jev `jev-1.13.0` routing
- **Commit:** `281c95a90dc8a3ddd9424b56d5decf0d9c521178` · input SHA-256 `b3b37b35bb9d1a0b…`

All operational tools in this run are clearly labelled **simulated** adapters: no real tenant, landlord or contractor was contacted, nothing was paid or booked, and a simulated receipt does not prove work happened.

## What the system received

The initial report and 20 further sources, submitted one at a time in availability order; each was processed and settled before the next became visible. Full text: `input.json`.

| # | Available at | Source |
|---|---|---|
| 0 | 2025-08-12T09:10:00+00:00 | Initial report — Event 001 — Portal |
| 1 | 2025-08-12T10:05:00+00:00 | Event 002 — Email from Maya Chen (Property Manager, Northbridge Lettings) |
| 2 | 2025-08-13T10:15:00+00:00 | Event 003 — Email from Maya Chen (Property Manager, Northbridge Lettings) |
| 3 | 2025-08-13T13:40:00+00:00 | Event 004 — Email from Dorian Pike (Landlord) |
| 4 | 2025-08-14T09:20:00+00:00 | Event 005 — Call from Maya Chen (Property Manager, Northbridge Lettings) |
| 5 | 2025-08-17T11:00:00+00:00 | Event 006 — Email from Dorian Pike (Landlord) |
| 6 | 2025-08-17T11:25:00+00:00 | Event 007 — Email from Maya Chen (Property Manager, Northbridge Lettings) |
| 7 | 2025-08-17T14:10:00+00:00 | Event 008 — Email from Elena Voss (Tenant) |
| 8 | 2025-08-18T09:00:00+00:00 | Event 009 — Email from Maya Chen (Property Manager, Northbridge Lettings) |
| 9 | 2025-08-19T09:15:00+00:00 | Event 010 — Email from Dorian Pike (Landlord) |
| 10 | 2025-08-19T10:30:00+00:00 | Event 011 — Email from Dorian Pike (Landlord) |
| 11 | 2025-08-20T08:40:00+00:00 | Event 012 — Email from Maya Chen (Property Manager, Northbridge Lettings) |
| 12 | 2025-08-27T10:05:00+00:00 | Event 013 — Email from Elena Voss (Tenant) |
| 13 | 2025-08-28T13:00:00+00:00 | Event 014 — Call from Maya Chen (Property Manager, Northbridge Lettings) |
| 14 | 2025-08-28T13:20:00+00:00 | Event 015 — Call from Maya Chen (Property Manager, Northbridge Lettings) |
| 15 | 2025-08-28T13:35:00+00:00 | Event 016 — Call from Maya Chen (Property Manager, Northbridge Lettings) |
| 16 | 2025-09-01T15:10:00+00:00 | Event 017 — Email from Maya Chen (Property Manager, Northbridge Lettings) |
| 17 | 2025-09-02T09:25:00+00:00 | Event 018 — Email from Elena Voss (Tenant) |
| 18 | 2025-09-10T09:05:00+00:00 | Event 019 — Email from Dorian Pike (Landlord) |
| 19 | 2025-09-10T18:20:00+00:00 | Event 020 — Email from Elena Voss (Tenant) |
| 20 | 2025-09-10T18:20:00+00:00 | Attachment forwarded-document.pdf (PDF text extraction) |

## Final decision — system case `b87095f6dbbf`

- **Decision (policy outcome):** **HUMAN REVIEW**
- **Proposed next action:** `close_item` — Reported maintenance (category windows)
- **Next step:** Verify the received source assertion. Verify completion of this work item with usable evidence.
- **Owner:** reviewer
- **Case state:** open · policy v2

**Latest reading (claude-opus-5, high confidence, route `close_item`):** Forwarded PDF is a Landlord Gas Safety Record for 8 Thistledown Mews, Vellumby — a different property from the case property at 24 Bramblewick Lane. It contains no information about the window work and requires no maintenance action on this case.

**Why:** Document is a gas safety certificate for an unrelated property and says nothing about the window work item; no maintenance action arises.

### Actions taken

- Drafted message to tenant: **awaiting_staff** (simulated channel; not sent to a real person) — “Hello, We're arranging for someone to come and take a look at the bedroom window. Could you let us know: 1. Which days and times over the next week or two would suit you for a visit? 2. Will you be home to let someone in, or is there another way access should be arranged? Thanks very much, Northbrid …”
- Drafted message to tenant: **awaiting_staff** (simulated channel; not sent to a real person) — “Hello Elena, Thanks for letting us know someone will be home each day up to 26 August - that's really helpful. Could you let us know a specific date and time that would suit best for the window to be inspected? It helps to have one slot pinned down. Also, could you confirm you're happy for someone t …”
- Drafted message to tenant: **sent** (simulated channel; not sent to a real person) — “Hello Elena, Thanks for letting us know your availability up to 26 August for the window to be looked at. So we have everything recorded correctly, could you let us know: 1. Which date and roughly what time within that period would suit you best? 2. Will you be home to let someone in, or would you p …”
- Drafted message to tenant: **awaiting_staff** (simulated channel; not sent to a real person) — “Hello Elena, Thanks for your message, and sorry you've not had an inspection yet. We've noted that you'd prefer contact in writing first rather than an unexpected call. Could you help us with two things: 1. How would you like access to be arranged - would you be home to let someone in yourself, and …”
- Clarification `access` to tenant: closed — Record consent for this visit and access method from the authorised person.
- Clarification `schedule` to tenant: closed — Confirm the active appointment with a precise date and time.
- Clarification `access` to tenant: closed — Record consent for this visit and access method from the authorised person.
- Clarification `schedule` to tenant: closed — Confirm the active appointment with a precise date and time.
- Clarification `triage` to tenant: closed — Clarify before routing: Whether the window cannot be closed at all and whether it poses a security or weather risk needs checking.
- Clarification `commitments` to staff: open — Resolve or explicitly cancel every outstanding commitment for this item.

### Escalated to a person (handover)

| Check | Owner | Rule | What the person must resolve | Evidence |
|---|---|---|---|---|
| `completion` | reviewer | `require-completion` | Verify the received source assertion. Verify completion of this work item with usable evidence. | Event 020 — Email from Elena Voss (Tenant) |

### Missing information and conflicting facts

- **issue_details**: The gas safety record relates to a different property address; confirm whether it was sent to this case in error or belongs to another file.
- 5 extracted claim(s) remain **unverified source assertions** (see REASONING.md); none was treated as verified authority.

## Failures

- None recorded. (Jev and Claude calls all returned; no workflow step failed.)

## Result

No approval was invented and no human response was supplied by the runner. The case is waiting on the person(s) listed in the handover above.

Trace: `REASONING.md` (why) · `AUDIT.md` (every step, actor and tool) · `evidence.json` / `records.jsonl` (raw records) · `checkpoint-NNN.json` (state after each source; kept in the local run directory, not published).
