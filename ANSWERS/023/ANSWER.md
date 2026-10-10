# Property Management — case 023: Heating maintenance at 7 Larkspur Fold

> **Run assumption:** the `identity` and `route` check(s) were set aside by policy (`assumed_checks`): treated as satisfied unless a source contradicted them. Nothing was verified; every other gate (access, authority, schedule, completion, money, triage) still applied.

- **Property (as supplied, unverified):** 7 Larkspur Fold, Orvane Heath, ZZ1 1ZZ
- **Decision cutoff:** 2025-02-12T16:35:00+00:00
- **Runner status:** **settled** · execution `native_local` · sources processed 25 of 25
- **Models:** Claude `claude-opus-5` (triage effort medium); Jev `jev-1.13.0` routing
- **Commit:** `281c95a90dc8a3ddd9424b56d5decf0d9c521178` · input SHA-256 `716258e3d16deb28…`

All operational tools in this run are clearly labelled **simulated** adapters: no real tenant, landlord or contractor was contacted, nothing was paid or booked, and a simulated receipt does not prove work happened.

## What the system received

The initial report and 24 further sources, submitted one at a time in availability order; each was processed and settled before the next became visible. Full text: `input.json`.

| # | Available at | Source |
|---|---|---|
| 0 | 2025-02-03T08:14:00+00:00 | Initial report — Event 001 — Portal |
| 1 | 2025-02-03T08:41:00+00:00 | Event 002 — Update from Ivo Merrick (Property Manager, Northbridge Lettings) |
| 2 | 2025-02-03T09:12:00+00:00 | Event 003 — Portal from Tessa Vane (Tenant) |
| 3 | 2025-02-03T10:05:00+00:00 | Event 004 — Email from Ivo Merrick (Property Manager, Northbridge Lettings) |
| 4 | 2025-02-03T12:22:00+00:00 | Event 005 — Email from Soren Dallow (Landlord) |
| 5 | 2025-02-04T09:18:00+00:00 | Event 006 — Email from Ivo Merrick (Property Manager, Northbridge Lettings) |
| 6 | 2025-02-04T10:03:00+00:00 | Event 007 — Email from Petra Quill (Contractor, Copper Finch Mechanical) |
| 7 | 2025-02-05T14:32:00+00:00 | Event 008 — Update from Petra Quill (Contractor, Copper Finch Mechanical) |
| 8 | 2025-02-05T14:54:00+00:00 | Event 009 — Email from Petra Quill (Contractor, Copper Finch Mechanical) |
| 9 | 2025-02-05T15:21:00+00:00 | Event 010 — Email from Ivo Merrick (Property Manager, Northbridge Lettings) |
| 10 | 2025-02-06T07:56:00+00:00 | Event 011 — SMS from Tessa Vane (Tenant) |
| 11 | 2025-02-06T10:38:00+00:00 | Event 012 — Email from Soren Dallow (Landlord) |
| 12 | 2025-02-06T13:17:00+00:00 | Event 013 — Portal from Ivo Merrick (Property Manager, Northbridge Lettings) |
| 13 | 2025-02-06T14:06:00+00:00 | Event 014 — Portal from Tessa Vane (Tenant) |
| 14 | 2025-02-07T09:24:00+00:00 | Event 015 — Email from Ivo Merrick (Property Manager, Northbridge Lettings) |
| 15 | 2025-02-07T13:47:00+00:00 | Event 016 — Email from Petra Quill (Contractor, Copper Finch Mechanical) |
| 16 | 2025-02-10T09:52:00+00:00 | Event 017 — Email from Petra Quill (Contractor, Copper Finch Mechanical) |
| 17 | 2025-02-10T10:26:00+00:00 | Event 018 — Document from Petra Quill (Contractor, Copper Finch Mechanical) |
| 18 | 2025-02-10T11:11:00+00:00 | Event 019 — Note from Ivo Merrick (Property Manager, Northbridge Lettings) |
| 19 | 2025-02-10T15:08:00+00:00 | Event 020 — Portal from Tessa Vane (Tenant) |
| 20 | 2025-02-11T09:16:00+00:00 | Event 021 — Email from Ivo Merrick (Property Manager, Northbridge Lettings) |
| 21 | 2025-02-12T11:42:00+00:00 | Event 022 — Email from Petra Quill (Contractor, Copper Finch Mechanical) |
| 22 | 2025-02-12T16:35:00+00:00 | Event 023 — Email from Ivo Merrick (Property Manager, Northbridge Lettings) |
| 23 | 2025-02-12T16:35:00+00:00 | Attachment invoice-NBL-CFM-250210-A.pdf (PDF text extraction) |
| 24 | 2025-02-12T16:35:00+00:00 | Attachment invoice-NBL-CFM-250210-B.pdf (PDF text extraction) |

## Final decision — system case `905bdba959da`

- **Decision (policy outcome):** **WAIT**
- **Proposed next action:** `clarify` — Intermittent heating failure (radiators), hot water unaffected (category other)
- **Next step:** Clarify before routing: Whether invoice B (£372.00) supersedes or sits alongside invoice A (£138.00) for the same 5 February service date; overlapping attendance and diagnosis charges are unresolved.; No parts record, attendance evidence or confirmation that the actuator replacement was actually carried out or that the heating fault is resolved.; No written landlord authorisation on file for actuator replacement; authority covered diagnosis only.
- **Owner:** case manager
- **Case state:** open · policy v2

**Latest reading (claude-opus-5, high confidence, route `clarify`):** Second invoice from Copper Finch Mechanical (NBL-CFM-250210-B) for £372.00 inc VAT covering heating valve actuator supply and replacement, same 5 February service date as the £138.00 invoice A. It is still unstated whether this supersedes or duplicates the other record, and no authorisation or completion evidence is provided.

**Why:** Billing document adds a second overlapping invoice without authorisation or completion evidence; clarification needed before any payment or further action.

### Actions taken

- Drafted message to tenant: **awaiting_staff** (simulated channel; not sent to a real person) — “Hello Tessa, Thanks for letting us know the radiator heating has cut out twice while your hot water is still working. So we can get this looked at properly, could you tell us how things stand at the moment: is the heating currently off, and have you noticed any leaks, unusual smells, or any warning …”
- Drafted message to tenant: **sent** (simulated channel; not sent to a real person) — “Hi Tessa, Thanks for getting back to us with those details — that's really helpful. Just one more thing: could you let us know whether the radiators are heating up at the moment, and if the boiler shows any symbol or code on its display now (a photo of the screen would be great if anything appears)? …”
- Drafted message to tenant: **sent** (simulated channel; not sent to a real person) — “Hi Tessa, Thanks again for the details about the radiators not heating properly. We're looking at arranging for an engineer to come and take a look on Thursday 5 February, sometime after 2pm. Could you let us know if someone aged 18 or over would be able to be home then to let them in, and if not, h …”
- Drafted message to tenant: **awaiting_staff** (simulated channel; not sent to a real person) — “Hi Tessa, Thanks for your patience while we look into the intermittent heating problem with your radiators. When you have a moment, could you help us with a few things? 1. Which dates and times in the next couple of weeks would suit you for someone to attend? Please give a day and a rough time. 2. W …”
- Drafted message to tenant: **awaiting_staff** (simulated channel; not sent to a real person) — “Hi Tessa, Thanks for your patience while the engineer visited on 5 February. So we have an up-to-date picture, could you let us know how the heating has been behaving since then — are the radiators heating up reliably, or is it still cutting out at times? Thanks very much, Northbridge Lettings”
- Drafted message to tenant: **awaiting_staff** (simulated channel; not sent to a real person) — “Hi Tessa, Thanks for letting us know the radiators are cold again — sorry you're having to manage with a portable heater in this weather. So we have a clear picture of how you're getting on, could you tell us how the property is keeping at the moment with just the one heater, and whether anyone in t …”
- Drafted message to tenant: **awaiting_staff** (simulated channel; not sent to a real person) — “Hi Tessa, Thanks for sending over the boiler-label details and for letting us know the radiators are still inconsistent while the hot water is fine. So we have the full picture, could you let us know how the cold radiators are affecting the household at the moment \u2014 in particular, whether anyon …”
- Clarification `triage` to tenant: closed — Clarify before routing: Awaiting tenant's answers on leaks, smells and boiler warning codes; whether heating is currently off is still unknown.
- Clarification `triage` to tenant: closed — Clarify before routing: The boiler displayed a brief symbol the previous night that the tenant could not identify; the specific fault/warning code is still unknown, as is whether the heating is currently working.
- Clarification `access` to tenant: closed — Record consent for this visit and access method from the authorised person.
- Clarification `access` to tenant: closed — Record consent for this visit and access method from the authorised person.
- Clarification `schedule` to tenant: closed — Confirm the active appointment with a precise date and time.
- Clarification `evidence` to tenant: closed — Supply usable evidence required for this work item.
- Clarification `triage` to tenant: closed — Clarify before routing: Landlord authorisation for the £372 inc VAT remedial estimate has been requested but not yet given; work cannot be instructed until a decision is received.
- Clarification `triage` to tenant: open — Clarify before routing: Landlord asks whether the actuator can be repaired rather than replaced and whether £372 inc VAT covers all parts, labour and testing; contractor response needed before a decision.; Tenant reported cold radiators again and is …

### Escalated to a person (handover)

- No open human review.

### Missing information and conflicting facts

- **issue_details** (blocks the route): Whether invoice B (£372.00) supersedes or sits alongside invoice A (£138.00) for the same 5 February service date; overlapping attendance and diagnosis charges are unresolved.
- **completion** (blocks the route): No parts record, attendance evidence or confirmation that the actuator replacement was actually carried out or that the heating fault is resolved.
- **issue_details** (blocks the route): No written landlord authorisation on file for actuator replacement; authority covered diagnosis only.
- 13 extracted claim(s) remain **unverified source assertions** (see REASONING.md); none was treated as verified authority.

## Failures

- None recorded. (Jev and Claude calls all returned; no workflow step failed.)

## Result

No approval was invented and no human response was supplied by the runner. See the decision above for the recorded end state.

Trace: `REASONING.md` (why) · `AUDIT.md` (every step, actor and tool) · `evidence.json` / `records.jsonl` (raw records) · `checkpoint-NNN.json` (state after each source; kept in the local run directory, not published).
