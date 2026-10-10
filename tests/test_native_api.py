"""Black-box FastAPI + native Python Workflow + actual application storage test.

Two interpreter processes run the app's real lifespan. There are no service,
step, clock or SDK doubles. Only BUILD 002 event 001 enters intake. Model calls
are disabled, and all application operations use the simulated adapters.
"""

from datetime import UTC, datetime
import json
import os
import select
import signal
from pathlib import Path
import subprocess
import sys
import time


ROOT = Path(__file__).resolve().parents[1]


def test_native_api_intake_evidence_and_restart(tmp_path):
    # An explicit directory retains evidence for the independent local check;
    # routine pytest runs isolate it in pytest's temporary directory.
    output = Path(os.getenv("PROPERTY_NATIVE_API_CHECK_DIR", str(tmp_path))).resolve()
    output.mkdir(parents=True, exist_ok=True)
    env = dict(os.environ)
    env.update({
        "APP_MODE": "demo",
        "AI_MODE": "literal_demo",
        "WORKFLOW_MODE": "native_local",
        "WORKFLOW_TARGET_WORLD": "local",
        "DATABASE_URL": f"sqlite:///{output / 'native-api-check.db'}",
        "WORKFLOW_LOCAL_DATA_DIR": str(output / "native-api-world"),
    })
    # Never inherit live model or external queue routing into this local check.
    env.pop("OPENAI_API_KEY", None)
    env.pop("VERCEL_QUEUE_BASE_URL", None)
    results = []
    for phase in ("intake", "restart"):
        env["PROPERTY_NATIVE_API_PHASE"] = phase
        process = subprocess.run(
            [sys.executable, "-c", "import runpy; runpy.run_path('tests/test_native_api.py', run_name='__main__')"],
            cwd=ROOT, env=env, capture_output=True, text=True, timeout=40,
        )
        assert process.returncode == 0, process.stdout + process.stderr
        result = json.loads(next(line for line in process.stdout.splitlines() if line.startswith('{"native_api"')))
        results.append(result)
        if phase == "intake":
            env["PROPERTY_NATIVE_API_CASE_ID"] = result["case_id"]
            env["PROPERTY_NATIVE_API_RUN_ID"] = result["run_id"]
            env["PROPERTY_NATIVE_API_REVISION"] = str(result["revision"])
            env["PROPERTY_NATIVE_API_EVENT_IDS"] = json.dumps(result["event_ids"])
    assert results[0]["run_id"] == results[1]["run_id"]
    assert results[0]["revision"] == results[1]["revision"]
    print(json.dumps({"native_api": "passed", "phases": results, "storage": str(output)}))


def test_native_evidence_review_dispatch_exactly_once(tmp_path):
    output = Path(os.getenv("PROPERTY_NATIVE_API_CHECK_DIR", str(tmp_path))).resolve()
    output.mkdir(parents=True, exist_ok=True)
    env = dict(os.environ)
    env.update({
        "APP_MODE": "demo", "AI_MODE": "literal_demo", "WORKFLOW_MODE": "native_local", "WORKFLOW_TARGET_WORLD": "local",
        "DATABASE_URL": f"sqlite:///{output / 'native-api-dispatch.db'}",
        "WORKFLOW_LOCAL_DATA_DIR": str(output / "native-api-dispatch-world"),
    })
    env.pop("OPENAI_API_KEY", None)
    env.pop("VERCEL_QUEUE_BASE_URL", None)
    results = []
    for phase in ("dispatch", "dispatch_restart"):
        env["PROPERTY_NATIVE_API_PHASE"] = phase
        process = subprocess.run(
            [sys.executable, "-c", "import runpy; runpy.run_path('tests/test_native_api.py', run_name='__main__')"],
            cwd=ROOT, env=env, capture_output=True, text=True, timeout=40,
        )
        assert process.returncode == 0, process.stdout + process.stderr
        result = json.loads(next(line for line in process.stdout.splitlines() if line.startswith('{"native_api"')))
        results.append(result)
        if phase == "dispatch":
            for key in ("case_id", "run_id", "receipt_id", "review_id", "revision"):
                env["PROPERTY_NATIVE_API_" + key.upper()] = str(result[key])
    assert results[0]["receipt_id"] == results[1]["receipt_id"]
    assert results[0]["run_id"] == results[1]["run_id"]
    assert all(r["provider_receipt_count"] == 1 for r in results)
    print(json.dumps({"native_api": "passed", "scenario": "evidence_review_dispatch", "phases": results, "storage": str(output)}))


def test_native_interrupted_step_redelivery_keeps_one_provider_receipt(tmp_path):
    """Kill a real process with a native step still running, then recover it.

    No histories are fabricated and no application/runtime functions are
    replaced. SIGSTOP lets the test verify the interruption point before kill.
    """
    output = Path(os.getenv("PROPERTY_NATIVE_API_CHECK_DIR", str(tmp_path))).resolve() / "forced-interruption"
    output.mkdir(parents=True, exist_ok=True)
    env = dict(os.environ)
    env.update({
        "APP_MODE": "demo", "AI_MODE": "literal_demo", "WORKFLOW_MODE": "native_local",
        "WORKFLOW_TARGET_WORLD": "local", "DATABASE_URL": f"sqlite:///{output / 'case.db'}",
        "WORKFLOW_LOCAL_DATA_DIR": str(output / "world"), "PROPERTY_NATIVE_API_PHASE": "dispatch_interrupt",
    })
    env.pop("OPENAI_API_KEY", None)
    env.pop("VERCEL_QUEUE_BASE_URL", None)
    command = [sys.executable, "-c", "import runpy; runpy.run_path('tests/test_native_api.py', run_name='__main__')"]
    process = subprocess.Popen(command, cwd=ROOT, env=env, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
    interrupted = None
    try:
        assert select.select([process.stdout], [], [], 25)[0], "Application did not reach the interruption scenario"
        line = process.stdout.readline()
        assert line.startswith('{"native_api"'), line + (process.stderr.read() if process.poll() is not None else "")
        ready = json.loads(line)
        assert ready["interrupt_ready"] is True
        native_steps = output / "world" / "steps"
        deadline = time.monotonic() + 10
        while time.monotonic() < deadline:
            running = [json.loads(p.read_text()) for p in native_steps.glob(f'{ready["run_id"]}-*.json')]
            running = [s for s in running if s["status"] == "running"]
            if not running:
                time.sleep(0.001)
                continue
            process.send_signal(signal.SIGSTOP)
            os.waitpid(process.pid, os.WUNTRACED)
            stopped = [json.loads(p.read_text()) for p in native_steps.glob(f'{ready["run_id"]}-*.json')]
            stopped = [s for s in stopped if s["status"] == "running"]
            if stopped:
                interrupted = stopped[0]
                break
            process.send_signal(signal.SIGCONT)
        assert interrupted is not None, "Could not capture a real running native step"
        # Capture the actual persisted state before killing the paused process.
        (output / "interruption.json").write_text(json.dumps({"run_id": ready["run_id"],
            "receipt_id": ready["receipt_id"], "step": interrupted}, indent=2))
    finally:
        process.kill()
        process.wait(timeout=5)
        process.stdout.close()
        process.stderr.close()
    for key in ("case_id", "run_id", "receipt_id", "review_id", "revision"):
        env["PROPERTY_NATIVE_API_" + key.upper()] = str(ready[key])
    env["PROPERTY_NATIVE_API_PHASE"] = "dispatch_restart"
    recovered = subprocess.run(command, cwd=ROOT, env=env, capture_output=True, text=True, timeout=40)
    assert recovered.returncode == 0, recovered.stdout + recovered.stderr
    after = json.loads(next(line for line in recovered.stdout.splitlines() if line.startswith('{"native_api"')))
    persisted = json.loads((output / "world" / "steps" / f'{ready["run_id"]}-{interrupted["stepId"]}.json').read_text())
    assert persisted["status"] == "completed"
    assert persisted["attempt"] == interrupted["attempt"] + 1
    assert after["run_id"] == ready["run_id"]
    assert after["receipt_id"] == ready["receipt_id"]
    assert after["provider_receipt_count"] == after["action_count"] == 1
    print(json.dumps({"native_api": "passed", "scenario": "forced_interrupted_step",
        "run_id": ready["run_id"], "step_id": interrupted["stepId"], "attempt_before": interrupted["attempt"],
        "attempt_after": persisted["attempt"], "provider_receipt_count": 1, "receipt_id": after["receipt_id"],
        "storage": str(output)}))


def _request(client, method, path, **kwargs):
    response = client.request(method, path, **kwargs)
    assert response.status_code == 200, (path, response.status_code, response.text)
    return response.json()


def _wait_detail(client, case_id, predicate):
    deadline = time.monotonic() + 15
    while time.monotonic() < deadline:
        detail = _request(client, "GET", f"/api/cases/{case_id}")
        errors = [r for r in detail["timeline"] if r["kind"] == "workflow_error"]
        assert not errors, errors
        if predicate(detail):
            return detail
        time.sleep(0.04)
    raise AssertionError(f"Native coordinator did not reach the required checkpoint: {json.dumps({'case_id': detail['case']['id'], 'revision': detail['case']['revision'], 'checkpoints': _checkpoints(detail), 'workflow_receipts': [r for r in detail['timeline'] if r['kind'] in {'workflow_receipt', 'workflow_recovery', 'workflow_error'}]})}")


def _checkpoints(detail):
    return [r for r in detail["timeline"] if r["kind"] == "cycle_checkpoint"]


def _events(detail):
    return [r for r in detail["timeline"] if r["kind"] == "incoming_event"]


def _receipts(detail):
    return [r for r in detail["timeline"] if r["kind"] == "simulated_provider_receipt"]


def _exercise_dispatch_phase():
    from fastapi.testclient import TestClient
    from app.main import app
    from app.workflows import signal_case_event

    phase = os.environ["PROPERTY_NATIVE_API_PHASE"]
    started_at = datetime.now(UTC)
    with TestClient(app) as client:
        _request(client, "POST", "/api/demo-session", json={"role": "case_manager"})
        if phase in {"dispatch", "dispatch_interrupt"}:
            # BUILD 002 event 001 contains both sentences. This is a labelled
            # input-only scenario withholding the first sentence until evidence
            # arrives, not an assertion about the historical order of messages.
            created = _request(client, "POST", "/api/cases", json={
                "title": "BUILD 002 derived quote request",
                "property_ref": "DEMO-FLAT-1",
                "report": "Run block lodged by pan connector.",
                "category": "plumbing",
                "work_item": "BUILD 002 obstruction investigation",
                "action": "request_quote",
            })
            case_id = created["case"]["id"]
            initial = _wait_detail(client, case_id, lambda d: bool(_checkpoints(d)))
            assert not _receipts(initial)
            assert any(b["key"] == "classification" for b in initial["decision"]["blockers"])
            evidence = _request(client, "POST", f"/api/cases/{case_id}/evidence", json={
                "text": "Toilet need to be removed to clear blockage. Run block lodged by pan connector.",
                "source_label": "BUILD 002 event 001 — input-only clarification scenario",
                "claims": [{"key": "classification", "value": True,
                            "source_quote": "Toilet need to be removed to clear blockage."}],
                "idempotency_key": "native-api-classification-002",
            })
            pending = _wait_detail(client, case_id, lambda d: any(c["payload"]["revision"] >= evidence["case"]["revision"] for c in _checkpoints(d)))
            review = next(r for r in pending["reviews"] if r["key"] == "classification" and r["status"] == "open")
            review_id = review["id"]
            claim = next(c for c in pending["claims"] if c["key"] == "classification" and not c["verified"])
            assert not _receipts(pending), "Source assertion must not dispatch before review"
            response = {"decision": "correct", "key": "classification", "value": True,
                        "claim_id": claim["id"], "source_id": claim["source_id"],
                        "reason": "The quoted toilet obstruction supports the plumbing classification for this quote request."}

            # Wrong-role input is rejected by the real HTTP authentication path.
            _request(client, "POST", "/api/demo-session", json={"role": "access_officer"})
            rejected = client.post(f"/api/reviews/{review_id}/respond", json=response)
            assert rejected.status_code == 403, rejected.text
            assert not _receipts(_request(client, "GET", f"/api/cases/{case_id}"))
            _request(client, "POST", "/api/demo-session", json={"role": "case_manager"})
            authorised = _request(client, "POST", f"/api/reviews/{review_id}/respond", json=response)
            review_event = next(e for e in reversed(_events(authorised)) if e["payload"]["event_type"] == "review_responded")
            detail = _wait_detail(client, case_id, lambda d: len(_receipts(d)) == 1 and any(review_event["id"] in c["payload"]["consumed_event_ids"] for c in _checkpoints(d)))
            assert detail["actions"][0]["actor"]["id"] == "native-case-coordinator"
            assert detail["actions"][0]["status"] == "succeeded"
            assert detail["case"]["last_verified_action"] == "request_quote"
            assert next(r for r in detail["reviews"] if r["id"] == review_id)["status"] == "resolved"
            receipt_id = _receipts(detail)[0]["id"]
            revision = detail["case"]["revision"]

            # Redeliver exactly the same committed event notification through
            # the real native hook on the application's existing event loop.
            before = len(_checkpoints(detail))
            event = _events(detail)[-1]
            receipt = client.portal.call(signal_case_event, case_id, event["id"], revision)
            assert receipt["status"] == "signalled"
            duplicate = client.post(f"/api/reviews/{review_id}/respond", json=response)
            assert duplicate.status_code == 409, duplicate.text
            detail = _wait_detail(client, case_id, lambda d: len(_checkpoints(d)) > before)
            assert detail["case"]["revision"] == revision
            assert [r["id"] for r in _receipts(detail)] == [receipt_id]
        else:
            case_id = os.environ["PROPERTY_NATIVE_API_CASE_ID"]
            review_id = os.environ["PROPERTY_NATIVE_API_REVIEW_ID"]
            receipt_id = os.environ["PROPERTY_NATIVE_API_RECEIPT_ID"]
            detail = _wait_detail(client, case_id, lambda d: any(datetime.fromisoformat(c["payload"]["assessed_at"]) >= started_at for c in _checkpoints(d)))
            assert detail["case"]["revision"] == int(os.environ["PROPERTY_NATIVE_API_REVISION"])
            assert [r["id"] for r in _receipts(detail)] == [receipt_id]
            assert next(r for r in detail["reviews"] if r["id"] == review_id)["status"] == "resolved"

        transport = [r["payload"] for r in detail["timeline"] if r["kind"] == "workflow_receipt"][-1]
        run_id = transport["run_id"]
        if phase == "dispatch_restart":
            assert run_id == os.environ["PROPERTY_NATIVE_API_RUN_ID"]
        assert len(detail["actions"]) == 1
        assert detail["actions"][0]["simulated"] is True
        assert _receipts(detail)[0]["payload"]["scope"]["action"] == "request_quote"
        output = {"native_api": "passed", "scenario": "evidence_review_dispatch", "phase": phase,
                  "case_id": case_id, "run_id": run_id, "receipt_id": receipt_id, "review_id": review_id,
                  "revision": detail["case"]["revision"], "checkpoint_count": len(_checkpoints(detail)),
                  "provider_receipt_count": len(_receipts(detail)), "action_count": len(detail["actions"])}
        if phase == "dispatch_interrupt":
            print(json.dumps({**output, "interrupt_ready": True}), flush=True)
            event = _events(detail)[-1]
            while True:
                client.portal.call(signal_case_event, case_id, event["id"], detail["case"]["revision"])
                time.sleep(0.02)
    print(json.dumps(output))


def _exercise_phase():
    from fastapi.testclient import TestClient
    from app.main import app

    started_at = datetime.now(UTC)
    phase = os.environ["PROPERTY_NATIVE_API_PHASE"]
    with TestClient(app) as client:
        health = _request(client, "GET", "/api/health")
        assert health["workflow_mode"] == "native_local"
        assert health["external_operations"] == "simulated"
        _request(client, "POST", "/api/demo-session", json={"role": "case_manager"})
        if phase == "intake":
            # This endpoint exercises the real intake service with a strict
            # chronological BUILD snapshot; no later description is read.
            created = _request(client, "POST", "/api/build-cases/002/import")
            case_id = created["case"]["id"]
            intake = next(e for e in _events(created) if e["payload"]["event_type"] == "intake")
            assert any(r["kind"] == "signal_outbox" and r["payload"]["event_id"] == intake["id"] for r in created["timeline"])
            assert created["case"]["interpretation"]["mode"] == "literal_demo"
            initial = _wait_detail(client, case_id, lambda d: any(intake["id"] in c["payload"]["consumed_event_ids"] for c in _checkpoints(d)))
            open_reviews = {r["id"] for r in initial["reviews"] if r["status"] == "open"}
            assert open_reviews, "The intended pending-review scenario was not established"
            assert initial["decision"]["outcome"] != "ACT"
            submitted = _request(client, "POST", f"/api/cases/{case_id}/evidence", json={
                "text": "BUILD 002 runtime check: the first report has been received. Identity and the permitted route remain unverified.",
                "source_label": "Simulated staff note for BUILD 002 native API check",
                "claims": [],
                "idempotency_key": "native-api-evidence-002",
            })
            assert submitted["case"]["revision"] > initial["case"]["revision"]
            evidence_event = next(e for e in reversed(_events(submitted)) if e["payload"]["event_type"] == "evidence_received")
            detail = _wait_detail(client, case_id, lambda d: any(c["payload"]["revision"] >= submitted["case"]["revision"] and evidence_event["id"] in c["payload"]["consumed_event_ids"] for c in _checkpoints(d)))
            assert open_reviews <= {r["id"] for r in detail["reviews"] if r["status"] == "open"}
            assert detail["decision"]["outcome"] != "ACT"
            assert not detail["actions"], "Receiving an unresolved note must not execute work"
        else:
            case_id = os.environ["PROPERTY_NATIVE_API_CASE_ID"]
            expected_revision = int(os.environ["PROPERTY_NATIVE_API_REVISION"])
            old_event_ids = set(json.loads(os.environ["PROPERTY_NATIVE_API_EVENT_IDS"]))
            detail = _wait_detail(client, case_id, lambda d: any(datetime.fromisoformat(c["payload"]["assessed_at"]) >= started_at for c in _checkpoints(d)))
            assert detail["case"]["revision"] == expected_revision
            assert {r["id"] for r in _events(detail)} == old_event_ids
            assert any(r["status"] == "open" for r in detail["reviews"])
            assert not detail["actions"]

        receipts = [r["payload"] for r in detail["timeline"] if r["kind"] == "workflow_receipt"]
        run_id = receipts[-1]["run_id"]
        if phase == "restart":
            assert run_id == os.environ["PROPERTY_NATIVE_API_RUN_ID"]
            assert receipts[-1]["transport"]["status"] == "signalled"
        consumed = set(_checkpoints(detail)[-1]["payload"]["consumed_event_ids"])
        assert {r["id"] for r in _events(detail)} <= consumed
        native_path = Path(os.environ["WORKFLOW_LOCAL_DATA_DIR"])
        assert (native_path / "runs" / f"{run_id}.json").exists()
        deadline = time.monotonic() + 10
        checkpoint_at = datetime.fromisoformat(_checkpoints(detail)[-1]["payload"]["assessed_at"])
        while time.monotonic() < deadline:
            native_events = [json.loads(p.read_text()) for p in (native_path / "events").glob(f"{run_id}-*.json")]
            scheduled = [e for e in native_events if e["eventType"] == "wait_created" and datetime.fromisoformat(e["createdAt"].replace("Z", "+00:00")) >= checkpoint_at]
            if scheduled:
                break
            time.sleep(0.02)
        assert scheduled, "The completed application cycle did not schedule a native wake"
        assert {"run_created", "hook_created", "step_completed"} <= {r["eventType"] for r in native_events}
        output = {"native_api": "passed", "phase": phase, "case_id": case_id, "run_id": run_id,
                  "revision": detail["case"]["revision"], "checkpoint_count": len(_checkpoints(detail)),
                  "event_ids": sorted(r["id"] for r in _events(detail)), "open_review_count": sum(r["status"] == "open" for r in detail["reviews"]),
                  "native_wake_scheduled": True}
    # Emitted after successful native FastAPI lifespan shutdown.
    print(json.dumps(output))


if __name__ == "__main__":
    if os.environ["PROPERTY_NATIVE_API_PHASE"].startswith("dispatch"):
        _exercise_dispatch_phase()
    else:
        _exercise_phase()
