# Local verification — 10 October 2026

The completed test run passed **71 tests in 14.81 seconds**, with one upstream Starlette/AnyIO deprecation warning. The command was `.venv/bin/python -m pytest -q`. SHA-256 hashes of application, static, test, dependency and deployment configuration files were captured immediately before and after the run; **none changed during that run**. The exact output and source hash manifest are saved in `var/final-test-output.txt` and `var/final-test-manifest.json`.

## Evidence obtained

- Real native Python SDK execution: start, step replay, typed hook resume, timer execution/cancellation, coordinator ownership and restart recovery. The SDK's local world and embedded queue were used, not a replacement workflow simulator. FastAPI integration tests also exercise native intake, new evidence while a review is pending, review/dispatch and restart across interpreter processes.
- Policy/application regressions: simultaneous blockers, scoped and changed-cost approval, explicit access refusal, material source conflict, missing evidence, partial closure, expired/wrong-role/duplicate responses, policy preview/publication/reassessment, completed-action history, finite numeric totals, canonical proposal scope, intake/evidence/action idempotency and uncertain-result reconciliation.
- `node --check static/app.js` passed. Dashboard render functions were exercised against actual API data in a Node VM.
- A browser-rendered local UI check on isolated storage created one fictional dishwasher quote case, observed one automatically recorded simulated action with no outstanding review, switched to the policy-editor demonstration role, changed the missing-access route, tested the draft and published version 2. The case and policy layouts were inspected in screenshots. The browser ran in the background because a subagent cannot show an in-app browser tab in the user's foreground window.
- BUILD replay validated all 58 supplied file hashes and assessed the first event of all 25 allowed cases with no adapter actions. All first-event snapshots remained at human review because the supplied chronological source did not establish all trusted mapping requirements. This is not an accuracy measurement. A selected BUILD 013 prefix through event 002 also replayed successfully. Reports are in `var/build-replay-first-events.json` and `var/build-replay-013-through-002.json`.

## Runtime isolation and limits

The initial shared default database unexpectedly included another task's reserved evaluation record; the dashboard auto-displayed it. That server was stopped and those contents were not used to change policy, implementation or tests. The incident and its limits are documented in `BUILD_REPLAY_BOUNDARY.md`. The final browser check used separate `var/build-only-ui-20261010.db` and `var/build-only-ui-world-20261010` storage. Existing shared records were not deleted.

No hosted Vercel execution, cloud database, production login, live model call, message delivery, physical access, contractor booking, payment or physical repair was tested or performed. All action receipts are labelled simulations. Local SDK persistence/replay is proof of local native execution, not proof of cloud execution. See `WORKFLOW_RUNTIME.md` and `README.md` for setup and remaining production integrations.

## Documentation and screenshot update check

On 10 October 2026, a fresh `.venv/bin/python -m pytest -q` run passed **132 tests in 12.74 seconds**, with one Starlette/AnyIO deprecation warning. `node --check static/app.js` and `git diff --check` also passed. This result covers the local source checked for the documentation and screenshot update; it does not establish cloud deployment, PostgreSQL behaviour, live model accuracy or external delivery.

The exact staged application snapshot was also exported to temporary storage and checked independently: **132 tests passed in 13.02 seconds**, JavaScript syntax passed, and the Git index remained unchanged during that run. Subsequent README edits only supplied the verified repository and support links.

Real browser captures show a fictional tenant report, the two resulting staff reviews and an unsaved access-policy interpretation. They use separate SQLite and native Workflow storage with literal interpretation. The images are embedded in `README.md` and `ARCHITECTURE.md`; their hashes and capture limits are recorded in `docs/screenshots/capture-notes.json`. No reserved dataset content or live operational service was used for these captures.
