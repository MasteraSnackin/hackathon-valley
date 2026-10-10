# Case 905bdba959da audit trail

Heating maintenance at 7 Larkspur Fold · 7 Larkspur Fold, Orvane Heath, ZZ1 1ZZ · status open · stage WAIT

- **Case ID:** `905bdba959da4e6f804f66c51c6d8092`
- **Entries:** 186 (from 628 immutable records; bookkeeping and unchanged assessments omitted)
- **Raw records:** [records.jsonl](records.jsonl)
- All outbound tools are simulated adapters; no real tenant, landlord or contractor was contacted.

<a id="entry-001"></a>
## 2026-10-10 16:26:03 UTC — 001 · Message received: Intake report

- **Recorded by:** demo-case_manager (case manager)
- **Reading:** queued for Jev routing / Claude triage

> Event 001 — Portal
> From: Tessa Vane (Tenant)
> To: Ivo Merrick (Property Manager, Northbridge Lettings)
>
> Reported that radiator heating had cut out twice since the previous evening while hot water remained available. A child lives at the property. Asked for an inspection.

<a id="entry-002"></a>
## 2026-10-10 16:26:03 UTC — 002 · Policy gates → WAIT

- **Actor:** Policy engine (rules v2, `domain.evaluate`)
- **Outcome:** WAIT · owner case manager
- **Blockers:** `triage` UNKNOWN → WAIT
- **Next step:** The latest message is being routed and read. Actions wait for the reading.

<a id="entry-003"></a>
## 2026-10-10 16:26:03 UTC — 003 · Workflow receipt

<a id="entry-004"></a>
## 2026-10-10 16:26:04 UTC — 004 · Jev routed the message

- **Actor:** Jev (jev-1.13.0 · 1296 in / 285 out tokens · 415 ms)
- **Tool:** TypeSafe `system_one` · step `route_case_messages`
- **Decision:** jev_route → `urgent_hazard` (confidence 0.46)
- **Signals:** hazard 0.60 · multiple_issues 0.12 · sensitive 0.98 · states_facts 0.03 · system_instructions 0.01
- **Why:** Possible hazard (Jev p=0.60); a person takes over before any automated contact.

<a id="entry-005"></a>
## 2026-10-10 16:26:11 UTC — 005 · Claude read the message

- **Actor:** Claude (claude-opus-5 · 387 in / 400 out tokens)
- **Tool:** Anthropic Messages API `ai.triage` (prompt property-triage-2026-10-10.3) · step `triage_case_messages`
- **Reading:** new request · route `urgent_hazard` · medium confidence
- **Work item:** Intermittent heating failure (radiators), hot water unaffected (other)
- **Summary:** Tenant Tessa Vane reports the radiator heating has cut out twice since the previous evening, with hot water still working. A child lives at the property and she has asked for an inspection.
- **Rationale:** Loss of heating with a child at the property is treated as a possible urgent situation needing a case manager, per router decision.
- **Extracted:** 0 claims · 3 ambiguities · 1 issue · risk flags: vulnerable_person
- **Unknown (affects route):** Is the heating currently off, and what boiler/system type and any fault codes? Need to know whether this is a total heating loss.
- **Unknown:** No availability or preferred times given for an inspection visit.
- **Unknown:** No explicit consent or access arrangement for entry stated.

<a id="entry-006"></a>
## 2026-10-10 16:26:11 UTC — 006 · Proposed action → `clarify`

- **Actor:** Triage reading (route `urgent_hazard`)
- **Work item:** Intermittent heating failure (radiators), hot water unaffected
- **Action revision:** 2

<a id="entry-007"></a>
## 2026-10-10 16:26:11 UTC — 007 · Claim `urgent` = true

- **Actor:** Claude (extracted)
- **Status:** unverified assertion — a person or policy must accept it

> Reported that radiator heating had cut out twice since the previous evening while hot water remained available.

<a id="entry-008"></a>
## 2026-10-10 16:26:11 UTC — 008 · Human review opened: `triage`

- **Actor:** Policy engine
- **Owner:** case manager · rule `require-triage`
- **Expires:** 2026-10-12 16:26:11 UTC

> Claude read this as a possible urgent hazard. A case manager must take over now and apply the urgent procedure.

<a id="entry-009"></a>
## 2026-10-10 16:26:11 UTC — 009 · Policy gates → HUMAN REVIEW

- **Actor:** Policy engine (rules v2, `domain.evaluate`)
- **Outcome:** HUMAN REVIEW · owner case manager
- **Blockers:** `triage` UNKNOWN → HUMAN REVIEW
- **Next step:** Claude read this as a possible urgent hazard. A case manager must take over now and apply the urgent procedure.

<a id="entry-010"></a>
## 2026-10-10 16:26:11 UTC — 010 · Message received: Event 002 — Update from Ivo Merrick (Property Manager, Northbridge Lettings)

- **Recorded by:** demo-case_manager (case manager)
- **Reading:** queued for Jev routing / Claude triage

> Event 002 — Update
> From: Ivo Merrick (Property Manager, Northbridge Lettings)
> To: Tessa Vane (Tenant)
>
> Acknowledged the report and asked about leaks, unusual smells, boiler warnings and access times. No entry arrangement was yet confirmed.

<a id="entry-011"></a>
## 2026-10-10 16:26:11 UTC — 011 · Policy gates → WAIT

- **Actor:** Policy engine (rules v2, `domain.evaluate`)
- **Outcome:** WAIT · owner case manager
- **Blockers:** `triage` UNKNOWN → WAIT
- **Next step:** The latest message is being routed and read. Actions wait for the reading.

<a id="entry-012"></a>
## 2026-10-10 16:26:11 UTC — 012 · Workflow receipt

<a id="entry-013"></a>
## 2026-10-10 16:26:11 UTC — 013 · Jev routed the message

- **Actor:** Jev (jev-1.13.0 · 1446 in / 282 out tokens · 355 ms)
- **Tool:** TypeSafe `system_one` · step `route_case_messages`
- **Decision:** jev_route → `clarify` (confidence 0.54)
- **Signals:** hazard 0.19 · multiple_issues 0.09 · sensitive 0.62 · states_facts 0.05 · system_instructions 0.01
- **Why:** Jev routes; Claude extracts quotes and claims. clarify is not a Jev-only route. Route confidence 0.54 is below the Jev-only bar 0.8. Possible distress, complaint or vulnerability.

<a id="entry-014"></a>
## 2026-10-10 16:26:16 UTC — 014 · Claude read the message

- **Actor:** Claude (claude-opus-5 · 696 in / 366 out tokens)
- **Tool:** Anthropic Messages API `ai.triage` (prompt property-triage-2026-10-10.3) · step `triage_case_messages`
- **Reading:** update · route `clarify` · high confidence
- **Work item:** Intermittent heating failure (radiators), hot water unaffected (other)
- **Summary:** Property manager acknowledged the tenant's intermittent heating report and asked about leaks, smells, boiler warnings and access times. No access arrangement confirmed yet.
- **Rationale:** Holding update requesting missing diagnostic and access information; no new facts or consent given, so clarify stands.
- **Extracted:** 0 claims · 2 ambiguities · 1 issue
- **Unknown (affects route):** Awaiting tenant's answers on leaks, smells and boiler warning codes; whether heating is currently off is still unknown.
- **Unknown:** No entry arrangement confirmed; access times still to be provided.

<a id="entry-015"></a>
## 2026-10-10 16:26:16 UTC — 015 · Clarification opened: `triage` → tenant

- **Actor:** Policy engine
- **Owner:** case manager
- **Deadline:** 2026-10-13 16:00:00 UTC

> Clarify before routing: Awaiting tenant's answers on leaks, smells and boiler warning codes; whether heating is currently off is still unknown.

<a id="entry-016"></a>
## 2026-10-10 16:26:16 UTC — 016 · Policy gates → CLARIFY

- **Actor:** Policy engine (rules v2, `domain.evaluate`)
- **Outcome:** CLARIFY · owner case manager
- **Blockers:** `triage` UNKNOWN → CLARIFY
- **Next step:** Clarify before routing: Awaiting tenant's answers on leaks, smells and boiler warning codes; whether heating is currently off is still unknown.

<a id="entry-017"></a>
## 2026-10-10 16:26:16 UTC — 017 · Policy gates → WAIT

- **Actor:** Policy engine (rules v2, `domain.evaluate`)
- **Outcome:** WAIT · owner case manager
- **Blockers:** `triage` UNKNOWN → WAIT
- **Next step:** Clarify before routing: Awaiting tenant's answers on leaks, smells and boiler warning codes; whether heating is currently off is still unknown.

<a id="entry-018"></a>
## 2026-10-10 16:26:23 UTC — 018 · Claude drafted a message to the tenant

- **Actor:** Claude (claude-opus-5 · 809 in / 463 out tokens)
- **Tool:** Anthropic Messages API `ai.draft_tenant_message` · step `compose_tenant_messages`
- **Claude's call:** staff_review — A child lives at the property and the heating is failing intermittently, and the question touches on possible gas smells/boiler faults - a staff member should check the wording and urgency before this goes out.
- **Send gate:** held for staff — Claude asked for staff review: A child lives at the property and the heating is failing intermittently, and the question touches on possible gas smells/boiler faults - a staff member should check the wording and urgency before this goes out. Risk flags: safety, vulnerable_person. A possible urgent hazard is recorded; a person handles contact.
- **Topics:** issue_details

> Hello Tessa,
>
> Thanks for letting us know the radiator heating has cut out twice while your hot water is still working. So we can get this looked at properly, could you tell us how things stand at the moment: is the heating currently off, and have you noticed any leaks, unusual smells, or any warning lights or codes showing on the boiler?
>
> If you ever smell gas or feel unsafe, please contact the emergency services or the National Gas Emergency Service straight away.
>
> Thanks very much,
> Northbridge Lettings

<a id="entry-019"></a>
## 2026-10-10 16:26:23 UTC — 019 · Message received: Event 003 — Portal from Tessa Vane (Tenant)

- **Recorded by:** demo-case_manager (case manager)
- **Reading:** queued for Jev routing / Claude triage

> Event 003 — Portal
> From: Tessa Vane (Tenant)
> To: Ivo Merrick (Property Manager, Northbridge Lettings)
>
> Confirmed no visible leak, unusual smell or current warning light. The boiler had shown a brief symbol the previous night, but she did not identify it. She can provide access after 14:00 on weekdays.

<a id="entry-020"></a>
## 2026-10-10 16:26:23 UTC — 020 · Workflow receipt

<a id="entry-021"></a>
## 2026-10-10 16:26:24 UTC — 021 · Jev routed the message

- **Actor:** Jev (jev-1.13.0 · 1588 in / 284 out tokens · 445 ms)
- **Tool:** TypeSafe `system_one` · step `route_case_messages`
- **Decision:** claude → no route
- **Signals:** hazard 0.13 · multiple_issues 0.09 · sensitive 0.61 · states_facts 0.85 · system_instructions 0.02
- **Why:** Jev route confidence 0.36 is below 0.5.

<a id="entry-022"></a>
## 2026-10-10 16:26:35 UTC — 022 · Claude read the message

- **Actor:** Claude (claude-opus-5 · 908 in / 879 out tokens)
- **Tool:** Anthropic Messages API `ai.triage` (prompt property-triage-2026-10-10.3) · step `triage_case_messages`
- **Reading:** answer to question · route `request_quote` · medium confidence
- **Work item:** Intermittent heating failure (radiators), hot water unaffected (other)
- **Summary:** Tenant replies to the property manager's questions: no visible leak, no unusual smell and no current warning light, though the boiler briefly showed an unidentified symbol the previous night. She states she can provide access after 14:00 on weekdays.
- **Rationale:** Tenant has answered the safety-screening questions with no hazard indicators, so the reported intermittent heating fault can move on to contractor assessment/quote; the unidentified boiler symbol and current heating status remain open but do not block an inspection.
- **Extracted:** 0 claims · 3 ambiguities · 1 issue
- **Unknown (affects route):** The boiler displayed a brief symbol the previous night that the tenant could not identify; the specific fault/warning code is still unknown, as is whether the heating is currently working.
- **Unknown:** Tenant gives general availability (after 14:00 on weekdays) but no specific appointment date and time is agreed.
- **Unknown:** It is unclear whether the tenant will be present to let a contractor in or is granting permission to enter by other means.

<a id="entry-023"></a>
## 2026-10-10 16:26:35 UTC — 023 · Proposed action → `request_quote`

- **Actor:** Triage reading (route `request_quote`)
- **Work item:** Intermittent heating failure (radiators), hot water unaffected
- **Action revision:** 3

<a id="entry-024"></a>
## 2026-10-10 16:26:35 UTC — 024 · Partial answer → narrower follow-up due

- **Actor:** Claude (reading)

> Confirmed no visible leak, unusual smell or current warning light. The boiler had shown a brief symbol the previous night, but she did not identify it.

<a id="entry-025"></a>
## 2026-10-10 16:26:35 UTC — 025 · Question closed

- **Why:** Evidence satisfied the requirement or the action was superseded; old reminders cancelled.

<a id="entry-026"></a>
## 2026-10-10 16:26:35 UTC — 026 · Human review opened: `supported`

- **Actor:** Policy engine
- **Owner:** case manager · rule `require-supported`
- **Expires:** 2026-10-12 16:26:35 UTC

> A case manager must define a supported action for this situation.

<a id="entry-027"></a>
## 2026-10-10 16:26:35 UTC — 027 · Clarification opened: `triage` → tenant

- **Actor:** Policy engine
- **Owner:** case manager
- **Deadline:** 2026-10-13 16:00:00 UTC

> Clarify before routing: The boiler displayed a brief symbol the previous night that the tenant could not identify; the specific fault/warning code is still unknown, as is whether the heating is currently working.

<a id="entry-028"></a>
## 2026-10-10 16:26:35 UTC — 028 · Policy gates → HUMAN REVIEW

- **Actor:** Policy engine (rules v2, `domain.evaluate`)
- **Outcome:** HUMAN REVIEW · owner case manager
- **Blockers:** `supported` UNKNOWN → HUMAN REVIEW; `triage` UNKNOWN → CLARIFY; `classification` UNKNOWN → WAIT
- **Next step:** A case manager must define a supported action for this situation.

<a id="entry-029"></a>
## 2026-10-10 16:26:35 UTC — 029 · Policy gates → HUMAN REVIEW

- **Actor:** Policy engine (rules v2, `domain.evaluate`)
- **Outcome:** HUMAN REVIEW · owner case manager
- **Blockers:** `supported` UNKNOWN → HUMAN REVIEW; `classification` UNKNOWN → WAIT; `triage` UNKNOWN → WAIT
- **Next step:** A case manager must define a supported action for this situation.

<a id="entry-030"></a>
## 2026-10-10 16:26:40 UTC — 030 · Claude drafted a message to the tenant

- **Actor:** Claude (claude-opus-5 · 1032 in / 313 out tokens)
- **Tool:** Anthropic Messages API `ai.draft_tenant_message` · step `compose_tenant_messages`
- **Claude's call:** auto_send — Identity and contact route verified, single information-gathering question on an approved topic (issue_details), no distress, complaint or safety concerns raised; no promises made.
- **Send gate:** auto-send allowed
- **Topics:** issue_details

> Hi Tessa,
>
> Thanks for getting back to us with those details — that's really helpful.
>
> Just one more thing: could you let us know whether the radiators are heating up at the moment, and if the boiler shows any symbol or code on its display now (a photo of the screen would be great if anything appears)?
>
> Thanks very much,
> Northbridge Lettings

<a id="entry-031"></a>
## 2026-10-10 16:26:40 UTC — 031 · Message sent to tenant

- **Actor:** Claude
- **Tool:** `simulated_in_app_thread` adapter — SIMULATED — no real message was sent

<a id="entry-032"></a>
## 2026-10-10 16:26:40 UTC — 032 · Message received: Event 004 — Email from Ivo Merrick (Property Manager, Northbridge Lettings)

- **Recorded by:** demo-case_manager (case manager)
- **Reading:** queued for Jev routing / Claude triage

> Event 004 — Email
> From: Ivo Merrick (Property Manager, Northbridge Lettings)
> To: Soren Dallow (Landlord)
>
> Requested approval for a diagnostic visit. Noted that the agency's routine repair limit is £180 including VAT and that work above that limit needs landlord approval.

<a id="entry-033"></a>
## 2026-10-10 16:26:40 UTC — 033 · Workflow receipt

<a id="entry-034"></a>
## 2026-10-10 16:26:40 UTC — 034 · Jev routed the message

- **Actor:** Jev (jev-1.13.0 · 1704 in / 282 out tokens · 262 ms)
- **Tool:** TypeSafe `system_one` · step `route_case_messages`
- **Decision:** jev_route → `request_quote` (confidence 0.91)
- **Signals:** hazard 0.16 · multiple_issues 0.04 · sensitive 0.64 · states_facts 0.69 · system_instructions 0.02
- **Why:** Jev routes; Claude extracts quotes and claims. The message may state facts that need exact quotes. Possible distress, complaint or vulnerability. Open tenant questions may be answered.

<a id="entry-035"></a>
## 2026-10-10 16:26:45 UTC — 035 · Claude read the message

- **Actor:** Claude (claude-opus-5 · 1219 in / 360 out tokens)
- **Tool:** Anthropic Messages API `ai.triage` (prompt property-triage-2026-10-10.3) · step `triage_case_messages`
- **Reading:** update · route `request_quote` · medium confidence
- **Work item:** Intermittent heating failure (radiators), hot water unaffected (other)
- **Summary:** Property manager emailed the landlord seeking approval for a diagnostic visit on the intermittent heating fault, noting the agency's routine repair limit of £180 including VAT above which landlord approval is needed.
- **Rationale:** Internal agency request for landlord approval of a diagnostic visit; the job still needs assessment/quote before instruction.
- **Extracted:** 0 claims · 1 ambiguity · 1 issue
- **Unknown:** No response yet on whether radiators are currently heating or what boiler code was shown; landlord approval for the diagnostic visit is still outstanding.

<a id="entry-036"></a>
## 2026-10-10 16:26:45 UTC — 036 · Question closed

- **Why:** Evidence satisfied the requirement or the action was superseded; old reminders cancelled.

<a id="entry-037"></a>
## 2026-10-10 16:26:45 UTC — 037 · Policy gates → HUMAN REVIEW

- **Actor:** Policy engine (rules v2, `domain.evaluate`)
- **Outcome:** HUMAN REVIEW · owner case manager
- **Blockers:** `supported` UNKNOWN → HUMAN REVIEW; `classification` UNKNOWN → WAIT
- **Next step:** A case manager must define a supported action for this situation.

<a id="entry-038"></a>
## 2026-10-10 16:26:45 UTC — 038 · Message received: Event 005 — Email from Soren Dallow (Landlord)

- **Recorded by:** demo-case_manager (case manager)
- **Reading:** queued for Jev routing / Claude triage

> Event 005 — Email
> From: Soren Dallow (Landlord)
> To: Ivo Merrick (Property Manager, Northbridge Lettings)
>
> Authorized diagnosis up to £180 including VAT only. Asked to be consulted before any remedial work or additional expenditure is authorized.

<a id="entry-039"></a>
## 2026-10-10 16:26:45 UTC — 039 · Policy gates → HUMAN REVIEW

- **Actor:** Policy engine (rules v2, `domain.evaluate`)
- **Outcome:** HUMAN REVIEW · owner case manager
- **Blockers:** `supported` UNKNOWN → HUMAN REVIEW; `classification` UNKNOWN → WAIT; `triage` UNKNOWN → WAIT
- **Next step:** A case manager must define a supported action for this situation.

<a id="entry-040"></a>
## 2026-10-10 16:26:45 UTC — 040 · Workflow receipt

<a id="entry-041"></a>
## 2026-10-10 16:26:45 UTC — 041 · Jev routed the message

- **Actor:** Jev (jev-1.13.0 · 1683 in / 282 out tokens · 279 ms)
- **Tool:** TypeSafe `system_one` · step `route_case_messages`
- **Decision:** jev_route → `request_quote` (confidence 0.84)
- **Signals:** hazard 0.04 · multiple_issues 0.04 · sensitive 0.03 · states_facts 0.86 · system_instructions 0.02
- **Why:** Jev routes; Claude extracts quotes and claims. The message may state facts that need exact quotes.

<a id="entry-042"></a>
## 2026-10-10 16:26:51 UTC — 042 · Claude read the message

- **Actor:** Claude (claude-opus-5 · 1225 in / 424 out tokens)
- **Tool:** Anthropic Messages API `ai.triage` (prompt property-triage-2026-10-10.3) · step `triage_case_messages`
- **Reading:** update · route `request_quote` · high confidence
- **Work item:** Intermittent heating failure (radiators), hot water unaffected (other)
- **Summary:** Landlord authorises a diagnostic visit up to £180 including VAT and asks to be consulted before any remedial work or further spend.
- **Rationale:** Landlord approval limited to diagnosis; contractor assessment/quote is still the next step.
- **Extracted:** 2 claims · 2 ambiguities · 1 issue
- **Unknown:** No appointment date/time agreed; tenant only gave general availability after 14:00 weekdays.
- **Unknown:** No explicit entry consent or access method confirmed for the diagnostic visit.

<a id="entry-043"></a>
## 2026-10-10 16:26:51 UTC — 043 · Claim `total` = 180.0

- **Actor:** Claude (extracted)
- **Status:** unverified assertion — a person or policy must accept it

> Authorized diagnosis up to £180 including VAT only.

<a id="entry-044"></a>
## 2026-10-10 16:26:51 UTC — 044 · Policy gates → HUMAN REVIEW

- **Actor:** Policy engine (rules v2, `domain.evaluate`)
- **Outcome:** HUMAN REVIEW · owner case manager
- **Blockers:** `supported` UNKNOWN → HUMAN REVIEW; `classification` UNKNOWN → WAIT
- **Next step:** A case manager must define a supported action for this situation.

<a id="entry-045"></a>
## 2026-10-10 16:26:51 UTC — 045 · Message received: Event 006 — Email from Ivo Merrick (Property Manager, Northbridge Lettings)

- **Recorded by:** demo-case_manager (case manager)
- **Reading:** queued for Jev routing / Claude triage

> Event 006 — Email
> From: Ivo Merrick (Property Manager, Northbridge Lettings)
> To: Petra Quill (Contractor, Copper Finch Mechanical)
>
> Requested diagnosis of intermittent radiator heating, a written report and an itemized estimate before work beyond diagnosis. Confirmed access after 14:00 and the diagnostic-only authorization ceiling of £180 including VAT.

<a id="entry-046"></a>
## 2026-10-10 16:26:51 UTC — 046 · Policy gates → HUMAN REVIEW

- **Actor:** Policy engine (rules v2, `domain.evaluate`)
- **Outcome:** HUMAN REVIEW · owner case manager
- **Blockers:** `supported` UNKNOWN → HUMAN REVIEW; `classification` UNKNOWN → WAIT; `triage` UNKNOWN → WAIT
- **Next step:** A case manager must define a supported action for this situation.

<a id="entry-047"></a>
## 2026-10-10 16:26:51 UTC — 047 · Workflow receipt

<a id="entry-048"></a>
## 2026-10-10 16:26:51 UTC — 048 · Jev routed the message

- **Actor:** Jev (jev-1.13.0 · 1706 in / 282 out tokens · 405 ms)
- **Tool:** TypeSafe `system_one` · step `route_case_messages`
- **Decision:** jev_route → `request_quote` (confidence 0.79)
- **Signals:** hazard 0.05 · multiple_issues 0.03 · sensitive 0.02 · states_facts 0.95 · system_instructions 0.02
- **Why:** Jev routes; Claude extracts quotes and claims. Route confidence 0.79 is below the Jev-only bar 0.8. The message may state facts that need exact quotes.

<a id="entry-049"></a>
## 2026-10-10 16:26:57 UTC — 049 · Claude read the message

- **Actor:** Claude (claude-opus-5 · 1500 in / 507 out tokens)
- **Tool:** Anthropic Messages API `ai.triage` (prompt property-triage-2026-10-10.3) · step `triage_case_messages`
- **Reading:** update · route `request_quote` · high confidence
- **Work item:** Intermittent heating failure (radiators), hot water unaffected (other)
- **Summary:** Property manager instructed the contractor to carry out a diagnostic visit for the intermittent radiator heating, requesting a written report and itemised estimate before any further work. Access after 14:00 and a diagnostic-only spend ceiling of £180 including VAT were confirmed.
- **Rationale:** Diagnostic and itemised estimate requested from contractor before any remedial work; quote stage.
- **Extracted:** 2 claims · 2 ambiguities · 1 issue
- **Unknown:** No specific appointment date and time agreed; only "after 14:00" is stated.
- **Unknown:** Access method unclear — whether the tenant will be present or keys are needed.

<a id="entry-050"></a>
## 2026-10-10 16:26:57 UTC — 050 · Claim `total` = 180.0

- **Actor:** Claude (extracted)
- **Status:** unverified assertion — a person or policy must accept it

> the diagnostic-only authorization ceiling of £180 including VAT

<a id="entry-051"></a>
## 2026-10-10 16:26:57 UTC — 051 · Policy gates → HUMAN REVIEW

- **Actor:** Policy engine (rules v2, `domain.evaluate`)
- **Outcome:** HUMAN REVIEW · owner case manager
- **Blockers:** `supported` UNKNOWN → HUMAN REVIEW; `classification` UNKNOWN → WAIT
- **Next step:** A case manager must define a supported action for this situation.

<a id="entry-052"></a>
## 2026-10-10 16:26:58 UTC — 052 · Message received: Event 007 — Email from Petra Quill (Contractor, Copper Finch Mechanical)

- **Recorded by:** demo-case_manager (case manager)
- **Reading:** queued for Jev routing / Claude triage

> Event 007 — Email
> From: Petra Quill (Contractor, Copper Finch Mechanical)
> To: Ivo Merrick (Property Manager, Northbridge Lettings)
>
> Confirmed attendance for 5 February after 14:00. Quoted £138 including VAT for attendance, diagnosis and testing; parts and remedial work were excluded.

<a id="entry-053"></a>
## 2026-10-10 16:26:58 UTC — 053 · Policy gates → HUMAN REVIEW

- **Actor:** Policy engine (rules v2, `domain.evaluate`)
- **Outcome:** HUMAN REVIEW · owner case manager
- **Blockers:** `supported` UNKNOWN → HUMAN REVIEW; `classification` UNKNOWN → WAIT; `triage` UNKNOWN → WAIT
- **Next step:** A case manager must define a supported action for this situation.

<a id="entry-054"></a>
## 2026-10-10 16:26:58 UTC — 054 · Workflow receipt

<a id="entry-055"></a>
## 2026-10-10 16:26:58 UTC — 055 · Jev routed the message

- **Actor:** Jev (jev-1.13.0 · 1708 in / 284 out tokens · 298 ms)
- **Tool:** TypeSafe `system_one` · step `route_case_messages`
- **Decision:** jev_route → `confirm_appointment` (confidence 0.62)
- **Signals:** hazard 0.04 · multiple_issues 0.03 · sensitive 0.02 · states_facts 0.98 · system_instructions 0.02
- **Why:** Jev routes; Claude extracts quotes and claims. confirm_appointment is not a Jev-only route. Route confidence 0.62 is below the Jev-only bar 0.8. The message may state facts that need exact quotes. A route change on an existing case.

<a id="entry-056"></a>
## 2026-10-10 16:27:03 UTC — 056 · Claude read the message

- **Actor:** Claude (claude-opus-5 · 1755 in / 464 out tokens)
- **Tool:** Anthropic Messages API `ai.triage` (prompt property-triage-2026-10-10.3) · step `triage_case_messages`
- **Reading:** access or appointment · route `confirm_appointment` · high confidence
- **Work item:** Intermittent heating failure (radiators), hot water unaffected (other)
- **Summary:** Contractor Copper Finch Mechanical confirms attendance on 5 February after 14:00 and quotes £138 including VAT for attendance, diagnosis and testing, excluding parts and remedial work.
- **Rationale:** Message arranges a visit for a known job and states the diagnostic price; appointment confirmation is the next step.
- **Extracted:** 2 claims · 2 ambiguities · 1 issue
- **Unknown:** No precise arrival time given, only 'after 14:00' on 5 February.
- **Unknown:** Tenant has not confirmed entry consent for this specific date.

<a id="entry-057"></a>
## 2026-10-10 16:27:03 UTC — 057 · Proposed action → `confirm_appointment`

- **Actor:** Triage reading (route `confirm_appointment`)
- **Work item:** Intermittent heating failure (radiators), hot water unaffected
- **Action revision:** 4

<a id="entry-058"></a>
## 2026-10-10 16:27:03 UTC — 058 · Claim `schedule` = true

- **Actor:** Claude (extracted)
- **Status:** unverified assertion — a person or policy must accept it

> Confirmed attendance for 5 February after 14:00.

<a id="entry-059"></a>
## 2026-10-10 16:27:03 UTC — 059 · Claim `total` = 138.0

- **Actor:** Claude (extracted)
- **Status:** unverified assertion — a person or policy must accept it

> Quoted £138 including VAT for attendance, diagnosis and testing; parts and remedial work were excluded.

<a id="entry-060"></a>
## 2026-10-10 16:27:03 UTC — 060 · Human review opened: `authority`

- **Actor:** Policy engine
- **Owner:** approver · rule `require-authority`
- **Expires:** 2026-10-12 16:27:03 UTC

> Obtain authority for this work item, provider and action.

<a id="entry-061"></a>
## 2026-10-10 16:27:03 UTC — 061 · Human review opened: `supported`

- **Actor:** Policy engine
- **Owner:** case manager · rule `require-supported`
- **Expires:** 2026-10-12 16:27:03 UTC

> A case manager must define a supported action for this situation.

<a id="entry-062"></a>
## 2026-10-10 16:27:03 UTC — 062 · Clarification opened: `access` → tenant

- **Actor:** Policy engine
- **Owner:** access officer
- **Deadline:** 2026-10-13 16:00:00 UTC

> Record consent for this visit and access method from the authorised person.

<a id="entry-063"></a>
## 2026-10-10 16:27:03 UTC — 063 · Human review opened: `schedule`

- **Actor:** Policy engine
- **Owner:** case manager · rule `require-schedule`
- **Expires:** 2026-10-12 16:27:03 UTC

> Verify the received source assertion. Confirm the active appointment with a precise date and time.

<a id="entry-064"></a>
## 2026-10-10 16:27:03 UTC — 064 · Policy gates → HUMAN REVIEW

- **Actor:** Policy engine (rules v2, `domain.evaluate`)
- **Outcome:** HUMAN REVIEW · owner approver
- **Blockers:** `authority` UNKNOWN → HUMAN REVIEW; `supported` UNKNOWN → HUMAN REVIEW; `schedule` UNKNOWN → HUMAN REVIEW; `access` UNKNOWN → CLARIFY
- **Next step:** Obtain authority for this work item, provider and action.

<a id="entry-065"></a>
## 2026-10-10 16:27:03 UTC — 065 · Policy gates → HUMAN REVIEW

- **Actor:** Policy engine (rules v2, `domain.evaluate`)
- **Outcome:** HUMAN REVIEW · owner approver
- **Blockers:** `authority` UNKNOWN → HUMAN REVIEW; `supported` UNKNOWN → HUMAN REVIEW; `schedule` UNKNOWN → HUMAN REVIEW; `access` UNKNOWN → WAIT
- **Next step:** Obtain authority for this work item, provider and action.

<a id="entry-066"></a>
## 2026-10-10 16:27:10 UTC — 066 · Claude drafted a message to the tenant

- **Actor:** Claude (claude-opus-5 · 1322 in / 489 out tokens)
- **Tool:** Anthropic Messages API `ai.draft_tenant_message` · step `compose_tenant_messages`
- **Claude's call:** auto_send — Policy mode is claude_decides, the single question is an access question within the permitted auto-send topics, tenant identity and contact route are verified, and the message only gathers access information without promising a visit, cost or outcome. No distress, complaint or safety concerns in the thread.
- **Send gate:** auto-send allowed
- **Topics:** access

> Hi Tessa,
>
> Thanks again for the details about the radiators not heating properly.
>
> We're looking at arranging for an engineer to come and take a look on Thursday 5 February, sometime after 2pm. Could you let us know if someone aged 18 or over would be able to be home then to let them in, and if not, how you'd prefer access to be arranged?
>
> Thanks very much,
> Northbridge Lettings

<a id="entry-067"></a>
## 2026-10-10 16:27:10 UTC — 067 · Message sent to tenant

- **Actor:** Claude
- **Tool:** `simulated_in_app_thread` adapter — SIMULATED — no real message was sent

<a id="entry-068"></a>
## 2026-10-10 16:27:10 UTC — 068 · Message received: Event 008 — Update from Petra Quill (Contractor, Copper Finch Mechanical)

- **Recorded by:** demo-case_manager (case manager)
- **Reading:** queued for Jev routing / Claude triage

> Event 008 — Update
> From: Petra Quill (Contractor, Copper Finch Mechanical)
> To: Ivo Merrick (Property Manager, Northbridge Lettings)
>
> Reported attending and finding an intermittent fault at the heating valve actuator. Said the heating operated during the visit and that no leak or immediate gas-safety concern was observed. No remedial work was reported in this update.

<a id="entry-069"></a>
## 2026-10-10 16:27:10 UTC — 069 · Policy gates → HUMAN REVIEW

- **Actor:** Policy engine (rules v2, `domain.evaluate`)
- **Outcome:** HUMAN REVIEW · owner approver
- **Blockers:** `authority` UNKNOWN → HUMAN REVIEW; `supported` UNKNOWN → HUMAN REVIEW; `schedule` UNKNOWN → HUMAN REVIEW; `access` UNKNOWN → WAIT; `triage` UNKNOWN → WAIT
- **Next step:** Obtain authority for this work item, provider and action.

<a id="entry-070"></a>
## 2026-10-10 16:27:10 UTC — 070 · Workflow receipt

<a id="entry-071"></a>
## 2026-10-10 16:27:11 UTC — 071 · Jev routed the message

- **Actor:** Jev (jev-1.13.0 · 1761 in / 284 out tokens · 382 ms)
- **Tool:** TypeSafe `system_one` · step `route_case_messages`
- **Decision:** jev_route → `confirm_appointment` (confidence 0.57)
- **Signals:** hazard 0.04 · multiple_issues 0.04 · sensitive 0.03 · states_facts 0.45 · system_instructions 0.02
- **Why:** Jev routes; Claude extracts quotes and claims. confirm_appointment is not a Jev-only route. Route confidence 0.57 is below the Jev-only bar 0.8. The message may state facts that need exact quotes. Open tenant questions may be answered.

<a id="entry-072"></a>
## 2026-10-10 16:27:17 UTC — 072 · Claude read the message

- **Actor:** Claude (claude-opus-5 · 1926 in / 508 out tokens)
- **Tool:** Anthropic Messages API `ai.triage` (prompt property-triage-2026-10-10.3) · step `triage_case_messages`
- **Reading:** update · route `request_quote` · medium confidence
- **Work item:** Intermittent heating failure (radiators), hot water unaffected (other)
- **Summary:** Contractor Petra Quill reports attending the property and diagnosing an intermittent fault at the heating valve actuator; heating operated during the visit, no leak or gas-safety concern observed. No remedial work carried out or quoted in this update.
- **Rationale:** Diagnosis attended but no remedial estimate yet; next step is obtaining a quote for the actuator fault rather than arranging another appointment.
- **Extracted:** 0 claims · 2 ambiguities · 1 issue
- **Unknown (affects route):** No itemised estimate or written report for the remedial valve actuator work has been provided; needed before instructing work (landlord consultation required above diagnosis).
- **Unknown:** Unclear whether the diagnostic visit is considered complete and whether the £138 diagnostic charge is now invoiced.
- **Objected to Jev's route:** The visit has already taken place, so confirm_appointment is no longer the live step; the message reports a diagnosis without an estimate, so a quote for the remedial work is needed next.

<a id="entry-073"></a>
## 2026-10-10 16:27:17 UTC — 073 · Proposed action → `request_quote`

- **Actor:** Triage reading (route `request_quote`)
- **Work item:** Intermittent heating failure (radiators), hot water unaffected
- **Action revision:** 5

<a id="entry-074"></a>
## 2026-10-10 16:27:17 UTC — 074 · Question closed

- **Why:** Evidence satisfied the requirement or the action was superseded; old reminders cancelled.

<a id="entry-075"></a>
## 2026-10-10 16:27:17 UTC — 075 · Human review opened: `supported`

- **Actor:** Policy engine
- **Owner:** case manager · rule `require-supported`
- **Expires:** 2026-10-12 16:27:17 UTC

> A case manager must define a supported action for this situation.

<a id="entry-076"></a>
## 2026-10-10 16:27:17 UTC — 076 · Human review opened: `triage`

- **Actor:** Policy engine
- **Owner:** case manager · rule `require-triage`
- **Expires:** 2026-10-12 16:27:17 UTC

> Jev routed this message to confirm_appointment, but Claude reads it as request_quote: The visit has already taken place, so confirm_appointment is no longer the live step; the message reports a diagnosis without an estimate, so a quote for the remedial work is needed next. The case follows Claude's route (a hazard is never de-escalated). Confirm or correct the route.

<a id="entry-077"></a>
## 2026-10-10 16:27:17 UTC — 077 · Policy gates → HUMAN REVIEW

- **Actor:** Policy engine (rules v2, `domain.evaluate`)
- **Outcome:** HUMAN REVIEW · owner case manager
- **Blockers:** `supported` UNKNOWN → HUMAN REVIEW; `triage` CONFLICT → HUMAN REVIEW; `classification` UNKNOWN → WAIT
- **Next step:** A case manager must define a supported action for this situation.

<a id="entry-078"></a>
## 2026-10-10 16:27:17 UTC — 078 · Message received: Event 009 — Email from Petra Quill (Contractor, Copper Finch Mechanical)

- **Recorded by:** demo-case_manager (case manager)
- **Reading:** queued for Jev routing / Claude triage

> Event 009 — Email
> From: Petra Quill (Contractor, Copper Finch Mechanical)
> To: Ivo Merrick (Property Manager, Northbridge Lettings)
>
> Sent an estimate for £372 including VAT for actuator supply and replacement, attendance and heating-system testing. Requested written authorization before proceeding. The estimate did not say whether the £138 diagnostic charge would be credited.

<a id="entry-079"></a>
## 2026-10-10 16:27:17 UTC — 079 · Policy gates → HUMAN REVIEW

- **Actor:** Policy engine (rules v2, `domain.evaluate`)
- **Outcome:** HUMAN REVIEW · owner case manager
- **Blockers:** `supported` UNKNOWN → HUMAN REVIEW; `classification` UNKNOWN → WAIT; `triage` UNKNOWN → WAIT
- **Next step:** A case manager must define a supported action for this situation.

<a id="entry-080"></a>
## 2026-10-10 16:27:17 UTC — 080 · Workflow receipt

<a id="entry-081"></a>
## 2026-10-10 16:27:18 UTC — 081 · Jev routed the message

- **Actor:** Jev (jev-1.13.0 · 1741 in / 282 out tokens · 252 ms)
- **Tool:** TypeSafe `system_one` · step `route_case_messages`
- **Decision:** claude → no route
- **Signals:** hazard 0.03 · multiple_issues 0.04 · sensitive 0.02 · states_facts 0.97 · system_instructions 0.02
- **Why:** Jev route confidence 0.39 is below 0.5.

<a id="entry-082"></a>
## 2026-10-10 16:27:24 UTC — 082 · Claude read the message

- **Actor:** Claude (claude-opus-5 · 1794 in / 540 out tokens)
- **Tool:** Anthropic Messages API `ai.triage` (prompt property-triage-2026-10-10.3) · step `triage_case_messages`
- **Reading:** update · route `instruct_work` · medium confidence
- **Work item:** Intermittent heating failure (radiators), hot water unaffected (other)
- **Summary:** Contractor Petra Quill has submitted an estimate of £372 including VAT to supply and replace the heating valve actuator, including attendance and system testing, and asks for written authorisation before proceeding. It is unclear whether the £138 diagnostic charge is credited against this figure.
- **Rationale:** The job has been diagnosed and a remedial estimate is now on the table; the next step is authorisation and instruction of the contractor, subject to landlord approval as the figure exceeds the £180 limit.
- **Extracted:** 1 claim · 2 ambiguities · 1 issue
- **Unknown:** The estimate does not state whether the £138 diagnostic charge is credited against the £372, so the full comparable commitment is unclear.
- **Unknown:** No written diagnostic report or itemised breakdown of the £372 estimate has been confirmed as supplied; the estimate exceeds the £180 routine limit so landlord approval is required before instructing.

<a id="entry-083"></a>
## 2026-10-10 16:27:24 UTC — 083 · Proposed action → `instruct_work`

- **Actor:** Triage reading (route `instruct_work`)
- **Work item:** Intermittent heating failure (radiators), hot water unaffected
- **Action revision:** 6

<a id="entry-084"></a>
## 2026-10-10 16:27:24 UTC — 084 · Claim `total` = 372.0

- **Actor:** Claude (extracted)
- **Status:** unverified assertion — a person or policy must accept it

> Sent an estimate for £372 including VAT for actuator supply and replacement, attendance and heating-system testing.

<a id="entry-085"></a>
## 2026-10-10 16:27:24 UTC — 085 · Human review opened: `authority`

- **Actor:** Policy engine
- **Owner:** approver · rule `require-authority`
- **Expires:** 2026-10-12 16:27:24 UTC

> Obtain authority for this work item, provider and action.

<a id="entry-086"></a>
## 2026-10-10 16:27:24 UTC — 086 · Human review opened: `supported`

- **Actor:** Policy engine
- **Owner:** case manager · rule `require-supported`
- **Expires:** 2026-10-12 16:27:24 UTC

> A case manager must define a supported action for this situation.

<a id="entry-087"></a>
## 2026-10-10 16:27:24 UTC — 087 · Clarification opened: `access` → tenant

- **Actor:** Policy engine
- **Owner:** access officer
- **Deadline:** 2026-10-13 16:00:00 UTC

> Record consent for this visit and access method from the authorised person.

<a id="entry-088"></a>
## 2026-10-10 16:27:24 UTC — 088 · Clarification opened: `schedule` → tenant

- **Actor:** Policy engine
- **Owner:** case manager
- **Deadline:** 2026-10-13 16:00:00 UTC

> Confirm the active appointment with a precise date and time.

<a id="entry-089"></a>
## 2026-10-10 16:27:24 UTC — 089 · Clarification opened: `evidence` → tenant

- **Actor:** Policy engine
- **Owner:** case manager
- **Deadline:** 2026-10-13 16:00:00 UTC

> Supply usable evidence required for this work item.

<a id="entry-090"></a>
## 2026-10-10 16:27:24 UTC — 090 · Human review opened: `total`

- **Actor:** Policy engine
- **Owner:** case manager · rule `require-total`
- **Expires:** 2026-10-12 16:27:24 UTC

> Verify the received source assertion. Establish the full comparable commitment, including tax.

<a id="entry-091"></a>
## 2026-10-10 16:27:24 UTC — 091 · Policy gates → HUMAN REVIEW

- **Actor:** Policy engine (rules v2, `domain.evaluate`)
- **Outcome:** HUMAN REVIEW · owner approver
- **Blockers:** `authority` UNKNOWN → HUMAN REVIEW; `supported` UNKNOWN → HUMAN REVIEW; `total` UNKNOWN → HUMAN REVIEW; `access` UNKNOWN → CLARIFY; `schedule` UNKNOWN → CLARIFY; `evidence` UNKNOWN → CLARIFY; `classification` UNKNOWN → WAIT
- **Next step:** Obtain authority for this work item, provider and action.

<a id="entry-092"></a>
## 2026-10-10 16:27:24 UTC — 092 · Policy gates → HUMAN REVIEW

- **Actor:** Policy engine (rules v2, `domain.evaluate`)
- **Outcome:** HUMAN REVIEW · owner approver
- **Blockers:** `authority` UNKNOWN → HUMAN REVIEW; `supported` UNKNOWN → HUMAN REVIEW; `total` UNKNOWN → HUMAN REVIEW; `access` UNKNOWN → WAIT; `schedule` UNKNOWN → WAIT; `evidence` UNKNOWN → WAIT; `classification` UNKNOWN → WAIT
- **Next step:** Obtain authority for this work item, provider and action.

<a id="entry-093"></a>
## 2026-10-10 16:27:33 UTC — 093 · Claude drafted a message to the tenant

- **Actor:** Claude (claude-opus-5 · 1746 in / 622 out tokens)
- **Tool:** Anthropic Messages API `ai.draft_tenant_message` · step `compose_tenant_messages`
- **Claude's call:** staff_review — Case next action is to instruct work and an estimate (\u00a3372) awaits authorisation, with an unresolved question over whether the \u00a3138 diagnostic fee is credited; a previous message already proposed Thursday 5 February, so staff should confirm the current appointment position before this goes out to avoid contradicting the tenant's expectations.
- **Send gate:** held for staff — Claude asked for staff review: Case next action is to instruct work and an estimate (\u00a3372) awaits authorisation, with an unresolved question over whether the \u00a3138 diagnostic fee is credited; a previous message already proposed Thursday 5 February, so staff should confirm the current appointment position before this goes out to avoid contradicting the tenant's expectations.
- **Topics:** access, availability, photo

> Hi Tessa,
>
> Thanks for your patience while we look into the intermittent heating problem with your radiators.
>
> When you have a moment, could you help us with a few things?
>
> 1. Which dates and times in the next couple of weeks would suit you for someone to attend? Please give a day and a rough time.
> 2. Would someone aged 18 or over be able to be home to let an engineer in, and if not, how would you prefer access to be arranged?
> 3. If the radiators stay cold again, could you send a photo of the boiler display and of the affected radiator?
>
> Thanks very much,
> Northbridge Lettings

<a id="entry-094"></a>
## 2026-10-10 16:27:33 UTC — 094 · Message received: Event 010 — Email from Ivo Merrick (Property Manager, Northbridge Lettings)

- **Recorded by:** demo-case_manager (case manager)
- **Reading:** queued for Jev routing / Claude triage

> Event 010 — Email
> From: Ivo Merrick (Property Manager, Northbridge Lettings)
> To: Soren Dallow (Landlord)
>
> Forwarded the estimate and asked whether the proposed work was authorized. Noted that it exceeded the routine limit and that the contractor had been told to obtain written authorization before remedial work.

<a id="entry-095"></a>
## 2026-10-10 16:27:33 UTC — 095 · Policy gates → HUMAN REVIEW

- **Actor:** Policy engine (rules v2, `domain.evaluate`)
- **Outcome:** HUMAN REVIEW · owner approver
- **Blockers:** `authority` UNKNOWN → HUMAN REVIEW; `supported` UNKNOWN → HUMAN REVIEW; `total` UNKNOWN → HUMAN REVIEW; `access` UNKNOWN → WAIT; `schedule` UNKNOWN → WAIT; `evidence` UNKNOWN → WAIT; `classification` UNKNOWN → WAIT; `triage` UNKNOWN → WAIT
- **Next step:** Obtain authority for this work item, provider and action.

<a id="entry-096"></a>
## 2026-10-10 16:27:33 UTC — 096 · Workflow receipt

<a id="entry-097"></a>
## 2026-10-10 16:27:33 UTC — 097 · Jev routed the message

- **Actor:** Jev (jev-1.13.0 · 1775 in / 283 out tokens · 253 ms)
- **Tool:** TypeSafe `system_one` · step `route_case_messages`
- **Decision:** jev_route → `instruct_work` (confidence 0.76)
- **Signals:** hazard 0.04 · multiple_issues 0.05 · sensitive 0.03 · states_facts 0.19 · system_instructions 0.02
- **Why:** Jev routes; Claude extracts quotes and claims. instruct_work is not a Jev-only route. Route confidence 0.76 is below the Jev-only bar 0.8. Open tenant questions may be answered.

<a id="entry-098"></a>
## 2026-10-10 16:27:40 UTC — 098 · Claude read the message

- **Actor:** Claude (claude-opus-5 · 2063 in / 536 out tokens)
- **Tool:** Anthropic Messages API `ai.triage` (prompt property-triage-2026-10-10.3) · step `triage_case_messages`
- **Reading:** update · route `instruct_work` · medium confidence
- **Work item:** Intermittent heating failure (radiators), hot water unaffected (other)
- **Summary:** The property manager forwarded the contractor's £372 inc VAT estimate to the landlord and asked whether the remedial work is authorised, noting it exceeds the agency's routine repair limit and that the contractor was told to get written authorisation first. No landlord decision yet.
- **Rationale:** Router set instruct_work; the message is the authorisation step for the already-quoted remedial job, though approval is still pending.
- **Extracted:** 0 claims · 2 ambiguities · 1 issue
- **Unknown (affects route):** Landlord authorisation for the £372 inc VAT remedial estimate has been requested but not yet given; work cannot be instructed until a decision is received.
- **Unknown:** Unclear whether the £138 diagnostic charge will be credited against the remedial estimate.

<a id="entry-099"></a>
## 2026-10-10 16:27:40 UTC — 099 · Clarification opened: `triage` → tenant

- **Actor:** Policy engine
- **Owner:** case manager
- **Deadline:** 2026-10-13 16:00:00 UTC

> Clarify before routing: Landlord authorisation for the £372 inc VAT remedial estimate has been requested but not yet given; work cannot be instructed until a decision is received.

<a id="entry-100"></a>
## 2026-10-10 16:27:40 UTC — 100 · Policy gates → HUMAN REVIEW

- **Actor:** Policy engine (rules v2, `domain.evaluate`)
- **Outcome:** HUMAN REVIEW · owner approver
- **Blockers:** `authority` UNKNOWN → HUMAN REVIEW; `supported` UNKNOWN → HUMAN REVIEW; `total` UNKNOWN → HUMAN REVIEW; `triage` UNKNOWN → CLARIFY; `access` UNKNOWN → WAIT; `schedule` UNKNOWN → WAIT; `evidence` UNKNOWN → WAIT; `classification` UNKNOWN → WAIT
- **Next step:** Obtain authority for this work item, provider and action.

<a id="entry-101"></a>
## 2026-10-10 16:27:40 UTC — 101 · Policy gates → HUMAN REVIEW

- **Actor:** Policy engine (rules v2, `domain.evaluate`)
- **Outcome:** HUMAN REVIEW · owner approver
- **Blockers:** `authority` UNKNOWN → HUMAN REVIEW; `supported` UNKNOWN → HUMAN REVIEW; `total` UNKNOWN → HUMAN REVIEW; `access` UNKNOWN → WAIT; `schedule` UNKNOWN → WAIT; `evidence` UNKNOWN → WAIT; `classification` UNKNOWN → WAIT; `triage` UNKNOWN → WAIT
- **Next step:** Obtain authority for this work item, provider and action.

<a id="entry-102"></a>
## 2026-10-10 16:27:46 UTC — 102 · Claude drafted a message to the tenant

- **Actor:** Claude (claude-opus-5 · 1628 in / 426 out tokens)
- **Tool:** Anthropic Messages API `ai.draft_tenant_message` · step `compose_tenant_messages`
- **Claude's call:** staff_review — The open question is really about landlord authorisation for the £372 inc VAT estimate, which the tenant cannot answer; the tenant-facing message only asks for a status update, so staff should confirm it is appropriate to send while the authorisation decision is outstanding and that no cost or landlord details are disclosed.
- **Send gate:** held for staff — Claude asked for staff review: The open question is really about landlord authorisation for the £372 inc VAT estimate, which the tenant cannot answer; the tenant-facing message only asks for a status update, so staff should confirm it is appropriate to send while the authorisation decision is outstanding and that no cost or landlord details are disclosed.
- **Topics:** issue_details

> Hi Tessa,
>
> Thanks for your patience while the engineer visited on 5 February.
>
> So we have an up-to-date picture, could you let us know how the heating has been behaving since then — are the radiators heating up reliably, or is it still cutting out at times?
>
> Thanks very much,
> Northbridge Lettings

<a id="entry-103"></a>
## 2026-10-10 16:27:46 UTC — 103 · Message received: Event 011 — SMS from Tessa Vane (Tenant)

- **Recorded by:** demo-case_manager (case manager)
- **Reading:** queued for Jev routing / Claude triage

> Event 011 — SMS
> From: Tessa Vane (Tenant)
> To: Ivo Merrick (Property Manager, Northbridge Lettings)
>
> Reported that the radiators were cold again. She was using one portable heater in the sitting room and said it was plugged directly into a wall socket. No new smell, leak or warning was reported.

<a id="entry-104"></a>
## 2026-10-10 16:27:46 UTC — 104 · Workflow receipt

<a id="entry-105"></a>
## 2026-10-10 16:27:47 UTC — 105 · Jev routed the message

- **Actor:** Jev (jev-1.13.0 · 1815 in / 282 out tokens · 321 ms)
- **Tool:** TypeSafe `system_one` · step `route_case_messages`
- **Decision:** claude → no route
- **Signals:** hazard 0.13 · multiple_issues 0.05 · sensitive 0.04 · states_facts 0.12 · system_instructions 0.02
- **Why:** Jev route confidence 0.47 is below 0.5.

<a id="entry-106"></a>
## 2026-10-10 16:27:54 UTC — 106 · Claude read the message

- **Actor:** Claude (claude-opus-5 · 2117 in / 658 out tokens)
- **Tool:** Anthropic Messages API `ai.triage` (prompt property-triage-2026-10-10.3) · step `triage_case_messages`
- **Reading:** update · route `instruct_work` · medium confidence
- **Work item:** Intermittent heating failure (radiators), hot water unaffected (other)
- **Summary:** Tenant reports the radiators are cold again after the 5 February diagnostic visit, and is using one portable heater plugged directly into a wall socket. No new smell, leak or warning reported.
- **Rationale:** Known job: tenant confirms the fault recurred after diagnosis, supporting the pending remedial work. Route retained as instruct_work, but landlord authorisation for the £372 estimate remains outstanding. No explicit hazard reported (no smell, leak or warning; heater plugged directly into a wall socket).
- **Extracted:** 1 claim · 2 ambiguities · 1 issue
- **Unknown (affects route):** Landlord authorisation for the £372 inc VAT remedial estimate is still outstanding; work cannot be instructed until a decision is received.
- **Unknown (affects route):** Check whether the tenant is without heating and whether anyone in the household is vulnerable, given reliance on a single portable heater in February.

<a id="entry-107"></a>
## 2026-10-10 16:27:54 UTC — 107 · Claim `completion` = false

- **Actor:** Claude (extracted)
- **Status:** unverified assertion — a person or policy must accept it

> Reported that the radiators were cold again.

<a id="entry-108"></a>
## 2026-10-10 16:27:55 UTC — 108 · Message received: Event 012 — Email from Soren Dallow (Landlord)

- **Recorded by:** demo-case_manager (case manager)
- **Reading:** queued for Jev routing / Claude triage

> Event 012 — Email
> From: Soren Dallow (Landlord)
> To: Ivo Merrick (Property Manager, Northbridge Lettings)
>
> Had not decided on the estimate. Asked whether the actuator could be repaired and whether the price included all parts, labour and testing. Did not authorize remedial work or further expenditure.

<a id="entry-109"></a>
## 2026-10-10 16:27:55 UTC — 109 · Workflow receipt

<a id="entry-110"></a>
## 2026-10-10 16:27:55 UTC — 110 · Jev routed the message

- **Actor:** Jev (jev-1.13.0 · 1803 in / 282 out tokens · 272 ms)
- **Tool:** TypeSafe `system_one` · step `route_case_messages`
- **Decision:** jev_route → `clarify` (confidence 0.84)
- **Signals:** hazard 0.06 · multiple_issues 0.05 · sensitive 0.04 · states_facts 0.15 · system_instructions 0.02
- **Why:** Jev routes; Claude extracts quotes and claims. clarify is not a Jev-only route. Open tenant questions may be answered. A route change on an existing case.

<a id="entry-111"></a>
## 2026-10-10 16:28:02 UTC — 111 · Claude read the message

- **Actor:** Claude (claude-opus-5 · 2252 in / 670 out tokens)
- **Tool:** Anthropic Messages API `ai.triage` (prompt property-triage-2026-10-10.3) · step `triage_case_messages`
- **Reading:** answer to question · route `clarify` · high confidence
- **Work item:** Intermittent heating failure (radiators), hot water unaffected (other)
- **Summary:** Landlord has not yet decided on the £372 inc VAT remedial estimate and asks whether the actuator could be repaired instead and whether the price covers all parts, labour and testing. No authorisation given.
- **Rationale:** Landlord withheld authorisation and raised questions about scope and price, so the item cannot be instructed; clarification required.
- **Extracted:** 1 claim · 2 ambiguities · 1 issue
- **Unknown (affects route):** Landlord asks whether the actuator can be repaired rather than replaced and whether £372 inc VAT covers all parts, labour and testing; contractor response needed before a decision.
- **Unknown (affects route):** Tenant reported cold radiators again and is relying on a single portable heater in February; check whether anyone in the household is vulnerable.

<a id="entry-112"></a>
## 2026-10-10 16:28:02 UTC — 112 · Proposed action → `clarify`

- **Actor:** Triage reading (route `clarify`)
- **Work item:** Intermittent heating failure (radiators), hot water unaffected
- **Action revision:** 7

<a id="entry-113"></a>
## 2026-10-10 16:28:02 UTC — 113 · Partial answer → narrower follow-up due

- **Actor:** Claude (reading)

> Had not decided on the estimate.

<a id="entry-114"></a>
## 2026-10-10 16:28:02 UTC — 114 · Question closed

- **Why:** Evidence satisfied the requirement or the action was superseded; old reminders cancelled.

<a id="entry-115"></a>
## 2026-10-10 16:28:02 UTC — 115 · Question closed

- **Why:** Evidence satisfied the requirement or the action was superseded; old reminders cancelled.

<a id="entry-116"></a>
## 2026-10-10 16:28:02 UTC — 116 · Question closed

- **Why:** Evidence satisfied the requirement or the action was superseded; old reminders cancelled.

<a id="entry-117"></a>
## 2026-10-10 16:28:02 UTC — 117 · Question closed

- **Why:** Evidence satisfied the requirement or the action was superseded; old reminders cancelled.

<a id="entry-118"></a>
## 2026-10-10 16:28:02 UTC — 118 · Clarification opened: `triage` → tenant

- **Actor:** Policy engine
- **Owner:** case manager
- **Deadline:** 2026-10-13 16:00:00 UTC

> Clarify before routing: Landlord asks whether the actuator can be repaired rather than replaced and whether £372 inc VAT covers all parts, labour and testing; contractor response needed before a decision.; Tenant reported cold radiators again and is relying on a single portable heater in February; check whether anyone in the household is vulnerable.

<a id="entry-119"></a>
## 2026-10-10 16:28:02 UTC — 119 · Policy gates → CLARIFY

- **Actor:** Policy engine (rules v2, `domain.evaluate`)
- **Outcome:** CLARIFY · owner case manager
- **Blockers:** `triage` UNKNOWN → CLARIFY
- **Next step:** Clarify before routing: Landlord asks whether the actuator can be repaired rather than replaced and whether £372 inc VAT covers all parts, labour and testing; contractor response needed before a decision.; Tenant reported cold radiators again and is relying on a single portable heater in February; check whether anyone in the household is vulnerable.

<a id="entry-120"></a>
## 2026-10-10 16:28:02 UTC — 120 · Policy gates → WAIT

- **Actor:** Policy engine (rules v2, `domain.evaluate`)
- **Outcome:** WAIT · owner case manager
- **Blockers:** `triage` UNKNOWN → WAIT
- **Next step:** Clarify before routing: Landlord asks whether the actuator can be repaired rather than replaced and whether £372 inc VAT covers all parts, labour and testing; contractor response needed before a decision.; Tenant reported cold radiators again and is relying on a single portable heater in February; check whether anyone in the household is vulnerable.

<a id="entry-121"></a>
## 2026-10-10 16:28:08 UTC — 121 · Claude drafted a message to the tenant

- **Actor:** Claude (claude-opus-5 · 1658 in / 400 out tokens)
- **Tool:** Anthropic Messages API `ai.draft_tenant_message` · step `compose_tenant_messages`
- **Claude's call:** staff_review — Tenant has been without heating again in February and is relying on a single portable heater; possible vulnerability and loss of heating means staff should check the wording and chase the outstanding estimate decision before contact.
- **Send gate:** held for staff — Claude asked for staff review: Tenant has been without heating again in February and is relying on a single portable heater; possible vulnerability and loss of heating means staff should check the wording and chase the outstanding estimate decision before contact. Risk flags: safety, vulnerable_person. A possible urgent hazard is recorded; a person handles contact.
- **Topics:** issue_details

> Hi Tessa,
>
> Thanks for letting us know the radiators are cold again — sorry you're having to manage with a portable heater in this weather.
>
> So we have a clear picture of how you're getting on, could you tell us how the property is keeping at the moment with just the one heater, and whether anyone in the household is elderly, very young, unwell or would find the cold particularly difficult?
>
> If you ever feel unsafe or unwell, please contact the emergency services on 999.
>
> Thanks very much,
> Northbridge Lettings

<a id="entry-122"></a>
## 2026-10-10 16:28:08 UTC — 122 · Message received: Event 013 — Portal from Ivo Merrick (Property Manager, Northbridge Lettings)

- **Recorded by:** demo-case_manager (case manager)
- **Reading:** queued for Jev routing / Claude triage

> Event 013 — Portal
> From: Ivo Merrick (Property Manager, Northbridge Lettings)
> To: Tessa Vane (Tenant)
>
> Asked whether heating or safety symptoms had changed, whether the equipment-label details were available, and whether the contractor could be given access if a return visit were arranged.

<a id="entry-123"></a>
## 2026-10-10 16:28:08 UTC — 123 · Workflow receipt

<a id="entry-124"></a>
## 2026-10-10 16:28:09 UTC — 124 · Jev routed the message

- **Actor:** Jev (jev-1.13.0 · 1772 in / 282 out tokens · 240 ms)
- **Tool:** TypeSafe `system_one` · step `route_case_messages`
- **Decision:** jev_route → `clarify` (confidence 0.78)
- **Signals:** hazard 0.15 · multiple_issues 0.08 · sensitive 0.08 · states_facts 0.22 · system_instructions 0.02
- **Why:** Jev routes; Claude extracts quotes and claims. clarify is not a Jev-only route. Route confidence 0.78 is below the Jev-only bar 0.8. Open tenant questions may be answered.

<a id="entry-125"></a>
## 2026-10-10 16:28:14 UTC — 125 · Claude read the message

- **Actor:** Claude (claude-opus-5 · 2089 in / 426 out tokens)
- **Tool:** Anthropic Messages API `ai.triage` (prompt property-triage-2026-10-10.3) · step `triage_case_messages`
- **Reading:** update · route `clarify` · high confidence
- **Work item:** Intermittent heating failure (radiators), hot water unaffected (other)
- **Summary:** Property manager asked the tenant whether heating or safety symptoms had changed, whether equipment-label details were available, and whether access could be given for a possible return visit. No new facts or decisions are provided.
- **Rationale:** Outbound clarification request from the property manager; no new information or authority, so the item remains awaiting clarification.
- **Extracted:** 0 claims · 2 ambiguities · 1 issue
- **Unknown (affects route):** Awaiting tenant's reply on whether heating or safety symptoms have changed and whether equipment-label details are available.
- **Unknown:** Tenant has not yet confirmed whether the contractor can be given access for a return visit.

<a id="entry-126"></a>
## 2026-10-10 16:28:15 UTC — 126 · Message received: Event 014 — Portal from Tessa Vane (Tenant)

- **Recorded by:** demo-case_manager (case manager)
- **Reading:** queued for Jev routing / Claude triage

> Event 014 — Portal
> From: Tessa Vane (Tenant)
> To: Ivo Merrick (Property Manager, Northbridge Lettings)
>
> Said the radiators were still inconsistent and repeated that hot water was available. Supplied the boiler-label details in the message. She had not agreed a return appointment.

<a id="entry-127"></a>
## 2026-10-10 16:28:15 UTC — 127 · Workflow receipt

<a id="entry-128"></a>
## 2026-10-10 16:28:15 UTC — 128 · Jev routed the message

- **Actor:** Jev (jev-1.13.0 · 1756 in / 284 out tokens · 243 ms)
- **Tool:** TypeSafe `system_one` · step `route_case_messages`
- **Decision:** jev_route → `clarify` (confidence 0.56)
- **Signals:** hazard 0.11 · multiple_issues 0.11 · sensitive 0.06 · states_facts 0.10 · system_instructions 0.02
- **Why:** Jev routes; Claude extracts quotes and claims. clarify is not a Jev-only route. Route confidence 0.56 is below the Jev-only bar 0.8. Open tenant questions may be answered.

<a id="entry-129"></a>
## 2026-10-10 16:28:22 UTC — 129 · Claude read the message

- **Actor:** Claude (claude-opus-5 · 1991 in / 508 out tokens)
- **Tool:** Anthropic Messages API `ai.triage` (prompt property-triage-2026-10-10.3) · step `triage_case_messages`
- **Reading:** answer to question · route `clarify` · medium confidence
- **Work item:** Intermittent heating failure (radiators), hot water unaffected (other)
- **Summary:** Tenant reports radiators still inconsistent with hot water unaffected, and supplies boiler-label details. No return appointment has been agreed.
- **Rationale:** Tenant partially answers symptom and label questions, but contractor repair/price clarification and landlord authority remain outstanding, so clarify stands.
- **Extracted:** 0 claims · 3 ambiguities · 1 issue
- **Unknown (affects route):** Contractor still to confirm whether the actuator can be repaired rather than replaced and whether £372 inc VAT covers all parts, labour and testing; landlord authority outstanding.
- **Unknown:** No return appointment agreed; tenant availability and access arrangements still needed.
- **Unknown (affects route):** Unclear whether anyone in the household is vulnerable while relying on a portable heater in February.

<a id="entry-130"></a>
## 2026-10-10 16:28:22 UTC — 130 · Partial answer → narrower follow-up due

- **Actor:** Claude (reading)

> Said the radiators were still inconsistent and repeated that hot water was available. Supplied the boiler-label details in the message.

<a id="entry-131"></a>
## 2026-10-10 16:28:29 UTC — 131 · Claude drafted a message to the tenant

- **Actor:** Claude (claude-opus-5 · 1612 in / 473 out tokens)
- **Tool:** Anthropic Messages API `ai.draft_tenant_message` · step `compose_tenant_messages`
- **Claude's call:** staff_review — Possible vulnerability: tenant is relying on a single portable heater in February with repeated loss of heating, and the question itself probes household vulnerability \u2014 staff should check tone and consider interim support before sending.
- **Send gate:** held for staff — Claude asked for staff review: Possible vulnerability: tenant is relying on a single portable heater in February with repeated loss of heating, and the question itself probes household vulnerability \u2014 staff should check tone and consider interim support before sending. Risk flags: safety, vulnerable_person. A possible urgent hazard is recorded; a person handles contact.
- **Topics:** issue_details

> Hi Tessa,
>
> Thanks for sending over the boiler-label details and for letting us know the radiators are still inconsistent while the hot water is fine.
>
> So we have the full picture, could you let us know how the cold radiators are affecting the household at the moment \u2014 in particular, whether anyone living there is elderly, very young, unwell or otherwise likely to be affected by the lack of heating?
>
> If you ever feel unsafe, please contact the emergency services.
>
> Thanks very much,
> Northbridge Lettings

<a id="entry-132"></a>
## 2026-10-10 16:28:29 UTC — 132 · Message received: Event 015 — Email from Ivo Merrick (Property Manager, Northbridge Lettings)

- **Recorded by:** demo-case_manager (case manager)
- **Reading:** queued for Jev routing / Claude triage

> Event 015 — Email
> From: Ivo Merrick (Property Manager, Northbridge Lettings)
> To: Petra Quill (Contractor, Copper Finch Mechanical)
>
> Asked for a repair alternative, confirmation of parts availability, a breakdown of the estimate and clarification of whether diagnosis would be credited. Repeated that no further work was authorized.

<a id="entry-133"></a>
## 2026-10-10 16:28:29 UTC — 133 · Workflow receipt

<a id="entry-134"></a>
## 2026-10-10 16:28:30 UTC — 134 · Jev routed the message

- **Actor:** Jev (jev-1.13.0 · 1762 in / 284 out tokens · 228 ms)
- **Tool:** TypeSafe `system_one` · step `route_case_messages`
- **Decision:** jev_route → `clarify` (confidence 0.88)
- **Signals:** hazard 0.11 · multiple_issues 0.07 · sensitive 0.09 · states_facts 0.13 · system_instructions 0.02
- **Why:** Jev routes; Claude extracts quotes and claims. clarify is not a Jev-only route. Open tenant questions may be answered.

<a id="entry-135"></a>
## 2026-10-10 16:28:37 UTC — 135 · Claude read the message

- **Actor:** Claude (claude-opus-5 · 2021 in / 567 out tokens)
- **Tool:** Anthropic Messages API `ai.triage` (prompt property-triage-2026-10-10.3) · step `triage_case_messages`
- **Reading:** update · route `clarify` · high confidence
- **Work item:** Intermittent heating failure (radiators), hot water unaffected (other)
- **Summary:** Property manager emailed the contractor asking for a repair alternative, parts availability, an estimate breakdown and whether the diagnostic charge would be credited, repeating that no further work is authorised.
- **Rationale:** Outbound chase to contractor; key pricing/repair questions and vulnerability check remain unresolved, so the item stays in clarify.
- **Extracted:** 1 claim · 2 ambiguities · 1 issue
- **Unknown (affects route):** Contractor has not yet answered whether the actuator can be repaired, whether £372 inc VAT covers all parts, labour and testing, or whether the £138 diagnostic fee is credited.
- **Unknown (affects route):** Still unknown whether anyone in the household is vulnerable while relying on a portable heater in February.

<a id="entry-136"></a>
## 2026-10-10 16:28:37 UTC — 136 · Partial answer → narrower follow-up due

- **Actor:** Claude (reading)

> Asked for a repair alternative, confirmation of parts availability, a breakdown of the estimate and clarification of whether diagnosis would be credited.

<a id="entry-137"></a>
## 2026-10-10 16:28:37 UTC — 137 · Message received: Event 016 — Email from Petra Quill (Contractor, Copper Finch Mechanical)

- **Recorded by:** demo-case_manager (case manager)
- **Reading:** queued for Jev routing / Claude triage

> Event 016 — Email
> From: Petra Quill (Contractor, Copper Finch Mechanical)
> To: Ivo Merrick (Property Manager, Northbridge Lettings)
>
> Replied that parts availability and estimate details still needed checking. Did not confirm a repair option, a credit, a return visit or completion of actuator work.

<a id="entry-138"></a>
## 2026-10-10 16:28:37 UTC — 138 · Workflow receipt

<a id="entry-139"></a>
## 2026-10-10 16:28:38 UTC — 139 · Jev routed the message

- **Actor:** Jev (jev-1.13.0 · 1759 in / 284 out tokens · 306 ms)
- **Tool:** TypeSafe `system_one` · step `route_case_messages`
- **Decision:** jev_route → `clarify` (confidence 0.89)
- **Signals:** hazard 0.13 · multiple_issues 0.07 · sensitive 0.11 · states_facts 0.08 · system_instructions 0.02
- **Why:** Jev routes; Claude extracts quotes and claims. clarify is not a Jev-only route. Open tenant questions may be answered.

<a id="entry-140"></a>
## 2026-10-10 16:28:42 UTC — 140 · Claude read the message

- **Actor:** Claude (claude-opus-5 · 1994 in / 404 out tokens)
- **Tool:** Anthropic Messages API `ai.triage` (prompt property-triage-2026-10-10.3) · step `triage_case_messages`
- **Reading:** update · route `clarify` · high confidence
- **Work item:** Intermittent heating failure (radiators), hot water unaffected (other)
- **Summary:** Contractor replied that parts availability and estimate details still need checking; no repair option, credit, return visit or completion confirmed.
- **Rationale:** Contractor gave no substantive answers; essential estimate details remain outstanding.
- **Extracted:** 0 claims · 2 ambiguities · 1 issue
- **Unknown (affects route):** Contractor still has not confirmed whether the actuator can be repaired, what the estimate covers, or whether the diagnostic fee is credited.
- **Unknown (affects route):** Unknown whether anyone in the household is vulnerable while relying on a portable heater in February.

<a id="entry-141"></a>
## 2026-10-10 16:28:43 UTC — 141 · Message received: Event 017 — Email from Petra Quill (Contractor, Copper Finch Mechanical)

- **Recorded by:** demo-case_manager (case manager)
- **Reading:** queued for Jev routing / Claude triage

> Event 017 — Email
> From: Petra Quill (Contractor, Copper Finch Mechanical)
> To: Ivo Merrick (Property Manager, Northbridge Lettings)
>
> Sent two invoice records dated 10 February and said they had been prepared from the job paperwork. The message did not say whether one replaced the other, whether both amounts were payable, or whether either had been paid. Invoice B describes actuator work as completed and gives a service date of 5 February, but Petra did not attach a signed completion record or explain how that claim relates to the estimate sent later on 5 February and the 7 February parts check.

<a id="entry-142"></a>
## 2026-10-10 16:28:43 UTC — 142 · Workflow receipt

<a id="entry-143"></a>
## 2026-10-10 16:28:43 UTC — 143 · Jev routed the message

- **Actor:** Jev (jev-1.13.0 · 1820 in / 284 out tokens · 378 ms)
- **Tool:** TypeSafe `system_one` · step `route_case_messages`
- **Decision:** jev_route → `clarify` (confidence 0.94)
- **Signals:** hazard 0.10 · multiple_issues 0.09 · sensitive 0.15 · states_facts 0.76 · system_instructions 0.02
- **Why:** Jev routes; Claude extracts quotes and claims. clarify is not a Jev-only route. The message may state facts that need exact quotes. Open tenant questions may be answered.

<a id="entry-144"></a>
## 2026-10-10 16:28:50 UTC — 144 · Claude read the message

- **Actor:** Claude (claude-opus-5 · 2068 in / 621 out tokens)
- **Tool:** Anthropic Messages API `ai.triage` (prompt property-triage-2026-10-10.3) · step `triage_case_messages`
- **Reading:** update · route `clarify` · high confidence
- **Work item:** Intermittent heating failure (radiators), hot water unaffected (other)
- **Summary:** Contractor sent two invoice records dated 10 February without saying whether one supersedes the other, whether both are payable, or whether either is paid. Invoice B claims actuator work completed on 5 February, but no signed completion record and it conflicts with the later estimate and 7 February parts check.
- **Rationale:** Conflicting and unverified invoice/completion information; cannot route to close or instruct until contractor clarifies.
- **Extracted:** 1 claim · 3 ambiguities · 1 issue
- **Unknown (affects route):** Invoice B claims actuator work completed on 5 February but no signed completion record and it conflicts with the later estimate and parts check.
- **Unknown (affects route):** Two invoices dated 10 February: unclear whether one replaces the other, whether both are payable, or whether either has been paid; no comparable total including VAT established.
- **Unknown (affects route):** Contractor still has not said whether the actuator can be repaired rather than replaced, or what the estimate covers.

<a id="entry-145"></a>
## 2026-10-10 16:28:50 UTC — 145 · Claim `completion` = true

- **Actor:** Claude (extracted)
- **Status:** unverified assertion — a person or policy must accept it

> Invoice B describes actuator work as completed and gives a service date of 5 February

<a id="entry-146"></a>
## 2026-10-10 16:28:51 UTC — 146 · Message received: Event 018 — Document from Petra Quill (Contractor, Copper Finch Mechanical)

- **Recorded by:** demo-case_manager (case manager)
- **Reading:** queued for Jev routing / Claude triage

> Event 018 — Document
> From: Petra Quill (Contractor, Copper Finch Mechanical)
> To: Ivo Merrick (Property Manager, Northbridge Lettings)
>
> The received invoice records list £138 for attendance, diagnosis, actuator inspection and an operational test, and £372 for actuator supply/replacement, attendance, diagnosis and heating-system testing. Both records identify 5 February as the service date. The second record's wider description includes activities also listed on the first; neither record states whether the other is credited, cancelled or superseded.

<a id="entry-147"></a>
## 2026-10-10 16:28:51 UTC — 147 · Workflow receipt

<a id="entry-148"></a>
## 2026-10-10 16:28:51 UTC — 148 · Jev routed the message

- **Actor:** Jev (jev-1.13.0 · 1876 in / 282 out tokens · 254 ms)
- **Tool:** TypeSafe `system_one` · step `route_case_messages`
- **Decision:** jev_route → `clarify` (confidence 0.98)
- **Signals:** hazard 0.14 · multiple_issues 0.07 · sensitive 0.17 · states_facts 0.95 · system_instructions 0.02
- **Why:** Jev routes; Claude extracts quotes and claims. clarify is not a Jev-only route. The message may state facts that need exact quotes. Open tenant questions may be answered.

<a id="entry-149"></a>
## 2026-10-10 16:28:59 UTC — 149 · Claude read the message

- **Actor:** Claude (claude-opus-5 · 2205 in / 693 out tokens)
- **Tool:** Anthropic Messages API `ai.triage` (prompt property-triage-2026-10-10.3) · step `triage_case_messages`
- **Reading:** update · route `clarify` · high confidence
- **Work item:** Intermittent heating failure (radiators), hot water unaffected (other)
- **Summary:** Contractor document itemises two invoice records (£138 and £372) both dated 5 February for service, with overlapping descriptions and no statement of whether one supersedes or credits the other. No comparable total, repair option or completion evidence provided.
- **Rationale:** Billing records conflict and overlap; no comparable total or completion evidence, so clarification is needed before any authority or payment decision.
- **Extracted:** 2 claims · 4 ambiguities · 1 issue
- **Unknown (affects route):** Whether the £138 and £372 records are cumulative or whether one supersedes/credits the other; no single comparable total including VAT established.
- **Unknown:** Whether the stated amounts include VAT.
- **Unknown (affects route):** Both records give 5 February as the service date but no completion evidence is supplied; unclear whether actuator replacement was actually carried out.
- **Unknown:** Contractor still has not said whether the actuator can be repaired rather than replaced, or what the estimate covers.

<a id="entry-150"></a>
## 2026-10-10 16:28:59 UTC — 150 · Claim `total` = 138.0

- **Actor:** Claude (extracted)
- **Status:** unverified assertion — a person or policy must accept it

> The received invoice records list £138 for attendance, diagnosis, actuator inspection and an operational test

<a id="entry-151"></a>
## 2026-10-10 16:28:59 UTC — 151 · Claim `total` = 372.0

- **Actor:** Claude (extracted)
- **Status:** unverified assertion — a person or policy must accept it

> £372 for actuator supply/replacement, attendance, diagnosis and heating-system testing

<a id="entry-152"></a>
## 2026-10-10 16:28:59 UTC — 152 · Partial answer → narrower follow-up due

- **Actor:** Claude (reading)

> £372 for actuator supply/replacement, attendance, diagnosis and heating-system testing

<a id="entry-153"></a>
## 2026-10-10 16:28:59 UTC — 153 · Message received: Event 019 — Note from Ivo Merrick (Property Manager, Northbridge Lettings)

- **Recorded by:** demo-case_manager (case manager)
- **Reading:** queued for Jev routing / Claude triage

> Event 019 — Note
> From: Ivo Merrick (Property Manager, Northbridge Lettings)
> To: Ivo Merrick (Property Manager, Northbridge Lettings)
>
> Compared the received records with the file: the landlord's written authority covers diagnosis only; the £372 estimate requesting authorization was sent after the stated service date; and the 7 February exchange still had parts and estimate details outstanding. The file contains no written authorization for actuator replacement and no return-visit or completion entry.

<a id="entry-154"></a>
## 2026-10-10 16:29:00 UTC — 154 · Workflow receipt

<a id="entry-155"></a>
## 2026-10-10 16:29:00 UTC — 155 · Jev routed the message

- **Actor:** Jev (jev-1.13.0 · 1914 in / 282 out tokens · 402 ms)
- **Tool:** TypeSafe `system_one` · step `route_case_messages`
- **Decision:** jev_route → `clarify` (confidence 0.97)
- **Signals:** hazard 0.17 · multiple_issues 0.09 · sensitive 0.32 · states_facts 0.87 · system_instructions 0.03
- **Why:** Jev routes; Claude extracts quotes and claims. clarify is not a Jev-only route. The message may state facts that need exact quotes. Open tenant questions may be answered.

<a id="entry-156"></a>
## 2026-10-10 16:29:07 UTC — 156 · Claude read the message

- **Actor:** Claude (claude-opus-5 · 2242 in / 645 out tokens)
- **Tool:** Anthropic Messages API `ai.triage` (prompt property-triage-2026-10-10.3) · step `triage_case_messages`
- **Reading:** update · route `clarify` · high confidence
- **Work item:** Intermittent heating failure (radiators), hot water unaffected (other)
- **Summary:** Internal file-review note from the property manager recording that written landlord authority covers diagnosis only, that the £372 estimate was sent after the stated service date, and that the file holds no authorization for actuator replacement and no completion or return-visit entry.
- **Rationale:** Internal note confirms authority and completion gaps; cannot instruct or close until the contractor clarifies invoices, repair option and completion evidence.
- **Extracted:** 2 claims · 3 ambiguities · 1 issue
- **Unknown (affects route):** Whether the £138 and £372 invoice records are cumulative or one supersedes the other; no single comparable total including VAT established.
- **Unknown (affects route):** Whether actuator replacement was in fact carried out on 5 February; no completion evidence on file.
- **Unknown (affects route):** Whether the actuator can be repaired rather than replaced, and whether anyone in the tenant household is vulnerable given ongoing cold radiators in February.

<a id="entry-157"></a>
## 2026-10-10 16:29:08 UTC — 157 · Claim `completion` = false

- **Actor:** Claude (extracted)
- **Status:** unverified assertion — a person or policy must accept it

> no return-visit or completion entry

<a id="entry-158"></a>
## 2026-10-10 16:29:08 UTC — 158 · Partial answer → narrower follow-up due

- **Actor:** Claude (reading)

> the £372 estimate requesting authorization was sent after the stated service date; and the 7 February exchange still had parts and estimate details outstanding

<a id="entry-159"></a>
## 2026-10-10 16:29:08 UTC — 159 · Message received: Event 020 — Portal from Tessa Vane (Tenant)

- **Recorded by:** demo-case_manager (case manager)
- **Reading:** queued for Jev routing / Claude triage

> Event 020 — Portal
> From: Tessa Vane (Tenant)
> To: Ivo Merrick (Property Manager, Northbridge Lettings)
>
> Said she recalled the 5 February visit but did not know whether the actuator had been replaced. She had not seen a contractor at the property since that visit. Heating was currently working intermittently, with one radiator cooler than the others.

<a id="entry-160"></a>
## 2026-10-10 16:29:08 UTC — 160 · Workflow receipt

<a id="entry-161"></a>
## 2026-10-10 16:29:08 UTC — 161 · Jev routed the message

- **Actor:** Jev (jev-1.13.0 · 1924 in / 282 out tokens · 331 ms)
- **Tool:** TypeSafe `system_one` · step `route_case_messages`
- **Decision:** jev_route → `clarify` (confidence 0.62)
- **Signals:** hazard 0.16 · multiple_issues 0.10 · sensitive 0.12 · states_facts 0.67 · system_instructions 0.02
- **Why:** Jev routes; Claude extracts quotes and claims. clarify is not a Jev-only route. Route confidence 0.62 is below the Jev-only bar 0.8. The message may state facts that need exact quotes. Open tenant questions may be answered.

<a id="entry-162"></a>
## 2026-10-10 16:29:14 UTC — 162 · Claude read the message

- **Actor:** Claude (claude-opus-5 · 2319 in / 436 out tokens)
- **Tool:** Anthropic Messages API `ai.triage` (prompt property-triage-2026-10-10.3) · step `triage_case_messages`
- **Reading:** answer to question · route `clarify` · high confidence
- **Work item:** Intermittent heating failure (radiators), hot water unaffected (other)
- **Summary:** Tenant recalls the 5 February visit but cannot say whether the actuator was replaced, and has seen no contractor since. Heating is working intermittently with one radiator cooler than the others.
- **Rationale:** Reply adds partial information but leaves completion, pricing and vulnerability questions open, so clarification continues.
- **Extracted:** 0 claims · 2 ambiguities · 1 issue
- **Unknown (affects route):** Tenant cannot confirm whether actuator replacement took place on 5 February; no completion evidence from contractor.
- **Unknown (affects route):** Whether anyone in the household is vulnerable given ongoing cold radiators in February remains unanswered.

<a id="entry-163"></a>
## 2026-10-10 16:29:14 UTC — 163 · Partial answer → narrower follow-up due

- **Actor:** Claude (reading)

> Said she recalled the 5 February visit but did not know whether the actuator had been replaced.

<a id="entry-164"></a>
## 2026-10-10 16:29:14 UTC — 164 · Message received: Event 021 — Email from Ivo Merrick (Property Manager, Northbridge Lettings)

- **Recorded by:** demo-case_manager (case manager)
- **Reading:** queued for Jev routing / Claude triage

> Event 021 — Email
> From: Ivo Merrick (Property Manager, Northbridge Lettings)
> To: Petra Quill (Contractor, Copper Finch Mechanical)
>
> Asked what work was actually completed and on what date, whether both invoice records remained current, whether either superseded the other, and how the overlapping charges were treated. Requested the job notes, any parts record and any authorization or attendance evidence for actuator work.

<a id="entry-165"></a>
## 2026-10-10 16:29:14 UTC — 165 · Workflow receipt

<a id="entry-166"></a>
## 2026-10-10 16:29:15 UTC — 166 · Jev routed the message

- **Actor:** Jev (jev-1.13.0 · 1890 in / 282 out tokens · 249 ms)
- **Tool:** TypeSafe `system_one` · step `route_case_messages`
- **Decision:** jev_route → `clarify` (confidence 0.79)
- **Signals:** hazard 0.11 · multiple_issues 0.09 · sensitive 0.18 · states_facts 0.20 · system_instructions 0.02
- **Why:** Jev routes; Claude extracts quotes and claims. clarify is not a Jev-only route. Route confidence 0.79 is below the Jev-only bar 0.8. Open tenant questions may be answered.

<a id="entry-167"></a>
## 2026-10-10 16:29:21 UTC — 167 · Claude read the message

- **Actor:** Claude (claude-opus-5 · 2290 in / 525 out tokens)
- **Tool:** Anthropic Messages API `ai.triage` (prompt property-triage-2026-10-10.3) · step `triage_case_messages`
- **Reading:** update · route `clarify` · high confidence
- **Work item:** Intermittent heating failure (radiators), hot water unaffected (other)
- **Summary:** Property manager asked the contractor to confirm what work was completed and when, whether both invoice records remain current or one supersedes the other, how overlapping charges are treated, and requested job notes, parts records and authorisation/attendance evidence for the actuator work.
- **Rationale:** Outbound chase to contractor seeking completion, authorisation and billing clarification; essential facts still missing, so clarify stands.
- **Extracted:** 0 claims · 3 ambiguities · 1 issue
- **Unknown (affects route):** Whether actuator replacement was carried out on 5 February remains unconfirmed; no completion evidence, job notes or parts record supplied.
- **Unknown (affects route):** Whether both invoice records (£138 and £372) are payable or one supersedes the other, and how overlapping charges are treated.
- **Unknown:** Whether anyone in the household is vulnerable given ongoing cold radiators in February is still unanswered.

<a id="entry-168"></a>
## 2026-10-10 16:29:21 UTC — 168 · Message received: Event 022 — Email from Petra Quill (Contractor, Copper Finch Mechanical)

- **Recorded by:** demo-case_manager (case manager)
- **Reading:** queued for Jev routing / Claude triage

> Event 022 — Email
> From: Petra Quill (Contractor, Copper Finch Mechanical)
> To: Ivo Merrick (Property Manager, Northbridge Lettings)
>
> Replied that she was checking the records and could not yet confirm whether the invoice entries represented separate chargeable work or whether one record replaced the other. She supplied no further completion evidence, revised invoice or parts confirmation.

<a id="entry-169"></a>
## 2026-10-10 16:29:22 UTC — 169 · Workflow receipt

<a id="entry-170"></a>
## 2026-10-10 16:29:22 UTC — 170 · Jev routed the message

- **Actor:** Jev (jev-1.13.0 · 1852 in / 282 out tokens · 228 ms)
- **Tool:** TypeSafe `system_one` · step `route_case_messages`
- **Decision:** jev_route → `clarify` (confidence 0.96)
- **Signals:** hazard 0.09 · multiple_issues 0.09 · sensitive 0.11 · states_facts 0.07 · system_instructions 0.02
- **Why:** Jev routes; Claude extracts quotes and claims. clarify is not a Jev-only route. Open tenant questions may be answered.

<a id="entry-171"></a>
## 2026-10-10 16:29:28 UTC — 171 · Claude read the message

- **Actor:** Claude (claude-opus-5 · 2296 in / 520 out tokens)
- **Tool:** Anthropic Messages API `ai.triage` (prompt property-triage-2026-10-10.3) · step `triage_case_messages`
- **Reading:** answer to question · route `clarify` · high confidence
- **Work item:** Intermittent heating failure (radiators), hot water unaffected (other)
- **Summary:** Contractor Petra Quill replied that she is still checking the records and cannot yet confirm whether the two invoice entries are separate chargeable work or whether one supersedes the other. No completion evidence, revised invoice or parts record was supplied.
- **Rationale:** Contractor provided no new substantive information; essential billing and completion facts remain outstanding, so clarification is still required.
- **Extracted:** 0 claims · 3 ambiguities · 1 issue
- **Unknown (affects route):** Still unconfirmed whether actuator replacement was carried out on 5 February; no completion evidence, job notes or parts record supplied.
- **Unknown:** Whether both invoice records (£138 and £372) are payable or one supersedes the other, and how overlapping charges are treated.
- **Unknown:** No answer yet on whether the actuator can be repaired rather than replaced, or whether £372 inc VAT covers all parts, labour and testing.

<a id="entry-172"></a>
## 2026-10-10 16:29:29 UTC — 172 · Message received: Event 023 — Email from Ivo Merrick (Property Manager, Northbridge Lettings)

- **Recorded by:** demo-case_manager (case manager)
- **Reading:** queued for Jev routing / Claude triage

> Event 023 — Email
> From: Ivo Merrick (Property Manager, Northbridge Lettings)
> To: Soren Dallow (Landlord)
>
> The two invoice records remain on file; there is no recorded payment, confirmed supersession or authorization for actuator work. The tenant reports intermittent heating and has not confirmed replacement. Please advise how you wish to proceed on the unresolved records and whether any further work or expenditure is authorized.

<a id="entry-173"></a>
## 2026-10-10 16:29:29 UTC — 173 · Workflow receipt

<a id="entry-174"></a>
## 2026-10-10 16:29:29 UTC — 174 · Jev routed the message

- **Actor:** Jev (jev-1.13.0 · 1836 in / 282 out tokens · 214 ms)
- **Tool:** TypeSafe `system_one` · step `route_case_messages`
- **Decision:** jev_route → `clarify` (confidence 0.86)
- **Signals:** hazard 0.11 · multiple_issues 0.09 · sensitive 0.19 · states_facts 0.19 · system_instructions 0.02
- **Why:** Jev routes; Claude extracts quotes and claims. clarify is not a Jev-only route. Open tenant questions may be answered.

<a id="entry-175"></a>
## 2026-10-10 16:29:34 UTC — 175 · Claude read the message

- **Actor:** Claude (claude-opus-5 · 2281 in / 395 out tokens)
- **Tool:** Anthropic Messages API `ai.triage` (prompt property-triage-2026-10-10.3) · step `triage_case_messages`
- **Reading:** update · route `clarify` · high confidence
- **Work item:** Intermittent heating failure (radiators), hot water unaffected (other)
- **Summary:** Property manager updates the landlord that two invoice records remain unresolved with no payment, supersession or authorisation for actuator work, and the tenant still reports intermittent heating. He asks the landlord how to proceed and whether further work or expenditure is authorised.
- **Rationale:** Authorisation and completion evidence remain unresolved; message seeks landlord instruction, so clarify stands.
- **Extracted:** 0 claims · 1 ambiguity · 1 issue
- **Unknown (affects route):** Landlord's decision on the unresolved invoice records and whether further work or expenditure is authorised is still outstanding; contractor has not supplied completion evidence, job notes or parts record.

<a id="entry-176"></a>
## 2026-10-10 16:29:34 UTC — 176 · Message received: Attachment invoice-NBL-CFM-250210-A.pdf (PDF text extraction)

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

<a id="entry-177"></a>
## 2026-10-10 16:29:34 UTC — 177 · Workflow receipt

<a id="entry-178"></a>
## 2026-10-10 16:29:35 UTC — 178 · Jev routed the message

- **Actor:** Jev (jev-1.13.0 · 1921 in / 282 out tokens · 351 ms)
- **Tool:** TypeSafe `system_one` · step `route_case_messages`
- **Decision:** jev_route → `clarify` (confidence 0.67)
- **Signals:** hazard 0.15 · multiple_issues 0.08 · sensitive 0.25 · states_facts 0.93 · system_instructions 0.04
- **Why:** Jev routes; Claude extracts quotes and claims. clarify is not a Jev-only route. Route confidence 0.67 is below the Jev-only bar 0.8. The message may state facts that need exact quotes. Open tenant questions may be answered.

<a id="entry-179"></a>
## 2026-10-10 16:29:41 UTC — 179 · Claude read the message

- **Actor:** Claude (claude-opus-5 · 2387 in / 519 out tokens)
- **Tool:** Anthropic Messages API `ai.triage` (prompt property-triage-2026-10-10.3) · step `triage_case_messages`
- **Reading:** update · route `clarify` · medium confidence
- **Work item:** Intermittent heating failure (radiators), hot water unaffected (other)
- **Summary:** Invoice NBL-CFM-250210-A from Copper Finch Mechanical dated 10 February 2025 for £138.00 inc VAT covering attendance, diagnosis, actuator inspection and operational test on 5 February. It does not address the overlapping £372 record, actuator replacement authorisation or completion evidence.
- **Rationale:** Document only restates the £138 charge; the overlapping invoice, authority and completion questions remain open, so clarification is still needed.
- **Extracted:** 1 claim · 2 ambiguities · 1 issue
- **Unknown (affects route):** Whether this £138 invoice supersedes or sits alongside the £372 record remains unstated; no parts record, completion evidence or authorisation for actuator replacement is supplied.
- **Unknown (affects route):** No confirmation whether the actuator was replaced or the heating fault resolved.

<a id="entry-180"></a>
## 2026-10-10 16:29:41 UTC — 180 · Claim `total` = 138.0

- **Actor:** Claude (extracted)
- **Status:** unverified assertion — a person or policy must accept it

> Total including VAT: £138.00

<a id="entry-181"></a>
## 2026-10-10 16:29:41 UTC — 181 · Message received: Attachment invoice-NBL-CFM-250210-B.pdf (PDF text extraction)

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

<a id="entry-182"></a>
## 2026-10-10 16:29:41 UTC — 182 · Workflow receipt

<a id="entry-183"></a>
## 2026-10-10 16:29:42 UTC — 183 · Jev routed the message

- **Actor:** Jev (jev-1.13.0 · 1994 in / 282 out tokens · 293 ms)
- **Tool:** TypeSafe `system_one` · step `route_case_messages`
- **Decision:** jev_route → `clarify` (confidence 0.80)
- **Signals:** hazard 0.23 · multiple_issues 0.09 · sensitive 0.21 · states_facts 0.94 · system_instructions 0.03
- **Why:** Jev routes; Claude extracts quotes and claims. clarify is not a Jev-only route. The message may state facts that need exact quotes. Open tenant questions may be answered.

<a id="entry-184"></a>
## 2026-10-10 16:29:50 UTC — 184 · Claude read the message

- **Actor:** Claude (claude-opus-5 · 2472 in / 645 out tokens)
- **Tool:** Anthropic Messages API `ai.triage` (prompt property-triage-2026-10-10.3) · step `triage_case_messages`
- **Reading:** update · route `clarify` · high confidence
- **Work item:** Intermittent heating failure (radiators), hot water unaffected (other)
- **Summary:** Second invoice from Copper Finch Mechanical (NBL-CFM-250210-B) for £372.00 inc VAT covering heating valve actuator supply and replacement, same 5 February service date as the £138.00 invoice A. It is still unstated whether this supersedes or duplicates the other record, and no authorisation or completion evidence is provided.
- **Rationale:** Billing document adds a second overlapping invoice without authorisation or completion evidence; clarification needed before any payment or further action.
- **Extracted:** 1 claim · 3 ambiguities · 1 issue
- **Unknown (affects route):** Whether invoice B (£372.00) supersedes or sits alongside invoice A (£138.00) for the same 5 February service date; overlapping attendance and diagnosis charges are unresolved.
- **Unknown (affects route):** No parts record, attendance evidence or confirmation that the actuator replacement was actually carried out or that the heating fault is resolved.
- **Unknown (affects route):** No written landlord authorisation on file for actuator replacement; authority covered diagnosis only.

<a id="entry-185"></a>
## 2026-10-10 16:29:50 UTC — 185 · Claim `total` = 372.0

- **Actor:** Claude (extracted)
- **Status:** unverified assertion — a person or policy must accept it

> Total including VAT: £372.00

<a id="entry-186"></a>
## 2026-10-10 16:29:50 UTC — 186 · Partial answer → narrower follow-up due

- **Actor:** Claude (reading)

> Heating valve actuator supply and replacement, attendance, fault diagnosis and heating-
> system testing.
