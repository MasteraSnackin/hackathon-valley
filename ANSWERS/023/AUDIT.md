# Case fea0d65b5f72 audit trail

Heating maintenance at 7 Larkspur Fold · 7 Larkspur Fold, Orvane Heath, ZZ1 1ZZ · status open · stage HUMAN REVIEW

- **Case ID:** `fea0d65b5f7244b9a7a7a89dbd627f2b`
- **Entries:** 208 (from 583 immutable records; bookkeeping and unchanged assessments omitted)
- **Raw records:** [records.jsonl](records.jsonl)
- All outbound tools are simulated adapters; no real tenant, landlord or contractor was contacted.

<a id="entry-001"></a>
## 2026-10-10 16:04:10 UTC — 001 · Message received: Intake report

- **Recorded by:** demo-case_manager (case manager)
- **Reading:** queued for Jev routing / Claude triage

> Event 001 — Portal
> From: Tessa Vane (Tenant)
> To: Ivo Merrick (Property Manager, Northbridge Lettings)
>
> Reported that radiator heating had cut out twice since the previous evening while hot water remained available. A child lives at the property. Asked for an inspection.

<a id="entry-002"></a>
## 2026-10-10 16:04:10 UTC — 002 · Human review opened: `identity`

- **Actor:** Policy engine
- **Owner:** case manager · rule `require-identity`
- **Expires:** 2026-10-12 16:04:10 UTC

> Verify the person, property and work item mapping.

<a id="entry-003"></a>
## 2026-10-10 16:04:10 UTC — 003 · Human review opened: `route`

- **Actor:** Policy engine
- **Owner:** case manager · rule `require-route`
- **Expires:** 2026-10-12 16:04:10 UTC

> Verify the recipient and permitted communication route.

<a id="entry-004"></a>
## 2026-10-10 16:04:10 UTC — 004 · Policy gates → HUMAN REVIEW

- **Actor:** Policy engine (rules v1, `domain.evaluate`)
- **Outcome:** HUMAN REVIEW · owner case manager
- **Blockers:** `identity` UNKNOWN → HUMAN REVIEW; `route` UNKNOWN → HUMAN REVIEW; `triage` UNKNOWN → WAIT
- **Next step:** Verify the person, property and work item mapping.

<a id="entry-005"></a>
## 2026-10-10 16:04:10 UTC — 005 · Workflow receipt

<a id="entry-006"></a>
## 2026-10-10 16:04:10 UTC — 006 · Jev routed the message

- **Actor:** Jev (jev-1.13.0 · 1296 in / 284 out tokens · 369 ms)
- **Tool:** TypeSafe `system_one` · step `route_case_messages`
- **Decision:** jev_route → `urgent_hazard` (confidence 0.54)
- **Signals:** hazard 0.58 · multiple_issues 0.11 · sensitive 0.97 · states_facts 0.03 · system_instructions 0.01
- **Why:** Possible hazard (Jev p=0.58); a person takes over before any automated contact.

<a id="entry-007"></a>
## 2026-10-10 16:04:16 UTC — 007 · Claude read the message

- **Actor:** Claude (claude-opus-5 · 387 in / 389 out tokens)
- **Tool:** Anthropic Messages API `ai.triage` (prompt property-triage-2026-10-10.3) · step `triage_case_messages`
- **Reading:** new request · route `urgent_hazard` · medium confidence
- **Work item:** Radiator heating cutting out intermittently (other)
- **Summary:** Tenant reports the radiator heating has cut out twice since the previous evening, with hot water still working. A child lives at the property and an inspection is requested.
- **Rationale:** Intermittent loss of heating with a child in the property; router flagged possible hazard for human handling.
- **Extracted:** 1 claim · 2 ambiguities · 1 issue · risk flags: vulnerable_person, safety
- **Unknown (affects route):** Is the heating currently off entirely, and is the boiler showing any fault code or pressure loss?
- **Unknown:** No availability or access arrangements given for an inspection visit.

<a id="entry-008"></a>
## 2026-10-10 16:04:16 UTC — 008 · Proposed action → `clarify`

- **Actor:** Triage reading (route `urgent_hazard`)
- **Work item:** Radiator heating cutting out intermittently
- **Action revision:** 2

<a id="entry-009"></a>
## 2026-10-10 16:04:16 UTC — 009 · Claim `urgent` = true

- **Actor:** Claude (extracted)
- **Status:** unverified assertion — a person or policy must accept it

> radiator heating had cut out twice since the previous evening

<a id="entry-010"></a>
## 2026-10-10 16:04:16 UTC — 010 · Human review opened: `identity`

- **Actor:** Policy engine
- **Owner:** case manager · rule `require-identity`
- **Expires:** 2026-10-12 16:04:16 UTC

> Verify the person, property and work item mapping.

<a id="entry-011"></a>
## 2026-10-10 16:04:16 UTC — 011 · Human review opened: `route`

- **Actor:** Policy engine
- **Owner:** case manager · rule `require-route`
- **Expires:** 2026-10-12 16:04:16 UTC

> Verify the recipient and permitted communication route.

<a id="entry-012"></a>
## 2026-10-10 16:04:16 UTC — 012 · Human review opened: `triage`

- **Actor:** Policy engine
- **Owner:** case manager · rule `require-triage`
- **Expires:** 2026-10-12 16:04:16 UTC

> Claude read this as a possible urgent hazard. A case manager must take over now and apply the urgent procedure.

<a id="entry-013"></a>
## 2026-10-10 16:04:16 UTC — 013 · Policy gates → HUMAN REVIEW

- **Actor:** Policy engine (rules v1, `domain.evaluate`)
- **Outcome:** HUMAN REVIEW · owner case manager
- **Blockers:** `identity` UNKNOWN → HUMAN REVIEW; `route` UNKNOWN → HUMAN REVIEW; `triage` UNKNOWN → HUMAN REVIEW
- **Next step:** Verify the person, property and work item mapping.

<a id="entry-014"></a>
## 2026-10-10 16:04:16 UTC — 014 · Message received: Event 002 — Update from Ivo Merrick (Property Manager, Northbridge Lettings)

- **Recorded by:** demo-case_manager (case manager)
- **Reading:** queued for Jev routing / Claude triage

> Event 002 — Update
> From: Ivo Merrick (Property Manager, Northbridge Lettings)
> To: Tessa Vane (Tenant)
>
> Acknowledged the report and asked about leaks, unusual smells, boiler warnings and access times. No entry arrangement was yet confirmed.

<a id="entry-015"></a>
## 2026-10-10 16:04:16 UTC — 015 · Policy gates → HUMAN REVIEW

- **Actor:** Policy engine (rules v1, `domain.evaluate`)
- **Outcome:** HUMAN REVIEW · owner case manager
- **Blockers:** `identity` UNKNOWN → HUMAN REVIEW; `route` UNKNOWN → HUMAN REVIEW; `triage` UNKNOWN → WAIT
- **Next step:** Verify the person, property and work item mapping.

<a id="entry-016"></a>
## 2026-10-10 16:04:16 UTC — 016 · Workflow receipt

<a id="entry-017"></a>
## 2026-10-10 16:04:16 UTC — 017 · Jev routed the message

- **Actor:** Jev (jev-1.13.0 · 1442 in / 282 out tokens · 359 ms)
- **Tool:** TypeSafe `system_one` · step `route_case_messages`
- **Decision:** jev_route → `clarify` (confidence 0.57)
- **Signals:** hazard 0.22 · multiple_issues 0.08 · sensitive 0.62 · states_facts 0.04 · system_instructions 0.01
- **Why:** Jev routes; Claude extracts quotes and claims. clarify is not a Jev-only route. Route confidence 0.57 is below the Jev-only bar 0.8. Possible distress, complaint or vulnerability.

<a id="entry-018"></a>
## 2026-10-10 16:04:21 UTC — 018 · Claude read the message

- **Actor:** Claude (claude-opus-5 · 682 in / 346 out tokens)
- **Tool:** Anthropic Messages API `ai.triage` (prompt property-triage-2026-10-10.3) · step `triage_case_messages`
- **Reading:** update · route `clarify` · high confidence
- **Work item:** Radiator heating cutting out intermittently (other)
- **Summary:** Property manager acknowledged the tenant's intermittent heating report and asked about leaks, smells, boiler warnings and access times. No access arrangement confirmed yet.
- **Rationale:** Manager is still gathering essential details; nothing yet to instruct or quote, so clarify stands.
- **Extracted:** 0 claims · 2 ambiguities · 1 issue · risk flags: vulnerable_person
- **Unknown (affects route):** Awaiting tenant's answers on leaks, smells and boiler warnings; is heating off entirely or intermittent?
- **Unknown:** No entry arrangement confirmed; access times still needed.

<a id="entry-019"></a>
## 2026-10-10 16:04:21 UTC — 019 · Policy gates → HUMAN REVIEW

- **Actor:** Policy engine (rules v1, `domain.evaluate`)
- **Outcome:** HUMAN REVIEW · owner case manager
- **Blockers:** `identity` UNKNOWN → HUMAN REVIEW; `route` UNKNOWN → HUMAN REVIEW; `triage` UNKNOWN → HUMAN REVIEW
- **Next step:** Verify the person, property and work item mapping.

<a id="entry-020"></a>
## 2026-10-10 16:04:21 UTC — 020 · Message received: Event 003 — Portal from Tessa Vane (Tenant)

- **Recorded by:** demo-case_manager (case manager)
- **Reading:** queued for Jev routing / Claude triage

> Event 003 — Portal
> From: Tessa Vane (Tenant)
> To: Ivo Merrick (Property Manager, Northbridge Lettings)
>
> Confirmed no visible leak, unusual smell or current warning light. The boiler had shown a brief symbol the previous night, but she did not identify it. She can provide access after 14:00 on weekdays.

<a id="entry-021"></a>
## 2026-10-10 16:04:21 UTC — 021 · Policy gates → HUMAN REVIEW

- **Actor:** Policy engine (rules v1, `domain.evaluate`)
- **Outcome:** HUMAN REVIEW · owner case manager
- **Blockers:** `identity` UNKNOWN → HUMAN REVIEW; `route` UNKNOWN → HUMAN REVIEW; `triage` UNKNOWN → WAIT
- **Next step:** Verify the person, property and work item mapping.

<a id="entry-022"></a>
## 2026-10-10 16:04:21 UTC — 022 · Workflow receipt

<a id="entry-023"></a>
## 2026-10-10 16:04:22 UTC — 023 · Jev routed the message

- **Actor:** Jev (jev-1.13.0 · 1553 in / 286 out tokens · 421 ms)
- **Tool:** TypeSafe `system_one` · step `route_case_messages`
- **Decision:** jev_route → `confirm_appointment` (confidence 0.72)
- **Signals:** hazard 0.13 · multiple_issues 0.10 · sensitive 0.61 · states_facts 0.84 · system_instructions 0.02
- **Why:** Jev routes; Claude extracts quotes and claims. confirm_appointment is not a Jev-only route. Route confidence 0.72 is below the Jev-only bar 0.8. The message may state facts that need exact quotes. Possible distress, complaint or vulnerability. A route change on an existing case.

<a id="entry-024"></a>
## 2026-10-10 16:04:32 UTC — 024 · Claude read the message

- **Actor:** Claude (claude-opus-5 · 932 in / 690 out tokens)
- **Tool:** Anthropic Messages API `ai.triage` (prompt property-triage-2026-10-10.3) · step `triage_case_messages`
- **Reading:** answer to question · route `request_quote` · medium confidence
- **Work item:** Radiator heating cutting out intermittently (other)
- **Summary:** Tenant replies that there is no visible leak, smell or current warning light, though the boiler briefly showed an unidentified symbol the previous night. She gives general availability after 14:00 on weekdays; no appointment has been agreed.
- **Rationale:** Tenant has answered the diagnostic questions; intermittent heating fault still needs an engineer assessment, and no firm appointment exists yet.
- **Extracted:** 0 claims · 3 ambiguities · 1 issue
- **Unknown:** Tenant offers after 14:00 on weekdays but no specific date and time is agreed; confirm an appointment slot.
- **Unknown:** The boiler displayed a brief unidentified symbol; ask tenant to note or photograph any code if it recurs.
- **Unknown:** Confirm who will admit the engineer and the entry method.
- **Objected to Jev's route:** confirm_appointment assumes an appointment to arrange or confirm, but the message only gives general weekday availability after 14:00 and no visit has been booked; the job still needs a contractor inspection/quote to be instructed.

<a id="entry-025"></a>
## 2026-10-10 16:04:32 UTC — 025 · Proposed action → `request_quote`

- **Actor:** Triage reading (route `request_quote`)
- **Work item:** Radiator heating cutting out intermittently
- **Action revision:** 3

<a id="entry-026"></a>
## 2026-10-10 16:04:32 UTC — 026 · Human review opened: `identity`

- **Actor:** Policy engine
- **Owner:** case manager · rule `require-identity`
- **Expires:** 2026-10-12 16:04:32 UTC

> Verify the person, property and work item mapping.

<a id="entry-027"></a>
## 2026-10-10 16:04:32 UTC — 027 · Human review opened: `route`

- **Actor:** Policy engine
- **Owner:** case manager · rule `require-route`
- **Expires:** 2026-10-12 16:04:32 UTC

> Verify the recipient and permitted communication route.

<a id="entry-028"></a>
## 2026-10-10 16:04:32 UTC — 028 · Human review opened: `classification`

- **Actor:** Policy engine
- **Owner:** case manager · rule `require-classification`
- **Expires:** 2026-10-12 16:04:32 UTC

> Confirm that the category and work item match the source request. A verified route is required before asking externally.

<a id="entry-029"></a>
## 2026-10-10 16:04:32 UTC — 029 · Human review opened: `supported`

- **Actor:** Policy engine
- **Owner:** case manager · rule `require-supported`
- **Expires:** 2026-10-12 16:04:32 UTC

> A case manager must define a supported action for this situation.

<a id="entry-030"></a>
## 2026-10-10 16:04:32 UTC — 030 · Human review opened: `triage`

- **Actor:** Policy engine
- **Owner:** case manager · rule `require-triage`
- **Expires:** 2026-10-12 16:04:32 UTC

> Jev routed this message to confirm_appointment, but Claude reads it as request_quote: confirm_appointment assumes an appointment to arrange or confirm, but the message only gives general weekday availability after 14:00 and no visit has been booked; the job still needs a contractor inspection/quote to be instructed. The case follows Claude's route (a hazard is never de-escalated). Confirm or correct the route.

<a id="entry-031"></a>
## 2026-10-10 16:04:32 UTC — 031 · Policy gates → HUMAN REVIEW

- **Actor:** Policy engine (rules v1, `domain.evaluate`)
- **Outcome:** HUMAN REVIEW · owner case manager
- **Blockers:** `identity` UNKNOWN → HUMAN REVIEW; `route` UNKNOWN → HUMAN REVIEW; `classification` UNKNOWN → HUMAN REVIEW; `supported` UNKNOWN → HUMAN REVIEW; `triage` CONFLICT → HUMAN REVIEW
- **Next step:** Verify the person, property and work item mapping.

<a id="entry-032"></a>
## 2026-10-10 16:04:32 UTC — 032 · Message received: Event 004 — Email from Ivo Merrick (Property Manager, Northbridge Lettings)

- **Recorded by:** demo-case_manager (case manager)
- **Reading:** queued for Jev routing / Claude triage

> Event 004 — Email
> From: Ivo Merrick (Property Manager, Northbridge Lettings)
> To: Soren Dallow (Landlord)
>
> Requested approval for a diagnostic visit. Noted that the agency's routine repair limit is £180 including VAT and that work above that limit needs landlord approval.

<a id="entry-033"></a>
## 2026-10-10 16:04:32 UTC — 033 · Policy gates → HUMAN REVIEW

- **Actor:** Policy engine (rules v1, `domain.evaluate`)
- **Outcome:** HUMAN REVIEW · owner case manager
- **Blockers:** `identity` UNKNOWN → HUMAN REVIEW; `route` UNKNOWN → HUMAN REVIEW; `classification` UNKNOWN → HUMAN REVIEW; `supported` UNKNOWN → HUMAN REVIEW; `triage` UNKNOWN → WAIT
- **Next step:** Verify the person, property and work item mapping.

<a id="entry-034"></a>
## 2026-10-10 16:04:32 UTC — 034 · Workflow receipt

<a id="entry-035"></a>
## 2026-10-10 16:04:32 UTC — 035 · Jev routed the message

- **Actor:** Jev (jev-1.13.0 · 1665 in / 282 out tokens · 363 ms)
- **Tool:** TypeSafe `system_one` · step `route_case_messages`
- **Decision:** jev_route → `request_quote` (confidence 0.89)
- **Signals:** hazard 0.19 · multiple_issues 0.03 · sensitive 0.65 · states_facts 0.70 · system_instructions 0.02
- **Why:** Jev routes; Claude extracts quotes and claims. The message may state facts that need exact quotes. Possible distress, complaint or vulnerability.

<a id="entry-036"></a>
## 2026-10-10 16:04:37 UTC — 036 · Claude read the message

- **Actor:** Claude (claude-opus-5 · 1040 in / 374 out tokens)
- **Tool:** Anthropic Messages API `ai.triage` (prompt property-triage-2026-10-10.3) · step `triage_case_messages`
- **Reading:** update · route `request_quote` · high confidence
- **Work item:** Radiator heating cutting out intermittently (other)
- **Summary:** Property manager emailed the landlord requesting approval for a diagnostic visit on the intermittent radiator heating fault, noting the agency's routine repair limit of £180 including VAT above which landlord approval is needed.
- **Rationale:** Agency is seeking landlord approval for a diagnostic visit; no quote or authority yet, so the job remains at the quote/assessment stage.
- **Extracted:** 0 claims · 2 ambiguities · 1 issue
- **Unknown:** No diagnostic visit cost or contractor has been stated; the £180 figure is a general agency limit, not a quote for this job.
- **Unknown:** Tenant offered weekday access after 14:00 but no appointment has been arranged or confirmed with a contractor.

<a id="entry-037"></a>
## 2026-10-10 16:04:37 UTC — 037 · Review superseded

- **Why:** Relevant evidence or current blockers changed; assess the current review.

<a id="entry-038"></a>
## 2026-10-10 16:04:37 UTC — 038 · Policy gates → HUMAN REVIEW

- **Actor:** Policy engine (rules v1, `domain.evaluate`)
- **Outcome:** HUMAN REVIEW · owner case manager
- **Blockers:** `identity` UNKNOWN → HUMAN REVIEW; `route` UNKNOWN → HUMAN REVIEW; `classification` UNKNOWN → HUMAN REVIEW; `supported` UNKNOWN → HUMAN REVIEW
- **Next step:** Verify the person, property and work item mapping.

<a id="entry-039"></a>
## 2026-10-10 16:04:38 UTC — 039 · Message received: Event 005 — Email from Soren Dallow (Landlord)

- **Recorded by:** demo-case_manager (case manager)
- **Reading:** queued for Jev routing / Claude triage

> Event 005 — Email
> From: Soren Dallow (Landlord)
> To: Ivo Merrick (Property Manager, Northbridge Lettings)
>
> Authorized diagnosis up to £180 including VAT only. Asked to be consulted before any remedial work or additional expenditure is authorized.

<a id="entry-040"></a>
## 2026-10-10 16:04:38 UTC — 040 · Policy gates → HUMAN REVIEW

- **Actor:** Policy engine (rules v1, `domain.evaluate`)
- **Outcome:** HUMAN REVIEW · owner case manager
- **Blockers:** `identity` UNKNOWN → HUMAN REVIEW; `route` UNKNOWN → HUMAN REVIEW; `classification` UNKNOWN → HUMAN REVIEW; `supported` UNKNOWN → HUMAN REVIEW; `triage` UNKNOWN → WAIT
- **Next step:** Verify the person, property and work item mapping.

<a id="entry-041"></a>
## 2026-10-10 16:04:38 UTC — 041 · Workflow receipt

<a id="entry-042"></a>
## 2026-10-10 16:04:38 UTC — 042 · Jev routed the message

- **Actor:** Jev (jev-1.13.0 · 1679 in / 282 out tokens · 408 ms)
- **Tool:** TypeSafe `system_one` · step `route_case_messages`
- **Decision:** jev_route → `request_quote` (confidence 0.86)
- **Signals:** hazard 0.05 · multiple_issues 0.03 · sensitive 0.03 · states_facts 0.87 · system_instructions 0.02
- **Why:** Jev routes; Claude extracts quotes and claims. The message may state facts that need exact quotes.

<a id="entry-043"></a>
## 2026-10-10 16:04:44 UTC — 043 · Claude read the message

- **Actor:** Claude (claude-opus-5 · 1218 in / 432 out tokens)
- **Tool:** Anthropic Messages API `ai.triage` (prompt property-triage-2026-10-10.3) · step `triage_case_messages`
- **Reading:** update · route `request_quote` · high confidence
- **Work item:** Radiator heating cutting out intermittently (other)
- **Summary:** Landlord Soren Dallow authorises a diagnostic visit up to £180 including VAT and asks to be consulted before any remedial work or further spend.
- **Rationale:** Landlord approval for a capped diagnostic visit; the job still needs a contractor quote/assessment, matching the router's request_quote.
- **Extracted:** 2 claims · 2 ambiguities · 1 issue
- **Unknown:** No appointment date/time agreed; tenant availability is after 14:00 weekdays only.
- **Unknown:** No entry arrangement confirmed for the diagnostic visit.

<a id="entry-044"></a>
## 2026-10-10 16:04:44 UTC — 044 · Claim `total` = 180.0

- **Actor:** Claude (extracted)
- **Status:** unverified assertion — a person or policy must accept it

> Authorized diagnosis up to £180 including VAT only.

<a id="entry-045"></a>
## 2026-10-10 16:04:44 UTC — 045 · Policy gates → HUMAN REVIEW

- **Actor:** Policy engine (rules v1, `domain.evaluate`)
- **Outcome:** HUMAN REVIEW · owner case manager
- **Blockers:** `identity` UNKNOWN → HUMAN REVIEW; `route` UNKNOWN → HUMAN REVIEW; `classification` UNKNOWN → HUMAN REVIEW; `supported` UNKNOWN → HUMAN REVIEW
- **Next step:** Verify the person, property and work item mapping.

<a id="entry-046"></a>
## 2026-10-10 16:04:44 UTC — 046 · Message received: Event 006 — Email from Ivo Merrick (Property Manager, Northbridge Lettings)

- **Recorded by:** demo-case_manager (case manager)
- **Reading:** queued for Jev routing / Claude triage

> Event 006 — Email
> From: Ivo Merrick (Property Manager, Northbridge Lettings)
> To: Petra Quill (Contractor, Copper Finch Mechanical)
>
> Requested diagnosis of intermittent radiator heating, a written report and an itemized estimate before work beyond diagnosis. Confirmed access after 14:00 and the diagnostic-only authorization ceiling of £180 including VAT.

<a id="entry-047"></a>
## 2026-10-10 16:04:44 UTC — 047 · Policy gates → HUMAN REVIEW

- **Actor:** Policy engine (rules v1, `domain.evaluate`)
- **Outcome:** HUMAN REVIEW · owner case manager
- **Blockers:** `identity` UNKNOWN → HUMAN REVIEW; `route` UNKNOWN → HUMAN REVIEW; `classification` UNKNOWN → HUMAN REVIEW; `supported` UNKNOWN → HUMAN REVIEW; `triage` UNKNOWN → WAIT
- **Next step:** Verify the person, property and work item mapping.

<a id="entry-048"></a>
## 2026-10-10 16:04:44 UTC — 048 · Workflow receipt

<a id="entry-049"></a>
## 2026-10-10 16:04:45 UTC — 049 · Jev routed the message

- **Actor:** Jev (jev-1.13.0 · 1702 in / 282 out tokens · 275 ms)
- **Tool:** TypeSafe `system_one` · step `route_case_messages`
- **Decision:** jev_route → `request_quote` (confidence 0.84)
- **Signals:** hazard 0.05 · multiple_issues 0.03 · sensitive 0.03 · states_facts 0.96 · system_instructions 0.02
- **Why:** Jev routes; Claude extracts quotes and claims. The message may state facts that need exact quotes.

<a id="entry-050"></a>
## 2026-10-10 16:04:51 UTC — 050 · Claude read the message

- **Actor:** Claude (claude-opus-5 · 1468 in / 517 out tokens)
- **Tool:** Anthropic Messages API `ai.triage` (prompt property-triage-2026-10-10.3) · step `triage_case_messages`
- **Reading:** update · route `request_quote` · high confidence
- **Work item:** Radiator heating cutting out intermittently (other)
- **Summary:** Property manager instructed contractor Copper Finch Mechanical to diagnose the intermittent radiator heating, provide a written report and itemised estimate before any work beyond diagnosis, noting access after 14:00 and a diagnostic-only authorisation ceiling of £180 including VAT.
- **Rationale:** Diagnostic and itemised estimate requested from contractor before any remedial work; quote stage ongoing.
- **Extracted:** 2 claims · 2 ambiguities · 1 issue
- **Unknown:** "After 14:00" is general availability; no specific visit date and time is agreed with the contractor.
- **Unknown:** Confirm the tenant has agreed entry for this specific visit and the access method.

<a id="entry-051"></a>
## 2026-10-10 16:04:51 UTC — 051 · Claim `total` = 180.0

- **Actor:** Claude (extracted)
- **Status:** unverified assertion — a person or policy must accept it

> the diagnostic-only authorization ceiling of £180 including VAT

<a id="entry-052"></a>
## 2026-10-10 16:04:51 UTC — 052 · Policy gates → HUMAN REVIEW

- **Actor:** Policy engine (rules v1, `domain.evaluate`)
- **Outcome:** HUMAN REVIEW · owner case manager
- **Blockers:** `identity` UNKNOWN → HUMAN REVIEW; `route` UNKNOWN → HUMAN REVIEW; `classification` UNKNOWN → HUMAN REVIEW; `supported` UNKNOWN → HUMAN REVIEW
- **Next step:** Verify the person, property and work item mapping.

<a id="entry-053"></a>
## 2026-10-10 16:04:51 UTC — 053 · Message received: Event 007 — Email from Petra Quill (Contractor, Copper Finch Mechanical)

- **Recorded by:** demo-case_manager (case manager)
- **Reading:** queued for Jev routing / Claude triage

> Event 007 — Email
> From: Petra Quill (Contractor, Copper Finch Mechanical)
> To: Ivo Merrick (Property Manager, Northbridge Lettings)
>
> Confirmed attendance for 5 February after 14:00. Quoted £138 including VAT for attendance, diagnosis and testing; parts and remedial work were excluded.

<a id="entry-054"></a>
## 2026-10-10 16:04:51 UTC — 054 · Policy gates → HUMAN REVIEW

- **Actor:** Policy engine (rules v1, `domain.evaluate`)
- **Outcome:** HUMAN REVIEW · owner case manager
- **Blockers:** `identity` UNKNOWN → HUMAN REVIEW; `route` UNKNOWN → HUMAN REVIEW; `classification` UNKNOWN → HUMAN REVIEW; `supported` UNKNOWN → HUMAN REVIEW; `triage` UNKNOWN → WAIT
- **Next step:** Verify the person, property and work item mapping.

<a id="entry-055"></a>
## 2026-10-10 16:04:51 UTC — 055 · Workflow receipt

<a id="entry-056"></a>
## 2026-10-10 16:04:52 UTC — 056 · Jev routed the message

- **Actor:** Jev (jev-1.13.0 · 1704 in / 284 out tokens · 345 ms)
- **Tool:** TypeSafe `system_one` · step `route_case_messages`
- **Decision:** jev_route → `confirm_appointment` (confidence 0.69)
- **Signals:** hazard 0.04 · multiple_issues 0.03 · sensitive 0.02 · states_facts 0.98 · system_instructions 0.02
- **Why:** Jev routes; Claude extracts quotes and claims. confirm_appointment is not a Jev-only route. Route confidence 0.69 is below the Jev-only bar 0.8. The message may state facts that need exact quotes. A route change on an existing case.

<a id="entry-057"></a>
## 2026-10-10 16:04:58 UTC — 057 · Claude read the message

- **Actor:** Claude (claude-opus-5 · 1748 in / 478 out tokens)
- **Tool:** Anthropic Messages API `ai.triage` (prompt property-triage-2026-10-10.3) · step `triage_case_messages`
- **Reading:** access or appointment · route `confirm_appointment` · high confidence
- **Work item:** Radiator heating cutting out intermittently (other)
- **Summary:** Contractor Petra Quill confirms attendance on 5 February after 14:00 for the diagnostic visit and quotes £138 including VAT for attendance, diagnosis and testing, excluding parts and remedial work.
- **Rationale:** Contractor arranging a visit for an already known job and stating the diagnostic price; appointment confirmation is the next step.
- **Extracted:** 2 claims · 2 ambiguities · 1 issue
- **Unknown:** No precise arrival time is given, only 'after 14:00' on 5 February; confirm a time window with the tenant.
- **Unknown:** Tenant has not confirmed consent/access for this specific date.

<a id="entry-058"></a>
## 2026-10-10 16:04:58 UTC — 058 · Proposed action → `confirm_appointment`

- **Actor:** Triage reading (route `confirm_appointment`)
- **Work item:** Radiator heating cutting out intermittently
- **Action revision:** 4

<a id="entry-059"></a>
## 2026-10-10 16:04:58 UTC — 059 · Claim `total` = 138.0

- **Actor:** Claude (extracted)
- **Status:** unverified assertion — a person or policy must accept it

> Quoted £138 including VAT for attendance, diagnosis and testing; parts and remedial work were excluded.

<a id="entry-060"></a>
## 2026-10-10 16:04:58 UTC — 060 · Claim `schedule` = true

- **Actor:** Claude (extracted)
- **Status:** unverified assertion — a person or policy must accept it

> Confirmed attendance for 5 February after 14:00.

<a id="entry-061"></a>
## 2026-10-10 16:04:58 UTC — 061 · Human review opened: `identity`

- **Actor:** Policy engine
- **Owner:** case manager · rule `require-identity`
- **Expires:** 2026-10-12 16:04:58 UTC

> Verify the person, property and work item mapping.

<a id="entry-062"></a>
## 2026-10-10 16:04:58 UTC — 062 · Human review opened: `route`

- **Actor:** Policy engine
- **Owner:** case manager · rule `require-route`
- **Expires:** 2026-10-12 16:04:58 UTC

> Verify the recipient and permitted communication route.

<a id="entry-063"></a>
## 2026-10-10 16:04:58 UTC — 063 · Human review opened: `access`

- **Actor:** Policy engine
- **Owner:** access officer · rule `require-access`
- **Expires:** 2026-10-12 16:04:58 UTC

> Record consent for this visit and access method from the authorised person. A verified route is required before asking externally.

<a id="entry-064"></a>
## 2026-10-10 16:04:58 UTC — 064 · Human review opened: `authority`

- **Actor:** Policy engine
- **Owner:** approver · rule `require-authority`
- **Expires:** 2026-10-12 16:04:58 UTC

> Obtain authority for this work item, provider and action.

<a id="entry-065"></a>
## 2026-10-10 16:04:58 UTC — 065 · Human review opened: `schedule`

- **Actor:** Policy engine
- **Owner:** case manager · rule `require-schedule`
- **Expires:** 2026-10-12 16:04:58 UTC

> Confirm the active appointment with a precise date and time. A verified route is required before asking externally.

<a id="entry-066"></a>
## 2026-10-10 16:04:58 UTC — 066 · Human review opened: `supported`

- **Actor:** Policy engine
- **Owner:** case manager · rule `require-supported`
- **Expires:** 2026-10-12 16:04:58 UTC

> A case manager must define a supported action for this situation.

<a id="entry-067"></a>
## 2026-10-10 16:04:58 UTC — 067 · Policy gates → HUMAN REVIEW

- **Actor:** Policy engine (rules v1, `domain.evaluate`)
- **Outcome:** HUMAN REVIEW · owner case manager
- **Blockers:** `identity` UNKNOWN → HUMAN REVIEW; `route` UNKNOWN → HUMAN REVIEW; `access` UNKNOWN → HUMAN REVIEW; `authority` UNKNOWN → HUMAN REVIEW; `schedule` UNKNOWN → HUMAN REVIEW; `supported` UNKNOWN → HUMAN REVIEW
- **Next step:** Verify the person, property and work item mapping.

<a id="entry-068"></a>
## 2026-10-10 16:04:58 UTC — 068 · Message received: Event 008 — Update from Petra Quill (Contractor, Copper Finch Mechanical)

- **Recorded by:** demo-case_manager (case manager)
- **Reading:** queued for Jev routing / Claude triage

> Event 008 — Update
> From: Petra Quill (Contractor, Copper Finch Mechanical)
> To: Ivo Merrick (Property Manager, Northbridge Lettings)
>
> Reported attending and finding an intermittent fault at the heating valve actuator. Said the heating operated during the visit and that no leak or immediate gas-safety concern was observed. No remedial work was reported in this update.

<a id="entry-069"></a>
## 2026-10-10 16:04:58 UTC — 069 · Policy gates → HUMAN REVIEW

- **Actor:** Policy engine (rules v1, `domain.evaluate`)
- **Outcome:** HUMAN REVIEW · owner case manager
- **Blockers:** `identity` UNKNOWN → HUMAN REVIEW; `route` UNKNOWN → HUMAN REVIEW; `access` UNKNOWN → HUMAN REVIEW; `authority` UNKNOWN → HUMAN REVIEW; `schedule` UNKNOWN → HUMAN REVIEW; `supported` UNKNOWN → HUMAN REVIEW; `triage` UNKNOWN → WAIT
- **Next step:** Verify the person, property and work item mapping.

<a id="entry-070"></a>
## 2026-10-10 16:04:58 UTC — 070 · Workflow receipt

<a id="entry-071"></a>
## 2026-10-10 16:04:58 UTC — 071 · Jev routed the message

- **Actor:** Jev (jev-1.13.0 · 1717 in / 284 out tokens · 317 ms)
- **Tool:** TypeSafe `system_one` · step `route_case_messages`
- **Decision:** claude → no route
- **Signals:** hazard 0.04 · multiple_issues 0.03 · sensitive 0.02 · states_facts 0.49 · system_instructions 0.02
- **Why:** Jev route confidence 0.29 is below 0.5.

<a id="entry-072"></a>
## 2026-10-10 16:05:09 UTC — 072 · Claude read the message

- **Actor:** Claude (claude-opus-5 · 1697 in / 731 out tokens)
- **Tool:** Anthropic Messages API `ai.triage` (prompt property-triage-2026-10-10.3) · step `triage_case_messages`
- **Reading:** update · route `request_quote` · medium confidence
- **Work item:** Radiator heating cutting out intermittently (other)
- **Summary:** Contractor Petra Quill reports attending the property and diagnosing an intermittent fault at the heating valve actuator; heating worked during the visit and no leak or gas-safety concern was seen. No remedial work or itemised estimate has been provided yet.
- **Rationale:** Diagnosis has been carried out but no remedial scope or price is stated; the next step is obtaining an itemised quote before landlord approval of any repair.
- **Extracted:** 0 claims · 3 ambiguities · 1 issue
- **Unknown (affects route):** No written report or itemised estimate for remedial work on the valve actuator has been supplied, so the cost and scope of the repair are unknown.
- **Unknown:** Unclear whether the diagnostic visit is regarded as complete and what the final diagnostic charge was against the £180 including VAT ceiling.
- **Unknown:** No follow-up visit date has been proposed for any remedial work.

<a id="entry-073"></a>
## 2026-10-10 16:05:09 UTC — 073 · Proposed action → `request_quote`

- **Actor:** Triage reading (route `request_quote`)
- **Work item:** Radiator heating cutting out intermittently
- **Action revision:** 5

<a id="entry-074"></a>
## 2026-10-10 16:05:09 UTC — 074 · Human review opened: `identity`

- **Actor:** Policy engine
- **Owner:** case manager · rule `require-identity`
- **Expires:** 2026-10-12 16:05:09 UTC

> Verify the person, property and work item mapping.

<a id="entry-075"></a>
## 2026-10-10 16:05:09 UTC — 075 · Human review opened: `route`

- **Actor:** Policy engine
- **Owner:** case manager · rule `require-route`
- **Expires:** 2026-10-12 16:05:09 UTC

> Verify the recipient and permitted communication route.

<a id="entry-076"></a>
## 2026-10-10 16:05:09 UTC — 076 · Human review opened: `classification`

- **Actor:** Policy engine
- **Owner:** case manager · rule `require-classification`
- **Expires:** 2026-10-12 16:05:09 UTC

> Confirm that the category and work item match the source request. A verified route is required before asking externally.

<a id="entry-077"></a>
## 2026-10-10 16:05:09 UTC — 077 · Human review opened: `supported`

- **Actor:** Policy engine
- **Owner:** case manager · rule `require-supported`
- **Expires:** 2026-10-12 16:05:09 UTC

> A case manager must define a supported action for this situation.

<a id="entry-078"></a>
## 2026-10-10 16:05:09 UTC — 078 · Human review opened: `triage`

- **Actor:** Policy engine
- **Owner:** case manager · rule `require-triage`
- **Expires:** 2026-10-12 16:05:09 UTC

> Clarify before routing: No written report or itemised estimate for remedial work on the valve actuator has been supplied, so the cost and scope of the repair are unknown. A verified route is required before asking externally.

<a id="entry-079"></a>
## 2026-10-10 16:05:09 UTC — 079 · Policy gates → HUMAN REVIEW

- **Actor:** Policy engine (rules v1, `domain.evaluate`)
- **Outcome:** HUMAN REVIEW · owner case manager
- **Blockers:** `identity` UNKNOWN → HUMAN REVIEW; `route` UNKNOWN → HUMAN REVIEW; `classification` UNKNOWN → HUMAN REVIEW; `supported` UNKNOWN → HUMAN REVIEW; `triage` UNKNOWN → HUMAN REVIEW
- **Next step:** Verify the person, property and work item mapping.

<a id="entry-080"></a>
## 2026-10-10 16:05:09 UTC — 080 · Message received: Event 009 — Email from Petra Quill (Contractor, Copper Finch Mechanical)

- **Recorded by:** demo-case_manager (case manager)
- **Reading:** queued for Jev routing / Claude triage

> Event 009 — Email
> From: Petra Quill (Contractor, Copper Finch Mechanical)
> To: Ivo Merrick (Property Manager, Northbridge Lettings)
>
> Sent an estimate for £372 including VAT for actuator supply and replacement, attendance and heating-system testing. Requested written authorization before proceeding. The estimate did not say whether the £138 diagnostic charge would be credited.

<a id="entry-081"></a>
## 2026-10-10 16:05:09 UTC — 081 · Policy gates → HUMAN REVIEW

- **Actor:** Policy engine (rules v1, `domain.evaluate`)
- **Outcome:** HUMAN REVIEW · owner case manager
- **Blockers:** `identity` UNKNOWN → HUMAN REVIEW; `route` UNKNOWN → HUMAN REVIEW; `classification` UNKNOWN → HUMAN REVIEW; `supported` UNKNOWN → HUMAN REVIEW; `triage` UNKNOWN → WAIT
- **Next step:** Verify the person, property and work item mapping.

<a id="entry-082"></a>
## 2026-10-10 16:05:09 UTC — 082 · Workflow receipt

<a id="entry-083"></a>
## 2026-10-10 16:05:09 UTC — 083 · Jev routed the message

- **Actor:** Jev (jev-1.13.0 · 1737 in / 282 out tokens · 234 ms)
- **Tool:** TypeSafe `system_one` · step `route_case_messages`
- **Decision:** claude → no route
- **Signals:** hazard 0.03 · multiple_issues 0.04 · sensitive 0.02 · states_facts 0.97 · system_instructions 0.02
- **Why:** Jev route confidence 0.33 is below 0.5.

<a id="entry-084"></a>
## 2026-10-10 16:05:16 UTC — 084 · Claude read the message

- **Actor:** Claude (claude-opus-5 · 1782 in / 550 out tokens)
- **Tool:** Anthropic Messages API `ai.triage` (prompt property-triage-2026-10-10.3) · step `triage_case_messages`
- **Reading:** update · route `instruct_work` · medium confidence
- **Work item:** Radiator heating cutting out intermittently (other)
- **Summary:** Contractor Petra Quill has submitted an estimate of £372 including VAT to supply and replace the heating valve actuator, including attendance and system testing, and asks for written authorisation before proceeding. It is unclear whether the £138 diagnostic charge is credited against this figure.
- **Rationale:** The job has been diagnosed and a written estimate supplied; the next step is a decision on instructing the contractor, though landlord authority above £180 must first be obtained.
- **Extracted:** 1 claim · 3 ambiguities · 1 issue
- **Unknown:** The estimate does not state whether the £138 diagnostic charge is credited against the £372, so the full comparable commitment is unclear.
- **Unknown (affects route):** £372 exceeds the agency's £180 routine repair limit and the landlord's diagnostic-only authorisation; landlord approval is needed before instructing.
- **Unknown:** No appointment date or time proposed for the remedial visit.

<a id="entry-085"></a>
## 2026-10-10 16:05:16 UTC — 085 · Proposed action → `instruct_work`

- **Actor:** Triage reading (route `instruct_work`)
- **Work item:** Radiator heating cutting out intermittently
- **Action revision:** 6

<a id="entry-086"></a>
## 2026-10-10 16:05:16 UTC — 086 · Claim `total` = 372.0

- **Actor:** Claude (extracted)
- **Status:** unverified assertion — a person or policy must accept it

> Sent an estimate for £372 including VAT for actuator supply and replacement, attendance and heating-system testing.

<a id="entry-087"></a>
## 2026-10-10 16:05:16 UTC — 087 · Human review opened: `identity`

- **Actor:** Policy engine
- **Owner:** case manager · rule `require-identity`
- **Expires:** 2026-10-12 16:05:16 UTC

> Verify the person, property and work item mapping.

<a id="entry-088"></a>
## 2026-10-10 16:05:16 UTC — 088 · Human review opened: `route`

- **Actor:** Policy engine
- **Owner:** case manager · rule `require-route`
- **Expires:** 2026-10-12 16:05:16 UTC

> Verify the recipient and permitted communication route.

<a id="entry-089"></a>
## 2026-10-10 16:05:16 UTC — 089 · Human review opened: `access`

- **Actor:** Policy engine
- **Owner:** access officer · rule `require-access`
- **Expires:** 2026-10-12 16:05:16 UTC

> Record consent for this visit and access method from the authorised person. A verified route is required before asking externally.

<a id="entry-090"></a>
## 2026-10-10 16:05:16 UTC — 090 · Human review opened: `authority`

- **Actor:** Policy engine
- **Owner:** approver · rule `require-authority`
- **Expires:** 2026-10-12 16:05:16 UTC

> Obtain authority for this work item, provider and action.

<a id="entry-091"></a>
## 2026-10-10 16:05:16 UTC — 091 · Human review opened: `schedule`

- **Actor:** Policy engine
- **Owner:** case manager · rule `require-schedule`
- **Expires:** 2026-10-12 16:05:16 UTC

> Confirm the active appointment with a precise date and time. A verified route is required before asking externally.

<a id="entry-092"></a>
## 2026-10-10 16:05:16 UTC — 092 · Human review opened: `evidence`

- **Actor:** Policy engine
- **Owner:** case manager · rule `require-evidence`
- **Expires:** 2026-10-12 16:05:16 UTC

> Supply usable evidence required for this work item. A verified route is required before asking externally.

<a id="entry-093"></a>
## 2026-10-10 16:05:16 UTC — 093 · Human review opened: `classification`

- **Actor:** Policy engine
- **Owner:** case manager · rule `require-classification`
- **Expires:** 2026-10-12 16:05:16 UTC

> Confirm that the category and work item match the source request. A verified route is required before asking externally.

<a id="entry-094"></a>
## 2026-10-10 16:05:16 UTC — 094 · Human review opened: `total`

- **Actor:** Policy engine
- **Owner:** case manager · rule `require-total`
- **Expires:** 2026-10-12 16:05:16 UTC

> Establish the full comparable commitment, including tax. A verified route is required before asking externally.

<a id="entry-095"></a>
## 2026-10-10 16:05:16 UTC — 095 · Human review opened: `supported`

- **Actor:** Policy engine
- **Owner:** case manager · rule `require-supported`
- **Expires:** 2026-10-12 16:05:16 UTC

> A case manager must define a supported action for this situation.

<a id="entry-096"></a>
## 2026-10-10 16:05:16 UTC — 096 · Human review opened: `triage`

- **Actor:** Policy engine
- **Owner:** case manager · rule `require-triage`
- **Expires:** 2026-10-12 16:05:16 UTC

> Clarify before routing: £372 exceeds the agency's £180 routine repair limit and the landlord's diagnostic-only authorisation; landlord approval is needed before instructing. A verified route is required before asking externally.

<a id="entry-097"></a>
## 2026-10-10 16:05:16 UTC — 097 · Policy gates → HUMAN REVIEW

- **Actor:** Policy engine (rules v1, `domain.evaluate`)
- **Outcome:** HUMAN REVIEW · owner case manager
- **Blockers:** `identity` UNKNOWN → HUMAN REVIEW; `route` UNKNOWN → HUMAN REVIEW; `access` UNKNOWN → HUMAN REVIEW; `authority` UNKNOWN → HUMAN REVIEW; `schedule` UNKNOWN → HUMAN REVIEW; `evidence` UNKNOWN → HUMAN REVIEW; `classification` UNKNOWN → HUMAN REVIEW; `total` UNKNOWN → HUMAN REVIEW; `supported` UNKNOWN → HUMAN REVIEW; `triage` UNKNOWN → HUMAN REVIEW
- **Next step:** Verify the person, property and work item mapping.

<a id="entry-098"></a>
## 2026-10-10 16:05:16 UTC — 098 · Message received: Event 010 — Email from Ivo Merrick (Property Manager, Northbridge Lettings)

- **Recorded by:** demo-case_manager (case manager)
- **Reading:** queued for Jev routing / Claude triage

> Event 010 — Email
> From: Ivo Merrick (Property Manager, Northbridge Lettings)
> To: Soren Dallow (Landlord)
>
> Forwarded the estimate and asked whether the proposed work was authorized. Noted that it exceeded the routine limit and that the contractor had been told to obtain written authorization before remedial work.

<a id="entry-099"></a>
## 2026-10-10 16:05:16 UTC — 099 · Policy gates → HUMAN REVIEW

- **Actor:** Policy engine (rules v1, `domain.evaluate`)
- **Outcome:** HUMAN REVIEW · owner case manager
- **Blockers:** `identity` UNKNOWN → HUMAN REVIEW; `route` UNKNOWN → HUMAN REVIEW; `access` UNKNOWN → HUMAN REVIEW; `authority` UNKNOWN → HUMAN REVIEW; `schedule` UNKNOWN → HUMAN REVIEW; `evidence` UNKNOWN → HUMAN REVIEW; `classification` UNKNOWN → HUMAN REVIEW; `total` UNKNOWN → HUMAN REVIEW; `supported` UNKNOWN → HUMAN REVIEW; `triage` UNKNOWN → WAIT
- **Next step:** Verify the person, property and work item mapping.

<a id="entry-100"></a>
## 2026-10-10 16:05:16 UTC — 100 · Workflow receipt

<a id="entry-101"></a>
## 2026-10-10 16:05:16 UTC — 101 · Jev routed the message

- **Actor:** Jev (jev-1.13.0 · 1730 in / 283 out tokens · 354 ms)
- **Tool:** TypeSafe `system_one` · step `route_case_messages`
- **Decision:** jev_route → `instruct_work` (confidence 0.79)
- **Signals:** hazard 0.05 · multiple_issues 0.04 · sensitive 0.03 · states_facts 0.16 · system_instructions 0.02
- **Why:** Jev routes; Claude extracts quotes and claims. instruct_work is not a Jev-only route. Route confidence 0.79 is below the Jev-only bar 0.8.

<a id="entry-102"></a>
## 2026-10-10 16:05:22 UTC — 102 · Claude read the message

- **Actor:** Claude (claude-opus-5 · 1905 in / 359 out tokens)
- **Tool:** Anthropic Messages API `ai.triage` (prompt property-triage-2026-10-10.3) · step `triage_case_messages`
- **Reading:** update · route `instruct_work` · medium confidence
- **Work item:** Radiator heating cutting out intermittently (other)
- **Summary:** The property manager forwarded the contractor's £372 estimate to the landlord and asked whether the remedial work is authorised, noting it exceeds the routine repair limit and that the contractor must have written authorisation first.
- **Rationale:** Router chose instruct_work for the known job; message is an authorisation request to the landlord and the next step is instructing once approval arrives.
- **Extracted:** 0 claims · 1 ambiguity · 1 issue
- **Unknown (affects route):** Landlord approval for the £372 remedial estimate has not yet been given; work cannot be instructed until written authorisation is received.
- **Objected to Jev's route:** No authority has yet been given for the £372 estimate, so the item cannot be instructed; it is awaiting landlord approval.

<a id="entry-103"></a>
## 2026-10-10 16:05:22 UTC — 103 · Policy gates → HUMAN REVIEW

- **Actor:** Policy engine (rules v1, `domain.evaluate`)
- **Outcome:** HUMAN REVIEW · owner case manager
- **Blockers:** `identity` UNKNOWN → HUMAN REVIEW; `route` UNKNOWN → HUMAN REVIEW; `access` UNKNOWN → HUMAN REVIEW; `authority` UNKNOWN → HUMAN REVIEW; `schedule` UNKNOWN → HUMAN REVIEW; `evidence` UNKNOWN → HUMAN REVIEW; `classification` UNKNOWN → HUMAN REVIEW; `total` UNKNOWN → HUMAN REVIEW; `supported` UNKNOWN → HUMAN REVIEW; `triage` CONFLICT → HUMAN REVIEW
- **Next step:** Verify the person, property and work item mapping.

<a id="entry-104"></a>
## 2026-10-10 16:05:22 UTC — 104 · Message received: Event 011 — SMS from Tessa Vane (Tenant)

- **Recorded by:** demo-case_manager (case manager)
- **Reading:** queued for Jev routing / Claude triage

> Event 011 — SMS
> From: Tessa Vane (Tenant)
> To: Ivo Merrick (Property Manager, Northbridge Lettings)
>
> Reported that the radiators were cold again. She was using one portable heater in the sitting room and said it was plugged directly into a wall socket. No new smell, leak or warning was reported.

<a id="entry-105"></a>
## 2026-10-10 16:05:22 UTC — 105 · Policy gates → HUMAN REVIEW

- **Actor:** Policy engine (rules v1, `domain.evaluate`)
- **Outcome:** HUMAN REVIEW · owner case manager
- **Blockers:** `identity` UNKNOWN → HUMAN REVIEW; `route` UNKNOWN → HUMAN REVIEW; `access` UNKNOWN → HUMAN REVIEW; `authority` UNKNOWN → HUMAN REVIEW; `schedule` UNKNOWN → HUMAN REVIEW; `evidence` UNKNOWN → HUMAN REVIEW; `classification` UNKNOWN → HUMAN REVIEW; `total` UNKNOWN → HUMAN REVIEW; `supported` UNKNOWN → HUMAN REVIEW; `triage` UNKNOWN → WAIT
- **Next step:** Verify the person, property and work item mapping.

<a id="entry-106"></a>
## 2026-10-10 16:05:22 UTC — 106 · Workflow receipt

<a id="entry-107"></a>
## 2026-10-10 16:05:22 UTC — 107 · Jev routed the message

- **Actor:** Jev (jev-1.13.0 · 1726 in / 283 out tokens · 283 ms)
- **Tool:** TypeSafe `system_one` · step `route_case_messages`
- **Decision:** jev_route → `instruct_work` (confidence 0.63)
- **Signals:** hazard 0.15 · multiple_issues 0.05 · sensitive 0.04 · states_facts 0.18 · system_instructions 0.02
- **Why:** Jev routes; Claude extracts quotes and claims. instruct_work is not a Jev-only route. Route confidence 0.63 is below the Jev-only bar 0.8.

<a id="entry-108"></a>
## 2026-10-10 16:05:27 UTC — 108 · Claude read the message

- **Actor:** Claude (claude-opus-5 · 1881 in / 423 out tokens)
- **Tool:** Anthropic Messages API `ai.triage` (prompt property-triage-2026-10-10.3) · step `triage_case_messages`
- **Reading:** update · route `instruct_work` · medium confidence
- **Work item:** Radiator heating cutting out intermittently (other)
- **Summary:** Tenant reports radiators cold again and is using a portable heater plugged directly into a wall socket. No smell, leak or warning reported; landlord authorisation for the £372 remedial estimate is still outstanding.
- **Rationale:** Fault recurring after diagnosis; next step is the remedial actuator work, but landlord authorisation remains outstanding. No explicit hazard reported.
- **Extracted:** 1 claim · 2 ambiguities · 1 issue · risk flags: safety
- **Unknown (affects route):** Whether the tenant or household includes anyone vulnerable, and how long the heating has been off, to judge urgency.
- **Unknown (affects route):** Landlord written authorisation for the £372 actuator replacement is still outstanding, so work cannot be instructed yet.

<a id="entry-109"></a>
## 2026-10-10 16:05:27 UTC — 109 · Claim `completion` = false

- **Actor:** Claude (extracted)
- **Status:** unverified assertion — a person or policy must accept it

> Reported that the radiators were cold again.

<a id="entry-110"></a>
## 2026-10-10 16:05:27 UTC — 110 · Policy gates → HUMAN REVIEW

- **Actor:** Policy engine (rules v1, `domain.evaluate`)
- **Outcome:** HUMAN REVIEW · owner case manager
- **Blockers:** `identity` UNKNOWN → HUMAN REVIEW; `route` UNKNOWN → HUMAN REVIEW; `access` UNKNOWN → HUMAN REVIEW; `authority` UNKNOWN → HUMAN REVIEW; `schedule` UNKNOWN → HUMAN REVIEW; `evidence` UNKNOWN → HUMAN REVIEW; `classification` UNKNOWN → HUMAN REVIEW; `total` UNKNOWN → HUMAN REVIEW; `supported` UNKNOWN → HUMAN REVIEW; `triage` UNKNOWN → HUMAN REVIEW
- **Next step:** Verify the person, property and work item mapping.

<a id="entry-111"></a>
## 2026-10-10 16:05:28 UTC — 111 · Message received: Event 012 — Email from Soren Dallow (Landlord)

- **Recorded by:** demo-case_manager (case manager)
- **Reading:** queued for Jev routing / Claude triage

> Event 012 — Email
> From: Soren Dallow (Landlord)
> To: Ivo Merrick (Property Manager, Northbridge Lettings)
>
> Had not decided on the estimate. Asked whether the actuator could be repaired and whether the price included all parts, labour and testing. Did not authorize remedial work or further expenditure.

<a id="entry-112"></a>
## 2026-10-10 16:05:28 UTC — 112 · Policy gates → HUMAN REVIEW

- **Actor:** Policy engine (rules v1, `domain.evaluate`)
- **Outcome:** HUMAN REVIEW · owner case manager
- **Blockers:** `identity` UNKNOWN → HUMAN REVIEW; `route` UNKNOWN → HUMAN REVIEW; `access` UNKNOWN → HUMAN REVIEW; `authority` UNKNOWN → HUMAN REVIEW; `schedule` UNKNOWN → HUMAN REVIEW; `evidence` UNKNOWN → HUMAN REVIEW; `classification` UNKNOWN → HUMAN REVIEW; `total` UNKNOWN → HUMAN REVIEW; `supported` UNKNOWN → HUMAN REVIEW; `triage` UNKNOWN → WAIT
- **Next step:** Verify the person, property and work item mapping.

<a id="entry-113"></a>
## 2026-10-10 16:05:28 UTC — 113 · Workflow receipt

<a id="entry-114"></a>
## 2026-10-10 16:05:28 UTC — 114 · Jev routed the message

- **Actor:** Jev (jev-1.13.0 · 1714 in / 282 out tokens · 245 ms)
- **Tool:** TypeSafe `system_one` · step `route_case_messages`
- **Decision:** jev_route → `clarify` (confidence 0.64)
- **Signals:** hazard 0.09 · multiple_issues 0.04 · sensitive 0.04 · states_facts 0.12 · system_instructions 0.02
- **Why:** Jev routes; Claude extracts quotes and claims. clarify is not a Jev-only route. Route confidence 0.64 is below the Jev-only bar 0.8. A route change on an existing case.

<a id="entry-115"></a>
## 2026-10-10 16:05:35 UTC — 115 · Claude read the message

- **Actor:** Claude (claude-opus-5 · 1931 in / 504 out tokens)
- **Tool:** Anthropic Messages API `ai.triage` (prompt property-triage-2026-10-10.3) · step `triage_case_messages`
- **Reading:** answer to question · route `clarify` · high confidence
- **Work item:** Radiator heating cutting out intermittently (other)
- **Summary:** Landlord Soren Dallow has not decided on the £372 actuator estimate and asks whether the actuator could be repaired instead and whether the price covers all parts, labour and testing. He explicitly did not authorise remedial work or further expenditure.
- **Rationale:** Authorisation withheld pending answers on repair option and price scope, so the item cannot be instructed and needs clarification.
- **Extracted:** 1 claim · 3 ambiguities · 1 issue
- **Unknown (affects route):** Landlord asks whether a repair of the actuator is possible instead of replacement; contractor needs to confirm.
- **Unknown:** Whether the £372 including VAT covers all parts, labour and testing, and whether the £138 diagnostic charge is credited.
- **Unknown (affects route):** Tenant reports radiators cold again and is using a portable heater; vulnerability and duration without heating still unknown.

<a id="entry-116"></a>
## 2026-10-10 16:05:35 UTC — 116 · Proposed action → `clarify`

- **Actor:** Triage reading (route `clarify`)
- **Work item:** Radiator heating cutting out intermittently
- **Action revision:** 7

<a id="entry-117"></a>
## 2026-10-10 16:05:35 UTC — 117 · Human review opened: `identity`

- **Actor:** Policy engine
- **Owner:** case manager · rule `require-identity`
- **Expires:** 2026-10-12 16:05:35 UTC

> Verify the person, property and work item mapping.

<a id="entry-118"></a>
## 2026-10-10 16:05:35 UTC — 118 · Human review opened: `route`

- **Actor:** Policy engine
- **Owner:** case manager · rule `require-route`
- **Expires:** 2026-10-12 16:05:35 UTC

> Verify the recipient and permitted communication route.

<a id="entry-119"></a>
## 2026-10-10 16:05:35 UTC — 119 · Human review opened: `triage`

- **Actor:** Policy engine
- **Owner:** case manager · rule `require-triage`
- **Expires:** 2026-10-12 16:05:35 UTC

> Clarify before routing: Landlord asks whether a repair of the actuator is possible instead of replacement; contractor needs to confirm.; Tenant reports radiators cold again and is using a portable heater; vulnerability and duration without heating still unknown. A verified route is required before asking externally.

<a id="entry-120"></a>
## 2026-10-10 16:05:35 UTC — 120 · Policy gates → HUMAN REVIEW

- **Actor:** Policy engine (rules v1, `domain.evaluate`)
- **Outcome:** HUMAN REVIEW · owner case manager
- **Blockers:** `identity` UNKNOWN → HUMAN REVIEW; `route` UNKNOWN → HUMAN REVIEW; `triage` UNKNOWN → HUMAN REVIEW
- **Next step:** Verify the person, property and work item mapping.

<a id="entry-121"></a>
## 2026-10-10 16:05:35 UTC — 121 · Message received: Event 013 — Portal from Ivo Merrick (Property Manager, Northbridge Lettings)

- **Recorded by:** demo-case_manager (case manager)
- **Reading:** queued for Jev routing / Claude triage

> Event 013 — Portal
> From: Ivo Merrick (Property Manager, Northbridge Lettings)
> To: Tessa Vane (Tenant)
>
> Asked whether heating or safety symptoms had changed, whether the equipment-label details were available, and whether the contractor could be given access if a return visit were arranged.

<a id="entry-122"></a>
## 2026-10-10 16:05:35 UTC — 122 · Policy gates → HUMAN REVIEW

- **Actor:** Policy engine (rules v1, `domain.evaluate`)
- **Outcome:** HUMAN REVIEW · owner case manager
- **Blockers:** `identity` UNKNOWN → HUMAN REVIEW; `route` UNKNOWN → HUMAN REVIEW; `triage` UNKNOWN → WAIT
- **Next step:** Verify the person, property and work item mapping.

<a id="entry-123"></a>
## 2026-10-10 16:05:35 UTC — 123 · Workflow receipt

<a id="entry-124"></a>
## 2026-10-10 16:05:36 UTC — 124 · Jev routed the message

- **Actor:** Jev (jev-1.13.0 · 1698 in / 282 out tokens · 384 ms)
- **Tool:** TypeSafe `system_one` · step `route_case_messages`
- **Decision:** jev_route → `clarify` (confidence 0.76)
- **Signals:** hazard 0.13 · multiple_issues 0.07 · sensitive 0.04 · states_facts 0.19 · system_instructions 0.02
- **Why:** Jev routes; Claude extracts quotes and claims. clarify is not a Jev-only route. Route confidence 0.76 is below the Jev-only bar 0.8.

<a id="entry-125"></a>
## 2026-10-10 16:05:40 UTC — 125 · Claude read the message

- **Actor:** Claude (claude-opus-5 · 1873 in / 376 out tokens)
- **Tool:** Anthropic Messages API `ai.triage` (prompt property-triage-2026-10-10.3) · step `triage_case_messages`
- **Reading:** update · route `clarify` · high confidence
- **Work item:** Radiator heating cutting out intermittently (other)
- **Summary:** Property manager asked the tenant whether heating or safety symptoms had changed, whether equipment-label details were available, and whether access could be given for a possible return visit. No new facts or decisions are asserted.
- **Rationale:** Outbound clarification request to the tenant; no new facts, so the item stays at clarify pending reply.
- **Extracted:** 0 claims · 2 ambiguities · 1 issue
- **Unknown (affects route):** Awaiting tenant's reply on whether heating or safety symptoms have changed and whether equipment-label details are available.
- **Unknown:** Tenant has not yet confirmed whether the contractor can be given access for a return visit.

<a id="entry-126"></a>
## 2026-10-10 16:05:40 UTC — 126 · Policy gates → HUMAN REVIEW

- **Actor:** Policy engine (rules v1, `domain.evaluate`)
- **Outcome:** HUMAN REVIEW · owner case manager
- **Blockers:** `identity` UNKNOWN → HUMAN REVIEW; `route` UNKNOWN → HUMAN REVIEW; `triage` UNKNOWN → HUMAN REVIEW
- **Next step:** Verify the person, property and work item mapping.

<a id="entry-127"></a>
## 2026-10-10 16:05:40 UTC — 127 · Message received: Event 014 — Portal from Tessa Vane (Tenant)

- **Recorded by:** demo-case_manager (case manager)
- **Reading:** queued for Jev routing / Claude triage

> Event 014 — Portal
> From: Tessa Vane (Tenant)
> To: Ivo Merrick (Property Manager, Northbridge Lettings)
>
> Said the radiators were still inconsistent and repeated that hot water was available. Supplied the boiler-label details in the message. She had not agreed a return appointment.

<a id="entry-128"></a>
## 2026-10-10 16:05:40 UTC — 128 · Policy gates → HUMAN REVIEW

- **Actor:** Policy engine (rules v1, `domain.evaluate`)
- **Outcome:** HUMAN REVIEW · owner case manager
- **Blockers:** `identity` UNKNOWN → HUMAN REVIEW; `route` UNKNOWN → HUMAN REVIEW; `triage` UNKNOWN → WAIT
- **Next step:** Verify the person, property and work item mapping.

<a id="entry-129"></a>
## 2026-10-10 16:05:40 UTC — 129 · Workflow receipt

<a id="entry-130"></a>
## 2026-10-10 16:05:41 UTC — 130 · Jev routed the message

- **Actor:** Jev (jev-1.13.0 · 1682 in / 282 out tokens · 328 ms)
- **Tool:** TypeSafe `system_one` · step `route_case_messages`
- **Decision:** jev_route → `clarify` (confidence 0.53)
- **Signals:** hazard 0.09 · multiple_issues 0.14 · sensitive 0.05 · states_facts 0.11 · system_instructions 0.02
- **Why:** Jev routes; Claude extracts quotes and claims. clarify is not a Jev-only route. Route confidence 0.53 is below the Jev-only bar 0.8.

<a id="entry-131"></a>
## 2026-10-10 16:05:46 UTC — 131 · Claude read the message

- **Actor:** Claude (claude-opus-5 · 1805 in / 374 out tokens)
- **Tool:** Anthropic Messages API `ai.triage` (prompt property-triage-2026-10-10.3) · step `triage_case_messages`
- **Reading:** answer to question · route `clarify` · medium confidence
- **Work item:** Radiator heating cutting out intermittently (other)
- **Summary:** Tenant reports radiators still inconsistent with hot water still available, and supplies the boiler-label details. No return appointment has been agreed.
- **Rationale:** Tenant reply provides label details but the heating fault persists and authorisation/appointment remain unresolved; router chose clarify.
- **Extracted:** 1 claim · 2 ambiguities · 1 issue
- **Unknown:** No return appointment agreed; tenant's availability for a contractor revisit is unknown.
- **Unknown:** Tenant has not stated whether the contractor may be given access for a return visit.

<a id="entry-132"></a>
## 2026-10-10 16:05:46 UTC — 132 · Claim `completion` = false

- **Actor:** Claude (extracted)
- **Status:** unverified assertion — a person or policy must accept it

> Said the radiators were still inconsistent

<a id="entry-133"></a>
## 2026-10-10 16:05:46 UTC — 133 · Review superseded

- **Why:** Relevant evidence or current blockers changed; assess the current review.

<a id="entry-134"></a>
## 2026-10-10 16:05:46 UTC — 134 · Policy gates → HUMAN REVIEW

- **Actor:** Policy engine (rules v1, `domain.evaluate`)
- **Outcome:** HUMAN REVIEW · owner case manager
- **Blockers:** `identity` UNKNOWN → HUMAN REVIEW; `route` UNKNOWN → HUMAN REVIEW
- **Next step:** Verify the person, property and work item mapping.

<a id="entry-135"></a>
## 2026-10-10 16:05:46 UTC — 135 · Message received: Event 015 — Email from Ivo Merrick (Property Manager, Northbridge Lettings)

- **Recorded by:** demo-case_manager (case manager)
- **Reading:** queued for Jev routing / Claude triage

> Event 015 — Email
> From: Ivo Merrick (Property Manager, Northbridge Lettings)
> To: Petra Quill (Contractor, Copper Finch Mechanical)
>
> Asked for a repair alternative, confirmation of parts availability, a breakdown of the estimate and clarification of whether diagnosis would be credited. Repeated that no further work was authorized.

<a id="entry-136"></a>
## 2026-10-10 16:05:46 UTC — 136 · Policy gates → HUMAN REVIEW

- **Actor:** Policy engine (rules v1, `domain.evaluate`)
- **Outcome:** HUMAN REVIEW · owner case manager
- **Blockers:** `identity` UNKNOWN → HUMAN REVIEW; `route` UNKNOWN → HUMAN REVIEW; `triage` UNKNOWN → WAIT
- **Next step:** Verify the person, property and work item mapping.

<a id="entry-137"></a>
## 2026-10-10 16:05:46 UTC — 137 · Workflow receipt

<a id="entry-138"></a>
## 2026-10-10 16:05:46 UTC — 138 · Jev routed the message

- **Actor:** Jev (jev-1.13.0 · 1688 in / 282 out tokens · 332 ms)
- **Tool:** TypeSafe `system_one` · step `route_case_messages`
- **Decision:** jev_route → `clarify` (confidence 0.88)
- **Signals:** hazard 0.06 · multiple_issues 0.08 · sensitive 0.03 · states_facts 0.10 · system_instructions 0.02
- **Why:** Jev routes; Claude extracts quotes and claims. clarify is not a Jev-only route.

<a id="entry-139"></a>
## 2026-10-10 16:05:51 UTC — 139 · Claude read the message

- **Actor:** Claude (claude-opus-5 · 1731 in / 369 out tokens)
- **Tool:** Anthropic Messages API `ai.triage` (prompt property-triage-2026-10-10.3) · step `triage_case_messages`
- **Reading:** update · route `clarify` · high confidence
- **Work item:** Radiator heating cutting out intermittently (other)
- **Summary:** Property manager asked the contractor for a repair alternative, parts availability, an estimate breakdown and whether the diagnostic charge would be credited, and repeated that no further work is authorised.
- **Rationale:** Outstanding information is needed from the contractor before the quote can be decided; no authority given.
- **Extracted:** 1 claim · 1 ambiguity · 1 issue
- **Unknown:** Awaiting contractor's response on repair option, parts availability, cost breakdown and whether the £138 diagnostic charge is credited.

<a id="entry-140"></a>
## 2026-10-10 16:05:51 UTC — 140 · Policy gates → HUMAN REVIEW

- **Actor:** Policy engine (rules v1, `domain.evaluate`)
- **Outcome:** HUMAN REVIEW · owner case manager
- **Blockers:** `identity` UNKNOWN → HUMAN REVIEW; `route` UNKNOWN → HUMAN REVIEW
- **Next step:** Verify the person, property and work item mapping.

<a id="entry-141"></a>
## 2026-10-10 16:05:51 UTC — 141 · Message received: Event 016 — Email from Petra Quill (Contractor, Copper Finch Mechanical)

- **Recorded by:** demo-case_manager (case manager)
- **Reading:** queued for Jev routing / Claude triage

> Event 016 — Email
> From: Petra Quill (Contractor, Copper Finch Mechanical)
> To: Ivo Merrick (Property Manager, Northbridge Lettings)
>
> Replied that parts availability and estimate details still needed checking. Did not confirm a repair option, a credit, a return visit or completion of actuator work.

<a id="entry-142"></a>
## 2026-10-10 16:05:51 UTC — 142 · Policy gates → HUMAN REVIEW

- **Actor:** Policy engine (rules v1, `domain.evaluate`)
- **Outcome:** HUMAN REVIEW · owner case manager
- **Blockers:** `identity` UNKNOWN → HUMAN REVIEW; `route` UNKNOWN → HUMAN REVIEW; `triage` UNKNOWN → WAIT
- **Next step:** Verify the person, property and work item mapping.

<a id="entry-143"></a>
## 2026-10-10 16:05:51 UTC — 143 · Workflow receipt

<a id="entry-144"></a>
## 2026-10-10 16:05:52 UTC — 144 · Jev routed the message

- **Actor:** Jev (jev-1.13.0 · 1685 in / 284 out tokens · 284 ms)
- **Tool:** TypeSafe `system_one` · step `route_case_messages`
- **Decision:** jev_route → `clarify` (confidence 0.87)
- **Signals:** hazard 0.05 · multiple_issues 0.07 · sensitive 0.03 · states_facts 0.06 · system_instructions 0.02
- **Why:** Jev routes; Claude extracts quotes and claims. clarify is not a Jev-only route.

<a id="entry-145"></a>
## 2026-10-10 16:05:57 UTC — 145 · Claude read the message

- **Actor:** Claude (claude-opus-5 · 1696 in / 362 out tokens)
- **Tool:** Anthropic Messages API `ai.triage` (prompt property-triage-2026-10-10.3) · step `triage_case_messages`
- **Reading:** update · route `clarify` · high confidence
- **Work item:** Radiator heating cutting out intermittently (other)
- **Summary:** Contractor replied that parts availability and estimate details still need checking; no repair option, credit, return visit or completion confirmed.
- **Rationale:** Contractor response leaves the key estimate and repair questions unresolved, so the item cannot progress to instruction or quote approval yet.
- **Extracted:** 0 claims · 2 ambiguities · 1 issue
- **Unknown (affects route):** Contractor has not confirmed whether a repair alternative to replacement is possible, parts availability, or an itemised estimate breakdown including whether diagnosis is credited.
- **Unknown:** No return visit date proposed by the contractor.

<a id="entry-146"></a>
## 2026-10-10 16:05:57 UTC — 146 · Human review opened: `triage`

- **Actor:** Policy engine
- **Owner:** case manager · rule `require-triage`
- **Expires:** 2026-10-12 16:05:57 UTC

> Clarify before routing: Contractor has not confirmed whether a repair alternative to replacement is possible, parts availability, or an itemised estimate breakdown including whether diagnosis is credited. A verified route is required before asking externally.

<a id="entry-147"></a>
## 2026-10-10 16:05:57 UTC — 147 · Policy gates → HUMAN REVIEW

- **Actor:** Policy engine (rules v1, `domain.evaluate`)
- **Outcome:** HUMAN REVIEW · owner case manager
- **Blockers:** `identity` UNKNOWN → HUMAN REVIEW; `route` UNKNOWN → HUMAN REVIEW; `triage` UNKNOWN → HUMAN REVIEW
- **Next step:** Verify the person, property and work item mapping.

<a id="entry-148"></a>
## 2026-10-10 16:05:57 UTC — 148 · Message received: Event 017 — Email from Petra Quill (Contractor, Copper Finch Mechanical)

- **Recorded by:** demo-case_manager (case manager)
- **Reading:** queued for Jev routing / Claude triage

> Event 017 — Email
> From: Petra Quill (Contractor, Copper Finch Mechanical)
> To: Ivo Merrick (Property Manager, Northbridge Lettings)
>
> Sent two invoice records dated 10 February and said they had been prepared from the job paperwork. The message did not say whether one replaced the other, whether both amounts were payable, or whether either had been paid. Invoice B describes actuator work as completed and gives a service date of 5 February, but Petra did not attach a signed completion record or explain how that claim relates to the estimate sent later on 5 February and the 7 February parts check.

<a id="entry-149"></a>
## 2026-10-10 16:05:57 UTC — 149 · Policy gates → HUMAN REVIEW

- **Actor:** Policy engine (rules v1, `domain.evaluate`)
- **Outcome:** HUMAN REVIEW · owner case manager
- **Blockers:** `identity` UNKNOWN → HUMAN REVIEW; `route` UNKNOWN → HUMAN REVIEW; `triage` UNKNOWN → WAIT
- **Next step:** Verify the person, property and work item mapping.

<a id="entry-150"></a>
## 2026-10-10 16:05:57 UTC — 150 · Workflow receipt

<a id="entry-151"></a>
## 2026-10-10 16:05:58 UTC — 151 · Jev routed the message

- **Actor:** Jev (jev-1.13.0 · 1746 in / 284 out tokens · 276 ms)
- **Tool:** TypeSafe `system_one` · step `route_case_messages`
- **Decision:** jev_route → `clarify` (confidence 0.89)
- **Signals:** hazard 0.06 · multiple_issues 0.08 · sensitive 0.04 · states_facts 0.73 · system_instructions 0.02
- **Why:** Jev routes; Claude extracts quotes and claims. clarify is not a Jev-only route. The message may state facts that need exact quotes.

<a id="entry-152"></a>
## 2026-10-10 16:06:04 UTC — 152 · Claude read the message

- **Actor:** Claude (claude-opus-5 · 1857 in / 524 out tokens)
- **Tool:** Anthropic Messages API `ai.triage` (prompt property-triage-2026-10-10.3) · step `triage_case_messages`
- **Reading:** update · route `clarify` · medium confidence
- **Work item:** Radiator heating cutting out intermittently (other)
- **Summary:** Contractor sent two invoice records dated 10 February without stating whether one supersedes the other, whether both are payable, or whether either is paid. Invoice B claims actuator work completed on 5 February but no signed completion record was provided and it conflicts with the later estimate and 7 February parts check.
- **Rationale:** Conflicting invoice and completion claims with no evidence or amounts; cannot act until contractor clarifies.
- **Extracted:** 1 claim · 2 ambiguities · 1 issue
- **Unknown (affects route):** Invoice B claims actuator work completed on 5 February but no signed completion record and it conflicts with the estimate sent later that day and the 7 February parts check.
- **Unknown (affects route):** Two invoices dated 10 February: unclear whether one replaces the other, whether both amounts are payable, or whether either has been paid. No totals stated.

<a id="entry-153"></a>
## 2026-10-10 16:06:04 UTC — 153 · Claim `completion` = true

- **Actor:** Claude (extracted)
- **Status:** unverified assertion — a person or policy must accept it

> Invoice B describes actuator work as completed and gives a service date of 5 February

<a id="entry-154"></a>
## 2026-10-10 16:06:04 UTC — 154 · Policy gates → HUMAN REVIEW

- **Actor:** Policy engine (rules v1, `domain.evaluate`)
- **Outcome:** HUMAN REVIEW · owner case manager
- **Blockers:** `identity` UNKNOWN → HUMAN REVIEW; `route` UNKNOWN → HUMAN REVIEW; `triage` UNKNOWN → HUMAN REVIEW
- **Next step:** Verify the person, property and work item mapping.

<a id="entry-155"></a>
## 2026-10-10 16:06:05 UTC — 155 · Message received: Event 018 — Document from Petra Quill (Contractor, Copper Finch Mechanical)

- **Recorded by:** demo-case_manager (case manager)
- **Reading:** queued for Jev routing / Claude triage

> Event 018 — Document
> From: Petra Quill (Contractor, Copper Finch Mechanical)
> To: Ivo Merrick (Property Manager, Northbridge Lettings)
>
> The received invoice records list £138 for attendance, diagnosis, actuator inspection and an operational test, and £372 for actuator supply/replacement, attendance, diagnosis and heating-system testing. Both records identify 5 February as the service date. The second record's wider description includes activities also listed on the first; neither record states whether the other is credited, cancelled or superseded.

<a id="entry-156"></a>
## 2026-10-10 16:06:05 UTC — 156 · Policy gates → HUMAN REVIEW

- **Actor:** Policy engine (rules v1, `domain.evaluate`)
- **Outcome:** HUMAN REVIEW · owner case manager
- **Blockers:** `identity` UNKNOWN → HUMAN REVIEW; `route` UNKNOWN → HUMAN REVIEW; `triage` UNKNOWN → WAIT
- **Next step:** Verify the person, property and work item mapping.

<a id="entry-157"></a>
## 2026-10-10 16:06:05 UTC — 157 · Workflow receipt

<a id="entry-158"></a>
## 2026-10-10 16:06:05 UTC — 158 · Jev routed the message

- **Actor:** Jev (jev-1.13.0 · 1802 in / 282 out tokens · 285 ms)
- **Tool:** TypeSafe `system_one` · step `route_case_messages`
- **Decision:** jev_route → `clarify` (confidence 0.97)
- **Signals:** hazard 0.05 · multiple_issues 0.06 · sensitive 0.03 · states_facts 0.95 · system_instructions 0.02
- **Why:** Jev routes; Claude extracts quotes and claims. clarify is not a Jev-only route. The message may state facts that need exact quotes.

<a id="entry-159"></a>
## 2026-10-10 16:06:12 UTC — 159 · Claude read the message

- **Actor:** Claude (claude-opus-5 · 1987 in / 602 out tokens)
- **Tool:** Anthropic Messages API `ai.triage` (prompt property-triage-2026-10-10.3) · step `triage_case_messages`
- **Reading:** update · route `clarify` · high confidence
- **Work item:** Radiator heating cutting out intermittently (other)
- **Summary:** Contractor document lists two invoice records for 5 February service: £138 for attendance/diagnosis/inspection/test and £372 for actuator supply/replacement plus overlapping activities. Neither record states whether one supersedes or credits the other, so the payable total remains unclear.
- **Rationale:** Invoice amounts stated but payability, duplication and VAT status unclear, and completion evidence still conflicts; clarification needed before any authority or closure.
- **Extracted:** 2 claims · 2 ambiguities · 1 issue
- **Unknown (affects route):** Whether the two invoice records are cumulative or one supersedes the other; the overlapping activities suggest possible duplication, and no payable total including tax is stated.
- **Unknown (affects route):** Both records cite 5 February as the service date, but actuator replacement conflicts with the estimate sent later that day and the 7 February parts check; no signed completion record supplied.

<a id="entry-160"></a>
## 2026-10-10 16:06:12 UTC — 160 · Claim `total` = 138.0

- **Actor:** Claude (extracted)
- **Status:** unverified assertion — a person or policy must accept it

> The received invoice records list £138 for attendance, diagnosis, actuator inspection and an operational test

<a id="entry-161"></a>
## 2026-10-10 16:06:12 UTC — 161 · Claim `total` = 372.0

- **Actor:** Claude (extracted)
- **Status:** unverified assertion — a person or policy must accept it

> £372 for actuator supply/replacement, attendance, diagnosis and heating-system testing

<a id="entry-162"></a>
## 2026-10-10 16:06:13 UTC — 162 · Policy gates → HUMAN REVIEW

- **Actor:** Policy engine (rules v1, `domain.evaluate`)
- **Outcome:** HUMAN REVIEW · owner case manager
- **Blockers:** `identity` UNKNOWN → HUMAN REVIEW; `route` UNKNOWN → HUMAN REVIEW; `triage` UNKNOWN → HUMAN REVIEW
- **Next step:** Verify the person, property and work item mapping.

<a id="entry-163"></a>
## 2026-10-10 16:06:13 UTC — 163 · Message received: Event 019 — Note from Ivo Merrick (Property Manager, Northbridge Lettings)

- **Recorded by:** demo-case_manager (case manager)
- **Reading:** queued for Jev routing / Claude triage

> Event 019 — Note
> From: Ivo Merrick (Property Manager, Northbridge Lettings)
> To: Ivo Merrick (Property Manager, Northbridge Lettings)
>
> Compared the received records with the file: the landlord's written authority covers diagnosis only; the £372 estimate requesting authorization was sent after the stated service date; and the 7 February exchange still had parts and estimate details outstanding. The file contains no written authorization for actuator replacement and no return-visit or completion entry.

<a id="entry-164"></a>
## 2026-10-10 16:06:13 UTC — 164 · Policy gates → HUMAN REVIEW

- **Actor:** Policy engine (rules v1, `domain.evaluate`)
- **Outcome:** HUMAN REVIEW · owner case manager
- **Blockers:** `identity` UNKNOWN → HUMAN REVIEW; `route` UNKNOWN → HUMAN REVIEW; `triage` UNKNOWN → WAIT
- **Next step:** Verify the person, property and work item mapping.

<a id="entry-165"></a>
## 2026-10-10 16:06:13 UTC — 165 · Workflow receipt

<a id="entry-166"></a>
## 2026-10-10 16:06:13 UTC — 166 · Jev routed the message

- **Actor:** Jev (jev-1.13.0 · 1840 in / 282 out tokens · 252 ms)
- **Tool:** TypeSafe `system_one` · step `route_case_messages`
- **Decision:** jev_route → `clarify` (confidence 0.98)
- **Signals:** hazard 0.04 · multiple_issues 0.05 · sensitive 0.03 · states_facts 0.89 · system_instructions 0.02
- **Why:** Jev routes; Claude extracts quotes and claims. clarify is not a Jev-only route. The message may state facts that need exact quotes.

<a id="entry-167"></a>
## 2026-10-10 16:06:20 UTC — 167 · Claude read the message

- **Actor:** Claude (claude-opus-5 · 2069 in / 478 out tokens)
- **Tool:** Anthropic Messages API `ai.triage` (prompt property-triage-2026-10-10.3) · step `triage_case_messages`
- **Reading:** update · route `clarify` · high confidence
- **Work item:** Radiator heating cutting out intermittently (other)
- **Summary:** Internal file note from the property manager recording that landlord authority covers diagnosis only, that the £372 estimate post-dates the stated service date, and that the file holds no written authorisation for actuator replacement and no completion or return-visit entry.
- **Rationale:** Internal note disputing authority and completion evidence; billing and completion facts unresolved, so clarification is needed before any instruction or payment.
- **Extracted:** 2 claims · 2 ambiguities · 1 issue
- **Unknown (affects route):** Whether the two invoice records are cumulative or one supersedes the other; no payable total including tax is stated.
- **Unknown (affects route):** Whether actuator replacement was ever carried out, given the £372 estimate was sent after the stated service date and no completion record exists.

<a id="entry-168"></a>
## 2026-10-10 16:06:20 UTC — 168 · Claim `completion` = false

- **Actor:** Claude (extracted)
- **Status:** unverified assertion — a person or policy must accept it

> no return-visit or completion entry

<a id="entry-169"></a>
## 2026-10-10 16:06:20 UTC — 169 · Policy gates → HUMAN REVIEW

- **Actor:** Policy engine (rules v1, `domain.evaluate`)
- **Outcome:** HUMAN REVIEW · owner case manager
- **Blockers:** `identity` UNKNOWN → HUMAN REVIEW; `route` UNKNOWN → HUMAN REVIEW; `triage` UNKNOWN → HUMAN REVIEW
- **Next step:** Verify the person, property and work item mapping.

<a id="entry-170"></a>
## 2026-10-10 16:06:21 UTC — 170 · Message received: Event 020 — Portal from Tessa Vane (Tenant)

- **Recorded by:** demo-case_manager (case manager)
- **Reading:** queued for Jev routing / Claude triage

> Event 020 — Portal
> From: Tessa Vane (Tenant)
> To: Ivo Merrick (Property Manager, Northbridge Lettings)
>
> Said she recalled the 5 February visit but did not know whether the actuator had been replaced. She had not seen a contractor at the property since that visit. Heating was currently working intermittently, with one radiator cooler than the others.

<a id="entry-171"></a>
## 2026-10-10 16:06:21 UTC — 171 · Policy gates → HUMAN REVIEW

- **Actor:** Policy engine (rules v1, `domain.evaluate`)
- **Outcome:** HUMAN REVIEW · owner case manager
- **Blockers:** `identity` UNKNOWN → HUMAN REVIEW; `route` UNKNOWN → HUMAN REVIEW; `triage` UNKNOWN → WAIT
- **Next step:** Verify the person, property and work item mapping.

<a id="entry-172"></a>
## 2026-10-10 16:06:21 UTC — 172 · Workflow receipt

<a id="entry-173"></a>
## 2026-10-10 16:06:22 UTC — 173 · Jev routed the message

- **Actor:** Jev (jev-1.13.0 · 1850 in / 282 out tokens · 385 ms)
- **Tool:** TypeSafe `system_one` · step `route_case_messages`
- **Decision:** jev_route → `clarify` (confidence 0.58)
- **Signals:** hazard 0.07 · multiple_issues 0.08 · sensitive 0.06 · states_facts 0.62 · system_instructions 0.02
- **Why:** Jev routes; Claude extracts quotes and claims. clarify is not a Jev-only route. Route confidence 0.58 is below the Jev-only bar 0.8. The message may state facts that need exact quotes.

<a id="entry-174"></a>
## 2026-10-10 16:06:27 UTC — 174 · Claude read the message

- **Actor:** Claude (claude-opus-5 · 2078 in / 412 out tokens)
- **Tool:** Anthropic Messages API `ai.triage` (prompt property-triage-2026-10-10.3) · step `triage_case_messages`
- **Reading:** answer to question · route `clarify` · medium confidence
- **Work item:** Radiator heating cutting out intermittently (other)
- **Summary:** Tenant confirms she recalls the 5 February visit but cannot say whether the actuator was replaced, and has seen no contractor since. Heating still works only intermittently with one radiator cooler than the rest.
- **Rationale:** Completion of the invoiced actuator work remains unverified and the fault persists; clarification needed before authorising or paying.
- **Extracted:** 1 claim · 2 ambiguities · 1 issue
- **Unknown (affects route):** Tenant cannot confirm whether actuator replacement was carried out; no return visit observed since 5 February.
- **Unknown:** Which radiator is cooler and whether hot water remains unaffected.

<a id="entry-175"></a>
## 2026-10-10 16:06:27 UTC — 175 · Claim `completion` = false

- **Actor:** Claude (extracted)
- **Status:** unverified assertion — a person or policy must accept it

> Heating was currently working intermittently, with one radiator cooler than the others.

<a id="entry-176"></a>
## 2026-10-10 16:06:27 UTC — 176 · Policy gates → HUMAN REVIEW

- **Actor:** Policy engine (rules v1, `domain.evaluate`)
- **Outcome:** HUMAN REVIEW · owner case manager
- **Blockers:** `identity` UNKNOWN → HUMAN REVIEW; `route` UNKNOWN → HUMAN REVIEW; `triage` UNKNOWN → HUMAN REVIEW
- **Next step:** Verify the person, property and work item mapping.

<a id="entry-177"></a>
## 2026-10-10 16:06:28 UTC — 177 · Message received: Event 021 — Email from Ivo Merrick (Property Manager, Northbridge Lettings)

- **Recorded by:** demo-case_manager (case manager)
- **Reading:** queued for Jev routing / Claude triage

> Event 021 — Email
> From: Ivo Merrick (Property Manager, Northbridge Lettings)
> To: Petra Quill (Contractor, Copper Finch Mechanical)
>
> Asked what work was actually completed and on what date, whether both invoice records remained current, whether either superseded the other, and how the overlapping charges were treated. Requested the job notes, any parts record and any authorization or attendance evidence for actuator work.

<a id="entry-178"></a>
## 2026-10-10 16:06:28 UTC — 178 · Policy gates → HUMAN REVIEW

- **Actor:** Policy engine (rules v1, `domain.evaluate`)
- **Outcome:** HUMAN REVIEW · owner case manager
- **Blockers:** `identity` UNKNOWN → HUMAN REVIEW; `route` UNKNOWN → HUMAN REVIEW; `triage` UNKNOWN → WAIT
- **Next step:** Verify the person, property and work item mapping.

<a id="entry-179"></a>
## 2026-10-10 16:06:28 UTC — 179 · Workflow receipt

<a id="entry-180"></a>
## 2026-10-10 16:06:28 UTC — 180 · Jev routed the message

- **Actor:** Jev (jev-1.13.0 · 1816 in / 282 out tokens · 255 ms)
- **Tool:** TypeSafe `system_one` · step `route_case_messages`
- **Decision:** jev_route → `clarify` (confidence 0.66)
- **Signals:** hazard 0.05 · multiple_issues 0.06 · sensitive 0.05 · states_facts 0.18 · system_instructions 0.02
- **Why:** Jev routes; Claude extracts quotes and claims. clarify is not a Jev-only route. Route confidence 0.66 is below the Jev-only bar 0.8.

<a id="entry-181"></a>
## 2026-10-10 16:06:35 UTC — 181 · Claude read the message

- **Actor:** Claude (claude-opus-5 · 2064 in / 412 out tokens)
- **Tool:** Anthropic Messages API `ai.triage` (prompt property-triage-2026-10-10.3) · step `triage_case_messages`
- **Reading:** update · route `clarify` · high confidence
- **Work item:** Radiator heating cutting out intermittently (other)
- **Summary:** Ivo Merrick asked the contractor to confirm what work was actually completed and when, whether both invoice records remain current or one supersedes the other, how overlapping charges are treated, and requested job notes, parts records and authorisation or attendance evidence for the actuator work.
- **Rationale:** Agent is chasing missing completion, billing and authorisation evidence; item cannot progress until the contractor answers.
- **Extracted:** 0 claims · 2 ambiguities · 1 issue
- **Unknown (affects route):** What actuator work was actually done and on what date remains unconfirmed; no job notes, parts record or attendance evidence received.
- **Unknown:** Whether both invoice records are payable or one supersedes the other, and how overlapping charges are handled, is unresolved.

<a id="entry-182"></a>
## 2026-10-10 16:06:35 UTC — 182 · Policy gates → HUMAN REVIEW

- **Actor:** Policy engine (rules v1, `domain.evaluate`)
- **Outcome:** HUMAN REVIEW · owner case manager
- **Blockers:** `identity` UNKNOWN → HUMAN REVIEW; `route` UNKNOWN → HUMAN REVIEW; `triage` UNKNOWN → HUMAN REVIEW
- **Next step:** Verify the person, property and work item mapping.

<a id="entry-183"></a>
## 2026-10-10 16:06:35 UTC — 183 · Message received: Event 022 — Email from Petra Quill (Contractor, Copper Finch Mechanical)

- **Recorded by:** demo-case_manager (case manager)
- **Reading:** queued for Jev routing / Claude triage

> Event 022 — Email
> From: Petra Quill (Contractor, Copper Finch Mechanical)
> To: Ivo Merrick (Property Manager, Northbridge Lettings)
>
> Replied that she was checking the records and could not yet confirm whether the invoice entries represented separate chargeable work or whether one record replaced the other. She supplied no further completion evidence, revised invoice or parts confirmation.

<a id="entry-184"></a>
## 2026-10-10 16:06:35 UTC — 184 · Policy gates → HUMAN REVIEW

- **Actor:** Policy engine (rules v1, `domain.evaluate`)
- **Outcome:** HUMAN REVIEW · owner case manager
- **Blockers:** `identity` UNKNOWN → HUMAN REVIEW; `route` UNKNOWN → HUMAN REVIEW; `triage` UNKNOWN → WAIT
- **Next step:** Verify the person, property and work item mapping.

<a id="entry-185"></a>
## 2026-10-10 16:06:35 UTC — 185 · Workflow receipt

<a id="entry-186"></a>
## 2026-10-10 16:06:36 UTC — 186 · Jev routed the message

- **Actor:** Jev (jev-1.13.0 · 1778 in / 282 out tokens · 262 ms)
- **Tool:** TypeSafe `system_one` · step `route_case_messages`
- **Decision:** jev_route → `clarify` (confidence 0.92)
- **Signals:** hazard 0.05 · multiple_issues 0.05 · sensitive 0.03 · states_facts 0.07 · system_instructions 0.02
- **Why:** Jev routes; Claude extracts quotes and claims. clarify is not a Jev-only route.

<a id="entry-187"></a>
## 2026-10-10 16:06:41 UTC — 187 · Claude read the message

- **Actor:** Claude (claude-opus-5 · 2052 in / 388 out tokens)
- **Tool:** Anthropic Messages API `ai.triage` (prompt property-triage-2026-10-10.3) · step `triage_case_messages`
- **Reading:** update · route `clarify` · high confidence
- **Work item:** Radiator heating cutting out intermittently (other)
- **Summary:** Contractor replied that she is still checking records and cannot yet confirm whether the two invoice entries are separate chargeable work or whether one supersedes the other. No completion evidence, revised invoice or parts confirmation supplied.
- **Rationale:** Contractor has not answered the outstanding questions; essential billing and completion information still missing, so the item stays at clarify.
- **Extracted:** 0 claims · 2 ambiguities · 1 issue
- **Unknown:** Whether the two invoice records are both payable or one supersedes the other is still unconfirmed.
- **Unknown (affects route):** What actuator work was done and on what date remains unevidenced; no job notes, parts record or attendance evidence supplied.

<a id="entry-188"></a>
## 2026-10-10 16:06:41 UTC — 188 · Policy gates → HUMAN REVIEW

- **Actor:** Policy engine (rules v1, `domain.evaluate`)
- **Outcome:** HUMAN REVIEW · owner case manager
- **Blockers:** `identity` UNKNOWN → HUMAN REVIEW; `route` UNKNOWN → HUMAN REVIEW; `triage` UNKNOWN → HUMAN REVIEW
- **Next step:** Verify the person, property and work item mapping.

<a id="entry-189"></a>
## 2026-10-10 16:06:41 UTC — 189 · Message received: Event 023 — Email from Ivo Merrick (Property Manager, Northbridge Lettings)

- **Recorded by:** demo-case_manager (case manager)
- **Reading:** queued for Jev routing / Claude triage

> Event 023 — Email
> From: Ivo Merrick (Property Manager, Northbridge Lettings)
> To: Soren Dallow (Landlord)
>
> The two invoice records remain on file; there is no recorded payment, confirmed supersession or authorization for actuator work. The tenant reports intermittent heating and has not confirmed replacement. Please advise how you wish to proceed on the unresolved records and whether any further work or expenditure is authorized.

<a id="entry-190"></a>
## 2026-10-10 16:06:41 UTC — 190 · Policy gates → HUMAN REVIEW

- **Actor:** Policy engine (rules v1, `domain.evaluate`)
- **Outcome:** HUMAN REVIEW · owner case manager
- **Blockers:** `identity` UNKNOWN → HUMAN REVIEW; `route` UNKNOWN → HUMAN REVIEW; `triage` UNKNOWN → WAIT
- **Next step:** Verify the person, property and work item mapping.

<a id="entry-191"></a>
## 2026-10-10 16:06:42 UTC — 191 · Workflow receipt

<a id="entry-192"></a>
## 2026-10-10 16:06:42 UTC — 192 · Jev routed the message

- **Actor:** Jev (jev-1.13.0 · 1762 in / 282 out tokens · 369 ms)
- **Tool:** TypeSafe `system_one` · step `route_case_messages`
- **Decision:** jev_route → `clarify` (confidence 0.79)
- **Signals:** hazard 0.08 · multiple_issues 0.07 · sensitive 0.04 · states_facts 0.25 · system_instructions 0.01
- **Why:** Jev routes; Claude extracts quotes and claims. clarify is not a Jev-only route. Route confidence 0.79 is below the Jev-only bar 0.8.

<a id="entry-193"></a>
## 2026-10-10 16:06:48 UTC — 193 · Claude read the message

- **Actor:** Claude (claude-opus-5 · 2114 in / 393 out tokens)
- **Tool:** Anthropic Messages API `ai.triage` (prompt property-triage-2026-10-10.3) · step `triage_case_messages`
- **Reading:** update · route `clarify` · high confidence
- **Work item:** Radiator heating cutting out intermittently (other)
- **Summary:** Property manager updates the landlord that two unreconciled invoice records remain on file with no payment, supersession or authority for actuator work, and the tenant still reports intermittent heating. He asks the landlord how to proceed and whether further work or expenditure is authorised.
- **Rationale:** Internal/landlord-facing update seeking instructions; invoice reconciliation and authority unresolved, so clarify matches the router decision.
- **Extracted:** 0 claims · 2 ambiguities · 1 issue
- **Unknown (affects route):** Whether actuator replacement was actually carried out, on what date, and which invoice record (if either) is payable remains unevidenced.
- **Unknown (affects route):** No completion evidence or authorisation for actuator work on file; landlord's decision on further work/expenditure is pending.

<a id="entry-194"></a>
## 2026-10-10 16:06:48 UTC — 194 · Policy gates → HUMAN REVIEW

- **Actor:** Policy engine (rules v1, `domain.evaluate`)
- **Outcome:** HUMAN REVIEW · owner case manager
- **Blockers:** `identity` UNKNOWN → HUMAN REVIEW; `route` UNKNOWN → HUMAN REVIEW; `triage` UNKNOWN → HUMAN REVIEW
- **Next step:** Verify the person, property and work item mapping.

<a id="entry-195"></a>
## 2026-10-10 16:06:48 UTC — 195 · Message received: Attachment invoice-NBL-CFM-250210-A.pdf (PDF text extraction)

- **Recorded by:** demo-case_manager (case manager)
- **Reading:** queued for Jev routing / Claude triage

> Attachment: invoice-NBL-CFM-250210-A.pdf
> Extracted text (pypdf; layout not preserved):
>
> BILLING DOCUMENT Copper Finch Mechanical — Invoice NBL-CFM-
> 250210-A
> Copper Finch Mechanical
> Invoice reference: NBL-CFM-250210-A
> Invoice date: 10 February 2025
> Customer: Northbridge Lettings
> Service address: 7 Larkspur Fold, Orvane Heath, ZZ1 1ZZ
> Service date: 5 February 2025
> Work invoiced
> Attendance, fault diagnosis, heating valve actuator inspection and operational test.
> Total including VAT: £138.00
> Payment terms: 14 days

<a id="entry-196"></a>
## 2026-10-10 16:06:48 UTC — 196 · Policy gates → HUMAN REVIEW

- **Actor:** Policy engine (rules v1, `domain.evaluate`)
- **Outcome:** HUMAN REVIEW · owner case manager
- **Blockers:** `identity` UNKNOWN → HUMAN REVIEW; `route` UNKNOWN → HUMAN REVIEW; `triage` UNKNOWN → WAIT
- **Next step:** Verify the person, property and work item mapping.

<a id="entry-197"></a>
## 2026-10-10 16:06:48 UTC — 197 · Workflow receipt

<a id="entry-198"></a>
## 2026-10-10 16:06:49 UTC — 198 · Jev routed the message

- **Actor:** Jev (jev-1.13.0 · 1847 in / 282 out tokens · 481 ms)
- **Tool:** TypeSafe `system_one` · step `route_case_messages`
- **Decision:** jev_route → `clarify` (confidence 0.63)
- **Signals:** hazard 0.08 · multiple_issues 0.05 · sensitive 0.05 · states_facts 0.94 · system_instructions 0.04
- **Why:** Jev routes; Claude extracts quotes and claims. clarify is not a Jev-only route. Route confidence 0.63 is below the Jev-only bar 0.8. The message may state facts that need exact quotes.

<a id="entry-199"></a>
## 2026-10-10 16:06:56 UTC — 199 · Claude read the message

- **Actor:** Claude (claude-opus-5 · 2223 in / 439 out tokens)
- **Tool:** Anthropic Messages API `ai.triage` (prompt property-triage-2026-10-10.3) · step `triage_case_messages`
- **Reading:** update · route `clarify` · medium confidence
- **Work item:** Radiator heating cutting out intermittently (other)
- **Summary:** Invoice document NBL-CFM-250210-A from Copper Finch Mechanical for £138.00 including VAT, covering attendance, diagnosis, actuator inspection and operational test on 5 February 2025 at the case property. It does not state whether it supersedes or is superseded by the £372 record.
- **Rationale:** Billing document adds the £138 total but leaves supersession, authorisation and completion unevidenced; clarification still required.
- **Extracted:** 1 claim · 2 ambiguities · 1 issue
- **Unknown (affects route):** The invoice does not state whether it replaces or is replaced by the £372 record, so which record is payable remains unresolved.
- **Unknown (affects route):** No statement that actuator replacement was carried out; invoice covers inspection and test only.

<a id="entry-200"></a>
## 2026-10-10 16:06:56 UTC — 200 · Claim `total` = 138.0

- **Actor:** Claude (extracted)
- **Status:** unverified assertion — a person or policy must accept it

> Total including VAT: £138.00

<a id="entry-201"></a>
## 2026-10-10 16:06:56 UTC — 201 · Policy gates → HUMAN REVIEW

- **Actor:** Policy engine (rules v1, `domain.evaluate`)
- **Outcome:** HUMAN REVIEW · owner case manager
- **Blockers:** `identity` UNKNOWN → HUMAN REVIEW; `route` UNKNOWN → HUMAN REVIEW; `triage` UNKNOWN → HUMAN REVIEW
- **Next step:** Verify the person, property and work item mapping.

<a id="entry-202"></a>
## 2026-10-10 16:06:56 UTC — 202 · Message received: Attachment invoice-NBL-CFM-250210-B.pdf (PDF text extraction)

- **Recorded by:** demo-case_manager (case manager)
- **Reading:** queued for Jev routing / Claude triage

> Attachment: invoice-NBL-CFM-250210-B.pdf
> Extracted text (pypdf; layout not preserved):
>
> BILLING DOCUMENT Copper Finch Mechanical — Invoice NBL-CFM-
> 250210-B
> Copper Finch Mechanical
> Invoice reference: NBL-CFM-250210-B
> Invoice date: 10 February 2025
> Customer: Northbridge Lettings
> Service address: 7 Larkspur Fold, Orvane Heath, ZZ1 1ZZ
> Service date: 5 February 2025
> Work invoiced
> Heating valve actuator supply and replacement, attendance, fault diagnosis and heating-
> system testing.
> Total including VAT: £372.00
> Payment terms: 14 days

<a id="entry-203"></a>
## 2026-10-10 16:06:56 UTC — 203 · Policy gates → HUMAN REVIEW

- **Actor:** Policy engine (rules v1, `domain.evaluate`)
- **Outcome:** HUMAN REVIEW · owner case manager
- **Blockers:** `identity` UNKNOWN → HUMAN REVIEW; `route` UNKNOWN → HUMAN REVIEW; `triage` UNKNOWN → WAIT
- **Next step:** Verify the person, property and work item mapping.

<a id="entry-204"></a>
## 2026-10-10 16:06:56 UTC — 204 · Workflow receipt

<a id="entry-205"></a>
## 2026-10-10 16:06:56 UTC — 205 · Jev routed the message

- **Actor:** Jev (jev-1.13.0 · 1920 in / 282 out tokens · 227 ms)
- **Tool:** TypeSafe `system_one` · step `route_case_messages`
- **Decision:** jev_route → `clarify` (confidence 0.79)
- **Signals:** hazard 0.08 · multiple_issues 0.06 · sensitive 0.03 · states_facts 0.94 · system_instructions 0.03
- **Why:** Jev routes; Claude extracts quotes and claims. clarify is not a Jev-only route. Route confidence 0.79 is below the Jev-only bar 0.8. The message may state facts that need exact quotes.

<a id="entry-206"></a>
## 2026-10-10 16:07:04 UTC — 206 · Claude read the message

- **Actor:** Claude (claude-opus-5 · 2289 in / 566 out tokens)
- **Tool:** Anthropic Messages API `ai.triage` (prompt property-triage-2026-10-10.3) · step `triage_case_messages`
- **Reading:** update · route `clarify` · medium confidence
- **Work item:** Radiator heating cutting out intermittently (other)
- **Summary:** Second Copper Finch Mechanical invoice (NBL-CFM-250210-B) for the same 5 February service date, totalling £372.00 including VAT, covering actuator supply and replacement plus diagnosis and testing. It does not state whether it supersedes the £138.00 invoice, and no authorisation or completion evidence is provided.
- **Rationale:** Billing document raising unresolved duplicate-invoice, authority and completion questions; cannot be actioned until the record position is clarified.
- **Extracted:** 1 claim · 3 ambiguities · 1 issue
- **Unknown (affects route):** This invoice covers the same 5 February service date as invoice NBL-CFM-250210-A (£138.00); it is not stated whether it supersedes that record or is separate chargeable work.
- **Unknown (affects route):** No completion evidence, parts record or attendance proof for the actuator replacement is supplied, and the tenant reports heating still intermittent.
- **Unknown (affects route):** No written landlord authorisation on file for actuator replacement; authority for the £372.00 spend is unconfirmed.

<a id="entry-207"></a>
## 2026-10-10 16:07:04 UTC — 207 · Claim `total` = 372.0

- **Actor:** Claude (extracted)
- **Status:** unverified assertion — a person or policy must accept it

> Total including VAT: £372.00

<a id="entry-208"></a>
## 2026-10-10 16:07:04 UTC — 208 · Policy gates → HUMAN REVIEW

- **Actor:** Policy engine (rules v1, `domain.evaluate`)
- **Outcome:** HUMAN REVIEW · owner case manager
- **Blockers:** `identity` UNKNOWN → HUMAN REVIEW; `route` UNKNOWN → HUMAN REVIEW; `triage` UNKNOWN → HUMAN REVIEW
- **Next step:** Verify the person, property and work item mapping.
