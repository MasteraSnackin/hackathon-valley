# Property Desk staff dashboard

This React application lets property staff inspect maintenance cases, answer scoped reviews and manage policy drafts. It uses the Python backend in this repository. The original tenant conversation and staff interface are still served by FastAPI; this application is a separate staff surface.

The design contract is in [DESIGN.md](../DESIGN.md). Read the [root README](../README.md) for Python installation, model configuration and the wider product, and [ARCHITECTURE.md](../ARCHITECTURE.md) for the workflow and evidence model.

## Run locally

Requirements: the repository's prepared Python environment, Node.js 22.12 or later and npm. Dependencies also accept Node 20 from 20.19. The frontend uses React, TypeScript, Vite and Tailwind.

Start an isolated backend from the repository root. This example disables model credentials and `.env.local` loading so that UI checks do not make provider calls:

```sh
mkdir -p var
property_ui_dir=$(mktemp -d "$PWD/var/staff-ui.XXXXXX")
printf 'Demo storage: %s\n' "$property_ui_dir"

env -u VERCEL_QUEUE_BASE_URL \
  PROPERTY_LOCAL_ENV=off \
  ANTHROPIC_API_KEY= ANTHROPIC_AUTH_TOKEN= TYPESAFE_API_KEY= \
  APP_MODE=demo WORKFLOW_MODE=native_local WORKFLOW_TARGET_WORLD=local \
  DATABASE_URL="sqlite:///$property_ui_dir/application.db" \
  WORKFLOW_LOCAL_DATA_DIR="$property_ui_dir/native-world" \
  .venv/bin/python -m uvicorn app.main:app \
  --host 127.0.0.1 --port 8017 --workers 1
```

Keep the printed directory if you want to resume this demo. Reuse the same `property_ui_dir` and run the server command again; repeating `mktemp` creates another empty store. Native local timers need the process to remain running. Use one worker without `--reload`.

The committed dashboard is available directly at [http://127.0.0.1:8017/dashboard](http://127.0.0.1:8017/dashboard). To develop it with hot reload, use a second terminal from the repository root:

```sh
cd web
npm ci
npm run dev -- --host 127.0.0.1 --port 5199 --strictPort
```

Open [the staff dashboard](http://127.0.0.1:5199). The original interface for the same isolated backend is at [http://127.0.0.1:8017](http://127.0.0.1:8017).

The development proxy in [vite.config.ts](vite.config.ts) sends `/api` requests to port **8017** and rewrites the outgoing origin to the backend's origin. Keep both servers on loopback. This is local development configuration, not a production authentication or deployment setup. The production build writes `static/dashboard/`, served by FastAPI at `/dashboard`; commit that rebuilt bundle alongside source changes. `VITE_ORIGINAL_WORKSPACE_URL` can change the link to the original interface; its default is `http://127.0.0.1:8017/` in development and `/` in the FastAPI-served build. It does not change the API proxy target.

Without provider credentials, case reading that requires a model remains unavailable or needs manual triage. That is expected in an offline UI check. Follow the root README if you intentionally want to configure model access; disabling `.env.local` and clearing existing credential variables are both necessary for an offline run.

## What the interface supports

- A searchable staff queue, status filters and an explicit refresh action. Stopped actions and cases needing a human appear ahead of other work.
- A selected case's original evidence, current proposed action, policy checks, outstanding reviews and activity.
- Review responses with an explicit reason: request evidence, verify an existing supported source assertion, wait until a deadline, reject an action or confirm an eligible interpretation. The selected demo role must own the review; the backend validates the response. Scoped authority, finance and custom-rule approvals use the original staff workspace.
- The published policy loaded from the backend, supported plain-English interpretation, saved drafts, impact previews and explicit publication by a policy editor. Guided controls cover access escalation, spending review, approval validity, follow-up timing, tenant-message review and model-interpretation acceptance. Additional rules can be removed from a draft; publication still requires a preview. Other settings are preserved.
- Explicit **Reassess with current policy** for a selected case awaiting a policy change. Supported staff roles can rerun its checks through the existing evaluation API; the result shows the policy version and remaining blockers. Reassessment grants no permission. If every requirement passes, the workflow can continue with simulated actions.
- Held message drafts with edit, simulated send and rejection/redraft controls, plus explicit due-timer checks. These require the selected case-manager role.
- Optional policy wording after a saved review, including the recorded reason and review ID. It opens the policy interpreter and follows the same draft and publication process; it cannot silently become a recurring permission.
- **Portfolio** adds related incidents, evidence comparison, tentative visit planning, property/asset history, recorded decision playback and saved-policy comparisons. The [workspace guide](../docs/PORTFOLIO_WORKSPACE.md) explains each flow. Profiles, incident decisions and plans require the property manager role; policy comparison requires the policy editor role.

The stage display describes the current action's evidence and decision state. A completed quote request or simulated action does not prove the repair is complete. An approval records a scoped decision; it does not contact or assign a contractor.

## Demo controls and data

Opening the dashboard creates a local demo session if no session exists, but does not import cases or submit review responses. Use the labelled demo-case action to import the selected chronological BUILD prefixes. Import failures are shown; the application does not manufacture blocked examples by automatically rejecting reviews.

Only the authorised BUILD cases may be used for development or UI examples. Do not load reserved evaluation cases into this interface. Imports use the chosen history prefix, and must not expose later outcomes as evidence available at intake.

Changing the demo role changes the backend session. It is useful for reviewing the different permissions, but it is not real login. Review decisions, policy drafts, publications and explicit reassessments are genuine writes to the connected local store. Use an isolated demo database and workflow directory, not the shared default store or production data.

External operational actions remain simulated. The dashboard does not send contractor messages, make bookings or payments, or provide a voice interface; backend voice intake adapters are documented separately.

## Checks

Run from `web/`:

```sh
npm run build
npm run lint
node --experimental-strip-types --test src/lib/pipeline.test.ts
node --experimental-strip-types --test src/lib/portfolio-api.test.ts
```

The build checks TypeScript and writes assets to `../static/dashboard/`. Lint checks source rules. These checks do not verify browser interactions, backend authorisation, model availability or a deployed Vercel workflow.

For a browser check, use the isolated backend above. Check an empty queue before explicitly loading examples, search and filter without losing the selected case, inspect a review's sources, and confirm that an unsupported or unauthorised response remains blocked. For policies, inspect interpretation, draft saving, preview and publication separately. A successful draft save must not be presented as a published policy. After publication, select a case marked as awaiting the new policy, reassess it explicitly and confirm that unrelated evidence and permission blockers remain visible.

## Current limits

- Tenant intake remains in the original static interface. React does not include a tenant/staff view switch, tenant conversation or voice flow.
- Demo role selection is not production staff login or tenant isolation.
- Policy interpretation supports the backend's rule vocabulary. Additional rules are readable, but React does not have a general structured rule builder. The policy flow does not execute arbitrary instructions or generate code from a human decision.
- Case ownership, contractor assignment and verified physical repair completion must not be inferred from a review button or action status.
- The dashboard refreshes after its own case actions, on explicit refresh and every 20 seconds while visible. It pauses automatic refresh after three failures and keeps the last loaded data visible. This is periodic fetching, not a live event stream.
- Cases, Policies and Portfolio remain mounted after their first visit to preserve selections and unsaved forms while switching workspaces. Evidence/playback panels reload their snapshot when switched. This is page-memory state, not storage across reloads.
- Contractor availability and case planning windows are staff-entered. Tentative plans check trade, window and slot conflicts but do not optimise routes or verify travel time. Property history uses explicit staff grouping rather than inferring a building from a map pin.
- The interpreter records source-review provenance in the editable draft reason; published policy has no separate structured source-review field.
- FastAPI serves the committed React build, but hosted Vercel operation and production identity remain unverified. External operational adapters are still simulated.
