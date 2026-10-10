# Property Management — case 007: Television, bedroom light and door handle

*PREPARATION ONLY — not official Reality Test results. System-generated; not edited by hand.*

- **Property (as supplied, unverified):** 8 Vellum Court, Brindlewick, ZZ1 1ZZ
- **Decision cutoff:** 2025-09-17T09:04:05+00:00
- **Runner status:** **settled** · execution `native_local` · sources processed 19 of 19
- **Models:** Claude `claude-opus-5` (triage effort medium); Jev `jev-1.13.0` routing
- **Commit:** `26542cfa3d481aa925490db741aa4fbab8f70e3c` · input SHA-256 `f79f08a35dff9aab…`

All operational tools in this run are clearly labelled **simulated** adapters: no real tenant, landlord or contractor was contacted, nothing was paid or booked, and a simulated receipt does not prove work happened.

## What the system received

The initial report and 18 further sources, submitted one at a time in availability order; each was processed and settled before the next became visible. Full text: `input.json`.

| # | Available at | Source |
|---|---|---|
| 0 | 2025-09-04T13:05:32+00:00 | Initial report — Event 001 — Portal |
| 1 | 2025-09-04T14:55:42+00:00 | Event 002 — Email from Mina Voss (Property Manager, Northbridge Lettings) |
| 2 | 2025-09-05T11:37:04+00:00 | Event 003 — Email from Corin Wex (Landlord, Brindlewick) |
| 3 | 2025-09-05T11:45:00+00:00 | Event 004 — Note from Mina Voss (Property Manager, Northbridge Lettings) |
| 4 | 2025-09-05T15:57:03+00:00 | Event 005 — Update from Oren Pike (Maintenance Coordinator, Northbridge Lettings) |
| 5 | 2025-09-07T16:29:16+00:00 | Event 006 — Email from Oren Pike (Maintenance Coordinator, Northbridge Lettings) |
| 6 | 2025-09-07T16:30:08+00:00 | Event 007 — Email from Corin Wex (Landlord, Brindlewick) |
| 7 | 2025-09-08T16:29:26+00:00 | Event 008 — Email from Oren Pike (Maintenance Coordinator, Northbridge Lettings) |
| 8 | 2025-09-08T16:29:34+00:00 | Event 009 — SMS from Oren Pike (Maintenance Coordinator, Northbridge Lettings) |
| 9 | 2025-09-10T16:29:12+00:00 | Event 010 — Note from Mina Voss (Property Manager, Northbridge Lettings) |
| 10 | 2025-09-11T10:30:08+00:00 | Event 011 — Update from Oren Pike (Maintenance Coordinator, Northbridge Lettings) |
| 11 | 2025-09-11T10:30:51+00:00 | Event 012 — Email from Oren Pike (Maintenance Coordinator, Northbridge Lettings) |
| 12 | 2025-09-14T10:30:29+00:00 | Event 013 — Email from Oren Pike (Maintenance Coordinator, Northbridge Lettings) |
| 13 | 2025-09-14T10:30:40+00:00 | Event 014 — SMS from Oren Pike (Maintenance Coordinator, Northbridge Lettings) |
| 14 | 2025-09-16T12:04:25+00:00 | Event 015 — Call from Jory Senn (Cover Property Manager, Northbridge Lettings) |
| 15 | 2025-09-16T13:41:07+00:00 | Event 016 — Email from Ada Pell (Tenant, Brindlewick) |
| 16 | 2025-09-16T13:42:26+00:00 | Event 017 — Email from Oren Pike (Maintenance Coordinator, Northbridge Lettings) |
| 17 | 2025-09-16T16:10:00+00:00 | Event 018 — Note from Mina Voss (Property Manager, Northbridge Lettings) |
| 18 | 2025-09-17T09:04:05+00:00 | Event 019 — Email from Rian Sol (Electrician, Bracken Spark Services) |

## Final decision — system case `7ec3757ef5ae`

- **Decision (policy outcome):** **HUMAN REVIEW**
- **Proposed next action:** `clarify` — Rear-door handle come off (category doors_locks)
- **Next step:** Verify the person, property and work item mapping.
- **Owner:** case manager
- **Case state:** open · policy v1
- **Split from system case** `ab40a5d2b243` as a separate issue.

**Latest reading (model, medium confidence, route `clarify`):** Internal note from the property manager to the coordinator recording that the rear-door handle issue was only mentioned during a phone call, with no separate report received and no handyman assigned. No new information about the TV electrical fault or the pending electrical visit.

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

## Final decision — system case `1c942163ad05`

- **Decision (policy outcome):** **HUMAN REVIEW**
- **Proposed next action:** `request_quote` — Rear-door handle come off (category doors_locks)
- **Next step:** Verify the person, property and work item mapping.
- **Owner:** case manager
- **Case state:** open · policy v1
- **Split from system case** `ab40a5d2b243` as a separate issue.

**Latest reading (model, medium confidence, route `request_quote`):** Call note from cover property manager: tenant will send availability for the electrical visit, believes the TV's main board is damaged and is open to it being removed, and is managing with a lamp instead of the downstairs light. Tenant also reported a rear-door handle coming off, which has no existing record and was asked to be submitted separately.

### Actions taken

- **No operational action was executed.** Nothing was booked, instructed, paid or sent. The system recorded readings, claims and policy assessments only.

### Escalated to a person (handover)

| Check | Owner | Rule | What the person must resolve | Evidence |
|---|---|---|---|---|
| `identity` | case manager | `require-identity` | Verify the person, property and work item mapping. | no source recorded |
| `route` | case manager | `require-route` | Verify the recipient and permitted communication route. | no source recorded |
| `classification` | case manager | `require-classification` | Confirm that the category and work item match the source request. A verified route is required before asking externally. | Split from case ab40a5d2b243: Event 015 — Call from Jory Senn (Cover Property Manager, Northbridge Lettings) |

### Missing information and conflicting facts

- None recorded by the latest reading.
- 1 extracted claim(s) remain **unverified source assertions** (see REASONING.md); none was treated as verified authority.

## Final decision — system case `3837532ab017`

- **Decision (policy outcome):** **HUMAN REVIEW**
- **Proposed next action:** `clarify` — Downstairs bedroom light flickering and popping (category other)
- **Next step:** Verify the person, property and work item mapping.
- **Owner:** case manager
- **Case state:** open · policy v1
- **Split from system case** `ab40a5d2b243` as a separate issue.

**Latest reading (model, medium confidence, route `urgent_hazard`):** Maintenance coordinator emailed the tenant asking for availability so an electrical contractor can attend regarding the TV and downstairs light, coordinating access around the dog. No date, time or consent is confirmed yet.

### Actions taken

- **No operational action was executed.** Nothing was booked, instructed, paid or sent. The system recorded readings, claims and policy assessments only.

### Escalated to a person (handover)

| Check | Owner | Rule | What the person must resolve | Evidence |
|---|---|---|---|---|
| `identity` | case manager | `require-identity` | Verify the person, property and work item mapping. | no source recorded |
| `route` | case manager | `require-route` | Verify the recipient and permitted communication route. | no source recorded |
| `triage` | case manager | `require-triage` | Claude read this as a possible urgent hazard. A case manager must take over now and apply the urgent procedure. | Split from case ab40a5d2b243: Event 006 — Email from Oren Pike (Maintenance Coordinator, Northbridge Lettings) |

### Missing information and conflicting facts

- None recorded by the latest reading.
- 1 extracted claim(s) remain **unverified source assertions** (see REASONING.md); none was treated as verified authority.

## Final decision — system case `fdf23c51e9a0`

- **Decision (policy outcome):** **HUMAN REVIEW**
- **Proposed next action:** `clarify` — Downstairs bedroom light flickering and popping (category other)
- **Next step:** Verify the person, property and work item mapping.
- **Owner:** case manager
- **Case state:** open · policy v1
- **Split from system case** `ab40a5d2b243` as a separate issue.

**Latest reading (model, medium confidence, route `urgent_hazard`):** Maintenance coordinator records that the downstairs bedroom light's flickering and popping symptoms have been added to the maintenance record, noting the landlord's approval covered only the TV.

### Actions taken

- **No operational action was executed.** Nothing was booked, instructed, paid or sent. The system recorded readings, claims and policy assessments only.

### Escalated to a person (handover)

| Check | Owner | Rule | What the person must resolve | Evidence |
|---|---|---|---|---|
| `identity` | case manager | `require-identity` | Verify the person, property and work item mapping. | no source recorded |
| `route` | case manager | `require-route` | Verify the recipient and permitted communication route. | no source recorded |
| `triage` | case manager | `require-triage` | Claude read this as a possible urgent hazard. A case manager must take over now and apply the urgent procedure. | Split from case ab40a5d2b243: Event 005 — Update from Oren Pike (Maintenance Coordinator, Northbridge Lettings) |

### Missing information and conflicting facts

- None recorded by the latest reading.
- 1 extracted claim(s) remain **unverified source assertions** (see REASONING.md); none was treated as verified authority.

## Final decision — system case `53ac0854de8d`

- **Decision (policy outcome):** **HUMAN REVIEW**
- **Proposed next action:** `clarify` — Downstairs bedroom light flickering and popping (category other)
- **Next step:** Verify the person, property and work item mapping.
- **Owner:** case manager
- **Case state:** open · policy v1
- **Split from system case** `ab40a5d2b243` as a separate issue.

**Latest reading (model, high confidence, route `urgent_hazard`):** Tenant reports a Samsung TV in the upstairs bedroom with an internal electrical fault that shorted and repeatedly tripped a fuse (now unplugged), and a downstairs bedroom light that flickers and pops when switched on. Asks that access be arranged in advance due to a dog at the property.

### Actions taken

- **No operational action was executed.** Nothing was booked, instructed, paid or sent. The system recorded readings, claims and policy assessments only.

### Escalated to a person (handover)

| Check | Owner | Rule | What the person must resolve | Evidence |
|---|---|---|---|---|
| `identity` | case manager | `require-identity` | Verify the person, property and work item mapping. | no source recorded |
| `route` | case manager | `require-route` | Verify the recipient and permitted communication route. | no source recorded |
| `triage` | case manager | `require-triage` | Claude read this as a possible urgent hazard. A case manager must take over now and apply the urgent procedure. | Split from case ab40a5d2b243: Intake report |

### Missing information and conflicting facts

- None recorded by the latest reading.
- 1 extracted claim(s) remain **unverified source assertions** (see REASONING.md); none was treated as verified authority.

## Final decision — system case `ab40a5d2b243`

- **Decision (policy outcome):** **HUMAN REVIEW**
- **Proposed next action:** `confirm_appointment` — Samsung TV electrical fault tripping fuse (category appliance)
- **Next step:** Verify the person, property and work item mapping.
- **Owner:** case manager
- **Case state:** open · policy v1

**Latest reading (claude-opus-5, high confidence, route `confirm_appointment`):** Electrician Rian Sol proposed attending on 29 September after 15:00 for the electrical visit, but gave no exact arrival time and no confirmation has been issued.

**Why:** Message is about arranging a visit for an already known job; no firm date and time agreed yet, so appointment confirmation is the next step.

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

### Missing information and conflicting facts

- **availability**: No exact arrival time given for 29 September; a precise slot is needed to confirm the appointment with the tenant.
- **access**: Tenant confirmation of the proposed date and the call-on-arrival arrangement has not been obtained.
- 5 extracted claim(s) remain **unverified source assertions** (see REASONING.md); none was treated as verified authority.

## Failures

- None recorded. (Jev and Claude calls all returned; no workflow step failed.)

## Result

No approval was invented and no human response was supplied by the runner. The case is waiting on the person(s) listed in the handover above.

Trace: `REASONING.md` (why) · `AUDIT.md` (every step, actor and tool) · `evidence.json` / `records.jsonl` (raw records) · `checkpoint-NNN.json` (state after each source; kept in the local run directory, not published).
