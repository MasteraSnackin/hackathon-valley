# Property Management — case 002: Gas record and boiler visit

> **Run assumption:** the `identity` and `route` check(s) were set aside by policy (`assumed_checks`): treated as satisfied unless a source contradicted them. Nothing was verified; every other gate (access, authority, schedule, completion, money, triage) still applied.

- **Property (as supplied, unverified):** 8 Brindlewick Row, Vellum Quay, ZZ1 1ZZ
- **Decision cutoff:** 2025-10-18T16:35:00+00:00
- **Runner status:** **settled** · execution `native_local` · sources processed 25 of 25
- **Models:** Claude `claude-opus-5` (triage effort medium); Jev `jev-1.13.0` routing
- **Commit:** `281c95a90dc8a3ddd9424b56d5decf0d9c521178` · input SHA-256 `ea1845adf408655e…`

All operational tools in this run are clearly labelled **simulated** adapters: no real tenant, landlord or contractor was contacted, nothing was paid or booked, and a simulated receipt does not prove work happened.

## What the system received

The initial report and 24 further sources, submitted one at a time in availability order; each was processed and settled before the next became visible. Full text: `input.json`.

| # | Available at | Source |
|---|---|---|
| 0 | 2025-10-01T08:42:00+00:00 | Initial report — Event 001 — Portal |
| 1 | 2025-10-01T09:18:00+00:00 | Event 002 — Note from Oren Vale (Property Manager, Northbridge Lettings) |
| 2 | 2025-10-01T11:06:00+00:00 | Event 003 — Portal from Iona Pell (Tenant) |
| 3 | 2025-10-02T10:14:00+00:00 | Event 004 — Email from Oren Vale (Property Manager, Northbridge Lettings) |
| 4 | 2025-10-03T08:51:00+00:00 | Event 005 — Email from Nessa Wold (Landlord) |
| 5 | 2025-10-03T13:22:00+00:00 | Event 006 — SMS from Riva Morn (Service Coordinator, Flintmere Gas Services) |
| 6 | 2025-10-04T09:07:00+00:00 | Event 007 — Portal from Iona Pell (Tenant) |
| 7 | 2025-10-09T08:48:00+00:00 | Event 008 — SMS from Tavin Rell (Gas Engineer, Flintmere Gas Services) |
| 8 | 2025-10-09T10:26:00+00:00 | Event 009 — Note from Tavin Rell (Gas Engineer, Flintmere Gas Services) |
| 9 | 2025-10-09T14:03:00+00:00 | Event 010 — Email from Riva Morn (Service Coordinator, Flintmere Gas Services) |
| 10 | 2025-10-10T09:32:00+00:00 | Event 011 — Document from Riva Morn (Service Coordinator, Flintmere Gas Services) |
| 11 | 2025-10-10T10:11:00+00:00 | Event 012 — Email from Nessa Wold (Landlord) |
| 12 | 2025-10-10T10:34:00+00:00 | Event 013 — Document from Oren Vale (Property Manager, Northbridge Lettings) |
| 13 | 2025-10-11T08:19:00+00:00 | Event 014 — Portal from Iona Pell (Tenant) |
| 14 | 2025-10-11T15:46:00+00:00 | Event 015 — Email from Riva Morn (Service Coordinator, Flintmere Gas Services) |
| 15 | 2025-10-12T10:02:00+00:00 | Event 016 — Email from Nessa Wold (Landlord) |
| 16 | 2025-10-13T07:56:00+00:00 | Event 017 — Portal from Iona Pell (Tenant) |
| 17 | 2025-10-13T11:25:00+00:00 | Event 018 — Email from Oren Vale (Property Manager, Northbridge Lettings) |
| 18 | 2025-10-14T09:41:00+00:00 | Event 019 — Email from Riva Morn (Service Coordinator, Flintmere Gas Services) |
| 19 | 2025-10-14T14:18:00+00:00 | Event 020 — Email from Oren Vale (Property Manager, Northbridge Lettings) |
| 20 | 2025-10-15T08:33:00+00:00 | Event 021 — Email from Tavin Rell (Gas Engineer, Flintmere Gas Services) |
| 21 | 2025-10-16T12:09:00+00:00 | Event 022 — Portal from Iona Pell (Tenant) |
| 22 | 2025-10-17T16:27:00+00:00 | Event 023 — Email from Nessa Wold (Landlord) |
| 23 | 2025-10-18T16:35:00+00:00 | Event 024 — Note from Oren Vale (Property Manager, Northbridge Lettings) |
| 24 | 2025-10-18T16:35:00+00:00 | Attachment gas-portal-record.pdf (PDF text extraction) |

## Final decision — system case `7a19790f7362`

- **Decision (policy outcome):** **HUMAN REVIEW**
- **Proposed next action:** `request_quote` — Recurring boiler lockout diagnostic (category appliance)
- **Next step:** Verify the received source assertion. Confirm that the category and work item match the source request.
- **Owner:** case manager
- **Case state:** open · policy v2
- **Split from system case** `23a92714cda6` as a separate issue.

**Latest reading (model, medium confidence, route `request_quote`):** Flintmere's coordinator states the job card covers the boiler and cooker, that the signed paperwork is paused by their quality desk while an appliance installation detail is reconciled against records held for the address, and that the engineer's entry remains satisfactory. They add that a lockout diagnostic would be a separate job.

### Actions taken

- **No operational action was executed.** Nothing was booked, instructed, paid or sent. The system recorded readings, claims and policy assessments only.

### Escalated to a person (handover)

| Check | Owner | Rule | What the person must resolve | Evidence |
|---|---|---|---|---|
| `classification` | case manager | `require-classification` | Verify the received source assertion. Confirm that the category and work item match the source request. | Split from case 23a92714cda6: Event 019 — Email from Riva Morn (Service Coordinator, Flintmere Gas Services) |

### Missing information and conflicting facts

- None recorded by the latest reading.
- 1 extracted claim(s) remain **unverified source assertions** (see REASONING.md); none was treated as verified authority.

## Final decision — system case `4df3e25b5325`

- **Decision (policy outcome):** **HUMAN REVIEW**
- **Proposed next action:** `close_item` — Annual gas safety visit on 9 October (category inspection)
- **Next step:** Verify the received source assertion. Verify completion of this work item with usable evidence.
- **Owner:** reviewer
- **Case state:** open · policy v2
- **Split from system case** `23a92714cda6` as a separate issue.

**Latest reading (model, medium confidence, route `close_item`):** Flintmere's gas engineer reports the 9 October annual gas visit is completed and recorded as satisfactory in the job app. He notes the tenant's intermittent boiler lockout was logged separately and no repair was carried out under this instruction.

### Actions taken

- Clarification `commitments` to staff: open — Resolve or explicitly cancel every outstanding commitment for this item.

### Escalated to a person (handover)

| Check | Owner | Rule | What the person must resolve | Evidence |
|---|---|---|---|---|
| `completion` | reviewer | `require-completion` | Verify the received source assertion. Verify completion of this work item with usable evidence. | Split from case 23a92714cda6: Event 009 — Note from Tavin Rell (Gas Engineer, Flintmere Gas Services) |

### Missing information and conflicting facts

- None recorded by the latest reading.
- 2 extracted claim(s) remain **unverified source assertions** (see REASONING.md); none was treated as verified authority.

## Final decision — system case `23a92714cda6`

- **Decision (policy outcome):** **WAIT**
- **Proposed next action:** `clarify` — Reported maintenance (category appliance)
- **Next step:** Clarify before routing: Portal shows job status Complete and Satisfactory, but the customer document is 'Processing' - unclear whether the check can be treated as complete without the signed record.; No date for issuing the signed paperwork and no explanation of the appliance installation query; no scope or cost for a lockout diagnostic.
- **Owner:** case manager
- **Case state:** open · policy v2

**Latest reading (claude-opus-5, medium confidence, route `clarify`):** Portal record export for job NBL-48217 shows a 9 October gas safety visit by Tavin Rell recorded as Complete/Satisfactory for boiler and cooker, but the customer document is still shown as 'Processing'. No date for the signed record, and no information on the lockout diagnostic.

**Why:** Document export confirms visit details but leaves the signed record, installation query and diagnostic scope unresolved, so clarification is still needed before routing.

### Actions taken

- Drafted message to tenant: **awaiting_staff** (simulated channel; not sent to a real person) — “Hello Iona, Thanks for getting in touch about the gas safety paperwork and the boiler. So we can look into the boiler side properly, could you tell us a bit more about the lockouts - how often the boiler locks out, when it started, whether any error code or light shows on the display, and whether yo …”
- Drafted message to tenant: **awaiting_staff** (simulated channel; not sent to a real person) — “Hello Iona, Thanks for letting us know the boiler has stopped twice during heating and restarted after a reset, and that you haven't noticed any gas smell. So we can arrange access for an engineer to attend for the gas safety check, could you let us know how you'd prefer access to be arranged - you …”
- Drafted message to tenant: **awaiting_staff** (simulated channel; not sent to a real person) — “Hello Iona, Thanks for providing access for the gas visit on 9 October. So we can look into the intermittent boiler lockout you mentioned, could you tell us a bit more about what's been happening? For example, how often the boiler locks out, when it last happened, and whether it affects your heating …”
- Drafted message to tenant: **sent** (simulated channel; not sent to a real person) — “Hello Iona, Thanks for providing access for the gas visit on 9 October. So we have an up-to-date picture, could you let us know whether the boiler has locked out again since that visit, and if so, roughly how often it has happened and what you see on the display when it does? Thanks very much, North …”
- Drafted message to tenant: **awaiting_staff** (simulated channel; not sent to a real person) — “Hello Iona, Thanks for letting us know the boiler locked out again overnight and that it's heating at the moment. So we have a clear picture to pass on, could you tell us how many times it has locked out since the visit on 9 October, and whether any code or message shows on the display when it happe …”
- Drafted message to tenant: **awaiting_staff** (simulated channel; not sent to a real person) — “Hello Iona, Thanks for letting us know the boiler locked out again overnight and restarted after you reset it. So we have a clear picture, could you tell us how many times it has locked out since the visit on 9 October, and whether anything shows on the display when it happens? It would also help to …”
- Drafted message to tenant: **awaiting_staff** (simulated channel; not sent to a real person) — “Hello Iona, Thanks again for your patience since the gas visit on 9 October. So we have a clear picture of what's happening with the boiler, could you let us know whether it has locked out again since that visit, and if so, what you see on the display and what you were doing at the time (for example …”
- Clarification `triage` to tenant: closed — Clarify before routing: Whether a new gas safety inspection has been booked or is needed, and whether the boiler lockout fault requires a separate engineer assessment.
- Clarification `access` to tenant: closed — Record consent for this visit and access method from the authorised person.
- Clarification `triage` to tenant: closed — Clarify before routing: No diagnosis or findings given for the intermittent boiler lockouts; unclear whether a further assessment or quote is needed and whether the landlord wants it instructed.
- Clarification `commitments` to staff: closed — Resolve or explicitly cancel every outstanding commitment for this item.
- Clarification `triage` to tenant: closed — Clarify before routing: No diagnosis or findings are given for the intermittent boiler lockouts; unclear whether a further assessment or quote is needed and whether the landlord wants it instructed.
- Clarification `triage` to tenant: closed — Clarify before routing: Awaiting contractor confirmation of what the portal entry covers, whether the gas appliance check is complete, and when paperwork will issue; also whether the recurring lockout needs a further visit.
- Clarification `triage` to tenant: open — Clarify before routing: No date given for when the signed paperwork will be issued, and no explanation of the appliance installation discrepancy being reconciled.; Contractor says a lockout diagnostic is a separate job but gives no cost, scope or whe …

### Escalated to a person (handover)

- No open human review.

### Missing information and conflicting facts

- **completion** (blocks the route): Portal shows job status Complete and Satisfactory, but the customer document is 'Processing' - unclear whether the check can be treated as complete without the signed record.
- **issue_details** (blocks the route): No date for issuing the signed paperwork and no explanation of the appliance installation query; no scope or cost for a lockout diagnostic.
- 7 extracted claim(s) remain **unverified source assertions** (see REASONING.md); none was treated as verified authority.

## Failures

- None recorded. (Jev and Claude calls all returned; no workflow step failed.)

## Result

No approval was invented and no human response was supplied by the runner. The case is waiting on the person(s) listed in the handover above.

Trace: `REASONING.md` (why) · `AUDIT.md` (every step, actor and tool) · `evidence.json` / `records.jsonl` (raw records) · `checkpoint-NNN.json` (state after each source; kept in the local run directory, not published).
