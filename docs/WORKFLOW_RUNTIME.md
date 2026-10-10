# Native Python Workflow runtime

Checked on 10 October 2026 against the [official Python guide](https://workflow-sdk.dev/docs/getting-started/python), the [published package](https://pypi.org/project/vercel-workflow/0.11.1/) and the installed `vercel-workflow==0.11.1` source. The Python SDK is beta. This project targets Python 3.12 (`>=3.12,<3.13` in `pyproject.toml`) and pins the SDK rather than assuming future beta versions have the same behaviour.

## Execution boundary

`app.workflows:wf` is an actual `vercel.workflow.Workflows` registry. `case_coordinator` is registered with `@wf.workflow`; `run_case_cycle` is registered with `@wf.step`. Typed `CaseSignal` instances resume a native `BaseHook`, and absolute aware datetimes go to `workflow.sleep`. The native SDK records and replays its own events. The application database stores case evidence and policy state; it is not a replacement workflow scheduler.

The SDK's local World uses native Workflow replay and an embedded Queue service. Local execution is real SDK execution, with a development queue in this process. It is not a Vercel cloud deployment. Workflow events persist in `WORKFLOW_LOCAL_DATA_DIR`; the embedded delivery queue is in memory. Keep the application database and the workflow directory together when restarting the demonstration.

Vercel cloud execution has not been verified by these tests. SQLite on a local machine is useful for the demonstration but cannot serve as a shared production case store across isolated serverless steps. Deployment needs a shared transactional database, durable attachment storage, access control, configured runtime identity and cloud acceptance checks before it can be described as operational.

## Coordinator and application contract

The coordinator acquires `property-case:{case_id}` before its first application step. The pinned SDK's native `hook.get_conflict()` confirms that registration. If a competing run already holds the token, the new run returns that owner's ID before executing any application cycle. A hook remains registered through steps and timers, so there is one event consumer for the case, including while human reviews are open.

The application supplies a synchronous function:

```python
def coordinator_cycle(case_id: str) -> dict:
    return {
        "terminal": False,
        "next_wake_at": "2026-10-12T09:00:00+01:00",  # or None
        "revision": 7,
    }
```

The step calls that function in a worker thread. It must use its own database connection/transaction. It must drain committed events in order, deduplicate event IDs, load current authority/policy, reconcile uncertain actions and persist its consumed revision. Step retries can occur after a database transaction committed. A stable business-action ID and transactional intent are therefore still necessary; a workflow retry does not establish exactly-once external effects.

Each wake executes a new step, so an earlier recorded policy decision is not mistaken for a fresh assessment. The service calculates working-hour deadlines and whether the question remains unresolved. The coordinator only waits for the supplied absolute time; a timer never confers consent or approval. Naive datetimes, non-boolean terminal flags and non-integer revisions fail validation.

One receive task survives timer wakes. An incoming event cancels the superseded timer; a timer wake leaves that same receiver waiting. When both complete together, the coordinator handles the wake by loading the database again. Hook payloads carry only case ID, event ID and revision, which are notification hints. They contain no approval authority or executable action. Authentication, reviewer role and approval scope are checked before committing an event and again by the service before action.

## Intake, outbox and recovery

Use the following sequence:

1. Authenticate and validate the incoming event, then commit the event and a pending wake record in one application transaction. Duplicate submissions keep the same event identity.
2. Call `await start_case_coordinator(case_id)` when the case lacks a live owner, and persist the returned run ID. The helper reuses a registered hook when possible. Native `workflow.start` returns after creation/queuing; it does not wait for completion.
3. Call `await signal_case_event(case_id, event_id, revision)`. A `signalled` receipt means the native runtime accepted a wake. A `pending` receipt with `hook_not_ready` means the committed event still requires recovery. Other transport failures propagate.
4. Mark events consumed only through the service's committed processing revision. A successful wake alone is not proof that processing or any proposed action completed.

A signal before hook registration is not lost: the event was committed first, and registration precedes the coordinator's initial cycle. A signal while a cycle is running is buffered by the native hook. An uncertain start can safely be reconciled by looking up the live token: the SDK has no caller-selected start idempotency key, but competing starts cannot both reach the application step while one owns the hook. Record and reconcile run IDs because a redundant run may complete with `existing_coordinator` and the actual owner ID.

On local startup, recover **all active cases**, including cases that have no newly unconsumed event. First call `recover_local_case_steps(case_id)` from the exclusive lifespan task and record its result. Then look up/start the coordinator and send a recovery wake tied to the durable case/recovery record. This causes replay of recorded work followed by a fresh cycle and reconstructs any future timer whose in-memory delivery was lost during process shutdown. Merely recovering cases with new events would miss a previously scheduled timer. Pending wake records also need an explicit recovery path after a transient delivery failure.

A hook wake alone cannot recover an interrupted step when the local queue delivery disappeared after `step_started` but before `step_completed`. The startup helper redelivers the unfinished invocation to the SDK's own executor. The SDK advances its attempt counter, applies retry limits and records the real completion. Recovery never edits history, marks a step completed itself or resets attempts. The application transaction may already have committed, so the service must remain idempotent.

If new evidence arrives just as a case becomes terminal, persist it and its wake first. Reconcile the stored run's terminal status and start a new coordinator when the application permits reopening. A terminal workflow result records the coordinator state; it does not prove that a physical repair has been completed.

## Application lifecycle

Set environment variables before application import. Creating the `Workflows` registry binds queue handlers to the SDK's selected World; changing environment afterwards does not retarget those handlers. Validate the application mode before startup recovery, then own the embedded SDK queue from the FastAPI lifespan task:

```python
from contextlib import asynccontextmanager
from fastapi import FastAPI
from app.workflows import native_runtime_lifespan, validate_runtime_mode, recover_local_case_steps

@asynccontextmanager
async def lifespan(app):
    validate_runtime_mode("native_local")
    async with native_runtime_lifespan():
        for case in get_service().list_cases():
            receipt = await recover_local_case_steps(case["id"])
            record_recovery_receipt(case["id"], receipt)
            await wake(case["id"])
        yield

app = FastAPI(lifespan=lifespan)
```

This sketch uses the application's service, wake and audit functions. It runs before accepting requests. The adapter is a narrow compatibility layer: the SDK exposes the embedded Queue service publicly but has no exported local-World shutdown or interrupted-step recovery interface. It sets the local World's queue client/service references while that official service is open, and clears them after shutdown. A non-blocking POSIX lock on `.property-runtime.lock` prevents a second process from owning the same local workflow directory. Recovery also requires the exact lifespan owner task, so a request handler cannot redeliver a currently executing step. The adapter refuses a different SDK version or an already-started embedded queue. Hosted mode owns its queue lifecycle and does not use this context manager; `recover_local_case_steps` is a no-op outside the embedded local World.

The exact private SDK dependency is `vercel.workflow._internal.world` and `vercel.workflow._internal.worlds.local.LocalWorld`: local mode/client/service fields, `data_dir`, `get_world`, typed `WorkflowInvokePayload`, `get_queue_name`, and native `runs_get`, `events_list`, `steps_get` and `queue` operations. Recovery accepts only this application's registered coordinator, step name and queue namespace. It skips terminal steps and preserves pending retry delays. This is SDK-native redelivery through version-pinned internals, not a public SDK recovery API. Revalidate these adapters and their tests before upgrading the SDK.

The embedded local mode needs no FastAPI queue route: the registry registers its subscriber directly with the SDK. The application rejects a `VERCEL_QUEUE_BASE_URL` in `native_local` mode: the SDK would select an external queue, whose delivery route this application has not configured. Multiple workers, multiple application processes sharing one workflow directory, and hot reload are not supported for this local demonstration.

## Modes and local start

| Application `WORKFLOW_MODE` | Required SDK World | Behaviour |
| --- | --- | --- |
| `manual_demo` | No native execution | Requests and explicit manual ticks run application policy logic; background workflow hooks and timers do not run. |
| `native_local` | Local World with embedded Queue | Real native Python Workflow replay, hooks and timers in one local application process. |
| `native_cloud` | Vercel World | Deployment preparation only; needs configured Vercel runtime identity, generated workflow routes and shared storage. Hosted execution has not been tested. |

`validate_runtime_mode()` rejects unknown application modes, unknown `WORKFLOW_TARGET_WORLD` values and a mode that does not match the actual World. This check verifies selection only; it does not authenticate a cloud account or prove that a deployment works. In 0.11.1 the SDK defaults to Vercel when `VERCEL_DEPLOYMENT_ID` is present, otherwise local. Explicit `WORKFLOW_TARGET_WORLD=local` or `vercel` removes that ambiguity. The SDK itself silently falls back to local for unknown target strings, which is why the application checks them.

From the `property-workflow` directory, after installing its pinned dependencies:

```sh
mkdir -p var
env -u VERCEL_QUEUE_BASE_URL \
  APP_MODE=demo WORKFLOW_MODE=native_local WORKFLOW_TARGET_WORLD=local \
  WORKFLOW_LOCAL_DATA_DIR="$PWD/var/workflow" \
  .venv/bin/python -m uvicorn app.main:app --host 127.0.0.1 --port 8000 --workers 1
```

The command selects a stable workflow event directory. Keep that directory and the application database for restart recovery, and use the same paths on the next start. A copied `.env` file is not automatically loaded by this command: export its intended settings or use an explicitly configured environment loader. Do not set `--reload` or increase the worker count. Closing the process stops all embedded queue deliveries; retained workflow events alone cannot wake a sleeping process. Startup must send the recovery wakes described above.

For deployment preparation, `pyproject.toml` declares:

```toml
[[tool.vercel.workflows]]
entrypoint = "app.workflows:wf"
```

`vercel.json` selects the FastAPI framework. Vercel's build integration generates the workflow routes from this registry. Configuration and manifest generation alone do not prove hosted scheduling, permissions or durability.

## Verification

Run the focused suite with:

```sh
.venv/bin/python -m pytest tests/test_native_workflow.py -q
```

The native subprocess smoke test uses the actual application coordinator and registered step, the installed SDK's local event store and queue, a controlled service double, typed resume and durable absolute timers. It checks early-hook absence, ownership on a competing native start, cancellation of a superseded timer and completion of a later timer. It inspects native event records for step, hook, wait and run completion.

Separate restart scenarios stop the first process after a recorded step, create a new process against the same native event directory, find the original owner and send a recovery hook. The hook-only scenario reaches the next application cycle. The timer scenario starts with a recorded 60-second wait, then the recovery wake causes a fresh service cycle to schedule a new short wait, which completes natively. Both assert that the original completed step is replayed rather than executed a second time; the timer scenario also checks two recorded waits and one completed wait. This proves active recovery after restart, not automatic resurrection of an in-memory queue. These scenarios use a controlled service, so they do not prove that the full application, cloud database or external communications have been exercised. The full application must also verify event ordering, reviewer authorisation, policy changes, action reconciliation and startup recovery.

All test case identifiers come from BUILD case `002`. Tests contact no tenant, landlord or contractor and make no deployment.

Recorded local verification on 10 October 2026: **9 focused tests passed in 8.57 seconds**. The native manifest command, `.venv/bin/python -m vercel.workflow manifest app.workflows:wf --stdout`, recognised `case_coordinator` and `run_case_cycle`. No build, Vercel credentials, hosted routes, hosted scheduling or cloud database were exercised by these checks.

### Actual FastAPI application integration

`tests/test_native_api.py` runs the real FastAPI lifespan, actual service and SQLite store, and native Workflow runtime in two separate interpreter processes. It uses HTTP requests through FastAPI's test client; it does not replace service methods, SDK functions, clocks or steps. The only case source is BUILD `002`, event `001`. Live model credentials are removed from the test environment.

The independent retained check used `var/native-api-check.db` and `var/native-api-world`. It passed intake → committed event/outbox → native cycle checkpoint; new evidence → a higher consumed revision while both existing reviews remained open; and application restart → a fresh checkpoint on the same native run without a new incoming event. No action executed. Native `wait_created` records also confirmed that the new cycle reconstructed its next wake.

The retained run was `wrun_01M4JP1G6K71EMA60D8ABREANP`: consumed revision advanced to `2`, and the checkpoint count advanced from `2` before restart to `3` after restart. Both reviews remained open. These observations demonstrate local application recovery, not Vercel cloud operation or real-world action delivery.

Routine isolated runs use `.venv/bin/python -m pytest tests/test_native_api.py -q`. To retain a separate application check under `var`, run `PROPERTY_NATIVE_API_CHECK_DIR=var .venv/bin/python -m pytest tests/test_native_api.py -q -s`. The test appends a fresh BUILD-derived case when the retained database already exists; it does not erase earlier evidence.

### Evidence, authorised review and automatic simulated dispatch

A second full-application regression in `tests/test_native_api.py` proves the complete supported resumption path. Its request-quote scenario derives only from BUILD `002` event `001`, uses the fictional `DEMO-FLAT-1` directory, and initially withholds the sentence identifying the toilet. This is an explicitly constructed input-only scenario, not a claim that the original historical events occurred in this order.

The initial missing classification blocks dispatch. Supplying the exact source quotation adds an unverified classification claim and a review; it still produces no provider receipt. An access-officer attempt to correct this classification receives HTTP 403. A case-manager correction with the claim ID, evidence source and reason resolves the review. The native coordinator then performs its fresh checks and automatically calls the simulated quote adapter, recording exactly one `simulated_provider_receipt` and one successful business action. The test never calls the manual execute endpoint.

The regression redelivers the same committed-event notification through the actual native hook, rejects a repeated review response with HTTP 409, then restarts the application in another interpreter. The existing run and provider receipt remain the same, and no second receipt or action is created.

Retained verification on 10 October 2026 used `var/native-api-dispatch.db` and `var/native-api-dispatch-world`: native run `wrun_01M4JP6MMNX6GG9YDAS5QBJ0MW`, receipt `4d98772d13be45e091c73e51116020be`, final revision `4`, one provider receipt and one successful action before and after restart. The dedicated regression passed in 1.82 seconds. This verifies automatic simulated dispatch and duplicate prevention for this local application scenario; it does not establish real provider delivery or cloud execution.

### Forced interruption during a native step

`test_native_interrupted_step_redelivery_keeps_one_provider_receipt` establishes the same evidence/review/automatic-dispatch path, then pauses the real application process using `SIGSTOP`. It checks the persisted native step is still `running` and kills that process with `SIGKILL`. A fresh interpreter starts the actual application. The startup helper redelivers the interrupted invocation, and the native executor completes the same step on its next attempt. No application or SDK methods are replaced and no event histories are manufactured.

The retained check in `var/forced-interruption` passed in 1.44 seconds: run `wrun_01M4JPDXYRDJBGVYED8KK147VH`, step `step_01M4JPDXYW0VFFACD8C911GFDM`, attempt `1` → `2`, and unchanged provider receipt `e8a61861722d497c9adcf31f0dd93a06`. The actual interruption state is recorded in `interruption.json`. After recovery there is still exactly one successful business action and one simulated provider receipt. A preserved example of the original gap is under `var/native-recovery-evidence`; it is diagnostic evidence, not the application's normal runtime store.
