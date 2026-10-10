# Property Management — case 021: Hot-water service report

*PREPARATION ONLY — not official Reality Test results. System-generated; not edited by hand.*

- **Property (as supplied, unverified):** 17 Wrenfold Quay, Larkhollow, ZZ1 1ZZ
- **Decision cutoff:** 2025-05-16T16:05:00+00:00
- **Runner status:** **settled** · execution `native_local` · sources processed 21 of 21
- **Models:** Claude `claude-opus-5` (triage effort medium); Jev `jev-1.13.0` routing
- **Commit:** `26542cfa3d481aa925490db741aa4fbab8f70e3c` · input SHA-256 `08f3b06c9cca4e8c…`

All operational tools in this run are clearly labelled **simulated** adapters: no real tenant, landlord or contractor was contacted, nothing was paid or booked, and a simulated receipt does not prove work happened.

## What the system received

The initial report and 20 further sources, submitted one at a time in availability order; each was processed and settled before the next became visible. Full text: `input.json`.

| # | Available at | Source |
|---|---|---|
| 0 | 2025-05-06T08:14:00+00:00 | Initial report — Event 001 — Portal |
| 1 | 2025-05-06T08:31:00+00:00 | Event 002 — Email from Maya Chen (Property Manager, Northbridge Lettings) |
| 2 | 2025-05-06T09:02:00+00:00 | Event 003 — Call from Maya Chen (Property Manager, Northbridge Lettings) |
| 3 | 2025-05-06T09:03:00+00:00 | Event 004 — Call from Maya Chen (Property Manager, Northbridge Lettings) |
| 4 | 2025-05-06T09:17:00+00:00 | Event 005 — Note from Maya Chen (Property Manager, Northbridge Lettings) |
| 5 | 2025-05-06T09:24:00+00:00 | Event 006 — Email from Maya Chen (Property Manager, Northbridge Lettings) |
| 6 | 2025-05-06T09:34:00+00:00 | Event 007 — Update from Maya Chen (Property Manager, Northbridge Lettings) |
| 7 | 2025-05-06T09:35:00+00:00 | Event 008 — Email from Maya Chen (Property Manager, Northbridge Lettings) |
| 8 | 2025-05-06T09:36:00+00:00 | Event 009 — Email from Maya Chen (Property Manager, Northbridge Lettings) |
| 9 | 2025-05-06T09:40:00+00:00 | Event 010 — Call from Maya Chen (Property Manager, Northbridge Lettings) |
| 10 | 2025-05-11T10:00:00+00:00 | Event 011 — Email from Maya Chen (Property Manager, Northbridge Lettings) |
| 11 | 2025-05-11T10:03:00+00:00 | Event 012 — Email from Iris Vale (Tenant, resident) |
| 12 | 2025-05-11T10:30:00+00:00 | Event 013 — Email from Maya Chen (Property Manager, Northbridge Lettings) |
| 13 | 2025-05-11T10:35:00+00:00 | Event 014 — Call from Maya Chen (Property Manager, Northbridge Lettings) |
| 14 | 2025-05-12T16:20:00+00:00 | Event 015 — Call from Maya Chen (Property Manager, Northbridge Lettings) |
| 15 | 2025-05-13T09:00:00+00:00 | Event 016 — Email from Maya Chen (Property Manager, Northbridge Lettings) |
| 16 | 2025-05-13T09:05:00+00:00 | Event 017 — Call from Maya Chen (Property Manager, Northbridge Lettings) |
| 17 | 2025-05-15T08:37:00+00:00 | Event 018 — Call from Maya Chen (Property Manager, Northbridge Lettings) |
| 18 | 2025-05-15T08:38:00+00:00 | Event 019 — Call from Maya Chen (Property Manager, Northbridge Lettings) |
| 19 | 2025-05-15T08:45:00+00:00 | Event 020 — Email from Maya Chen (Property Manager, Northbridge Lettings) |
| 20 | 2025-05-16T16:05:00+00:00 | Event 021 — Update from Maya Chen (Property Manager, Northbridge Lettings) |

## Final decision — system case `35898bfbf0ff`

- **Decision (policy outcome):** **HUMAN REVIEW**
- **Proposed next action:** `clarify` — Letterbox not working (category other)
- **Next step:** Verify the person, property and work item mapping.
- **Owner:** case manager
- **Case state:** open · policy v1
- **Split from system case** `3b7cd7857ae6` as a separate issue.

**Latest reading (model, high confidence, route `clarify`):** Property manager notes the hot-water maintenance request remains open, with the landlord's update and the tenant's earlier letterbox report on file. No new confirmation from the tenant and no plumber report.

### Actions taken

- **No operational action was executed.** Nothing was booked, instructed, paid or sent. The system recorded readings, claims and policy assessments only.

### Escalated to a person (handover)

| Check | Owner | Rule | What the person must resolve | Evidence |
|---|---|---|---|---|
| `identity` | case manager | `require-identity` | Verify the person, property and work item mapping. | no source recorded |
| `route` | case manager | `require-route` | Verify the recipient and permitted communication route. | no source recorded |

### Missing information and conflicting facts

- None recorded by the latest reading.

## Final decision — system case `38616dcb346f`

- **Decision (policy outcome):** **HUMAN REVIEW**
- **Proposed next action:** `clarify` — Letterbox not working (category doors_locks)
- **Next step:** Verify the person, property and work item mapping.
- **Owner:** case manager
- **Case state:** open · policy v1
- **Split from system case** `3b7cd7857ae6` as a separate issue.

**Latest reading (model, medium confidence, route `clarify`):** Landlord Ravi Sethi reported by phone that his plumber attended the previous day and fixed the hot water issue, based on a text from the plumber. No work description, report, invoice or check details were provided, and the tenant has not confirmed restoration.

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

## Final decision — system case `ae3efdc97f91`

- **Decision (policy outcome):** **HUMAN REVIEW**
- **Proposed next action:** `clarify` — Letterbox not working (category doors_locks)
- **Next step:** Verify the person, property and work item mapping.
- **Owner:** case manager
- **Case state:** open · policy v1
- **Split from system case** `3b7cd7857ae6` as a separate issue.

**Latest reading (model, medium confidence, route `clarify`):** Tenant reports still no hot water and no contractor attendance despite landlord's assurances. Tenant also raised a separate letterbox fault and asked whether it should be reported separately.

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

## Final decision — system case `3b7cd7857ae6`

- **Decision (policy outcome):** **HUMAN REVIEW**
- **Proposed next action:** `clarify` — No hot water or shower - boiler has no power (category plumbing)
- **Next step:** Verify the person, property and work item mapping.
- **Owner:** case manager
- **Case state:** open · policy v1

**Latest reading (claude-opus-5, high confidence, route `clarify`):** Property manager notes the hot-water maintenance request remains open, with the landlord's update and the tenant's earlier letterbox report on file. No new confirmation from the tenant and no plumber report.

**Why:** Internal status note with no new facts; completion unverified so the item stays at clarify.

### Actions taken

- **No operational action was executed.** Nothing was booked, instructed, paid or sent. The system recorded readings, claims and policy assessments only.

### Escalated to a person (handover)

| Check | Owner | Rule | What the person must resolve | Evidence |
|---|---|---|---|---|
| `identity` | case manager | `require-identity` | Verify the person, property and work item mapping. | no source recorded |
| `route` | case manager | `require-route` | Verify the recipient and permitted communication route. | no source recorded |
| `triage` | case manager | `require-triage` | Claude read this as a possible urgent hazard. A case manager must take over now and apply the urgent procedure. | Event 017 — Call from Maya Chen (Property Manager, Northbridge Lettings) |

### Missing information and conflicting facts

- **completion** (blocks the route): Tenant has still not confirmed whether hot water is restored; no work description, report or invoice from the landlord's plumber.
- **issue_details** (blocks the route): No detail on the letterbox fault (what is broken, security impact) to allow it to be raised as its own item.
- 10 extracted claim(s) remain **unverified source assertions** (see REASONING.md); none was treated as verified authority.

## Failures

- None recorded. (Jev and Claude calls all returned; no workflow step failed.)

## Result

No approval was invented and no human response was supplied by the runner. The case is waiting on the person(s) listed in the handover above.

Trace: `REASONING.md` (why) · `AUDIT.md` (every step, actor and tool) · `evidence.json` / `records.jsonl` (raw records) · `checkpoint-NNN.json` (state after each source; kept in the local run directory, not published).
