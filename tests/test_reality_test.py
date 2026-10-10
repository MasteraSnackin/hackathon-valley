"""Runner safety/format tests with invented inputs, never reserved datasets.

The native smoke uses a deterministic AI double, not live Claude or an accuracy
claim. Other subprocess tests deliberately remove credentials before execution.
"""
from __future__ import annotations

from copy import deepcopy
import json
import os
from pathlib import Path
import subprocess
import sys

import pytest
from pydantic import ValidationError

from app import reality_test as runner


def fictional():
    return {"schema_version": 1, "title": "Fictional tap report", "property_ref": "FICTIONAL-17",
            "as_of": "2026-10-10T12:00:00+01:00", "report_available_at": "2026-10-10T10:00:00+01:00",
            "report": "The kitchen tap leaks.", "evidence": [{"source_label": "Fictional tenant follow-up",
                "text": "The tap still leaks. Please ask before entry.", "available_at": "2026-10-10T11:00:00+01:00"}]}


def write_json(path, data):
    path.write_text(json.dumps(data))
    return path


def credential_free(monkeypatch):
    for key in ("ANTHROPIC_API_KEY", "ANTHROPIC_AUTH_TOKEN", "VERCEL_QUEUE_BASE_URL"):
        monkeypatch.delenv(key, raising=False)
    monkeypatch.setenv("PROPERTY_LOCAL_ENV", "off")


@pytest.mark.parametrize("change", [
    {"expected_answer": "approve"},
    {"claims": [{"key": "authority", "value": True}]},
    {"property_ref": "DEMO-FLAT-1"},
    {"as_of": "2026-10-10T09:00:00+01:00"},
    {"as_of": "2026-10-10T12:00:00"},
    {"evidence": [{"source_label": "Future", "text": "Future outcome", "available_at": "2026-10-10T13:00:00+01:00"}]},
])
def test_inputs_reject_answers_authority_demo_identity_and_future_information(change):
    with pytest.raises(ValidationError):
        runner.CaseInput.model_validate({**fictional(), **change})


def test_manifest_cannot_escape_or_collide(tmp_path):
    external = write_json(tmp_path / "outside.json", fictional())
    inside = tmp_path / "inputs"
    inside.mkdir()
    (inside / "link.json").symlink_to(external)
    for name in ("../outside.json", str(external), "link.json"):
        with pytest.raises(ValueError):
            runner.safe_input_path(inside, name)
    with pytest.raises(ValidationError):
        runner.Manifest.model_validate({"schema_version": 1, "dataset_kind": "development_fixture", "cases": [
            {"id": "CASE-a", "input_file": "a.json"}, {"id": "case-A", "input_file": "a.json"}]})
    with pytest.raises(ValidationError):
        runner.CaseRef(id="../unsafe", input_file="a.json")


def test_official_mode_requires_frozen_revision_credentials_and_real_release(tmp_path):
    with pytest.raises(ValidationError):
        runner.RunnerConfig(mode="official")
    with pytest.raises(ValidationError):
        runner.RunnerConfig(mode="official", expected_commit="a" * 40, require_model_credentials=False)
    manifest = write_json(tmp_path / "manifest.json", {"schema_version": 1, "dataset_kind": "development_fixture",
        "cases": [{"id": "fictional", "input_file": "case.json"}]})
    config = write_json(tmp_path / "config.json", {"mode": "official", "expected_commit": "a" * 40})
    with pytest.raises(ValueError, match="Development fixtures"):
        runner.run_batch(manifest, config, tmp_path / "output")


def test_preflight_is_read_only_and_does_not_load_local_credentials(tmp_path, monkeypatch):
    credential_free(monkeypatch)
    write_json(tmp_path / "case.json", fictional())
    manifest = write_json(tmp_path / "manifest.json", {"schema_version": 1, "dataset_kind": "development_fixture",
        "cases": [{"id": "fictional", "input_file": "case.json"}]})
    config = write_json(tmp_path / "config.json", {})
    before = set(tmp_path.iterdir())
    result = runner.preflight(manifest, config)
    assert result["execution"] == "not_started"
    assert result["cases"][0]["valid"] is True
    assert result["model_credential_present"] is False
    assert result["ready_to_attempt"] is False
    assert set(tmp_path.iterdir()) == before


def test_batch_keeps_invalid_and_missing_credentials_outputs_and_refuses_overwrite(tmp_path, monkeypatch):
    credential_free(monkeypatch)
    write_json(tmp_path / "good.json", fictional())
    (tmp_path / "bad.json").write_text('{"broken":')
    manifest = write_json(tmp_path / "manifest.json", {"schema_version": 1, "dataset_kind": "development_fixture", "cases": [
        {"id": "bad", "input_file": "bad.json"}, {"id": "good", "input_file": "good.json"}]})
    config = write_json(tmp_path / "config.json", {"workers": 2, "case_timeout_seconds": 10})
    output = tmp_path / "run"
    result = runner.run_batch(manifest, config, output)
    assert result["settled"] == 0 and result["case_count"] == 2
    assert result["cases"][0]["status"] == "input_invalid"
    assert "Missing exported Anthropic credentials" in result["cases"][1]["error"]
    for case_id in ("good", "bad"):
        assert (output / "ANSWERS" / case_id / "ANSWER.md").is_file()
        assert (output / "ANSWERS" / case_id / "REASONING.md").is_file()
        assert "No application case evidence" in (output / "ANSWERS" / case_id / "ANSWER.md").read_text()
    assert (output / "ANSWERS/bad/input.json").read_text() == '{"broken":'
    with pytest.raises(FileExistsError):
        runner.run_batch(manifest, config, output)


def test_checkpoint_does_not_confuse_assessment_with_execution():
    detail = {"case": {"revision": 3}, "timeline": [
        {"kind": "incoming_event", "id": "event"},
        {"kind": "cycle_checkpoint", "payload": {"revision": 3, "consumed_event_ids": ["event"],
            "assessed_at": "2026-10-10T10:00:00+00:00"}}]}
    assert runner.checkpoint_settled(detail, {"run_id": None}) is False
    assert runner.checkpoint_settled(detail, {"run_id": "run", "unfinished_steps": True}) is False
    assert runner.checkpoint_settled(detail, {"run_id": "run", "completed": True}) is True
    detail["case"]["revision"] = 4
    assert runner.checkpoint_settled(detail, {"run_id": "run", "completed": True}) is False


def test_native_worker_with_fake_model_preserves_chronology_and_real_sdk_evidence(tmp_path, monkeypatch):
    credential_free(monkeypatch)
    case_dir = tmp_path / "case"
    case_dir.mkdir()
    write_json(case_dir / "input.json", fictional())
    config = runner.RunnerConfig(require_model_credentials=False, policy_settings={"tenant_messages": "off"})
    config_path = write_json(tmp_path / "config.json", config.model_dump())
    env = runner.worker_environment(config, tmp_path / "runtime")
    (tmp_path / "runtime").mkdir()
    # Runs the actual app + SDK in a fresh process. The fake exists only in this
    # test wrapper and is unavailable from the command-line production runner.
    code = '''
import json, sys
from pathlib import Path
from app import ai, reality_test as r
seen=[]
def fake_triage(text, context):
    seen.append({"text":text,"earlier":[x["text"] for x in context["earlier_messages"]]})
    parsed=ai.Triage(intent="new_request",summary="Fictional deterministic test reading",issues=[
        ai.TriageIssue(category="plumbing",route="request_quote",work_item="Kitchen tap",source_quote=text,relation="current_case")
    ],claims=[],ambiguities=[],answers=[],risk_flags=[],confidence="high",rationale="Fixture route for runner plumbing only")
    return parsed.model_dump(), {"provider":"test-double","model":"offline-fixture","prompt_version":"fictional-test","request_id":"fixture"}
ai.triage=fake_triage
directory=Path(sys.argv[1])
result=r._worker(directory/"input.json",Path(sys.argv[2]),directory)
(directory/"observed-model-inputs.json").write_text(json.dumps(seen))
print(json.dumps(result))
'''
    done = subprocess.run([sys.executable, "-c", code, str(case_dir), str(config_path)], cwd=runner.ROOT,
                          env=env, capture_output=True, text=True, timeout=45)
    assert done.returncode == 0, done.stdout + done.stderr
    result = runner.load_json(case_dir / "result.json")
    assert result["status"] == "settled" and result["execution"] == "native_local"
    seen = runner.load_json(case_dir / "observed-model-inputs.json")
    assert seen[0]["earlier"] == []
    assert seen[1]["earlier"] == [fictional()["report"]]
    evidence = runner.load_json(case_dir / "evidence.json")
    assert evidence["input_source_index"] == 1
    assert evidence["policy"]["settings"]["tenant_messages"] == "off"
    assert evidence["policy"]["version"] == 2
    assert len(evidence["cases"]) == 1
    detail = evidence["cases"][0]
    assert not detail["actions"], "Fixture cannot inject identity/route authority"
    assert detail["case"]["triage"]["state"] == "done"
    assert {b["key"] for b in detail["decision"]["blockers"]} >= {"identity", "route"}
    events = evidence["native"][0]["events"]
    assert {"run_created", "step_completed", "wait_created"} <= {e["eventType"] for e in events}
    assert any("triage_case_messages" in s["stepName"] for s in evidence["native"][0]["steps"])
    for index in (0, 1):
        assert (case_dir / f"checkpoint-{index:03d}.json").is_file()
    provenance = {"git_commit": "test", "config_sha256": "test", "input_sha256": "test"}
    runner.markdown_evidence("fictional", case_dir, provenance, config, result)
    assert "PREPARATION ONLY" in (case_dir / "ANSWER.md").read_text()
    assert "Fixture route for runner plumbing only" in (case_dir / "REASONING.md").read_text()


def test_credential_values_are_redacted(monkeypatch):
    monkeypatch.setenv("ANTHROPIC_API_KEY", "fictional-secret-value")
    assert runner.scrub({"error": ["failure fictional-secret-value"]}) == {"error": ["failure [REDACTED]"]}


def test_hard_batch_timeout_preserves_pending_cases(tmp_path, monkeypatch):
    credential_free(monkeypatch)
    write_json(tmp_path / "case.json", fictional())
    manifest = write_json(tmp_path / "manifest.json", {"schema_version": 1, "dataset_kind": "development_fixture", "cases": [
        {"id": "slow", "input_file": "case.json"}, {"id": "queued", "input_file": "case.json"}]})
    config = write_json(tmp_path / "config.json", {"workers": 1, "case_timeout_seconds": 5, "batch_timeout_seconds": 5})
    original = subprocess.Popen
    def slow_worker(command, **kwargs):
        if isinstance(command, list) and "app.reality_test" in command:
            command = [sys.executable, "-c", "import time; time.sleep(60)"]
        return original(command, **kwargs)
    monkeypatch.setattr(runner.subprocess, "Popen", slow_worker)
    result = runner.run_batch(manifest, config, tmp_path / "run")
    assert result["cases"][0]["status"] == "timeout"
    assert result["cases"][1]["status"] == "not_run_batch_deadline"
    assert (tmp_path / "run/ANSWERS/queued/ANSWER.md").exists()


def test_source_change_marks_run_invalid_without_discarding_failures(tmp_path, monkeypatch):
    credential_free(monkeypatch)
    write_json(tmp_path / "case.json", fictional())
    manifest = write_json(tmp_path / "manifest.json", {"schema_version": 1, "dataset_kind": "development_fixture",
        "cases": [{"id": "case", "input_file": "case.json"}]})
    config = write_json(tmp_path / "config.json", {})
    calls = []
    def changing_source(_):
        calls.append(True)
        return {"git_commit": "frozen", "source_tree_sha256": str(len(calls)), "source_dirty": True}
    monkeypatch.setattr(runner, "source_provenance", changing_source)
    result = runner.run_batch(manifest, config, tmp_path / "run")
    assert result["status"] == "invalid_source_changed" and result["source_unchanged"] is False
    assert result["cases"][0]["status"] == "worker_failed"
    assert (tmp_path / "run/summary.json").exists()
    assert "INVALID RUN" in (tmp_path / "run/README.md").read_text()
    assert "INVALID RUN" in (tmp_path / "run/ANSWERS/case/ANSWER.md").read_text()
