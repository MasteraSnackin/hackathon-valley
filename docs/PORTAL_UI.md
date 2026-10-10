# Tenant and property-manager workspace

The two views share the existing Python case service and native Vercel Workflow
coordinator. The view toggle is a local demonstration convenience, not a
production login or authorisation mechanism.

## Tenant journey

Start with a description of the problem. The conversation gathers the tenant's
name, address and issue, retaining information already supplied and asking for
missing details. A complete report creates one shared case. Further messages
become original evidence on that case and wake its coordinator.

The tenant session has a separate cookie and conversation ownership checks. Its
API returns only the tenant's messages, supplied details and a plain-language
progress projection. It does not return internal reviews, policy controls, staff
evidence or the shared case list. Supplying a statement is not permission to act.

The tenant's own name and address, given in their session, are stored on the case
as self-identification (never as a verified claim). Policy setting
`tenant_self_identification` (default `clarify`, `request_quote`) lets them satisfy
the identity and route checks for those information-gathering actions only; replies
go back to the same in-app thread. Visits, keys, instructing work, closing and
archiving still need the case manager. If the tenant later corrects their name or
address, self-identification stops counting and the case manager verifies.

Conversation extraction is a bounded, local demonstration parser. Unrecognised
wording needs clarification. This is not a verified general-purpose conversational
model or a production identity service.

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
| `POST /api/tenant/conversations/{id}/messages` | Add a message and continue the shared case |
| `POST /api/policy-assistant/interpret` | Interpret supported plain-English policy wording without saving |
| `GET /api/policy-assistant/reviews/{id}/suggestion` | Suggest a reusable draft based on a resolved review |

Existing `/api/policies/draft`, preview and publish routes retain their role and
freshness checks. Policy-assistant endpoints require a staff session.
