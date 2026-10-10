# Claude triage and tenant messaging

With the default `router: jev` policy, TypeSafe Jev routes each message first and Claude reads only what Jev hands off or routed with facts to extract; see [Jev routing](JEV_ROUTING.md). The rest of this page describes Claude's reading. With `router: claude`, or without a TypeSafe key, Claude reads every incoming message, chooses the workflow route, extracts quoted assertions and drafts tenant questions. The policy engine and named staff still decide what may happen. There is no keyword interpreter: when Claude is unavailable, a person triages the message.

## Tenant intake (before submission)

In the tenant portal, Claude (`ai.tenant_intake`, effort `CLAUDE_INTAKE_EFFORT`, default `low`) reads the conversation, extracts name, address and each separate problem, and writes the reply. Missing details get a friendly "Hey, before I continue, could you clarify a few things for us?" with at most three questions. `ai.checked_intake` keeps only values found in the tenant's own words; the summary card is shown only when name, address and a problem are all present. Nothing is submitted until the tenant confirms. A confirming reply counts only after a summary was shown. When Claude is unavailable, the local phrase parser fills the same card.

## Where it runs

Each case has one native Vercel Workflow coordinator (`app.workflows.case_coordinator`). It runs three kinds of durable step:

| Step | Service function | What it does |
| --- | --- | --- |
| `run_case_cycle` | `coordinator_cycle` | Assesses policy, runs timers, executes permitted simulated actions, reports whether model work is due |
| `triage_case_messages` | `triage_messages` | Claude reads each stored, unread message; routes the case; splits separate issues into new cases and starts their coordinators |
| `compose_tenant_messages` | `compose_tenant_messages` | Claude drafts questions for open tenant clarifications and recommends auto-send or staff review; the policy gate decides |

```
message stored (HTTP request returns at once; triage state "pending", actions WAIT)
  → run_case_cycle reports needs_triage
  → triage_case_messages: Claude reading → route, claims, ambiguities, answers
  → run_case_cycle: gates re-evaluated; routine permitted action may execute
  → compose_tenant_messages when a tenant question is open
  → wait for the next message, staff decision or timer
```

The model is called outside database transactions. Results are stored with idempotent keys (`triage:{source}:{attempt}`, `tenant_message:{questions}`, `tenant_message_sent:{id}`, `split:{source}:{issue}`), so a retried step never applies a reading twice, splits twice or sends twice. A crash between Claude's response and the commit costs one repeated call, not a duplicate effect. At most eight model steps run per wake.

`WORKFLOW_MODE=manual_demo` runs the same service functions inline in the HTTP request, labelled as manual mode.

## Routing

Claude picks one route per issue from `ROUTES` in `app/domain.py`. Each route maps to exactly one policy action:

`request_quote`, `confirm_appointment`, `supply_keys`, `instruct_work`, `close_item`, `clarify`, `urgent_hazard` (→ clarify, held for a person), `archive`, `unsupported` (→ clarify, category other).

- The first reading names the work item and sets the action. Later messages move the same item along its workflow; the work item name is kept so evidence keeps its scope.
- A route or category chosen by staff (at intake or via the proposal endpoint) is manual triage and is never overridden by Claude.
- A separate problem in the same message becomes its own case (`parent_case_id`), with the issue's quotes and claims.

## What Claude may assert

Only `access`, `keys`, `schedule`, `completion`, `total` and `urgent`, each with an exact quote from the message. All are stored **unverified**; the named role verifies them through the existing review cards. Identity, contact route, authority, commitments and finance never come from the model. Quotes not found verbatim in the source are dropped and listed in `rejected_items`.

The derived category label is the one exception, as the implementation plan allows (R6): with policy `triage_auto_accept` (`high` by default, or `medium` / `never`), a classification at or above that confidence is recorded as verified, with the policy version in its verification note. Otherwise the case manager confirms it.

## Holds created by triage

`triage_check` in `app/domain.py` adds a `triage` blocker:

| Situation | Response |
| --- | --- |
| Message not yet read | WAIT (every action held) |
| Claude unavailable, refused or returned invalid output | HUMAN REVIEW: case manager triages manually or retries (`POST /api/cases/{id}/triage/retry`) |
| `urgent_hazard` route | HUMAN REVIEW: a person takes over before any automated contact |
| Staff category differs from Claude's | CONFLICT → HUMAN REVIEW |
| Route-affecting ambiguity | CLARIFY: a tenant question when the route is verified, otherwise HUMAN REVIEW |

The case manager can confirm Claude's reading by approving the `triage` review.

## Tenant questions

Policy CLARIFY blockers for tenant-answerable facts (`access`, `keys`, `schedule`, `completion`, `evidence`, `classification`, `triage`) create tracked questions. Claude writes one message covering up to `tenant_max_questions` of them, and recommends `auto_send` or `staff_review` with a reason, using the case data, conversation and policy it is given.

The deterministic gate sends automatically only if **all** hold:

- policy `tenant_messages` is `claude_decides` (not `staff_approval` or `off`);
- Claude chose `auto_send`;
- every question topic is in `tenant_auto_send_topics`;
- every open question is covered;
- there are no risk flags from the draft or the triage;
- there is no possible urgent hazard;
- tenant identity and contact route are verified.

Otherwise the draft waits for a case manager (`POST /api/messages/{id}/approve`, optional edited text) or is held because the route is unverified. A rejection (`POST /api/messages/{id}/reject`, `redraft: true`) lets Claude redraft with the staff reason as feedback.

Sending is a simulated in-app thread. Reminders count from the actual send time; escalation also runs while a draft waits. A reply (`POST /api/cases/{id}/tenant-reply`) is stored evidence; Claude's next reading marks each open question answered, partial or unanswered. An answered question is never asked again: if the reply did not settle the fact, it goes to a person. A partial answer allows `tenant_follow_ups` narrower follow-ups.

## Model call

- Model: `CLAUDE_MODEL`, default `claude-opus-5`.
- API: Anthropic Python SDK `beta.messages.parse` with Pydantic structured output.
- Thinking: adaptive. Effort is `CLAUDE_TRIAGE_EFFORT` (default `medium`) for triage, `CLAUDE_DRAFT_EFFORT` (default `low`) for drafts and `CLAUDE_INTAKE_EFFORT` (default `low`) for the tenant intake assistant.
- Fallbacks: server-side `fallbacks: "default"` (`server-side-fallback-2026-07-01`). A refusal still hands the message to a person.
- Caching: the static system prompt carries a `cache_control` breakpoint. In the live native test, about 3.9k prompt tokens were read from the cache.
- Audit: each reading records the model, request ID, prompt version, effort, token usage and whether a fallback was used.

Credentials come from `ANTHROPIC_API_KEY`. For local development, put it in the git-ignored `.env.local`. It is never logged or shown; `/api/health` reports only whether one is configured.

## Verification

- `tests/test_claude_live.py` (marker `claude`) calls the real API on fictional messages. Scenarios:
  - routing, clarification and re-reading;
  - splitting a separate issue into its own case;
  - tenant question, consent reply and access-officer review;
  - staff-approval policy;
  - hazard hold;
  - prompt injection.
- `tests/test_native_api.py::test_native_claude_triage_step_routes_a_new_report` runs the same path inside the real native workflow runtime.
- All other tests are offline. They use manual staff triage or a removed credential. Without a credential the `claude` tests are skipped.
