"""Operator-assumed identity/route checks: explicit, recorded, never over a contradiction."""
from copy import deepcopy
from datetime import datetime, timezone

import pytest
from pydantic import ValidationError

from app.domain import DEFAULT_SETTINGS, PolicyInput, evaluate, scope_of

AT = datetime(2026, 10, 12, 9, tzinfo=timezone.utc)
CASE = {"id": "fictional-assumed", "property_ref": "FICTIONAL-ASSUMED-1", "category": "plumbing",
        "revision": 1, "action_revision": 1,
        "proposal": {"action": "clarify", "work_item": "Dripping tap", "provider": "Fictional provider",
                     "access_method": "tenant_present", "scope": {}}}


def policy(**settings):
    return {"version": 2, "settings": {**deepcopy(DEFAULT_SETTINGS), **settings}, "rules": []}


def test_default_keeps_identity_and_route_as_human_review():
    result = evaluate(CASE, [], [], policy(), at=AT)
    assert {b["key"] for b in result["blockers"]} == {"identity", "route"}
    assert result["outcome"] == "HUMAN REVIEW"


def test_assumed_checks_pass_with_a_recorded_reason():
    result = evaluate(CASE, [], [], policy(assumed_checks=["identity", "route"]), at=AT)
    assert result["outcome"] == "ACT"
    checks = {c["key"]: c for c in result["checks"]}
    assert checks["identity"]["status"] == "PASS"
    assert "Assumed satisfied by policy v2" in checks["identity"]["reason"]


def test_assumption_never_overrides_a_contradicting_source():
    claim = {"id": "c1", "key": "identity", "value": False, "scope": scope_of(CASE), "verified": False, "source_id": "s1"}
    result = evaluate(CASE, [claim], [], policy(assumed_checks=["identity", "route"]), at=AT)
    assert result["outcome"] == "STOP ACTION"


def test_only_identity_and_route_can_be_assumed():
    with pytest.raises(ValidationError):
        PolicyInput(base_version=1, settings={"assumed_checks": ["authority"]})
    PolicyInput(base_version=1, settings={"assumed_checks": ["identity"]})
