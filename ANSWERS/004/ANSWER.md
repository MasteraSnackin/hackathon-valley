# Property Management — case 004: Front entrance lock report

*PREPARATION ONLY — not official Reality Test results. System-generated; not edited by hand.*

- **Property (as supplied, unverified):** 18 Larkspur Quay, Morrowfen, ZZ1 1ZZ
- **Decision cutoff:** 2025-09-16T08:33:00+00:00
- **Runner status:** **settled** · execution `native_local` · sources processed 23 of 23
- **Models:** Claude `claude-opus-5` (triage effort medium); Jev `jev-1.13.0` routing
- **Commit:** `26542cfa3d481aa925490db741aa4fbab8f70e3c` · input SHA-256 `cd29af163368b0bb…`

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

## Final decision — system case `75a5ba3f5ecc`

- **Decision (policy outcome):** **HUMAN REVIEW**
- **Proposed next action:** `request_quote` — Hot water running too hot (category plumbing)
- **Next step:** Verify the person, property and work item mapping.
- **Owner:** case manager
- **Case state:** open · policy v1
- **Split from system case** `2b4d6e09ed25` as a separate issue.

**Latest reading (model, medium confidence, route `request_quote`):** During a call about the existing front-door lock case, the tenant raised three further unresolved matters: a broken bedroom blind, glazing in a door the landlord had said would be addressed, and hot water she says is too hot. She asked who owns these items; the agency could not confirm status during the call.

### Actions taken

- **No operational action was executed.** Nothing was booked, instructed, paid or sent. The system recorded readings, claims and policy assessments only.

### Escalated to a person (handover)

| Check | Owner | Rule | What the person must resolve | Evidence |
|---|---|---|---|---|
| `identity` | case manager | `require-identity` | Verify the person, property and work item mapping. | no source recorded |
| `route` | case manager | `require-route` | Verify the recipient and permitted communication route. | no source recorded |
| `classification` | case manager | `require-classification` | Confirm that the category and work item match the source request. A verified route is required before asking externally. | Split from case 2b4d6e09ed25: Event 021 — Call from Nessa Vale (Tenant) |

### Missing information and conflicting facts

- None recorded by the latest reading.
- 1 extracted claim(s) remain **unverified source assertions** (see REASONING.md); none was treated as verified authority.

## Final decision — system case `d0d4a356136e`

- **Decision (policy outcome):** **HUMAN REVIEW**
- **Proposed next action:** `clarify` — Glazing in door said to be addressed previously (category windows)
- **Next step:** Verify the person, property and work item mapping.
- **Owner:** case manager
- **Case state:** open · policy v1
- **Split from system case** `2b4d6e09ed25` as a separate issue.

**Latest reading (model, medium confidence, route `clarify`):** During a call about the existing front-door lock case, the tenant raised three further unresolved matters: a broken bedroom blind, glazing in a door the landlord had said would be addressed, and hot water she says is too hot. She asked who owns these items; the agency could not confirm status during the call.

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

## Final decision — system case `173ac00cf977`

- **Decision (policy outcome):** **HUMAN REVIEW**
- **Proposed next action:** `archive` — Tenant paint touch-ups at her own expense (category other)
- **Next step:** Verify the person, property and work item mapping.
- **Owner:** case manager
- **Case state:** open · policy v1
- **Split from system case** `2b4d6e09ed25` as a separate issue.

**Latest reading (model, medium confidence, route `archive`):** Internal note from the property manager recording that the landlord has approved proceeding with the front-door lock repair or replacement, and separately agreed the tenant may carry out skirting-board paint touch-ups at her own expense.

### Actions taken

- **No operational action was executed.** Nothing was booked, instructed, paid or sent. The system recorded readings, claims and policy assessments only.

### Escalated to a person (handover)

| Check | Owner | Rule | What the person must resolve | Evidence |
|---|---|---|---|---|
| `identity` | case manager | `require-identity` | Verify the person, property and work item mapping. | no source recorded |
| `authority` | approver | `require-authority` | Obtain authority for this work item, provider and action. | no source recorded |

### Missing information and conflicting facts

- None recorded by the latest reading.

## Final decision — system case `974598b017cd`

- **Decision (policy outcome):** **HUMAN REVIEW**
- **Proposed next action:** `clarify` — Tenant to do skirting-board paint touch-ups at own expense (category other)
- **Next step:** Verify the person, property and work item mapping.
- **Owner:** case manager
- **Case state:** open · policy v1
- **Split from system case** `2b4d6e09ed25` as a separate issue.

**Latest reading (model, medium confidence, route `unsupported`):** Property manager reports a call with the landlord, who is away, asks for email contact, and states the front-door work should already have been done. He also agreed during the call that the tenant may do skirting-board paint touch-ups at her own expense.

### Actions taken

- **No operational action was executed.** Nothing was booked, instructed, paid or sent. The system recorded readings, claims and policy assessments only.

### Escalated to a person (handover)

| Check | Owner | Rule | What the person must resolve | Evidence |
|---|---|---|---|---|
| `identity` | case manager | `require-identity` | Verify the person, property and work item mapping. | no source recorded |
| `route` | case manager | `require-route` | Verify the recipient and permitted communication route. | no source recorded |

### Missing information and conflicting facts

- None recorded by the latest reading.

## Final decision — system case `2b4d6e09ed25`

- **Decision (policy outcome):** **STOP ACTION**
- **Proposed next action:** `confirm_appointment` — Front-door lock loose and intermittent; door catches (category doors_locks)
- **Next step:** Confirm the active appointment with a precise date and time.
- **Owner:** case manager
- **Case state:** open · policy v1

**Latest reading (claude-opus-5, medium confidence, route `confirm_appointment`):** Tenant reports the landlord's contractor is due to attend that day sometime after 10:00, with no narrower time given, and will update the agency. No confirmation of attendance or of the lock being repaired or replaced.

**Why:** Message concerns timing of an expected contractor visit on a known job; no firm time or completion asserted.

### Actions taken

- **No operational action was executed.** Nothing was booked, instructed, paid or sent. The system recorded readings, claims and policy assessments only.

### Escalated to a person (handover)

| Check | Owner | Rule | What the person must resolve | Evidence |
|---|---|---|---|---|
| `schedule` | case manager | `require-schedule` | Confirm the active appointment with a precise date and time. | Event 017 — Email from Mira Sol (Property Manager, Northbridge Lettings) |
| `identity` | case manager | `require-identity` | Verify the person, property and work item mapping. | no source recorded |
| `route` | case manager | `require-route` | Verify the recipient and permitted communication route. | no source recorded |
| `access` | access officer | `require-access` | Record consent for this visit and access method from the authorised person. A verified route is required before asking externally. | no source recorded |
| `authority` | approver | `require-authority` | Obtain authority for this work item, provider and action. | no source recorded |

### Missing information and conflicting facts

- **availability**: No precise appointment time: contractor said "after 10:00" that day with no narrower window; confirmation of attendance needed.
- **completion**: Unknown whether the lock has been repaired or replaced; tenant has not confirmed.
- 2 extracted claim(s) remain **unverified source assertions** (see REASONING.md); none was treated as verified authority.

## Failures

- None recorded. (Jev and Claude calls all returned; no workflow step failed.)

## Result

No approval was invented and no human response was supplied by the runner. The case is waiting on the person(s) listed in the handover above.

Trace: `REASONING.md` (why) · `AUDIT.md` (every step, actor and tool) · `evidence.json` / `records.jsonl` (raw records) · `checkpoint-NNN.json` (state after each source; kept in the local run directory, not published).
