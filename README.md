# Property Desk

A local property maintenance prototype with Python policy evaluation, a staff dashboard and the native Python Vercel Workflow SDK. All communications, bookings, instructions and payment-related actions are simulated. No public deployment or real external action has been performed.

## Run locally

Use Python 3.12 (pinned in `.python-version`). Dependencies are managed with [uv](https://docs.astral.sh/uv/); `uv.lock` is the exact resolved set. The native SDK is pinned to `vercel-workflow==0.11.1`.

```sh
uv sync
printf 'ANTHROPIC_API_KEY=your-key\n' > .env.local   # git-ignored; loaded at startup
APP_MODE=demo WORKFLOW_MODE=native_local WORKFLOW_TARGET_WORLD=local uv run uvicorn app.main:app --host 127.0.0.1 --port 8017
```

Claude (`CLAUDE_MODEL`, default `claude-opus-5`) reads every message, routes it to a workflow and drafts tenant questions; see `docs/CLAUDE_TRIAGE.md`. Without a credential each message is handed to a case manager for manual triage.

`uv sync` creates `.venv` and installs the runtime dependencies plus the `dev` group (pytest, pypdf). Add a dependency with `uv add <package>` (or `uv add --dev <package>`). `requirements.lock` is kept for pip-only environments; refresh it after changing dependencies with `uv export --no-hashes --no-emit-project -o requirements.lock`. Without uv: `python3.12 -m venv .venv && .venv/bin/python -m pip install -r requirements.lock`.

The existing `.venv` can be used directly; recreating it is unnecessary when dependencies are already installed. Open <http://127.0.0.1:8017>. Use one Uvicorn process without `--reload`. Do not set `VERCEL_QUEUE_BASE_URL` for local mode. The application loads only the git-ignored `.env.local` (existing environment variables win); `.env.example` documents optional settings.

The default application database is `var/property.db`. The native SDK stores its separate local workflow history in its configured local data directory; see `docs/WORKFLOW_RUNTIME.md`. Stop with Ctrl-C. Restarting from the same directory preserves cases and reviews and wakes their stored coordinators. The app must be running for local timers to be delivered.

To use the dashboard without running the native queue, set `WORKFLOW_MODE=manual_demo`. This is explicitly labelled manual demonstration mode. In that mode, the staff member uses **Reassess timers** and **Simulate action**; it is not native durable workflow execution.

## Try the product

1. Keep the **Case manager** demonstration role. Create a case with property reference `DEMO-FLAT-1`, a report such as “The dishwasher stops during its cycle”, and the supported appliance category. This fictional property has a preconfigured trusted identity and contact route. Other property references remain unverified.
2. The initial work instruction shows every missing requirement separately. Add original evidence and exact quoted claims. A source assertion does not verify itself.
3. Switch to the role named on a review. Verify a particular source claim or grant an explicitly scoped work/financial approval. The access officer checks recorded consent; an approver cannot replace it with a generic approval. The remaining blockers stay visible.
4. To demonstrate routine automatic progress, change the proposal to **Request a quote** on the same fictional dishwasher item. The directory and source-supported category meet its requirements. Native mode records one simulated action, without an unnecessary manager review. It does not infer permission to repair from that quote request.
5. Switch to **Policy editor**. Change the missing-access route, add an ALL/ANY condition group, or adjust the demonstration review limit. Save a draft, test its effects on current saved cases, compare, and publish. Existing cases receive a visible reassessment hold before changed settings can release an action.
6. Import a BUILD case using a chosen event count. The decision sees only that chronological prefix. Later history and every attachment are excluded. The catalogue title is not supplied to interpretation as case evidence.

Demonstration role switching is restricted to loopback and is not production authentication. Use fictional or supplied BUILD material in this local demo.

## What is implemented

- Separate immutable source records, claims, interpretations, policy versions, decisions, reviews and simulated action receipts, with a staff dashboard and linked source quotations.
- Per-action PASS / FAIL / UNKNOWN / CONFLICT checks. Every applicable blocker accumulates; financial approval never removes missing access. A later timestamp does not silently resolve conflicting claims.
- Readable editable ALL/ANY rules, action/property/category filters, owner, additional required facts, reminder limits, working-hour deadlines, holiday dates and review thresholds. Rules can add requirements and routes; they cannot remove the core identity, consent or authority gates.
- Role-checked factual correction, scoped expiring approval, rejection, evidence request and deferral. A rejected action remains held until the case manager changes the proposal. Superseded, expired and duplicate responses cannot execute it.
- Immutable policy publication with a current impact preview, explicit reassessment of pending cases, and preserved historical decision versions.
- Bounded simulated clarification requests and reminders, then human/deputy escalation. Silence cannot become consent, completion or approval.
- Native Workflow steps, one ordered case event consumer, typed hooks, durable timers and startup recovery. Every incoming event commits to the application database before signalling. The coordinator rechecks all current gates before any simulated execution.
- Stable business action IDs, idempotent evidence/intake keys, a simulated provider receipt ledger and an explicit uncertain-result reconciliation path. These checks demonstrate the design; real provider idempotency and read-back still need adapter-specific implementation.
- Claude triage as native workflow steps: each stored message is read by Claude, which chooses the workflow route, names the work item, splits separate issues into their own cases and extracts exact-quoted assertions (stored unverified). Unreadable, ambiguous, hazardous or disputed readings hold the action for a person. There is no keyword fallback.
- Claude-drafted tenant questions. Claude recommends auto-send or staff review from the case data and policy; a deterministic gate (policy mode, allowed topics, risk flags, hazards, verified route) decides. Staff approve, edit or reject drafts. Replies are read by Claude and close answered questions; answers remain unverified assertions. Sending is simulated.

The `total` fact means the **full comparable cumulative commitment for this job, including tax**, supplied and verified from evidence. The prototype does not have a real accounting integration to calculate it across invoices. Unknown is not zero. The illustrative default review limit is £100 inclusive; £100.01 requires a separate financial review.

## Tests and BUILD replay

```sh
uv run pytest -q                 # live Claude tests run when a key is configured
uv run pytest -q -m "not claude" # offline only
uv run python -m app.replay --all-first --output var/build-replay-first-events.json
uv run python -m app.replay --case 013 --events 2
```

The replay command validates the fixed BUILD manifest hashes, uses an isolated temporary database and the published demonstration policy, sends each selected history prefix to Claude for triage, and records assessments and any drafted tenant questions without running any adapter or sending anything. It is a development replay, not an accuracy score. Human acceptable-outcome labels and a separately run reserved evaluation remain future work. No reserved evaluation material is loaded by these tools.

The tests cover authority/access independence, conflicting and missing evidence, partial closure, policy publication during a wait, wrong-role and stale review responses, uncertain action reconciliation, duplicate intake/evidence/action handling, native hook/timer execution and native recovery across processes. See `docs/WORKFLOW_RUNTIME.md` for the specific native runtime proof and its limits.

## API

Interactive local schema: <http://127.0.0.1:8017/docs>.

| Endpoint | Purpose |
| --- | --- |
| `POST /api/demo-session` with `{"role":"case_manager"}` | Create the labelled loopback-only demonstration cookie session |
| `GET /api/session`, `GET /api/health` | Current modes and simulation labels |
| `GET /api/cases`, `POST /api/cases` | List/create cases; intake accepts an optional `idempotency_key` |
| `GET /api/cases/{id}` | Evidence, current decision, reviews, questions, actions and timeline |
| `POST /api/cases/{id}/evidence` | Original text and exact source-linked claims; optional idempotency key |
| `POST /api/cases/{id}/proposal` | Change scoped action and increment its revision |
| `POST /api/cases/{id}/evaluate` | Explicit policy reassessment |
| `POST /api/cases/{id}/tenant-reply` | Simulated tenant reply `{"text": ...}`; Claude reads it in the next coordinator step |
| `POST /api/cases/{id}/triage/retry` | Retry a failed Claude reading |
| `POST /api/messages/{id}/approve`, `POST /api/messages/{id}/reject` | Send (optionally edited) or reject a Claude-drafted tenant message; `{"reason":...,"redraft":true}` asks for a new draft |
| `POST /api/reviews/{id}/respond` | Role-checked `correct`, `approve`, `reject`, `defer` or `more_evidence` |
| `POST /api/cases/{id}/execute` | Simulated result; `{"outcome":"uncertain"}` demonstrates a lost acknowledgement |
| `POST /api/cases/{id}/reconcile` | Read the simulated provider receipt before retry |
| `POST /api/cases/{id}/tick` | Reassess timers at the actual current time |
| `GET /api/policies` | Active policy and saved drafts |
| `POST /api/policies/draft` | New immutable draft with base version and reason |
| `POST /api/policies/{id}/preview`, `POST /api/policies/{id}/publish` | Compare, then publish a still-current preview |
| `GET /api/build-cases` | Fixed allowed BUILD catalogue and first-event previews |
| `GET /api/build-cases/{id}/snapshot?event_count=2` | Selected history prefix |
| `POST /api/build-cases/{id}/import` with `{"event_count":2}` | Import that prefix as a new assessment case |

Evidence fields: `text`, `source_label`, optional `occurred_at` with timezone, `claims:[{key,value,source_quote,scope}]`. Omitted claim scope uses the current action. Property/person mappings can be scoped narrowly to the applicable property by an authorised verifier. No caller may override the proposal's canonical action/property/provider/work-item fields through `proposal.scope`.

For a correction, submit the chosen `claim_id`, its `source_id`, a reason and the review's required role. For approval, submit a source, reason, expiry and the exact scope from the review card. A hook token is never an authorisation credential.

## Deployment preparation and remaining boundaries

`vercel.json` selects FastAPI and `pyproject.toml` registers `app.workflows:wf`. Native cloud mode requires `APP_MODE=production`, `WORKFLOW_MODE=native_cloud`, the Vercel runtime/world configuration, a PostgreSQL `DATABASE_URL` and separately provisioned staff identities in `STAFF_TOKEN_ROLES`. The app fails startup if cloud/local workflow modes disagree. No cloud project has been linked or deployed.

The production API's token hashes are a deployment placeholder; a production browser login, organisation/tenant isolation, a real authority directory, attachment object storage, communications/contractor/accounting adapters, operational monitoring and cloud acceptance testing remain required before real use. The native Python SDK is beta. Only the explicit `demo` policy profile is configured; incompatible/unsupported profiles remain held. Files under `handoff/` and `data/build/` remain read-only.

See `docs/BUILD_REPLAY_BOUNDARY.md` for the documented attachment exclusion, including the retrospective material in BUILD 008.
