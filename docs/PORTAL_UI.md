# Tenant and property-manager workspace

The two views share the existing Python case service and native Vercel Workflow
coordinator. The view toggle is a local demonstration convenience, not a
production login or authorisation mechanism.

## Tenant journey

Start with a description of the problem. Claude reads the whole conversation and
gathers the tenant's name, address and each separate problem. If anything is
missing it asks in a friendly way ("Hey, before I continue, could you clarify a few
things for us?"), at most three questions at a time.

When the details are complete, the tenant sees a **Here's what I've got** card with
their name, address and numbered problems. Nothing reaches property management
until the tenant presses **Yes, send it** (or replies that it is right). **Something's
not right** lets them type a correction, which refreshes the summary. Confirming
creates one shared case whose report keeps the tenant's own words first, followed
by the labelled confirmed summary. On the staff side, Claude triage routes the case,
splits separate problems into their own cases and the policy engine holds anything
ambiguous for a person. Further tenant messages become original evidence on that
case and wake its coordinator.

The tenant session has a separate cookie and conversation ownership checks. Its
API returns only the tenant's messages, supplied details and a plain-language
progress projection. It does not return internal reviews, policy controls, staff
evidence or the shared case list. Supplying a statement is not permission to act.

The name and address the tenant confirmed in their summary are stored on the case
as self-identification (never as a verified claim). Policy setting
`tenant_self_identification` (default `clarify`, `request_quote`) lets them satisfy
the identity and route checks for those information-gathering actions only; replies
go back to the same in-app thread. Visits, keys, instructing work, closing and
archiving still need the case manager. If the tenant later corrects their name or
address, self-identification stops counting and the case manager verifies.

Claude only proposes the summary. A name, address or problem is kept only if it
occurs in the tenant's own messages, and the summary card appears only when all
three are present, whatever Claude says. A tenant's confirmation records that they
checked the wording; it does not verify identity, address or permission. When
Claude is unavailable, the bounded local phrase parser fills the same card, and
unrecognised wording needs clarification. This is not a production identity
service. Tenant messages are sent to the Anthropic API before submission.

## Property-manager journey

Requests requiring attention appear ahead of routine work. Opening a request
shows its current action, evidence, unresolved checks and human decisions.
Completion of a quote or another intermediate action does not mark the repair
resolved. Resolution requires the existing completion checks.

The policy workspace retains editable thresholds and structured conditions.
Plain-English input produces a proposed interpretation for supported policy
settings and conditions. Missing values and unsupported instructions do not
silently become executable rules. The user can edit the structured result,
save it as a draft, preview its effects and publish it with the policy-editor
role. Pending cases retain the existing explicit reassessment requirement.

After answering a human review, staff can request a reusable policy suggestion.
It carries the source review reference and remains a draft. A decision about
one visit's access or one job's authority never grants global consent or
authority. No source code is rewritten and no policy is published automatically.

## Local boundaries

- All contractor contact, bookings and other external actions remain simulated.
- Tenant demo sessions are local-only and disabled in production mode until a
  real tenant identity and organisation access model is provided.
- No voice integration or real tenant login is included in this UI work.
- BUILD and reserved evaluation boundaries remain unchanged. UI checks use
  fictional scenarios in separate storage.
- Existing native Workflow durability and case policy checks remain the action
  authority; neither view can bypass them.

## Endpoints

| Endpoint | Purpose |
| --- | --- |
| `GET /api/tenant/session` | Current tenant session and owned conversations |
| `POST /api/tenant/session` | Establish a loopback-only demo tenant session |
| `POST /api/tenant/conversations` | Begin a report with text and an idempotency key |
| `GET /api/tenant/conversations/{id}` | Read an owned conversation and safe progress |
| `POST /api/tenant/conversations/{id}/messages` | Add a message: answer a question, correct the summary, or update the shared case |
| `POST /api/tenant/conversations/{id}/confirm` | Confirm the summary and send the request to property management |
| `POST /api/policy-assistant/interpret` | Interpret supported plain-English policy wording without saving |
| `GET /api/policy-assistant/reviews/{id}/suggestion` | Suggest a reusable draft based on a resolved review |

Existing `/api/policies/draft`, preview and publish routes retain their role and
freshness checks. Policy-assistant endpoints require a staff session.
