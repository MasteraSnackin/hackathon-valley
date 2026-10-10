"""Native Python Vercel Workflow orchestration; application state lives in service.

The hook transports wake notifications, never authority or the source event itself.
Intake must commit its event and recovery record before calling these helpers.
"""

from __future__ import annotations

import asyncio
import os
from contextlib import asynccontextmanager, suppress
from typing import Literal

from pydantic import AwareDatetime, BaseModel, ConfigDict, Field
from vercel import workflow


wf = workflow.Workflows(
    sandbox_policy=workflow.SandboxPolicy(share_sandboxes=True),
)

# Server-side lifecycle state; never read by the replayed workflow body.
_local_runtime_owner = None


class CaseSignal(BaseModel, workflow.BaseHook):
    """A committed event is available; all substantive data is loaded in a step."""

    model_config = ConfigDict(extra="forbid", strict=True)
    case_id: str = Field(min_length=1, max_length=100, pattern=r"^[A-Za-z0-9_-]+$")
    event_id: str = Field(min_length=1, max_length=200)
    revision: int = Field(ge=0)
    kind: Literal["case_changed"] = "case_changed"


class CycleResult(BaseModel):
    """Validated service boundary. Naive deadlines are rejected, not guessed."""

    model_config = ConfigDict(extra="forbid")
    terminal: bool = Field(strict=True)
    next_wake_at: AwareDatetime | None
    revision: int = Field(ge=0, strict=True)


def case_hook_token(case_id: str) -> str:
    # Apply the same validation to starts and resumes, without reading a database
    # in the deterministic workflow body.
    CaseSignal(case_id=case_id, event_id="token-validation", revision=0)
    return f"property-case:{case_id}"


@wf.step(max_retries=3)
async def run_case_cycle(case_id: str) -> dict:
    """A fresh durable step per wake, not a replayed previous policy assessment.

    service.coordinator_cycle must transactionally drain ordered committed events,
    check current policy/authority and deduplicate action intents. Native step
    retries may call this function again after its transaction has committed.
    """
    from app.service import coordinator_cycle

    result = await asyncio.to_thread(coordinator_cycle, case_id)
    return CycleResult.model_validate(result).model_dump(mode="json")


async def _receive_signal(hook: workflow.HookEvent[CaseSignal]) -> CaseSignal:
    return await hook


@wf.workflow
async def case_coordinator(*, case_id: str) -> dict:
    """One ordered case consumer, with one persistent receive and native timers."""
    async with CaseSignal.wait(token=case_hook_token(case_id)) as hook:
        # 0.11.1's native conflict awaiter establishes the token claim before the
        # first application step. This also closes the pre-registration race:
        # an event signalled too early is already in the committed event store.
        existing = await hook.get_conflict()
        if existing is not None:
            return {"case_id": case_id, "status": "existing_coordinator", "run_id": existing.run_id}

        receiver = asyncio.create_task(_receive_signal(hook))
        timer = None
        try:
            while True:
                state = CycleResult.model_validate(await run_case_cycle(case_id))
                if state.terminal:
                    return {"case_id": case_id, "status": "terminal", "revision": state.revision}

                # A signal can arrive while the database step is executing. Its
                # revision is a hint only; rerun the ordered consumer even when
                # a duplicated signal refers to an older revision.
                if not receiver.done() and state.next_wake_at is not None:
                    timer = asyncio.create_task(workflow.sleep(state.next_wake_at))
                    try:
                        await asyncio.wait({receiver, timer}, return_when=asyncio.FIRST_COMPLETED)
                        if timer.done():
                            timer.result()  # Do not hide a failed durable timer.
                    finally:
                        if not timer.done():
                            timer.cancel()
                            with suppress(asyncio.CancelledError):
                                await timer
                        timer = None
                elif not receiver.done():
                    await receiver

                if receiver.done():
                    receiver.result()  # Preserve typed-hook validation errors.
                    receiver = asyncio.create_task(_receive_signal(hook))
                # On a timer wake the same receive remains pending. Cancelling
                # and replacing it could consume a simultaneous message twice
                # or leave two hook consumers competing for the next payload.
        finally:
            receiver.cancel()
            with suppress(asyncio.CancelledError):
                await receiver


async def start_case_coordinator(case_id: str) -> str:
    """Return an existing live owner or start a native run.

    Call after committing the case/event. Persist the returned run id. The
    native start API has no caller-supplied idempotency key in the pinned SDK;
    concurrent starts converge through the hook claim before any service step.
    """
    token = case_hook_token(case_id)
    try:
        hook = await workflow.get_hook_by_token(token)
    except workflow.HookNotFoundError:
        run = await workflow.start(case_coordinator, case_id=case_id)
        return run.run_id
    return hook.run_id


async def signal_case_event(case_id: str, event_id: str, revision: int) -> dict:
    """Wake an existing run. A transport receipt does not mean event processing.

    Hook absence is recoverable, including immediately after native start. Keep
    the committed event/outbox pending; a fresh cycle reads it after registration.
    Other runtime errors propagate so callers cannot report false success.
    """
    signal = CaseSignal(case_id=case_id, event_id=event_id, revision=revision)
    try:
        hook = await signal.resume(case_hook_token(case_id))
    except workflow.HookNotFoundError:
        return {"status": "pending", "reason": "hook_not_ready", "run_id": None}
    return {"status": "signalled", "run_id": hook.run_id}


def validate_runtime_mode(mode: str) -> None:
    """Reject an application mode that mislabels the SDK's selected runtime.

    The SDK creates its World when the workflow registry is imported, and an
    unknown WORKFLOW_TARGET_WORLD otherwise silently selects its local World.
    Set environment before importing this module; changing it later cannot
    change the registry's queue handlers safely.
    """
    if mode not in {"manual_demo", "native_local", "native_cloud"}:
        raise ValueError("WORKFLOW_MODE must be manual_demo, native_local or native_cloud")
    if mode == "manual_demo":
        return
    if os.getenv("WORKFLOW_TARGET_WORLD") not in {None, "", "local", "vercel"}:
        raise ValueError("WORKFLOW_TARGET_WORLD must be local or vercel")

    from vercel.workflow._internal.world import get_world
    from vercel.workflow._internal.worlds.local import LocalWorld
    from vercel.workflow._internal.worlds.vercel import VercelWorld

    world = get_world()
    if mode == "native_local":
        if not isinstance(world, LocalWorld):
            raise RuntimeError("native_local requires WORKFLOW_TARGET_WORLD=local before application import")
        if world._queue_mode != "embedded":
            raise RuntimeError("native_local requires the embedded queue; unset VERCEL_QUEUE_BASE_URL")
    elif not isinstance(world, VercelWorld):
        raise RuntimeError("native_cloud requires WORKFLOW_TARGET_WORLD=vercel and configured Vercel credentials")


@asynccontextmanager
async def native_runtime_lifespan():
    """Own the SDK's embedded queue in the ASGI lifespan task, when local.

    0.11.1 has no public World lifecycle API. This small, version-guarded adapter
    supplies the SDK's own public embedded Queue service to its local World;
    it does not implement an alternative scheduler. This application supports
    embedded local mode only here; hosted mode owns its own queue lifecycle.
    """
    from importlib.metadata import version
    import fcntl

    from vercel.queue.embedded import embedded_queue_service
    from vercel.workflow._internal.world import get_world
    validate_runtime_mode("native_local")
    world = get_world()
    if version("vercel-workflow") != "0.11.1":
        raise RuntimeError("Revalidate the native local lifecycle adapter before upgrading vercel-workflow")
    if world._queue_client is not None:
        raise RuntimeError("Start the native local runtime lifespan before starting or resuming any workflow")
    world.data_dir.mkdir(parents=True, exist_ok=True)
    with (world.data_dir / ".property-runtime.lock").open("a") as lock:
        try:
            fcntl.flock(lock, fcntl.LOCK_EX | fcntl.LOCK_NB)
        except BlockingIOError:
            raise RuntimeError("Another process already owns this native local workflow directory") from None
        global _local_runtime_owner
        try:
            async with embedded_queue_service() as service:
                world._embedded_queue_service = service
                world._queue_client = service.get_async_client()
                _local_runtime_owner = asyncio.current_task()
                yield
        finally:
            _local_runtime_owner = None
            world._queue_client = None
            world._embedded_queue_service = None
            fcntl.flock(lock, fcntl.LOCK_UN)


async def recover_local_case_steps(case_id: str) -> dict:
    """Redeliver unfinished native steps at exclusive local application startup.

    Call from the native_runtime_lifespan owner's task before the case's normal
    wake. Pinned SDK internals queue an existing native invocation; this never
    invents completion records, rewrites history or resets retry attempts.
    """
    from datetime import UTC, datetime
    from importlib.metadata import version
    from vercel.workflow._internal import world as native
    from vercel.workflow._internal.worlds.local import LocalWorld

    world = native.get_world()
    if not isinstance(world, LocalWorld) or world._queue_mode != "embedded":
        return {"status": "not_local", "step_ids": []}
    if version("vercel-workflow") != "0.11.1":
        raise RuntimeError("Revalidate native local step recovery before upgrading vercel-workflow")
    if _local_runtime_owner is None or asyncio.current_task() is not _local_runtime_owner:
        raise RuntimeError("Recover local steps only from the exclusive native runtime startup task")
    try:
        hook = await workflow.get_hook_by_token(case_hook_token(case_id))
    except workflow.HookNotFoundError:
        return {"status": "no_live_hook", "step_ids": []}
    run = await world.runs_get(hook.run_id)
    if run.workflow_name != case_coordinator.workflow_id:
        raise RuntimeError("Case hook belongs to an unexpected workflow; recovery refused")
    if run.status in {"completed", "failed", "cancelled"}:
        return {"status": "terminal", "run_id": hook.run_id, "step_ids": []}
    namespace = (run.execution_context or {}).get("queueNamespace")
    if namespace != wf.namespace:
        raise RuntimeError("Case workflow queue namespace differs from the registered application")
    events = await world.events_list(hook.run_id)
    step_ids = list(dict.fromkeys(e.correlation_id for e in events.data if e.event_type == "step_created"))
    requeued = []
    for step_id in step_ids:
        step = await world.steps_get(hook.run_id, step_id)
        if step.status in {"completed", "failed"}:
            continue
        if step.step_name != run_case_cycle.name:
            raise RuntimeError("Recovery encountered an unrecognised case coordinator step")
        at = datetime.now(UTC)
        retry_at = getattr(step, "retry_after", None)
        delay = max(0, (retry_at - at).total_seconds()) if retry_at else None
        await world.queue(
            native.get_queue_name(run.workflow_name, namespace),
            native.WorkflowInvokePayload(run_id=hook.run_id, step_id=step_id,
                                         step_name=step.step_name, requested_at=at),
            idempotency_key=step_id,
            delay_seconds=min(delay, 82800) if delay is not None else None,
        )
        requeued.append(step_id)
    return {"status": "requeued" if requeued else "not_needed", "run_id": hook.run_id,
            "step_ids": requeued, "sdk_version": "0.11.1"}


__all__ = ["wf", "CaseSignal", "case_coordinator", "case_hook_token", "start_case_coordinator", "signal_case_event", "native_runtime_lifespan", "validate_runtime_mode", "recover_local_case_steps"]
