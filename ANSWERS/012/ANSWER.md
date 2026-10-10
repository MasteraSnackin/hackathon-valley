# Property Management — case 012: Lock Maintenance Request

*PREPARATION ONLY — not official Reality Test results. System-generated; not edited by hand.*

- **Property (as supplied, unverified):** Unit 2, 18 Brindlewick Mews, Orellin ZZ1 1ZZ
- **Decision cutoff:** 2025-09-25T12:06:33+00:00
- **Runner status:** **settled** · execution `native_local` · sources processed 25 of 25
- **Models:** Claude `claude-opus-5` (triage effort medium); Jev `jev-1.13.0` routing
- **Commit:** `26542cfa3d481aa925490db741aa4fbab8f70e3c` · input SHA-256 `9f2327bea788a66b…`

All operational tools in this run are clearly labelled **simulated** adapters: no real tenant, landlord or contractor was contacted, nothing was paid or booked, and a simulated receipt does not prove work happened.

## What the system received

The initial report and 24 further sources, submitted one at a time in availability order; each was processed and settled before the next became visible. Full text: `input.json`.

| # | Available at | Source |
|---|---|---|
| 0 | 2025-09-04T08:08:44+00:00 | Initial report — Event 001 — Portal |
| 1 | 2025-09-04T09:14:23+00:00 | Event 002 — Email from Ilyra Venn (Property Manager, Northbridge Lettings) |
| 2 | 2025-09-04T10:22:19+00:00 | Event 003 — Email from Sella Marr (Landlord, Northbridge Lettings) |
| 3 | 2025-09-04T14:29:18+00:00 | Event 004 — Email from Ilyra Venn (Property Manager, Northbridge Lettings) |
| 4 | 2025-09-09T15:32:14+00:00 | Event 005 — Email from Ilyra Venn (Property Manager, Northbridge Lettings) |
| 5 | 2025-09-09T15:35:28+00:00 | Event 006 — Call from Ilyra Venn (Property Manager, Northbridge Lettings) |
| 6 | 2025-09-10T15:32:09+00:00 | Event 007 — Email from Ilyra Venn (Property Manager, Northbridge Lettings) |
| 7 | 2025-09-11T09:10:18+00:00 | Event 008 — Email from Perrin Dall (Tenant, Northbridge Lettings) |
| 8 | 2025-09-11T09:11:04+00:00 | Event 009 — Email from Ilyra Venn (Property Manager, Northbridge Lettings) |
| 9 | 2025-09-11T09:58:33+00:00 | Event 010 — Call from Tarin Vale (Contractor, Hearthline Access) |
| 10 | 2025-09-11T12:00:35+00:00 | Event 011 — Email from Ilyra Venn (Property Manager, Northbridge Lettings) |
| 11 | 2025-09-11T15:05:35+00:00 | Event 012 — Email from Ilyra Venn (Property Manager, Northbridge Lettings) |
| 12 | 2025-09-11T15:05:39+00:00 | Event 013 — Update from Ilyra Venn (Property Manager, Northbridge Lettings) |
| 13 | 2025-09-11T15:05:50+00:00 | Event 014 — Email from Ilyra Venn (Property Manager, Northbridge Lettings) |
| 14 | 2025-09-11T15:05:54+00:00 | Event 015 — Email from Ilyra Venn (Property Manager, Northbridge Lettings) |
| 15 | 2025-09-11T15:28:21+00:00 | Event 016 — Email from Tarin Vale (Contractor, Hearthline Access) |
| 16 | 2025-09-11T15:37:29+00:00 | Event 017 — Email from Perrin Dall (Tenant, Northbridge Lettings) |
| 17 | 2025-09-11T15:38:12+00:00 | Event 018 — Email from Ilyra Venn (Property Manager, Northbridge Lettings) |
| 18 | 2025-09-14T04:57:12+00:00 | Event 019 — Email from Perrin Dall (Tenant, Northbridge Lettings) |
| 19 | 2025-09-14T04:58:07+00:00 | Event 020 — Email from Ilyra Venn (Property Manager, Northbridge Lettings) |
| 20 | 2025-09-15T08:01:36+00:00 | Event 021 — Email from Ilyra Venn (Property Manager, Northbridge Lettings) |
| 21 | 2025-09-17T09:45:57+00:00 | Event 022 — Call from Ilyra Venn (Property Manager, Northbridge Lettings) |
| 22 | 2025-09-22T10:07:54+00:00 | Event 023 — Call from Ilyra Venn (Property Manager, Northbridge Lettings) |
| 23 | 2025-09-24T09:42:09+00:00 | Event 024 — Note from Ilyra Venn (Property Manager, Northbridge Lettings) |
| 24 | 2025-09-25T12:06:33+00:00 | Event 025 — Call from Ilyra Venn (Property Manager, Northbridge Lettings) |

## Final decision — system case `cbe9f303f698`

- **Decision (policy outcome):** **HUMAN REVIEW**
- **Proposed next action:** `request_quote` — Mould appearing in bathroom (category other)
- **Next step:** Verify the person, property and work item mapping.
- **Owner:** case manager
- **Case state:** open · policy v1
- **Split from system case** `8f694f83c9f0` as a separate issue.

**Latest reading (model, medium confidence, route `request_quote`):** Tenant clarifies via call that the faults concern opening-sash window locks, not internal door locks: bedroom sash will not lock, bathroom sash is stuck with sticking locking buttons, and the kitchen sash has no key. Tenant grants access for tradespeople but no key handover arrangement or appointment date is given, and newly mentions mould in the bathroom.

### Actions taken

- **No operational action was executed.** Nothing was booked, instructed, paid or sent. The system recorded readings, claims and policy assessments only.

### Escalated to a person (handover)

| Check | Owner | Rule | What the person must resolve | Evidence |
|---|---|---|---|---|
| `identity` | case manager | `require-identity` | Verify the person, property and work item mapping. | no source recorded |
| `route` | case manager | `require-route` | Verify the recipient and permitted communication route. | no source recorded |
| `classification` | case manager | `require-classification` | Confirm that the category and work item match the source request. A verified route is required before asking externally. | no source recorded |
| `supported` | case manager | `require-supported` | A case manager must define a supported action for this situation. | no source recorded |

### Missing information and conflicting facts

- None recorded by the latest reading.

## Final decision — system case `1c3916e6e294`

- **Decision (policy outcome):** **HUMAN REVIEW**
- **Proposed next action:** `request_quote` — Kitchen sash has no key (category windows)
- **Next step:** Verify the person, property and work item mapping.
- **Owner:** case manager
- **Case state:** open · policy v1
- **Split from system case** `8f694f83c9f0` as a separate issue.

**Latest reading (model, medium confidence, route `request_quote`):** Tenant clarifies via call that the faults concern opening-sash window locks, not internal door locks: bedroom sash will not lock, bathroom sash is stuck with sticking locking buttons, and the kitchen sash has no key. Tenant grants access for tradespeople but no key handover arrangement or appointment date is given, and newly mentions mould in the bathroom.

### Actions taken

- **No operational action was executed.** Nothing was booked, instructed, paid or sent. The system recorded readings, claims and policy assessments only.

### Escalated to a person (handover)

| Check | Owner | Rule | What the person must resolve | Evidence |
|---|---|---|---|---|
| `identity` | case manager | `require-identity` | Verify the person, property and work item mapping. | no source recorded |
| `route` | case manager | `require-route` | Verify the recipient and permitted communication route. | no source recorded |
| `classification` | case manager | `require-classification` | Confirm that the category and work item match the source request. A verified route is required before asking externally. | Split from case 8f694f83c9f0: Event 006 — Call from Ilyra Venn (Property Manager, Northbridge Lettings) |

### Missing information and conflicting facts

- None recorded by the latest reading.
- 1 extracted claim(s) remain **unverified source assertions** (see REASONING.md); none was treated as verified authority.

## Final decision — system case `395cb087080c`

- **Decision (policy outcome):** **HUMAN REVIEW**
- **Proposed next action:** `request_quote` — Bedroom sash opens but will not lock (category windows)
- **Next step:** Verify the person, property and work item mapping.
- **Owner:** case manager
- **Case state:** open · policy v1
- **Split from system case** `8f694f83c9f0` as a separate issue.

**Latest reading (model, medium confidence, route `request_quote`):** Tenant clarifies via call that the faults concern opening-sash window locks, not internal door locks: bedroom sash will not lock, bathroom sash is stuck with sticking locking buttons, and the kitchen sash has no key. Tenant grants access for tradespeople but no key handover arrangement or appointment date is given, and newly mentions mould in the bathroom.

### Actions taken

- **No operational action was executed.** Nothing was booked, instructed, paid or sent. The system recorded readings, claims and policy assessments only.

### Escalated to a person (handover)

| Check | Owner | Rule | What the person must resolve | Evidence |
|---|---|---|---|---|
| `identity` | case manager | `require-identity` | Verify the person, property and work item mapping. | no source recorded |
| `route` | case manager | `require-route` | Verify the recipient and permitted communication route. | no source recorded |
| `classification` | case manager | `require-classification` | Confirm that the category and work item match the source request. A verified route is required before asking externally. | Split from case 8f694f83c9f0: Event 006 — Call from Ilyra Venn (Property Manager, Northbridge Lettings) |

### Missing information and conflicting facts

- None recorded by the latest reading.
- 1 extracted claim(s) remain **unverified source assertions** (see REASONING.md); none was treated as verified authority.

## Final decision — system case `073084709ae9`

- **Decision (policy outcome):** **HUMAN REVIEW**
- **Proposed next action:** `clarify` — Missing keys (category doors_locks)
- **Next step:** Verify the person, property and work item mapping.
- **Owner:** case manager
- **Case state:** open · policy v1
- **Split from system case** `8f694f83c9f0` as a separate issue.

**Latest reading (model, medium confidence, route `clarify`):** Tenant at Unit 2, 18 Brindlewick Mews reports the bathroom window will not open and the bedroom window opens but will not secure, and also reports that keys are missing.

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

## Final decision — system case `fda327516e30`

- **Decision (policy outcome):** **HUMAN REVIEW**
- **Proposed next action:** `request_quote` — Bedroom window opens but will not secure (category windows)
- **Next step:** Verify the person, property and work item mapping.
- **Owner:** case manager
- **Case state:** open · policy v1
- **Split from system case** `8f694f83c9f0` as a separate issue.

**Latest reading (model, medium confidence, route `request_quote`):** Tenant at Unit 2, 18 Brindlewick Mews reports the bathroom window will not open and the bedroom window opens but will not secure, and also reports that keys are missing.

### Actions taken

- **No operational action was executed.** Nothing was booked, instructed, paid or sent. The system recorded readings, claims and policy assessments only.

### Escalated to a person (handover)

| Check | Owner | Rule | What the person must resolve | Evidence |
|---|---|---|---|---|
| `identity` | case manager | `require-identity` | Verify the person, property and work item mapping. | no source recorded |
| `route` | case manager | `require-route` | Verify the recipient and permitted communication route. | no source recorded |
| `classification` | case manager | `require-classification` | Confirm that the category and work item match the source request. A verified route is required before asking externally. | Split from case 8f694f83c9f0: Intake report |

### Missing information and conflicting facts

- None recorded by the latest reading.
- 1 extracted claim(s) remain **unverified source assertions** (see REASONING.md); none was treated as verified authority.

## Final decision — system case `8f694f83c9f0`

- **Decision (policy outcome):** **HUMAN REVIEW**
- **Proposed next action:** `close_item` — Bathroom window will not open (category windows)
- **Next step:** Verify the person, property and work item mapping.
- **Owner:** case manager
- **Case state:** open · policy v1

**Latest reading (claude-opus-5, medium confidence, route `close_item`):** Contractor Edrin Moss again states the bathroom window work is complete and promises to send the invoice later today. No invoice, appointment record or attendance evidence is on file.

**Why:** Contractor reports the work item finished, matching the close_item route, though supporting evidence remains outstanding.

### Actions taken

- **No operational action was executed.** Nothing was booked, instructed, paid or sent. The system recorded readings, claims and policy assessments only.

### Escalated to a person (handover)

| Check | Owner | Rule | What the person must resolve | Evidence |
|---|---|---|---|---|
| `identity` | case manager | `require-identity` | Verify the person, property and work item mapping. | no source recorded |
| `commitments` | case manager | `require-commitments` | Resolve or explicitly cancel every outstanding commitment for this item. A verified route is required before asking externally. | no source recorded |
| `completion` | reviewer | `require-completion` | Verify completion of this work item with usable evidence. A verified route is required before asking externally. | Event 023 — Call from Ilyra Venn (Property Manager, Northbridge Lettings), Event 024 — Note from Ilyra Venn (Property Manager, Northbridge Lettings), Event 025 — Call from Ilyra Venn (Property Manager, Northbridge Lettin … |

### Missing information and conflicting facts

- **completion**: Completion is still asserted verbally only; no invoice, attendance record or work description has been supplied to verify it.
- **access**: No record of how entry was obtained; keys were previously said not to have been collected and three attempts failed.
- 10 extracted claim(s) remain **unverified source assertions** (see REASONING.md); none was treated as verified authority.

## Failures

- None recorded. (Jev and Claude calls all returned; no workflow step failed.)

## Result

No approval was invented and no human response was supplied by the runner. The case is waiting on the person(s) listed in the handover above.

Trace: `REASONING.md` (why) · `AUDIT.md` (every step, actor and tool) · `evidence.json` / `records.jsonl` (raw records) · `checkpoint-NNN.json` (state after each source; kept in the local run directory, not published).
