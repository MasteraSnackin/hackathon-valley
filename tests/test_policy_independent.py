"""Independent acceptance checks using fictional, build-only policy scenarios."""
from copy import deepcopy
from datetime import datetime, timedelta, timezone

import pytest
from pydantic import ValidationError

from app.domain import (
    ClaimInput, DEFAULT_SETTINGS, ProposalInput, evaluate, scope_of, working_after,
)


AT = datetime(2026, 10, 12, 9, tzinfo=timezone.utc)


def scenario(action="instruct_work", amount=80):
    case = {
        "id": "independent-fictional-case", "property_ref": "FICTIONAL-REVIEW-1",
        "category": "windows", "revision": 1, "action_revision": 1,
        "proposal": {"action": action, "work_item": "Window handle",
                     "provider": "Fictional provider", "access_method": "tenant_present", "scope": {}},
    }
    policy = {"version": 1, "settings": deepcopy(DEFAULT_SETTINGS), "rules": []}
    claims = [
        {"id": key, "key": key, "value": amount if key == "total" else True,
         "scope": scope_of(case), "verified": True, "source_id": "source-" + key}
        for key in ["identity", "route", "access", "authority", "schedule", "evidence",
                    "classification", "total", "completion", "commitments"]
    ]
    return case, claims, policy


def grant(case, key="finance", policy_version=1):
    return {"key": key, "action_revision": case["action_revision"],
            "scope": scope_of(case), "policy_version": policy_version,
            "expires_at": (AT + timedelta(hours=2)).isoformat(), "source_id": "scoped-grant"}


def test_missing_access_changes_route_but_remains_blocked():
    case, claims, policy = scenario()
    claims = [c for c in claims if c["key"] != "access"]
    ordinary = evaluate(case, claims, [], policy, at=AT)
    assert ordinary["outcome"] == "CLARIFY"
    assert {b["key"] for b in ordinary["blockers"]} == {"access"}
    policy["settings"]["access_immediate_review"] = True
    immediate = evaluate(case, claims, [], policy, at=AT)
    assert immediate["outcome"] == "HUMAN REVIEW"
    assert immediate["blockers"][0]["key"] == "access"


def test_finance_approval_leaves_other_blockers_intact():
    case, claims, policy = scenario(amount=150)
    claims = [c for c in claims if c["key"] not in {"access", "schedule"}]
    before = evaluate(case, claims, [], policy, at=AT)
    assert {b["key"] for b in before["blockers"]} == {"finance", "access", "schedule"}
    after = evaluate(case, claims, [grant(case)], policy, at=AT)
    assert {b["key"] for b in after["blockers"]} == {"access", "schedule"}
    assert after["outcome"] != "ACT"


def test_explicit_refusal_survives_approval_and_weaker_custom_rule():
    case, claims, policy = scenario()
    for claim in claims:
        if claim["key"] == "authority": claim["value"] = False
    policy["rules"] = [{"id": "ask-first", "actions": ["instruct_work"], "match": "all",
                        "conditions": [{"key": "authority", "status": "FAIL"}],
                        "response": "CLARIFY", "owner": "case_manager"}]
    result = evaluate(case, claims, [grant(case, "authority")], policy, at=AT)
    assert result["outcome"] == "STOP ACTION"
    assert any(b["key"] == "authority" and b["status"] == "FAIL" for b in result["blockers"])


def test_irrelevant_cost_conflict_does_not_block_supported_item_closure():
    case, claims, policy = scenario(action="close_item")
    claims.append({**next(c for c in claims if c["key"] == "total"),
                   "id": "different-cost", "source_id": "other-cost-source", "value": 130})
    result = evaluate(case, claims, [], policy, at=AT)
    assert result["outcome"] == "ACT"
    assert not result["blockers"]


def test_material_conflict_retains_both_sources():
    case, claims, policy = scenario()
    claims.append({**next(c for c in claims if c["key"] == "schedule"),
                   "id": "other-schedule", "source_id": "other-schedule-source", "value": False})
    result = evaluate(case, claims, [], policy, at=AT)
    blocker = next(b for b in result["blockers"] if b["key"] == "schedule")
    assert blocker["status"] == "CONFLICT"
    assert set(blocker["source_ids"]) == {"source-schedule", "other-schedule-source"}
    assert blocker["response"] == "HUMAN REVIEW"


def test_approval_does_not_transfer_to_new_proposal_or_policy():
    case, claims, policy = scenario(amount=150)
    approval = grant(case)
    assert evaluate(case, claims, [approval], policy, at=AT)["outcome"] == "ACT"
    case["action_revision"] += 1
    assert evaluate(case, claims, [approval], policy, at=AT)["outcome"] != "ACT"
    case["action_revision"] -= 1
    policy["version"] = 2
    assert evaluate(case, claims, [approval], policy, at=AT)["outcome"] != "ACT"


def test_relaxed_threshold_does_not_silently_release_pending_reassessment():
    case, claims, policy = scenario(amount=150)
    policy["settings"]["review_limit"] = 200
    case["policy_pending"] = True
    result = evaluate(case, claims, [], policy, at=AT)
    assert result["outcome"] != "ACT"
    assert {b["key"] for b in result["blockers"]} == {"policy"}


@pytest.mark.parametrize("reserved", ["property_ref", "work_item", "provider", "access_method", "action"])
def test_extra_scope_cannot_replace_action_identity(reserved):
    with pytest.raises(ValidationError):
        ProposalInput(action="instruct_work", work_item="Window", scope={reserved: "different"})


@pytest.mark.parametrize("invalid", [float("nan"), float("inf"), float("-inf")])
def test_non_finite_amount_is_not_valid_evidence(invalid):
    with pytest.raises(ValidationError):
        ClaimInput(key="total", value=invalid, source_quote="An invalid amount")


def test_business_deadline_skips_weekend_and_configured_holiday():
    friday = datetime(2026, 10, 9, 15, tzinfo=timezone.utc)  # 16:00 London
    expected = datetime(2026, 10, 13, 9, tzinfo=timezone.utc)  # Tuesday 10:00 London
    assert working_after(friday, 2, ["2026-10-12"]) == expected
