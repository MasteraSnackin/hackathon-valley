# Voice intake: tenants, landlords, letting agencies and contractors

The voice agent (built separately) posts each caller turn to `POST /api/inbound`. The workflow works out who is calling, which property and case it concerns, and what that caller may hear. It then hands the message to the existing case coordinator, which routes it with Jev and reads it with Claude as usual. Everything outbound stays simulated.

## Request

```http
POST /api/inbound
Authorization: Bearer $VOICE_BRIDGE_TOKEN
Content-Type: application/json

{"call_id": "call-123-turn-1", "caller_number": "+447700900201",
 "transcript": "About Flat 7 Park View: the landlord is happy to go ahead.",
 "intent": "report", "channel": "voice"}
```

| Field | Meaning |
| --- | --- |
| `call_id` | Required idempotency key. A retry with the same body returns the same answer; the same id with a different body is `409`. |
| `caller_number` | Caller ID. Matched against the fictional directory; never stored. |
| `transcript` | What the caller said. Untrusted data. |
| `intent` | `report` (default): stored as case evidence and read by the workflow. `status_enquiry`: answered from a filtered summary and **not** added to the case. |
| `channel` | `voice` (default), `sms` or `email`. |
| `occurred_at` | Optional ISO timestamp with timezone. |

Set `VOICE_BRIDGE_TOKEN` in the git-ignored `.env.local`. Without a token, only a loopback staff demo session can post (the **Demo tools → Simulate a call** panel). Through a tunnel (for example ngrok), `/api/inbound` accepts only the bearer token. Every other staff route stays closed, as for the ElevenLabs tenant line in [Phone intake](VOICE_PHONE.md).

## Response (fast, no model call)

```json
{"outcome": "attached", "case_id": "…", "party": {"kind": "agency", "name": "Harbour Lettings", "verified": true, "match": "caller_id_fictional_directory"},
 "property": {"ref": "DEMO-PARK-7", "address": "Flat 7, Park View, Demo Town"},
 "say": "Thanks. I've added that to the boiler not heating job at Flat 7, Park View, Demo Town. The team will follow up.", "simulated": true}
```

Speak `say` to the caller. `outcome` is one of:

- `new_case`: no open job for the property, so a case was opened.
- `attached`: added to the property's latest open job. If Claude finds a separate problem, it splits it into its own case.
- `status`: a status answer, filtered for the kind of caller.
- `needs_property`: the caller has several properties and didn't name one. Ask which property, then send a new turn.

## Who is who

| Caller | Match | Can do |
| --- | --- | --- |
| Tenant | Number in the directory; one property | Report, update, give access, availability and photos; hears progress and appointment status, never the price |
| Landlord | Number in the directory | Approve or decline work (`authority`); hears the quote and whether approval is pending |
| Letting agency | Number in the directory; acts for the landlord | Same as the landlord |
| Contractor | Number in the directory | Give the quote (`total`) and report completion; hears the job, address, appointment and access status, never the tenant's details |
| Unknown number | Not in the directory | A case for a person to check; hears no case details |

`app/parties.py` holds the fictional directory. All numbers are in Ofcom's reserved 07700 900xxx drama range:

| Number | Party | Properties |
| --- | --- | --- |
| 07700 900101 | Tenant Alex Taylor | Flat 7, Park View (`DEMO-PARK-7`) |
| 07700 900102 | Tenant Sam Rivera | 2 Sample Lane (`DEMO-LANE-2`) |
| 07700 900201 | Landlord Morgan Lee | both |
| 07700 900301 | Letting agency Harbour Lettings | both |
| 07700 900401 | Demo contractor | both |

## Rules the policy enforces

- **Whose word counts.** `FACT_SOURCES` lists who may assert what: access consent only from the tenant, approval only from the landlord or agency, the quote only from the contractor, completion from the tenant or contractor. A positive claim from anyone else is stored as **hearsay**: staff can see it, but it never satisfies a check. A refusal from anyone still stops the action (fail closed).
- **Authority is never automatic.** Claude may now read an `authority` claim, but only from a directory-matched sender. It is stored unverified, and an approver must verify it in Human review.
- **Questions go to the right party.** On directory properties, a missing approval becomes a question to the landlord (topic `approval`) and a missing quote becomes a question to the contractor (topic `quote`). Tenant topics are unchanged. Claude drafts each message and the same deterministic gate decides auto-send or staff review. The policy settings are `party_messages` and `party_auto_send_topics`. A reply can close only questions addressed to that party; for landlord questions, the agency can answer too.
- **Caller ID is a demonstration identity.** A directory match counts as verified identity and contact route for these fictional properties only. Production needs real identity verification, because caller ID can be spoofed.

## Demo script

1. Tenant (900101): "The boiler is not heating the flat." A new case opens; Claude routes it to a quote request, which the coordinator runs (simulated).
2. Contractor (900401): "Quote for the boiler at Flat 7 Park View is £450 including VAT." The quote is recorded as the contractor's claim. A simulated approval question goes to the landlord, and tenant questions (access, availability, photos) go to the tenant.
3. Agency (900301): "About Flat 7 Park View, the landlord is happy to go ahead." This records an approval claim from the agency and an approver verifies it in Human review.
4. Any caller, `status_enquiry`: "Any news?" Each caller gets a status answer filtered for their role.

## Not verified

The offline tests use scripted Claude readings. `test_live_claude_reads_a_landlord_approval_and_drafts_a_landlord_question` exercises the real prompts and is skipped without `ANTHROPIC_API_KEY`. Real telephony, real identity checks and real message delivery are not implemented.
