# Property Management — case 014: Heating service request at 7 Mallowmere Walk

*PREPARATION ONLY — not official Reality Test results. System-generated; not edited by hand.*

- **Property (as supplied, unverified):** 7 Mallowmere Walk, Larkfen, ZZ1 1ZZ
- **Decision cutoff:** 2025-01-14T17:08:00+00:00
- **Runner status:** **settled** · execution `native_local` · sources processed 19 of 19
- **Models:** Claude `claude-opus-5` (triage effort medium); Jev `jev-1.13.0` routing
- **Commit:** `26542cfa3d481aa925490db741aa4fbab8f70e3c` · input SHA-256 `d103d0e8d228e4f0…`

All operational tools in this run are clearly labelled **simulated** adapters: no real tenant, landlord or contractor was contacted, nothing was paid or booked, and a simulated receipt does not prove work happened.

## What the system received

The initial report and 18 further sources, submitted one at a time in availability order; each was processed and settled before the next became visible. Full text: `input.json`.

| # | Available at | Source |
|---|---|---|
| 0 | 2025-01-14T08:12:00+00:00 | Initial report — Event 001 — Portal |
| 1 | 2025-01-14T08:26:00+00:00 | Event 002 — Update from Maya Chen (Property Manager, Northbridge Lettings) |
| 2 | 2025-01-14T08:39:00+00:00 | Event 003 — SMS from Leah Venn (Tenant) |
| 3 | 2025-01-14T09:03:00+00:00 | Event 004 — Call from Maya Chen (Property Manager, Northbridge Lettings) |
| 4 | 2025-01-14T09:24:00+00:00 | Event 005 — Email from Maya Chen (Property Manager, Northbridge Lettings) |
| 5 | 2025-01-14T09:41:00+00:00 | Event 006 — Email from Daniel Hart (Heating Contractor, Brackenridge Heat Services) |
| 6 | 2025-01-14T10:02:00+00:00 | Event 007 — Note from Maya Chen (Property Manager, Northbridge Lettings) |
| 7 | 2025-01-14T10:18:00+00:00 | Event 008 — SMS from Leah Venn (Tenant) |
| 8 | 2025-01-14T10:37:00+00:00 | Event 009 — Call from Maya Chen (Property Manager, Northbridge Lettings) |
| 9 | 2025-01-14T11:06:00+00:00 | Event 010 — Email from Owen Pike (Landlord) |
| 10 | 2025-01-14T11:22:00+00:00 | Event 011 — Email from Maya Chen (Property Manager, Northbridge Lettings) |
| 11 | 2025-01-14T11:48:00+00:00 | Event 012 — Email from Daniel Hart (Heating Contractor, Brackenridge Heat Services) |
| 12 | 2025-01-14T12:14:00+00:00 | Event 013 — SMS from Leah Venn (Tenant) |
| 13 | 2025-01-14T12:47:00+00:00 | Event 014 — Email from Owen Pike (Landlord) |
| 14 | 2025-01-14T13:16:00+00:00 | Event 015 — Call from Maya Chen (Property Manager, Northbridge Lettings) |
| 15 | 2025-01-14T14:03:00+00:00 | Event 016 — Email from Maya Chen (Property Manager, Northbridge Lettings) |
| 16 | 2025-01-14T15:11:00+00:00 | Event 017 — Update from Priya Noll (Duty Manager, Northbridge Lettings) |
| 17 | 2025-01-14T16:42:00+00:00 | Event 018 — Portal from Leah Venn (Tenant) |
| 18 | 2025-01-14T17:08:00+00:00 | Event 019 — Call from Daniel Hart (Heating Contractor, Brackenridge Heat Services) |

## Final decision — system case `e35b4a82e105`

- **Decision (policy outcome):** **HUMAN REVIEW**
- **Proposed next action:** `clarify` — Tenant's plug-in heater overheating - advised not to be used (category appliance)
- **Next step:** Verify the person, property and work item mapping.
- **Owner:** case manager
- **Case state:** open · policy v1
- **Split from system case** `bb1c8adfab87` as a separate issue.

**Latest reading (model, medium confidence, route `urgent_hazard`):** Contractor confirms no same-day engineer; a 15 January cancellation slot may arise but cannot be held without a booking. They cannot assess or advise remotely and say the plug-in heater Leah described should not be used.

### Actions taken

- **No operational action was executed.** Nothing was booked, instructed, paid or sent. The system recorded readings, claims and policy assessments only.

### Escalated to a person (handover)

| Check | Owner | Rule | What the person must resolve | Evidence |
|---|---|---|---|---|
| `identity` | case manager | `require-identity` | Verify the person, property and work item mapping. | no source recorded |
| `route` | case manager | `require-route` | Verify the recipient and permitted communication route. | no source recorded |
| `triage` | case manager | `require-triage` | Claude read this as a possible urgent hazard. A case manager must take over now and apply the urgent procedure. | Split from case bb1c8adfab87: Event 012 — Email from Daniel Hart (Heating Contractor, Brackenridge Heat Services) |

### Missing information and conflicting facts

- None recorded by the latest reading.
- 2 extracted claim(s) remain **unverified source assertions** (see REASONING.md); none was treated as verified authority.

## Final decision — system case `d826e3f15079`

- **Decision (policy outcome):** **HUMAN REVIEW**
- **Proposed next action:** `clarify` — Plug-in heater casing overheating (category appliance)
- **Next step:** Verify the person, property and work item mapping.
- **Owner:** case manager
- **Case state:** open · policy v1
- **Split from system case** `bb1c8adfab87` as a separate issue.

**Latest reading (model, high confidence, route `urgent_hazard`):** Tenant reports living-room temperature of 12
insufficient heating and a plug-in heater whose casing becomes unusually hot, which she has stopped using. She may stay with her niece tonight if transport can be arranged, but accessibility there is unconfirmed.

### Actions taken

- **No operational action was executed.** Nothing was booked, instructed, paid or sent. The system recorded readings, claims and policy assessments only.

### Escalated to a person (handover)

| Check | Owner | Rule | What the person must resolve | Evidence |
|---|---|---|---|---|
| `identity` | case manager | `require-identity` | Verify the person, property and work item mapping. | no source recorded |
| `route` | case manager | `require-route` | Verify the recipient and permitted communication route. | no source recorded |
| `triage` | case manager | `require-triage` | Claude read this as a possible urgent hazard. A case manager must take over now and apply the urgent procedure. | Split from case bb1c8adfab87: Event 008 — SMS from Leah Venn (Tenant) |

### Missing information and conflicting facts

- None recorded by the latest reading.
- 1 extracted claim(s) remain **unverified source assertions** (see REASONING.md); none was treated as verified authority.

## Final decision — system case `bb1c8adfab87`

- **Decision (policy outcome):** **HUMAN REVIEW**
- **Proposed next action:** `confirm_appointment` — Cold radiators and unresponsive heating controller (category other)
- **Next step:** Verify the person, property and work item mapping.
- **Owner:** case manager
- **Case state:** open · policy v1

**Latest reading (claude-opus-5, high confidence, route `confirm_appointment`):** Contractor Daniel Hart reports a cancellation slot on 15 January 09:00–11:00 available if booked by 17:30, at the same £168 diagnostic call-out with no repair or parts included. The slot is not booked and the tenant's direct access confirmation with call and notice is still needed.

**Why:** Message concerns arranging a visit for an already known job; slot not yet booked so no schedule claim.

### Actions taken

- **No operational action was executed.** Nothing was booked, instructed, paid or sent. The system recorded readings, claims and policy assessments only.

### Escalated to a person (handover)

| Check | Owner | Rule | What the person must resolve | Evidence |
|---|---|---|---|---|
| `identity` | case manager | `require-identity` | Verify the person, property and work item mapping. | no source recorded |
| `route` | case manager | `require-route` | Verify the recipient and permitted communication route. | no source recorded |
| `access` | access officer | `require-access` | Record consent for this visit and access method from the authorised person. A verified route is required before asking externally. | Event 013 — SMS from Leah Venn (Tenant) |
| `authority` | approver | `require-authority` | Obtain authority for this work item, provider and action. | no source recorded |
| `schedule` | case manager | `require-schedule` | Confirm the active appointment with a precise date and time. A verified route is required before asking externally. | no source recorded |
| `supported` | case manager | `require-supported` | A case manager must define a supported action for this situation. | no source recorded |

### Missing information and conflicting facts

- **availability**: The slot is offered but not booked; needs booking by 17:30 to hold it.
- **access**: Tenant's direct confirmation of access, with required call and 30 minutes' notice, is still outstanding.
- **issue_details**: Whether £168 includes VAT is not stated.
- 18 extracted claim(s) remain **unverified source assertions** (see REASONING.md); none was treated as verified authority.

## Failures

- None recorded. (Jev and Claude calls all returned; no workflow step failed.)

## Result

No approval was invented and no human response was supplied by the runner. The case is waiting on the person(s) listed in the handover above.

Trace: `REASONING.md` (why) · `AUDIT.md` (every step, actor and tool) · `evidence.json` / `records.jsonl` (raw records) · `checkpoint-NNN.json` (state after each source; kept in the local run directory, not published).
