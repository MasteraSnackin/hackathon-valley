"""Policy drafting acceptance checks using entirely fictional local fixtures."""
from copy import deepcopy
from datetime import timedelta

import pytest
from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from fastapi.testclient import TestClient

from app import service as service_module
from app.domain import (
    ClaimInput, DEFAULT_SETTINGS, EvidenceInput, Intake, PolicyInput,
    ReviewResponse, evaluate, now, scope_of, stamp,
)
from app.policy_assistant import create_policy_assistant_router, interpret_policy
from app.service import Conflict, Forbidden, Service
from app.store import Store


def actor(role='case_manager'):
    return {'id': 'fictional-' + role, 'role': role}


@pytest.fixture
def active():
    return {'version': 8, 'settings': deepcopy(DEFAULT_SETTINGS), 'rules': []}


@pytest.fixture
def service(tmp_path, monkeypatch):
    instance = Service(Store('sqlite:///' + str(tmp_path / 'policy-assistant-fictional.db')))
    monkeypatch.setattr(service_module, '_service', instance)
    monkeypatch.setattr(service_module, 'interpret', lambda _: {
        'mode': 'fictional_fixture', 'category': 'plumbing', 'claims': [],
        'source_quote': '', 'summary': 'Fictional test input; no external model.'})
    return instance


@pytest.fixture
def client(service):
    app = FastAPI()

    def identity(request: Request):
        role = request.headers.get('x-fictional-role')
        if not role:
            raise Forbidden('Staff session required')
        return actor(role)

    @app.exception_handler(Forbidden)
    async def forbidden(request, exc):
        return JSONResponse({'detail': str(exc)}, 403)

    app.include_router(create_policy_assistant_router(identity))
    with TestClient(app) as test_client:
        yield test_client


def post(client, text, role='case_manager', review_id=None):
    data = {'text': text}
    if review_id:
        data['review_id'] = review_id
    return client.post('/api/policy-assistant/interpret', json=data,
                       headers={'x-fictional-role': role})


def record_snapshot(service):
    with service.db.tx() as connection:
        return service.db.list(connection), service.active(connection), service.db.case_list(connection)


def case(service):
    return service.intake(Intake(
        title='Fictional tap repair', property_ref='FICTIONAL-FLAT-A',
        report='Fictional fixture: the kitchen tap requires inspection.',
        category='plumbing', work_item='Kitchen tap', action='instruct_work'), actor())


def access_review(service, decision='correct'):
    detail = case(service)
    text = 'Fictional source grants consent for this visit only.'
    detail = service.evidence(detail['case']['id'], EvidenceInput(
        text=text, source_label='Fictional consent source',
        claims=[ClaimInput(key='access', value=True, source_quote=text)]), actor())
    review = next(r for r in detail['reviews'] if r['key'] == 'access' and r['status'] == 'open')
    claim = next(c for c in detail['claims'] if c['key'] == 'access')
    if decision:
        service.respond(review['id'], ReviewResponse(
            decision=decision, reason='Fictional reviewer checked this visit only.',
            claim_id=claim['id'] if decision == 'correct' else None,
            source_id=claim['source_id']), actor('access_officer'))
    return review, claim


def test_spending_threshold_preserves_every_unrelated_setting_and_rule(active):
    active['settings'].update({'reminder_hours': 3, 'escalation_hours': 15,
                               'holiday_dates': ['2026-12-25'],
                               'required_per_action': {'request_quote': ['evidence']}})
    active['rules'] = [{
        'id': 'keep-completion', 'conditions': [{'key': 'completion', 'status': 'UNKNOWN'}],
        'actions': ['close_item'], 'response': 'HUMAN REVIEW', 'owner': 'reviewer',
        'match': 'all', 'required': True, 'property_ref': 'FICTIONAL-B', 'category': None,
    }]
    before = deepcopy(active)
    result = interpret_policy('Set the spending review threshold to £250', active)
    assert result.status == 'ready'
    expected = deepcopy(before['settings'])
    expected['review_limit'] = 250
    assert result.draft.settings == expected
    assert [r.model_dump() for r in result.draft.rules] == before['rules']
    assert result.draft.base_version == 8
    assert active == before


@pytest.mark.parametrize('text,key,value', [
    ('Require human review for spending over £1,250.50', 'review_limit', 1250.50),
    ('Set financial review limit to 350 pounds', 'review_limit', 350),
    ('Escalate missing access permission immediately', 'access_immediate_review', True),
    ('Request access permission when it is missing', 'access_immediate_review', False),
    ('Remind after 4 working hours', 'reminder_hours', 4),
    ('Escalate after 24 working hours', 'escalation_hours', 24),
    ('Set reminder limit to two', 'reminder_limit', 2),
])
def test_supported_settings(text, key, value, active):
    result = interpret_policy(text, active)
    assert result.status == 'ready', result
    assert result.draft.settings[key] == value


def test_combined_followups_and_invalid_order(active):
    result = interpret_policy('Remind after 4 working hours and escalate after 12 working hours with at most 2 reminders', active)
    assert result.status == 'ready'
    assert {k: result.draft.settings[k] for k in ['reminder_hours', 'escalation_hours', 'reminder_limit']} == {
        'reminder_hours': 4, 'escalation_hours': 12, 'reminder_limit': 2}
    assert 'original request' in result.summary
    invalid = interpret_policy('Remind after 20 working hours', active)
    assert invalid.status == 'clarification'
    assert invalid.draft is None


@pytest.mark.parametrize('text', [
    'Set spending threshold to 250',
    'Set spending threshold to $250',
    'Require review for spending at least £250',
    'Set spending threshold to £250 for this tenant',
    'Set spending threshold to £250 and delete all other rules',
    'Remind after 4 hours',
    'Escalate after two days',
    'Set reminder limit to 100',
    'Require human review when completion is missing',
    'Require human review when identity and schedule are conflicting for all actions',
])
def test_ambiguous_or_unrepresentable_requests_have_no_draft(text, active):
    result = interpret_policy(text, active)
    assert result.status in {'clarification', 'unsupported'}
    assert result.draft is None
    assert result.questions or result.warnings


@pytest.mark.parametrize('text', [
    'Grant universal access to every property',
    'Mark all identity facts verified',
    'Automatically approve work without authority',
    'Disable required consent checks',
    'Treat all access as approved',
    'Assume permission from silence for all future visits',
])
def test_case_permissions_and_hard_gates_cannot_be_created_by_text(text, active):
    result = interpret_policy(text, active)
    assert result.status == 'unsupported'
    assert result.draft is None


@pytest.mark.parametrize('text,key,state,action,response', [
    ('Require human review when completion is missing for close_item', 'completion', 'UNKNOWN', 'close_item', 'HUMAN REVIEW'),
    ('Stop action if evidence is missing before instructing work', 'evidence', 'UNKNOWN', 'instruct_work', 'STOP ACTION'),
    ('Require human review for identity conflicts for all actions', 'identity', 'CONFLICT', None, 'HUMAN REVIEW'),
    ('Escalate scheduling conflicts to a case manager for confirm_appointment', 'schedule', 'CONFLICT', 'confirm_appointment', 'HUMAN REVIEW'),
])
def test_reusable_custom_conditions(text, key, state, action, response, active):
    result = interpret_policy(text, active)
    assert result.status == 'ready', result
    rule = result.draft.rules[-1]
    assert rule.conditions == [{'key': key, 'status': state}]
    assert rule.actions == ([action] if action else [])
    assert rule.response == response


def test_quoted_property_identity_preserved_and_deliberate_update_only(active):
    first = interpret_policy('Require human review when identity is conflicting for all actions at property "FICTIONAL-Flat A"', active)
    assert first.status == 'ready'
    rule = first.draft.rules[-1]
    assert rule.property_ref == 'FICTIONAL-Flat A'
    active['rules'] = [rule.model_dump()]
    duplicate = interpret_policy('Require human review when identity is conflicting for all actions at property "FICTIONAL-Flat A"', active)
    assert len(duplicate.draft.rules) == 1
    update = interpret_policy(f'Update rule {rule.id}: Stop action when evidence is missing for instruct_work', active)
    assert update.status == 'ready'
    assert update.draft.rules[0].id == rule.id
    assert update.draft.rules[0].conditions[0]['key'] == 'evidence'
    assert interpret_policy('Update rule absent: Stop action when evidence is missing for instruct_work', active).draft is None


def test_suggestion_keeps_case_decision_distinct_and_never_mutates(client, service):
    review, claim = access_review(service)
    before = record_snapshot(service)
    response = client.get(f"/api/policy-assistant/reviews/{review['id']}/suggestion", headers={'x-fictional-role': 'reviewer'})
    assert response.status_code == 200
    result = response.json()
    assert result['status'] == 'ready'
    assert result['source_review_id'] == review['id']
    assert result['suggested_text']
    rule = result['draft']['rules'][-1]
    assert rule['conditions'] == [{'key': 'access', 'status': 'UNKNOWN'}]
    assert rule['property_ref'] == 'FICTIONAL-FLAT-A'
    assert rule['actions'] == ['instruct_work']
    assert rule['response'] == 'HUMAN REVIEW'
    assert review['id'] in result['draft']['reason']
    assert claim['source_id'] in result['draft']['reason']
    assert any('not permission' in warning for warning in result['warnings'])
    assert record_snapshot(service) == before
    compose = post(client, 'Make this a policy', review_id=review['id'])
    assert compose.json()['draft']['rules'] == result['draft']['rules']
    assert record_snapshot(service) == before


def test_rejected_access_review_still_suggests_only_a_restrictive_rule(client, service):
    review, _ = access_review(service, decision='reject')
    result = client.get(f"/api/policy-assistant/reviews/{review['id']}/suggestion", headers={'x-fictional-role': 'access_officer'}).json()
    assert result['source_review_id'] == review['id']
    assert result['suggested_text']
    assert result['draft']['rules'][-1]['response'] in {'HUMAN REVIEW', 'STOP ACTION'}


def test_open_and_stale_reviews_do_not_supply_resolution_suggestions(client, service):
    review, _ = access_review(service, decision=None)
    result = client.get(f"/api/policy-assistant/reviews/{review['id']}/suggestion", headers={'x-fictional-role': 'case_manager'}).json()
    assert result['status'] == 'clarification'
    assert result['draft'] is None


def test_financial_case_approval_never_invents_a_reusable_threshold(client, service):
    detail = case(service)
    text = 'Fictional full commitment is £350 including tax.'
    detail = service.evidence(detail['case']['id'], EvidenceInput(
        text=text, source_label='Fictional quotation',
        claims=[ClaimInput(key='total', value=350, source_quote=text)]), actor())
    claim = next(c for c in detail['claims'] if c['key'] == 'total')
    total_review = next(r for r in detail['reviews'] if r['key'] == 'total' and r['status'] == 'open')
    detail = service.respond(total_review['id'], ReviewResponse(
        decision='correct', reason='Fictional full quotation checked.',
        source_id=claim['source_id'], claim_id=claim['id']), actor())
    finance_review = next(r for r in detail['reviews'] if r['key'] == 'finance' and r['status'] == 'open')
    service.respond(finance_review['id'], ReviewResponse(
        decision='approve', reason='Fictional approval for this work item only.',
        source_id=claim['source_id'], scope=scope_of(detail['case']),
        expires_at=stamp(now() + timedelta(hours=1))), actor('approver'))
    before = record_snapshot(service)
    result = client.get(f"/api/policy-assistant/reviews/{finance_review['id']}/suggestion", headers={'x-fictional-role': 'approver'}).json()
    assert result['status'] == 'clarification'
    assert result['draft'] is None
    assert result['source_review_id'] == finance_review['id']
    assert 'threshold' in result['questions'][0]
    assert record_snapshot(service) == before


def test_staff_only_and_missing_ids_have_identical_errors(client, service):
    review, _ = access_review(service)
    path = f"/api/policy-assistant/reviews/{review['id']}/suggestion"
    assert client.get(path).status_code == 403
    assert client.get(path, headers={'x-fictional-role': 'tenant'}).status_code == 403
    assert post(client, 'Set spending threshold to £250', role='tenant').status_code == 403
    with service.db.tx() as connection:
        policy_id = service.active(connection)['id']
    headers = {'x-fictional-role': 'case_manager'}
    missing = client.get('/api/policy-assistant/reviews/missing/suggestion', headers=headers)
    wrong_kind = client.get(f'/api/policy-assistant/reviews/{policy_id}/suggestion', headers=headers)
    assert missing.status_code == wrong_kind.status_code == 404
    assert missing.json() == wrong_kind.json() == {'detail': 'Review not found'}
    assert post(client, 'Set spending threshold to £250', review_id='missing').status_code == 404


def test_case_manager_can_propose_but_editor_must_save_preview_and_publish(client, service):
    before = record_snapshot(service)
    response = post(client, 'Set the spending review threshold to £250')
    assert response.status_code == 200
    draft = PolicyInput(**response.json()['draft'])
    assert record_snapshot(service) == before
    with pytest.raises(Forbidden):
        service.draft(draft, actor())
    saved = service.draft(draft, actor('policy_editor'))
    with pytest.raises(Conflict):
        service.publish(saved['id'], actor('policy_editor'))
    service.preview(saved['id'], actor('policy_editor'))
    service.publish(saved['id'], actor('policy_editor'))
    assert service.policies()['active']['settings']['review_limit'] == 250


def test_weaker_rule_cannot_relax_refusal_or_scope_gate(active):
    result = interpret_policy('Ask for clarification when access is refused for instruct_work', active)
    assert result.status == 'ready'
    fictional_case = {
        'id': 'fictional-refusal', 'property_ref': 'FICTIONAL-A', 'category': 'plumbing',
        'revision': 1, 'action_revision': 1,
        'proposal': {'action': 'instruct_work', 'work_item': 'Tap', 'provider': 'Fictional contractor',
                     'access_method': 'tenant_present', 'scope': {}},
    }
    claims = [{'id': 'fictional-access', 'key': 'access', 'value': False,
               'verified': True, 'scope': scope_of(fictional_case), 'source_id': 'fictional-source'}]
    policy = {'version': 9, 'settings': result.draft.settings, 'rules': [r.model_dump() for r in result.draft.rules]}
    decision = evaluate(fictional_case, claims, [], policy)
    assert decision['outcome'] == 'STOP ACTION'
    assert any(b['key'] == 'access' and b['response'] == 'STOP ACTION' for b in decision['blockers'])
    assert any(b['key'] == 'authority' for b in decision['blockers'])


def test_unknown_clause_is_not_silently_dropped(active):
    result = interpret_policy('Set spending threshold to £250 and send emails to the tenant', active)
    assert result.status != 'ready'
    assert result.draft is None
