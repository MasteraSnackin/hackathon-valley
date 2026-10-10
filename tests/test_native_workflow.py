"""Contract tests and a real native-SDK local-world smoke run.

The subprocess isolates the SDK registry, embedded queue and sandbox. It uses
the real app coordinator but a controlled service double; it is not cloud proof.
"""

from __future__ import annotations

import asyncio
from datetime import UTC, datetime, timedelta
import json
import os
from pathlib import Path
import subprocess
import sys
import types

import pytest
from pydantic import ValidationError


def test_hook_payload_rejects_untyped_or_extra_authority():
    from app.workflows import CaseSignal

    with pytest.raises(ValidationError):
        CaseSignal(case_id="002", event_id="event-1", revision="1")
    with pytest.raises(ValidationError):
        CaseSignal(case_id="002", event_id="event-1", revision=1, approved=True)


def test_cycle_requires_timezone_aware_deadline():
    from app.workflows import CycleResult

    with pytest.raises(ValidationError):
        CycleResult(terminal=False, next_wake_at="2026-10-12T09:00:00", revision=1)
    result = CycleResult(terminal=False, next_wake_at="2026-10-12T09:00:00+01:00", revision=1)
    assert result.next_wake_at.utcoffset() == timedelta(hours=1)


def test_signal_before_hook_is_retained_as_pending(monkeypatch):
    from app import workflows
    from vercel import workflow

    async def absent(self, token):
        assert token == "property-case:002"
        raise workflow.HookNotFoundError(token=token)

    monkeypatch.setattr(workflows.CaseSignal, "resume", absent)
    assert asyncio.run(workflows.signal_case_event("002", "event-1", 1)) == {
        "status": "pending", "reason": "hook_not_ready", "run_id": None,
    }


def test_transport_failure_is_not_reported_as_success(monkeypatch):
    from app import workflows

    async def failed(self, token):
        raise ConnectionError("unavailable")

    monkeypatch.setattr(workflows.CaseSignal, "resume", failed)
    with pytest.raises(ConnectionError):
        asyncio.run(workflows.signal_case_event("002", "event-1", 1))


def test_start_reuses_a_registered_coordinator(monkeypatch):
    from app import workflows

    async def existing(token):
        assert token == "property-case:002"
        return types.SimpleNamespace(run_id="existing-run")

    monkeypatch.setattr(workflows.workflow, "get_hook_by_token", existing)
    assert asyncio.run(workflows.start_case_coordinator("002")) == "existing-run"


def test_real_native_coordinator_steps_hooks_timers_and_competing_start(tmp_path):
    env = dict(os.environ)
    env["WORKFLOW_TARGET_WORLD"] = "local"
    env["WORKFLOW_LOCAL_DATA_DIR"] = str(tmp_path / "native-events")
    # The native smoke must never inherit a queue endpoint from another app.
    env.pop("VERCEL_QUEUE_BASE_URL", None)
    project = Path(__file__).resolve().parents[1]
    result = subprocess.run(
        [sys.executable, "-c", "import runpy; runpy.run_path('tests/test_native_workflow.py', run_name='__main__')"],
        cwd=project, env=env, capture_output=True, text=True, timeout=40,
    )
    assert result.returncode == 0, result.stdout + result.stderr
    evidence = json.loads(next(line for line in result.stdout.splitlines() if line.startswith('{"native_smoke"')))
    assert evidence["native_smoke"] == "passed"
    assert evidence["cycle_count"] == 4
    assert {"hook_created", "hook_received", "wait_created", "wait_completed", "step_completed", "run_completed"} <= set(evidence["event_types"])


@pytest.mark.parametrize("scenario", ["hook", "timer"])
def test_native_replays_after_process_restart(tmp_path, scenario):
    env = dict(os.environ)
    env["WORKFLOW_TARGET_WORLD"] = "local"
    env["WORKFLOW_LOCAL_DATA_DIR"] = str(tmp_path / "native-events")
    env["PROPERTY_NATIVE_SMOKE_SCENARIO"] = scenario
    env.pop("VERCEL_QUEUE_BASE_URL", None)
    for phase in ("start", "resume"):
        env["PROPERTY_NATIVE_SMOKE_PHASE"] = phase
        result = subprocess.run(
            [sys.executable, "-c", "import runpy; runpy.run_path('tests/test_native_workflow.py', run_name='__main__')"],
            cwd=Path(__file__).resolve().parents[1], env=env,
            capture_output=True, text=True, timeout=30,
        )
        assert result.returncode == 0, result.stdout + result.stderr
        assert f'"restart_phase": "{phase}"' in result.stdout
    evidence = json.loads((tmp_path / "restart-state.json").read_text())
    assert evidence["cycle_count"] == (3 if scenario == "timer" else 2)
    assert evidence["result"]["status"] == "terminal"
    if scenario == "timer":
        assert evidence["wait_count"] == 2
        assert evidence["completed_wait_count"] == 1


def test_runtime_modes_cannot_silently_select_a_different_world(monkeypatch, tmp_path):
    from app import workflows
    from vercel.workflow._internal import world
    from vercel.workflow._internal.worlds.local import LocalWorld
    from vercel.workflow._internal.worlds.vercel import VercelWorld

    monkeypatch.setenv("WORKFLOW_LOCAL_DATA_DIR", str(tmp_path))
    monkeypatch.delenv("VERCEL_QUEUE_BASE_URL", raising=False)
    monkeypatch.setenv("WORKFLOW_TARGET_WORLD", "local")
    local = LocalWorld()
    monkeypatch.setattr(world, "get_world", lambda: local)
    workflows.validate_runtime_mode("native_local")
    with pytest.raises(RuntimeError, match="native_cloud requires"):
        workflows.validate_runtime_mode("native_cloud")
    with pytest.raises(ValueError, match="WORKFLOW_MODE"):
        workflows.validate_runtime_mode("typo")
    monkeypatch.setenv("WORKFLOW_TARGET_WORLD", "typo")
    with pytest.raises(ValueError, match="WORKFLOW_TARGET_WORLD"):
        workflows.validate_runtime_mode("native_local")
    workflows.validate_runtime_mode("manual_demo")

    monkeypatch.setenv("WORKFLOW_TARGET_WORLD", "local")
    local._queue_mode = "external"
    with pytest.raises(RuntimeError, match="unset VERCEL_QUEUE_BASE_URL"):
        workflows.validate_runtime_mode("native_local")

    # Construct no network client and load no credentials: only the selected
    # runtime's class identity is needed for this configuration guard.
    cloud = object.__new__(VercelWorld)
    monkeypatch.setattr(world, "get_world", lambda: cloud)
    workflows.validate_runtime_mode("native_cloud")
    with pytest.raises(RuntimeError, match="native_local requires"):
        workflows.validate_runtime_mode("native_local")


async def _restart_smoke(phase):
    from app import workflows
    from vercel import workflow

    state_path = Path(os.environ["WORKFLOW_LOCAL_DATA_DIR"]).parent / "restart-state.json"
    state = json.loads(state_path.read_text()) if state_path.exists() else {"cycle_count": 0}
    timer_scenario = os.getenv("PROPERTY_NATIVE_SMOKE_SCENARIO") == "timer"
    final_cycle = 3 if timer_scenario else 2
    event_dir = Path(os.environ["WORKFLOW_LOCAL_DATA_DIR"]) / "events"

    def coordinator_cycle(case_id):
        assert case_id == "002"
        state["cycle_count"] += 1
        number = state["cycle_count"]
        deadline = None
        if timer_scenario and number < final_cycle:
            deadline = (datetime.now(UTC) + timedelta(seconds=60 if number == 1 else 0.1)).isoformat()
        return {"terminal": number == final_cycle, "next_wake_at": deadline, "revision": number}

    service_double = types.ModuleType("app.service")
    service_double.coordinator_cycle = coordinator_cycle
    sys.modules["app.service"] = service_double
    if phase == "start":
        state["run_id"] = await workflows.start_case_coordinator("002")

        async def settled_first_cycle():
            expected_event = "wait_created" if timer_scenario else "step_completed"
            while not any(json.loads(p.read_text())["eventType"] == expected_event for p in event_dir.glob(f'{state["run_id"]}-*.json')):
                await asyncio.sleep(0.01)

        await asyncio.wait_for(settled_first_cycle(), timeout=10)
        assert state["cycle_count"] == 1
    else:
        # Startup must actively wake every live case: persisted native events
        # survive, while an old embedded queue's delayed deliveries do not.
        assert await workflows.start_case_coordinator("002") == state["run_id"]
        receipt = await workflows.signal_case_event("002", "committed-after-restart", 2)
        assert receipt == {"status": "signalled", "run_id": state["run_id"]}
        state["result"] = await asyncio.wait_for(workflow.Run(state["run_id"]).return_value(), timeout=10)
        assert state["cycle_count"] == final_cycle  # Completed step 1 was replayed, not rerun.
        events = [json.loads(p.read_text())["eventType"] for p in event_dir.glob(f'{state["run_id"]}-*.json')]
        assert events.count("step_completed") == final_cycle
        state["wait_count"] = events.count("wait_created")
        state["completed_wait_count"] = events.count("wait_completed")
    state_path.write_text(json.dumps(state))
    print(json.dumps({"restart_phase": phase, "cycle_count": state["cycle_count"]}))


async def _native_smoke():
    # Imported only in the isolated subprocess, before the real workflow runs.
    # Steps run outside the replay sandbox and use this controlled service.
    from app import workflows
    from vercel import workflow

    first_cycle = asyncio.Event()
    second_cycle = asyncio.Event()
    loop = asyncio.get_running_loop()
    calls = []

    def coordinator_cycle(case_id):
        assert case_id == "002"
        calls.append(case_id)
        number = len(calls)
        if number == 1:
            loop.call_soon_threadsafe(first_cycle.set)
            return {"terminal": False, "next_wake_at": None, "revision": 1}
        if number == 2:
            loop.call_soon_threadsafe(second_cycle.set)
            return {"terminal": False, "next_wake_at": (datetime.now(UTC) + timedelta(seconds=60)).isoformat(), "revision": 2}
        if number == 3:
            return {"terminal": False, "next_wake_at": (datetime.now(UTC) + timedelta(seconds=0.1)).isoformat(), "revision": 3}
        return {"terminal": True, "next_wake_at": None, "revision": 4}

    service_double = types.ModuleType("app.service")
    service_double.coordinator_cycle = coordinator_cycle
    sys.modules["app.service"] = service_double

    missing = await workflows.signal_case_event("002", "before-start", 1)
    assert missing["status"] == "pending"
    run_id = await workflows.start_case_coordinator("002")
    await asyncio.wait_for(first_cycle.wait(), timeout=10)

    # Force the race route past the helper's lookup. The duplicate must acquire
    # no application cycle, and reports the live owner's native run id.
    duplicate = await workflow.start(workflows.case_coordinator, case_id="002")
    duplicate_result = await asyncio.wait_for(duplicate.return_value(), timeout=10)
    assert duplicate_result == {"case_id": "002", "status": "existing_coordinator", "run_id": run_id}
    assert len(calls) == 1

    receipt = await workflows.signal_case_event("002", "committed-event-2", 2)
    assert receipt == {"status": "signalled", "run_id": run_id}
    await asyncio.wait_for(second_cycle.wait(), timeout=10)
    event_dir = Path(os.environ["WORKFLOW_LOCAL_DATA_DIR"]) / "events"

    async def wait_for_timer_registration():
        while not any(json.loads(p.read_text())["eventType"] == "wait_created" for p in event_dir.glob(f"{run_id}-*.json")):
            await asyncio.sleep(0.01)

    await asyncio.wait_for(wait_for_timer_registration(), timeout=10)
    # The next signal cancels the long timer. The following short timer fires
    # with a receiver still pending; both branches use the real SDK runtime.
    await workflows.signal_case_event("002", "committed-event-3", 3)
    result = await asyncio.wait_for(workflow.Run(run_id).return_value(), timeout=10)
    assert result == {"case_id": "002", "status": "terminal", "revision": 4}
    assert len(calls) == 4
    events = []
    for path in event_dir.glob(f"{run_id}-*.json"):
        record = json.loads(path.read_text())
        events.append(record["eventType"])
    print(json.dumps({"native_smoke": "passed", "run_id": run_id, "cycle_count": len(calls), "event_types": sorted(set(events))}))


async def _smoke_with_lifespan():
    from app.workflows import native_runtime_lifespan

    async with native_runtime_lifespan():
        if phase := os.getenv("PROPERTY_NATIVE_SMOKE_PHASE"):
            await _restart_smoke(phase)
        else:
            await _native_smoke()


if __name__ == "__main__":
    asyncio.run(_smoke_with_lifespan())
