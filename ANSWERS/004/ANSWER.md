# Property Management — case 004: Front entrance lock report

> **Run assumption:** the `identity` and `route` check(s) were set aside by policy (`assumed_checks`): treated as satisfied unless a source contradicted them. Nothing was verified; every other gate (access, authority, schedule, completion, money, triage) still applied.

- **Property (as supplied, unverified):** 18 Larkspur Quay, Morrowfen, ZZ1 1ZZ
- **Decision cutoff:** 2025-09-16T08:33:00+00:00
- **Runner status:** **settled** · execution `native_local` · sources processed 23 of 23
- **Models:** Claude `claude-opus-5` (triage effort medium); Jev `jev-1.13.0` routing
- **Commit:** `281c95a90dc8a3ddd9424b56d5decf0d9c521178` · input SHA-256 `cd29af163368b0bb…`

All operational tools in this run are clearly labelled **simulated** adapters: no real tenant, landlord or contractor was contacted, nothing was paid or booked, and a simulated receipt does not prove work happened.

## What the system received

The initial report and 22 further sources, submitted one at a time in availability order; each was processed and settled before the next became visible. Full text: `input.json`.

| # | Available at | Source |
|---|---|---|
| 0 | 2025-08-27T10:05:00+00:00 | Initial report — Event 001 — Portal |
| 1 | 2025-08-27T10:24:00+00:00 | Event 002 — Email from Mira Sol (Property Manager, Northbridge Lettings) |
| 2 | 2025-08-27T10:31:00+00:00 | Event 003 — Email from Mira Sol (Property Manager, Northbridge Lettings) |
| 3 | 2025-08-28T10:20:00+00:00 | Event 004 — Email from Mira Sol (Property Manager, Northbridge Lettings) |
| 4 | 2025-09-01T09:15:00+00:00 | Event 005 — Call from Mira Sol (Property Manager, Northbridge Lettings) |
| 5 | 2025-09-01T10:05:00+00:00 | Event 006 — Note from Mira Sol (Property Manager, Northbridge Lettings) |
| 6 | 2025-09-01T11:20:00+00:00 | Event 007 — Email from Mira Sol (Property Manager, Northbridge Lettings) |
| 7 | 2025-09-01T11:35:00+00:00 | Event 008 — Email from Mira Sol (Property Manager, Northbridge Lettings) |
| 8 | 2025-09-01T12:10:00+00:00 | Event 009 — Email from Nessa Vale (Tenant) |
| 9 | 2025-09-01T12:24:00+00:00 | Event 010 — Email from Mira Sol (Property Manager, Northbridge Lettings) |
| 10 | 2025-09-01T14:30:00+00:00 | Event 011 — Email from Tomas Elde (Landlord) |
| 11 | 2025-09-02T08:40:00+00:00 | Event 012 — Note from Mira Sol (Property Manager, Northbridge Lettings) |
| 12 | 2025-09-02T09:10:00+00:00 | Event 013 — Call from Mira Sol (Property Manager, Northbridge Lettings) |
| 13 | 2025-09-02T09:25:00+00:00 | Event 014 — Call from Mira Sol (Property Manager, Northbridge Lettings) |
| 14 | 2025-09-02T09:40:00+00:00 | Event 015 — Email from Mira Sol (Property Manager, Northbridge Lettings) |
| 15 | 2025-09-02T10:05:00+00:00 | Event 016 — Email from Tomas Elde (Landlord) |
| 16 | 2025-09-02T10:25:00+00:00 | Event 017 — Email from Mira Sol (Property Manager, Northbridge Lettings) |
| 17 | 2025-09-03T10:00:00+00:00 | Event 018 — Note from Mira Sol (Property Manager, Northbridge Lettings) |
| 18 | 2025-09-08T15:00:00+00:00 | Event 019 — Note from Mira Sol (Property Manager, Northbridge Lettings) |
| 19 | 2025-09-09T17:15:00+00:00 | Event 020 — Call from Mira Sol (Property Manager, Northbridge Lettings) |
| 20 | 2025-09-09T17:30:00+00:00 | Event 021 — Call from Nessa Vale (Tenant) |
| 21 | 2025-09-15T09:15:00+00:00 | Event 022 — Email from Mira Sol (Property Manager, Northbridge Lettings) |
| 22 | 2025-09-16T08:33:00+00:00 | Event 023 — Email from Nessa Vale (Tenant) |

## Final decision — system case `10754625eb22`

- **Decision (policy outcome):** **NO FURTHER ACTION**
- **Proposed next action:** `clarify` — Hot water running too hot (category plumbing)
- **Next step:** This action already has a confirmed simulated receipt. Select a new proposal for further work.
- **Owner:** case manager
- **Case state:** in_progress · policy v2
- **Split from system case** `34e0058a29d1` as a separate issue.

**Latest reading (model, medium confidence, route `clarify`):** On a call about the front-door lock case, the tenant raised three further unresolved matters: a broken bedroom blind, glazing in a door the landlord had said would be addressed, and hot water that is too hot. The agency could not confirm the status or ownership of these items during the call.

### Actions taken

- `clarify` → **succeeded** via Demo contractor (simulated adapter) — Hot water running too hot

### Escalated to a person (handover)

- No open human review.

### Missing information and conflicting facts

- None recorded by the latest reading.
- 1 extracted claim(s) remain **unverified source assertions** (see REASONING.md); none was treated as verified authority.

## Final decision — system case `0313bcb886d6`

- **Decision (policy outcome):** **NO FURTHER ACTION**
- **Proposed next action:** `clarify` — Door glazing previously said to be addressed (category windows)
- **Next step:** This action already has a confirmed simulated receipt. Select a new proposal for further work.
- **Owner:** case manager
- **Case state:** in_progress · policy v2
- **Split from system case** `34e0058a29d1` as a separate issue.

**Latest reading (model, medium confidence, route `clarify`):** On a call about the front-door lock case, the tenant raised three further unresolved matters: a broken bedroom blind, glazing in a door the landlord had said would be addressed, and hot water that is too hot. The agency could not confirm the status or ownership of these items during the call.

### Actions taken

- `clarify` → **succeeded** via Demo contractor (simulated adapter) — Door glazing previously said to be addressed

### Escalated to a person (handover)

- No open human review.

### Missing information and conflicting facts

- None recorded by the latest reading.
- 1 extracted claim(s) remain **unverified source assertions** (see REASONING.md); none was treated as verified authority.

## Final decision — system case `2a351ac4ea60`

- **Decision (policy outcome):** **HUMAN REVIEW**
- **Proposed next action:** `archive` — Tenant's own-expense skirting-board paint touch-ups (category other)
- **Next step:** Obtain authority for this work item, provider and action.
- **Owner:** approver
- **Case state:** open · policy v2
- **Split from system case** `34e0058a29d1` as a separate issue.

**Latest reading (model, medium confidence, route `archive`):** Internal note from the property manager recording that the landlord has approved proceeding with the front-door lock repair or replacement, and separately agreed the tenant may do skirting-board paint touch-ups at her own expense.

### Actions taken

- **No operational action was executed.** Nothing was booked, instructed, paid or sent. The system recorded readings, claims and policy assessments only.

### Escalated to a person (handover)

| Check | Owner | Rule | What the person must resolve | Evidence |
|---|---|---|---|---|
| `authority` | approver | `require-authority` | Obtain authority for this work item, provider and action. | no source recorded |

### Missing information and conflicting facts

- None recorded by the latest reading.

## Final decision — system case `be23f13bdb53`

- **Decision (policy outcome):** **HUMAN REVIEW**
- **Proposed next action:** `archive` — Tenant skirting-board paint touch-ups at her own expense (category other)
- **Next step:** Obtain authority for this work item, provider and action.
- **Owner:** approver
- **Case state:** open · policy v2
- **Split from system case** `34e0058a29d1` as a separate issue.

**Latest reading (model, medium confidence, route `archive`):** Property manager records a call with the landlord: he is away, asks for email contact, and states the front-door work should already have been done. He also agrees the tenant may do skirting-board paint touch-ups at her own expense.

### Actions taken

- **No operational action was executed.** Nothing was booked, instructed, paid or sent. The system recorded readings, claims and policy assessments only.

### Escalated to a person (handover)

| Check | Owner | Rule | What the person must resolve | Evidence |
|---|---|---|---|---|
| `authority` | approver | `require-authority` | Obtain authority for this work item, provider and action. | no source recorded |

### Missing information and conflicting facts

- None recorded by the latest reading.

## Final decision — system case `34e0058a29d1`

- **Decision (policy outcome):** **WAIT**
- **Proposed next action:** `clarify` — Front-door lock loose and intermittent; door catches (category doors_locks)
- **Next step:** Clarify before routing: No confirmation the contractor attended or that the lock was repaired or replaced.
- **Owner:** case manager
- **Case state:** open · policy v2

**Latest reading (claude-opus-5, medium confidence, route `clarify`):** Tenant says the landlord's contractor is due to attend that day sometime after 10:00 but with no narrower time; no confirmation yet of attendance or that the lock has been repaired or replaced. Tenant will update the agency.

**Why:** Status update without a confirmed appointment time or completion evidence; still needs clarification before routing.

### Actions taken

- Drafted message to tenant: **sent** (simulated channel; not sent to a real person) — “Hello Nessa, Thanks for letting us know about the front-door lock being loose and intermittent, with the door sometimes catching instead of closing cleanly. Could you let us know whether the door can be locked securely at all times, or whether there are periods when the property can't be locked at a …”
- Drafted message to tenant: **sent** (simulated channel; not sent to a real person) — “Hello Nessa, Thanks again for the details about the front-door lock being loose and intermittent, with the door sometimes catching instead of closing cleanly. So we have the full picture, could you describe how the lock is behaving now - for example, does the key turn stiffly, does the handle or loc …”
- Drafted message to tenant: **sent** (simulated channel; not sent to a real person) — “Hello Nessa, Thanks for bearing with us about the front-door lock being loose and intermittent, with the door catching. So we can get things moving, could you let us know which dates and times in the next week or two would suit you for a visit? Also, would you be able to be at home to let someone in …”
- Drafted message to tenant: **sent** (simulated channel; not sent to a real person) — “Hello Nessa, Thanks for sending through those three windows for the front-door lock visit - that's really helpful. Just so we have it clearly recorded, could you confirm you'll be at the property yourself to let the locksmith in during whichever of those windows is used, or whether you'd prefer a di …”
- Drafted message to tenant: **awaiting_staff** (simulated channel; not sent to a real person) — “Hello Nessa, Thanks for sending through those three windows for the front-door lock. Before anything is arranged, could you let us know whether anyone has already called at the property about the lock recently - and if so, roughly when that was and whether you were in at the time? If you ever feel u …”
- Drafted message to tenant: **awaiting_staff** (simulated channel; not sent to a real person) — “Hello Nessa, Thanks for raising the other three things on the phone - the broken bedroom blind, the glazing in the door, and the hot water being too hot. So we have the details recorded properly, could you let us know: 1. For the door glazing - which door it is, and what's wrong with the glass? 2. F …”
- Drafted message to tenant: **awaiting_staff** (simulated channel; not sent to a real person) — “Hello Nessa, Thanks for your patience about the front-door lock being loose and intermittent, with the door catching. Could you let us know whether anyone has been back to fit the new lock, and how the door and lock are working at the moment? If you ever feel unsafe, please contact the emergency ser …”
- Drafted message to tenant: **awaiting_staff** (simulated channel; not sent to a real person) — “Hello Nessa, Thanks for letting us know someone was due to come after 10:00. Could you let us know whether he has now attended, and if so whether the front-door lock has been replaced or repaired, or whether it's still loose and intermittent with the door catching? If you ever feel unsafe, please co …”
- Clarification `triage` to tenant: closed — Clarify before routing: Is the door still securable at all times, or are there periods when the property cannot be locked? This affects whether it is a security risk needing immediate attention.
- Clarification `classification` to tenant: closed — Confirm that the category and work item match the source request.
- Clarification `access` to tenant: closed — Record consent for this visit and access method from the authorised person.
- Clarification `schedule` to tenant: closed — Confirm the active appointment with a precise date and time.
- Clarification `triage` to tenant: closed — Clarify before routing: No date or time is given for the landlord's contractor's attendance; the tenant's offered windows remain unconfirmed.
- Clarification `triage` to tenant: closed — Clarify before routing: The door glazing item: which door, what the defect is, and whether the landlord already instructed anyone to deal with it.; Hot water 'too hot' - whether this is a scalding risk (thermostat/TMV setting) and which outlets are a …
- Clarification `triage` to tenant: open — Clarify before routing: Unknown whether the landlord's contractor has returned and replaced the lock; no completion evidence recorded.

### Escalated to a person (handover)

- No open human review.

### Missing information and conflicting facts

- **completion** (blocks the route): No confirmation the contractor attended or that the lock was repaired or replaced.
- **availability**: Contractor said to be attending that day after 10:00 but no precise time confirmed.
- 3 extracted claim(s) remain **unverified source assertions** (see REASONING.md); none was treated as verified authority.

## Failures

- None recorded. (Jev and Claude calls all returned; no workflow step failed.)

## Result

No approval was invented and no human response was supplied by the runner. The case is waiting on the person(s) listed in the handover above.

Trace: `REASONING.md` (why) · `AUDIT.md` (every step, actor and tool) · `evidence.json` / `records.jsonl` (raw records) · `checkpoint-NNN.json` (state after each source; kept in the local run directory, not published).
