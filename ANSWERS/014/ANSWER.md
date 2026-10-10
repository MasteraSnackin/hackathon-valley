# Property Management — case 014: Heating service request at 7 Mallowmere Walk

> **Run assumption:** the `identity` and `route` check(s) were set aside by policy (`assumed_checks`): treated as satisfied unless a source contradicted them. Nothing was verified; every other gate (access, authority, schedule, completion, money, triage) still applied.

- **Property (as supplied, unverified):** 7 Mallowmere Walk, Larkfen, ZZ1 1ZZ
- **Decision cutoff:** 2025-01-14T17:08:00+00:00
- **Runner status:** **settled** · execution `native_local` · sources processed 19 of 19
- **Models:** Claude `claude-opus-5` (triage effort medium); Jev `jev-1.13.0` routing
- **Commit:** `281c95a90dc8a3ddd9424b56d5decf0d9c521178` · input SHA-256 `d103d0e8d228e4f0…`

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

## Final decision — system case `817ba5f476ab`

- **Decision (policy outcome):** **HUMAN REVIEW**
- **Proposed next action:** `clarify` — Plug-in heater casing becoming unusually hot (category appliance)
- **Next step:** Claude read this as a possible urgent hazard. A case manager must take over now and apply the urgent procedure.
- **Owner:** case manager
- **Case state:** open · policy v2
- **Split from system case** `6d4b8896e387` as a separate issue.

**Latest reading (model, high confidence, route `urgent_hazard`):** Tenant reports living-room temperature of 12°C with heating still off, and that her only plug-in heater overheats so she has stopped using it. She may stay with her niece tonight if transport can be arranged but has not confirmed this.

### Actions taken

- **No operational action was executed.** Nothing was booked, instructed, paid or sent. The system recorded readings, claims and policy assessments only.

### Escalated to a person (handover)

| Check | Owner | Rule | What the person must resolve | Evidence |
|---|---|---|---|---|
| `triage` | case manager | `require-triage` | Claude read this as a possible urgent hazard. A case manager must take over now and apply the urgent procedure. | Split from case 6d4b8896e387: Event 008 — SMS from Leah Venn (Tenant) |

### Missing information and conflicting facts

- None recorded by the latest reading.
- 1 extracted claim(s) remain **unverified source assertions** (see REASONING.md); none was treated as verified authority.

## Final decision — system case `6d4b8896e387`

- **Decision (policy outcome):** **HUMAN REVIEW**
- **Proposed next action:** `clarify` — Cold radiators and unresponsive heating controller (category plumbing)
- **Next step:** Claude read this as a possible urgent hazard. A case manager must take over now and apply the urgent procedure.
- **Owner:** case manager
- **Case state:** open · policy v2

**Latest reading (claude-opus-5, medium confidence, route `urgent_hazard`):** Contractor Daniel Hart reports a cancellation slot on 15 January 09:00–11:00, holdable only if booked by 17:30, at the same £168 diagnostic call-out with no repair work included. The slot is not booked and the tenant's direct access confirmation is still needed.

**Why:** Router flagged possible urgent no-heating hazard for a vulnerable tenant; message itself is an appointment offer not yet booked and no access confirmed.

### Actions taken

- Drafted message to tenant: **awaiting_staff** (simulated channel; not sent to a real person) — “Hello Leah, Thanks for letting us know that the radiators are cold and the heating controller is unresponsive, and that you still have hot water. So we can get this looked at properly, could you let us know whether anyone in the household might be particularly affected by being without heating \u201 …”
- Drafted message to tenant: **sent** (simulated channel; not sent to a real person) — “Hello Leah, Thanks for letting us know that your radiators are cold and the heating controller is unresponsive, with hot water still working. So we have the full picture, could you let us know what the boiler display is showing at the moment (any numbers, codes or warning lights), and whether you've …”
- Drafted message to tenant: **awaiting_staff** (simulated channel; not sent to a real person) — “Hello Leah, Thanks for confirming there's no gas smell or visible leak and that the boiler display is blank. So we can arrange things to suit you, could you let us know: 1. Who would be at the property to let someone in, and how you'd like them to let you know they've arrived (for example, a call fr …”
- Drafted message to tenant: **awaiting_staff** (simulated channel; not sent to a real person) — “Hello Leah, Thanks for confirming there's no gas smell or visible leak and that the boiler display is blank. So we can get things moving, could you let us know who will be at the property to let an engineer in, and the best number for them to call from outside before coming to the door? It would als …”
- Clarification `triage` to tenant: closed — Clarify before routing: Confirm whether anyone in the household is vulnerable or at risk from lack of heating, which could make this urgent.
- Clarification `classification` to tenant: closed — Confirm that the category and work item match the source request.
- Clarification `triage` to tenant: open — Clarify before routing: No access arrangement is confirmed for the tenant herself; only that the niece may not grant access or approve work. Need confirmation of who will let the contractor in and how.; No date or time has been proposed or agreed for …

### Escalated to a person (handover)

| Check | Owner | Rule | What the person must resolve | Evidence |
|---|---|---|---|---|
| `triage` | case manager | `require-triage` | Claude read this as a possible urgent hazard. A case manager must take over now and apply the urgent procedure. | Event 003 — SMS from Leah Venn (Tenant) |

### Missing information and conflicting facts

- **access** (blocks the route): Tenant's direct confirmation of access, with the required call and 30 minutes' notice, is still outstanding.
- **availability**: The 15 January 09:00–11:00 slot is offered but not booked and must be confirmed by 17:30.
- 22 extracted claim(s) remain **unverified source assertions** (see REASONING.md); none was treated as verified authority.

## Failures

- None recorded. (Jev and Claude calls all returned; no workflow step failed.)

## Result

No approval was invented and no human response was supplied by the runner. The case is waiting on the person(s) listed in the handover above.

Trace: `REASONING.md` (why) · `AUDIT.md` (every step, actor and tool) · `evidence.json` / `records.jsonl` (raw records) · `checkpoint-NNN.json` (state after each source; kept in the local run directory, not published).
