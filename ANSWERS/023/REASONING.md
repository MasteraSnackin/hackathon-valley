# Reasoning — Property Management case 023

Exported from the system's recorded policy assessments, claims and concise model rationales. It is not reconstructed after the fact and does not contain hidden chain-of-thought.

## System case `fea0d65b5f72` — HUMAN REVIEW

### Why this decision (policy gates)

The model cannot create authority: the policy engine decides from recorded checks. Each blocker below kept the action from running.

- `identity` is **UNKNOWN** → HUMAN REVIEW (rule `require-identity`, owner case manager): Verify the person, property and work item mapping. — evidence: no source recorded
- `route` is **UNKNOWN** → HUMAN REVIEW (rule `require-route`, owner case manager): Verify the recipient and permitted communication route. — evidence: no source recorded
- `triage` is **UNKNOWN** → HUMAN REVIEW (rule `require-triage`, owner case manager): Clarify before routing: This invoice covers the same 5 February service date as invoice NBL-CFM-250210-A (£138.00); it is not stated whether it supersedes that record or is separate chargeable work.; No completion evidence, parts record or attendance proof for the actuator replacement is supplied, and the tenant reports heating still intermittent.; No written landlord authorisation on file for actuator replacement; authority for the £372.00 spend is unconfirmed. A verified route is required before asking externally. — evidence: Attachment invoice-NBL-CFM-250210-B.pdf (PDF text extraction)

### Claims extracted from the sources

Every claim is a source assertion with an exact quote; unverified claims were never used as authority.

- `urgent` = true — unverified assertion; from Intake report: “radiator heating had cut out twice since the previous evening”
- `total` = 180.0 — unverified assertion; from Event 005 — Email from Soren Dallow (Landlord): “Authorized diagnosis up to £180 including VAT only.”
- `total` = 180.0 — unverified assertion; from Event 006 — Email from Ivo Merrick (Property Manager, Northbridge Lettings): “the diagnostic-only authorization ceiling of £180 including VAT”
- `total` = 138.0 — unverified assertion; from Event 007 — Email from Petra Quill (Contractor, Copper Finch Mechanical): “Quoted £138 including VAT for attendance, diagnosis and testing; parts and remedial work were excluded.”
- `schedule` = true — unverified assertion; from Event 007 — Email from Petra Quill (Contractor, Copper Finch Mechanical): “Confirmed attendance for 5 February after 14:00.”
- `total` = 372.0 — unverified assertion; from Event 009 — Email from Petra Quill (Contractor, Copper Finch Mechanical): “Sent an estimate for £372 including VAT for actuator supply and replacement, attendance and heating-system testing.”
- `completion` = false — unverified assertion; from Event 011 — SMS from Tessa Vane (Tenant): “Reported that the radiators were cold again.”
- `completion` = false — unverified assertion; from Event 014 — Portal from Tessa Vane (Tenant): “Said the radiators were still inconsistent”
- `completion` = true — unverified assertion; from Event 017 — Email from Petra Quill (Contractor, Copper Finch Mechanical): “Invoice B describes actuator work as completed and gives a service date of 5 February”
- `total` = 138.0 — unverified assertion; from Event 018 — Document from Petra Quill (Contractor, Copper Finch Mechanical): “The received invoice records list £138 for attendance, diagnosis, actuator inspection and an operational test”
- `total` = 372.0 — unverified assertion; from Event 018 — Document from Petra Quill (Contractor, Copper Finch Mechanical): “£372 for actuator supply/replacement, attendance, diagnosis and heating-system testing”
- `completion` = false — unverified assertion; from Event 019 — Note from Ivo Merrick (Property Manager, Northbridge Lettings): “no return-visit or completion entry”
- `completion` = false — unverified assertion; from Event 020 — Portal from Tessa Vane (Tenant): “Heating was currently working intermittently, with one radiator cooler than the others.”
- `total` = 138.0 — unverified assertion; from Attachment invoice-NBL-CFM-250210-A.pdf (PDF text extraction): “Total including VAT: £138.00”
- `total` = 372.0 — unverified assertion; from Attachment invoice-NBL-CFM-250210-B.pdf (PDF text extraction): “Total including VAT: £372.00”

### Reading of each source (Jev route → Claude reading)

**Intake report** — Jev `jev_route` → `urgent_hazard` — Possible hazard (Jev p=0.58); a person takes over before any automated contact.. claude-opus-5: new_request, route `urgent_hazard`, medium confidence.
Tenant reports the radiator heating has cut out twice since the previous evening, with hot water still working. A child lives at the property and an inspection is requested. *Why:* Intermittent loss of heating with a child in the property; router flagged possible hazard for human handling.
- Unknown (affects route): Is the heating currently off entirely, and is the boiler showing any fault code or pressure loss?
- Unknown: No availability or access arrangements given for an inspection visit.
- Risk flags: vulnerable_person, safety

**Event 002 — Update from Ivo Merrick (Property Manager, Northbridge Lettings)** — Jev `jev_route` → `clarify` — Jev routes; Claude extracts quotes and claims. clarify is not a Jev-only route. Route confidence 0.57 is below the Jev-only bar 0.8. Possible distress, complaint or vulnerability.. claude-opus-5: update, route `clarify`, high confidence.
Property manager acknowledged the tenant's intermittent heating report and asked about leaks, smells, boiler warnings and access times. No access arrangement confirmed yet. *Why:* Manager is still gathering essential details; nothing yet to instruct or quote, so clarify stands.
- Unknown (affects route): Awaiting tenant's answers on leaks, smells and boiler warnings; is heating off entirely or intermittent?
- Unknown: No entry arrangement confirmed; access times still needed.
- Risk flags: vulnerable_person

**Event 003 — Portal from Tessa Vane (Tenant)** — Jev `jev_route` → `confirm_appointment` — Jev routes; Claude extracts quotes and claims. confirm_appointment is not a Jev-only route. Route confidence 0.72 is below the Jev-only bar 0.8. The message may state facts that need exact quotes. Possible distress, complaint or vulnerability. A route change on an existing case.. claude-opus-5: answer_to_question, route `request_quote`, medium confidence.
Tenant replies that there is no visible leak, smell or current warning light, though the boiler briefly showed an unidentified symbol the previous night. She gives general availability after 14:00 on weekdays; no appointment has been agreed. *Why:* Tenant has answered the diagnostic questions; intermittent heating fault still needs an engineer assessment, and no firm appointment exists yet.
- Unknown: Tenant offers after 14:00 on weekdays but no specific date and time is agreed; confirm an appointment slot.
- Unknown: The boiler displayed a brief unidentified symbol; ask tenant to note or photograph any code if it recurs.
- Unknown: Confirm who will admit the engineer and the entry method.
- Objected to Jev's route: confirm_appointment assumes an appointment to arrange or confirm, but the message only gives general weekday availability after 14:00 and no visit has been booked; the job still needs a contractor inspection/quote to be instructed.

**Event 004 — Email from Ivo Merrick (Property Manager, Northbridge Lettings)** — Jev `jev_route` → `request_quote` — Jev routes; Claude extracts quotes and claims. The message may state facts that need exact quotes. Possible distress, complaint or vulnerability.. claude-opus-5: update, route `request_quote`, high confidence.
Property manager emailed the landlord requesting approval for a diagnostic visit on the intermittent radiator heating fault, noting the agency's routine repair limit of £180 including VAT above which landlord approval is needed. *Why:* Agency is seeking landlord approval for a diagnostic visit; no quote or authority yet, so the job remains at the quote/assessment stage.
- Unknown: No diagnostic visit cost or contractor has been stated; the £180 figure is a general agency limit, not a quote for this job.
- Unknown: Tenant offered weekday access after 14:00 but no appointment has been arranged or confirmed with a contractor.

**Event 005 — Email from Soren Dallow (Landlord)** — Jev `jev_route` → `request_quote` — Jev routes; Claude extracts quotes and claims. The message may state facts that need exact quotes.. claude-opus-5: update, route `request_quote`, high confidence.
Landlord Soren Dallow authorises a diagnostic visit up to £180 including VAT and asks to be consulted before any remedial work or further spend. *Why:* Landlord approval for a capped diagnostic visit; the job still needs a contractor quote/assessment, matching the router's request_quote.
- Unknown: No appointment date/time agreed; tenant availability is after 14:00 weekdays only.
- Unknown: No entry arrangement confirmed for the diagnostic visit.

**Event 006 — Email from Ivo Merrick (Property Manager, Northbridge Lettings)** — Jev `jev_route` → `request_quote` — Jev routes; Claude extracts quotes and claims. The message may state facts that need exact quotes.. claude-opus-5: update, route `request_quote`, high confidence.
Property manager instructed contractor Copper Finch Mechanical to diagnose the intermittent radiator heating, provide a written report and itemised estimate before any work beyond diagnosis, noting access after 14:00 and a diagnostic-only authorisation ceiling of £180 including VAT. *Why:* Diagnostic and itemised estimate requested from contractor before any remedial work; quote stage ongoing.
- Unknown: "After 14:00" is general availability; no specific visit date and time is agreed with the contractor.
- Unknown: Confirm the tenant has agreed entry for this specific visit and the access method.

**Event 007 — Email from Petra Quill (Contractor, Copper Finch Mechanical)** — Jev `jev_route` → `confirm_appointment` — Jev routes; Claude extracts quotes and claims. confirm_appointment is not a Jev-only route. Route confidence 0.69 is below the Jev-only bar 0.8. The message may state facts that need exact quotes. A route change on an existing case.. claude-opus-5: access_or_appointment, route `confirm_appointment`, high confidence.
Contractor Petra Quill confirms attendance on 5 February after 14:00 for the diagnostic visit and quotes £138 including VAT for attendance, diagnosis and testing, excluding parts and remedial work. *Why:* Contractor arranging a visit for an already known job and stating the diagnostic price; appointment confirmation is the next step.
- Unknown: No precise arrival time is given, only 'after 14:00' on 5 February; confirm a time window with the tenant.
- Unknown: Tenant has not confirmed consent/access for this specific date.

**Event 008 — Update from Petra Quill (Contractor, Copper Finch Mechanical)** — Jev `claude` — Jev route confidence 0.29 is below 0.5.. claude-opus-5: update, route `request_quote`, medium confidence.
Contractor Petra Quill reports attending the property and diagnosing an intermittent fault at the heating valve actuator; heating worked during the visit and no leak or gas-safety concern was seen. No remedial work or itemised estimate has been provided yet. *Why:* Diagnosis has been carried out but no remedial scope or price is stated; the next step is obtaining an itemised quote before landlord approval of any repair.
- Unknown (affects route): No written report or itemised estimate for remedial work on the valve actuator has been supplied, so the cost and scope of the repair are unknown.
- Unknown: Unclear whether the diagnostic visit is regarded as complete and what the final diagnostic charge was against the £180 including VAT ceiling.
- Unknown: No follow-up visit date has been proposed for any remedial work.

**Event 009 — Email from Petra Quill (Contractor, Copper Finch Mechanical)** — Jev `claude` — Jev route confidence 0.33 is below 0.5.. claude-opus-5: update, route `instruct_work`, medium confidence.
Contractor Petra Quill has submitted an estimate of £372 including VAT to supply and replace the heating valve actuator, including attendance and system testing, and asks for written authorisation before proceeding. It is unclear whether the £138 diagnostic charge is credited against this figure. *Why:* The job has been diagnosed and a written estimate supplied; the next step is a decision on instructing the contractor, though landlord authority above £180 must first be obtained.
- Unknown: The estimate does not state whether the £138 diagnostic charge is credited against the £372, so the full comparable commitment is unclear.
- Unknown (affects route): £372 exceeds the agency's £180 routine repair limit and the landlord's diagnostic-only authorisation; landlord approval is needed before instructing.
- Unknown: No appointment date or time proposed for the remedial visit.

**Event 010 — Email from Ivo Merrick (Property Manager, Northbridge Lettings)** — Jev `jev_route` → `instruct_work` — Jev routes; Claude extracts quotes and claims. instruct_work is not a Jev-only route. Route confidence 0.79 is below the Jev-only bar 0.8.. claude-opus-5: update, route `instruct_work`, medium confidence.
The property manager forwarded the contractor's £372 estimate to the landlord and asked whether the remedial work is authorised, noting it exceeds the routine repair limit and that the contractor must have written authorisation first. *Why:* Router chose instruct_work for the known job; message is an authorisation request to the landlord and the next step is instructing once approval arrives.
- Unknown (affects route): Landlord approval for the £372 remedial estimate has not yet been given; work cannot be instructed until written authorisation is received.
- Objected to Jev's route: No authority has yet been given for the £372 estimate, so the item cannot be instructed; it is awaiting landlord approval.

**Event 011 — SMS from Tessa Vane (Tenant)** — Jev `jev_route` → `instruct_work` — Jev routes; Claude extracts quotes and claims. instruct_work is not a Jev-only route. Route confidence 0.63 is below the Jev-only bar 0.8.. claude-opus-5: update, route `instruct_work`, medium confidence.
Tenant reports radiators cold again and is using a portable heater plugged directly into a wall socket. No smell, leak or warning reported; landlord authorisation for the £372 remedial estimate is still outstanding. *Why:* Fault recurring after diagnosis; next step is the remedial actuator work, but landlord authorisation remains outstanding. No explicit hazard reported.
- Unknown (affects route): Whether the tenant or household includes anyone vulnerable, and how long the heating has been off, to judge urgency.
- Unknown (affects route): Landlord written authorisation for the £372 actuator replacement is still outstanding, so work cannot be instructed yet.
- Risk flags: safety

**Event 012 — Email from Soren Dallow (Landlord)** — Jev `jev_route` → `clarify` — Jev routes; Claude extracts quotes and claims. clarify is not a Jev-only route. Route confidence 0.64 is below the Jev-only bar 0.8. A route change on an existing case.. claude-opus-5: answer_to_question, route `clarify`, high confidence.
Landlord Soren Dallow has not decided on the £372 actuator estimate and asks whether the actuator could be repaired instead and whether the price covers all parts, labour and testing. He explicitly did not authorise remedial work or further expenditure. *Why:* Authorisation withheld pending answers on repair option and price scope, so the item cannot be instructed and needs clarification.
- Unknown (affects route): Landlord asks whether a repair of the actuator is possible instead of replacement; contractor needs to confirm.
- Unknown: Whether the £372 including VAT covers all parts, labour and testing, and whether the £138 diagnostic charge is credited.
- Unknown (affects route): Tenant reports radiators cold again and is using a portable heater; vulnerability and duration without heating still unknown.

**Event 013 — Portal from Ivo Merrick (Property Manager, Northbridge Lettings)** — Jev `jev_route` → `clarify` — Jev routes; Claude extracts quotes and claims. clarify is not a Jev-only route. Route confidence 0.76 is below the Jev-only bar 0.8.. claude-opus-5: update, route `clarify`, high confidence.
Property manager asked the tenant whether heating or safety symptoms had changed, whether equipment-label details were available, and whether access could be given for a possible return visit. No new facts or decisions are asserted. *Why:* Outbound clarification request to the tenant; no new facts, so the item stays at clarify pending reply.
- Unknown (affects route): Awaiting tenant's reply on whether heating or safety symptoms have changed and whether equipment-label details are available.
- Unknown: Tenant has not yet confirmed whether the contractor can be given access for a return visit.

**Event 014 — Portal from Tessa Vane (Tenant)** — Jev `jev_route` → `clarify` — Jev routes; Claude extracts quotes and claims. clarify is not a Jev-only route. Route confidence 0.53 is below the Jev-only bar 0.8.. claude-opus-5: answer_to_question, route `clarify`, medium confidence.
Tenant reports radiators still inconsistent with hot water still available, and supplies the boiler-label details. No return appointment has been agreed. *Why:* Tenant reply provides label details but the heating fault persists and authorisation/appointment remain unresolved; router chose clarify.
- Unknown: No return appointment agreed; tenant's availability for a contractor revisit is unknown.
- Unknown: Tenant has not stated whether the contractor may be given access for a return visit.

**Event 015 — Email from Ivo Merrick (Property Manager, Northbridge Lettings)** — Jev `jev_route` → `clarify` — Jev routes; Claude extracts quotes and claims. clarify is not a Jev-only route.. claude-opus-5: update, route `clarify`, high confidence.
Property manager asked the contractor for a repair alternative, parts availability, an estimate breakdown and whether the diagnostic charge would be credited, and repeated that no further work is authorised. *Why:* Outstanding information is needed from the contractor before the quote can be decided; no authority given.
- Unknown: Awaiting contractor's response on repair option, parts availability, cost breakdown and whether the £138 diagnostic charge is credited.

**Event 016 — Email from Petra Quill (Contractor, Copper Finch Mechanical)** — Jev `jev_route` → `clarify` — Jev routes; Claude extracts quotes and claims. clarify is not a Jev-only route.. claude-opus-5: update, route `clarify`, high confidence.
Contractor replied that parts availability and estimate details still need checking; no repair option, credit, return visit or completion confirmed. *Why:* Contractor response leaves the key estimate and repair questions unresolved, so the item cannot progress to instruction or quote approval yet.
- Unknown (affects route): Contractor has not confirmed whether a repair alternative to replacement is possible, parts availability, or an itemised estimate breakdown including whether diagnosis is credited.
- Unknown: No return visit date proposed by the contractor.

**Event 017 — Email from Petra Quill (Contractor, Copper Finch Mechanical)** — Jev `jev_route` → `clarify` — Jev routes; Claude extracts quotes and claims. clarify is not a Jev-only route. The message may state facts that need exact quotes.. claude-opus-5: update, route `clarify`, medium confidence.
Contractor sent two invoice records dated 10 February without stating whether one supersedes the other, whether both are payable, or whether either is paid. Invoice B claims actuator work completed on 5 February but no signed completion record was provided and it conflicts with the later estimate and 7 February parts check. *Why:* Conflicting invoice and completion claims with no evidence or amounts; cannot act until contractor clarifies.
- Unknown (affects route): Invoice B claims actuator work completed on 5 February but no signed completion record and it conflicts with the estimate sent later that day and the 7 February parts check.
- Unknown (affects route): Two invoices dated 10 February: unclear whether one replaces the other, whether both amounts are payable, or whether either has been paid. No totals stated.

**Event 018 — Document from Petra Quill (Contractor, Copper Finch Mechanical)** — Jev `jev_route` → `clarify` — Jev routes; Claude extracts quotes and claims. clarify is not a Jev-only route. The message may state facts that need exact quotes.. claude-opus-5: update, route `clarify`, high confidence.
Contractor document lists two invoice records for 5 February service: £138 for attendance/diagnosis/inspection/test and £372 for actuator supply/replacement plus overlapping activities. Neither record states whether one supersedes or credits the other, so the payable total remains unclear. *Why:* Invoice amounts stated but payability, duplication and VAT status unclear, and completion evidence still conflicts; clarification needed before any authority or closure.
- Unknown (affects route): Whether the two invoice records are cumulative or one supersedes the other; the overlapping activities suggest possible duplication, and no payable total including tax is stated.
- Unknown (affects route): Both records cite 5 February as the service date, but actuator replacement conflicts with the estimate sent later that day and the 7 February parts check; no signed completion record supplied.

**Event 019 — Note from Ivo Merrick (Property Manager, Northbridge Lettings)** — Jev `jev_route` → `clarify` — Jev routes; Claude extracts quotes and claims. clarify is not a Jev-only route. The message may state facts that need exact quotes.. claude-opus-5: update, route `clarify`, high confidence.
Internal file note from the property manager recording that landlord authority covers diagnosis only, that the £372 estimate post-dates the stated service date, and that the file holds no written authorisation for actuator replacement and no completion or return-visit entry. *Why:* Internal note disputing authority and completion evidence; billing and completion facts unresolved, so clarification is needed before any instruction or payment.
- Unknown (affects route): Whether the two invoice records are cumulative or one supersedes the other; no payable total including tax is stated.
- Unknown (affects route): Whether actuator replacement was ever carried out, given the £372 estimate was sent after the stated service date and no completion record exists.

**Event 020 — Portal from Tessa Vane (Tenant)** — Jev `jev_route` → `clarify` — Jev routes; Claude extracts quotes and claims. clarify is not a Jev-only route. Route confidence 0.58 is below the Jev-only bar 0.8. The message may state facts that need exact quotes.. claude-opus-5: answer_to_question, route `clarify`, medium confidence.
Tenant confirms she recalls the 5 February visit but cannot say whether the actuator was replaced, and has seen no contractor since. Heating still works only intermittently with one radiator cooler than the rest. *Why:* Completion of the invoiced actuator work remains unverified and the fault persists; clarification needed before authorising or paying.
- Unknown (affects route): Tenant cannot confirm whether actuator replacement was carried out; no return visit observed since 5 February.
- Unknown: Which radiator is cooler and whether hot water remains unaffected.

**Event 021 — Email from Ivo Merrick (Property Manager, Northbridge Lettings)** — Jev `jev_route` → `clarify` — Jev routes; Claude extracts quotes and claims. clarify is not a Jev-only route. Route confidence 0.66 is below the Jev-only bar 0.8.. claude-opus-5: update, route `clarify`, high confidence.
Ivo Merrick asked the contractor to confirm what work was actually completed and when, whether both invoice records remain current or one supersedes the other, how overlapping charges are treated, and requested job notes, parts records and authorisation or attendance evidence for the actuator work. *Why:* Agent is chasing missing completion, billing and authorisation evidence; item cannot progress until the contractor answers.
- Unknown (affects route): What actuator work was actually done and on what date remains unconfirmed; no job notes, parts record or attendance evidence received.
- Unknown: Whether both invoice records are payable or one supersedes the other, and how overlapping charges are handled, is unresolved.

**Event 022 — Email from Petra Quill (Contractor, Copper Finch Mechanical)** — Jev `jev_route` → `clarify` — Jev routes; Claude extracts quotes and claims. clarify is not a Jev-only route.. claude-opus-5: update, route `clarify`, high confidence.
Contractor replied that she is still checking records and cannot yet confirm whether the two invoice entries are separate chargeable work or whether one supersedes the other. No completion evidence, revised invoice or parts confirmation supplied. *Why:* Contractor has not answered the outstanding questions; essential billing and completion information still missing, so the item stays at clarify.
- Unknown: Whether the two invoice records are both payable or one supersedes the other is still unconfirmed.
- Unknown (affects route): What actuator work was done and on what date remains unevidenced; no job notes, parts record or attendance evidence supplied.

**Event 023 — Email from Ivo Merrick (Property Manager, Northbridge Lettings)** — Jev `jev_route` → `clarify` — Jev routes; Claude extracts quotes and claims. clarify is not a Jev-only route. Route confidence 0.79 is below the Jev-only bar 0.8.. claude-opus-5: update, route `clarify`, high confidence.
Property manager updates the landlord that two unreconciled invoice records remain on file with no payment, supersession or authority for actuator work, and the tenant still reports intermittent heating. He asks the landlord how to proceed and whether further work or expenditure is authorised. *Why:* Internal/landlord-facing update seeking instructions; invoice reconciliation and authority unresolved, so clarify matches the router decision.
- Unknown (affects route): Whether actuator replacement was actually carried out, on what date, and which invoice record (if either) is payable remains unevidenced.
- Unknown (affects route): No completion evidence or authorisation for actuator work on file; landlord's decision on further work/expenditure is pending.

**Attachment invoice-NBL-CFM-250210-A.pdf (PDF text extraction)** — Jev `jev_route` → `clarify` — Jev routes; Claude extracts quotes and claims. clarify is not a Jev-only route. Route confidence 0.63 is below the Jev-only bar 0.8. The message may state facts that need exact quotes.. claude-opus-5: update, route `clarify`, medium confidence.
Invoice document NBL-CFM-250210-A from Copper Finch Mechanical for £138.00 including VAT, covering attendance, diagnosis, actuator inspection and operational test on 5 February 2025 at the case property. It does not state whether it supersedes or is superseded by the £372 record. *Why:* Billing document adds the £138 total but leaves supersession, authorisation and completion unevidenced; clarification still required.
- Unknown (affects route): The invoice does not state whether it replaces or is replaced by the £372 record, so which record is payable remains unresolved.
- Unknown (affects route): No statement that actuator replacement was carried out; invoice covers inspection and test only.

**Attachment invoice-NBL-CFM-250210-B.pdf (PDF text extraction)** — Jev `jev_route` → `clarify` — Jev routes; Claude extracts quotes and claims. clarify is not a Jev-only route. Route confidence 0.79 is below the Jev-only bar 0.8. The message may state facts that need exact quotes.. claude-opus-5: update, route `clarify`, medium confidence.
Second Copper Finch Mechanical invoice (NBL-CFM-250210-B) for the same 5 February service date, totalling £372.00 including VAT, covering actuator supply and replacement plus diagnosis and testing. It does not state whether it supersedes the £138.00 invoice, and no authorisation or completion evidence is provided. *Why:* Billing document raising unresolved duplicate-invoice, authority and completion questions; cannot be actioned until the record position is clarified.
- Unknown (affects route): This invoice covers the same 5 February service date as invoice NBL-CFM-250210-A (£138.00); it is not stated whether it supersedes that record or is separate chargeable work.
- Unknown (affects route): No completion evidence, parts record or attendance proof for the actuator replacement is supplied, and the tenant reports heating still intermittent.
- Unknown (affects route): No written landlord authorisation on file for actuator replacement; authority for the £372.00 spend is unconfirmed.
