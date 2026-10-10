# Reasoning — Property Management case 029

Exported from the system's recorded policy assessments, claims and concise model rationales. It is not reconstructed after the fact and does not contain hidden chain-of-thought.

## System case `586f18c17a05` — HUMAN REVIEW

### Why this decision (policy gates)

The model cannot create authority: the policy engine decides from recorded checks. Each blocker below kept the action from running.

- `identity` is **UNKNOWN** → HUMAN REVIEW (rule `require-identity`, owner case manager): Verify the person, property and work item mapping. — evidence: no source recorded
- `route` is **UNKNOWN** → HUMAN REVIEW (rule `require-route`, owner case manager): Verify the recipient and permitted communication route. — evidence: no source recorded

### Claims extracted from the sources

Every claim is a source assertion with an exact quote; unverified claims were never used as authority.

- `classification` = true — verified; from Split from case a65384cfd3a3: Event 005 — Email from Orren Vale (Landlord): “he asked someone to look into intermittent boiler pressure loss”

### Reading of each source (Jev route → Claude reading)

## System case `a65384cfd3a3` — HUMAN REVIEW

### Why this decision (policy gates)

The model cannot create authority: the policy engine decides from recorded checks. Each blocker below kept the action from running.

- `identity` is **UNKNOWN** → HUMAN REVIEW (rule `require-identity`, owner case manager): Verify the person, property and work item mapping. — evidence: no source recorded
- `route` is **UNKNOWN** → HUMAN REVIEW (rule `require-route`, owner case manager): Verify the recipient and permitted communication route. — evidence: no source recorded
- `triage` is **UNKNOWN** → WAIT (rule `require-triage`, owner case manager): The latest message is being routed and read. Actions wait for the reading. — evidence: Event 012 — Call from Tamsin Rook (Property Manager, Northbridge Lettings)

### Claims extracted from the sources

Every claim is a source assertion with an exact quote; unverified claims were never used as authority.

- `access` = false — unverified assertion; from Intake report: “has not agreed to a visit or key arrangement”
- `keys` = false — unverified assertion; from Intake report: “has not agreed to a visit or key arrangement”
- `keys` = false — unverified assertion; from Event 005 — Email from Orren Vale (Landlord): “has not fixed a date or discussed keys or access with the tenant”
- `access` = false — unverified assertion; from Event 005 — Email from Orren Vale (Landlord): “has not fixed a date or discussed keys or access with the tenant”
- `access` = false — unverified assertion; from Event 006 — Call from Elowen Vey (Tenant): “she does not consider him an access contact and does not want him asked to let anyone in”

### Reading of each source (Jev route → Claude reading)

**Intake report** — Jev `claude` — Jev route confidence 0.24 is below 0.5.. claude-opus-5: new_request, route `unsupported`, medium confidence.
Tenant Elowen Vey reports that an unidentified caller claiming to be a heating contractor asked her to leave the front-door key in the outside meter cabinet for a possible visit on Wednesday 14 May. She states she has no appointment window and has not agreed to any visit or key arrangement. *Why:* No maintenance defect is reported; the message concerns an unverified third party requesting unsupervised key access, which falls outside the standard repair categories and needs a case manager to define handling and verify the caller.
- Unknown (affects route): Whether any heating visit has in fact been arranged by the agency or landlord, and whether the caller is a genuine instructed contractor, is unknown; the key-in-meter-cabinet request should be verified before any entry.
- Unknown (affects route): No underlying heating defect or job is described, so it is unclear what work, if any, the supposed visit relates to.
- Unknown: Confirm the agreed key custody arrangement for this property and that no key is to be left in an unsecured external cabinet.
- Risk flags: safety

**Event 002 — Note from Tamsin Rook (Property Manager, Northbridge Lettings)** — Jev `jev_route` → `clarify` — Jev routes; Claude extracts quotes and claims. clarify is not a Jev-only route.. claude-opus-5: update, route `clarify`, high confidence.
Property manager notes a maintenance enquiry has been opened and that the property record shows no active work order or confirmed appointment for the reported heating visit. *Why:* Internal note confirming no appointment or work order exists; verification still outstanding, so clarify stands.
- Unknown: Caller's identity and legitimacy remain unverified; no key should be left in the meter cabinet until confirmed.
- Unknown (affects route): No underlying heating defect or job is described, so the purpose of any visit is unknown.
- Risk flags: possible_wrong_recipient

**Event 003 — SMS from Elowen Vey (Tenant)** — Jev `jev_route` → `clarify` — Jev routes; Claude extracts quotes and claims. clarify is not a Jev-only route.. claude-opus-5: update, route `clarify`, high confidence.
Tenant provides the caller's stated name (Bram Alder) and phone number (07700 900683) for the unverified request to leave a key in the outside meter cabinet. She confirmed the property address to him but gave no entry code or access details. *Why:* Additional identifying detail about an unverified caller; no job or appointment exists, so clarification is still needed before any action.
- Unknown (affects route): No underlying heating defect or job is described, so the purpose of any visit is unknown.
- Unknown: Caller's identity unverified; no contractor named Bram Alder is linked to any work order for this property.
- Risk flags: possible_wrong_recipient, sensitive_personal_data

**Event 004 — Email from Tamsin Rook (Property Manager, Northbridge Lettings)** — Jev `jev_route` → `clarify` — Jev routes; Claude extracts quotes and claims. clarify is not a Jev-only route.. claude-opus-5: update, route `clarify`, high confidence.
Property manager emailed the landlord asking whether he had arranged any heating work, identified the contractor, or agreed a date or key arrangement. No new facts established. *Why:* Outbound verification enquiry; no new information yet, so the item remains in clarification pending the landlord's reply.
- Unknown (affects route): Awaiting landlord confirmation whether any contractor visit or key arrangement was authorised.
- Unknown (affects route): No underlying heating defect or job is described, so the purpose of any visit is unknown.
- Risk flags: safety, possible_wrong_recipient

**Event 005 — Email from Orren Vale (Landlord)** — Jev `jev_route` → `clarify` — Jev routes; Claude extracts quotes and claims. clarify is not a Jev-only route.. claude-opus-5: answer_to_question, route `clarify`, high confidence.
Landlord confirms he asked someone to look into intermittent boiler pressure loss but has not fixed a date, discussed keys or access, and cannot confirm the caller's identity. The key-in-meter-cabinet request remains unverified. *Why:* Landlord cannot verify the caller or confirm any key/access arrangement; identity must be clarified before any entry.
- Unknown (affects route): Identity of the contractor the landlord engaged is unknown, so the caller cannot be verified.
- Unknown: No date or appointment window agreed for any boiler visit.
- Risk flags: safety, possible_wrong_recipient

**Event 006 — Call from Elowen Vey (Tenant)** — Jev `jev_route` → `clarify` — Jev routes; Claude extracts quotes and claims. clarify is not a Jev-only route. Route confidence 0.58 is below the Jev-only bar 0.8. Possible distress, complaint or vulnerability.. claude-opus-5: update, route `clarify`, high confidence.
Tenant will be away during the proposed Wednesday morning period and states her 15-year-old son is not an access contact and should not be asked to let anyone in. Caller's identity remains unverified and no appointment or key arrangement exists. *Why:* Unverified caller seeking key access; tenant refuses access via her minor son and is away. Cannot act until contractor identity is verified.
- Unknown: No access arrangement is possible for Wednesday morning as the tenant is away; alternative date and verified contractor needed.
- Unknown (affects route): Identity of the contractor the landlord engaged is still unknown, so the caller cannot be verified.
- Unknown: Tenant's alternative availability for a boiler visit is not stated.
- Risk flags: safety, vulnerable_person

**Event 007 — Email from Orren Vale (Landlord)** — Jev `jev_route` → `clarify` — Jev routes; Claude extracts quotes and claims. clarify is not a Jev-only route. Possible distress, complaint or vulnerability.. claude-opus-5: update, route `clarify`, high confidence.
Landlord forwards a message from the caller Bram Alder saying he 'might call in Wednesday morning'. It gives no appointment window, work reference, business address, or tenant agreement to access, so the caller remains unverified. *Why:* Forwarded message adds no verification of identity, appointment or access consent, so clarification is still required before any visit or key arrangement.
- Unknown (affects route): Contractor's identity and business details still unverified; no work reference supplied.
- Unknown: 'Might call in Wednesday morning' is not a confirmed appointment window.
- Unknown: No tenant consent to entry; tenant will be away and her son is not an access contact.
- Risk flags: safety

**Event 008 — Email from Tamsin Rook (Property Manager, Northbridge Lettings)** — Jev `jev_route` → `clarify` — Jev routes; Claude extracts quotes and claims. clarify is not a Jev-only route. Possible distress, complaint or vulnerability.. claude-opus-5: update, route `clarify`, high confidence.
Property manager emailed the purported contractor asking him to confirm his business identity and contact details, the work he believes he has been asked to do, the proposed visit time, and whether he asked the tenant to leave a key in the meter cabinet. No new facts confirmed yet. *Why:* Outbound verification request; identity, scope and key arrangement still unverified, so the item stays at clarify.
- Unknown (affects route): Contractor's business identity, contact details and the scope of work he believes he was instructed to do remain unconfirmed.
- Unknown (affects route): Unconfirmed whether the caller asked for a key to be left in the meter cabinet; no authorised key arrangement exists.
- Unknown: No proposed visit date and time confirmed.
- Risk flags: safety

**Event 009 — Email from Bram Alder (Contractor, Hearthline Boiler Service)** — Jev `jev_route` → `clarify` — Jev routes; Claude extracts quotes and claims. clarify is not a Jev-only route. The message may state facts that need exact quotes.. claude-opus-5: answer_to_question, route `clarify`, high confidence.
Contractor Bram Alder replies that he understood the landlord wanted him to 'check the boiler' and that Wednesday morning might suit, and confirms the meter-cabinet key request was to avoid a wasted journey. No work reference, business address or confirmed appointment time provided. *Why:* Identity, authority and key arrangement still unverified; cannot arrange access yet.
- Unknown (affects route): Contractor's business identity, address and work reference remain unconfirmed; scope stated only as 'check the boiler'.
- Unknown (affects route): Contractor confirms he asked for a key in the meter cabinet; no authorised key arrangement exists and tenant has not consented.
- Unknown: 'Wednesday morning might suit' is not a confirmed date and time, and the tenant is away then.
- Risk flags: safety

**Event 010 — Portal from Elowen Vey (Tenant)** — Jev `jev_route` → `clarify` — Jev routes; Claude extracts quotes and claims. clarify is not a Jev-only route. Route confidence 0.56 is below the Jev-only bar 0.8.. claude-opus-5: update, route `clarify`, high confidence.
Tenant reports the meter cabinet is outside and shared with neighbouring homes, and asks whether a visit has actually been arranged, stating she has no appointment details. *Why:* Contractor identity, scope and appointment remain unverified and the proposed key location is insecure; clarification needed before any access or key arrangement.
- Unknown (affects route): Proposed key drop point is an outside cabinet shared with neighbouring homes; no secure or authorised key arrangement exists.
- Unknown: No appointment has been confirmed to the tenant; she has no date or time details.
- Unknown (affects route): Tenant has not consented to entry and no verified contractor identity exists.
- Risk flags: safety

**Event 011 — Email from Orren Vale (Landlord)** — Jev `jev_route` → `clarify` — Jev routes; Claude extracts quotes and claims. clarify is not a Jev-only route. Route confidence 0.70 is below the Jev-only bar 0.8.. claude-opus-5: update, route `clarify`, high confidence.
Landlord says he has used Bram Alder before at another property but has not verified current business details or insurance. He wants the boiler pressure issue investigated but gives no date. *Why:* Identity, access and scheduling still unresolved; clarification needed before any visit or key arrangement.
- Unknown (affects route): Contractor's current business identity and insurance remain unverified.
- Unknown: No date or time proposed for the visit.
- Unknown (affects route): Tenant consent and a secure key arrangement are still absent.

## Failures and uncertainties

- Runner: Batch runner process was stopped when the operator's agent session ended, after 11 of 20 sources had settled. The runner itself recorded no result for this case; this status was written afterwards by the operator to mark the interruption. Partial evidence up to checkpoint-010 is preserved; nothing after that was processed.
- The run did not settle cleanly (status `interrupted`); any recorded state is partial.
