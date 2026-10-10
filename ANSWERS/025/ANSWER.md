# Property Management — case 025: Kitchen tap maintenance request

> **Run assumption:** the `identity` and `route` check(s) were set aside by policy (`assumed_checks`): treated as satisfied unless a source contradicted them. Nothing was verified; every other gate (access, authority, schedule, completion, money, triage) still applied.

- **Property (as supplied, unverified):** 18 Thistlewick Row, Fenmere, ZZ1 1ZZ
- **Decision cutoff:** 2025-09-15T11:11:18+00:00
- **Runner status:** **settled** · execution `native_local` · sources processed 23 of 23
- **Models:** Claude `claude-opus-5` (triage effort medium); Jev `jev-1.13.0` routing
- **Commit:** `281c95a90dc8a3ddd9424b56d5decf0d9c521178` · input SHA-256 `7ec08748e429981a…`

All operational tools in this run are clearly labelled **simulated** adapters: no real tenant, landlord or contractor was contacted, nothing was paid or booked, and a simulated receipt does not prove work happened.

## What the system received

The initial report and 22 further sources, submitted one at a time in availability order; each was processed and settled before the next became visible. Full text: `input.json`.

| # | Available at | Source |
|---|---|---|
| 0 | 2025-08-04T18:10:50+00:00 | Initial report — Event 001 — Portal |
| 1 | 2025-08-05T07:33:17+00:00 | Event 002 — Email from Tessa Wren (Property Manager, Northbridge Lettings) |
| 2 | 2025-08-05T08:52:24+00:00 | Event 003 — Email from Orin Bell (Landlord) |
| 3 | 2025-08-05T09:30:38+00:00 | Event 004 — Email from Tessa Wren (Property Manager, Northbridge Lettings) |
| 4 | 2025-08-06T09:30:26+00:00 | Event 005 — Email from Tessa Wren (Property Manager, Northbridge Lettings) |
| 5 | 2025-08-07T09:54:37+00:00 | Event 006 — Email from Tessa Wren (Property Manager, Northbridge Lettings) |
| 6 | 2025-08-07T12:01:14+00:00 | Event 007 — Email from Nia Calder (Tenant) |
| 7 | 2025-08-07T13:05:43+00:00 | Event 008 — Email from Tessa Wren (Property Manager, Northbridge Lettings) |
| 8 | 2025-08-12T12:41:48+00:00 | Event 009 — Email from Tessa Wren (Property Manager, Northbridge Lettings) |
| 9 | 2025-08-12T18:55:02+00:00 | Event 010 — Email from Nia Calder (Tenant) |
| 10 | 2025-08-12T18:56:42+00:00 | Event 011 — Email from Tessa Wren (Property Manager, Northbridge Lettings) |
| 11 | 2025-09-05T19:40:02+00:00 | Event 012 — Email from Nia Calder (Tenant) |
| 12 | 2025-09-07T09:50:37+00:00 | Event 013 — Call from Tessa Wren (Property Manager, Northbridge Lettings) |
| 13 | 2025-09-09T08:02:07+00:00 | Event 014 — Email from Ivo Fenlock (Contractor, Bracken & Vale Plumbing) |
| 14 | 2025-09-09T16:39:08+00:00 | Event 015 — Email from Nia Calder (Tenant) |
| 15 | 2025-09-09T17:09:49+00:00 | Event 016 — Email from Tessa Wren (Property Manager, Northbridge Lettings) |
| 16 | 2025-09-10T06:06:05+00:00 | Event 017 — Email from Ivo Fenlock (Contractor, Bracken & Vale Plumbing) |
| 17 | 2025-09-10T10:51:20+00:00 | Event 018 — Email from Tessa Wren (Property Manager, Northbridge Lettings) |
| 18 | 2025-09-15T10:03:43+00:00 | Event 019 — Document from Ivo Fenlock (Contractor, Bracken & Vale Plumbing) |
| 19 | 2025-09-15T11:03:41+00:00 | Event 020 — Email from Tessa Wren (Property Manager, Northbridge Lettings) |
| 20 | 2025-09-15T11:05:47+00:00 | Event 021 — Call from Tessa Wren (Property Manager, Northbridge Lettings) |
| 21 | 2025-09-15T11:11:18+00:00 | Event 022 — Document from Ivo Fenlock (Contractor, Bracken & Vale Plumbing) |
| 22 | 2025-09-15T11:11:18+00:00 | Attachment corrected-plumbing-invoice.pdf (PDF text extraction) |

## Final decision — system case `62745fc84f4c`

- **Decision (policy outcome):** **NO FURTHER ACTION**
- **Proposed next action:** `clarify` — Separate boiler matter \u2013 scope unknown (category other)
- **Next step:** This action already has a confirmed simulated receipt. Select a new proposal for further work.
- **Owner:** case manager
- **Case state:** in_progress · policy v2
- **Split from system case** `03b80531e1ed` as a separate issue.

**Latest reading (model, medium confidence, route `clarify`):** Call note: contractor agrees to amend the invoice postcode and resend. A separate boiler matter was mentioned; the manager will check with the relevant engineer what work was done, and no boiler work is documented on this tap job.

### Actions taken

- `clarify` → **succeeded** via Demo contractor (simulated adapter) — Separate boiler matter \u2013 scope unknown

### Escalated to a person (handover)

- No open human review.

### Missing information and conflicting facts

- None recorded by the latest reading.

## Final decision — system case `8b6a524fc47a`

- **Decision (policy outcome):** **NO FURTHER ACTION**
- **Proposed next action:** `clarify` — Loose kitchen drawer with snapped brackets (category other)
- **Next step:** This action already has a confirmed simulated receipt. Select a new proposal for further work.
- **Owner:** case manager
- **Case state:** in_progress · policy v2
- **Split from system case** `03b80531e1ed` as a separate issue.

**Latest reading (model, high confidence, route `clarify`):** Property manager confirms a visit to the property on 10 September with the contractor, noting timing may vary as the contractor must collect keys from the office.

### Actions taken

- `clarify` → **succeeded** via Demo contractor (simulated adapter) — Loose kitchen drawer with snapped brackets

### Escalated to a person (handover)

- No open human review.

### Missing information and conflicting facts

- None recorded by the latest reading.

## Final decision — system case `71a954267a8e`

- **Decision (policy outcome):** **HUMAN REVIEW**
- **Proposed next action:** `request_quote` — Top kitchen drawer loose, front brackets snapped (category other)
- **Next step:** A case manager must define a supported action for this situation.
- **Owner:** case manager
- **Case state:** open · policy v2
- **Split from system case** `03b80531e1ed` as a separate issue.

**Latest reading (model, high confidence, route `request_quote`):** Tenant chases the outstanding plumbing appointment for the leaking tap, saying no contact has been made despite availability already given. She also reports a loose top kitchen drawer with apparently snapped metal front brackets and asks whether it can be repaired at the same visit.

### Actions taken

- **No operational action was executed.** Nothing was booked, instructed, paid or sent. The system recorded readings, claims and policy assessments only.

### Escalated to a person (handover)

| Check | Owner | Rule | What the person must resolve | Evidence |
|---|---|---|---|---|
| `supported` | case manager | `require-supported` | A case manager must define a supported action for this situation. | no source recorded |

### Missing information and conflicting facts

- None recorded by the latest reading.

## Final decision — system case `03b80531e1ed`

- **Decision (policy outcome):** **HUMAN REVIEW**
- **Proposed next action:** `clarify` — Reported maintenance (category plumbing)
- **Next step:** The tenant replied, but the reply did not settle this. Review it and record the fact. Clarify before routing: The corrected invoice shows no price or total including VAT; the full comparable commitment is not established.
- **Owner:** case manager
- **Case state:** open · policy v2

**Latest reading (claude-opus-5, medium confidence, route `clarify`):** Corrected invoice from Bracken & Vale Plumbing for supply and install of a new mono kitchen sink tap at 18 Thistlewick Row, with the postcode amended to the recorded property address. No total amount is shown in the extracted text.

**Why:** Corrected invoice resolves the postcode query but gives no total or completion evidence, so further clarification is needed before accepting.

### Actions taken

- Drafted message to tenant: **sent** (simulated channel; not sent to a real person) — “Hello Nia, Thanks for your patience regarding the dripping mixer tap and cloudy water. So that we can arrange for someone to come and take a look, could you let us know: 1. Which days and times suit you best over the next week or two? 2. Will you be home to let them in, or is there another way acces …”
- Drafted message to tenant: **sent** (simulated channel; not sent to a real person) — “Hello Nia, Thanks for letting us know you're home every day next week except Monday - that's really helpful. Just one more thing: when someone comes to look at the dripping mixer tap and cloudy water, are you happy to let them in yourself, or would you prefer access to be arranged another way (for e …”
- Drafted message to tenant: **awaiting_staff** (simulated channel; not sent to a real person) — “Hello Nia, Thanks for getting back to us, and sorry you've been waiting to hear about the leaking tap. We're following that up. On the top kitchen drawer that's loose with the metal front brackets looking snapped, could you tell us a little more about it - for example, whether the drawer still opens …”
- Drafted message to tenant: **awaiting_staff** (simulated channel; not sent to a real person) — “Hello Nia, Thanks again for your help with this. Just one quick thing to check: has a new kitchen mixer tap been fitted at your home recently? If so, it would be helpful to know roughly when the work was done. Just reply to this message and we'll take it from there. Best wishes, Northbridge Lettings”
- Drafted message to tenant: **awaiting_staff** (simulated channel; not sent to a real person) — “Hello Nia, Thanks again for your help with this. Just a couple of quick questions so we can keep our records straight: 1. Has the kitchen mixer tap been replaced at your home at 18 Thistlewick Row, and is it now working as it should? 2. Has anyone also looked at or carried out any work on your boile …”
- Clarification `access` to tenant: closed — Record consent for this visit and access method from the authorised person.
- Clarification `schedule` to tenant: closed — Confirm the active appointment with a precise date and time.
- Clarification `triage` to tenant: closed — Clarify before routing: Whether the drawer repair should be added to the plumbing visit or handled as a separate job with its own quote.
- Clarification `triage` to tenant: closed — Clarify before routing: The postcode on the invoice does not match the recorded property postcode; confirm the invoice relates to 18 Thistlewick Row before accepting it.

### Escalated to a person (handover)

| Check | Owner | Rule | What the person must resolve | Evidence |
|---|---|---|---|---|
| `triage` | case manager | `require-triage` | The tenant replied, but the reply did not settle this. Review it and record the fact. Clarify before routing: The corrected invoice shows no price or total including VAT; the full comparable commitment is not established … | Attachment corrected-plumbing-invoice.pdf (PDF text extraction) |

### Missing information and conflicting facts

- **issue_details** (blocks the route): The corrected invoice shows no price or total including VAT; the full comparable commitment is not established.
- **completion**: No evidence confirming the tap installation was completed and verified at the property.
- 7 extracted claim(s) remain **unverified source assertions** (see REASONING.md); none was treated as verified authority.

## Failures

- None recorded. (Jev and Claude calls all returned; no workflow step failed.)

## Result

No approval was invented and no human response was supplied by the runner. The case is waiting on the person(s) listed in the handover above.

Trace: `REASONING.md` (why) · `AUDIT.md` (every step, actor and tool) · `evidence.json` / `records.jsonl` (raw records) · `checkpoint-NNN.json` (state after each source; kept in the local run directory, not published).
