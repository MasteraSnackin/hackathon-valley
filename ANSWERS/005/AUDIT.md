# Case ce1ad40fc558 audit trail

Heating repair invoice and payment details · 18 Brindlewick Row, Vellmere, ZZ1 1ZZ · status open · stage HUMAN REVIEW

- **Case ID:** `ce1ad40fc55840fd9b633c94d6e45e9d`
- **Entries:** 189 (from 504 immutable records; bookkeeping and unchanged assessments omitted)
- **Raw records:** [records.jsonl](records.jsonl)
- All outbound tools are simulated adapters; no real tenant, landlord or contractor was contacted.

<a id="entry-001"></a>
## 2026-10-10 15:58:48 UTC — 001 · Message received: Intake report

- **Recorded by:** demo-case_manager (case manager)
- **Reading:** queued for Jev routing / Claude triage

> Event 001 — Portal
> From: Iris Bell (Tenant)
> To: Maya Chen (Property Manager, Northbridge Lettings)
>
> Reports that the heating stopped overnight. The display on the hall thermostat is blank. Hot water is still available from the immersion switch.

<a id="entry-002"></a>
## 2026-10-10 15:58:48 UTC — 002 · Human review opened: `identity`

- **Actor:** Policy engine
- **Owner:** case manager · rule `require-identity`
- **Expires:** 2026-10-12 15:58:48 UTC

> Verify the person, property and work item mapping.

<a id="entry-003"></a>
## 2026-10-10 15:58:48 UTC — 003 · Human review opened: `route`

- **Actor:** Policy engine
- **Owner:** case manager · rule `require-route`
- **Expires:** 2026-10-12 15:58:48 UTC

> Verify the recipient and permitted communication route.

<a id="entry-004"></a>
## 2026-10-10 15:58:48 UTC — 004 · Policy gates → HUMAN REVIEW

- **Actor:** Policy engine (rules v1, `domain.evaluate`)
- **Outcome:** HUMAN REVIEW · owner case manager
- **Blockers:** `identity` UNKNOWN → HUMAN REVIEW; `route` UNKNOWN → HUMAN REVIEW; `triage` UNKNOWN → WAIT
- **Next step:** Verify the person, property and work item mapping.

<a id="entry-005"></a>
## 2026-10-10 15:58:48 UTC — 005 · Workflow receipt

<a id="entry-006"></a>
## 2026-10-10 15:58:48 UTC — 006 · Jev routed the message

- **Actor:** Jev (jev-1.13.0 · 1286 in / 284 out tokens · 304 ms)
- **Tool:** TypeSafe `system_one` · step `route_case_messages`
- **Decision:** jev_route → `urgent_hazard` (confidence 0.87)
- **Signals:** hazard 0.31 · multiple_issues 0.25 · sensitive 0.03 · states_facts 0.02 · system_instructions 0.01
- **Why:** Possible hazard (Jev p=0.31); a person takes over before any automated contact.

<a id="entry-007"></a>
## 2026-10-10 15:58:56 UTC — 007 · Claude read the message

- **Actor:** Claude (claude-opus-5 · 379 in / 474 out tokens)
- **Tool:** Anthropic Messages API `ai.triage` (prompt property-triage-2026-10-10.3) · step `triage_case_messages`
- **Reading:** new request · route `urgent_hazard` · medium confidence
- **Work item:** Heating not working, blank thermostat display (appliance)
- **Summary:** Tenant reports heating stopped overnight with a blank hall thermostat display; hot water still available via the immersion switch.
- **Rationale:** Complete loss of heating could be urgent depending on occupants; router escalated for human review before contact.
- **Extracted:** 0 claims · 3 ambiguities · 1 issue
- **Unknown (affects route):** Is anyone in the household vulnerable or at risk from loss of heating, and is the boiler showing any fault code?
- **Unknown:** Tenant's availability for an engineer visit is not stated.
- **Unknown:** No access arrangement or consent to enter given.

<a id="entry-008"></a>
## 2026-10-10 15:58:56 UTC — 008 · Proposed action → `clarify`

- **Actor:** Triage reading (route `urgent_hazard`)
- **Work item:** Heating not working, blank thermostat display
- **Action revision:** 2

<a id="entry-009"></a>
## 2026-10-10 15:58:56 UTC — 009 · Claim `urgent` = true

- **Actor:** Claude (extracted)
- **Status:** unverified assertion — a person or policy must accept it

> Reports that the heating stopped overnight. The display on the hall thermostat is blank.

<a id="entry-010"></a>
## 2026-10-10 15:58:56 UTC — 010 · Human review opened: `identity`

- **Actor:** Policy engine
- **Owner:** case manager · rule `require-identity`
- **Expires:** 2026-10-12 15:58:56 UTC

> Verify the person, property and work item mapping.

<a id="entry-011"></a>
## 2026-10-10 15:58:56 UTC — 011 · Human review opened: `route`

- **Actor:** Policy engine
- **Owner:** case manager · rule `require-route`
- **Expires:** 2026-10-12 15:58:56 UTC

> Verify the recipient and permitted communication route.

<a id="entry-012"></a>
## 2026-10-10 15:58:56 UTC — 012 · Human review opened: `triage`

- **Actor:** Policy engine
- **Owner:** case manager · rule `require-triage`
- **Expires:** 2026-10-12 15:58:56 UTC

> Claude read this as a possible urgent hazard. A case manager must take over now and apply the urgent procedure.

<a id="entry-013"></a>
## 2026-10-10 15:58:56 UTC — 013 · Policy gates → HUMAN REVIEW

- **Actor:** Policy engine (rules v1, `domain.evaluate`)
- **Outcome:** HUMAN REVIEW · owner case manager
- **Blockers:** `identity` UNKNOWN → HUMAN REVIEW; `route` UNKNOWN → HUMAN REVIEW; `triage` UNKNOWN → HUMAN REVIEW
- **Next step:** Verify the person, property and work item mapping.

<a id="entry-014"></a>
## 2026-10-10 15:58:56 UTC — 014 · Message received: Event 002 — Update from Northbridge Lettings workflow (System)

- **Recorded by:** demo-case_manager (case manager)
- **Reading:** queued for Jev routing / Claude triage

> Event 002 — Update
> From: Northbridge Lettings workflow (System)
> To: Iris Bell (Tenant)
>
> Maintenance request NBL-005-184 opened and assigned for review.

<a id="entry-015"></a>
## 2026-10-10 15:58:56 UTC — 015 · Policy gates → HUMAN REVIEW

- **Actor:** Policy engine (rules v1, `domain.evaluate`)
- **Outcome:** HUMAN REVIEW · owner case manager
- **Blockers:** `identity` UNKNOWN → HUMAN REVIEW; `route` UNKNOWN → HUMAN REVIEW; `triage` UNKNOWN → WAIT
- **Next step:** Verify the person, property and work item mapping.

<a id="entry-016"></a>
## 2026-10-10 15:58:56 UTC — 016 · Workflow receipt

<a id="entry-017"></a>
## 2026-10-10 15:58:56 UTC — 017 · Jev routed the message

- **Actor:** Jev (jev-1.13.0 · 1412 in / 284 out tokens · 286 ms)
- **Tool:** TypeSafe `system_one` · step `route_case_messages`
- **Decision:** claude → no route
- **Signals:** hazard 0.12 · multiple_issues 0.04 · sensitive 0.03 · states_facts 0.02 · system_instructions 0.03
- **Why:** Jev route confidence 0.47 is below 0.5.

<a id="entry-018"></a>
## 2026-10-10 15:59:02 UTC — 018 · Claude read the message

- **Actor:** Claude (claude-opus-5 · 530 in / 376 out tokens)
- **Tool:** Anthropic Messages API `ai.triage` (prompt property-triage-2026-10-10.3) · step `triage_case_messages`
- **Reading:** not actionable · route `none` · high confidence
- **Summary:** Automated acknowledgement from the Northbridge Lettings workflow confirming maintenance request NBL-005-184 has been opened and assigned for review. No new information about the heating fault.
- **Rationale:** System-generated case acknowledgement with no maintenance content; nothing to action or route beyond the existing case.
- **Extracted:** 0 claims · 1 ambiguity · 0 issues
- **Unknown (affects route):** Still unknown whether anyone in the household is vulnerable or at risk from the loss of heating, and whether the boiler shows a fault code.

<a id="entry-019"></a>
## 2026-10-10 15:59:02 UTC — 019 · Policy gates → HUMAN REVIEW

- **Actor:** Policy engine (rules v1, `domain.evaluate`)
- **Outcome:** HUMAN REVIEW · owner case manager
- **Blockers:** `identity` UNKNOWN → HUMAN REVIEW; `route` UNKNOWN → HUMAN REVIEW; `triage` UNKNOWN → HUMAN REVIEW
- **Next step:** Verify the person, property and work item mapping.

<a id="entry-020"></a>
## 2026-10-10 15:59:02 UTC — 020 · Message received: Event 003 — Email from Maya Chen (Property Manager, Northbridge Lettings)

- **Recorded by:** demo-case_manager (case manager)
- **Reading:** queued for Jev routing / Claude triage

> Event 003 — Email
> From: Maya Chen (Property Manager, Northbridge Lettings)
> To: Iris Bell (Tenant)
>
> Asks whether the thermostat display shows anything and whether any warning lights, leaks, or unusual smells are present.

<a id="entry-021"></a>
## 2026-10-10 15:59:02 UTC — 021 · Policy gates → HUMAN REVIEW

- **Actor:** Policy engine (rules v1, `domain.evaluate`)
- **Outcome:** HUMAN REVIEW · owner case manager
- **Blockers:** `identity` UNKNOWN → HUMAN REVIEW; `route` UNKNOWN → HUMAN REVIEW; `triage` UNKNOWN → WAIT
- **Next step:** Verify the person, property and work item mapping.

<a id="entry-022"></a>
## 2026-10-10 15:59:02 UTC — 022 · Workflow receipt

<a id="entry-023"></a>
## 2026-10-10 15:59:03 UTC — 023 · Jev routed the message

- **Actor:** Jev (jev-1.13.0 · 1504 in / 284 out tokens · 650 ms)
- **Tool:** TypeSafe `system_one` · step `route_case_messages`
- **Decision:** jev_route → `clarify` (confidence 0.81)
- **Signals:** hazard 0.21 · multiple_issues 0.05 · sensitive 0.03 · states_facts 0.02 · system_instructions 0.01
- **Why:** Jev routes; Claude extracts quotes and claims. clarify is not a Jev-only route.

<a id="entry-024"></a>
## 2026-10-10 15:59:08 UTC — 024 · Claude read the message

- **Actor:** Claude (claude-opus-5 · 790 in / 327 out tokens)
- **Tool:** Anthropic Messages API `ai.triage` (prompt property-triage-2026-10-10.3) · step `triage_case_messages`
- **Reading:** update · route `clarify` · high confidence
- **Work item:** Heating not working, blank thermostat display (appliance)
- **Summary:** Property manager emails the tenant asking for more detail about the thermostat display and whether there are warning lights, leaks or unusual smells. No new facts or decisions provided.
- **Rationale:** Agent is seeking diagnostic information; the case cannot progress until the tenant replies.
- **Extracted:** 0 claims · 1 ambiguity · 1 issue
- **Unknown (affects route):** Awaiting tenant's answer on thermostat display state, warning lights, leaks or smells; also unknown whether anyone in the household is vulnerable or whether the boiler shows a fault code.

<a id="entry-025"></a>
## 2026-10-10 15:59:08 UTC — 025 · Policy gates → HUMAN REVIEW

- **Actor:** Policy engine (rules v1, `domain.evaluate`)
- **Outcome:** HUMAN REVIEW · owner case manager
- **Blockers:** `identity` UNKNOWN → HUMAN REVIEW; `route` UNKNOWN → HUMAN REVIEW; `triage` UNKNOWN → HUMAN REVIEW
- **Next step:** Verify the person, property and work item mapping.

<a id="entry-026"></a>
## 2026-10-10 15:59:08 UTC — 026 · Message received: Event 004 — Portal from Iris Bell (Tenant)

- **Recorded by:** demo-case_manager (case manager)
- **Reading:** queued for Jev routing / Claude triage

> Event 004 — Portal
> From: Iris Bell (Tenant)
> To: Maya Chen (Property Manager, Northbridge Lettings)
>
> Says the thermostat display is blank. There is no visible leak or unusual smell, and the household can use the immersion for hot water.

<a id="entry-027"></a>
## 2026-10-10 15:59:08 UTC — 027 · Policy gates → HUMAN REVIEW

- **Actor:** Policy engine (rules v1, `domain.evaluate`)
- **Outcome:** HUMAN REVIEW · owner case manager
- **Blockers:** `identity` UNKNOWN → HUMAN REVIEW; `route` UNKNOWN → HUMAN REVIEW; `triage` UNKNOWN → WAIT
- **Next step:** Verify the person, property and work item mapping.

<a id="entry-028"></a>
## 2026-10-10 15:59:08 UTC — 028 · Workflow receipt

<a id="entry-029"></a>
## 2026-10-10 15:59:08 UTC — 029 · Jev routed the message

- **Actor:** Jev (jev-1.13.0 · 1593 in / 284 out tokens · 333 ms)
- **Tool:** TypeSafe `system_one` · step `route_case_messages`
- **Decision:** jev_route → `request_quote` (confidence 0.61)
- **Signals:** hazard 0.11 · multiple_issues 0.04 · sensitive 0.03 · states_facts 0.02 · system_instructions 0.02
- **Why:** Jev routes; Claude extracts quotes and claims. Route confidence 0.61 is below the Jev-only bar 0.8. A route change on an existing case.

<a id="entry-030"></a>
## 2026-10-10 15:59:14 UTC — 030 · Claude read the message

- **Actor:** Claude (claude-opus-5 · 1012 in / 359 out tokens)
- **Tool:** Anthropic Messages API `ai.triage` (prompt property-triage-2026-10-10.3) · step `triage_case_messages`
- **Reading:** answer to question · route `request_quote` · medium confidence
- **Work item:** Heating not working, blank thermostat display (appliance)
- **Summary:** Tenant confirms the thermostat display is blank with no leaks or unusual smells, and hot water is available via the immersion. Heating remains out.
- **Rationale:** Tenant answered the diagnostic questions; no hazard indicators, so the defect needs a contractor assessment/quote.
- **Extracted:** 0 claims · 2 ambiguities · 1 issue
- **Unknown (affects route):** Unknown whether the boiler itself shows a fault code or warning lights, and whether anyone in the household is vulnerable (no heating).
- **Unknown:** No access or appointment availability given for an engineer visit.

<a id="entry-031"></a>
## 2026-10-10 15:59:14 UTC — 031 · Proposed action → `request_quote`

- **Actor:** Triage reading (route `request_quote`)
- **Work item:** Heating not working, blank thermostat display
- **Action revision:** 3

<a id="entry-032"></a>
## 2026-10-10 15:59:14 UTC — 032 · Human review opened: `identity`

- **Actor:** Policy engine
- **Owner:** case manager · rule `require-identity`
- **Expires:** 2026-10-12 15:59:14 UTC

> Verify the person, property and work item mapping.

<a id="entry-033"></a>
## 2026-10-10 15:59:14 UTC — 033 · Human review opened: `route`

- **Actor:** Policy engine
- **Owner:** case manager · rule `require-route`
- **Expires:** 2026-10-12 15:59:14 UTC

> Verify the recipient and permitted communication route.

<a id="entry-034"></a>
## 2026-10-10 15:59:14 UTC — 034 · Human review opened: `classification`

- **Actor:** Policy engine
- **Owner:** case manager · rule `require-classification`
- **Expires:** 2026-10-12 15:59:14 UTC

> Confirm that the category and work item match the source request. A verified route is required before asking externally.

<a id="entry-035"></a>
## 2026-10-10 15:59:14 UTC — 035 · Human review opened: `triage`

- **Actor:** Policy engine
- **Owner:** case manager · rule `require-triage`
- **Expires:** 2026-10-12 15:59:14 UTC

> Clarify before routing: Unknown whether the boiler itself shows a fault code or warning lights, and whether anyone in the household is vulnerable (no heating). A verified route is required before asking externally.

<a id="entry-036"></a>
## 2026-10-10 15:59:14 UTC — 036 · Policy gates → HUMAN REVIEW

- **Actor:** Policy engine (rules v1, `domain.evaluate`)
- **Outcome:** HUMAN REVIEW · owner case manager
- **Blockers:** `identity` UNKNOWN → HUMAN REVIEW; `route` UNKNOWN → HUMAN REVIEW; `classification` UNKNOWN → HUMAN REVIEW; `triage` UNKNOWN → HUMAN REVIEW
- **Next step:** Verify the person, property and work item mapping.

<a id="entry-037"></a>
## 2026-10-10 15:59:14 UTC — 037 · Message received: Event 005 — Email from Maya Chen (Property Manager, Northbridge Lettings)

- **Recorded by:** demo-case_manager (case manager)
- **Reading:** queued for Jev routing / Claude triage

> Event 005 — Email
> From: Maya Chen (Property Manager, Northbridge Lettings)
> To: Rowan Pike (Contractor, Hearthline Heating)
>
> Requests an inspection and diagnostic report for the heating fault. Asks Rowan to contact the tenant to arrange access and to obtain approval before undertaking work beyond diagnosis.

<a id="entry-038"></a>
## 2026-10-10 15:59:14 UTC — 038 · Policy gates → HUMAN REVIEW

- **Actor:** Policy engine (rules v1, `domain.evaluate`)
- **Outcome:** HUMAN REVIEW · owner case manager
- **Blockers:** `identity` UNKNOWN → HUMAN REVIEW; `route` UNKNOWN → HUMAN REVIEW; `classification` UNKNOWN → HUMAN REVIEW; `triage` UNKNOWN → WAIT
- **Next step:** Verify the person, property and work item mapping.

<a id="entry-039"></a>
## 2026-10-10 15:59:14 UTC — 039 · Workflow receipt

<a id="entry-040"></a>
## 2026-10-10 15:59:15 UTC — 040 · Jev routed the message

- **Actor:** Jev (jev-1.13.0 · 1626 in / 284 out tokens · 328 ms)
- **Tool:** TypeSafe `system_one` · step `route_case_messages`
- **Decision:** jev_route → `request_quote` (confidence 0.68)
- **Signals:** hazard 0.10 · multiple_issues 0.03 · sensitive 0.03 · states_facts 0.11 · system_instructions 0.02
- **Why:** Jev routes; Claude extracts quotes and claims. Route confidence 0.68 is below the Jev-only bar 0.8.

<a id="entry-041"></a>
## 2026-10-10 15:59:19 UTC — 041 · Claude read the message

- **Actor:** Claude (claude-opus-5 · 1209 in / 378 out tokens)
- **Tool:** Anthropic Messages API `ai.triage` (prompt property-triage-2026-10-10.3) · step `triage_case_messages`
- **Reading:** update · route `request_quote` · high confidence
- **Work item:** Heating not working, blank thermostat display (appliance)
- **Summary:** Property manager instructs contractor Hearthline Heating to inspect and provide a diagnostic report for the heating fault, asking them to arrange access with the tenant and get approval before any work beyond diagnosis.
- **Rationale:** Diagnostic/assessment instructed before any repair authority; matches request_quote stage.
- **Extracted:** 1 claim · 2 ambiguities · 1 issue
- **Unknown:** No appointment date or time agreed yet; contractor to contact tenant directly.
- **Unknown:** Tenant has not yet granted access for the contractor visit.

<a id="entry-042"></a>
## 2026-10-10 15:59:19 UTC — 042 · Claim `classification` = "appliance"

- **Actor:** Claude (extracted)
- **Status:** unverified assertion — a person or policy must accept it

> Requests an inspection and diagnostic report for the heating fault.

<a id="entry-043"></a>
## 2026-10-10 15:59:19 UTC — 043 · Human review opened: `classification`

- **Actor:** Policy engine
- **Owner:** case manager · rule `require-classification`
- **Expires:** 2026-10-12 15:59:19 UTC

> Confirm that the category and work item match the source request. A verified route is required before asking externally.

<a id="entry-044"></a>
## 2026-10-10 15:59:19 UTC — 044 · Review superseded

- **Why:** Relevant evidence or current blockers changed; assess the current review.

<a id="entry-045"></a>
## 2026-10-10 15:59:19 UTC — 045 · Review superseded

- **Why:** Relevant evidence or current blockers changed; assess the current review.

<a id="entry-046"></a>
## 2026-10-10 15:59:19 UTC — 046 · Policy gates → HUMAN REVIEW

- **Actor:** Policy engine (rules v1, `domain.evaluate`)
- **Outcome:** HUMAN REVIEW · owner case manager
- **Blockers:** `identity` UNKNOWN → HUMAN REVIEW; `route` UNKNOWN → HUMAN REVIEW; `classification` UNKNOWN → HUMAN REVIEW
- **Next step:** Verify the person, property and work item mapping.

<a id="entry-047"></a>
## 2026-10-10 15:59:20 UTC — 047 · Message received: Event 006 — Email from Rowan Pike (Contractor, Hearthline Heating)

- **Recorded by:** demo-case_manager (case manager)
- **Reading:** queued for Jev routing / Claude triage

> Event 006 — Email
> From: Rowan Pike (Contractor, Hearthline Heating)
> To: Maya Chen (Property Manager, Northbridge Lettings)
>
> Confirms availability the following morning. Says the inspection charge is £95 plus VAT and that any repair would be quoted separately.

<a id="entry-048"></a>
## 2026-10-10 15:59:20 UTC — 048 · Policy gates → HUMAN REVIEW

- **Actor:** Policy engine (rules v1, `domain.evaluate`)
- **Outcome:** HUMAN REVIEW · owner case manager
- **Blockers:** `identity` UNKNOWN → HUMAN REVIEW; `route` UNKNOWN → HUMAN REVIEW; `classification` UNKNOWN → HUMAN REVIEW; `triage` UNKNOWN → WAIT
- **Next step:** Verify the person, property and work item mapping.

<a id="entry-049"></a>
## 2026-10-10 15:59:20 UTC — 049 · Workflow receipt

<a id="entry-050"></a>
## 2026-10-10 15:59:20 UTC — 050 · Jev routed the message

- **Actor:** Jev (jev-1.13.0 · 1647 in / 286 out tokens · 308 ms)
- **Tool:** TypeSafe `system_one` · step `route_case_messages`
- **Decision:** jev_route → `confirm_appointment` (confidence 0.56)
- **Signals:** hazard 0.07 · multiple_issues 0.03 · sensitive 0.02 · states_facts 0.95 · system_instructions 0.01
- **Why:** Jev routes; Claude extracts quotes and claims. confirm_appointment is not a Jev-only route. Route confidence 0.56 is below the Jev-only bar 0.8. The message may state facts that need exact quotes. A route change on an existing case.

<a id="entry-051"></a>
## 2026-10-10 15:59:27 UTC — 051 · Claude read the message

- **Actor:** Claude (claude-opus-5 · 1401 in / 504 out tokens)
- **Tool:** Anthropic Messages API `ai.triage` (prompt property-triage-2026-10-10.3) · step `triage_case_messages`
- **Reading:** access or appointment · route `confirm_appointment` · high confidence
- **Work item:** Heating not working, blank thermostat display (appliance)
- **Summary:** Contractor Rowan Pike confirms availability the following morning for the heating inspection and states the inspection charge is £95 plus VAT, with any repair quoted separately.
- **Rationale:** Contractor is arranging the visit for a known job; router's confirm_appointment fits, with the inspection price recorded as a total claim.
- **Extracted:** 1 claim · 2 ambiguities · 1 issue
- **Unknown:** "The following morning" gives no precise date or time, and no appointment has been agreed with the tenant yet.
- **Unknown:** No confirmation that the tenant has been contacted and granted access for the visit.

<a id="entry-052"></a>
## 2026-10-10 15:59:27 UTC — 052 · Proposed action → `confirm_appointment`

- **Actor:** Triage reading (route `confirm_appointment`)
- **Work item:** Heating not working, blank thermostat display
- **Action revision:** 4

<a id="entry-053"></a>
## 2026-10-10 15:59:27 UTC — 053 · Claim `total` = 114.0

- **Actor:** Claude (extracted)
- **Status:** unverified assertion — a person or policy must accept it

> the inspection charge is £95 plus VAT

<a id="entry-054"></a>
## 2026-10-10 15:59:27 UTC — 054 · Human review opened: `identity`

- **Actor:** Policy engine
- **Owner:** case manager · rule `require-identity`
- **Expires:** 2026-10-12 15:59:27 UTC

> Verify the person, property and work item mapping.

<a id="entry-055"></a>
## 2026-10-10 15:59:27 UTC — 055 · Human review opened: `route`

- **Actor:** Policy engine
- **Owner:** case manager · rule `require-route`
- **Expires:** 2026-10-12 15:59:27 UTC

> Verify the recipient and permitted communication route.

<a id="entry-056"></a>
## 2026-10-10 15:59:27 UTC — 056 · Human review opened: `access`

- **Actor:** Policy engine
- **Owner:** access officer · rule `require-access`
- **Expires:** 2026-10-12 15:59:27 UTC

> Record consent for this visit and access method from the authorised person. A verified route is required before asking externally.

<a id="entry-057"></a>
## 2026-10-10 15:59:27 UTC — 057 · Human review opened: `authority`

- **Actor:** Policy engine
- **Owner:** approver · rule `require-authority`
- **Expires:** 2026-10-12 15:59:27 UTC

> Obtain authority for this work item, provider and action.

<a id="entry-058"></a>
## 2026-10-10 15:59:27 UTC — 058 · Human review opened: `schedule`

- **Actor:** Policy engine
- **Owner:** case manager · rule `require-schedule`
- **Expires:** 2026-10-12 15:59:27 UTC

> Confirm the active appointment with a precise date and time. A verified route is required before asking externally.

<a id="entry-059"></a>
## 2026-10-10 15:59:27 UTC — 059 · Policy gates → HUMAN REVIEW

- **Actor:** Policy engine (rules v1, `domain.evaluate`)
- **Outcome:** HUMAN REVIEW · owner case manager
- **Blockers:** `identity` UNKNOWN → HUMAN REVIEW; `route` UNKNOWN → HUMAN REVIEW; `access` UNKNOWN → HUMAN REVIEW; `authority` UNKNOWN → HUMAN REVIEW; `schedule` UNKNOWN → HUMAN REVIEW
- **Next step:** Verify the person, property and work item mapping.

<a id="entry-060"></a>
## 2026-10-10 15:59:27 UTC — 060 · Message received: Event 007 — Note from Maya Chen (Property Manager, Northbridge Lettings)

- **Recorded by:** demo-case_manager (case manager)
- **Reading:** queued for Jev routing / Claude triage

> Event 007 — Note
> From: Maya Chen (Property Manager, Northbridge Lettings)
> To: Jonas Reed (Landlord)
>
> Requests approval for the £95 plus VAT diagnostic visit only. Notes that no repair estimate has yet been provided.

<a id="entry-061"></a>
## 2026-10-10 15:59:27 UTC — 061 · Policy gates → HUMAN REVIEW

- **Actor:** Policy engine (rules v1, `domain.evaluate`)
- **Outcome:** HUMAN REVIEW · owner case manager
- **Blockers:** `identity` UNKNOWN → HUMAN REVIEW; `route` UNKNOWN → HUMAN REVIEW; `access` UNKNOWN → HUMAN REVIEW; `authority` UNKNOWN → HUMAN REVIEW; `schedule` UNKNOWN → HUMAN REVIEW; `triage` UNKNOWN → WAIT
- **Next step:** Verify the person, property and work item mapping.

<a id="entry-062"></a>
## 2026-10-10 15:59:27 UTC — 062 · Workflow receipt

<a id="entry-063"></a>
## 2026-10-10 15:59:27 UTC — 063 · Jev routed the message

- **Actor:** Jev (jev-1.13.0 · 1652 in / 286 out tokens · 238 ms)
- **Tool:** TypeSafe `system_one` · step `route_case_messages`
- **Decision:** jev_route → `confirm_appointment` (confidence 0.91)
- **Signals:** hazard 0.08 · multiple_issues 0.03 · sensitive 0.03 · states_facts 0.93 · system_instructions 0.02
- **Why:** Jev routes; Claude extracts quotes and claims. confirm_appointment is not a Jev-only route. The message may state facts that need exact quotes.

<a id="entry-064"></a>
## 2026-10-10 15:59:35 UTC — 064 · Claude read the message

- **Actor:** Claude (claude-opus-5 · 1566 in / 617 out tokens)
- **Tool:** Anthropic Messages API `ai.triage` (prompt property-triage-2026-10-10.3) · step `triage_case_messages`
- **Reading:** update · route `instruct_work` · medium confidence
- **Work item:** Heating not working, blank thermostat display (appliance)
- **Summary:** Maya Chen asks the landlord to approve the £95 plus VAT diagnostic visit for the heating fault, noting no repair estimate has been given yet.
- **Rationale:** Assessment has been quoted at £95 plus VAT; the next step is landlord authority to instruct the diagnostic visit, not arranging an appointment.
- **Extracted:** 1 claim · 1 ambiguity · 1 issue
- **Unknown:** Landlord approval for the diagnostic charge has not yet been given; awaiting response.
- **Objected to Jev's route:** The message is an authority request to the landlord for the quoted diagnostic charge, not about arranging or confirming a visit, so confirm_appointment does not fit.

<a id="entry-065"></a>
## 2026-10-10 15:59:35 UTC — 065 · Proposed action → `instruct_work`

- **Actor:** Triage reading (route `instruct_work`)
- **Work item:** Heating not working, blank thermostat display
- **Action revision:** 5

<a id="entry-066"></a>
## 2026-10-10 15:59:35 UTC — 066 · Claim `total` = 114.0

- **Actor:** Claude (extracted)
- **Status:** unverified assertion — a person or policy must accept it

> Requests approval for the £95 plus VAT diagnostic visit only.

<a id="entry-067"></a>
## 2026-10-10 15:59:35 UTC — 067 · Human review opened: `identity`

- **Actor:** Policy engine
- **Owner:** case manager · rule `require-identity`
- **Expires:** 2026-10-12 15:59:35 UTC

> Verify the person, property and work item mapping.

<a id="entry-068"></a>
## 2026-10-10 15:59:35 UTC — 068 · Human review opened: `route`

- **Actor:** Policy engine
- **Owner:** case manager · rule `require-route`
- **Expires:** 2026-10-12 15:59:35 UTC

> Verify the recipient and permitted communication route.

<a id="entry-069"></a>
## 2026-10-10 15:59:35 UTC — 069 · Human review opened: `access`

- **Actor:** Policy engine
- **Owner:** access officer · rule `require-access`
- **Expires:** 2026-10-12 15:59:35 UTC

> Record consent for this visit and access method from the authorised person. A verified route is required before asking externally.

<a id="entry-070"></a>
## 2026-10-10 15:59:35 UTC — 070 · Human review opened: `authority`

- **Actor:** Policy engine
- **Owner:** approver · rule `require-authority`
- **Expires:** 2026-10-12 15:59:35 UTC

> Obtain authority for this work item, provider and action.

<a id="entry-071"></a>
## 2026-10-10 15:59:35 UTC — 071 · Human review opened: `schedule`

- **Actor:** Policy engine
- **Owner:** case manager · rule `require-schedule`
- **Expires:** 2026-10-12 15:59:35 UTC

> Confirm the active appointment with a precise date and time. A verified route is required before asking externally.

<a id="entry-072"></a>
## 2026-10-10 15:59:35 UTC — 072 · Human review opened: `evidence`

- **Actor:** Policy engine
- **Owner:** case manager · rule `require-evidence`
- **Expires:** 2026-10-12 15:59:35 UTC

> Supply usable evidence required for this work item. A verified route is required before asking externally.

<a id="entry-073"></a>
## 2026-10-10 15:59:35 UTC — 073 · Human review opened: `classification`

- **Actor:** Policy engine
- **Owner:** case manager · rule `require-classification`
- **Expires:** 2026-10-12 15:59:35 UTC

> Confirm that the category and work item match the source request. A verified route is required before asking externally.

<a id="entry-074"></a>
## 2026-10-10 15:59:35 UTC — 074 · Human review opened: `total`

- **Actor:** Policy engine
- **Owner:** case manager · rule `require-total`
- **Expires:** 2026-10-12 15:59:35 UTC

> Establish the full comparable commitment, including tax. A verified route is required before asking externally.

<a id="entry-075"></a>
## 2026-10-10 15:59:35 UTC — 075 · Human review opened: `triage`

- **Actor:** Policy engine
- **Owner:** case manager · rule `require-triage`
- **Expires:** 2026-10-12 15:59:35 UTC

> Jev routed this message to confirm_appointment, but Claude reads it as instruct_work: The message is an authority request to the landlord for the quoted diagnostic charge, not about arranging or confirming a visit, so confirm_appointment does not fit. The case follows Claude's route (a hazard is never de-escalated). Confirm or correct the route.

<a id="entry-076"></a>
## 2026-10-10 15:59:35 UTC — 076 · Policy gates → HUMAN REVIEW

- **Actor:** Policy engine (rules v1, `domain.evaluate`)
- **Outcome:** HUMAN REVIEW · owner case manager
- **Blockers:** `identity` UNKNOWN → HUMAN REVIEW; `route` UNKNOWN → HUMAN REVIEW; `access` UNKNOWN → HUMAN REVIEW; `authority` UNKNOWN → HUMAN REVIEW; `schedule` UNKNOWN → HUMAN REVIEW; `evidence` UNKNOWN → HUMAN REVIEW; `classification` UNKNOWN → HUMAN REVIEW; `total` UNKNOWN → HUMAN REVIEW; `triage` CONFLICT → HUMAN REVIEW
- **Next step:** Verify the person, property and work item mapping.

<a id="entry-077"></a>
## 2026-10-10 15:59:35 UTC — 077 · Message received: Event 008 — Email from Jonas Reed (Landlord)

- **Recorded by:** demo-case_manager (case manager)
- **Reading:** queued for Jev routing / Claude triage

> Event 008 — Email
> From: Jonas Reed (Landlord)
> To: Maya Chen (Property Manager, Northbridge Lettings)
>
> Approves the diagnostic visit up to £95 plus VAT. Says to contact him before authorising repair work.

<a id="entry-078"></a>
## 2026-10-10 15:59:35 UTC — 078 · Policy gates → HUMAN REVIEW

- **Actor:** Policy engine (rules v1, `domain.evaluate`)
- **Outcome:** HUMAN REVIEW · owner case manager
- **Blockers:** `identity` UNKNOWN → HUMAN REVIEW; `route` UNKNOWN → HUMAN REVIEW; `access` UNKNOWN → HUMAN REVIEW; `authority` UNKNOWN → HUMAN REVIEW; `schedule` UNKNOWN → HUMAN REVIEW; `evidence` UNKNOWN → HUMAN REVIEW; `classification` UNKNOWN → HUMAN REVIEW; `total` UNKNOWN → HUMAN REVIEW; `triage` UNKNOWN → WAIT
- **Next step:** Verify the person, property and work item mapping.

<a id="entry-079"></a>
## 2026-10-10 15:59:35 UTC — 079 · Workflow receipt

<a id="entry-080"></a>
## 2026-10-10 15:59:36 UTC — 080 · Jev routed the message

- **Actor:** Jev (jev-1.13.0 · 1652 in / 286 out tokens · 293 ms)
- **Tool:** TypeSafe `system_one` · step `route_case_messages`
- **Decision:** jev_route → `confirm_appointment` (confidence 0.59)
- **Signals:** hazard 0.12 · multiple_issues 0.02 · sensitive 0.03 · states_facts 0.95 · system_instructions 0.03
- **Why:** Jev routes; Claude extracts quotes and claims. confirm_appointment is not a Jev-only route. Route confidence 0.59 is below the Jev-only bar 0.8. The message may state facts that need exact quotes. A route change on an existing case.

<a id="entry-081"></a>
## 2026-10-10 15:59:43 UTC — 081 · Claude read the message

- **Actor:** Claude (claude-opus-5 · 1614 in / 563 out tokens)
- **Tool:** Anthropic Messages API `ai.triage` (prompt property-triage-2026-10-10.3) · step `triage_case_messages`
- **Reading:** update · route `instruct_work` · high confidence
- **Work item:** Heating not working, blank thermostat display (appliance)
- **Summary:** Landlord Jonas Reed approves the £95 plus VAT diagnostic visit only, and asks to be contacted before any repair work is authorised.
- **Rationale:** Landlord authority given for the already-quoted diagnostic visit, so the next step is instructing the contractor.
- **Extracted:** 2 claims · 2 ambiguities · 1 issue
- **Unknown:** No appointment date or time is confirmed with the tenant for the diagnostic visit.
- **Unknown:** Tenant access arrangements for the contractor visit are not stated.
- **Objected to Jev's route:** The message does not arrange or change a visit; it grants landlord authority for the quoted diagnostic. instruct_work fits better than confirm_appointment.

<a id="entry-082"></a>
## 2026-10-10 15:59:43 UTC — 082 · Claim `total` = 114.0

- **Actor:** Claude (extracted)
- **Status:** unverified assertion — a person or policy must accept it

> up to £95 plus VAT

<a id="entry-083"></a>
## 2026-10-10 15:59:43 UTC — 083 · Human review opened: `total`

- **Actor:** Policy engine
- **Owner:** case manager · rule `require-total`
- **Expires:** 2026-10-12 15:59:43 UTC

> Establish the full comparable commitment, including tax. A verified route is required before asking externally.

<a id="entry-084"></a>
## 2026-10-10 15:59:43 UTC — 084 · Review superseded

- **Why:** Relevant evidence or current blockers changed; assess the current review.

<a id="entry-085"></a>
## 2026-10-10 15:59:43 UTC — 085 · Policy gates → HUMAN REVIEW

- **Actor:** Policy engine (rules v1, `domain.evaluate`)
- **Outcome:** HUMAN REVIEW · owner case manager
- **Blockers:** `identity` UNKNOWN → HUMAN REVIEW; `route` UNKNOWN → HUMAN REVIEW; `access` UNKNOWN → HUMAN REVIEW; `authority` UNKNOWN → HUMAN REVIEW; `schedule` UNKNOWN → HUMAN REVIEW; `evidence` UNKNOWN → HUMAN REVIEW; `classification` UNKNOWN → HUMAN REVIEW; `total` UNKNOWN → HUMAN REVIEW; `triage` CONFLICT → HUMAN REVIEW
- **Next step:** Verify the person, property and work item mapping.

<a id="entry-086"></a>
## 2026-10-10 15:59:43 UTC — 086 · Message received: Event 009 — SMS from Rowan Pike (Contractor, Hearthline Heating)

- **Recorded by:** demo-case_manager (case manager)
- **Reading:** queued for Jev routing / Claude triage

> Event 009 — SMS
> From: Rowan Pike (Contractor, Hearthline Heating)
> To: Iris Bell (Tenant)
>
> Offers an appointment window of 09:00–11:00 on 7 May. Iris replies that the front door buzzer is unreliable and asks Rowan to call on arrival.

<a id="entry-087"></a>
## 2026-10-10 15:59:43 UTC — 087 · Policy gates → HUMAN REVIEW

- **Actor:** Policy engine (rules v1, `domain.evaluate`)
- **Outcome:** HUMAN REVIEW · owner case manager
- **Blockers:** `identity` UNKNOWN → HUMAN REVIEW; `route` UNKNOWN → HUMAN REVIEW; `access` UNKNOWN → HUMAN REVIEW; `authority` UNKNOWN → HUMAN REVIEW; `schedule` UNKNOWN → HUMAN REVIEW; `evidence` UNKNOWN → HUMAN REVIEW; `classification` UNKNOWN → HUMAN REVIEW; `total` UNKNOWN → HUMAN REVIEW; `triage` UNKNOWN → WAIT
- **Next step:** Verify the person, property and work item mapping.

<a id="entry-088"></a>
## 2026-10-10 15:59:43 UTC — 088 · Workflow receipt

<a id="entry-089"></a>
## 2026-10-10 15:59:44 UTC — 089 · Jev routed the message

- **Actor:** Jev (jev-1.13.0 · 1651 in / 286 out tokens · 294 ms)
- **Tool:** TypeSafe `system_one` · step `route_case_messages`
- **Decision:** jev_route → `confirm_appointment` (confidence 0.61)
- **Signals:** hazard 0.10 · multiple_issues 0.04 · sensitive 0.05 · states_facts 0.91 · system_instructions 0.02
- **Why:** Jev routes; Claude extracts quotes and claims. confirm_appointment is not a Jev-only route. Route confidence 0.61 is below the Jev-only bar 0.8. The message may state facts that need exact quotes. A route change on an existing case.

<a id="entry-090"></a>
## 2026-10-10 15:59:48 UTC — 090 · Claude read the message

- **Actor:** Claude (claude-opus-5 · 1666 in / 371 out tokens)
- **Tool:** Anthropic Messages API `ai.triage` (prompt property-triage-2026-10-10.3) · step `triage_case_messages`
- **Reading:** access or appointment · route `confirm_appointment` · high confidence
- **Work item:** Heating not working, blank thermostat display (appliance)
- **Summary:** Contractor Rowan Pike offers a 09:00-11:00 appointment window on 7 May; tenant Iris Bell notes the front door buzzer is unreliable and asks him to call on arrival.
- **Rationale:** Message is about arranging a visit for the known heating job, so confirm_appointment applies.
- **Extracted:** 0 claims · 2 ambiguities · 1 issue
- **Unknown:** The appointment window is offered but the tenant has not explicitly confirmed acceptance of 09:00-11:00 on 7 May.
- **Unknown:** Tenant asks for a call on arrival due to an unreliable buzzer but has not explicitly granted entry permission.

<a id="entry-091"></a>
## 2026-10-10 15:59:48 UTC — 091 · Proposed action → `confirm_appointment`

- **Actor:** Triage reading (route `confirm_appointment`)
- **Work item:** Heating not working, blank thermostat display
- **Action revision:** 6

<a id="entry-092"></a>
## 2026-10-10 15:59:48 UTC — 092 · Human review opened: `identity`

- **Actor:** Policy engine
- **Owner:** case manager · rule `require-identity`
- **Expires:** 2026-10-12 15:59:48 UTC

> Verify the person, property and work item mapping.

<a id="entry-093"></a>
## 2026-10-10 15:59:48 UTC — 093 · Human review opened: `route`

- **Actor:** Policy engine
- **Owner:** case manager · rule `require-route`
- **Expires:** 2026-10-12 15:59:48 UTC

> Verify the recipient and permitted communication route.

<a id="entry-094"></a>
## 2026-10-10 15:59:48 UTC — 094 · Human review opened: `access`

- **Actor:** Policy engine
- **Owner:** access officer · rule `require-access`
- **Expires:** 2026-10-12 15:59:48 UTC

> Record consent for this visit and access method from the authorised person. A verified route is required before asking externally.

<a id="entry-095"></a>
## 2026-10-10 15:59:48 UTC — 095 · Human review opened: `authority`

- **Actor:** Policy engine
- **Owner:** approver · rule `require-authority`
- **Expires:** 2026-10-12 15:59:48 UTC

> Obtain authority for this work item, provider and action.

<a id="entry-096"></a>
## 2026-10-10 15:59:48 UTC — 096 · Human review opened: `schedule`

- **Actor:** Policy engine
- **Owner:** case manager · rule `require-schedule`
- **Expires:** 2026-10-12 15:59:48 UTC

> Confirm the active appointment with a precise date and time. A verified route is required before asking externally.

<a id="entry-097"></a>
## 2026-10-10 15:59:48 UTC — 097 · Policy gates → HUMAN REVIEW

- **Actor:** Policy engine (rules v1, `domain.evaluate`)
- **Outcome:** HUMAN REVIEW · owner case manager
- **Blockers:** `identity` UNKNOWN → HUMAN REVIEW; `route` UNKNOWN → HUMAN REVIEW; `access` UNKNOWN → HUMAN REVIEW; `authority` UNKNOWN → HUMAN REVIEW; `schedule` UNKNOWN → HUMAN REVIEW
- **Next step:** Verify the person, property and work item mapping.

<a id="entry-098"></a>
## 2026-10-10 15:59:49 UTC — 098 · Message received: Event 010 — Call from Rowan Pike (Contractor, Hearthline Heating)

- **Recorded by:** demo-case_manager (case manager)
- **Reading:** queued for Jev routing / Claude triage

> Event 010 — Call
> From: Rowan Pike (Contractor, Hearthline Heating)
> To: Iris Bell (Tenant)
>
> Calls from outside the property after the buzzer does not respond. Iris confirms access by phone.

<a id="entry-099"></a>
## 2026-10-10 15:59:49 UTC — 099 · Policy gates → HUMAN REVIEW

- **Actor:** Policy engine (rules v1, `domain.evaluate`)
- **Outcome:** HUMAN REVIEW · owner case manager
- **Blockers:** `identity` UNKNOWN → HUMAN REVIEW; `route` UNKNOWN → HUMAN REVIEW; `access` UNKNOWN → HUMAN REVIEW; `authority` UNKNOWN → HUMAN REVIEW; `schedule` UNKNOWN → HUMAN REVIEW; `triage` UNKNOWN → WAIT
- **Next step:** Verify the person, property and work item mapping.

<a id="entry-100"></a>
## 2026-10-10 15:59:49 UTC — 100 · Workflow receipt

<a id="entry-101"></a>
## 2026-10-10 15:59:49 UTC — 101 · Jev routed the message

- **Actor:** Jev (jev-1.13.0 · 1636 in / 286 out tokens · 374 ms)
- **Tool:** TypeSafe `system_one` · step `route_case_messages`
- **Decision:** jev_route → `confirm_appointment` (confidence 1.00)
- **Signals:** hazard 0.12 · multiple_issues 0.04 · sensitive 0.03 · states_facts 0.92 · system_instructions 0.02
- **Why:** Jev routes; Claude extracts quotes and claims. confirm_appointment is not a Jev-only route. The message may state facts that need exact quotes.

<a id="entry-102"></a>
## 2026-10-10 15:59:53 UTC — 102 · Claude read the message

- **Actor:** Claude (claude-opus-5 · 1627 in / 323 out tokens)
- **Tool:** Anthropic Messages API `ai.triage` (prompt property-triage-2026-10-10.3) · step `triage_case_messages`
- **Reading:** access or appointment · route `confirm_appointment` · high confidence
- **Work item:** Heating not working, blank thermostat display (appliance)
- **Summary:** Contractor Rowan Pike called from outside the property after the buzzer failed; the tenant confirmed access by phone for the diagnostic visit.
- **Rationale:** Message concerns access for the already arranged inspection visit; tenant granted entry.
- **Extracted:** 1 claim · 1 ambiguity · 1 issue
- **Unknown:** Unclear whether the contractor actually gained entry and the inspection went ahead.

<a id="entry-103"></a>
## 2026-10-10 15:59:53 UTC — 103 · Claim `access` = true

- **Actor:** Claude (extracted)
- **Status:** unverified assertion — a person or policy must accept it

> Iris confirms access by phone

<a id="entry-104"></a>
## 2026-10-10 15:59:53 UTC — 104 · Human review opened: `access`

- **Actor:** Policy engine
- **Owner:** access officer · rule `require-access`
- **Expires:** 2026-10-12 15:59:53 UTC

> Record consent for this visit and access method from the authorised person. A verified route is required before asking externally.

<a id="entry-105"></a>
## 2026-10-10 15:59:53 UTC — 105 · Review superseded

- **Why:** Relevant evidence or current blockers changed; assess the current review.

<a id="entry-106"></a>
## 2026-10-10 15:59:53 UTC — 106 · Policy gates → HUMAN REVIEW

- **Actor:** Policy engine (rules v1, `domain.evaluate`)
- **Outcome:** HUMAN REVIEW · owner case manager
- **Blockers:** `identity` UNKNOWN → HUMAN REVIEW; `route` UNKNOWN → HUMAN REVIEW; `access` UNKNOWN → HUMAN REVIEW; `authority` UNKNOWN → HUMAN REVIEW; `schedule` UNKNOWN → HUMAN REVIEW
- **Next step:** Verify the person, property and work item mapping.

<a id="entry-107"></a>
## 2026-10-10 15:59:54 UTC — 107 · Message received: Event 011 — Email from Rowan Pike (Contractor, Hearthline Heating)

- **Recorded by:** demo-case_manager (case manager)
- **Reading:** queued for Jev routing / Claude triage

> Event 011 — Email
> From: Rowan Pike (Contractor, Hearthline Heating)
> To: Maya Chen (Property Manager, Northbridge Lettings)
>
> Reports that he attended, found a failed control board, and restored heating temporarily by resetting the unit. Says a replacement board may be needed and estimates £460 plus VAT for parts and labour. No written job sheet is attached.

<a id="entry-108"></a>
## 2026-10-10 15:59:54 UTC — 108 · Policy gates → HUMAN REVIEW

- **Actor:** Policy engine (rules v1, `domain.evaluate`)
- **Outcome:** HUMAN REVIEW · owner case manager
- **Blockers:** `identity` UNKNOWN → HUMAN REVIEW; `route` UNKNOWN → HUMAN REVIEW; `access` UNKNOWN → HUMAN REVIEW; `authority` UNKNOWN → HUMAN REVIEW; `schedule` UNKNOWN → HUMAN REVIEW; `triage` UNKNOWN → WAIT
- **Next step:** Verify the person, property and work item mapping.

<a id="entry-109"></a>
## 2026-10-10 15:59:54 UTC — 109 · Workflow receipt

<a id="entry-110"></a>
## 2026-10-10 15:59:54 UTC — 110 · Jev routed the message

- **Actor:** Jev (jev-1.13.0 · 1665 in / 284 out tokens · 269 ms)
- **Tool:** TypeSafe `system_one` · step `route_case_messages`
- **Decision:** claude → no route
- **Signals:** hazard 0.15 · multiple_issues 0.05 · sensitive 0.03 · states_facts 0.97 · system_instructions 0.02
- **Why:** Jev route confidence 0.49 is below 0.5.

<a id="entry-111"></a>
## 2026-10-10 16:00:07 UTC — 111 · Claude read the message

- **Actor:** Claude (claude-opus-5 · 1590 in / 1009 out tokens)
- **Tool:** Anthropic Messages API `ai.triage` (prompt property-triage-2026-10-10.3) · step `triage_case_messages`
- **Reading:** update · route `request_quote` · medium confidence
- **Work item:** Heating not working, blank thermostat display (appliance)
- **Summary:** Contractor Rowan Pike reports he attended the diagnostic visit, found a failed control board and temporarily restored heating by resetting the unit. He estimates £460 plus VAT for a replacement board, and no written job sheet was provided.
- **Rationale:** Diagnostic visit completed but the repair is only an informal estimate with no written job sheet, so a firm quote is needed before the landlord can authorise the board replacement.
- **Extracted:** 2 claims · 2 ambiguities · 1 issue
- **Unknown (affects route):** The estimate is verbal and tentative ('may be needed'); a written job sheet or formal quote with scope and parts is not provided.
- **Unknown:** Heating is only temporarily restored; unclear how long the reset will hold and whether the board replacement is required.

<a id="entry-112"></a>
## 2026-10-10 16:00:07 UTC — 112 · Proposed action → `request_quote`

- **Actor:** Triage reading (route `request_quote`)
- **Work item:** Heating not working, blank thermostat display
- **Action revision:** 7

<a id="entry-113"></a>
## 2026-10-10 16:00:07 UTC — 113 · Claim `total` = 552.0

- **Actor:** Claude (extracted)
- **Status:** unverified assertion — a person or policy must accept it

> estimates £460 plus VAT for parts and labour

<a id="entry-114"></a>
## 2026-10-10 16:00:07 UTC — 114 · Claim `completion` = false

- **Actor:** Claude (extracted)
- **Status:** unverified assertion — a person or policy must accept it

> restored heating temporarily by resetting the unit. Says a replacement board may be needed

<a id="entry-115"></a>
## 2026-10-10 16:00:07 UTC — 115 · Human review opened: `identity`

- **Actor:** Policy engine
- **Owner:** case manager · rule `require-identity`
- **Expires:** 2026-10-12 16:00:07 UTC

> Verify the person, property and work item mapping.

<a id="entry-116"></a>
## 2026-10-10 16:00:07 UTC — 116 · Human review opened: `route`

- **Actor:** Policy engine
- **Owner:** case manager · rule `require-route`
- **Expires:** 2026-10-12 16:00:07 UTC

> Verify the recipient and permitted communication route.

<a id="entry-117"></a>
## 2026-10-10 16:00:07 UTC — 117 · Human review opened: `classification`

- **Actor:** Policy engine
- **Owner:** case manager · rule `require-classification`
- **Expires:** 2026-10-12 16:00:07 UTC

> Confirm that the category and work item match the source request. A verified route is required before asking externally.

<a id="entry-118"></a>
## 2026-10-10 16:00:07 UTC — 118 · Human review opened: `triage`

- **Actor:** Policy engine
- **Owner:** case manager · rule `require-triage`
- **Expires:** 2026-10-12 16:00:07 UTC

> Clarify before routing: The estimate is verbal and tentative ('may be needed'); a written job sheet or formal quote with scope and parts is not provided. A verified route is required before asking externally.

<a id="entry-119"></a>
## 2026-10-10 16:00:07 UTC — 119 · Policy gates → HUMAN REVIEW

- **Actor:** Policy engine (rules v1, `domain.evaluate`)
- **Outcome:** HUMAN REVIEW · owner case manager
- **Blockers:** `identity` UNKNOWN → HUMAN REVIEW; `route` UNKNOWN → HUMAN REVIEW; `classification` UNKNOWN → HUMAN REVIEW; `triage` UNKNOWN → HUMAN REVIEW
- **Next step:** Verify the person, property and work item mapping.

<a id="entry-120"></a>
## 2026-10-10 16:00:08 UTC — 120 · Message received: Event 012 — Email from Maya Chen (Property Manager, Northbridge Lettings)

- **Recorded by:** demo-case_manager (case manager)
- **Reading:** queued for Jev routing / Claude triage

> Event 012 — Email
> From: Maya Chen (Property Manager, Northbridge Lettings)
> To: Rowan Pike (Contractor, Hearthline Heating)
>
> Asks whether the £460 estimate includes the diagnostic charge, requests a written breakdown and job sheet, and asks whether the temporary reset is safe to use pending a decision.

<a id="entry-121"></a>
## 2026-10-10 16:00:08 UTC — 121 · Policy gates → HUMAN REVIEW

- **Actor:** Policy engine (rules v1, `domain.evaluate`)
- **Outcome:** HUMAN REVIEW · owner case manager
- **Blockers:** `identity` UNKNOWN → HUMAN REVIEW; `route` UNKNOWN → HUMAN REVIEW; `classification` UNKNOWN → HUMAN REVIEW; `triage` UNKNOWN → WAIT
- **Next step:** Verify the person, property and work item mapping.

<a id="entry-122"></a>
## 2026-10-10 16:00:08 UTC — 122 · Workflow receipt

<a id="entry-123"></a>
## 2026-10-10 16:00:08 UTC — 123 · Jev routed the message

- **Actor:** Jev (jev-1.13.0 · 1687 in / 284 out tokens · 335 ms)
- **Tool:** TypeSafe `system_one` · step `route_case_messages`
- **Decision:** jev_route → `request_quote` (confidence 0.60)
- **Signals:** hazard 0.13 · multiple_issues 0.05 · sensitive 0.03 · states_facts 0.62 · system_instructions 0.02
- **Why:** Jev routes; Claude extracts quotes and claims. Route confidence 0.60 is below the Jev-only bar 0.8. The message may state facts that need exact quotes.

<a id="entry-124"></a>
## 2026-10-10 16:00:13 UTC — 124 · Claude read the message

- **Actor:** Claude (claude-opus-5 · 1728 in / 403 out tokens)
- **Tool:** Anthropic Messages API `ai.triage` (prompt property-triage-2026-10-10.3) · step `triage_case_messages`
- **Reading:** update · route `request_quote` · high confidence
- **Work item:** Heating not working, blank thermostat display (appliance)
- **Summary:** Property manager asks the contractor whether the £460 estimate includes the diagnostic charge, requests a written breakdown and job sheet, and asks whether the temporary reset is safe to use pending a decision.
- **Rationale:** Staff chasing a written, comparable quote for the control board replacement; job not yet instructed.
- **Extracted:** 0 claims · 2 ambiguities · 1 issue
- **Unknown:** Whether the £460 estimate is inclusive of the £95 diagnostic charge and VAT is not yet established; no written breakdown or job sheet received.
- **Unknown:** Safety of continuing to use the temporarily reset unit pending a decision is unconfirmed.

<a id="entry-125"></a>
## 2026-10-10 16:00:13 UTC — 125 · Review superseded

- **Why:** Relevant evidence or current blockers changed; assess the current review.

<a id="entry-126"></a>
## 2026-10-10 16:00:13 UTC — 126 · Policy gates → HUMAN REVIEW

- **Actor:** Policy engine (rules v1, `domain.evaluate`)
- **Outcome:** HUMAN REVIEW · owner case manager
- **Blockers:** `identity` UNKNOWN → HUMAN REVIEW; `route` UNKNOWN → HUMAN REVIEW; `classification` UNKNOWN → HUMAN REVIEW
- **Next step:** Verify the person, property and work item mapping.

<a id="entry-127"></a>
## 2026-10-10 16:00:14 UTC — 127 · Message received: Event 013 — SMS from Iris Bell (Tenant)

- **Recorded by:** demo-case_manager (case manager)
- **Reading:** queued for Jev routing / Claude triage

> Event 013 — SMS
> From: Iris Bell (Tenant)
> To: Maya Chen (Property Manager, Northbridge Lettings)
>
> Says the heating is currently running after the visit but asks whether it is expected to remain operational. Reports no new symptoms.

<a id="entry-128"></a>
## 2026-10-10 16:00:14 UTC — 128 · Policy gates → HUMAN REVIEW

- **Actor:** Policy engine (rules v1, `domain.evaluate`)
- **Outcome:** HUMAN REVIEW · owner case manager
- **Blockers:** `identity` UNKNOWN → HUMAN REVIEW; `route` UNKNOWN → HUMAN REVIEW; `classification` UNKNOWN → HUMAN REVIEW; `triage` UNKNOWN → WAIT
- **Next step:** Verify the person, property and work item mapping.

<a id="entry-129"></a>
## 2026-10-10 16:00:14 UTC — 129 · Workflow receipt

<a id="entry-130"></a>
## 2026-10-10 16:00:14 UTC — 130 · Jev routed the message

- **Actor:** Jev (jev-1.13.0 · 1664 in / 284 out tokens · 567 ms)
- **Tool:** TypeSafe `system_one` · step `route_case_messages`
- **Decision:** claude → no route
- **Signals:** hazard 0.06 · multiple_issues 0.04 · sensitive 0.03 · states_facts 0.49 · system_instructions 0.02
- **Why:** Jev route confidence 0.49 is below 0.5.

<a id="entry-131"></a>
## 2026-10-10 16:00:23 UTC — 131 · Claude read the message

- **Actor:** Claude (claude-opus-5 · 1567 in / 627 out tokens)
- **Tool:** Anthropic Messages API `ai.triage` (prompt property-triage-2026-10-10.3) · step `triage_case_messages`
- **Reading:** update · route `request_quote` · medium confidence
- **Work item:** Heating not working, blank thermostat display (appliance)
- **Summary:** Tenant Iris Bell reports the heating is running following the contractor's visit and asks whether it is expected to keep working. No new symptoms reported; the replacement control board decision is still outstanding.
- **Rationale:** Tenant update on an open case; the temporary reset is holding but the replacement board quote and job sheet are still awaited, so the item remains at the quote stage.
- **Extracted:** 0 claims · 2 ambiguities · 1 issue
- **Unknown:** Tenant says heating is running after the temporary reset, but this is not confirmation that the work item is complete; the contractor's written breakdown, job sheet and confirmation that the reset is safe pending a decision are still outstanding.
- **Unknown:** Tenant asks whether the heating is expected to remain operational - needs a reply based on the contractor's assessment of the failed control board.

<a id="entry-132"></a>
## 2026-10-10 16:00:23 UTC — 132 · Policy gates → HUMAN REVIEW

- **Actor:** Policy engine (rules v1, `domain.evaluate`)
- **Outcome:** HUMAN REVIEW · owner case manager
- **Blockers:** `identity` UNKNOWN → HUMAN REVIEW; `route` UNKNOWN → HUMAN REVIEW; `classification` UNKNOWN → HUMAN REVIEW
- **Next step:** Verify the person, property and work item mapping.

<a id="entry-133"></a>
## 2026-10-10 16:00:23 UTC — 133 · Message received: Event 014 — Email from Rowan Pike (Contractor, Hearthline Heating)

- **Recorded by:** demo-case_manager (case manager)
- **Reading:** queued for Jev routing / Claude triage

> Event 014 — Email
> From: Rowan Pike (Contractor, Hearthline Heating)
> To: Maya Chen (Property Manager, Northbridge Lettings)
>
> Replies that the estimate is separate from the diagnostic charge. Says the reset is not a permanent repair and the fault could recur; recommends replacement of the control board. Does not provide the requested job sheet.

<a id="entry-134"></a>
## 2026-10-10 16:00:23 UTC — 134 · Policy gates → HUMAN REVIEW

- **Actor:** Policy engine (rules v1, `domain.evaluate`)
- **Outcome:** HUMAN REVIEW · owner case manager
- **Blockers:** `identity` UNKNOWN → HUMAN REVIEW; `route` UNKNOWN → HUMAN REVIEW; `classification` UNKNOWN → HUMAN REVIEW; `triage` UNKNOWN → WAIT
- **Next step:** Verify the person, property and work item mapping.

<a id="entry-135"></a>
## 2026-10-10 16:00:23 UTC — 135 · Workflow receipt

<a id="entry-136"></a>
## 2026-10-10 16:00:24 UTC — 136 · Jev routed the message

- **Actor:** Jev (jev-1.13.0 · 1696 in / 284 out tokens · 278 ms)
- **Tool:** TypeSafe `system_one` · step `route_case_messages`
- **Decision:** jev_route → `request_quote` (confidence 0.69)
- **Signals:** hazard 0.06 · multiple_issues 0.06 · sensitive 0.03 · states_facts 0.59 · system_instructions 0.01
- **Why:** Jev routes; Claude extracts quotes and claims. Route confidence 0.69 is below the Jev-only bar 0.8. The message may state facts that need exact quotes.

<a id="entry-137"></a>
## 2026-10-10 16:00:28 UTC — 137 · Claude read the message

- **Actor:** Claude (claude-opus-5 · 1689 in / 374 out tokens)
- **Tool:** Anthropic Messages API `ai.triage` (prompt property-triage-2026-10-10.3) · step `triage_case_messages`
- **Reading:** update · route `request_quote` · high confidence
- **Work item:** Heating not working, blank thermostat display (appliance)
- **Summary:** Contractor confirms the £460 estimate is separate from the diagnostic charge and recommends replacing the control board, warning the reset is temporary. The requested written job sheet and breakdown were not provided.
- **Rationale:** Estimate remains unsupported by a written breakdown or job sheet, so a proper quote is still needed before instructing work.
- **Extracted:** 0 claims · 2 ambiguities · 1 issue
- **Unknown:** No written job sheet or cost breakdown supplied; the VAT-inclusive total for the board replacement is still unconfirmed.
- **Unknown (affects route):** Contractor has not stated whether the temporary reset is safe to continue using pending a decision.

<a id="entry-138"></a>
## 2026-10-10 16:00:28 UTC — 138 · Human review opened: `triage`

- **Actor:** Policy engine
- **Owner:** case manager · rule `require-triage`
- **Expires:** 2026-10-12 16:00:28 UTC

> Clarify before routing: Contractor has not stated whether the temporary reset is safe to continue using pending a decision. A verified route is required before asking externally.

<a id="entry-139"></a>
## 2026-10-10 16:00:28 UTC — 139 · Policy gates → HUMAN REVIEW

- **Actor:** Policy engine (rules v1, `domain.evaluate`)
- **Outcome:** HUMAN REVIEW · owner case manager
- **Blockers:** `identity` UNKNOWN → HUMAN REVIEW; `route` UNKNOWN → HUMAN REVIEW; `classification` UNKNOWN → HUMAN REVIEW; `triage` UNKNOWN → HUMAN REVIEW
- **Next step:** Verify the person, property and work item mapping.

<a id="entry-140"></a>
## 2026-10-10 16:00:29 UTC — 140 · Message received: Event 015 — Email from Maya Chen (Property Manager, Northbridge Lettings)

- **Recorded by:** demo-case_manager (case manager)
- **Reading:** queued for Jev routing / Claude triage

> Event 015 — Email
> From: Maya Chen (Property Manager, Northbridge Lettings)
> To: Jonas Reed (Landlord)
>
> Forwards the £460 plus VAT estimate and asks whether to proceed. Notes the contractor has not supplied a job sheet or confirmed the reset's expected duration.

<a id="entry-141"></a>
## 2026-10-10 16:00:29 UTC — 141 · Policy gates → HUMAN REVIEW

- **Actor:** Policy engine (rules v1, `domain.evaluate`)
- **Outcome:** HUMAN REVIEW · owner case manager
- **Blockers:** `identity` UNKNOWN → HUMAN REVIEW; `route` UNKNOWN → HUMAN REVIEW; `classification` UNKNOWN → HUMAN REVIEW; `triage` UNKNOWN → WAIT
- **Next step:** Verify the person, property and work item mapping.

<a id="entry-142"></a>
## 2026-10-10 16:00:29 UTC — 142 · Workflow receipt

<a id="entry-143"></a>
## 2026-10-10 16:00:29 UTC — 143 · Jev routed the message

- **Actor:** Jev (jev-1.13.0 · 1677 in / 284 out tokens · 288 ms)
- **Tool:** TypeSafe `system_one` · step `route_case_messages`
- **Decision:** claude → no route
- **Signals:** hazard 0.09 · multiple_issues 0.04 · sensitive 0.03 · states_facts 0.96 · system_instructions 0.01
- **Why:** Jev route confidence 0.47 is below 0.5.

<a id="entry-144"></a>
## 2026-10-10 16:00:45 UTC — 144 · Claude read the message

- **Actor:** Claude (claude-opus-5 · 1661 in / 1202 out tokens)
- **Tool:** Anthropic Messages API `ai.triage` (prompt property-triage-2026-10-10.3) · step `triage_case_messages`
- **Reading:** update · route `request_quote` · medium confidence
- **Work item:** Heating not working, blank thermostat display (appliance)
- **Summary:** The property manager has forwarded the contractor's £460 plus VAT estimate for the control board replacement to the landlord and asked whether to proceed. She notes the contractor still has not supplied a job sheet or confirmed how long the temporary reset will hold.
- **Rationale:** The estimate lacks a written breakdown and job sheet and the landlord has not yet authorised spend, so the item remains at the quote/assessment stage rather than ready for instruction.
- **Extracted:** 1 claim · 4 ambiguities · 1 issue
- **Unknown:** Contractor has still not supplied the written job sheet or cost breakdown for the £460 plus VAT estimate.
- **Unknown:** No VAT-inclusive total has been stated in writing; the £552 figure is derived from "£460 plus VAT" at the standard rate.
- **Unknown:** Contractor has not confirmed whether the temporary reset is safe to continue using, or how long it is expected to hold, pending the landlord's decision.
- **Unknown (affects route):** Landlord has not yet responded, so no authority to instruct the control board replacement exists.

<a id="entry-145"></a>
## 2026-10-10 16:00:45 UTC — 145 · Claim `total` = 552.0

- **Actor:** Claude (extracted)
- **Status:** unverified assertion — a person or policy must accept it

> Forwards the £460 plus VAT estimate and asks whether to proceed.

<a id="entry-146"></a>
## 2026-10-10 16:00:45 UTC — 146 · Policy gates → HUMAN REVIEW

- **Actor:** Policy engine (rules v1, `domain.evaluate`)
- **Outcome:** HUMAN REVIEW · owner case manager
- **Blockers:** `identity` UNKNOWN → HUMAN REVIEW; `route` UNKNOWN → HUMAN REVIEW; `classification` UNKNOWN → HUMAN REVIEW; `triage` UNKNOWN → HUMAN REVIEW
- **Next step:** Verify the person, property and work item mapping.

<a id="entry-147"></a>
## 2026-10-10 16:00:46 UTC — 147 · Message received: Event 016 — Email from Jonas Reed (Landlord)

- **Recorded by:** demo-case_manager (case manager)
- **Reading:** queued for Jev routing / Claude triage

> Event 016 — Email
> From: Jonas Reed (Landlord)
> To: Maya Chen (Property Manager, Northbridge Lettings)
>
> Says he is travelling and asks for a clearer breakdown and written attendance record before deciding on the repair. Does not approve the quoted repair.

<a id="entry-148"></a>
## 2026-10-10 16:00:46 UTC — 148 · Policy gates → HUMAN REVIEW

- **Actor:** Policy engine (rules v1, `domain.evaluate`)
- **Outcome:** HUMAN REVIEW · owner case manager
- **Blockers:** `identity` UNKNOWN → HUMAN REVIEW; `route` UNKNOWN → HUMAN REVIEW; `classification` UNKNOWN → HUMAN REVIEW; `triage` UNKNOWN → WAIT
- **Next step:** Verify the person, property and work item mapping.

<a id="entry-149"></a>
## 2026-10-10 16:00:46 UTC — 149 · Workflow receipt

<a id="entry-150"></a>
## 2026-10-10 16:00:47 UTC — 150 · Jev routed the message

- **Actor:** Jev (jev-1.13.0 · 1656 in / 284 out tokens · 262 ms)
- **Tool:** TypeSafe `system_one` · step `route_case_messages`
- **Decision:** claude → no route
- **Signals:** hazard 0.07 · multiple_issues 0.04 · sensitive 0.04 · states_facts 0.15 · system_instructions 0.02
- **Why:** Jev route confidence 0.43 is below 0.5.

<a id="entry-151"></a>
## 2026-10-10 16:00:56 UTC — 151 · Claude read the message

- **Actor:** Claude (claude-opus-5 · 1642 in / 648 out tokens)
- **Tool:** Anthropic Messages API `ai.triage` (prompt property-triage-2026-10-10.3) · step `triage_case_messages`
- **Reading:** update · route `request_quote` · high confidence
- **Work item:** Heating not working, blank thermostat display (appliance)
- **Summary:** Landlord Jonas Reed replies that he is travelling and wants a clearer cost breakdown and a written attendance record before deciding on the control board replacement. He does not approve the quoted repair at this stage.
- **Rationale:** Landlord withholds approval and requests a fuller written quote and attendance record, so the item stays at the quote-gathering stage rather than moving to instruction.
- **Extracted:** 1 claim · 3 ambiguities · 1 issue
- **Unknown:** Contractor has still not supplied the written job sheet and itemised breakdown the landlord now requires before deciding.
- **Unknown:** Unclear how long the temporary reset is expected to hold while the decision is deferred, and whether the tenant is at risk of losing heating again.
- **Unknown:** Landlord is travelling; no indication of when a decision can be expected.

<a id="entry-152"></a>
## 2026-10-10 16:00:56 UTC — 152 · Review superseded

- **Why:** Relevant evidence or current blockers changed; assess the current review.

<a id="entry-153"></a>
## 2026-10-10 16:00:56 UTC — 153 · Policy gates → HUMAN REVIEW

- **Actor:** Policy engine (rules v1, `domain.evaluate`)
- **Outcome:** HUMAN REVIEW · owner case manager
- **Blockers:** `identity` UNKNOWN → HUMAN REVIEW; `route` UNKNOWN → HUMAN REVIEW; `classification` UNKNOWN → HUMAN REVIEW
- **Next step:** Verify the person, property and work item mapping.

<a id="entry-154"></a>
## 2026-10-10 16:00:56 UTC — 154 · Message received: Event 017 — Email from Maya Chen (Property Manager, Northbridge Lettings)

- **Recorded by:** demo-case_manager (case manager)
- **Reading:** queued for Jev routing / Claude triage

> Event 017 — Email
> From: Maya Chen (Property Manager, Northbridge Lettings)
> To: Rowan Pike (Contractor, Hearthline Heating)
>
> Requests the itemised estimate and attendance record again. Asks Rowan not to order parts or carry out the quoted replacement unless separately authorised.

<a id="entry-155"></a>
## 2026-10-10 16:00:56 UTC — 155 · Policy gates → HUMAN REVIEW

- **Actor:** Policy engine (rules v1, `domain.evaluate`)
- **Outcome:** HUMAN REVIEW · owner case manager
- **Blockers:** `identity` UNKNOWN → HUMAN REVIEW; `route` UNKNOWN → HUMAN REVIEW; `classification` UNKNOWN → HUMAN REVIEW; `triage` UNKNOWN → WAIT
- **Next step:** Verify the person, property and work item mapping.

<a id="entry-156"></a>
## 2026-10-10 16:00:56 UTC — 156 · Workflow receipt

<a id="entry-157"></a>
## 2026-10-10 16:00:57 UTC — 157 · Jev routed the message

- **Actor:** Jev (jev-1.13.0 · 1677 in / 284 out tokens · 365 ms)
- **Tool:** TypeSafe `system_one` · step `route_case_messages`
- **Decision:** jev_route → `request_quote` (confidence 0.63)
- **Signals:** hazard 0.07 · multiple_issues 0.04 · sensitive 0.05 · states_facts 0.10 · system_instructions 0.02
- **Why:** Jev routes; Claude extracts quotes and claims. Route confidence 0.63 is below the Jev-only bar 0.8.

<a id="entry-158"></a>
## 2026-10-10 16:01:02 UTC — 158 · Claude read the message

- **Actor:** Claude (claude-opus-5 · 1715 in / 394 out tokens)
- **Tool:** Anthropic Messages API `ai.triage` (prompt property-triage-2026-10-10.3) · step `triage_case_messages`
- **Reading:** update · route `request_quote` · high confidence
- **Work item:** Heating not working, blank thermostat display (appliance)
- **Summary:** Property manager chases the contractor for an itemised estimate and written attendance record, and instructs him not to order parts or carry out the quoted control board replacement unless separately authorised.
- **Rationale:** Quote documentation is still being chased and the work is expressly not authorised, so the item remains at the quote stage.
- **Extracted:** 1 claim · 1 ambiguity · 1 issue
- **Unknown:** Itemised breakdown and written attendance record still outstanding from the contractor; the expected duration of the temporary reset is still unconfirmed.

<a id="entry-159"></a>
## 2026-10-10 16:01:02 UTC — 159 · Policy gates → HUMAN REVIEW

- **Actor:** Policy engine (rules v1, `domain.evaluate`)
- **Outcome:** HUMAN REVIEW · owner case manager
- **Blockers:** `identity` UNKNOWN → HUMAN REVIEW; `route` UNKNOWN → HUMAN REVIEW; `classification` UNKNOWN → HUMAN REVIEW
- **Next step:** Verify the person, property and work item mapping.

<a id="entry-160"></a>
## 2026-10-10 16:01:02 UTC — 160 · Message received: Event 018 — Email from Rowan Pike (Contractor, Hearthline Heating)

- **Recorded by:** demo-case_manager (case manager)
- **Reading:** queued for Jev routing / Claude triage

> Event 018 — Email
> From: Rowan Pike (Contractor, Hearthline Heating)
> To: Maya Chen (Property Manager, Northbridge Lettings)
>
> Sends invoice NBL-005-INV-71 for £114 including VAT, described as diagnostic attendance on 7 May. Says the heating fault did not recur during his visit. The invoice lists remittance details 00-00-00 / 00000000 and a payment due date of 19 May.

<a id="entry-161"></a>
## 2026-10-10 16:01:02 UTC — 161 · Policy gates → HUMAN REVIEW

- **Actor:** Policy engine (rules v1, `domain.evaluate`)
- **Outcome:** HUMAN REVIEW · owner case manager
- **Blockers:** `identity` UNKNOWN → HUMAN REVIEW; `route` UNKNOWN → HUMAN REVIEW; `classification` UNKNOWN → HUMAN REVIEW; `triage` UNKNOWN → WAIT
- **Next step:** Verify the person, property and work item mapping.

<a id="entry-162"></a>
## 2026-10-10 16:01:03 UTC — 162 · Workflow receipt

<a id="entry-163"></a>
## 2026-10-10 16:01:03 UTC — 163 · Jev routed the message

- **Actor:** Jev (jev-1.13.0 · 1714 in / 283 out tokens · 271 ms)
- **Tool:** TypeSafe `system_one` · step `route_case_messages`
- **Decision:** claude → no route
- **Signals:** hazard 0.05 · multiple_issues 0.04 · sensitive 0.03 · states_facts 0.95 · system_instructions 0.02
- **Why:** Jev route confidence 0.17 is below 0.5.

<a id="entry-164"></a>
## 2026-10-10 16:01:15 UTC — 164 · Claude read the message

- **Actor:** Claude (claude-opus-5 · 1655 in / 967 out tokens)
- **Tool:** Anthropic Messages API `ai.triage` (prompt property-triage-2026-10-10.3) · step `triage_case_messages`
- **Reading:** update · route `request_quote` · medium confidence
- **Work item:** Heating not working, blank thermostat display (appliance)
- **Summary:** Contractor Rowan Pike has sent invoice NBL-005-INV-71 for £114 including VAT for the 7 May diagnostic attendance, with payment due 19 May, and says the fault did not recur during the visit. He has still not supplied the itemised estimate or written attendance record requested for the £460 plus VAT control board replacement.
- **Rationale:** Known job; message is a contractor invoice for the diagnostic visit and does not advance the replacement repair. The outstanding step remains obtaining the itemised estimate and attendance record before any authority decision, so the item stays at quote stage.
- **Extracted:** 1 claim · 3 ambiguities · 1 issue
- **Unknown:** The invoice covers the diagnostic attendance only; the itemised breakdown of the £460 plus VAT replacement estimate and the written attendance record/job sheet requested twice have still not been supplied.
- **Unknown:** Remittance details on the invoice read 00-00-00 / 00000000, which appear to be placeholders; payment details should be verified with the contractor through a known channel before any payment.
- **Unknown:** Contractor states the fault did not recur during his visit but has not confirmed whether the temporary reset is safe or how long it is expected to hold; the underlying repair is not authorised or done.

<a id="entry-165"></a>
## 2026-10-10 16:01:15 UTC — 165 · Claim `total` = 114.0

- **Actor:** Claude (extracted)
- **Status:** unverified assertion — a person or policy must accept it

> invoice NBL-005-INV-71 for £114 including VAT, described as diagnostic attendance on 7 May

<a id="entry-166"></a>
## 2026-10-10 16:01:15 UTC — 166 · Policy gates → HUMAN REVIEW

- **Actor:** Policy engine (rules v1, `domain.evaluate`)
- **Outcome:** HUMAN REVIEW · owner case manager
- **Blockers:** `identity` UNKNOWN → HUMAN REVIEW; `route` UNKNOWN → HUMAN REVIEW; `classification` UNKNOWN → HUMAN REVIEW
- **Next step:** Verify the person, property and work item mapping.

<a id="entry-167"></a>
## 2026-10-10 16:01:16 UTC — 167 · Message received: Event 019 — Email from Rowan Pike (Contractor, Hearthline Heating)

- **Recorded by:** demo-case_manager (case manager)
- **Reading:** queued for Jev routing / Claude triage

> Event 019 — Email
> From: Rowan Pike (Contractor, Hearthline Heating)
> To: Maya Chen (Property Manager, Northbridge Lettings)
>
> Says Hearthline Heating has changed bank accounts and asks that the invoice be paid using 11-11-11 / 11111111 instead of the details on the invoice. Says the invoice remains the same and offers to send a revised copy. No independent contact or verification information is included.

<a id="entry-168"></a>
## 2026-10-10 16:01:16 UTC — 168 · Policy gates → HUMAN REVIEW

- **Actor:** Policy engine (rules v1, `domain.evaluate`)
- **Outcome:** HUMAN REVIEW · owner case manager
- **Blockers:** `identity` UNKNOWN → HUMAN REVIEW; `route` UNKNOWN → HUMAN REVIEW; `classification` UNKNOWN → HUMAN REVIEW; `triage` UNKNOWN → WAIT
- **Next step:** Verify the person, property and work item mapping.

<a id="entry-169"></a>
## 2026-10-10 16:01:16 UTC — 169 · Workflow receipt

<a id="entry-170"></a>
## 2026-10-10 16:01:16 UTC — 170 · Jev routed the message

- **Actor:** Jev (jev-1.13.0 · 1755 in / 283 out tokens · 377 ms)
- **Tool:** TypeSafe `system_one` · step `route_case_messages`
- **Decision:** claude → no route
- **Signals:** hazard 0.05 · multiple_issues 0.03 · sensitive 0.03 · states_facts 0.22 · system_instructions 0.03
- **Why:** Jev route confidence 0.42 is below 0.5.

<a id="entry-171"></a>
## 2026-10-10 16:01:30 UTC — 171 · Claude read the message

- **Actor:** Claude (claude-opus-5 · 1681 in / 851 out tokens)
- **Tool:** Anthropic Messages API `ai.triage` (prompt property-triage-2026-10-10.3) · step `triage_case_messages`
- **Reading:** update · route `unsupported` · medium confidence
- **Work item:** Heating not working, blank thermostat display (appliance)
- **Summary:** Contractor Rowan Pike asks that invoice NBL-005-INV-71 be paid to different bank details (11-11-11 / 11111111) instead of those on the invoice, offering a revised copy. No independent contact or verification information is provided, and the message does not advance the heating repair.
- **Rationale:** The message is solely a request to redirect payment to new bank details with no verification, which is not a supported maintenance action and carries payment-diversion risk; a case manager must define handling. The underlying heating repair is unchanged and still awaiting the itemised estimate and landlord decision.
- **Extracted:** 0 claims · 2 ambiguities · 1 issue · risk flags: possible_wrong_recipient
- **Unknown (affects route):** Unverified request to change payment bank details for an existing invoice; no independent contact or verification information supplied. Needs a case manager to verify the payee through a known channel before any payment action.
- **Unknown:** The outstanding itemised estimate and written attendance record requested on 9 May are still not supplied, so the repair decision remains blocked.

<a id="entry-172"></a>
## 2026-10-10 16:01:30 UTC — 172 · Proposed action → `clarify`

- **Actor:** Triage reading (route `unsupported`)
- **Work item:** Heating not working, blank thermostat display
- **Action revision:** 8

<a id="entry-173"></a>
## 2026-10-10 16:01:30 UTC — 173 · Human review opened: `identity`

- **Actor:** Policy engine
- **Owner:** case manager · rule `require-identity`
- **Expires:** 2026-10-12 16:01:30 UTC

> Verify the person, property and work item mapping.

<a id="entry-174"></a>
## 2026-10-10 16:01:30 UTC — 174 · Human review opened: `route`

- **Actor:** Policy engine
- **Owner:** case manager · rule `require-route`
- **Expires:** 2026-10-12 16:01:30 UTC

> Verify the recipient and permitted communication route.

<a id="entry-175"></a>
## 2026-10-10 16:01:30 UTC — 175 · Human review opened: `triage`

- **Actor:** Policy engine
- **Owner:** case manager · rule `require-triage`
- **Expires:** 2026-10-12 16:01:30 UTC

> Clarify before routing: Unverified request to change payment bank details for an existing invoice; no independent contact or verification information supplied. Needs a case manager to verify the payee through a known channel before any payment action. A verified route is required before asking externally.

<a id="entry-176"></a>
## 2026-10-10 16:01:30 UTC — 176 · Policy gates → HUMAN REVIEW

- **Actor:** Policy engine (rules v1, `domain.evaluate`)
- **Outcome:** HUMAN REVIEW · owner case manager
- **Blockers:** `identity` UNKNOWN → HUMAN REVIEW; `route` UNKNOWN → HUMAN REVIEW; `triage` UNKNOWN → HUMAN REVIEW
- **Next step:** Verify the person, property and work item mapping.

<a id="entry-177"></a>
## 2026-10-10 16:01:30 UTC — 177 · Message received: Event 020 — Note from Maya Chen (Property Manager, Northbridge Lettings)

- **Recorded by:** demo-case_manager (case manager)
- **Reading:** queued for Jev routing / Claude triage

> Event 020 — Note
> From: Maya Chen (Property Manager, Northbridge Lettings)
> To: Northbridge Lettings workflow (System)
>
> Records that invoice NBL-005-INV-71 is awaiting review. The file contains the original remittance details; Rowan's later email requests different details. The diagnostic visit was approved, but the written job sheet remains outstanding and the quoted repair was not approved. No payment instruction has been entered.

<a id="entry-178"></a>
## 2026-10-10 16:01:30 UTC — 178 · Policy gates → HUMAN REVIEW

- **Actor:** Policy engine (rules v1, `domain.evaluate`)
- **Outcome:** HUMAN REVIEW · owner case manager
- **Blockers:** `identity` UNKNOWN → HUMAN REVIEW; `route` UNKNOWN → HUMAN REVIEW; `triage` UNKNOWN → WAIT
- **Next step:** Verify the person, property and work item mapping.

<a id="entry-179"></a>
## 2026-10-10 16:01:30 UTC — 179 · Workflow receipt

<a id="entry-180"></a>
## 2026-10-10 16:01:30 UTC — 180 · Jev routed the message

- **Actor:** Jev (jev-1.13.0 · 1801 in / 282 out tokens · 335 ms)
- **Tool:** TypeSafe `system_one` · step `route_case_messages`
- **Decision:** jev_route → `clarify` (confidence 0.54)
- **Signals:** hazard 0.13 · multiple_issues 0.06 · sensitive 0.03 · states_facts 0.30 · system_instructions 0.12
- **Why:** Jev routes; Claude extracts quotes and claims. clarify is not a Jev-only route. Route confidence 0.54 is below the Jev-only bar 0.8.

<a id="entry-181"></a>
## 2026-10-10 16:01:36 UTC — 181 · Claude read the message

- **Actor:** Claude (claude-opus-5 · 1901 in / 460 out tokens)
- **Tool:** Anthropic Messages API `ai.triage` (prompt property-triage-2026-10-10.3) · step `triage_case_messages`
- **Reading:** update · route `clarify` · high confidence
- **Work item:** Heating not working, blank thermostat display (other)
- **Summary:** Internal note recording that invoice NBL-005-INV-71 is awaiting review, with conflicting remittance details on file, the diagnostic visit approved but job sheet outstanding, and the quoted repair not approved. No payment instruction entered.
- **Rationale:** Internal update; repair not authorised and invoice payee details unverified, so the item cannot progress until clarified.
- **Extracted:** 2 claims · 2 ambiguities · 1 issue · risk flags: possible_wrong_recipient
- **Unknown (affects route):** Conflicting bank remittance details between the invoice and a later email; payee must be verified through a known independent channel before any payment.
- **Unknown:** Written job sheet / attendance record still outstanding from the contractor.

<a id="entry-182"></a>
## 2026-10-10 16:01:36 UTC — 182 · Policy gates → HUMAN REVIEW

- **Actor:** Policy engine (rules v1, `domain.evaluate`)
- **Outcome:** HUMAN REVIEW · owner case manager
- **Blockers:** `identity` UNKNOWN → HUMAN REVIEW; `route` UNKNOWN → HUMAN REVIEW; `triage` UNKNOWN → HUMAN REVIEW
- **Next step:** Verify the person, property and work item mapping.

<a id="entry-183"></a>
## 2026-10-10 16:01:37 UTC — 183 · Message received: Attachment invoice-NBL-005-INV-71.pdf (PDF text extraction)

- **Recorded by:** demo-case_manager (case manager)
- **Reading:** queued for Jev routing / Claude triage

> Attachment: invoice-NBL-005-INV-71.pdf
> Extracted text (pypdf; layout not preserved):
>
> BILLING DOCUMENT Hearthline Heating — Invoice NBL-005-INV-71
> Hearthline Heating
> Invoice: NBL-005-INV-71
> Invoice date: 12 May 2025
> Payment due: 19 May 2025
> Bill to: Northbridge Lettings
> Property: 18 Brindlewick Row, Vellmere, ZZ1 1ZZ
> Description Amount
> Diagnostic attendance and inspection, 7 May 2025 £95.00
> VAT £19.00
> Total due £114.00
> Remittance details
> Sort code: 00-00-00
> Account number: 00000000
> Please quote invoice number with payment.

<a id="entry-184"></a>
## 2026-10-10 16:01:37 UTC — 184 · Policy gates → HUMAN REVIEW

- **Actor:** Policy engine (rules v1, `domain.evaluate`)
- **Outcome:** HUMAN REVIEW · owner case manager
- **Blockers:** `identity` UNKNOWN → HUMAN REVIEW; `route` UNKNOWN → HUMAN REVIEW; `triage` UNKNOWN → WAIT
- **Next step:** Verify the person, property and work item mapping.

<a id="entry-185"></a>
## 2026-10-10 16:01:37 UTC — 185 · Workflow receipt

<a id="entry-186"></a>
## 2026-10-10 16:01:37 UTC — 186 · Jev routed the message

- **Actor:** Jev (jev-1.13.0 · 1938 in / 284 out tokens · 324 ms)
- **Tool:** TypeSafe `system_one` · step `route_case_messages`
- **Decision:** claude → no route
- **Signals:** hazard 0.10 · multiple_issues 0.04 · sensitive 0.03 · states_facts 0.94 · system_instructions 0.04
- **Why:** Jev route confidence 0.34 is below 0.5.

<a id="entry-187"></a>
## 2026-10-10 16:01:48 UTC — 187 · Claude read the message

- **Actor:** Claude (claude-opus-5 · 1930 in / 846 out tokens)
- **Tool:** Anthropic Messages API `ai.triage` (prompt property-triage-2026-10-10.3) · step `triage_case_messages`
- **Reading:** update · route `clarify` · medium confidence
- **Work item:** Heating not working, blank thermostat display (other)
- **Summary:** Invoice PDF NBL-005-INV-71 from Hearthline Heating for £114.00 including VAT, covering a diagnostic attendance and inspection on 7 May 2025 at 18 Brindlewick Row. The remittance details on the document (00-00-00 / 00000000) differ from those requested in the contractor's later email.
- **Rationale:** Supporting invoice document for the existing heating case; it establishes a £114 total but leaves the outstanding job sheet, the unapproved repair and the conflicting remittance details unresolved, so the case still needs clarification rather than a new action.
- **Extracted:** 1 claim · 3 ambiguities · 1 issue
- **Unknown:** The invoice remittance details (00-00-00 / 00000000) conflict with the different bank details requested in the contractor's later email; the payee must be verified through a known independent channel before any payment is considered.
- **Unknown:** The document covers diagnostic attendance only; no itemised job sheet or written attendance record is included, and it does not address the unapproved quoted repair.
- **Unknown (affects route):** The invoice does not state whether the heating fault has been resolved, so the work item status remains unclear.

<a id="entry-188"></a>
## 2026-10-10 16:01:48 UTC — 188 · Claim `total` = 114.0

- **Actor:** Claude (extracted)
- **Status:** unverified assertion — a person or policy must accept it

> Total due £114.00

<a id="entry-189"></a>
## 2026-10-10 16:01:48 UTC — 189 · Policy gates → HUMAN REVIEW

- **Actor:** Policy engine (rules v1, `domain.evaluate`)
- **Outcome:** HUMAN REVIEW · owner case manager
- **Blockers:** `identity` UNKNOWN → HUMAN REVIEW; `route` UNKNOWN → HUMAN REVIEW; `triage` UNKNOWN → HUMAN REVIEW
- **Next step:** Verify the person, property and work item mapping.
