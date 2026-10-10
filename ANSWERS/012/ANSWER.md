# Property Management — case 012: Lock Maintenance Request

> **Run assumption:** the `identity` and `route` check(s) were set aside by policy (`assumed_checks`): treated as satisfied unless a source contradicted them. Nothing was verified; every other gate (access, authority, schedule, completion, money, triage) still applied.

- **Property (as supplied, unverified):** Unit 2, 18 Brindlewick Mews, Orellin ZZ1 1ZZ
- **Decision cutoff:** 2025-09-25T12:06:33+00:00
- **Runner status:** **settled** · execution `native_local` · sources processed 25 of 25
- **Models:** Claude `claude-opus-5` (triage effort medium); Jev `jev-1.13.0` routing
- **Commit:** `281c95a90dc8a3ddd9424b56d5decf0d9c521178` · input SHA-256 `9f2327bea788a66b…`

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

## Final decision — system case `e6659b8ac7c2`

- **Decision (policy outcome):** **HUMAN REVIEW**
- **Proposed next action:** `request_quote` — Mould appearing in bathroom (category other)
- **Next step:** A case manager must define a supported action for this situation.
- **Owner:** case manager
- **Case state:** open · policy v2
- **Split from system case** `74913d80417d` as a separate issue.

**Latest reading (model, medium confidence, route `request_quote`):** The property manager records a call with the tenant clarifying that the lock problems are on the opening window sashes (bedroom sash will not lock, bathroom sash stuck with sticking locking buttons, kitchen sash has no key). The tenant grants access for tradespeople but no key handover or appointment time is set, and mould in the bathroom is newly mentioned.

### Actions taken

- **No operational action was executed.** Nothing was booked, instructed, paid or sent. The system recorded readings, claims and policy assessments only.

### Escalated to a person (handover)

| Check | Owner | Rule | What the person must resolve | Evidence |
|---|---|---|---|---|
| `supported` | case manager | `require-supported` | A case manager must define a supported action for this situation. | no source recorded |

### Missing information and conflicting facts

- None recorded by the latest reading.

## Final decision — system case `a20e67bf627d`

- **Decision (policy outcome):** **NO FURTHER ACTION**
- **Proposed next action:** `clarify` — Missing keys (category doors_locks)
- **Next step:** This action already has a confirmed simulated receipt. Select a new proposal for further work.
- **Owner:** case manager
- **Case state:** in_progress · policy v2
- **Split from system case** `74913d80417d` as a separate issue.

**Latest reading (model, medium confidence, route `clarify`):** Tenant reports the bathroom window will not open and the bedroom window opens but cannot be secured, and also says keys are missing. No access, appointment or cost details provided.

### Actions taken

- `clarify` → **succeeded** via Demo contractor (simulated adapter) — Missing keys

### Escalated to a person (handover)

- No open human review.

### Missing information and conflicting facts

- None recorded by the latest reading.
- 1 extracted claim(s) remain **unverified source assertions** (see REASONING.md); none was treated as verified authority.

## Final decision — system case `25bc7c82b79e`

- **Decision (policy outcome):** **HUMAN REVIEW**
- **Proposed next action:** `request_quote` — Bedroom window will not secure when closed (category windows)
- **Next step:** Verify the received source assertion. Confirm that the category and work item match the source request.
- **Owner:** case manager
- **Case state:** open · policy v2
- **Split from system case** `74913d80417d` as a separate issue.

**Latest reading (model, medium confidence, route `request_quote`):** Tenant reports the bathroom window will not open and the bedroom window opens but cannot be secured, and also says keys are missing. No access, appointment or cost details provided.

### Actions taken

- **No operational action was executed.** Nothing was booked, instructed, paid or sent. The system recorded readings, claims and policy assessments only.

### Escalated to a person (handover)

| Check | Owner | Rule | What the person must resolve | Evidence |
|---|---|---|---|---|
| `classification` | case manager | `require-classification` | Verify the received source assertion. Confirm that the category and work item match the source request. | Split from case 74913d80417d: Intake report |

### Missing information and conflicting facts

- None recorded by the latest reading.
- 1 extracted claim(s) remain **unverified source assertions** (see REASONING.md); none was treated as verified authority.

## Final decision — system case `74913d80417d`

- **Decision (policy outcome):** **WAIT**
- **Proposed next action:** `clarify` — Bathroom window will not open (category windows)
- **Next step:** Clarify before routing: Completion is asserted again with no invoice, appointment, visit notes or attendance evidence; confirm with the tenant whether access occurred and the window now opens.
- **Owner:** case manager
- **Case state:** open · policy v2

**Latest reading (claude-opus-5, high confidence, route `clarify`):** Contractor again states the bathroom window work is complete and promises an invoice later today. No invoice, appointment, visit notes or attendance evidence is on file.

**Why:** Repeated unevidenced completion claim conflicting with failed access history; needs clarification before closing.

### Actions taken

- Drafted message to tenant: **sent** (simulated channel; not sent to a real person) — “Hello Perrin, Thanks for letting us know about the bathroom window that will not open and the bedroom window that opens but will not secure. So we can get this moving, could you tell us a bit more about the missing keys? In particular, which keys they are (for example property, window or communal do …”
- Drafted message to tenant: **sent** (simulated channel; not sent to a real person) — “Hello Perrin, Thanks again for your report. Just so we have the details right, could you confirm what happens when you try to open the bathroom window - for example, whether the handle moves but the window stays shut, or whether the handle or lock itself is stuck? Many thanks, Northbridge Lettings”
- Drafted message to tenant: **sent** (simulated channel; not sent to a real person) — “Hello Perrin, Thanks for bearing with us on this. Just one more thing so we have the details right: when you mentioned the locks, are these the locks on the opening windows themselves (the bathroom and bedroom windows), or locks on internal room doors? Many thanks, Northbridge Lettings”
- Drafted message to tenant: **awaiting_staff** (simulated channel; not sent to a real person) — “Hello Perrin, Thanks for your patience while we sort out the bathroom window that will not open and the bedroom window that opens but will not secure. So we can arrange for someone to come and take a look, could you let us know: 1. Which days and times suit you best over the next couple of weeks? 2. …”
- Drafted message to tenant: **awaiting_staff** (simulated channel; not sent to a real person) — “Hello Perrin, Thanks for getting back to us about the windows. So we can firm things up, could you let us know which days and rough times over the next couple of weeks would suit best for someone to attend? Even though you're happy for access at any time, it helps to have a preferred date and time s …”
- Drafted message to tenant: **awaiting_staff** (simulated channel; not sent to a real person) — “Hello Perrin, Thanks for coming back to us about the bathroom window that will not open. So we can get everything lined up, could you help with three things? 1. If you are at work, are you happy for someone to enter the property without you there, and is there anyone else aged 18 or over who would b …”
- Drafted message to tenant: **sent** (simulated channel; not sent to a real person) — “Hello Perrin, Thanks for your message about access while you're at work. So we can sort out the arrangements, could you let us know who currently holds a set of keys for the flat, and whether you'd be happy for keys to be used for entry while you're out and then returned to you afterwards? Many than …”
- Drafted message to tenant: **awaiting_staff** (simulated channel; not sent to a real person) — “Hello Perrin, Thanks for your patience with this one. Could you let us know whether anyone has been into the flat recently to look at the bathroom window, and whether the window now opens as it should? Many thanks, Northbridge Lettings”
- Clarification `triage` to tenant: closed — Clarify before routing: Unclear which keys are missing (property, window or communal), whether they are lost or never supplied, and whether replacement or a lock change is needed.
- Clarification `classification` to tenant: closed — Confirm that the category and work item match the source request.
- Clarification `triage` to tenant: closed — Clarify before routing: Whether the reported lock problems relate to window sashes or internal room doors is still unresolved; scope of authorised work remains unclear.
- Clarification `access` to tenant: closed — Record consent for this visit and access method from the authorised person.
- Clarification `schedule` to tenant: closed — Confirm the active appointment with a precise date and time.
- Clarification `triage` to tenant: closed — Clarify before routing: Still unclear whether the lock problems are on the window sashes or on internal room doors, which affects the work item and scope of authorised work.
- Clarification `access` to tenant: closed — Record consent for this visit and access method from the authorised person.
- Clarification `keys` to tenant: closed — Establish key custody and return arrangements.
- Clarification `schedule` to tenant: closed — Confirm the active appointment with a precise date and time.
- Clarification `triage` to tenant: open — Clarify before routing: Contractor asserts the work was completed on 19 September but provides no visit details, work description or completion evidence; this conflicts with earlier reports of three failed access attempts and no management keys colle …

### Escalated to a person (handover)

- No open human review.

### Missing information and conflicting facts

- **completion** (blocks the route): Completion is asserted again with no invoice, appointment, visit notes or attendance evidence; confirm with the tenant whether access occurred and the window now opens.
- 7 extracted claim(s) remain **unverified source assertions** (see REASONING.md); none was treated as verified authority.

## Failures

- None recorded. (Jev and Claude calls all returned; no workflow step failed.)

## Result

No approval was invented and no human response was supplied by the runner. The case is waiting on the person(s) listed in the handover above.

Trace: `REASONING.md` (why) · `AUDIT.md` (every step, actor and tool) · `evidence.json` / `records.jsonl` (raw records) · `checkpoint-NNN.json` (state after each source; kept in the local run directory, not published).
