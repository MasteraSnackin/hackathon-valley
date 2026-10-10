"""Bounded, evidence-preserving runner for newly released Reality Test inputs.

No dataset is loaded implicitly. Each input runs in a separate process and store,
through the application's actual API and native local Vercel Workflow lifespan.
"""
from __future__ import annotations

import argparse
from concurrent.futures import ThreadPoolExecutor
from datetime import datetime, timezone
import hashlib
from importlib.metadata import PackageNotFoundError, version
import json
import os
from pathlib import Path
import re
import signal
import subprocess
import sys
import time
from typing import Literal

from pydantic import AwareDatetime, BaseModel, ConfigDict, Field, model_validator

ROOT = Path(__file__).resolve().parents[1]
SOURCE_PATHS = ["app", "config", "pyproject.toml", "uv.lock", "requirements.lock"]
SAFE_ID = r"^[A-Za-z0-9][A-Za-z0-9_-]{0,79}$"


class Strict(BaseModel):
    model_config = ConfigDict(extra="forbid")


class Source(Strict):
    source_label: str = Field(min_length=1, max_length=200)
    text: str = Field(min_length=1, max_length=50000)
    available_at: AwareDatetime


class CaseInput(Strict):
    schema_version: Literal[1]
    title: str = Field(min_length=3, max_length=160)
    property_ref: str = Field(min_length=2, max_length=200)
    as_of: AwareDatetime
    report_available_at: AwareDatetime
    report: str = Field(min_length=3, max_length=30000)
    evidence: list[Source] = Field(default_factory=list, max_length=100)

    @model_validator(mode="after")
    def chronological(self):
        if self.property_ref == "DEMO-FLAT-1":
            raise ValueError("The preconfigured fictional demo directory is forbidden in evaluation")
        previous = self.report_available_at
        if previous > self.as_of:
            raise ValueError("Report is not available at the decision cutoff")
        for source in self.evidence:
            if not previous <= source.available_at <= self.as_of:
                raise ValueError("Evidence must be ordered by availability and within the cutoff")
            previous = source.available_at
        return self


class CaseRef(Strict):
    id: str = Field(pattern=SAFE_ID)
    input_file: str = Field(min_length=1, max_length=1000)


class Manifest(Strict):
    schema_version: Literal[1]
    dataset_kind: Literal["development_fixture", "organiser_release"]
    cases: list[CaseRef] = Field(min_length=1, max_length=1000)

    @model_validator(mode="after")
    def unique_ids(self):
        # Case-fold because macOS filesystems are usually case insensitive.
        ids = [case.id.casefold() for case in self.cases]
        if len(ids) != len(set(ids)):
            raise ValueError("Case IDs must be unique, including letter case")
        return self


class RunnerConfig(Strict):
    schema_version: Literal[1] = 1
    mode: Literal["preparation", "official"] = "preparation"
    expected_commit: str | None = Field(default=None, pattern=r"^[0-9a-f]{40}$")
    model: str = Field(default="claude-opus-5", min_length=1, max_length=100)
    jev_model: str = Field(default="jev-1.13.0", min_length=1, max_length=100)
    jev_timeout_seconds: float = Field(default=30, ge=1, le=120)
    triage_effort: Literal["low", "medium", "high", "max"] = "medium"
    extract_effort: Literal["low", "medium", "high", "max"] = "low"
    draft_effort: Literal["low", "medium", "high", "max"] = "low"
    model_timeout_seconds: float = Field(default=30, ge=1, le=120)
    case_timeout_seconds: float = Field(default=150, ge=5, le=900)
    batch_timeout_seconds: float = Field(default=1500, ge=5, le=1700)
    workers: int = Field(default=4, ge=1, le=8)
    poll_seconds: float = Field(default=0.25, ge=0.02, le=5)
    require_model_credentials: bool = True
    policy_settings: dict = Field(default_factory=dict)
    policy_rules: list[dict] = Field(default_factory=list, max_length=50)

    @model_validator(mode="after")
    def official_requirements(self):
        if self.mode == "official" and (not self.expected_commit or not self.require_model_credentials):
            raise ValueError("Official mode requires the frozen commit and model credentials")
        # Validate before spawning processes. No application runtime is imported.
        from .domain import PolicyInput
        PolicyInput(base_version=1, settings=self.policy_settings, rules=self.policy_rules)
        return self


def utcnow():
    return datetime.now(timezone.utc).isoformat()


def digest(data: bytes):
    return hashlib.sha256(data).hexdigest()


def canonical(value):
    return json.dumps(value, sort_keys=True, ensure_ascii=False, separators=(",", ":")).encode()


def scrub(value):
    """Never publish credential values inherited by this process in error text."""
    secrets = [v for k, v in os.environ.items()
               if len(v) >= 8 and any(part in k.upper() for part in ("KEY", "TOKEN", "SECRET", "PASSWORD"))]
    def clean(item):
        if isinstance(item, str):
            for secret in secrets:
                item = item.replace(secret, "[REDACTED]")
            return item
        if isinstance(item, dict):
            return {k: clean(v) for k, v in item.items()}
        if isinstance(item, list):
            return [clean(v) for v in item]
        return item
    return clean(value)


def atomic_json(path, value):
    path = Path(path)
    temporary = path.with_suffix(path.suffix + ".tmp")
    temporary.write_text(json.dumps(scrub(value), indent=2, ensure_ascii=False) + "\n")
    temporary.replace(path)


def atomic_text(path, text):
    path = Path(path)
    temporary = path.with_suffix(path.suffix + ".tmp")
    temporary.write_text(scrub(text))
    temporary.replace(path)


def load_json(path):
    return json.loads(Path(path).read_text())


def safe_input_path(base: Path, name: str):
    relative = Path(name)
    if relative.is_absolute() or ".." in relative.parts:
        raise ValueError("input_file must be a relative path inside the manifest directory")
    target = (base / relative).resolve(strict=True)
    if not target.is_relative_to(base.resolve()) or not target.is_file():
        raise ValueError("input_file must resolve to a file inside the manifest directory")
    if target.stat().st_size > 6_000_000:
        raise ValueError("Case JSON exceeds the 6 MB input limit")
    return target


def source_provenance(config: RunnerConfig):
    def git(*args):
        return subprocess.check_output(["git", *args], cwd=ROOT, text=True).strip()
    commit = git("rev-parse", "HEAD")
    dirty = bool(git("status", "--porcelain", "--", *SOURCE_PATHS))
    if config.mode == "official":
        if commit != config.expected_commit:
            raise ValueError("Current commit differs from expected frozen commit")
        if dirty:
            raise ValueError("Official mode requires clean tracked and untracked application/configuration sources")
    files = git("ls-files", "--cached", "--others", "--exclude-standard", "--", *SOURCE_PATHS).splitlines()
    hashes = {name: digest((ROOT / name).read_bytes()) for name in files if (ROOT / name).is_file()}
    installed = {}
    for name in ("vercel-workflow", "anthropic", "typesafe-sdk", "fastapi", "pydantic"):
        try:
            installed[name] = version(name)
        except PackageNotFoundError:
            installed[name] = None
    return {"git_commit": commit, "source_dirty": dirty, "source_files_sha256": hashes,
            "source_tree_sha256": digest(canonical(hashes)), "python": sys.version,
            "installed_packages": installed}


def worker_environment(config: RunnerConfig, runtime: Path):
    env = dict(os.environ)
    # Never discover .env.local, reuse a shared store, contact a hosted queue or
    # substitute manual_demo. Credentials must be explicitly exported by operator.
    env.update(APP_MODE="demo", WORKFLOW_MODE="native_local", WORKFLOW_TARGET_WORLD="local",
               PROPERTY_LOCAL_ENV="off", DATABASE_URL=f"sqlite:///{runtime / 'application.db'}",
               WORKFLOW_LOCAL_DATA_DIR=str(runtime / "native-world"), CLAUDE_MODEL=config.model,
               CLAUDE_TIMEOUT=str(config.model_timeout_seconds), CLAUDE_TRIAGE_EFFORT=config.triage_effort,
               CLAUDE_EXTRACT_EFFORT=config.extract_effort, CLAUDE_DRAFT_EFFORT=config.draft_effort,
               JEV_MODEL=config.jev_model, JEV_TIMEOUT=str(config.jev_timeout_seconds))
    env.pop("VERCEL_QUEUE_BASE_URL", None)
    return env


def model_environment(config: RunnerConfig):
    from .domain import DEFAULT_SETTINGS
    return {"anthropic_credential_present": bool(os.getenv("ANTHROPIC_API_KEY") or os.getenv("ANTHROPIC_AUTH_TOKEN")),
            "typesafe_credential_present": bool(os.getenv("TYPESAFE_API_KEY")),
            "policy_router": config.policy_settings.get("router", DEFAULT_SETTINGS["router"]),
            "claude_model": config.model, "jev_model": config.jev_model,
            "triage_effort": config.triage_effort, "extract_effort": config.extract_effort,
            "draft_effort": config.draft_effort, "jev_timeout_seconds": config.jev_timeout_seconds,
            "claude_timeout_seconds": config.model_timeout_seconds}


def _request(client, method, path, **kwargs):
    response = client.request(method, path, **kwargs)
    if response.status_code != 200:
        # Do not copy request headers or credentials to output.
        raise RuntimeError(f"Application request {method} {path} returned HTTP {response.status_code}")
    return response.json()


async def _run_id(case_id):
    from .workflows import case_hook_token
    from vercel import workflow
    try:
        return (await workflow.get_hook_by_token(case_hook_token(case_id))).run_id
    except workflow.HookNotFoundError:
        return None


def native_state(client, case_id, world_path):
    run_id = client.portal.call(_run_id, case_id)
    cache = getattr(client, "_reality_run_ids", {})
    if run_id:
        cache[case_id] = run_id
        client._reality_run_ids = cache
    else:
        # A terminal coordinator closes its hook; retain its actual run identity.
        run_id = cache.get(case_id)
        if not run_id:
            from .service import get_service
            receipts = [r["payload"] for r in get_service().detail(case_id)["timeline"] if r["kind"] == "workflow_receipt"]
            run_id = receipts[-1].get("run_id") if receipts else None
        if not run_id:
            # Hook creation events survive terminal-run hook deletion. Their
            # plain token avoids deserializing arbitrary native input payloads.
            for path in sorted((world_path / "events").glob("*.json")):
                event = load_json(path)
                if event.get("eventType") == "hook_created" and event.get("eventData", {}).get("token") == f"property-case:{case_id}":
                    run_id = event["runId"]
                    cache[case_id] = run_id
                    client._reality_run_ids = cache
                    break
    if not run_id:
        return {"case_id": case_id, "run_id": None, "waiting": False}
    return {"case_id": case_id, **read_native_run(world_path, run_id)}


def read_native_run(world_path, run_id):
    """Read our isolated SDK records without hydrating serialized input payloads."""
    def records(folder, pattern):
        return [load_json(path) for path in sorted((world_path / folder).glob(pattern))]
    runs = records("runs", f"{run_id}.json")
    events = records("events", f"{run_id}-*.json")
    steps = records("steps", f"{run_id}-*.json")
    completed = {e.get("correlationId") for e in events if e.get("eventType") == "wait_completed"}
    waits = [e for e in events if e.get("eventType") == "wait_created" and e.get("correlationId") not in completed]
    failed = any(r.get("status") in {"failed", "cancelled"} for r in runs) or any(s.get("status") == "failed" for s in steps)
    unfinished = any(s.get("status") not in {"completed", "failed"} for s in steps)
    # Native event data is retained, but secret values are removed on export.
    return {"run_id": run_id, "failed": failed, "unfinished_steps": unfinished,
            "runs": runs, "steps": steps, "events": events, "open_waits": waits,
            "completed": any(r.get("status") == "completed" for r in runs)}


def checkpoint_settled(detail, native):
    checkpoints = [r["payload"] for r in detail["timeline"] if r["kind"] == "cycle_checkpoint"]
    if not checkpoints or not native.get("run_id") or native.get("unfinished_steps"):
        return False
    checkpoint = checkpoints[-1]
    if checkpoint["revision"] != detail["case"]["revision"]:
        return False
    events = {r["id"] for r in detail["timeline"] if r["kind"] == "incoming_event"}
    if not events <= set(checkpoint["consumed_event_ids"]):
        return False
    if native.get("completed"):
        return True
    assessed = datetime.fromisoformat(checkpoint["assessed_at"])
    for wait in native.get("open_waits", []):
        created = datetime.fromisoformat(wait["createdAt"].replace("Z", "+00:00"))
        resume = wait.get("eventData", {}).get("resumeAt")
        if created >= assessed and resume and datetime.fromisoformat(resume.replace("Z", "+00:00")) > datetime.now(timezone.utc):
            return True
    return False


def collect(client, case_dir, *, source_index):
    from .service import get_service
    service = get_service()
    cases = service.list_cases()
    details = [service.detail(case["id"]) for case in cases]
    native = [native_state(client, detail["case"]["id"], Path(os.environ["WORKFLOW_LOCAL_DATA_DIR"])) for detail in details]
    world_path = Path(os.environ["WORKFLOW_LOCAL_DATA_DIR"])
    known = {n["run_id"] for n in native if n.get("run_id")}
    # A native failure before hook creation has no discoverable case mapping.
    # Preserve it anyway: every run in this isolated store belongs to this input.
    unassociated = [read_native_run(world_path, path.stem) for path in sorted((world_path / "runs").glob("*.json")) if path.stem not in known]
    policy = service.policies()["active"]
    payload = {"captured_at": utcnow(), "input_source_index": source_index,
               "policy": policy, "policy_content_sha256": digest(canonical({k: policy[k] for k in ("version", "settings", "rules")})),
               "cases": details, "native": native, "unassociated_native_runs": unassociated}
    atomic_json(case_dir / "evidence.json", payload)
    return payload


def settle(client, case_dir, config, source_index):
    from .service import get_service
    service = get_service()
    while True:  # The parent enforces a hard per-process and whole-batch deadline.
        snapshot = collect(client, case_dir, source_index=source_index)
        if any(n.get("failed") for n in snapshot["native"] + snapshot["unassociated_native_runs"]):
            raise RuntimeError("Native workflow or step failed; see evidence.json")
        if any(r["kind"] == "workflow_error" for d in snapshot["cases"] for r in d["timeline"]):
            raise RuntimeError("Native workflow transport failed; see evidence.json")
        ready = bool(snapshot["cases"])
        ready &= all(n.get("completed") for n in snapshot["unassociated_native_runs"])
        for detail, native in zip(snapshot["cases"], snapshot["native"]):
            with service.db.tx() as connection:
                current = service.db.case(connection, detail["case"]["id"])
                pending = service.pending_sources(connection, current["id"])
                questions = service.tenant_questions_due(connection, current, service.active(connection))
            ready &= not pending and not questions and checkpoint_settled(detail, native)
            ready &= current["revision"] == detail["case"]["revision"]
        # A newly split issue must also have a native checkpoint before returning.
        ready &= {c["id"] for c in service.list_cases()} == {d["case"]["id"] for d in snapshot["cases"]}
        if ready:
            return snapshot
        time.sleep(config.poll_seconds)


def _worker(input_path: Path, config_path: Path, case_dir: Path):
    config = RunnerConfig.model_validate(load_json(config_path))
    data = CaseInput.model_validate(load_json(input_path))
    required = {"APP_MODE": "demo", "WORKFLOW_MODE": "native_local", "WORKFLOW_TARGET_WORLD": "local", "PROPERTY_LOCAL_ENV": "off"}
    if any(os.getenv(key) != value for key, value in required.items()) or os.getenv("VERCEL_QUEUE_BASE_URL"):
        raise RuntimeError("Worker requires the runner's explicitly isolated local environment")
    database = os.getenv("DATABASE_URL", "")
    world = os.getenv("WORKFLOW_LOCAL_DATA_DIR", "")
    if not database.startswith("sqlite:///") or not world:
        raise RuntimeError("Worker requires isolated SQLite and native state paths")
    database_path = Path(database.removeprefix("sqlite:///"))
    if database_path.exists() or Path(world).exists() or database_path.parent.resolve() != Path(world).parent.resolve():
        raise RuntimeError("Worker refuses existing/shared database or native state")
    from . import ai
    if config.require_model_credentials and not ai.configured():
        raise RuntimeError("Missing exported Anthropic credentials; no model or workflow executed")
    from fastapi.testclient import TestClient
    from .main import app
    with TestClient(app) as client:
        _request(client, "POST", "/api/demo-session", json={"role": "policy_editor"})
        health = _request(client, "GET", "/api/health")
        if health["workflow_mode"] != "native_local" or health["external_operations"] != "simulated":
            raise RuntimeError("Runner requires native local Workflow and simulated operational adapters")
        if config.policy_settings or config.policy_rules:
            policy = _request(client, "POST", "/api/policies/draft", json={"base_version": 1,
                "settings": config.policy_settings, "rules": config.policy_rules,
                "reason": "Frozen Reality Test runner configuration, applied before any cases"})
            _request(client, "POST", f"/api/policies/{policy['id']}/preview")
            _request(client, "POST", f"/api/policies/{policy['id']}/publish")
        _request(client, "POST", "/api/demo-session", json={"role": "case_manager"})
        atomic_json(case_dir / "runtime-status.json", {"health": health, "model_environment": model_environment(config),
                    "execution_started_at": utcnow()})
        created = _request(client, "POST", "/api/cases", json={"title": data.title,
            "property_ref": data.property_ref, "report": data.report, "triage": "claude"})
        case_id = created["case"]["id"]
        snapshot = settle(client, case_dir, config, 0)
        atomic_json(case_dir / "checkpoint-000.json", snapshot)
        for index, source in enumerate(data.evidence, 1):
            _request(client, "POST", f"/api/cases/{case_id}/evidence", json={"text": source.text,
                "source_label": source.source_label, "occurred_at": source.available_at.isoformat(),
                "claims": [], "idempotency_key": f"reality-source-{index}"})
            snapshot = settle(client, case_dir, config, index)
            atomic_json(case_dir / f"checkpoint-{index:03d}.json", snapshot)
        failures = [r for d in snapshot["cases"] for r in d["timeline"] if
                    (r["kind"] == "interpretation" and r["payload"].get("status") == "failed") or
                    (r["kind"] == "tenant_message" and r["payload"].get("status") == "draft_failed")]
        fallbacks = [r for d in snapshot["cases"] for r in d["timeline"]
                     if r["kind"] == "routing" and r["payload"].get("error_type")]
        result = {"status": "model_failed" if failures else "settled", "system_case_id": case_id,
                  "execution": "native_local", "external_operations": "simulated",
                  "sources_processed": len(data.evidence) + 1,
                  "finished_at": utcnow(), "model_failure_count": len(failures),
                  "routing_fallback_count": len(fallbacks),
                  "routing_fallback_errors": sorted({r["payload"]["error_type"] for r in fallbacks})}
        atomic_json(case_dir / "result.json", result)
    return result


def markdown_evidence(case_id, case_dir, provenance, config, result):
    # Formatting only: ANSWER.md / REASONING.md / AUDIT.md from the recorded evidence.
    from .answer_export import write_answers
    write_answers(case_id, case_dir, provenance, config, result)


def run_batch(manifest_path: Path, config_path: Path, output: Path):
    config_bytes = config_path.read_bytes()
    config = RunnerConfig.model_validate_json(config_bytes)
    manifest_bytes = manifest_path.read_bytes()
    manifest = Manifest.model_validate_json(manifest_bytes)
    if config.mode == "official" and manifest.dataset_kind != "organiser_release":
        raise ValueError("Development fixtures cannot be used in official mode")
    provenance = {**source_provenance(config), "config_sha256": digest(config_bytes),
                  "manifest_sha256": digest(manifest_bytes), "started_at": utcnow(),
                  "model_environment": model_environment(config),
                  "mode": config.mode, "runtime": "native_local", "external_operations": "simulated"}
    # Exclusive directory creation prevents overwriting or mixing previous results.
    output.mkdir(parents=True, exist_ok=False)
    (output / "ANSWERS").mkdir()
    (output / "runtime").mkdir()
    (output / "config.json").write_bytes(config_bytes)
    (output / "manifest.json").write_bytes(manifest_bytes)
    atomic_json(output / "provenance.json", provenance)
    deadline = time.monotonic() + config.batch_timeout_seconds

    def process(ref):
        case_dir = output / "ANSWERS" / ref.id
        case_dir.mkdir()
        runtime = output / "runtime" / ref.id
        runtime.mkdir()
        case_provenance = {**provenance, "input_sha256": "unavailable"}
        result = {"status": "input_invalid", "execution": "not_started"}
        try:
            path = safe_input_path(manifest_path.parent, ref.input_file)
            data = path.read_bytes()
            case_provenance["input_sha256"] = digest(data)
            # Preserve exact input bytes, including malformed JSON, before validation.
            (case_dir / "input.json").write_bytes(data)
            CaseInput.model_validate_json(data)
            remaining = deadline - time.monotonic()
            if remaining <= 0:
                result = {"status": "not_run_batch_deadline", "execution": "not_started"}
            else:
                command = [sys.executable, "-m", "app.reality_test", "--worker", str(case_dir.resolve()),
                           "--config", str((output / "config.json").resolve())]
                env = worker_environment(config, runtime.resolve())
                with subprocess.Popen(command, cwd=ROOT, env=env, stdout=subprocess.PIPE, stderr=subprocess.PIPE,
                                      text=True, start_new_session=True) as child:
                    try:
                        stdout, stderr = child.communicate(timeout=min(config.case_timeout_seconds, remaining))
                        result = load_json(case_dir / "result.json") if (case_dir / "result.json").exists() else {
                            "status": "worker_failed", "execution": "see_partial_evidence", "error": f"Worker exited {child.returncode}"}
                        if child.returncode and result["status"] == "settled":
                            result = {**result, "status": "worker_shutdown_failed"}
                    except subprocess.TimeoutExpired:
                        os.killpg(child.pid, signal.SIGKILL)
                        stdout, stderr = child.communicate()
                        result = {"status": "timeout", "execution": "see_partial_evidence", "error": "Hard case/batch deadline reached; worker stopped, partial evidence preserved"}
                atomic_text(case_dir / "worker.log", stdout + stderr)
        except Exception as exc:
            # Validation text can echo input content; retain a bounded, redacted error.
            result = {**result, "error": f"{type(exc).__name__}: {exc}"[:2000]}
        result["finished_at"] = utcnow()
        atomic_json(case_dir / "provenance.json", case_provenance)
        atomic_json(case_dir / "result.json", result)
        markdown_evidence(ref.id, case_dir, case_provenance, config, result)
        return {"case_id": ref.id, **result}

    with ThreadPoolExecutor(max_workers=config.workers) as pool:
        results = list(pool.map(process, manifest.cases))
    # Preserve the run summary even if a source change breaks official preflight.
    final_source = source_provenance(config.model_copy(update={"mode": "preparation"}))
    changed = final_source["git_commit"] != provenance["git_commit"] or final_source["source_tree_sha256"] != provenance["source_tree_sha256"]
    summary = {"mode": config.mode, "status": "invalid_source_changed" if changed else "finished",
               "finished_at": utcnow(), "source_unchanged": not changed,
               "settled": sum(r["status"] == "settled" for r in results), "case_count": len(results), "cases": results}
    atomic_json(output / "summary.json", summary)
    invalid_notice = "**INVALID RUN: application source or Git commit changed during execution. Do not submit this as evidence from the frozen system.**\n\n" if changed else ""
    if changed:
        for ref in manifest.cases:
            answer = output / "ANSWERS" / ref.id / "ANSWER.md"
            atomic_text(answer, invalid_notice + answer.read_text())
    atomic_text(output / "README.md", "# Reality Test run\n\n" +
                invalid_notice +
                ("OFFICIAL RUN\n\n" if config.mode == "official" else "PREPARATION ONLY — not official results.\n\n") +
                "See summary.json for every case, including failures. ANSWERS contains evidence-bound exports.\n\n"
                "runtime contains isolated databases and native SDK state; keep it local and do not publish it automatically.\n"
                "Review inputs/logs for personal data before publication. Never manually improve answers or hide failed cases.\n")
    return summary


def preflight(manifest_path: Path, config_path: Path):
    """Read/validate only. Does not start Workflow, call a model or create outputs."""
    config = RunnerConfig.model_validate_json(config_path.read_bytes())
    manifest = Manifest.model_validate_json(manifest_path.read_bytes())
    if config.mode == "official" and manifest.dataset_kind != "organiser_release":
        raise ValueError("Development fixtures cannot be used in official mode")
    provenance = source_provenance(config)
    entries = []
    for ref in manifest.cases:
        try:
            path = safe_input_path(manifest_path.parent, ref.input_file)
            data = path.read_bytes()
            CaseInput.model_validate_json(data)
            entries.append({"case_id": ref.id, "valid": True, "sha256": digest(data)})
        except Exception as exc:
            entries.append({"case_id": ref.id, "valid": False, "error": f"{type(exc).__name__}: {exc}"[:2000]})
    configured = bool(os.getenv("ANTHROPIC_API_KEY") or os.getenv("ANTHROPIC_AUTH_TOKEN"))
    missing = [name for name, installed in provenance["installed_packages"].items() if installed is None]
    return {"status": "validated_only", "mode": config.mode, "execution": "not_started",
            "model_credential_present": configured, "credentials_required": config.require_model_credentials,
            "model_environment": model_environment(config),
            "missing_packages": missing,
            "ready_to_attempt": all(e["valid"] for e in entries) and (configured or not config.require_model_credentials) and not missing,
            "provenance": provenance, "cases": entries}


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--manifest", type=Path)
    parser.add_argument("--config", type=Path, required=True)
    parser.add_argument("--output", type=Path, help="New run directory; must not already exist")
    parser.add_argument("--validate-only", action="store_true", help="Check inputs/configuration without execution or network calls")
    parser.add_argument("--worker", type=Path, help=argparse.SUPPRESS)
    args = parser.parse_args(argv)
    if args.worker:
        try:
            result = _worker(args.worker / "input.json", args.config, args.worker)
            return 0 if result["status"] == "settled" else 1
        except Exception as exc:
            result = {"status": "worker_failed", "error": f"{type(exc).__name__}: {exc}"[:2000],
                      "execution": "native_local_partial" if (args.worker / "runtime-status.json").exists() else "not_started",
                      "finished_at": utcnow()}
            atomic_json(args.worker / "result.json", result)
            return 1
    if args.validate_only:
        if not args.manifest:
            parser.error("--manifest is required")
        try:
            result = preflight(args.manifest.resolve(), args.config.resolve())
            print(json.dumps(scrub(result), indent=2))
            return 0 if result["ready_to_attempt"] else 1
        except Exception as exc:
            print(scrub(f"Preflight refused: {type(exc).__name__}: {exc}"), file=sys.stderr)
            return 2
    if not args.manifest or not args.output:
        parser.error("--manifest and --output are required")
    try:
        summary = run_batch(args.manifest.resolve(), args.config.resolve(), args.output.resolve())
    except Exception as exc:
        print(scrub(f"Runner refused: {type(exc).__name__}: {exc}"), file=sys.stderr)
        return 2
    print(json.dumps({k: v for k, v in summary.items() if k != "cases"}))
    return 0 if summary["status"] == "finished" and summary["settled"] == summary["case_count"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
