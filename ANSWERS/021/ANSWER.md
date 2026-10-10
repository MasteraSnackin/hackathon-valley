# Property Management — case 021: Hot-water service report

> **Run assumption:** the `identity` and `route` check(s) were set aside by policy (`assumed_checks`): treated as satisfied unless a source contradicted them. Nothing was verified; every other gate (access, authority, schedule, completion, money, triage) still applied.

- **Property (as supplied, unverified):** 17 Wrenfold Quay, Larkhollow, ZZ1 1ZZ
- **Decision cutoff:** 2025-05-16T16:05:00+00:00
- **Runner status:** **settled** · execution `native_local` · sources processed 21 of 21
- **Models:** Claude `claude-opus-5` (triage effort medium); Jev `jev-1.13.0` routing
- **Commit:** `281c95a90dc8a3ddd9424b56d5decf0d9c521178` · input SHA-256 `08f3b06c9cca4e8c…`

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

## Final decision — system case `43cac6fc4e6d`

- **Decision (policy outcome):** **NO FURTHER ACTION**
- **Proposed next action:** `clarify` — Letterbox not working (category doors_locks)
- **Next step:** This action already has a confirmed simulated receipt. Select a new proposal for further work.
- **Owner:** case manager
- **Case state:** in_progress · policy v2
- **Split from system case** `82ffb1409e64` as a separate issue.

**Latest reading (model, high confidence, route `clarify`):** Maya Chen notes the hot-water maintenance request remains open, with the landlord's second-hand completion update and the tenant's earlier letterbox report on file. No new evidence or tenant confirmation provided.

### Actions taken

- `clarify` → **succeeded** via Demo contractor (simulated adapter) — Letterbox not working

### Escalated to a person (handover)

- No open human review.

### Missing information and conflicting facts

- None recorded by the latest reading.

## Final decision — system case `2c0d54d5cc56`

- **Decision (policy outcome):** **NO FURTHER ACTION**
- **Proposed next action:** `clarify` — Letterbox not working (category doors_locks)
- **Next step:** This action already has a confirmed simulated receipt. Select a new proposal for further work.
- **Owner:** case manager
- **Case state:** in_progress · policy v2
- **Split from system case** `82ffb1409e64` as a separate issue.

**Latest reading (model, medium confidence, route `clarify`):** Landlord Ravi Sethi reported by phone that his plumber attended the previous day and fixed the hot water issue, based on a text from the plumber. No work description, report, invoice or check details were provided, and the tenant's last report was still no hot water.

### Actions taken

- `clarify` → **succeeded** via Demo contractor (simulated adapter) — Letterbox not working

### Escalated to a person (handover)

- No open human review.

### Missing information and conflicting facts

- None recorded by the latest reading.
- 1 extracted claim(s) remain **unverified source assertions** (see REASONING.md); none was treated as verified authority.

## Final decision — system case `be4c43b9785f`

- **Decision (policy outcome):** **NO FURTHER ACTION**
- **Proposed next action:** `clarify` — Letterbox not working (category doors_locks)
- **Next step:** This action already has a confirmed simulated receipt. Select a new proposal for further work.
- **Owner:** case manager
- **Case state:** in_progress · policy v2
- **Split from system case** `82ffb1409e64` as a separate issue.

**Latest reading (model, medium confidence, route `clarify`):** Tenant reports still no hot water and that nobody has attended to fix the boiler. Tenant also raised a separate issue that the letterbox is not working and asked if it needs a separate report.

### Actions taken

- `clarify` → **succeeded** via Demo contractor (simulated adapter) — Letterbox not working

### Escalated to a person (handover)

- No open human review.

### Missing information and conflicting facts

- None recorded by the latest reading.
- 1 extracted claim(s) remain **unverified source assertions** (see REASONING.md); none was treated as verified authority.

## Final decision — system case `82ffb1409e64`

- **Decision (policy outcome):** **WAIT**
- **Proposed next action:** `clarify` — No hot water or shower; boiler has no power (category plumbing)
- **Next step:** Clarify before routing: No tenant confirmation or contractor report/invoice confirming hot water restored and boiler/electrical checks done.; Letterbox fault has no detail (what is broken, security impact) to allow routing.
- **Owner:** case manager
- **Case state:** open · policy v2

**Latest reading (claude-opus-5, high confidence, route `clarify`):** Maya Chen notes the hot-water maintenance request remains open, with the landlord's second-hand completion update and the tenant's earlier letterbox report on file. No new evidence or tenant confirmation provided.

**Why:** Status update with no new evidence; completion remains unverified, so clarification is still needed.

### Actions taken

- Drafted message to tenant: **awaiting_staff** (simulated channel; not sent to a real person) — “Hello Iris, Thanks for letting us know the shower and hot water aren't working and that the boiler has no power. Just a few quick questions so we can get this looked into: 1. Could you tell us the make and model of the boiler (usually on the front or a label inside the casing)? 2. Is anything else e …”
- Drafted message to tenant: **awaiting_staff** (simulated channel; not sent to a real person) — “Hello Iris, Thanks for letting us know that the shower and hot water aren't working and that the boiler has no power even after checking the switch. So we can get the right help organised, could you let us know: 1. The make and model of the boiler, if you're able to see it (often on a label on the f …”
- Drafted message to tenant: **awaiting_staff** (simulated channel; not sent to a real person) — “Hello, Thanks for your patience regarding the no hot water or shower and the boiler having no power. So that we have the right details on file, could you help with a few things? 1. If someone gets in touch to arrange attending, are you happy for them to come into the property, and how would they get …”
- Drafted message to tenant: **awaiting_staff** (simulated channel; not sent to a real person) — “Hello Iris, Thanks for letting us know there's still no hot water or shower and the boiler has no power. Sorry you're still dealing with this. So we can get things moving, could you help with a few details? 1. Has anyone been out to look at the boiler yet, and is anything else electrical in the flat …”
- Drafted message to tenant: **awaiting_staff** (simulated channel; not sent to a real person) — “Hello Iris, Thanks for your patience while we follow up on the no hot water and shower issue, with the boiler having no power. Could you let us know whether the hot water is now working at the property, or whether you're still without it? Thanks very much, Northbridge Lettings”
- Clarification `triage` to tenant: closed — Clarify before routing: Boiler make/model, whether other electrics are affected, and whether anyone in the household is vulnerable are still unknown.
- Clarification `access` to tenant: closed — Record consent for this visit and access method from the authorised person.
- Clarification `schedule` to tenant: closed — Confirm the active appointment with a precise date and time.
- Clarification `triage` to tenant: closed — Clarify before routing: Boiler make/model, whether other electrics are affected, and whether anyone in the household is vulnerable remain unknown.
- Clarification `access` to tenant: closed — Record consent for this visit and access method from the authorised person.
- Clarification `schedule` to tenant: closed — Confirm the active appointment with a precise date and time.
- Clarification `triage` to tenant: closed — Clarify before routing: No contractor name or precise date and time was given for the evening visit; attendance is only believed, not confirmed.; Whether anyone in the household is vulnerable and whether other electrics are affected remains unknown; …
- Clarification `triage` to tenant: open — Clarify before routing: Completion is second-hand with no report, invoice or evidence of boiler/electrical checks; tenant has not confirmed hot water restored.

### Escalated to a person (handover)

| Check | Owner | Rule | What the person must resolve | Evidence |
|---|---|---|---|---|
| `triage` | case manager | `require-triage` | Claude read this as a possible urgent hazard. A case manager must take over now and apply the urgent procedure. | Event 016 — Email from Maya Chen (Property Manager, Northbridge Lettings) |

### Missing information and conflicting facts

- **completion** (blocks the route): No tenant confirmation or contractor report/invoice confirming hot water restored and boiler/electrical checks done.
- **issue_details** (blocks the route): Letterbox fault has no detail (what is broken, security impact) to allow routing.
- 14 extracted claim(s) remain **unverified source assertions** (see REASONING.md); none was treated as verified authority.

## Failures

- None recorded. (Jev and Claude calls all returned; no workflow step failed.)

## Result

No approval was invented and no human response was supplied by the runner. The case is waiting on the person(s) listed in the handover above.

Trace: `REASONING.md` (why) · `AUDIT.md` (every step, actor and tool) · `evidence.json` / `records.jsonl` (raw records) · `checkpoint-NNN.json` (state after each source; kept in the local run directory, not published).
