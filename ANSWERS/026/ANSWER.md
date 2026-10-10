# Property Management — case 026: Moisture inspection and repair coordination

> **Run assumption:** the `identity` and `route` check(s) were set aside by policy (`assumed_checks`): treated as satisfied unless a source contradicted them. Nothing was verified; every other gate (access, authority, schedule, completion, money, triage) still applied.

- **Property (as supplied, unverified):** 18 Juniper Fold, Velden Quay, ZZ1 1ZZ
- **Decision cutoff:** 2025-03-06T16:40:00+00:00
- **Runner status:** **settled** · execution `native_local` · sources processed 20 of 20
- **Models:** Claude `claude-opus-5` (triage effort medium); Jev `jev-1.13.0` routing
- **Commit:** `281c95a90dc8a3ddd9424b56d5decf0d9c521178` · input SHA-256 `9bd160a4eb6a5b3a…`

All operational tools in this run are clearly labelled **simulated** adapters: no real tenant, landlord or contractor was contacted, nothing was paid or booked, and a simulated receipt does not prove work happened.

## What the system received

The initial report and 19 further sources, submitted one at a time in availability order; each was processed and settled before the next became visible. Full text: `input.json`.

| # | Available at | Source |
|---|---|---|
| 0 | 2025-03-04T08:15:00+00:00 | Initial report — Event 001 — Portal |
| 1 | 2025-03-04T08:32:00+00:00 | Event 002 — Update from Northbridge Lettings workflow (System) |
| 2 | 2025-03-04T09:05:00+00:00 | Event 003 — Email from Maya Chen (Property Manager, Northbridge Lettings) |
| 3 | 2025-03-04T09:27:00+00:00 | Event 004 — Email from Iris Bell (Tenant, 18 Juniper Fold) |
| 4 | 2025-03-04T10:10:00+00:00 | Event 005 — Call from Maya Chen (Property Manager, Northbridge Lettings) |
| 5 | 2025-03-04T11:18:00+00:00 | Event 006 — Email from Maya Chen (Property Manager, Northbridge Lettings) |
| 6 | 2025-03-04T13:42:00+00:00 | Event 007 — Email from Owen Pike (Contractor, Brindle Survey & Drying) |
| 7 | 2025-03-04T14:05:00+00:00 | Event 008 — Email from Maya Chen (Property Manager, Northbridge Lettings) |
| 8 | 2025-03-04T14:31:00+00:00 | Event 009 — Email from Iris Bell (Tenant, 18 Juniper Fold) |
| 9 | 2025-03-05T08:50:00+00:00 | Event 010 — Email from Maya Chen (Property Manager, Northbridge Lettings) |
| 10 | 2025-03-05T09:16:00+00:00 | Event 011 — Email from Gareth Vale (Owner, 18 Juniper Fold) |
| 11 | 2025-03-05T09:40:00+00:00 | Event 012 — Update from Maya Chen (Property Manager, Northbridge Lettings) |
| 12 | 2025-03-05T11:22:00+00:00 | Event 013 — Email from Maya Chen (Property Manager, Northbridge Lettings) |
| 13 | 2025-03-05T11:29:00+00:00 | Event 014 — Email from Iris Bell (Tenant, 18 Juniper Fold) |
| 14 | 2025-03-05T11:37:00+00:00 | Event 015 — Call from Maya Chen (Property Manager, Northbridge Lettings) |
| 15 | 2025-03-05T11:51:00+00:00 | Event 016 — Note from Maya Chen (Property Manager, Northbridge Lettings) |
| 16 | 2025-03-05T12:18:00+00:00 | Event 017 — Email from Elena Frost (Privacy Lead, Northbridge Lettings) |
| 17 | 2025-03-05T13:04:00+00:00 | Event 018 — Email from Maya Chen (Property Manager, Northbridge Lettings) |
| 18 | 2025-03-06T15:12:00+00:00 | Event 019 — Call from Owen Pike (Contractor, Brindle Survey & Drying) |
| 19 | 2025-03-06T16:40:00+00:00 | Event 020 — Email from Iris Bell (Tenant, 18 Juniper Fold) |

## Final decision — system case `49880af0adfb`

- **Decision (policy outcome):** **NO FURTHER ACTION**
- **Proposed next action:** `clarify` — Misdirected email containing another tenant's personal data (category other)
- **Next step:** This action already has a confirmed simulated receipt. Select a new proposal for further work.
- **Owner:** case manager
- **Case state:** in_progress · policy v2
- **Split from system case** `17a21c54dedf` as a separate issue.

**Latest reading (model, medium confidence, route `unsupported`):** Maya Chen has logged the misdirected email incident with the agency's privacy lead, noting the personal data categories visible, the tenant's confirmation she did not forward it, and that the maintenance booking is still in progress. No assessment or notification decision has been made yet.

### Actions taken

- `clarify` → **succeeded** via Demo contractor (simulated adapter) — Misdirected email containing another tenant's personal data

### Escalated to a person (handover)

- No open human review.

### Missing information and conflicting facts

- None recorded by the latest reading.

## Final decision — system case `a912913014a6`

- **Decision (policy outcome):** **NO FURTHER ACTION**
- **Proposed next action:** `clarify` — Misdirected email containing another tenant's personal data (category other)
- **Next step:** This action already has a confirmed simulated receipt. Select a new proposal for further work.
- **Owner:** case manager
- **Case state:** in_progress · policy v2
- **Split from system case** `17a21c54dedf` as a separate issue.

**Latest reading (model, medium confidence, route `unsupported`):** Maya Chen called Iris Bell to ask her not to forward or share the misdirected email containing another tenant's personal data, and said the agency is investigating. Iris confirmed the email is still in her inbox, undeleted. No change to the window inspection arrangements.

### Actions taken

- `clarify` → **succeeded** via Demo contractor (simulated adapter) — Misdirected email containing another tenant's personal data

### Escalated to a person (handover)

- No open human review.

### Missing information and conflicting facts

- None recorded by the latest reading.

## Final decision — system case `fd5e2cd8afb7`

- **Decision (policy outcome):** **NO FURTHER ACTION**
- **Proposed next action:** `clarify` — Third-party personal data sent to tenant in error (category other)
- **Next step:** This action already has a confirmed simulated receipt. Select a new proposal for further work.
- **Owner:** case manager
- **Case state:** in_progress · policy v2
- **Split from system case** `17a21c54dedf` as a separate issue.

**Latest reading (model, medium confidence, route `unsupported`):** Tenant Iris Bell reports that the appointment confirmation email she received contained another person's personal information; she says she has not forwarded it and asks the agency what to do with the message. She does not address the outstanding access question for the 2025-03-06 inspection.

### Actions taken

- `clarify` → **succeeded** via Demo contractor (simulated adapter) — Third-party personal data sent to tenant in error

### Escalated to a person (handover)

- No open human review.

### Missing information and conflicting facts

- None recorded by the latest reading.

## Final decision — system case `17a21c54dedf`

- **Decision (policy outcome):** **STOP ACTION**
- **Proposed next action:** `confirm_appointment` — Damp staining and lifting paint below kitchen window (category other)
- **Next step:** Confirm the active appointment with a precise date and time.
- **Owner:** case manager
- **Case state:** open · policy v2

**Latest reading (claude-opus-5, high confidence, route `confirm_appointment`):** Tenant asks whether the inspection is still going ahead and what to do with the misdirected email containing another tenant's information. She reports the damp stain looked darker, with no dripping or electrical symptoms.

**Why:** Tenant chasing the arranged visit after contractor rescheduled; next step is confirming the appointment.

### Actions taken

- `clarify` → **succeeded** via Demo contractor (simulated adapter) — Damp staining and lifting paint below kitchen window
- Drafted message to tenant: **sent** (simulated channel; not sent to a real person) — “Hello Iris, Thanks for letting us know about the damp staining and lifting paint below your kitchen window, and that the patch has grown since last week. So we can work out what's causing it, could you tell us a bit more: does the patch feel wet or damp to the touch after rain, and have you noticed …”
- Drafted message to tenant: **sent** (simulated channel; not sent to a real person) — “Hello Iris, Thanks again for your patience. Just so we have the details right before we take the next step, could you confirm that the problem is the damp staining and lifting paint on the wall below your kitchen window, and let us know roughly how big the patch is now? Many thanks, Northbridge Lett …”
- Drafted message to tenant: **sent** (simulated channel; not sent to a real person) — “Hello Iris, Thanks for your patience with the damp staining and lifting paint below your kitchen window. Could you let us know whether the afternoon of Thursday 6 March, any time after 1pm, works for you? And will you be home to let someone in, or is there another way you'd prefer access to be arran …”
- Drafted message to tenant: **awaiting_staff** (simulated channel; not sent to a real person) — “Hello Iris, Thanks for confirming you'll be home after 1pm on Thursday 6 March. Just to make sure access is all set, could you confirm you're happy to let someone in yourself on the day, or if you'd prefer access to be arranged another way? Also, thank you for mentioning the mark is nearest the sock …”
- Drafted message to tenant: **awaiting_staff** (simulated channel; not sent to a real person) — “Hello Iris, Thank you for letting us know about the email you received, and for flagging it rather than passing it on. We're sorry about that, and someone will come back to you shortly about how to handle the message. In the meantime, could you let us know whether the afternoon of Thursday 6 March, …”
- Drafted message to tenant: **awaiting_staff** (simulated channel; not sent to a real person) — “Hello Iris, Thanks again for letting us know about the email you received, and for not passing it on. So we can follow this up properly, could you confirm whether the email is still in your inbox at the moment? We'll come back to you shortly about what to do with it. Many thanks, Northbridge Letting …”
- Drafted message to tenant: **awaiting_staff** (simulated channel; not sent to a real person) — “Hello Iris, Thanks for bearing with us about the damp staining and lifting paint below your kitchen window. Unfortunately the earlier slot can't go ahead, and we're now looking at the afternoon of Friday 7 March, any time after 1pm. Could you let us know whether that afternoon would suit you, and wh …”
- Clarification `triage` to tenant: closed — Clarify before routing: Source of damp unclear - could be window seal failure, condensation, or a plumbing leak; affects which trade attends.
- Clarification `classification` to tenant: closed — Confirm that the category and work item match the source request.
- Clarification `access` to tenant: closed — Record consent for this visit and access method from the authorised person.
- Clarification `schedule` to tenant: closed — Confirm the active appointment with a precise date and time.
- Clarification `triage` to tenant: closed — Clarify before routing: Needs a case manager to define handling for the misdirected personal data (other tenant's name, address and arrears) and confirm instructions to Iris for deleting the message.
- Clarification `access` to tenant: open — Record consent for this visit and access method from the authorised person.

### Escalated to a person (handover)

| Check | Owner | Rule | What the person must resolve | Evidence |
|---|---|---|---|---|
| `schedule` | case manager | `require-schedule` | Confirm the active appointment with a precise date and time. | Event 019 — Call from Owen Pike (Contractor, Brindle Survey & Drying) |
| `authority` | approver | `require-authority` | Obtain authority for this work item, provider and action. | no source recorded |
| `supported` | case manager | `require-supported` | A case manager must define a supported action for this situation. | no source recorded |

### Missing information and conflicting facts

- **availability**: Tenant has not confirmed the contractor's proposed 2025-03-07 after 13:00 slot; no date/time agreed.
- **access**: No consent for entry or access method given.
- **issue_details**: Stain reported as darker; may need reassessment of urgency, though no dripping or electrical symptoms.
- 4 extracted claim(s) remain **unverified source assertions** (see REASONING.md); none was treated as verified authority.

## Failures

- None recorded. (Jev and Claude calls all returned; no workflow step failed.)

## Result

No approval was invented and no human response was supplied by the runner. The case is waiting on the person(s) listed in the handover above.

Trace: `REASONING.md` (why) · `AUDIT.md` (every step, actor and tool) · `evidence.json` / `records.jsonl` (raw records) · `checkpoint-NNN.json` (state after each source; kept in the local run directory, not published).
