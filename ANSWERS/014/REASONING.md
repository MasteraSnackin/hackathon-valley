# Reasoning — Property Management case 014

Exported from the system's recorded policy assessments, claims and concise model rationales. It is not reconstructed after the fact and does not contain hidden chain-of-thought.

## System case `e35b4a82e105` — HUMAN REVIEW

### Why this decision (policy gates)

The model cannot create authority: the policy engine decides from recorded checks. Each blocker below kept the action from running.

- `identity` is **UNKNOWN** → HUMAN REVIEW (rule `require-identity`, owner case manager): Verify the person, property and work item mapping. — evidence: no source recorded
- `route` is **UNKNOWN** → HUMAN REVIEW (rule `require-route`, owner case manager): Verify the recipient and permitted communication route. — evidence: no source recorded
- `triage` is **UNKNOWN** → HUMAN REVIEW (rule `require-triage`, owner case manager): Claude read this as a possible urgent hazard. A case manager must take over now and apply the urgent procedure. — evidence: Split from case bb1c8adfab87: Event 012 — Email from Daniel Hart (Heating Contractor, Brackenridge Heat Services)

### Claims extracted from the sources

Every claim is a source assertion with an exact quote; unverified claims were never used as authority.

- `urgent` = true — unverified assertion; from Split from case bb1c8adfab87: Event 012 — Email from Daniel Hart (Heating Contractor, Brackenridge Heat Services): “advised that the heater Leah described should not be used”
- `classification` = true — unverified assertion; from Split from case bb1c8adfab87: Event 012 — Email from Daniel Hart (Heating Contractor, Brackenridge Heat Services): “advised that the heater Leah described should not be used”

### Reading of each source (Jev route → Claude reading)

## System case `d826e3f15079` — HUMAN REVIEW

### Why this decision (policy gates)

The model cannot create authority: the policy engine decides from recorded checks. Each blocker below kept the action from running.

- `identity` is **UNKNOWN** → HUMAN REVIEW (rule `require-identity`, owner case manager): Verify the person, property and work item mapping. — evidence: no source recorded
- `route` is **UNKNOWN** → HUMAN REVIEW (rule `require-route`, owner case manager): Verify the recipient and permitted communication route. — evidence: no source recorded
- `triage` is **UNKNOWN** → HUMAN REVIEW (rule `require-triage`, owner case manager): Claude read this as a possible urgent hazard. A case manager must take over now and apply the urgent procedure. — evidence: Split from case bb1c8adfab87: Event 008 — SMS from Leah Venn (Tenant)

### Claims extracted from the sources

Every claim is a source assertion with an exact quote; unverified claims were never used as authority.

- `urgent` = true — unverified assertion; from Split from case bb1c8adfab87: Event 008 — SMS from Leah Venn (Tenant): “one small plug-in heater whose casing becomes unusually hot”
- `classification` = true — verified; from Split from case bb1c8adfab87: Event 008 — SMS from Leah Venn (Tenant): “She has one small plug-in heater whose casing becomes unusually hot and has stopped using it.”

### Reading of each source (Jev route → Claude reading)

## System case `bb1c8adfab87` — HUMAN REVIEW

### Why this decision (policy gates)

The model cannot create authority: the policy engine decides from recorded checks. Each blocker below kept the action from running.

- `identity` is **UNKNOWN** → HUMAN REVIEW (rule `require-identity`, owner case manager): Verify the person, property and work item mapping. — evidence: no source recorded
- `route` is **UNKNOWN** → HUMAN REVIEW (rule `require-route`, owner case manager): Verify the recipient and permitted communication route. — evidence: no source recorded
- `access` is **UNKNOWN** → HUMAN REVIEW (rule `require-access`, owner access officer): Record consent for this visit and access method from the authorised person. A verified route is required before asking externally. — evidence: Event 013 — SMS from Leah Venn (Tenant)
- `authority` is **UNKNOWN** → HUMAN REVIEW (rule `require-authority`, owner approver): Obtain authority for this work item, provider and action. — evidence: no source recorded
- `schedule` is **UNKNOWN** → HUMAN REVIEW (rule `require-schedule`, owner case manager): Confirm the active appointment with a precise date and time. A verified route is required before asking externally. — evidence: no source recorded
- `supported` is **UNKNOWN** → HUMAN REVIEW (rule `require-supported`, owner case manager): A case manager must define a supported action for this situation. — evidence: no source recorded

### Claims extracted from the sources

Every claim is a source assertion with an exact quote; unverified claims were never used as authority.

- `urgent` = true — unverified assertion; from Event 003 — SMS from Leah Venn (Tenant): “Said there was no gas smell or visible leak and the boiler display was blank.”
- `access` = false — unverified assertion; from Event 004 — Call from Maya Chen (Property Manager, Northbridge Lettings): “is not authorised to approve work or provide access in her absence”
- `urgent` = true — unverified assertion; from Event 004 — Call from Maya Chen (Property Manager, Northbridge Lettings): “Leah said her adult niece, Erin Vale, sometimes stays overnight but is not authorised to approve work or provide access in her absence.”
- `urgent` = true — unverified assertion; from Event 005 — Email from Maya Chen (Property Manager, Northbridge Lettings): “Sent the reported symptoms and asked for the earliest diagnostic appointment, including whether a same-day visit was available.”
- `total` = 168.0 — unverified assertion; from Event 006 — Email from Daniel Hart (Heating Contractor, Brackenridge Heat Services): “The diagnostic call-out is a fixed £168 including VAT”
- `urgent` = true — unverified assertion; from Event 008 — SMS from Leah Venn (Tenant): “Reported a living-room temperature of 12°C at 10:10.”
- `urgent` = true — unverified assertion; from Event 009 — Call from Maya Chen (Property Manager, Northbridge Lettings): “Reported the heating failure, the tenant's temperature reading and the 17 January appointment offer.”
- `urgent` = true — unverified assertion; from Event 011 — Email from Maya Chen (Property Manager, Northbridge Lettings): “Asked about an earlier slot, a cancellation list and phone triage, and whether the contractor could offer safe temporary-heating advice without a visit.”
- `urgent` = true — unverified assertion; from Event 012 — Email from Daniel Hart (Heating Contractor, Brackenridge Heat Services): “Confirmed no same-day engineer was available. A cancellation slot might arise on 15 January but could not be reserved without a booking.”
- `access` = true — unverified assertion; from Event 013 — SMS from Leah Venn (Tenant): “She can admit a contractor on 15 January if given at least 30 minutes' notice and a direct call.”
- `keys` = false — unverified assertion; from Event 013 — SMS from Leah Venn (Tenant): “No key is held by the agency.”
- `total` = 168.0 — unverified assertion; from Event 014 — Email from Owen Pike (Landlord): “the £168 diagnostic call-out”
- `urgent` = true — unverified assertion; from Event 015 — Call from Maya Chen (Property Manager, Northbridge Lettings): “Discussed possible interim arrangements. Leah said she has no suitable spare heater and is concerned about carrying one because of her mobility impairment.”
- `urgent` = true — unverified assertion; from Event 016 — Email from Maya Chen (Property Manager, Northbridge Lettings): “Escalated the cold-weather report, access requirements, late standard appointment and available £250 urgent-repair authority.”
- `urgent` = true — unverified assertion; from Event 017 — Update from Priya Noll (Duty Manager, Northbridge Lettings): “The duty file records no separate spending limit for temporary equipment, transport or accommodation.”
- `urgent` = true — unverified assertion; from Event 018 — Portal from Leah Venn (Tenant): “Reported the living-room temperature as 10°C at 16:25.”
- `schedule` = false — unverified assertion; from Event 018 — Portal from Leah Venn (Tenant): “No appointment or interim arrangement had been confirmed.”
- `total` = 168.0 — unverified assertion; from Event 019 — Call from Daniel Hart (Heating Contractor, Brackenridge Heat Services): “It would be the same £168 diagnostic call-out; no repair work or parts were included.”

### Reading of each source (Jev route → Claude reading)

**Intake report** — Jev `claude` — Possibly several issues: splitting cases needs Claude.. claude-opus-5: new_request, route `request_quote`, medium confidence.
Tenant Leah Venn reports the radiators are cold and the heating controller is unresponsive at 7 Mallowmere Walk; hot water is still available. She has asked for a repair appointment. *Why:* Newly reported heating defect with no stated hazard or vulnerability; hot water remains available, so it needs a contractor assessment/quote rather than emergency handling.
- Unknown (affects route): Unclear what heating system is installed (boiler type, controller model), whether the boiler is firing and whether any error codes are shown.
- Unknown (affects route): Unclear whether anyone in the household is vulnerable or at particular risk from lack of heating, which would make this urgent.
- Unknown: Only states she was at home this morning; no ongoing availability or preferred appointment slots given.
- Unknown: No explicit permission to enter or access method stated for a contractor visit.

**Event 002 — Update from Maya Chen (Property Manager, Northbridge Lettings)** — Jev `jev_route` → `request_quote` — Jev routes; Claude extracts quotes and claims. Route confidence 0.70 is below the Jev-only bar 0.8.. claude-opus-5: update, route `request_quote`, medium confidence.
Property manager acknowledged the tenant's heating report and asked about the boiler display, any gas smell or leak, and access arrangements. No new facts or decisions provided. *Why:* Agency acknowledgement with outstanding questions; defect still needs contractor assessment, so request_quote per router decision stands.
- Unknown (affects route): Boiler display status, any gas smell or visible leak still unknown - awaiting tenant reply.
- Unknown: Access arrangements not yet agreed; no date or entry method confirmed.

**Event 003 — SMS from Leah Venn (Tenant)** — Jev `jev_route` → `urgent_hazard` — Possible hazard (Jev p=0.63); a person takes over before any automated contact.. claude-opus-5: answer_to_question, route `urgent_hazard`, medium confidence.
Tenant confirms no gas smell or visible leak and a blank boiler display. She has a mobility impairment and asks that any attendee phone from outside rather than arrive unannounced. *Why:* Router flagged possible hazard (no heating, vulnerable person) requiring a case manager; tenant's reply rules out gas smell/leak but blank display and mobility impairment support human handling.
- Unknown: No appointment date or time offered; tenant's availability still unknown.
- Unknown: Tenant asks attendee to call from outside; explicit permission to enter and access method not confirmed.
- Risk flags: vulnerable_person

**Event 004 — Call from Maya Chen (Property Manager, Northbridge Lettings)** — Jev `jev_route` → `urgent_hazard` — Possible hazard (Jev p=0.34); a person takes over before any automated contact.. claude-opus-5: update, route `urgent_hazard`, medium confidence.
Property manager records that the tenant's niece is not authorised to approve work or provide access, and that medical details must not be shared with contractors beyond saying she needs extra time to answer the door. *Why:* Router route retained; message is an access/authority restriction update on the existing no-heating case involving a vulnerable tenant.
- Unknown: Access arrangements with Leah herself (date, time, call-ahead) are still not confirmed.
- Risk flags: vulnerable_person, sensitive_personal_data

**Event 005 — Email from Maya Chen (Property Manager, Northbridge Lettings)** — Jev `jev_route` → `urgent_hazard` — Possible hazard (Jev p=0.50); a person takes over before any automated contact.. claude-opus-5: update, route `urgent_hazard`, medium confidence.
Property manager emailed the heating contractor with the reported symptoms and asked for the earliest diagnostic appointment, including possible same-day attendance. Access must be arranged directly with the tenant. *Why:* Following router: no heating for a tenant with a mobility impairment is treated as potentially urgent and needs a case manager; message itself is an update arranging a diagnostic visit.
- Unknown: No appointment date or time has been agreed yet; contractor response awaited.
- Unknown: Access is to be arranged directly with the tenant; no consent or method recorded for a specific visit.
- Risk flags: vulnerable_person

**Event 006 — Email from Daniel Hart (Heating Contractor, Brackenridge Heat Services)** — Jev `jev_route` → `confirm_appointment` — Jev routes; Claude extracts quotes and claims. confirm_appointment is not a Jev-only route. The message may state facts that need exact quotes. Possible distress, complaint or vulnerability. A route change on an existing case.. claude-opus-5: access_or_appointment, route `confirm_appointment`, high confidence.
Heating contractor Daniel Hart offers a diagnostic appointment slot on 17 January, 10:00–14:00, with a fixed call-out charge of £168 including VAT. Parts or remedial work would be quoted separately. *Why:* Contractor proposing a visit slot for a known job; next step is confirming the appointment with the tenant.
- Unknown: The offered slot is a four-hour window and has not been agreed with the tenant, who needs a call from outside before arrival.
- Unknown: Access must still be arranged directly with the tenant; no consent recorded for 17 January.
- Risk flags: vulnerable_person

**Event 007 — Note from Maya Chen (Property Manager, Northbridge Lettings)** — Jev `jev_route` → `confirm_appointment` — Jev routes; Claude extracts quotes and claims. confirm_appointment is not a Jev-only route. Route confidence 0.72 is below the Jev-only bar 0.8. The message may state facts that need exact quotes.. claude-opus-5: update, route `confirm_appointment`, medium confidence.
Internal note by Maya Chen recording the property authority record: a £250 per urgent repair incident limit inclusive of diagnostic call-out, labour and parts, which Maya may authorise without further landlord consent. Temporary heaters, transport and accommodation are excluded. *Why:* Internal note recording authority limits; the live next step remains confirming the offered diagnostic appointment with the tenant, matching the router decision.
- Unknown: The note records a delegated spend limit but does not itself authorise the £168 diagnostic call-out or confirm the 17 January 10:00–14:00 appointment; staff should confirm whether authority is being exercised.

**Event 008 — SMS from Leah Venn (Tenant)** — Jev `jev_route` → `urgent_hazard` — Possible hazard (Jev p=0.79); a person takes over before any automated contact.. claude-opus-5: update, route `urgent_hazard`, high confidence.
Tenant reports living-room temperature of 12
insufficient heating and a plug-in heater whose casing becomes unusually hot, which she has stopped using. She may stay with her niece tonight if transport can be arranged, but accessibility there is unconfirmed. *Why:* No heating in cold conditions for a tenant with a mobility impairment, plus an overheating plug-in heater; immediate human attention required, consistent with router decision.
- Unknown: Whether the tenant can actually stay with her niece tonight is unconfirmed, including transport and whether that home is accessible.
- Unknown: No confirmation of access or appointment timing for the 17 January slot; earlier/same-day attendance may be needed given no heating.
- Risk flags: safety, vulnerable_person

**Event 009 — Call from Maya Chen (Property Manager, Northbridge Lettings)** — Jev `jev_route` → `urgent_hazard` — Possible hazard (Jev p=0.52); a person takes over before any automated contact.. claude-opus-5: update, route `urgent_hazard`, medium confidence.
Property manager called the landlord to report the heating failure, the tenant's 12°C reading and the contractor's 17 January appointment offer, and asked about a faster diagnostic visit and interim arrangements. No landlord decision is recorded in the message. *Why:* Loss of heating in cold conditions for a tenant with a mobility impairment; router's urgent_hazard route accepted and a person should handle next steps.
- Unknown: Whether an earlier diagnostic visit than 17 January can be obtained is still unresolved.
- Unknown: Landlord's response on interim arrangements (heating/accommodation) is not recorded.
- Risk flags: vulnerable_person, safety

**Event 010 — Email from Owen Pike (Landlord)** — Jev `jev_route` → `clarify` — Jev routes; Claude extracts quotes and claims. clarify is not a Jev-only route. Route confidence 0.59 is below the Jev-only bar 0.8.. claude-opus-5: update, route `clarify`, medium confidence.
Landlord Owen Pike instructs that a quote be obtained before committing to non-emergency expenditure, and notes he is travelling and may be slow to respond. He did not address the 17 January diagnostic appointment or interim arrangements. *Why:* Landlord response leaves the key question of whether the diagnostic visit is emergency expenditure unanswered, so the item cannot be instructed or booked yet; matches router's clarify.
- Unknown (affects route): Landlord has not said whether this heating failure counts as emergency/urgent expenditure, so it is unclear if the £168 diagnostic call-out may proceed under the agency's urgent-repair authority.
- Unknown: Landlord did not respond to the 17 January 10:00-14:00 appointment offer or to interim heating/accommodation arrangements.
- Risk flags: vulnerable_person, safety

**Event 011 — Email from Maya Chen (Property Manager, Northbridge Lettings)** — Jev `jev_route` → `urgent_hazard` — Possible hazard (Jev p=0.54); a person takes over before any automated contact.. claude-opus-5: update, route `urgent_hazard`, medium confidence.
Property manager asked the heating contractor about an earlier appointment slot, a cancellation list, phone triage, and safe temporary-heating advice without a visit. No new appointment or authority confirmed. *Why:* Router flagged a possible hazard: no heating in cold conditions plus an overheating plug-in heater; a case manager should handle before further action.
- Unknown: No earlier appointment has been confirmed; the 17 January 10:00-14:00 slot remains the only offer.
- Unknown: Whether the agency will authorise the £168 diagnostic as urgent repair expenditure is still unresolved.
- Risk flags: safety, vulnerable_person

**Event 012 — Email from Daniel Hart (Heating Contractor, Brackenridge Heat Services)** — Jev `jev_route` → `urgent_hazard` — Possible hazard (Jev p=0.33); a person takes over before any automated contact.. claude-opus-5: update, route `urgent_hazard`, medium confidence.
Contractor confirms no same-day engineer; a 15 January cancellation slot may arise but cannot be held without a booking. They cannot assess or advise remotely and say the plug-in heater Leah described should not be used. *Why:* Router set urgent_hazard; unheated property in January plus an unsafe heater warrant case manager handling before booking.
- Unknown (affects route): Whether to book the 17 January slot to stay eligible for a possible 15 January cancellation; no appointment is confirmed.
- Unknown: Interim heating arrangements for the tenant remain unresolved as the contractor cannot advise remotely.
- Risk flags: safety

**Event 013 — SMS from Leah Venn (Tenant)** — Jev `jev_route` → `confirm_appointment` — Jev routes; Claude extracts quotes and claims. confirm_appointment is not a Jev-only route. The message may state facts that need exact quotes. A route change on an existing case.. claude-opus-5: access_or_appointment, route `confirm_appointment`, high confidence.
Tenant confirms she will not use the suspect heater and can admit a contractor on 15 January with at least 30 minutes' notice and a direct call, but cannot guarantee access on 17 January due to a hospital appointment. She states the agency holds no key. *Why:* Message is about arranging contractor access for the known heating job; conditional availability and key position stated.
- Unknown: No specific time on 15 January is agreed, and the 15 January cancellation slot is not confirmed; 17 January access is uncertain due to a hospital appointment.
- Unknown: Confirm the direct contact number for the 30-minute notice call.
- Risk flags: safety, vulnerable_person

**Event 014 — Email from Owen Pike (Landlord)** — Jev `claude` — Jev route confidence 0.42 is below 0.5.. claude-opus-5: update, route `instruct_work`, medium confidence.
Landlord Owen Pike clarifies that his earlier instruction to obtain a quote applied only to non-emergency spending and that a standing £250 urgent-repair authority remains. He states Maya may authorise the £168 diagnostic call-out without further consent if the incident is treated as urgent, with later work kept within the incident limit or referred for consent. *Why:* Landlord has given conditional spend authority for the diagnostic call-out, so the next step on the known heating job is instructing the contractor to attend rather than seeking a further quote; appointment confirmation remains outstanding.
- Unknown (affects route): The landlord's authority is conditional on the incident being treated as an urgent repair; staff must confirm whether that classification applies before relying on the £168 approval.
- Unknown: It is not stated whether the £168 figure includes VAT, nor what the 'incident limit' covers beyond the £250 standing authority.
- Unknown: The message does not address the possible 15 January cancellation slot or the tenant's access constraints; an appointment still needs confirming.
- Risk flags: safety

**Event 015 — Call from Maya Chen (Property Manager, Northbridge Lettings)** — Jev `jev_route` → `urgent_hazard` — Possible hazard (Jev p=0.69); a person takes over before any automated contact.. claude-opus-5: update, route `urgent_hazard`, medium confidence.
Maya Chen called the tenant about interim heating arrangements. Leah has no suitable spare heater, cannot carry one due to a mobility impairment, and asked whether a heater could be delivered or transport to her niece's home arranged; she still needs to check step-free access there. *Why:* Vulnerable tenant without heating in January and no viable interim heat source; router's urgent_hazard route is appropriate for case manager handling.
- Unknown (affects route): Whether the desk can arrange delivery of a temporary heater or transport to the niece's home, and who authorises that cost.
- Unknown: Step-free access at the niece's address is unconfirmed, so the relocation option cannot yet be relied on.
- Risk flags: vulnerable_person, safety

**Event 016 — Email from Maya Chen (Property Manager, Northbridge Lettings)** — Jev `jev_route` → `urgent_hazard` — Possible hazard (Jev p=0.67); a person takes over before any automated contact.. claude-opus-5: update, route `urgent_hazard`, medium confidence.
Maya Chen has escalated the cold-weather heating failure internally to the duty manager, covering access requirements, the late standard appointment slot and the £250 urgent-repair authority. She asks what cover or separate spending authority applies to temporary heating, transport or accommodation. *Why:* Internal escalation of a no-heating situation affecting a tenant with a mobility impairment in cold weather; a case manager must take it on, consistent with the router's urgent_hazard route.
- Unknown: Whether temporary heating, transport or alternative accommodation costs are covered, and who authorises that spend beyond the £250 urgent-repair authority.
- Unknown: No confirmed appointment date and time for the diagnostic visit; tenant can only admit on 15 January with 30 minutes' notice.
- Risk flags: vulnerable_person, safety

**Event 017 — Update from Priya Noll (Duty Manager, Northbridge Lettings)** — Jev `jev_route` → `urgent_hazard` — Possible hazard (Jev p=0.35); a person takes over before any automated contact.. claude-opus-5: update, route `urgent_hazard`, medium confidence.
Duty Manager confirms the office can contact the landlord again and check approved suppliers for heater delivery, and that the duty file records no separate spending limit for temporary heating, transport or accommodation. *Why:* Internal update on an open heating case with no heat for a tenant with mobility impairment in cold weather; router's urgent_hazard route retained for human handling.
- Unknown: No spending authority exists for temporary heating, transport or accommodation; staff need a decision on who authorises these costs for a vulnerable tenant without heating.
- Unknown: Whether a 15 January cancellation slot can be booked with the 30 minutes' notice and direct call the tenant requires.
- Risk flags: vulnerable_person, safety

**Event 018 — Portal from Leah Venn (Tenant)** — Jev `jev_route` → `urgent_hazard` — Possible hazard (Jev p=0.78); a person takes over before any automated contact.. claude-opus-5: chase, route `urgent_hazard`, high confidence.
Tenant reports the living-room at 10°C at 16:25 with no heating fix, appointment or interim arrangement confirmed, and asks for an update before the office closes. A possible stay at her niece's is unconfirmed pending step-free access. *Why:* Cold-weather no-heating report at 10°C for a tenant with mobility impairment; needs immediate human handling, consistent with router decision.
- Unknown: Whether the niece's spare room is usable tonight depends on step-free entrance, still unconfirmed.
- Unknown: No appointment date/time agreed; tenant previously offered 15 January with 30 minutes' notice.
- Risk flags: safety, vulnerable_person, distress

**Event 019 — Call from Daniel Hart (Heating Contractor, Brackenridge Heat Services)** — Jev `jev_route` → `confirm_appointment` — Jev routes; Claude extracts quotes and claims. confirm_appointment is not a Jev-only route. The message may state facts that need exact quotes. A route change on an existing case.. claude-opus-5: access_or_appointment, route `confirm_appointment`, high confidence.
Contractor Daniel Hart reports a cancellation slot on 15 January 09:00–11:00 available if booked by 17:30, at the same £168 diagnostic call-out with no repair or parts included. The slot is not booked and the tenant's direct access confirmation with call and notice is still needed. *Why:* Message concerns arranging a visit for an already known job; slot not yet booked so no schedule claim.
- Unknown: The slot is offered but not booked; needs booking by 17:30 to hold it.
- Unknown: Tenant's direct confirmation of access, with required call and 30 minutes' notice, is still outstanding.
- Unknown: Whether £168 includes VAT is not stated.
