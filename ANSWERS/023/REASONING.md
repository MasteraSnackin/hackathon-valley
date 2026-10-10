# Reasoning — Property Management case 023

Exported from the system's recorded policy assessments, claims and concise model rationales. It is not reconstructed after the fact and does not contain hidden chain-of-thought.

## System case `905bdba959da` — WAIT

### Why this decision (policy gates)

The model cannot create authority: the policy engine decides from recorded checks. Each blocker below kept the action from running.

- `triage` is **UNKNOWN** → WAIT (rule `require-triage`, owner case manager): Clarify before routing: Whether invoice B (£372.00) supersedes or sits alongside invoice A (£138.00) for the same 5 February service date; overlapping attendance and diagnosis charges are unresolved.; No parts record, attendance evidence or confirmation that the actuator replacement was actually carried out or that the heating fault is resolved.; No written landlord authorisation on file for actuator replacement; authority covered diagnosis only. — evidence: Attachment invoice-NBL-CFM-250210-B.pdf (PDF text extraction)

### Claims extracted from the sources

Every claim is a source assertion with an exact quote; unverified claims were never used as authority.

- `urgent` = true — unverified assertion; from Intake report: “Reported that radiator heating had cut out twice since the previous evening while hot water remained available.”
- `total` = 180.0 — unverified assertion; from Event 005 — Email from Soren Dallow (Landlord): “Authorized diagnosis up to £180 including VAT only.”
- `total` = 180.0 — unverified assertion; from Event 006 — Email from Ivo Merrick (Property Manager, Northbridge Lettings): “the diagnostic-only authorization ceiling of £180 including VAT”
- `schedule` = true — unverified assertion; from Event 007 — Email from Petra Quill (Contractor, Copper Finch Mechanical): “Confirmed attendance for 5 February after 14:00.”
- `total` = 138.0 — unverified assertion; from Event 007 — Email from Petra Quill (Contractor, Copper Finch Mechanical): “Quoted £138 including VAT for attendance, diagnosis and testing; parts and remedial work were excluded.”
- `total` = 372.0 — unverified assertion; from Event 009 — Email from Petra Quill (Contractor, Copper Finch Mechanical): “Sent an estimate for £372 including VAT for actuator supply and replacement, attendance and heating-system testing.”
- `completion` = false — unverified assertion; from Event 011 — SMS from Tessa Vane (Tenant): “Reported that the radiators were cold again.”
- `completion` = true — unverified assertion; from Event 017 — Email from Petra Quill (Contractor, Copper Finch Mechanical): “Invoice B describes actuator work as completed and gives a service date of 5 February”
- `total` = 138.0 — unverified assertion; from Event 018 — Document from Petra Quill (Contractor, Copper Finch Mechanical): “The received invoice records list £138 for attendance, diagnosis, actuator inspection and an operational test”
- `total` = 372.0 — unverified assertion; from Event 018 — Document from Petra Quill (Contractor, Copper Finch Mechanical): “£372 for actuator supply/replacement, attendance, diagnosis and heating-system testing”
- `completion` = false — unverified assertion; from Event 019 — Note from Ivo Merrick (Property Manager, Northbridge Lettings): “no return-visit or completion entry”
- `total` = 138.0 — unverified assertion; from Attachment invoice-NBL-CFM-250210-A.pdf (PDF text extraction): “Total including VAT: £138.00”
- `total` = 372.0 — unverified assertion; from Attachment invoice-NBL-CFM-250210-B.pdf (PDF text extraction): “Total including VAT: £372.00”

### Reading of each source (Jev route → Claude reading)

**Intake report** — Jev `jev_route` → `urgent_hazard` — Possible hazard (Jev p=0.60); a person takes over before any automated contact.. claude-opus-5: new_request, route `urgent_hazard`, medium confidence.
Tenant Tessa Vane reports the radiator heating has cut out twice since the previous evening, with hot water still working. A child lives at the property and she has asked for an inspection. *Why:* Loss of heating with a child at the property is treated as a possible urgent situation needing a case manager, per router decision.
- Unknown (affects route): Is the heating currently off, and what boiler/system type and any fault codes? Need to know whether this is a total heating loss.
- Unknown: No availability or preferred times given for an inspection visit.
- Unknown: No explicit consent or access arrangement for entry stated.
- Risk flags: vulnerable_person

**Event 002 — Update from Ivo Merrick (Property Manager, Northbridge Lettings)** — Jev `jev_route` → `clarify` — Jev routes; Claude extracts quotes and claims. clarify is not a Jev-only route. Route confidence 0.54 is below the Jev-only bar 0.8. Possible distress, complaint or vulnerability.. claude-opus-5: update, route `clarify`, high confidence.
Property manager acknowledged the tenant's intermittent heating report and asked about leaks, smells, boiler warnings and access times. No access arrangement confirmed yet. *Why:* Holding update requesting missing diagnostic and access information; no new facts or consent given, so clarify stands.
- Unknown (affects route): Awaiting tenant's answers on leaks, smells and boiler warning codes; whether heating is currently off is still unknown.
- Unknown: No entry arrangement confirmed; access times still to be provided.

**Event 003 — Portal from Tessa Vane (Tenant)** — Jev `claude` — Jev route confidence 0.36 is below 0.5.. claude-opus-5: answer_to_question, route `request_quote`, medium confidence.
Tenant replies to the property manager's questions: no visible leak, no unusual smell and no current warning light, though the boiler briefly showed an unidentified symbol the previous night. She states she can provide access after 14:00 on weekdays. *Why:* Tenant has answered the safety-screening questions with no hazard indicators, so the reported intermittent heating fault can move on to contractor assessment/quote; the unidentified boiler symbol and current heating status remain open but do not block an inspection.
- Unknown (affects route): The boiler displayed a brief symbol the previous night that the tenant could not identify; the specific fault/warning code is still unknown, as is whether the heating is currently working.
- Unknown: Tenant gives general availability (after 14:00 on weekdays) but no specific appointment date and time is agreed.
- Unknown: It is unclear whether the tenant will be present to let a contractor in or is granting permission to enter by other means.

**Event 004 — Email from Ivo Merrick (Property Manager, Northbridge Lettings)** — Jev `jev_route` → `request_quote` — Jev routes; Claude extracts quotes and claims. The message may state facts that need exact quotes. Possible distress, complaint or vulnerability. Open tenant questions may be answered.. claude-opus-5: update, route `request_quote`, medium confidence.
Property manager emailed the landlord seeking approval for a diagnostic visit on the intermittent heating fault, noting the agency's routine repair limit of £180 including VAT above which landlord approval is needed. *Why:* Internal agency request for landlord approval of a diagnostic visit; the job still needs assessment/quote before instruction.
- Unknown: No response yet on whether radiators are currently heating or what boiler code was shown; landlord approval for the diagnostic visit is still outstanding.

**Event 005 — Email from Soren Dallow (Landlord)** — Jev `jev_route` → `request_quote` — Jev routes; Claude extracts quotes and claims. The message may state facts that need exact quotes.. claude-opus-5: update, route `request_quote`, high confidence.
Landlord authorises a diagnostic visit up to £180 including VAT and asks to be consulted before any remedial work or further spend. *Why:* Landlord approval limited to diagnosis; contractor assessment/quote is still the next step.
- Unknown: No appointment date/time agreed; tenant only gave general availability after 14:00 weekdays.
- Unknown: No explicit entry consent or access method confirmed for the diagnostic visit.

**Event 006 — Email from Ivo Merrick (Property Manager, Northbridge Lettings)** — Jev `jev_route` → `request_quote` — Jev routes; Claude extracts quotes and claims. Route confidence 0.79 is below the Jev-only bar 0.8. The message may state facts that need exact quotes.. claude-opus-5: update, route `request_quote`, high confidence.
Property manager instructed the contractor to carry out a diagnostic visit for the intermittent radiator heating, requesting a written report and itemised estimate before any further work. Access after 14:00 and a diagnostic-only spend ceiling of £180 including VAT were confirmed. *Why:* Diagnostic and itemised estimate requested from contractor before any remedial work; quote stage.
- Unknown: No specific appointment date and time agreed; only "after 14:00" is stated.
- Unknown: Access method unclear — whether the tenant will be present or keys are needed.

**Event 007 — Email from Petra Quill (Contractor, Copper Finch Mechanical)** — Jev `jev_route` → `confirm_appointment` — Jev routes; Claude extracts quotes and claims. confirm_appointment is not a Jev-only route. Route confidence 0.62 is below the Jev-only bar 0.8. The message may state facts that need exact quotes. A route change on an existing case.. claude-opus-5: access_or_appointment, route `confirm_appointment`, high confidence.
Contractor Copper Finch Mechanical confirms attendance on 5 February after 14:00 and quotes £138 including VAT for attendance, diagnosis and testing, excluding parts and remedial work. *Why:* Message arranges a visit for a known job and states the diagnostic price; appointment confirmation is the next step.
- Unknown: No precise arrival time given, only 'after 14:00' on 5 February.
- Unknown: Tenant has not confirmed entry consent for this specific date.

**Event 008 — Update from Petra Quill (Contractor, Copper Finch Mechanical)** — Jev `jev_route` → `confirm_appointment` — Jev routes; Claude extracts quotes and claims. confirm_appointment is not a Jev-only route. Route confidence 0.57 is below the Jev-only bar 0.8. The message may state facts that need exact quotes. Open tenant questions may be answered.. claude-opus-5: update, route `request_quote`, medium confidence.
Contractor Petra Quill reports attending the property and diagnosing an intermittent fault at the heating valve actuator; heating operated during the visit, no leak or gas-safety concern observed. No remedial work carried out or quoted in this update. *Why:* Diagnosis attended but no remedial estimate yet; next step is obtaining a quote for the actuator fault rather than arranging another appointment.
- Unknown (affects route): No itemised estimate or written report for the remedial valve actuator work has been provided; needed before instructing work (landlord consultation required above diagnosis).
- Unknown: Unclear whether the diagnostic visit is considered complete and whether the £138 diagnostic charge is now invoiced.
- Objected to Jev's route: The visit has already taken place, so confirm_appointment is no longer the live step; the message reports a diagnosis without an estimate, so a quote for the remedial work is needed next.

**Event 009 — Email from Petra Quill (Contractor, Copper Finch Mechanical)** — Jev `claude` — Jev route confidence 0.39 is below 0.5.. claude-opus-5: update, route `instruct_work`, medium confidence.
Contractor Petra Quill has submitted an estimate of £372 including VAT to supply and replace the heating valve actuator, including attendance and system testing, and asks for written authorisation before proceeding. It is unclear whether the £138 diagnostic charge is credited against this figure. *Why:* The job has been diagnosed and a remedial estimate is now on the table; the next step is authorisation and instruction of the contractor, subject to landlord approval as the figure exceeds the £180 limit.
- Unknown: The estimate does not state whether the £138 diagnostic charge is credited against the £372, so the full comparable commitment is unclear.
- Unknown: No written diagnostic report or itemised breakdown of the £372 estimate has been confirmed as supplied; the estimate exceeds the £180 routine limit so landlord approval is required before instructing.

**Event 010 — Email from Ivo Merrick (Property Manager, Northbridge Lettings)** — Jev `jev_route` → `instruct_work` — Jev routes; Claude extracts quotes and claims. instruct_work is not a Jev-only route. Route confidence 0.76 is below the Jev-only bar 0.8. Open tenant questions may be answered.. claude-opus-5: update, route `instruct_work`, medium confidence.
The property manager forwarded the contractor's £372 inc VAT estimate to the landlord and asked whether the remedial work is authorised, noting it exceeds the agency's routine repair limit and that the contractor was told to get written authorisation first. No landlord decision yet. *Why:* Router set instruct_work; the message is the authorisation step for the already-quoted remedial job, though approval is still pending.
- Unknown (affects route): Landlord authorisation for the £372 inc VAT remedial estimate has been requested but not yet given; work cannot be instructed until a decision is received.
- Unknown: Unclear whether the £138 diagnostic charge will be credited against the remedial estimate.

**Event 011 — SMS from Tessa Vane (Tenant)** — Jev `claude` — Jev route confidence 0.47 is below 0.5.. claude-opus-5: update, route `instruct_work`, medium confidence.
Tenant reports the radiators are cold again after the 5 February diagnostic visit, and is using one portable heater plugged directly into a wall socket. No new smell, leak or warning reported. *Why:* Known job: tenant confirms the fault recurred after diagnosis, supporting the pending remedial work. Route retained as instruct_work, but landlord authorisation for the £372 estimate remains outstanding. No explicit hazard reported (no smell, leak or warning; heater plugged directly into a wall socket).
- Unknown (affects route): Landlord authorisation for the £372 inc VAT remedial estimate is still outstanding; work cannot be instructed until a decision is received.
- Unknown (affects route): Check whether the tenant is without heating and whether anyone in the household is vulnerable, given reliance on a single portable heater in February.

**Event 012 — Email from Soren Dallow (Landlord)** — Jev `jev_route` → `clarify` — Jev routes; Claude extracts quotes and claims. clarify is not a Jev-only route. Open tenant questions may be answered. A route change on an existing case.. claude-opus-5: answer_to_question, route `clarify`, high confidence.
Landlord has not yet decided on the £372 inc VAT remedial estimate and asks whether the actuator could be repaired instead and whether the price covers all parts, labour and testing. No authorisation given. *Why:* Landlord withheld authorisation and raised questions about scope and price, so the item cannot be instructed; clarification required.
- Unknown (affects route): Landlord asks whether the actuator can be repaired rather than replaced and whether £372 inc VAT covers all parts, labour and testing; contractor response needed before a decision.
- Unknown (affects route): Tenant reported cold radiators again and is relying on a single portable heater in February; check whether anyone in the household is vulnerable.

**Event 013 — Portal from Ivo Merrick (Property Manager, Northbridge Lettings)** — Jev `jev_route` → `clarify` — Jev routes; Claude extracts quotes and claims. clarify is not a Jev-only route. Route confidence 0.78 is below the Jev-only bar 0.8. Open tenant questions may be answered.. claude-opus-5: update, route `clarify`, high confidence.
Property manager asked the tenant whether heating or safety symptoms had changed, whether equipment-label details were available, and whether access could be given for a possible return visit. No new facts or decisions are provided. *Why:* Outbound clarification request from the property manager; no new information or authority, so the item remains awaiting clarification.
- Unknown (affects route): Awaiting tenant's reply on whether heating or safety symptoms have changed and whether equipment-label details are available.
- Unknown: Tenant has not yet confirmed whether the contractor can be given access for a return visit.

**Event 014 — Portal from Tessa Vane (Tenant)** — Jev `jev_route` → `clarify` — Jev routes; Claude extracts quotes and claims. clarify is not a Jev-only route. Route confidence 0.56 is below the Jev-only bar 0.8. Open tenant questions may be answered.. claude-opus-5: answer_to_question, route `clarify`, medium confidence.
Tenant reports radiators still inconsistent with hot water unaffected, and supplies boiler-label details. No return appointment has been agreed. *Why:* Tenant partially answers symptom and label questions, but contractor repair/price clarification and landlord authority remain outstanding, so clarify stands.
- Unknown (affects route): Contractor still to confirm whether the actuator can be repaired rather than replaced and whether £372 inc VAT covers all parts, labour and testing; landlord authority outstanding.
- Unknown: No return appointment agreed; tenant availability and access arrangements still needed.
- Unknown (affects route): Unclear whether anyone in the household is vulnerable while relying on a portable heater in February.

**Event 015 — Email from Ivo Merrick (Property Manager, Northbridge Lettings)** — Jev `jev_route` → `clarify` — Jev routes; Claude extracts quotes and claims. clarify is not a Jev-only route. Open tenant questions may be answered.. claude-opus-5: update, route `clarify`, high confidence.
Property manager emailed the contractor asking for a repair alternative, parts availability, an estimate breakdown and whether the diagnostic charge would be credited, repeating that no further work is authorised. *Why:* Outbound chase to contractor; key pricing/repair questions and vulnerability check remain unresolved, so the item stays in clarify.
- Unknown (affects route): Contractor has not yet answered whether the actuator can be repaired, whether £372 inc VAT covers all parts, labour and testing, or whether the £138 diagnostic fee is credited.
- Unknown (affects route): Still unknown whether anyone in the household is vulnerable while relying on a portable heater in February.

**Event 016 — Email from Petra Quill (Contractor, Copper Finch Mechanical)** — Jev `jev_route` → `clarify` — Jev routes; Claude extracts quotes and claims. clarify is not a Jev-only route. Open tenant questions may be answered.. claude-opus-5: update, route `clarify`, high confidence.
Contractor replied that parts availability and estimate details still need checking; no repair option, credit, return visit or completion confirmed. *Why:* Contractor gave no substantive answers; essential estimate details remain outstanding.
- Unknown (affects route): Contractor still has not confirmed whether the actuator can be repaired, what the estimate covers, or whether the diagnostic fee is credited.
- Unknown (affects route): Unknown whether anyone in the household is vulnerable while relying on a portable heater in February.

**Event 017 — Email from Petra Quill (Contractor, Copper Finch Mechanical)** — Jev `jev_route` → `clarify` — Jev routes; Claude extracts quotes and claims. clarify is not a Jev-only route. The message may state facts that need exact quotes. Open tenant questions may be answered.. claude-opus-5: update, route `clarify`, high confidence.
Contractor sent two invoice records dated 10 February without saying whether one supersedes the other, whether both are payable, or whether either is paid. Invoice B claims actuator work completed on 5 February, but no signed completion record and it conflicts with the later estimate and 7 February parts check. *Why:* Conflicting and unverified invoice/completion information; cannot route to close or instruct until contractor clarifies.
- Unknown (affects route): Invoice B claims actuator work completed on 5 February but no signed completion record and it conflicts with the later estimate and parts check.
- Unknown (affects route): Two invoices dated 10 February: unclear whether one replaces the other, whether both are payable, or whether either has been paid; no comparable total including VAT established.
- Unknown (affects route): Contractor still has not said whether the actuator can be repaired rather than replaced, or what the estimate covers.

**Event 018 — Document from Petra Quill (Contractor, Copper Finch Mechanical)** — Jev `jev_route` → `clarify` — Jev routes; Claude extracts quotes and claims. clarify is not a Jev-only route. The message may state facts that need exact quotes. Open tenant questions may be answered.. claude-opus-5: update, route `clarify`, high confidence.
Contractor document itemises two invoice records (£138 and £372) both dated 5 February for service, with overlapping descriptions and no statement of whether one supersedes or credits the other. No comparable total, repair option or completion evidence provided. *Why:* Billing records conflict and overlap; no comparable total or completion evidence, so clarification is needed before any authority or payment decision.
- Unknown (affects route): Whether the £138 and £372 records are cumulative or whether one supersedes/credits the other; no single comparable total including VAT established.
- Unknown: Whether the stated amounts include VAT.
- Unknown (affects route): Both records give 5 February as the service date but no completion evidence is supplied; unclear whether actuator replacement was actually carried out.
- Unknown: Contractor still has not said whether the actuator can be repaired rather than replaced, or what the estimate covers.

**Event 019 — Note from Ivo Merrick (Property Manager, Northbridge Lettings)** — Jev `jev_route` → `clarify` — Jev routes; Claude extracts quotes and claims. clarify is not a Jev-only route. The message may state facts that need exact quotes. Open tenant questions may be answered.. claude-opus-5: update, route `clarify`, high confidence.
Internal file-review note from the property manager recording that written landlord authority covers diagnosis only, that the £372 estimate was sent after the stated service date, and that the file holds no authorization for actuator replacement and no completion or return-visit entry. *Why:* Internal note confirms authority and completion gaps; cannot instruct or close until the contractor clarifies invoices, repair option and completion evidence.
- Unknown (affects route): Whether the £138 and £372 invoice records are cumulative or one supersedes the other; no single comparable total including VAT established.
- Unknown (affects route): Whether actuator replacement was in fact carried out on 5 February; no completion evidence on file.
- Unknown (affects route): Whether the actuator can be repaired rather than replaced, and whether anyone in the tenant household is vulnerable given ongoing cold radiators in February.

**Event 020 — Portal from Tessa Vane (Tenant)** — Jev `jev_route` → `clarify` — Jev routes; Claude extracts quotes and claims. clarify is not a Jev-only route. Route confidence 0.62 is below the Jev-only bar 0.8. The message may state facts that need exact quotes. Open tenant questions may be answered.. claude-opus-5: answer_to_question, route `clarify`, high confidence.
Tenant recalls the 5 February visit but cannot say whether the actuator was replaced, and has seen no contractor since. Heating is working intermittently with one radiator cooler than the others. *Why:* Reply adds partial information but leaves completion, pricing and vulnerability questions open, so clarification continues.
- Unknown (affects route): Tenant cannot confirm whether actuator replacement took place on 5 February; no completion evidence from contractor.
- Unknown (affects route): Whether anyone in the household is vulnerable given ongoing cold radiators in February remains unanswered.

**Event 021 — Email from Ivo Merrick (Property Manager, Northbridge Lettings)** — Jev `jev_route` → `clarify` — Jev routes; Claude extracts quotes and claims. clarify is not a Jev-only route. Route confidence 0.79 is below the Jev-only bar 0.8. Open tenant questions may be answered.. claude-opus-5: update, route `clarify`, high confidence.
Property manager asked the contractor to confirm what work was completed and when, whether both invoice records remain current or one supersedes the other, how overlapping charges are treated, and requested job notes, parts records and authorisation/attendance evidence for the actuator work. *Why:* Outbound chase to contractor seeking completion, authorisation and billing clarification; essential facts still missing, so clarify stands.
- Unknown (affects route): Whether actuator replacement was carried out on 5 February remains unconfirmed; no completion evidence, job notes or parts record supplied.
- Unknown (affects route): Whether both invoice records (£138 and £372) are payable or one supersedes the other, and how overlapping charges are treated.
- Unknown: Whether anyone in the household is vulnerable given ongoing cold radiators in February is still unanswered.

**Event 022 — Email from Petra Quill (Contractor, Copper Finch Mechanical)** — Jev `jev_route` → `clarify` — Jev routes; Claude extracts quotes and claims. clarify is not a Jev-only route. Open tenant questions may be answered.. claude-opus-5: answer_to_question, route `clarify`, high confidence.
Contractor Petra Quill replied that she is still checking the records and cannot yet confirm whether the two invoice entries are separate chargeable work or whether one supersedes the other. No completion evidence, revised invoice or parts record was supplied. *Why:* Contractor provided no new substantive information; essential billing and completion facts remain outstanding, so clarification is still required.
- Unknown (affects route): Still unconfirmed whether actuator replacement was carried out on 5 February; no completion evidence, job notes or parts record supplied.
- Unknown: Whether both invoice records (£138 and £372) are payable or one supersedes the other, and how overlapping charges are treated.
- Unknown: No answer yet on whether the actuator can be repaired rather than replaced, or whether £372 inc VAT covers all parts, labour and testing.

**Event 023 — Email from Ivo Merrick (Property Manager, Northbridge Lettings)** — Jev `jev_route` → `clarify` — Jev routes; Claude extracts quotes and claims. clarify is not a Jev-only route. Open tenant questions may be answered.. claude-opus-5: update, route `clarify`, high confidence.
Property manager updates the landlord that two invoice records remain unresolved with no payment, supersession or authorisation for actuator work, and the tenant still reports intermittent heating. He asks the landlord how to proceed and whether further work or expenditure is authorised. *Why:* Authorisation and completion evidence remain unresolved; message seeks landlord instruction, so clarify stands.
- Unknown (affects route): Landlord's decision on the unresolved invoice records and whether further work or expenditure is authorised is still outstanding; contractor has not supplied completion evidence, job notes or parts record.

**Attachment invoice-NBL-CFM-250210-A.pdf (PDF text extraction)** — Jev `jev_route` → `clarify` — Jev routes; Claude extracts quotes and claims. clarify is not a Jev-only route. Route confidence 0.67 is below the Jev-only bar 0.8. The message may state facts that need exact quotes. Open tenant questions may be answered.. claude-opus-5: update, route `clarify`, medium confidence.
Invoice NBL-CFM-250210-A from Copper Finch Mechanical dated 10 February 2025 for £138.00 inc VAT covering attendance, diagnosis, actuator inspection and operational test on 5 February. It does not address the overlapping £372 record, actuator replacement authorisation or completion evidence. *Why:* Document only restates the £138 charge; the overlapping invoice, authority and completion questions remain open, so clarification is still needed.
- Unknown (affects route): Whether this £138 invoice supersedes or sits alongside the £372 record remains unstated; no parts record, completion evidence or authorisation for actuator replacement is supplied.
- Unknown (affects route): No confirmation whether the actuator was replaced or the heating fault resolved.

**Attachment invoice-NBL-CFM-250210-B.pdf (PDF text extraction)** — Jev `jev_route` → `clarify` — Jev routes; Claude extracts quotes and claims. clarify is not a Jev-only route. The message may state facts that need exact quotes. Open tenant questions may be answered.. claude-opus-5: update, route `clarify`, high confidence.
Second invoice from Copper Finch Mechanical (NBL-CFM-250210-B) for £372.00 inc VAT covering heating valve actuator supply and replacement, same 5 February service date as the £138.00 invoice A. It is still unstated whether this supersedes or duplicates the other record, and no authorisation or completion evidence is provided. *Why:* Billing document adds a second overlapping invoice without authorisation or completion evidence; clarification needed before any payment or further action.
- Unknown (affects route): Whether invoice B (£372.00) supersedes or sits alongside invoice A (£138.00) for the same 5 February service date; overlapping attendance and diagnosis charges are unresolved.
- Unknown (affects route): No parts record, attendance evidence or confirmation that the actuator replacement was actually carried out or that the heating fault is resolved.
- Unknown (affects route): No written landlord authorisation on file for actuator replacement; authority covered diagnosis only.
