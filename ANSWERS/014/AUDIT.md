# Case e35b4a82e105 audit trail

Heating service request at 7 Mallowmere Walk · Tenant's plug-in heater overheating - advised not to be used · 7 Mallowmere Walk, Larkfen, ZZ1 1ZZ · status open · stage HUMAN REVIEW

- **Case ID:** `e35b4a82e1054db5be645bfd0f8757d5`
- **Split from:** [bb1c8adfab87](../bb1c8adfab8743939fbc77714ff36e88/history.md)
- **Entries:** 7 (from 12 immutable records; bookkeeping and unchanged assessments omitted)
- **Raw records:** [records.jsonl](records.jsonl)
- All outbound tools are simulated adapters; no real tenant, landlord or contractor was contacted.

<a id="entry-001"></a>
## 2026-10-10 16:03:10 UTC — 001 · Message received: Split from case bb1c8adfab87: Event 012 — Email from Daniel Hart (Heating Contractor, Brackenridge Heat Services)

- **Recorded by:** Claude
- **Reading:** not required

> Event 012 — Email
> From: Daniel Hart (Heating Contractor, Brackenridge Heat Services)
> To: Maya Chen (Property Manager, Northbridge Lettings)
>
> Confirmed no same-day engineer was available. A cancellation slot might arise on 15 January but could not be reserved without a booking. Brackenridge Heat Services could not assess the property or advise on a substitute heater remotely, and advised that the heater Leah described should not be used.

<a id="entry-002"></a>
## 2026-10-10 16:03:10 UTC — 002 · Claim `urgent` = true

- **Actor:** Claude (extracted)
- **Status:** unverified assertion — a person or policy must accept it

> advised that the heater Leah described should not be used

<a id="entry-003"></a>
## 2026-10-10 16:03:10 UTC — 003 · Claim `classification` = "appliance"

- **Actor:** Claude (extracted)
- **Status:** unverified assertion — a person or policy must accept it

> advised that the heater Leah described should not be used

<a id="entry-004"></a>
## 2026-10-10 16:03:10 UTC — 004 · Human review opened: `identity`

- **Actor:** Policy engine
- **Owner:** case manager · rule `require-identity`
- **Expires:** 2026-10-12 16:03:10 UTC

> Verify the person, property and work item mapping.

<a id="entry-005"></a>
## 2026-10-10 16:03:10 UTC — 005 · Human review opened: `route`

- **Actor:** Policy engine
- **Owner:** case manager · rule `require-route`
- **Expires:** 2026-10-12 16:03:10 UTC

> Verify the recipient and permitted communication route.

<a id="entry-006"></a>
## 2026-10-10 16:03:10 UTC — 006 · Human review opened: `triage`

- **Actor:** Policy engine
- **Owner:** case manager · rule `require-triage`
- **Expires:** 2026-10-12 16:03:10 UTC

> Claude read this as a possible urgent hazard. A case manager must take over now and apply the urgent procedure.

<a id="entry-007"></a>
## 2026-10-10 16:03:10 UTC — 007 · Policy gates → HUMAN REVIEW

- **Actor:** Policy engine (rules v1, `domain.evaluate`)
- **Outcome:** HUMAN REVIEW · owner case manager
- **Blockers:** `identity` UNKNOWN → HUMAN REVIEW; `route` UNKNOWN → HUMAN REVIEW; `triage` UNKNOWN → HUMAN REVIEW
- **Next step:** Verify the person, property and work item mapping.


---

# Case d826e3f15079 audit trail

Heating service request at 7 Mallowmere Walk · Plug-in heater casing overheating · 7 Mallowmere Walk, Larkfen, ZZ1 1ZZ · status open · stage HUMAN REVIEW

- **Case ID:** `d826e3f150794342b6c2b3dbdf4888be`
- **Split from:** [bb1c8adfab87](../bb1c8adfab8743939fbc77714ff36e88/history.md)
- **Entries:** 7 (from 12 immutable records; bookkeeping and unchanged assessments omitted)
- **Raw records:** [records.jsonl](records.jsonl)
- All outbound tools are simulated adapters; no real tenant, landlord or contractor was contacted.

<a id="entry-001"></a>
## 2026-10-10 16:02:45 UTC — 001 · Message received: Split from case bb1c8adfab87: Event 008 — SMS from Leah Venn (Tenant)

- **Recorded by:** Claude
- **Reading:** not required

> Event 008 — SMS
> From: Leah Venn (Tenant)
> To: Maya Chen (Property Manager, Northbridge Lettings)
>
> Reported a living-room temperature of 12°C at 10:10. She has one small plug-in heater whose casing becomes unusually hot and has stopped using it. She may be able to stay with her niece tonight if transport can be arranged, but has not confirmed whether the home is accessible.

<a id="entry-002"></a>
## 2026-10-10 16:02:45 UTC — 002 · Claim `urgent` = true

- **Actor:** Claude (extracted)
- **Status:** unverified assertion — a person or policy must accept it

> one small plug-in heater whose casing becomes unusually hot

<a id="entry-003"></a>
## 2026-10-10 16:02:45 UTC — 003 · Claim `classification` = "appliance"

- **Actor:** Claude (extracted)
- **Status:** verified — Claude's derived category, auto-accepted by policy v1 at high confidence

> She has one small plug-in heater whose casing becomes unusually hot and has stopped using it.

<a id="entry-004"></a>
## 2026-10-10 16:02:45 UTC — 004 · Human review opened: `identity`

- **Actor:** Policy engine
- **Owner:** case manager · rule `require-identity`
- **Expires:** 2026-10-12 16:02:45 UTC

> Verify the person, property and work item mapping.

<a id="entry-005"></a>
## 2026-10-10 16:02:45 UTC — 005 · Human review opened: `route`

- **Actor:** Policy engine
- **Owner:** case manager · rule `require-route`
- **Expires:** 2026-10-12 16:02:45 UTC

> Verify the recipient and permitted communication route.

<a id="entry-006"></a>
## 2026-10-10 16:02:45 UTC — 006 · Human review opened: `triage`

- **Actor:** Policy engine
- **Owner:** case manager · rule `require-triage`
- **Expires:** 2026-10-12 16:02:45 UTC

> Claude read this as a possible urgent hazard. A case manager must take over now and apply the urgent procedure.

<a id="entry-007"></a>
## 2026-10-10 16:02:45 UTC — 007 · Policy gates → HUMAN REVIEW

- **Actor:** Policy engine (rules v1, `domain.evaluate`)
- **Outcome:** HUMAN REVIEW · owner case manager
- **Blockers:** `identity` UNKNOWN → HUMAN REVIEW; `route` UNKNOWN → HUMAN REVIEW; `triage` UNKNOWN → HUMAN REVIEW
- **Next step:** Verify the person, property and work item mapping.


---

# Case bb1c8adfab87 audit trail

Heating service request at 7 Mallowmere Walk · 7 Mallowmere Walk, Larkfen, ZZ1 1ZZ · status open · stage HUMAN REVIEW

- **Case ID:** `bb1c8adfab8743939fbc77714ff36e88`
- **Entries:** 186 (from 471 immutable records; bookkeeping and unchanged assessments omitted)
- **Raw records:** [records.jsonl](records.jsonl)
- All outbound tools are simulated adapters; no real tenant, landlord or contractor was contacted.

<a id="entry-001"></a>
## 2026-10-10 16:01:49 UTC — 001 · Message received: Intake report

- **Recorded by:** demo-case_manager (case manager)
- **Reading:** queued for Jev routing / Claude triage

> Event 001 — Portal
> From: Leah Venn (Tenant)
> To: Maya Chen (Property Manager, Northbridge Lettings)
>
> Reported that the radiators are cold and the heating controller is unresponsive. Hot water is still available. Asked for a repair appointment and said she was at home this morning.

<a id="entry-002"></a>
## 2026-10-10 16:01:49 UTC — 002 · Human review opened: `identity`

- **Actor:** Policy engine
- **Owner:** case manager · rule `require-identity`
- **Expires:** 2026-10-12 16:01:49 UTC

> Verify the person, property and work item mapping.

<a id="entry-003"></a>
## 2026-10-10 16:01:49 UTC — 003 · Human review opened: `route`

- **Actor:** Policy engine
- **Owner:** case manager · rule `require-route`
- **Expires:** 2026-10-12 16:01:49 UTC

> Verify the recipient and permitted communication route.

<a id="entry-004"></a>
## 2026-10-10 16:01:49 UTC — 004 · Policy gates → HUMAN REVIEW

- **Actor:** Policy engine (rules v1, `domain.evaluate`)
- **Outcome:** HUMAN REVIEW · owner case manager
- **Blockers:** `identity` UNKNOWN → HUMAN REVIEW; `route` UNKNOWN → HUMAN REVIEW; `triage` UNKNOWN → WAIT
- **Next step:** Verify the person, property and work item mapping.

<a id="entry-005"></a>
## 2026-10-10 16:01:49 UTC — 005 · Workflow receipt

<a id="entry-006"></a>
## 2026-10-10 16:01:50 UTC — 006 · Jev routed the message

- **Actor:** Jev (jev-1.13.0 · 1300 in / 284 out tokens · 377 ms)
- **Tool:** TypeSafe `system_one` · step `route_case_messages`
- **Decision:** claude → no route
- **Signals:** hazard 0.15 · multiple_issues 0.50 · sensitive 0.03 · states_facts 0.04 · system_instructions 0.02
- **Why:** Possibly several issues: splitting cases needs Claude.

<a id="entry-007"></a>
## 2026-10-10 16:01:59 UTC — 007 · Claude read the message

- **Actor:** Claude (claude-opus-5 · 324 in / 699 out tokens)
- **Tool:** Anthropic Messages API `ai.triage` (prompt property-triage-2026-10-10.3) · step `triage_case_messages`
- **Reading:** new request · route `request_quote` · medium confidence
- **Work item:** Cold radiators and unresponsive heating controller (other)
- **Summary:** Tenant Leah Venn reports the radiators are cold and the heating controller is unresponsive at 7 Mallowmere Walk; hot water is still available. She has asked for a repair appointment.
- **Rationale:** Newly reported heating defect with no stated hazard or vulnerability; hot water remains available, so it needs a contractor assessment/quote rather than emergency handling.
- **Extracted:** 0 claims · 4 ambiguities · 1 issue
- **Unknown (affects route):** Unclear what heating system is installed (boiler type, controller model), whether the boiler is firing and whether any error codes are shown.
- **Unknown (affects route):** Unclear whether anyone in the household is vulnerable or at particular risk from lack of heating, which would make this urgent.
- **Unknown:** Only states she was at home this morning; no ongoing availability or preferred appointment slots given.
- **Unknown:** No explicit permission to enter or access method stated for a contractor visit.

<a id="entry-008"></a>
## 2026-10-10 16:01:59 UTC — 008 · Proposed action → `request_quote`

- **Actor:** Triage reading (route `request_quote`)
- **Work item:** Cold radiators and unresponsive heating controller
- **Action revision:** 2

<a id="entry-009"></a>
## 2026-10-10 16:01:59 UTC — 009 · Human review opened: `identity`

- **Actor:** Policy engine
- **Owner:** case manager · rule `require-identity`
- **Expires:** 2026-10-12 16:01:59 UTC

> Verify the person, property and work item mapping.

<a id="entry-010"></a>
## 2026-10-10 16:01:59 UTC — 010 · Human review opened: `route`

- **Actor:** Policy engine
- **Owner:** case manager · rule `require-route`
- **Expires:** 2026-10-12 16:01:59 UTC

> Verify the recipient and permitted communication route.

<a id="entry-011"></a>
## 2026-10-10 16:01:59 UTC — 011 · Human review opened: `classification`

- **Actor:** Policy engine
- **Owner:** case manager · rule `require-classification`
- **Expires:** 2026-10-12 16:01:59 UTC

> Confirm that the category and work item match the source request. A verified route is required before asking externally.

<a id="entry-012"></a>
## 2026-10-10 16:01:59 UTC — 012 · Human review opened: `supported`

- **Actor:** Policy engine
- **Owner:** case manager · rule `require-supported`
- **Expires:** 2026-10-12 16:01:59 UTC

> A case manager must define a supported action for this situation.

<a id="entry-013"></a>
## 2026-10-10 16:01:59 UTC — 013 · Human review opened: `triage`

- **Actor:** Policy engine
- **Owner:** case manager · rule `require-triage`
- **Expires:** 2026-10-12 16:01:59 UTC

> Clarify before routing: Unclear what heating system is installed (boiler type, controller model), whether the boiler is firing and whether any error codes are shown.; Unclear whether anyone in the household is vulnerable or at particular risk from lack of heating, which would make this urgent. A verified route is required before asking externally.

<a id="entry-014"></a>
## 2026-10-10 16:01:59 UTC — 014 · Policy gates → HUMAN REVIEW

- **Actor:** Policy engine (rules v1, `domain.evaluate`)
- **Outcome:** HUMAN REVIEW · owner case manager
- **Blockers:** `identity` UNKNOWN → HUMAN REVIEW; `route` UNKNOWN → HUMAN REVIEW; `classification` UNKNOWN → HUMAN REVIEW; `supported` UNKNOWN → HUMAN REVIEW; `triage` UNKNOWN → HUMAN REVIEW
- **Next step:** Verify the person, property and work item mapping.

<a id="entry-015"></a>
## 2026-10-10 16:02:00 UTC — 015 · Message received: Event 002 — Update from Maya Chen (Property Manager, Northbridge Lettings)

- **Recorded by:** demo-case_manager (case manager)
- **Reading:** queued for Jev routing / Claude triage

> Event 002 — Update
> From: Maya Chen (Property Manager, Northbridge Lettings)
> To: Leah Venn (Tenant)
>
> Acknowledged the report and asked about the boiler display, any smell of gas or visible leak, and suitable access arrangements.

<a id="entry-016"></a>
## 2026-10-10 16:02:00 UTC — 016 · Policy gates → HUMAN REVIEW

- **Actor:** Policy engine (rules v1, `domain.evaluate`)
- **Outcome:** HUMAN REVIEW · owner case manager
- **Blockers:** `identity` UNKNOWN → HUMAN REVIEW; `route` UNKNOWN → HUMAN REVIEW; `classification` UNKNOWN → HUMAN REVIEW; `supported` UNKNOWN → HUMAN REVIEW; `triage` UNKNOWN → WAIT
- **Next step:** Verify the person, property and work item mapping.

<a id="entry-017"></a>
## 2026-10-10 16:02:00 UTC — 017 · Workflow receipt

<a id="entry-018"></a>
## 2026-10-10 16:02:00 UTC — 018 · Jev routed the message

- **Actor:** Jev (jev-1.13.0 · 1441 in / 284 out tokens · 335 ms)
- **Tool:** TypeSafe `system_one` · step `route_case_messages`
- **Decision:** jev_route → `request_quote` (confidence 0.70)
- **Signals:** hazard 0.27 · multiple_issues 0.11 · sensitive 0.03 · states_facts 0.08 · system_instructions 0.01
- **Why:** Jev routes; Claude extracts quotes and claims. Route confidence 0.70 is below the Jev-only bar 0.8.

<a id="entry-019"></a>
## 2026-10-10 16:02:09 UTC — 019 · Claude read the message

- **Actor:** Claude (claude-opus-5 · 699 in / 357 out tokens)
- **Tool:** Anthropic Messages API `ai.triage` (prompt property-triage-2026-10-10.3) · step `triage_case_messages`
- **Reading:** update · route `request_quote` · medium confidence
- **Work item:** Cold radiators and unresponsive heating controller (other)
- **Summary:** Property manager acknowledged the tenant's heating report and asked about the boiler display, any gas smell or leak, and access arrangements. No new facts or decisions provided.
- **Rationale:** Agency acknowledgement with outstanding questions; defect still needs contractor assessment, so request_quote per router decision stands.
- **Extracted:** 0 claims · 2 ambiguities · 1 issue
- **Unknown (affects route):** Boiler display status, any gas smell or visible leak still unknown - awaiting tenant reply.
- **Unknown:** Access arrangements not yet agreed; no date or entry method confirmed.

<a id="entry-020"></a>
## 2026-10-10 16:02:09 UTC — 020 · Policy gates → HUMAN REVIEW

- **Actor:** Policy engine (rules v1, `domain.evaluate`)
- **Outcome:** HUMAN REVIEW · owner case manager
- **Blockers:** `identity` UNKNOWN → HUMAN REVIEW; `route` UNKNOWN → HUMAN REVIEW; `classification` UNKNOWN → HUMAN REVIEW; `supported` UNKNOWN → HUMAN REVIEW; `triage` UNKNOWN → HUMAN REVIEW
- **Next step:** Verify the person, property and work item mapping.

<a id="entry-021"></a>
## 2026-10-10 16:02:09 UTC — 021 · Message received: Event 003 — SMS from Leah Venn (Tenant)

- **Recorded by:** demo-case_manager (case manager)
- **Reading:** queued for Jev routing / Claude triage

> Event 003 — SMS
> From: Leah Venn (Tenant)
> To: Maya Chen (Property Manager, Northbridge Lettings)
>
> Said there was no gas smell or visible leak and the boiler display was blank. She has a mobility impairment and cannot use the stairs quickly. Asked that an attendee call from outside rather than arrive unannounced.

<a id="entry-022"></a>
## 2026-10-10 16:02:09 UTC — 022 · Policy gates → HUMAN REVIEW

- **Actor:** Policy engine (rules v1, `domain.evaluate`)
- **Outcome:** HUMAN REVIEW · owner case manager
- **Blockers:** `identity` UNKNOWN → HUMAN REVIEW; `route` UNKNOWN → HUMAN REVIEW; `classification` UNKNOWN → HUMAN REVIEW; `supported` UNKNOWN → HUMAN REVIEW; `triage` UNKNOWN → WAIT
- **Next step:** Verify the person, property and work item mapping.

<a id="entry-023"></a>
## 2026-10-10 16:02:09 UTC — 023 · Workflow receipt

<a id="entry-024"></a>
## 2026-10-10 16:02:09 UTC — 024 · Jev routed the message

- **Actor:** Jev (jev-1.13.0 · 1547 in / 284 out tokens · 267 ms)
- **Tool:** TypeSafe `system_one` · step `route_case_messages`
- **Decision:** jev_route → `urgent_hazard` (confidence 0.60)
- **Signals:** hazard 0.63 · multiple_issues 0.15 · sensitive 0.96 · states_facts 0.13 · system_instructions 0.02
- **Why:** Possible hazard (Jev p=0.63); a person takes over before any automated contact.

<a id="entry-025"></a>
## 2026-10-10 16:02:14 UTC — 025 · Claude read the message

- **Actor:** Claude (claude-opus-5 · 845 in / 378 out tokens)
- **Tool:** Anthropic Messages API `ai.triage` (prompt property-triage-2026-10-10.3) · step `triage_case_messages`
- **Reading:** answer to question · route `urgent_hazard` · medium confidence
- **Work item:** Cold radiators and unresponsive heating controller (other)
- **Summary:** Tenant confirms no gas smell or visible leak and a blank boiler display. She has a mobility impairment and asks that any attendee phone from outside rather than arrive unannounced.
- **Rationale:** Router flagged possible hazard (no heating, vulnerable person) requiring a case manager; tenant's reply rules out gas smell/leak but blank display and mobility impairment support human handling.
- **Extracted:** 0 claims · 2 ambiguities · 1 issue · risk flags: vulnerable_person
- **Unknown:** No appointment date or time offered; tenant's availability still unknown.
- **Unknown:** Tenant asks attendee to call from outside; explicit permission to enter and access method not confirmed.

<a id="entry-026"></a>
## 2026-10-10 16:02:14 UTC — 026 · Proposed action → `clarify`

- **Actor:** Triage reading (route `urgent_hazard`)
- **Work item:** Cold radiators and unresponsive heating controller
- **Action revision:** 3

<a id="entry-027"></a>
## 2026-10-10 16:02:14 UTC — 027 · Claim `urgent` = true

- **Actor:** Claude (extracted)
- **Status:** unverified assertion — a person or policy must accept it

> Said there was no gas smell or visible leak and the boiler display was blank.

<a id="entry-028"></a>
## 2026-10-10 16:02:14 UTC — 028 · Human review opened: `identity`

- **Actor:** Policy engine
- **Owner:** case manager · rule `require-identity`
- **Expires:** 2026-10-12 16:02:14 UTC

> Verify the person, property and work item mapping.

<a id="entry-029"></a>
## 2026-10-10 16:02:14 UTC — 029 · Human review opened: `route`

- **Actor:** Policy engine
- **Owner:** case manager · rule `require-route`
- **Expires:** 2026-10-12 16:02:14 UTC

> Verify the recipient and permitted communication route.

<a id="entry-030"></a>
## 2026-10-10 16:02:14 UTC — 030 · Human review opened: `triage`

- **Actor:** Policy engine
- **Owner:** case manager · rule `require-triage`
- **Expires:** 2026-10-12 16:02:14 UTC

> Claude read this as a possible urgent hazard. A case manager must take over now and apply the urgent procedure.

<a id="entry-031"></a>
## 2026-10-10 16:02:14 UTC — 031 · Policy gates → HUMAN REVIEW

- **Actor:** Policy engine (rules v1, `domain.evaluate`)
- **Outcome:** HUMAN REVIEW · owner case manager
- **Blockers:** `identity` UNKNOWN → HUMAN REVIEW; `route` UNKNOWN → HUMAN REVIEW; `triage` UNKNOWN → HUMAN REVIEW
- **Next step:** Verify the person, property and work item mapping.

<a id="entry-032"></a>
## 2026-10-10 16:02:14 UTC — 032 · Message received: Event 004 — Call from Maya Chen (Property Manager, Northbridge Lettings)

- **Recorded by:** demo-case_manager (case manager)
- **Reading:** queued for Jev routing / Claude triage

> Event 004 — Call
> From: Maya Chen (Property Manager, Northbridge Lettings)
> To: Leah Venn (Tenant)
>
> Leah said her adult niece, Erin Vale, sometimes stays overnight but is not authorised to approve work or provide access in her absence. Leah asked that medical details not be shared with contractors; she agreed the agency could say she needs extra time to answer the door.

<a id="entry-033"></a>
## 2026-10-10 16:02:14 UTC — 033 · Policy gates → HUMAN REVIEW

- **Actor:** Policy engine (rules v1, `domain.evaluate`)
- **Outcome:** HUMAN REVIEW · owner case manager
- **Blockers:** `identity` UNKNOWN → HUMAN REVIEW; `route` UNKNOWN → HUMAN REVIEW; `triage` UNKNOWN → WAIT
- **Next step:** Verify the person, property and work item mapping.

<a id="entry-034"></a>
## 2026-10-10 16:02:14 UTC — 034 · Workflow receipt

<a id="entry-035"></a>
## 2026-10-10 16:02:14 UTC — 035 · Jev routed the message

- **Actor:** Jev (jev-1.13.0 · 1671 in / 284 out tokens · 262 ms)
- **Tool:** TypeSafe `system_one` · step `route_case_messages`
- **Decision:** jev_route → `urgent_hazard` (confidence 0.39)
- **Signals:** hazard 0.34 · multiple_issues 0.10 · sensitive 0.89 · states_facts 0.15 · system_instructions 0.02
- **Why:** Possible hazard (Jev p=0.34); a person takes over before any automated contact.

<a id="entry-036"></a>
## 2026-10-10 16:02:19 UTC — 036 · Claude read the message

- **Actor:** Claude (claude-opus-5 · 1041 in / 386 out tokens)
- **Tool:** Anthropic Messages API `ai.triage` (prompt property-triage-2026-10-10.3) · step `triage_case_messages`
- **Reading:** update · route `urgent_hazard` · medium confidence
- **Work item:** Cold radiators and unresponsive heating controller (other)
- **Summary:** Property manager records that the tenant's niece is not authorised to approve work or provide access, and that medical details must not be shared with contractors beyond saying she needs extra time to answer the door.
- **Rationale:** Router route retained; message is an access/authority restriction update on the existing no-heating case involving a vulnerable tenant.
- **Extracted:** 1 claim · 1 ambiguity · 1 issue · risk flags: vulnerable_person, sensitive_personal_data
- **Unknown:** Access arrangements with Leah herself (date, time, call-ahead) are still not confirmed.

<a id="entry-037"></a>
## 2026-10-10 16:02:19 UTC — 037 · Claim `access` = false

- **Actor:** Claude (extracted)
- **Status:** unverified assertion — a person or policy must accept it

> is not authorised to approve work or provide access in her absence

<a id="entry-038"></a>
## 2026-10-10 16:02:19 UTC — 038 · Claim `urgent` = true

- **Actor:** Claude (extracted)
- **Status:** unverified assertion — a person or policy must accept it

> Leah said her adult niece, Erin Vale, sometimes stays overnight but is not authorised to approve work or provide access in her absence.

<a id="entry-039"></a>
## 2026-10-10 16:02:19 UTC — 039 · Policy gates → HUMAN REVIEW

- **Actor:** Policy engine (rules v1, `domain.evaluate`)
- **Outcome:** HUMAN REVIEW · owner case manager
- **Blockers:** `identity` UNKNOWN → HUMAN REVIEW; `route` UNKNOWN → HUMAN REVIEW; `triage` UNKNOWN → HUMAN REVIEW
- **Next step:** Verify the person, property and work item mapping.

<a id="entry-040"></a>
## 2026-10-10 16:02:20 UTC — 040 · Message received: Event 005 — Email from Maya Chen (Property Manager, Northbridge Lettings)

- **Recorded by:** demo-case_manager (case manager)
- **Reading:** queued for Jev routing / Claude triage

> Event 005 — Email
> From: Maya Chen (Property Manager, Northbridge Lettings)
> To: Daniel Hart (Heating Contractor, Brackenridge Heat Services)
>
> Sent the reported symptoms and asked for the earliest diagnostic appointment, including whether a same-day visit was available. Noted that access must be arranged directly with Leah.

<a id="entry-041"></a>
## 2026-10-10 16:02:20 UTC — 041 · Policy gates → HUMAN REVIEW

- **Actor:** Policy engine (rules v1, `domain.evaluate`)
- **Outcome:** HUMAN REVIEW · owner case manager
- **Blockers:** `identity` UNKNOWN → HUMAN REVIEW; `route` UNKNOWN → HUMAN REVIEW; `triage` UNKNOWN → WAIT
- **Next step:** Verify the person, property and work item mapping.

<a id="entry-042"></a>
## 2026-10-10 16:02:20 UTC — 042 · Workflow receipt

<a id="entry-043"></a>
## 2026-10-10 16:02:20 UTC — 043 · Jev routed the message

- **Actor:** Jev (jev-1.13.0 · 1692 in / 286 out tokens · 321 ms)
- **Tool:** TypeSafe `system_one` · step `route_case_messages`
- **Decision:** jev_route → `urgent_hazard` (confidence 0.49)
- **Signals:** hazard 0.50 · multiple_issues 0.24 · sensitive 0.42 · states_facts 0.13 · system_instructions 0.02
- **Why:** Possible hazard (Jev p=0.50); a person takes over before any automated contact.

<a id="entry-044"></a>
## 2026-10-10 16:02:25 UTC — 044 · Claude read the message

- **Actor:** Claude (claude-opus-5 · 1264 in / 387 out tokens)
- **Tool:** Anthropic Messages API `ai.triage` (prompt property-triage-2026-10-10.3) · step `triage_case_messages`
- **Reading:** update · route `urgent_hazard` · medium confidence
- **Work item:** Cold radiators and unresponsive heating controller (other)
- **Summary:** Property manager emailed the heating contractor with the reported symptoms and asked for the earliest diagnostic appointment, including possible same-day attendance. Access must be arranged directly with the tenant.
- **Rationale:** Following router: no heating for a tenant with a mobility impairment is treated as potentially urgent and needs a case manager; message itself is an update arranging a diagnostic visit.
- **Extracted:** 0 claims · 2 ambiguities · 1 issue · risk flags: vulnerable_person
- **Unknown:** No appointment date or time has been agreed yet; contractor response awaited.
- **Unknown:** Access is to be arranged directly with the tenant; no consent or method recorded for a specific visit.

<a id="entry-045"></a>
## 2026-10-10 16:02:25 UTC — 045 · Claim `urgent` = true

- **Actor:** Claude (extracted)
- **Status:** unverified assertion — a person or policy must accept it

> Sent the reported symptoms and asked for the earliest diagnostic appointment, including whether a same-day visit was available.

<a id="entry-046"></a>
## 2026-10-10 16:02:25 UTC — 046 · Policy gates → HUMAN REVIEW

- **Actor:** Policy engine (rules v1, `domain.evaluate`)
- **Outcome:** HUMAN REVIEW · owner case manager
- **Blockers:** `identity` UNKNOWN → HUMAN REVIEW; `route` UNKNOWN → HUMAN REVIEW; `triage` UNKNOWN → HUMAN REVIEW
- **Next step:** Verify the person, property and work item mapping.

<a id="entry-047"></a>
## 2026-10-10 16:02:25 UTC — 047 · Message received: Event 006 — Email from Daniel Hart (Heating Contractor, Brackenridge Heat Services)

- **Recorded by:** demo-case_manager (case manager)
- **Reading:** queued for Jev routing / Claude triage

> Event 006 — Email
> From: Daniel Hart (Heating Contractor, Brackenridge Heat Services)
> To: Maya Chen (Property Manager, Northbridge Lettings)
>
> Offered the next standard appointment on 17 January, 10:00–14:00. The diagnostic call-out is a fixed £168 including VAT; replacement parts or remedial work are not included and would be quoted separately.

<a id="entry-048"></a>
## 2026-10-10 16:02:25 UTC — 048 · Policy gates → HUMAN REVIEW

- **Actor:** Policy engine (rules v1, `domain.evaluate`)
- **Outcome:** HUMAN REVIEW · owner case manager
- **Blockers:** `identity` UNKNOWN → HUMAN REVIEW; `route` UNKNOWN → HUMAN REVIEW; `triage` UNKNOWN → WAIT
- **Next step:** Verify the person, property and work item mapping.

<a id="entry-049"></a>
## 2026-10-10 16:02:25 UTC — 049 · Workflow receipt

<a id="entry-050"></a>
## 2026-10-10 16:02:26 UTC — 050 · Jev routed the message

- **Actor:** Jev (jev-1.13.0 · 1731 in / 286 out tokens · 272 ms)
- **Tool:** TypeSafe `system_one` · step `route_case_messages`
- **Decision:** jev_route → `confirm_appointment` (confidence 0.82)
- **Signals:** hazard 0.22 · multiple_issues 0.21 · sensitive 0.47 · states_facts 0.97 · system_instructions 0.01
- **Why:** Jev routes; Claude extracts quotes and claims. confirm_appointment is not a Jev-only route. The message may state facts that need exact quotes. Possible distress, complaint or vulnerability. A route change on an existing case.

<a id="entry-051"></a>
## 2026-10-10 16:02:31 UTC — 051 · Claude read the message

- **Actor:** Claude (claude-opus-5 · 1551 in / 433 out tokens)
- **Tool:** Anthropic Messages API `ai.triage` (prompt property-triage-2026-10-10.3) · step `triage_case_messages`
- **Reading:** access or appointment · route `confirm_appointment` · high confidence
- **Work item:** Cold radiators and unresponsive heating controller (other)
- **Summary:** Heating contractor Daniel Hart offers a diagnostic appointment slot on 17 January, 10:00–14:00, with a fixed call-out charge of £168 including VAT. Parts or remedial work would be quoted separately.
- **Rationale:** Contractor proposing a visit slot for a known job; next step is confirming the appointment with the tenant.
- **Extracted:** 1 claim · 2 ambiguities · 1 issue · risk flags: vulnerable_person
- **Unknown:** The offered slot is a four-hour window and has not been agreed with the tenant, who needs a call from outside before arrival.
- **Unknown:** Access must still be arranged directly with the tenant; no consent recorded for 17 January.

<a id="entry-052"></a>
## 2026-10-10 16:02:31 UTC — 052 · Proposed action → `confirm_appointment`

- **Actor:** Triage reading (route `confirm_appointment`)
- **Work item:** Cold radiators and unresponsive heating controller
- **Action revision:** 4

<a id="entry-053"></a>
## 2026-10-10 16:02:31 UTC — 053 · Claim `total` = 168.0

- **Actor:** Claude (extracted)
- **Status:** unverified assertion — a person or policy must accept it

> The diagnostic call-out is a fixed £168 including VAT

<a id="entry-054"></a>
## 2026-10-10 16:02:31 UTC — 054 · Human review opened: `identity`

- **Actor:** Policy engine
- **Owner:** case manager · rule `require-identity`
- **Expires:** 2026-10-12 16:02:31 UTC

> Verify the person, property and work item mapping.

<a id="entry-055"></a>
## 2026-10-10 16:02:31 UTC — 055 · Human review opened: `route`

- **Actor:** Policy engine
- **Owner:** case manager · rule `require-route`
- **Expires:** 2026-10-12 16:02:31 UTC

> Verify the recipient and permitted communication route.

<a id="entry-056"></a>
## 2026-10-10 16:02:31 UTC — 056 · Human review opened: `access`

- **Actor:** Policy engine
- **Owner:** access officer · rule `require-access`
- **Expires:** 2026-10-12 16:02:31 UTC

> Record consent for this visit and access method from the authorised person. A verified route is required before asking externally.

<a id="entry-057"></a>
## 2026-10-10 16:02:31 UTC — 057 · Human review opened: `authority`

- **Actor:** Policy engine
- **Owner:** approver · rule `require-authority`
- **Expires:** 2026-10-12 16:02:31 UTC

> Obtain authority for this work item, provider and action.

<a id="entry-058"></a>
## 2026-10-10 16:02:31 UTC — 058 · Human review opened: `schedule`

- **Actor:** Policy engine
- **Owner:** case manager · rule `require-schedule`
- **Expires:** 2026-10-12 16:02:31 UTC

> Confirm the active appointment with a precise date and time. A verified route is required before asking externally.

<a id="entry-059"></a>
## 2026-10-10 16:02:31 UTC — 059 · Human review opened: `supported`

- **Actor:** Policy engine
- **Owner:** case manager · rule `require-supported`
- **Expires:** 2026-10-12 16:02:31 UTC

> A case manager must define a supported action for this situation.

<a id="entry-060"></a>
## 2026-10-10 16:02:31 UTC — 060 · Policy gates → HUMAN REVIEW

- **Actor:** Policy engine (rules v1, `domain.evaluate`)
- **Outcome:** HUMAN REVIEW · owner case manager
- **Blockers:** `identity` UNKNOWN → HUMAN REVIEW; `route` UNKNOWN → HUMAN REVIEW; `access` UNKNOWN → HUMAN REVIEW; `authority` UNKNOWN → HUMAN REVIEW; `schedule` UNKNOWN → HUMAN REVIEW; `supported` UNKNOWN → HUMAN REVIEW
- **Next step:** Verify the person, property and work item mapping.

<a id="entry-061"></a>
## 2026-10-10 16:02:31 UTC — 061 · Message received: Event 007 — Note from Maya Chen (Property Manager, Northbridge Lettings)

- **Recorded by:** demo-case_manager (case manager)
- **Reading:** queued for Jev routing / Claude triage

> Event 007 — Note
> From: Maya Chen (Property Manager, Northbridge Lettings)
> To: Maya Chen (Property Manager, Northbridge Lettings)
>
> Reviewed the property authority record: the £250 limit is per urgent repair incident, inclusive of diagnostic call-out, labour and parts, and Maya may authorise qualifying urgent-repair expenditure up to that total without further landlord consent. Temporary heaters, transport and accommodation are not covered by this repair authority.

<a id="entry-062"></a>
## 2026-10-10 16:02:31 UTC — 062 · Policy gates → HUMAN REVIEW

- **Actor:** Policy engine (rules v1, `domain.evaluate`)
- **Outcome:** HUMAN REVIEW · owner case manager
- **Blockers:** `identity` UNKNOWN → HUMAN REVIEW; `route` UNKNOWN → HUMAN REVIEW; `access` UNKNOWN → HUMAN REVIEW; `authority` UNKNOWN → HUMAN REVIEW; `schedule` UNKNOWN → HUMAN REVIEW; `supported` UNKNOWN → HUMAN REVIEW; `triage` UNKNOWN → WAIT
- **Next step:** Verify the person, property and work item mapping.

<a id="entry-063"></a>
## 2026-10-10 16:02:31 UTC — 063 · Workflow receipt

<a id="entry-064"></a>
## 2026-10-10 16:02:31 UTC — 064 · Jev routed the message

- **Actor:** Jev (jev-1.13.0 · 1768 in / 284 out tokens · 326 ms)
- **Tool:** TypeSafe `system_one` · step `route_case_messages`
- **Decision:** jev_route → `confirm_appointment` (confidence 0.72)
- **Signals:** hazard 0.12 · multiple_issues 0.18 · sensitive 0.20 · states_facts 0.91 · system_instructions 0.04
- **Why:** Jev routes; Claude extracts quotes and claims. confirm_appointment is not a Jev-only route. Route confidence 0.72 is below the Jev-only bar 0.8. The message may state facts that need exact quotes.

<a id="entry-065"></a>
## 2026-10-10 16:02:37 UTC — 065 · Claude read the message

- **Actor:** Claude (claude-opus-5 · 1830 in / 433 out tokens)
- **Tool:** Anthropic Messages API `ai.triage` (prompt property-triage-2026-10-10.3) · step `triage_case_messages`
- **Reading:** update · route `confirm_appointment` · medium confidence
- **Work item:** Cold radiators and unresponsive heating controller (other)
- **Summary:** Internal note by Maya Chen recording the property authority record: a £250 per urgent repair incident limit inclusive of diagnostic call-out, labour and parts, which Maya may authorise without further landlord consent. Temporary heaters, transport and accommodation are excluded.
- **Rationale:** Internal note recording authority limits; the live next step remains confirming the offered diagnostic appointment with the tenant, matching the router decision.
- **Extracted:** 0 claims · 1 ambiguity · 1 issue
- **Unknown:** The note records a delegated spend limit but does not itself authorise the £168 diagnostic call-out or confirm the 17 January 10:00–14:00 appointment; staff should confirm whether authority is being exercised.

<a id="entry-066"></a>
## 2026-10-10 16:02:37 UTC — 066 · Policy gates → HUMAN REVIEW

- **Actor:** Policy engine (rules v1, `domain.evaluate`)
- **Outcome:** HUMAN REVIEW · owner case manager
- **Blockers:** `identity` UNKNOWN → HUMAN REVIEW; `route` UNKNOWN → HUMAN REVIEW; `access` UNKNOWN → HUMAN REVIEW; `authority` UNKNOWN → HUMAN REVIEW; `schedule` UNKNOWN → HUMAN REVIEW; `supported` UNKNOWN → HUMAN REVIEW
- **Next step:** Verify the person, property and work item mapping.

<a id="entry-067"></a>
## 2026-10-10 16:02:37 UTC — 067 · Message received: Event 008 — SMS from Leah Venn (Tenant)

- **Recorded by:** demo-case_manager (case manager)
- **Reading:** queued for Jev routing / Claude triage

> Event 008 — SMS
> From: Leah Venn (Tenant)
> To: Maya Chen (Property Manager, Northbridge Lettings)
>
> Reported a living-room temperature of 12°C at 10:10. She has one small plug-in heater whose casing becomes unusually hot and has stopped using it. She may be able to stay with her niece tonight if transport can be arranged, but has not confirmed whether the home is accessible.

<a id="entry-068"></a>
## 2026-10-10 16:02:37 UTC — 068 · Policy gates → HUMAN REVIEW

- **Actor:** Policy engine (rules v1, `domain.evaluate`)
- **Outcome:** HUMAN REVIEW · owner case manager
- **Blockers:** `identity` UNKNOWN → HUMAN REVIEW; `route` UNKNOWN → HUMAN REVIEW; `access` UNKNOWN → HUMAN REVIEW; `authority` UNKNOWN → HUMAN REVIEW; `schedule` UNKNOWN → HUMAN REVIEW; `supported` UNKNOWN → HUMAN REVIEW; `triage` UNKNOWN → WAIT
- **Next step:** Verify the person, property and work item mapping.

<a id="entry-069"></a>
## 2026-10-10 16:02:37 UTC — 069 · Workflow receipt

<a id="entry-070"></a>
## 2026-10-10 16:02:37 UTC — 070 · Jev routed the message

- **Actor:** Jev (jev-1.13.0 · 1771 in / 283 out tokens · 277 ms)
- **Tool:** TypeSafe `system_one` · step `route_case_messages`
- **Decision:** jev_route → `urgent_hazard` (confidence 0.60)
- **Signals:** hazard 0.79 · multiple_issues 0.12 · sensitive 0.15 · states_facts 0.06 · system_instructions 0.02
- **Why:** Possible hazard (Jev p=0.79); a person takes over before any automated contact.

<a id="entry-071"></a>
## 2026-10-10 16:02:45 UTC — 071 · Claude read the message

- **Actor:** Claude (claude-opus-5 · 1844 in / 615 out tokens)
- **Tool:** Anthropic Messages API `ai.triage` (prompt property-triage-2026-10-10.3) · step `triage_case_messages`
- **Reading:** update · route `urgent_hazard` · high confidence
- **Work item:** Cold radiators and unresponsive heating controller (other)
- **Summary:** Tenant reports living-room temperature of 12
insufficient heating and a plug-in heater whose casing becomes unusually hot, which she has stopped using. She may stay with her niece tonight if transport can be arranged, but accessibility there is unconfirmed.
- **Rationale:** No heating in cold conditions for a tenant with a mobility impairment, plus an overheating plug-in heater; immediate human attention required, consistent with router decision.
- **Extracted:** 2 claims · 2 ambiguities · 2 issues · risk flags: safety, vulnerable_person
- **Unknown:** Whether the tenant can actually stay with her niece tonight is unconfirmed, including transport and whether that home is accessible.
- **Unknown:** No confirmation of access or appointment timing for the 17 January slot; earlier/same-day attendance may be needed given no heating.

<a id="entry-072"></a>
## 2026-10-10 16:02:45 UTC — 072 · Proposed action → `clarify`

- **Actor:** Triage reading (route `urgent_hazard`)
- **Work item:** Cold radiators and unresponsive heating controller
- **Action revision:** 5

<a id="entry-073"></a>
## 2026-10-10 16:02:45 UTC — 073 · Claim `urgent` = true

- **Actor:** Claude (extracted)
- **Status:** unverified assertion — a person or policy must accept it

> Reported a living-room temperature of 12°C at 10:10.

<a id="entry-074"></a>
## 2026-10-10 16:02:45 UTC — 074 · Separate issue split into a new case

- **Actor:** Claude
- **Issue:** #2 of the message

<a id="entry-075"></a>
## 2026-10-10 16:02:45 UTC — 075 · Human review opened: `identity`

- **Actor:** Policy engine
- **Owner:** case manager · rule `require-identity`
- **Expires:** 2026-10-12 16:02:45 UTC

> Verify the person, property and work item mapping.

<a id="entry-076"></a>
## 2026-10-10 16:02:45 UTC — 076 · Human review opened: `route`

- **Actor:** Policy engine
- **Owner:** case manager · rule `require-route`
- **Expires:** 2026-10-12 16:02:45 UTC

> Verify the recipient and permitted communication route.

<a id="entry-077"></a>
## 2026-10-10 16:02:45 UTC — 077 · Human review opened: `triage`

- **Actor:** Policy engine
- **Owner:** case manager · rule `require-triage`
- **Expires:** 2026-10-12 16:02:45 UTC

> Claude read this as a possible urgent hazard. A case manager must take over now and apply the urgent procedure.

<a id="entry-078"></a>
## 2026-10-10 16:02:45 UTC — 078 · Policy gates → HUMAN REVIEW

- **Actor:** Policy engine (rules v1, `domain.evaluate`)
- **Outcome:** HUMAN REVIEW · owner case manager
- **Blockers:** `identity` UNKNOWN → HUMAN REVIEW; `route` UNKNOWN → HUMAN REVIEW; `triage` UNKNOWN → HUMAN REVIEW
- **Next step:** Verify the person, property and work item mapping.

<a id="entry-079"></a>
## 2026-10-10 16:02:45 UTC — 079 · Message received: Event 009 — Call from Maya Chen (Property Manager, Northbridge Lettings)

- **Recorded by:** demo-case_manager (case manager)
- **Reading:** queued for Jev routing / Claude triage

> Event 009 — Call
> From: Maya Chen (Property Manager, Northbridge Lettings)
> To: Owen Pike (Landlord)
>
> Reported the heating failure, the tenant's temperature reading and the 17 January appointment offer. Asked about a faster diagnostic visit and possible interim arrangements.

<a id="entry-080"></a>
## 2026-10-10 16:02:45 UTC — 080 · Policy gates → HUMAN REVIEW

- **Actor:** Policy engine (rules v1, `domain.evaluate`)
- **Outcome:** HUMAN REVIEW · owner case manager
- **Blockers:** `identity` UNKNOWN → HUMAN REVIEW; `route` UNKNOWN → HUMAN REVIEW; `triage` UNKNOWN → WAIT
- **Next step:** Verify the person, property and work item mapping.

<a id="entry-081"></a>
## 2026-10-10 16:02:45 UTC — 081 · Workflow receipt

<a id="entry-082"></a>
## 2026-10-10 16:02:45 UTC — 082 · Jev routed the message

- **Actor:** Jev (jev-1.13.0 · 1761 in / 282 out tokens · 220 ms)
- **Tool:** TypeSafe `system_one` · step `route_case_messages`
- **Decision:** jev_route → `urgent_hazard` (confidence 0.43)
- **Signals:** hazard 0.52 · multiple_issues 0.10 · sensitive 0.15 · states_facts 0.32 · system_instructions 0.02
- **Why:** Possible hazard (Jev p=0.52); a person takes over before any automated contact.

<a id="entry-083"></a>
## 2026-10-10 16:02:51 UTC — 083 · Claude read the message

- **Actor:** Claude (claude-opus-5 · 1858 in / 400 out tokens)
- **Tool:** Anthropic Messages API `ai.triage` (prompt property-triage-2026-10-10.3) · step `triage_case_messages`
- **Reading:** update · route `urgent_hazard` · medium confidence
- **Work item:** Cold radiators and unresponsive heating controller (other)
- **Summary:** Property manager called the landlord to report the heating failure, the tenant's 12°C reading and the contractor's 17 January appointment offer, and asked about a faster diagnostic visit and interim arrangements. No landlord decision is recorded in the message.
- **Rationale:** Loss of heating in cold conditions for a tenant with a mobility impairment; router's urgent_hazard route accepted and a person should handle next steps.
- **Extracted:** 0 claims · 2 ambiguities · 1 issue · risk flags: vulnerable_person, safety
- **Unknown:** Whether an earlier diagnostic visit than 17 January can be obtained is still unresolved.
- **Unknown:** Landlord's response on interim arrangements (heating/accommodation) is not recorded.

<a id="entry-084"></a>
## 2026-10-10 16:02:51 UTC — 084 · Claim `urgent` = true

- **Actor:** Claude (extracted)
- **Status:** unverified assertion — a person or policy must accept it

> Reported the heating failure, the tenant's temperature reading and the 17 January appointment offer.

<a id="entry-085"></a>
## 2026-10-10 16:02:51 UTC — 085 · Policy gates → HUMAN REVIEW

- **Actor:** Policy engine (rules v1, `domain.evaluate`)
- **Outcome:** HUMAN REVIEW · owner case manager
- **Blockers:** `identity` UNKNOWN → HUMAN REVIEW; `route` UNKNOWN → HUMAN REVIEW; `triage` UNKNOWN → HUMAN REVIEW
- **Next step:** Verify the person, property and work item mapping.

<a id="entry-086"></a>
## 2026-10-10 16:02:51 UTC — 086 · Message received: Event 010 — Email from Owen Pike (Landlord)

- **Recorded by:** demo-case_manager (case manager)
- **Reading:** queued for Jev routing / Claude triage

> Event 010 — Email
> From: Owen Pike (Landlord)
> To: Maya Chen (Property Manager, Northbridge Lettings)
>
> Said to obtain a quote before committing to non-emergency expenditure. He was travelling and might not respond promptly. He did not address the diagnostic appointment or temporary arrangements in this message.

<a id="entry-087"></a>
## 2026-10-10 16:02:51 UTC — 087 · Policy gates → HUMAN REVIEW

- **Actor:** Policy engine (rules v1, `domain.evaluate`)
- **Outcome:** HUMAN REVIEW · owner case manager
- **Blockers:** `identity` UNKNOWN → HUMAN REVIEW; `route` UNKNOWN → HUMAN REVIEW; `triage` UNKNOWN → WAIT
- **Next step:** Verify the person, property and work item mapping.

<a id="entry-088"></a>
## 2026-10-10 16:02:51 UTC — 088 · Workflow receipt

<a id="entry-089"></a>
## 2026-10-10 16:02:51 UTC — 089 · Jev routed the message

- **Actor:** Jev (jev-1.13.0 · 1728 in / 284 out tokens · 251 ms)
- **Tool:** TypeSafe `system_one` · step `route_case_messages`
- **Decision:** jev_route → `clarify` (confidence 0.59)
- **Signals:** hazard 0.15 · multiple_issues 0.07 · sensitive 0.07 · states_facts 0.07 · system_instructions 0.02
- **Why:** Jev routes; Claude extracts quotes and claims. clarify is not a Jev-only route. Route confidence 0.59 is below the Jev-only bar 0.8.

<a id="entry-090"></a>
## 2026-10-10 16:02:58 UTC — 090 · Claude read the message

- **Actor:** Claude (claude-opus-5 · 1872 in / 502 out tokens)
- **Tool:** Anthropic Messages API `ai.triage` (prompt property-triage-2026-10-10.3) · step `triage_case_messages`
- **Reading:** update · route `clarify` · medium confidence
- **Work item:** Cold radiators and unresponsive heating controller (other)
- **Summary:** Landlord Owen Pike instructs that a quote be obtained before committing to non-emergency expenditure, and notes he is travelling and may be slow to respond. He did not address the 17 January diagnostic appointment or interim arrangements.
- **Rationale:** Landlord response leaves the key question of whether the diagnostic visit is emergency expenditure unanswered, so the item cannot be instructed or booked yet; matches router's clarify.
- **Extracted:** 1 claim · 2 ambiguities · 1 issue · risk flags: vulnerable_person, safety
- **Unknown (affects route):** Landlord has not said whether this heating failure counts as emergency/urgent expenditure, so it is unclear if the £168 diagnostic call-out may proceed under the agency's urgent-repair authority.
- **Unknown:** Landlord did not respond to the 17 January 10:00-14:00 appointment offer or to interim heating/accommodation arrangements.

<a id="entry-091"></a>
## 2026-10-10 16:02:58 UTC — 091 · Policy gates → HUMAN REVIEW

- **Actor:** Policy engine (rules v1, `domain.evaluate`)
- **Outcome:** HUMAN REVIEW · owner case manager
- **Blockers:** `identity` UNKNOWN → HUMAN REVIEW; `route` UNKNOWN → HUMAN REVIEW; `triage` UNKNOWN → HUMAN REVIEW
- **Next step:** Verify the person, property and work item mapping.

<a id="entry-092"></a>
## 2026-10-10 16:02:58 UTC — 092 · Message received: Event 011 — Email from Maya Chen (Property Manager, Northbridge Lettings)

- **Recorded by:** demo-case_manager (case manager)
- **Reading:** queued for Jev routing / Claude triage

> Event 011 — Email
> From: Maya Chen (Property Manager, Northbridge Lettings)
> To: Daniel Hart (Heating Contractor, Brackenridge Heat Services)
>
> Asked about an earlier slot, a cancellation list and phone triage, and whether the contractor could offer safe temporary-heating advice without a visit.

<a id="entry-093"></a>
## 2026-10-10 16:02:58 UTC — 093 · Policy gates → HUMAN REVIEW

- **Actor:** Policy engine (rules v1, `domain.evaluate`)
- **Outcome:** HUMAN REVIEW · owner case manager
- **Blockers:** `identity` UNKNOWN → HUMAN REVIEW; `route` UNKNOWN → HUMAN REVIEW; `triage` UNKNOWN → WAIT
- **Next step:** Verify the person, property and work item mapping.

<a id="entry-094"></a>
## 2026-10-10 16:02:58 UTC — 094 · Workflow receipt

<a id="entry-095"></a>
## 2026-10-10 16:02:58 UTC — 095 · Jev routed the message

- **Actor:** Jev (jev-1.13.0 · 1696 in / 284 out tokens · 288 ms)
- **Tool:** TypeSafe `system_one` · step `route_case_messages`
- **Decision:** jev_route → `urgent_hazard` (confidence 0.39)
- **Signals:** hazard 0.54 · multiple_issues 0.13 · sensitive 0.17 · states_facts 0.04 · system_instructions 0.02
- **Why:** Possible hazard (Jev p=0.54); a person takes over before any automated contact.

<a id="entry-096"></a>
## 2026-10-10 16:03:03 UTC — 096 · Claude read the message

- **Actor:** Claude (claude-opus-5 · 1905 in / 411 out tokens)
- **Tool:** Anthropic Messages API `ai.triage` (prompt property-triage-2026-10-10.3) · step `triage_case_messages`
- **Reading:** update · route `urgent_hazard` · medium confidence
- **Work item:** Cold radiators and unresponsive heating controller (other)
- **Summary:** Property manager asked the heating contractor about an earlier appointment slot, a cancellation list, phone triage, and safe temporary-heating advice without a visit. No new appointment or authority confirmed.
- **Rationale:** Router flagged a possible hazard: no heating in cold conditions plus an overheating plug-in heater; a case manager should handle before further action.
- **Extracted:** 0 claims · 2 ambiguities · 1 issue · risk flags: safety, vulnerable_person
- **Unknown:** No earlier appointment has been confirmed; the 17 January 10:00-14:00 slot remains the only offer.
- **Unknown:** Whether the agency will authorise the £168 diagnostic as urgent repair expenditure is still unresolved.

<a id="entry-097"></a>
## 2026-10-10 16:03:03 UTC — 097 · Claim `urgent` = true

- **Actor:** Claude (extracted)
- **Status:** unverified assertion — a person or policy must accept it

> Asked about an earlier slot, a cancellation list and phone triage, and whether the contractor could offer safe temporary-heating advice without a visit.

<a id="entry-098"></a>
## 2026-10-10 16:03:03 UTC — 098 · Policy gates → HUMAN REVIEW

- **Actor:** Policy engine (rules v1, `domain.evaluate`)
- **Outcome:** HUMAN REVIEW · owner case manager
- **Blockers:** `identity` UNKNOWN → HUMAN REVIEW; `route` UNKNOWN → HUMAN REVIEW; `triage` UNKNOWN → HUMAN REVIEW
- **Next step:** Verify the person, property and work item mapping.

<a id="entry-099"></a>
## 2026-10-10 16:03:03 UTC — 099 · Message received: Event 012 — Email from Daniel Hart (Heating Contractor, Brackenridge Heat Services)

- **Recorded by:** demo-case_manager (case manager)
- **Reading:** queued for Jev routing / Claude triage

> Event 012 — Email
> From: Daniel Hart (Heating Contractor, Brackenridge Heat Services)
> To: Maya Chen (Property Manager, Northbridge Lettings)
>
> Confirmed no same-day engineer was available. A cancellation slot might arise on 15 January but could not be reserved without a booking. Brackenridge Heat Services could not assess the property or advise on a substitute heater remotely, and advised that the heater Leah described should not be used.

<a id="entry-100"></a>
## 2026-10-10 16:03:03 UTC — 100 · Policy gates → HUMAN REVIEW

- **Actor:** Policy engine (rules v1, `domain.evaluate`)
- **Outcome:** HUMAN REVIEW · owner case manager
- **Blockers:** `identity` UNKNOWN → HUMAN REVIEW; `route` UNKNOWN → HUMAN REVIEW; `triage` UNKNOWN → WAIT
- **Next step:** Verify the person, property and work item mapping.

<a id="entry-101"></a>
## 2026-10-10 16:03:03 UTC — 101 · Workflow receipt

<a id="entry-102"></a>
## 2026-10-10 16:03:04 UTC — 102 · Jev routed the message

- **Actor:** Jev (jev-1.13.0 · 1709 in / 286 out tokens · 272 ms)
- **Tool:** TypeSafe `system_one` · step `route_case_messages`
- **Decision:** jev_route → `urgent_hazard` (confidence 0.47)
- **Signals:** hazard 0.33 · multiple_issues 0.09 · sensitive 0.05 · states_facts 0.09 · system_instructions 0.02
- **Why:** Possible hazard (Jev p=0.33); a person takes over before any automated contact.

<a id="entry-103"></a>
## 2026-10-10 16:03:10 UTC — 103 · Claude read the message

- **Actor:** Claude (claude-opus-5 · 1867 in / 524 out tokens)
- **Tool:** Anthropic Messages API `ai.triage` (prompt property-triage-2026-10-10.3) · step `triage_case_messages`
- **Reading:** update · route `urgent_hazard` · medium confidence
- **Work item:** Cold radiators and unresponsive heating controller (other)
- **Summary:** Contractor confirms no same-day engineer; a 15 January cancellation slot may arise but cannot be held without a booking. They cannot assess or advise remotely and say the plug-in heater Leah described should not be used.
- **Rationale:** Router set urgent_hazard; unheated property in January plus an unsafe heater warrant case manager handling before booking.
- **Extracted:** 1 claim · 2 ambiguities · 2 issues · risk flags: safety
- **Unknown (affects route):** Whether to book the 17 January slot to stay eligible for a possible 15 January cancellation; no appointment is confirmed.
- **Unknown:** Interim heating arrangements for the tenant remain unresolved as the contractor cannot advise remotely.

<a id="entry-104"></a>
## 2026-10-10 16:03:10 UTC — 104 · Claim `urgent` = true

- **Actor:** Claude (extracted)
- **Status:** unverified assertion — a person or policy must accept it

> Confirmed no same-day engineer was available. A cancellation slot might arise on 15 January but could not be reserved without a booking.

<a id="entry-105"></a>
## 2026-10-10 16:03:10 UTC — 105 · Separate issue split into a new case

- **Actor:** Claude
- **Issue:** #2 of the message

<a id="entry-106"></a>
## 2026-10-10 16:03:10 UTC — 106 · Policy gates → HUMAN REVIEW

- **Actor:** Policy engine (rules v1, `domain.evaluate`)
- **Outcome:** HUMAN REVIEW · owner case manager
- **Blockers:** `identity` UNKNOWN → HUMAN REVIEW; `route` UNKNOWN → HUMAN REVIEW; `triage` UNKNOWN → HUMAN REVIEW
- **Next step:** Verify the person, property and work item mapping.

<a id="entry-107"></a>
## 2026-10-10 16:03:10 UTC — 107 · Message received: Event 013 — SMS from Leah Venn (Tenant)

- **Recorded by:** demo-case_manager (case manager)
- **Reading:** queued for Jev routing / Claude triage

> Event 013 — SMS
> From: Leah Venn (Tenant)
> To: Maya Chen (Property Manager, Northbridge Lettings)
>
> Confirmed she would not use the suspect heater. She can admit a contractor on 15 January if given at least 30 minutes' notice and a direct call. She cannot guarantee access on 17 January because of a hospital appointment. No key is held by the agency.

<a id="entry-108"></a>
## 2026-10-10 16:03:10 UTC — 108 · Policy gates → HUMAN REVIEW

- **Actor:** Policy engine (rules v1, `domain.evaluate`)
- **Outcome:** HUMAN REVIEW · owner case manager
- **Blockers:** `identity` UNKNOWN → HUMAN REVIEW; `route` UNKNOWN → HUMAN REVIEW; `triage` UNKNOWN → WAIT
- **Next step:** Verify the person, property and work item mapping.

<a id="entry-109"></a>
## 2026-10-10 16:03:10 UTC — 109 · Workflow receipt

<a id="entry-110"></a>
## 2026-10-10 16:03:11 UTC — 110 · Jev routed the message

- **Actor:** Jev (jev-1.13.0 · 1725 in / 286 out tokens · 340 ms)
- **Tool:** TypeSafe `system_one` · step `route_case_messages`
- **Decision:** jev_route → `confirm_appointment` (confidence 0.88)
- **Signals:** hazard 0.23 · multiple_issues 0.06 · sensitive 0.13 · states_facts 0.92 · system_instructions 0.02
- **Why:** Jev routes; Claude extracts quotes and claims. confirm_appointment is not a Jev-only route. The message may state facts that need exact quotes. A route change on an existing case.

<a id="entry-111"></a>
## 2026-10-10 16:03:19 UTC — 111 · Claude read the message

- **Actor:** Claude (claude-opus-5 · 1922 in / 506 out tokens)
- **Tool:** Anthropic Messages API `ai.triage` (prompt property-triage-2026-10-10.3) · step `triage_case_messages`
- **Reading:** access or appointment · route `confirm_appointment` · high confidence
- **Work item:** Cold radiators and unresponsive heating controller (other)
- **Summary:** Tenant confirms she will not use the suspect heater and can admit a contractor on 15 January with at least 30 minutes' notice and a direct call, but cannot guarantee access on 17 January due to a hospital appointment. She states the agency holds no key.
- **Rationale:** Message is about arranging contractor access for the known heating job; conditional availability and key position stated.
- **Extracted:** 2 claims · 2 ambiguities · 1 issue · risk flags: safety, vulnerable_person
- **Unknown:** No specific time on 15 January is agreed, and the 15 January cancellation slot is not confirmed; 17 January access is uncertain due to a hospital appointment.
- **Unknown:** Confirm the direct contact number for the 30-minute notice call.

<a id="entry-112"></a>
## 2026-10-10 16:03:19 UTC — 112 · Proposed action → `confirm_appointment`

- **Actor:** Triage reading (route `confirm_appointment`)
- **Work item:** Cold radiators and unresponsive heating controller
- **Action revision:** 6

<a id="entry-113"></a>
## 2026-10-10 16:03:19 UTC — 113 · Claim `access` = true

- **Actor:** Claude (extracted)
- **Status:** unverified assertion — a person or policy must accept it

> She can admit a contractor on 15 January if given at least 30 minutes' notice and a direct call.

<a id="entry-114"></a>
## 2026-10-10 16:03:19 UTC — 114 · Claim `keys` = false

- **Actor:** Claude (extracted)
- **Status:** unverified assertion — a person or policy must accept it

> No key is held by the agency.

<a id="entry-115"></a>
## 2026-10-10 16:03:19 UTC — 115 · Human review opened: `identity`

- **Actor:** Policy engine
- **Owner:** case manager · rule `require-identity`
- **Expires:** 2026-10-12 16:03:19 UTC

> Verify the person, property and work item mapping.

<a id="entry-116"></a>
## 2026-10-10 16:03:19 UTC — 116 · Human review opened: `route`

- **Actor:** Policy engine
- **Owner:** case manager · rule `require-route`
- **Expires:** 2026-10-12 16:03:19 UTC

> Verify the recipient and permitted communication route.

<a id="entry-117"></a>
## 2026-10-10 16:03:19 UTC — 117 · Human review opened: `access`

- **Actor:** Policy engine
- **Owner:** access officer · rule `require-access`
- **Expires:** 2026-10-12 16:03:19 UTC

> Record consent for this visit and access method from the authorised person. A verified route is required before asking externally.

<a id="entry-118"></a>
## 2026-10-10 16:03:19 UTC — 118 · Human review opened: `authority`

- **Actor:** Policy engine
- **Owner:** approver · rule `require-authority`
- **Expires:** 2026-10-12 16:03:19 UTC

> Obtain authority for this work item, provider and action.

<a id="entry-119"></a>
## 2026-10-10 16:03:19 UTC — 119 · Human review opened: `schedule`

- **Actor:** Policy engine
- **Owner:** case manager · rule `require-schedule`
- **Expires:** 2026-10-12 16:03:19 UTC

> Confirm the active appointment with a precise date and time. A verified route is required before asking externally.

<a id="entry-120"></a>
## 2026-10-10 16:03:19 UTC — 120 · Human review opened: `supported`

- **Actor:** Policy engine
- **Owner:** case manager · rule `require-supported`
- **Expires:** 2026-10-12 16:03:19 UTC

> A case manager must define a supported action for this situation.

<a id="entry-121"></a>
## 2026-10-10 16:03:19 UTC — 121 · Policy gates → HUMAN REVIEW

- **Actor:** Policy engine (rules v1, `domain.evaluate`)
- **Outcome:** HUMAN REVIEW · owner case manager
- **Blockers:** `identity` UNKNOWN → HUMAN REVIEW; `route` UNKNOWN → HUMAN REVIEW; `access` UNKNOWN → HUMAN REVIEW; `authority` UNKNOWN → HUMAN REVIEW; `schedule` UNKNOWN → HUMAN REVIEW; `supported` UNKNOWN → HUMAN REVIEW
- **Next step:** Verify the person, property and work item mapping.

<a id="entry-122"></a>
## 2026-10-10 16:03:19 UTC — 122 · Message received: Event 014 — Email from Owen Pike (Landlord)

- **Recorded by:** demo-case_manager (case manager)
- **Reading:** queued for Jev routing / Claude triage

> Event 014 — Email
> From: Owen Pike (Landlord)
> To: Maya Chen (Property Manager, Northbridge Lettings)
>
> Clarified that his request for a quote before committing expenditure concerned non-emergency spending and did not withdraw the standing £250 urgent-repair authority. If the incident is treated as an urgent repair, Maya may authorise the £168 diagnostic call-out without further consent; any later work must remain within the incident limit or be referred for consent.

<a id="entry-123"></a>
## 2026-10-10 16:03:19 UTC — 123 · Policy gates → HUMAN REVIEW

- **Actor:** Policy engine (rules v1, `domain.evaluate`)
- **Outcome:** HUMAN REVIEW · owner case manager
- **Blockers:** `identity` UNKNOWN → HUMAN REVIEW; `route` UNKNOWN → HUMAN REVIEW; `access` UNKNOWN → HUMAN REVIEW; `authority` UNKNOWN → HUMAN REVIEW; `schedule` UNKNOWN → HUMAN REVIEW; `supported` UNKNOWN → HUMAN REVIEW; `triage` UNKNOWN → WAIT
- **Next step:** Verify the person, property and work item mapping.

<a id="entry-124"></a>
## 2026-10-10 16:03:19 UTC — 124 · Workflow receipt

<a id="entry-125"></a>
## 2026-10-10 16:03:20 UTC — 125 · Jev routed the message

- **Actor:** Jev (jev-1.13.0 · 1763 in / 283 out tokens · 273 ms)
- **Tool:** TypeSafe `system_one` · step `route_case_messages`
- **Decision:** claude → no route
- **Signals:** hazard 0.17 · multiple_issues 0.09 · sensitive 0.15 · states_facts 0.94 · system_instructions 0.03
- **Why:** Jev route confidence 0.42 is below 0.5.

<a id="entry-126"></a>
## 2026-10-10 16:03:33 UTC — 126 · Claude read the message

- **Actor:** Claude (claude-opus-5 · 1759 in / 1093 out tokens)
- **Tool:** Anthropic Messages API `ai.triage` (prompt property-triage-2026-10-10.3) · step `triage_case_messages`
- **Reading:** update · route `instruct_work` · medium confidence
- **Work item:** Cold radiators and unresponsive heating controller (other)
- **Summary:** Landlord Owen Pike clarifies that his earlier instruction to obtain a quote applied only to non-emergency spending and that a standing £250 urgent-repair authority remains. He states Maya may authorise the £168 diagnostic call-out without further consent if the incident is treated as urgent, with later work kept within the incident limit or referred for consent.
- **Rationale:** Landlord has given conditional spend authority for the diagnostic call-out, so the next step on the known heating job is instructing the contractor to attend rather than seeking a further quote; appointment confirmation remains outstanding.
- **Extracted:** 3 claims · 3 ambiguities · 1 issue · risk flags: safety
- **Unknown (affects route):** The landlord's authority is conditional on the incident being treated as an urgent repair; staff must confirm whether that classification applies before relying on the £168 approval.
- **Unknown:** It is not stated whether the £168 figure includes VAT, nor what the 'incident limit' covers beyond the £250 standing authority.
- **Unknown:** The message does not address the possible 15 January cancellation slot or the tenant's access constraints; an appointment still needs confirming.

<a id="entry-127"></a>
## 2026-10-10 16:03:33 UTC — 127 · Proposed action → `instruct_work`

- **Actor:** Triage reading (route `instruct_work`)
- **Work item:** Cold radiators and unresponsive heating controller
- **Action revision:** 7

<a id="entry-128"></a>
## 2026-10-10 16:03:33 UTC — 128 · Claim `total` = 168.0

- **Actor:** Claude (extracted)
- **Status:** unverified assertion — a person or policy must accept it

> the £168 diagnostic call-out

<a id="entry-129"></a>
## 2026-10-10 16:03:33 UTC — 129 · Human review opened: `identity`

- **Actor:** Policy engine
- **Owner:** case manager · rule `require-identity`
- **Expires:** 2026-10-12 16:03:33 UTC

> Verify the person, property and work item mapping.

<a id="entry-130"></a>
## 2026-10-10 16:03:33 UTC — 130 · Human review opened: `route`

- **Actor:** Policy engine
- **Owner:** case manager · rule `require-route`
- **Expires:** 2026-10-12 16:03:33 UTC

> Verify the recipient and permitted communication route.

<a id="entry-131"></a>
## 2026-10-10 16:03:33 UTC — 131 · Human review opened: `access`

- **Actor:** Policy engine
- **Owner:** access officer · rule `require-access`
- **Expires:** 2026-10-12 16:03:33 UTC

> Record consent for this visit and access method from the authorised person. A verified route is required before asking externally.

<a id="entry-132"></a>
## 2026-10-10 16:03:33 UTC — 132 · Human review opened: `authority`

- **Actor:** Policy engine
- **Owner:** approver · rule `require-authority`
- **Expires:** 2026-10-12 16:03:33 UTC

> Obtain authority for this work item, provider and action.

<a id="entry-133"></a>
## 2026-10-10 16:03:33 UTC — 133 · Human review opened: `schedule`

- **Actor:** Policy engine
- **Owner:** case manager · rule `require-schedule`
- **Expires:** 2026-10-12 16:03:33 UTC

> Confirm the active appointment with a precise date and time. A verified route is required before asking externally.

<a id="entry-134"></a>
## 2026-10-10 16:03:33 UTC — 134 · Human review opened: `evidence`

- **Actor:** Policy engine
- **Owner:** case manager · rule `require-evidence`
- **Expires:** 2026-10-12 16:03:33 UTC

> Supply usable evidence required for this work item. A verified route is required before asking externally.

<a id="entry-135"></a>
## 2026-10-10 16:03:33 UTC — 135 · Human review opened: `classification`

- **Actor:** Policy engine
- **Owner:** case manager · rule `require-classification`
- **Expires:** 2026-10-12 16:03:33 UTC

> Confirm that the category and work item match the source request. A verified route is required before asking externally.

<a id="entry-136"></a>
## 2026-10-10 16:03:33 UTC — 136 · Human review opened: `total`

- **Actor:** Policy engine
- **Owner:** case manager · rule `require-total`
- **Expires:** 2026-10-12 16:03:33 UTC

> Establish the full comparable commitment, including tax. A verified route is required before asking externally.

<a id="entry-137"></a>
## 2026-10-10 16:03:33 UTC — 137 · Human review opened: `supported`

- **Actor:** Policy engine
- **Owner:** case manager · rule `require-supported`
- **Expires:** 2026-10-12 16:03:33 UTC

> A case manager must define a supported action for this situation.

<a id="entry-138"></a>
## 2026-10-10 16:03:34 UTC — 138 · Human review opened: `triage`

- **Actor:** Policy engine
- **Owner:** case manager · rule `require-triage`
- **Expires:** 2026-10-12 16:03:33 UTC

> Clarify before routing: The landlord's authority is conditional on the incident being treated as an urgent repair; staff must confirm whether that classification applies before relying on the £168 approval. A verified route is required before asking externally.

<a id="entry-139"></a>
## 2026-10-10 16:03:34 UTC — 139 · Policy gates → HUMAN REVIEW

- **Actor:** Policy engine (rules v1, `domain.evaluate`)
- **Outcome:** HUMAN REVIEW · owner case manager
- **Blockers:** `identity` UNKNOWN → HUMAN REVIEW; `route` UNKNOWN → HUMAN REVIEW; `access` UNKNOWN → HUMAN REVIEW; `authority` UNKNOWN → HUMAN REVIEW; `schedule` UNKNOWN → HUMAN REVIEW; `evidence` UNKNOWN → HUMAN REVIEW; `classification` UNKNOWN → HUMAN REVIEW; `total` UNKNOWN → HUMAN REVIEW; `supported` UNKNOWN → HUMAN REVIEW; `triage` UNKNOWN → HUMAN REVIEW
- **Next step:** Verify the person, property and work item mapping.

<a id="entry-140"></a>
## 2026-10-10 16:03:34 UTC — 140 · Message received: Event 015 — Call from Maya Chen (Property Manager, Northbridge Lettings)

- **Recorded by:** demo-case_manager (case manager)
- **Reading:** queued for Jev routing / Claude triage

> Event 015 — Call
> From: Maya Chen (Property Manager, Northbridge Lettings)
> To: Leah Venn (Tenant)
>
> Discussed possible interim arrangements. Leah said she has no suitable spare heater and is concerned about carrying one because of her mobility impairment. She asked whether delivery of a heater or transport to her niece's home could be arranged. She still needed to check whether the niece's entrance was step-free.

<a id="entry-141"></a>
## 2026-10-10 16:03:34 UTC — 141 · Policy gates → HUMAN REVIEW

- **Actor:** Policy engine (rules v1, `domain.evaluate`)
- **Outcome:** HUMAN REVIEW · owner case manager
- **Blockers:** `identity` UNKNOWN → HUMAN REVIEW; `route` UNKNOWN → HUMAN REVIEW; `access` UNKNOWN → HUMAN REVIEW; `authority` UNKNOWN → HUMAN REVIEW; `schedule` UNKNOWN → HUMAN REVIEW; `evidence` UNKNOWN → HUMAN REVIEW; `classification` UNKNOWN → HUMAN REVIEW; `total` UNKNOWN → HUMAN REVIEW; `supported` UNKNOWN → HUMAN REVIEW; `triage` UNKNOWN → WAIT
- **Next step:** Verify the person, property and work item mapping.

<a id="entry-142"></a>
## 2026-10-10 16:03:34 UTC — 142 · Workflow receipt

<a id="entry-143"></a>
## 2026-10-10 16:03:34 UTC — 143 · Jev routed the message

- **Actor:** Jev (jev-1.13.0 · 1783 in / 285 out tokens · 313 ms)
- **Tool:** TypeSafe `system_one` · step `route_case_messages`
- **Decision:** jev_route → `urgent_hazard` (confidence 0.39)
- **Signals:** hazard 0.69 · multiple_issues 0.06 · sensitive 0.89 · states_facts 0.05 · system_instructions 0.02
- **Why:** Possible hazard (Jev p=0.69); a person takes over before any automated contact.

<a id="entry-144"></a>
## 2026-10-10 16:03:40 UTC — 144 · Claude read the message

- **Actor:** Claude (claude-opus-5 · 1900 in / 435 out tokens)
- **Tool:** Anthropic Messages API `ai.triage` (prompt property-triage-2026-10-10.3) · step `triage_case_messages`
- **Reading:** update · route `urgent_hazard` · medium confidence
- **Work item:** Cold radiators and unresponsive heating controller (other)
- **Summary:** Maya Chen called the tenant about interim heating arrangements. Leah has no suitable spare heater, cannot carry one due to a mobility impairment, and asked whether a heater could be delivered or transport to her niece's home arranged; she still needs to check step-free access there.
- **Rationale:** Vulnerable tenant without heating in January and no viable interim heat source; router's urgent_hazard route is appropriate for case manager handling.
- **Extracted:** 0 claims · 2 ambiguities · 1 issue · risk flags: vulnerable_person, safety
- **Unknown (affects route):** Whether the desk can arrange delivery of a temporary heater or transport to the niece's home, and who authorises that cost.
- **Unknown:** Step-free access at the niece's address is unconfirmed, so the relocation option cannot yet be relied on.

<a id="entry-145"></a>
## 2026-10-10 16:03:40 UTC — 145 · Proposed action → `clarify`

- **Actor:** Triage reading (route `urgent_hazard`)
- **Work item:** Cold radiators and unresponsive heating controller
- **Action revision:** 8

<a id="entry-146"></a>
## 2026-10-10 16:03:40 UTC — 146 · Claim `urgent` = true

- **Actor:** Claude (extracted)
- **Status:** unverified assertion — a person or policy must accept it

> Discussed possible interim arrangements. Leah said she has no suitable spare heater and is concerned about carrying one because of her mobility impairment.

<a id="entry-147"></a>
## 2026-10-10 16:03:40 UTC — 147 · Human review opened: `identity`

- **Actor:** Policy engine
- **Owner:** case manager · rule `require-identity`
- **Expires:** 2026-10-12 16:03:40 UTC

> Verify the person, property and work item mapping.

<a id="entry-148"></a>
## 2026-10-10 16:03:40 UTC — 148 · Human review opened: `route`

- **Actor:** Policy engine
- **Owner:** case manager · rule `require-route`
- **Expires:** 2026-10-12 16:03:40 UTC

> Verify the recipient and permitted communication route.

<a id="entry-149"></a>
## 2026-10-10 16:03:40 UTC — 149 · Human review opened: `triage`

- **Actor:** Policy engine
- **Owner:** case manager · rule `require-triage`
- **Expires:** 2026-10-12 16:03:40 UTC

> Claude read this as a possible urgent hazard. A case manager must take over now and apply the urgent procedure.

<a id="entry-150"></a>
## 2026-10-10 16:03:40 UTC — 150 · Policy gates → HUMAN REVIEW

- **Actor:** Policy engine (rules v1, `domain.evaluate`)
- **Outcome:** HUMAN REVIEW · owner case manager
- **Blockers:** `identity` UNKNOWN → HUMAN REVIEW; `route` UNKNOWN → HUMAN REVIEW; `triage` UNKNOWN → HUMAN REVIEW
- **Next step:** Verify the person, property and work item mapping.

<a id="entry-151"></a>
## 2026-10-10 16:03:40 UTC — 151 · Message received: Event 016 — Email from Maya Chen (Property Manager, Northbridge Lettings)

- **Recorded by:** demo-case_manager (case manager)
- **Reading:** queued for Jev routing / Claude triage

> Event 016 — Email
> From: Maya Chen (Property Manager, Northbridge Lettings)
> To: Priya Noll (Duty Manager, Northbridge Lettings)
>
> Escalated the cold-weather report, access requirements, late standard appointment and available £250 urgent-repair authority. Asked what cover or separate spending authority applied to temporary heating, transport or accommodation.

<a id="entry-152"></a>
## 2026-10-10 16:03:40 UTC — 152 · Policy gates → HUMAN REVIEW

- **Actor:** Policy engine (rules v1, `domain.evaluate`)
- **Outcome:** HUMAN REVIEW · owner case manager
- **Blockers:** `identity` UNKNOWN → HUMAN REVIEW; `route` UNKNOWN → HUMAN REVIEW; `triage` UNKNOWN → WAIT
- **Next step:** Verify the person, property and work item mapping.

<a id="entry-153"></a>
## 2026-10-10 16:03:40 UTC — 153 · Workflow receipt

<a id="entry-154"></a>
## 2026-10-10 16:03:41 UTC — 154 · Jev routed the message

- **Actor:** Jev (jev-1.13.0 · 1766 in / 284 out tokens · 551 ms)
- **Tool:** TypeSafe `system_one` · step `route_case_messages`
- **Decision:** jev_route → `urgent_hazard` (confidence 0.79)
- **Signals:** hazard 0.67 · multiple_issues 0.17 · sensitive 0.53 · states_facts 0.64 · system_instructions 0.02
- **Why:** Possible hazard (Jev p=0.67); a person takes over before any automated contact.

<a id="entry-155"></a>
## 2026-10-10 16:03:48 UTC — 155 · Claude read the message

- **Actor:** Claude (claude-opus-5 · 1909 in / 460 out tokens)
- **Tool:** Anthropic Messages API `ai.triage` (prompt property-triage-2026-10-10.3) · step `triage_case_messages`
- **Reading:** update · route `urgent_hazard` · medium confidence
- **Work item:** Cold radiators and unresponsive heating controller (other)
- **Summary:** Maya Chen has escalated the cold-weather heating failure internally to the duty manager, covering access requirements, the late standard appointment slot and the £250 urgent-repair authority. She asks what cover or separate spending authority applies to temporary heating, transport or accommodation.
- **Rationale:** Internal escalation of a no-heating situation affecting a tenant with a mobility impairment in cold weather; a case manager must take it on, consistent with the router's urgent_hazard route.
- **Extracted:** 0 claims · 2 ambiguities · 1 issue · risk flags: vulnerable_person, safety
- **Unknown:** Whether temporary heating, transport or alternative accommodation costs are covered, and who authorises that spend beyond the £250 urgent-repair authority.
- **Unknown:** No confirmed appointment date and time for the diagnostic visit; tenant can only admit on 15 January with 30 minutes' notice.

<a id="entry-156"></a>
## 2026-10-10 16:03:48 UTC — 156 · Claim `urgent` = true

- **Actor:** Claude (extracted)
- **Status:** unverified assertion — a person or policy must accept it

> Escalated the cold-weather report, access requirements, late standard appointment and available £250 urgent-repair authority.

<a id="entry-157"></a>
## 2026-10-10 16:03:48 UTC — 157 · Policy gates → HUMAN REVIEW

- **Actor:** Policy engine (rules v1, `domain.evaluate`)
- **Outcome:** HUMAN REVIEW · owner case manager
- **Blockers:** `identity` UNKNOWN → HUMAN REVIEW; `route` UNKNOWN → HUMAN REVIEW; `triage` UNKNOWN → HUMAN REVIEW
- **Next step:** Verify the person, property and work item mapping.

<a id="entry-158"></a>
## 2026-10-10 16:03:48 UTC — 158 · Message received: Event 017 — Update from Priya Noll (Duty Manager, Northbridge Lettings)

- **Recorded by:** demo-case_manager (case manager)
- **Reading:** queued for Jev routing / Claude triage

> Event 017 — Update
> From: Priya Noll (Duty Manager, Northbridge Lettings)
> To: Maya Chen (Property Manager, Northbridge Lettings)
>
> Confirmed the office could contact the landlord again and check approved suppliers for heater delivery. The duty file records no separate spending limit for temporary equipment, transport or accommodation.

<a id="entry-159"></a>
## 2026-10-10 16:03:48 UTC — 159 · Policy gates → HUMAN REVIEW

- **Actor:** Policy engine (rules v1, `domain.evaluate`)
- **Outcome:** HUMAN REVIEW · owner case manager
- **Blockers:** `identity` UNKNOWN → HUMAN REVIEW; `route` UNKNOWN → HUMAN REVIEW; `triage` UNKNOWN → WAIT
- **Next step:** Verify the person, property and work item mapping.

<a id="entry-160"></a>
## 2026-10-10 16:03:49 UTC — 160 · Workflow receipt

<a id="entry-161"></a>
## 2026-10-10 16:03:49 UTC — 161 · Jev routed the message

- **Actor:** Jev (jev-1.13.0 · 1763 in / 282 out tokens · 286 ms)
- **Tool:** TypeSafe `system_one` · step `route_case_messages`
- **Decision:** jev_route → `urgent_hazard` (confidence 0.60)
- **Signals:** hazard 0.35 · multiple_issues 0.10 · sensitive 0.49 · states_facts 0.08 · system_instructions 0.02
- **Why:** Possible hazard (Jev p=0.35); a person takes over before any automated contact.

<a id="entry-162"></a>
## 2026-10-10 16:03:54 UTC — 162 · Claude read the message

- **Actor:** Claude (claude-opus-5 · 1886 in / 411 out tokens)
- **Tool:** Anthropic Messages API `ai.triage` (prompt property-triage-2026-10-10.3) · step `triage_case_messages`
- **Reading:** update · route `urgent_hazard` · medium confidence
- **Work item:** Cold radiators and unresponsive heating controller (other)
- **Summary:** Duty Manager confirms the office can contact the landlord again and check approved suppliers for heater delivery, and that the duty file records no separate spending limit for temporary heating, transport or accommodation.
- **Rationale:** Internal update on an open heating case with no heat for a tenant with mobility impairment in cold weather; router's urgent_hazard route retained for human handling.
- **Extracted:** 0 claims · 2 ambiguities · 1 issue · risk flags: vulnerable_person, safety
- **Unknown:** No spending authority exists for temporary heating, transport or accommodation; staff need a decision on who authorises these costs for a vulnerable tenant without heating.
- **Unknown:** Whether a 15 January cancellation slot can be booked with the 30 minutes' notice and direct call the tenant requires.

<a id="entry-163"></a>
## 2026-10-10 16:03:54 UTC — 163 · Claim `urgent` = true

- **Actor:** Claude (extracted)
- **Status:** unverified assertion — a person or policy must accept it

> The duty file records no separate spending limit for temporary equipment, transport or accommodation.

<a id="entry-164"></a>
## 2026-10-10 16:03:54 UTC — 164 · Policy gates → HUMAN REVIEW

- **Actor:** Policy engine (rules v1, `domain.evaluate`)
- **Outcome:** HUMAN REVIEW · owner case manager
- **Blockers:** `identity` UNKNOWN → HUMAN REVIEW; `route` UNKNOWN → HUMAN REVIEW; `triage` UNKNOWN → HUMAN REVIEW
- **Next step:** Verify the person, property and work item mapping.

<a id="entry-165"></a>
## 2026-10-10 16:03:54 UTC — 165 · Message received: Event 018 — Portal from Leah Venn (Tenant)

- **Recorded by:** demo-case_manager (case manager)
- **Reading:** queued for Jev routing / Claude triage

> Event 018 — Portal
> From: Leah Venn (Tenant)
> To: Maya Chen (Property Manager, Northbridge Lettings)
>
> Reported the living-room temperature as 10°C at 16:25. Her niece's spare room might be available tonight, but Leah had not confirmed whether the entrance was step-free. Asked for an update before the office closed. No appointment or interim arrangement had been confirmed.

<a id="entry-166"></a>
## 2026-10-10 16:03:54 UTC — 166 · Policy gates → HUMAN REVIEW

- **Actor:** Policy engine (rules v1, `domain.evaluate`)
- **Outcome:** HUMAN REVIEW · owner case manager
- **Blockers:** `identity` UNKNOWN → HUMAN REVIEW; `route` UNKNOWN → HUMAN REVIEW; `triage` UNKNOWN → WAIT
- **Next step:** Verify the person, property and work item mapping.

<a id="entry-167"></a>
## 2026-10-10 16:03:54 UTC — 167 · Workflow receipt

<a id="entry-168"></a>
## 2026-10-10 16:03:55 UTC — 168 · Jev routed the message

- **Actor:** Jev (jev-1.13.0 · 1747 in / 283 out tokens · 354 ms)
- **Tool:** TypeSafe `system_one` · step `route_case_messages`
- **Decision:** jev_route → `urgent_hazard` (confidence 0.56)
- **Signals:** hazard 0.78 · multiple_issues 0.12 · sensitive 0.77 · states_facts 0.05 · system_instructions 0.02
- **Why:** Possible hazard (Jev p=0.78); a person takes over before any automated contact.

<a id="entry-169"></a>
## 2026-10-10 16:04:01 UTC — 169 · Claude read the message

- **Actor:** Claude (claude-opus-5 · 1900 in / 502 out tokens)
- **Tool:** Anthropic Messages API `ai.triage` (prompt property-triage-2026-10-10.3) · step `triage_case_messages`
- **Reading:** chase · route `urgent_hazard` · high confidence
- **Work item:** Cold radiators and unresponsive heating controller (other)
- **Summary:** Tenant reports the living-room at 10°C at 16:25 with no heating fix, appointment or interim arrangement confirmed, and asks for an update before the office closes. A possible stay at her niece's is unconfirmed pending step-free access.
- **Rationale:** Cold-weather no-heating report at 10°C for a tenant with mobility impairment; needs immediate human handling, consistent with router decision.
- **Extracted:** 2 claims · 2 ambiguities · 1 issue · risk flags: safety, vulnerable_person, distress
- **Unknown:** Whether the niece's spare room is usable tonight depends on step-free entrance, still unconfirmed.
- **Unknown:** No appointment date/time agreed; tenant previously offered 15 January with 30 minutes' notice.

<a id="entry-170"></a>
## 2026-10-10 16:04:01 UTC — 170 · Claim `urgent` = true

- **Actor:** Claude (extracted)
- **Status:** unverified assertion — a person or policy must accept it

> Reported the living-room temperature as 10°C at 16:25.

<a id="entry-171"></a>
## 2026-10-10 16:04:01 UTC — 171 · Claim `schedule` = false

- **Actor:** Claude (extracted)
- **Status:** unverified assertion — a person or policy must accept it

> No appointment or interim arrangement had been confirmed.

<a id="entry-172"></a>
## 2026-10-10 16:04:01 UTC — 172 · Policy gates → HUMAN REVIEW

- **Actor:** Policy engine (rules v1, `domain.evaluate`)
- **Outcome:** HUMAN REVIEW · owner case manager
- **Blockers:** `identity` UNKNOWN → HUMAN REVIEW; `route` UNKNOWN → HUMAN REVIEW; `triage` UNKNOWN → HUMAN REVIEW
- **Next step:** Verify the person, property and work item mapping.

<a id="entry-173"></a>
## 2026-10-10 16:04:02 UTC — 173 · Message received: Event 019 — Call from Daniel Hart (Heating Contractor, Brackenridge Heat Services)

- **Recorded by:** demo-case_manager (case manager)
- **Reading:** queued for Jev routing / Claude triage

> Event 019 — Call
> From: Daniel Hart (Heating Contractor, Brackenridge Heat Services)
> To: Maya Chen (Property Manager, Northbridge Lettings)
>
> Said a cancellation appointment for 15 January, 09:00–11:00, had become available and could be held only if booked by 17:30. It would be the same £168 diagnostic call-out; no repair work or parts were included. Leah's direct confirmation of access, including the required call and notice, would still be needed. The slot has not been booked.

<a id="entry-174"></a>
## 2026-10-10 16:04:02 UTC — 174 · Policy gates → HUMAN REVIEW

- **Actor:** Policy engine (rules v1, `domain.evaluate`)
- **Outcome:** HUMAN REVIEW · owner case manager
- **Blockers:** `identity` UNKNOWN → HUMAN REVIEW; `route` UNKNOWN → HUMAN REVIEW; `triage` UNKNOWN → WAIT
- **Next step:** Verify the person, property and work item mapping.

<a id="entry-175"></a>
## 2026-10-10 16:04:02 UTC — 175 · Workflow receipt

<a id="entry-176"></a>
## 2026-10-10 16:04:02 UTC — 176 · Jev routed the message

- **Actor:** Jev (jev-1.13.0 · 1787 in / 284 out tokens · 404 ms)
- **Tool:** TypeSafe `system_one` · step `route_case_messages`
- **Decision:** jev_route → `confirm_appointment` (confidence 0.82)
- **Signals:** hazard 0.22 · multiple_issues 0.07 · sensitive 0.13 · states_facts 0.94 · system_instructions 0.02
- **Why:** Jev routes; Claude extracts quotes and claims. confirm_appointment is not a Jev-only route. The message may state facts that need exact quotes. A route change on an existing case.

<a id="entry-177"></a>
## 2026-10-10 16:04:09 UTC — 177 · Claude read the message

- **Actor:** Claude (claude-opus-5 · 1950 in / 501 out tokens)
- **Tool:** Anthropic Messages API `ai.triage` (prompt property-triage-2026-10-10.3) · step `triage_case_messages`
- **Reading:** access or appointment · route `confirm_appointment` · high confidence
- **Work item:** Cold radiators and unresponsive heating controller (other)
- **Summary:** Contractor Daniel Hart reports a cancellation slot on 15 January 09:00–11:00 available if booked by 17:30, at the same £168 diagnostic call-out with no repair or parts included. The slot is not booked and the tenant's direct access confirmation with call and notice is still needed.
- **Rationale:** Message concerns arranging a visit for an already known job; slot not yet booked so no schedule claim.
- **Extracted:** 1 claim · 3 ambiguities · 1 issue
- **Unknown:** The slot is offered but not booked; needs booking by 17:30 to hold it.
- **Unknown:** Tenant's direct confirmation of access, with required call and 30 minutes' notice, is still outstanding.
- **Unknown:** Whether £168 includes VAT is not stated.

<a id="entry-178"></a>
## 2026-10-10 16:04:09 UTC — 178 · Proposed action → `confirm_appointment`

- **Actor:** Triage reading (route `confirm_appointment`)
- **Work item:** Cold radiators and unresponsive heating controller
- **Action revision:** 9

<a id="entry-179"></a>
## 2026-10-10 16:04:09 UTC — 179 · Claim `total` = 168.0

- **Actor:** Claude (extracted)
- **Status:** unverified assertion — a person or policy must accept it

> It would be the same £168 diagnostic call-out; no repair work or parts were included.

<a id="entry-180"></a>
## 2026-10-10 16:04:09 UTC — 180 · Human review opened: `identity`

- **Actor:** Policy engine
- **Owner:** case manager · rule `require-identity`
- **Expires:** 2026-10-12 16:04:09 UTC

> Verify the person, property and work item mapping.

<a id="entry-181"></a>
## 2026-10-10 16:04:09 UTC — 181 · Human review opened: `route`

- **Actor:** Policy engine
- **Owner:** case manager · rule `require-route`
- **Expires:** 2026-10-12 16:04:09 UTC

> Verify the recipient and permitted communication route.

<a id="entry-182"></a>
## 2026-10-10 16:04:09 UTC — 182 · Human review opened: `access`

- **Actor:** Policy engine
- **Owner:** access officer · rule `require-access`
- **Expires:** 2026-10-12 16:04:09 UTC

> Record consent for this visit and access method from the authorised person. A verified route is required before asking externally.

<a id="entry-183"></a>
## 2026-10-10 16:04:09 UTC — 183 · Human review opened: `authority`

- **Actor:** Policy engine
- **Owner:** approver · rule `require-authority`
- **Expires:** 2026-10-12 16:04:09 UTC

> Obtain authority for this work item, provider and action.

<a id="entry-184"></a>
## 2026-10-10 16:04:09 UTC — 184 · Human review opened: `schedule`

- **Actor:** Policy engine
- **Owner:** case manager · rule `require-schedule`
- **Expires:** 2026-10-12 16:04:09 UTC

> Confirm the active appointment with a precise date and time. A verified route is required before asking externally.

<a id="entry-185"></a>
## 2026-10-10 16:04:09 UTC — 185 · Human review opened: `supported`

- **Actor:** Policy engine
- **Owner:** case manager · rule `require-supported`
- **Expires:** 2026-10-12 16:04:09 UTC

> A case manager must define a supported action for this situation.

<a id="entry-186"></a>
## 2026-10-10 16:04:09 UTC — 186 · Policy gates → HUMAN REVIEW

- **Actor:** Policy engine (rules v1, `domain.evaluate`)
- **Outcome:** HUMAN REVIEW · owner case manager
- **Blockers:** `identity` UNKNOWN → HUMAN REVIEW; `route` UNKNOWN → HUMAN REVIEW; `access` UNKNOWN → HUMAN REVIEW; `authority` UNKNOWN → HUMAN REVIEW; `schedule` UNKNOWN → HUMAN REVIEW; `supported` UNKNOWN → HUMAN REVIEW
- **Next step:** Verify the person, property and work item mapping.
