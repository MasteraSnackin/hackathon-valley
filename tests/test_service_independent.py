"""Independent transition regressions using fictional sources, not held-out cases."""
from datetime import timedelta

import pytest

from app.domain import (ClaimInput, EvidenceInput, Intake, PolicyInput,
                        ReviewResponse, Rule, now, scope_of, stamp)
from app.service import Conflict, Service
from app.store import Store


def actor(role='case_manager'):
    return {'id': 'independent-' + role, 'role': role}


@pytest.fixture
def service(tmp_path):
    return Service(Store('sqlite:///' + str(tmp_path / 'independent.db')))


def create(service):
    return service.intake(Intake(title='Fictional dishwasher repair',
        property_ref='DEMO-FLAT-1', report='The dishwasher stops mid-cycle.',
        category='appliance', work_item='Dishwasher motor repair', action='instruct_work',
        triage='staff'), actor())


def open_review(detail, key):
    return next(r for r in reversed(detail['reviews'])
                if r['key'] == key and r['status'] == 'open')


def submit(service, cid, key, value):
    quote = f'Fictional authorised source confirms {key} = {value} for this work.'
    return service.evidence(cid, EvidenceInput(text=quote,
        source_label='Fictional test evidence',
        claims=[ClaimInput(key=key, value=value, source_quote=quote)]), actor())


def verify_latest(service, detail, key):
    claim = next(c for c in reversed(detail['claims']) if c['key'] == key)
    review = open_review(detail, key)
    return service.respond(review['id'], ReviewResponse(decision='correct',
        reason='Checked the source, identity and exact work scope.',
        claim_id=claim['id'], source_id=claim['source_id']), actor(review['owner']))


def ready(service, total=150, omit=()):
    detail = create(service)
    cid = detail['case']['id']
    for key, value in [('access', True), ('authority', True), ('schedule', True),
                       ('evidence', True), ('total', total)]:
        if key not in omit:
            detail = verify_latest(service, submit(service, cid, key, value), key)
    return detail


def approve(service, detail, key):
    review = open_review(detail, key)
    return service.respond(review['id'], ReviewResponse(decision='approve',
        reason='Approve only the currently evidenced scoped requirement.',
        source_id=detail['evidence'][-1]['id'], scope=scope_of(detail['case']),
        expires_at=stamp(now() + timedelta(hours=1))), actor(review['owner']))


def test_changed_amount_requires_a_fresh_financial_decision(service):
    detail = approve(service, ready(service), 'finance')
    assert detail['decision']['outcome'] == 'ACT'
    cid = detail['case']['id']
    detail = submit(service, cid, 'total', 250)
    assert next(b for b in detail['decision']['blockers'] if b['key'] == 'total')['status'] == 'CONFLICT'
    detail = verify_latest(service, detail, 'total')
    assert any(b['key'] == 'finance' for b in detail['decision']['blockers'])
    with pytest.raises(Conflict):
        service.execute(cid, actor())


def test_received_consent_can_be_verified_without_waiting_for_timeout(service):
    detail = ready(service, total=80, omit={'access'})
    assert any(q['key'] == 'access' and q['status'] == 'open' for q in detail['questions'])
    detail = submit(service, detail['case']['id'], 'access', True)
    assert open_review(detail, 'access')['owner'] == 'access_officer'
    detail = verify_latest(service, detail, 'access')
    assert detail['decision']['outcome'] == 'ACT'
    assert all(q['status'] == 'closed' for q in detail['questions'] if q['key'] == 'access')


def test_custom_gate_approval_leaves_missing_consent_blocked(service):
    detail = ready(service, total=80, omit={'access'})
    cid = detail['case']['id']
    policy = service.policies()['active']
    draft = service.draft(PolicyInput(base_version=policy['version'], settings=policy['settings'],
        rules=[Rule(id='appliance-quality-review', actions=['instruct_work'],
                    conditions=[{'key': 'classification', 'status': 'PASS'}],
                    response='HUMAN REVIEW', owner='case_manager')]), actor('policy_editor'))
    service.preview(draft['id'], actor('policy_editor'))
    service.publish(draft['id'], actor('policy_editor'))
    detail = service.evaluate_case(cid, actor())
    detail = approve(service, detail, 'rule:appliance-quality-review')
    blockers = {b['key'] for b in detail['decision']['blockers']}
    assert 'rule:appliance-quality-review' not in blockers
    assert 'access' in blockers
    with pytest.raises(Conflict):
        service.execute(cid, actor())


def test_financial_rejection_stops_current_proposal(service):
    detail = ready(service)
    cid = detail['case']['id']
    review = open_review(detail, 'finance')
    detail = service.respond(review['id'], ReviewResponse(decision='reject',
        reason='The proposed repair has been rejected pending a revised scope.'), actor('approver'))
    assert detail['decision']['outcome'] == 'STOP ACTION'
    detail = service.evaluate_case(cid, actor())
    assert detail['decision']['outcome'] == 'STOP ACTION'
    with pytest.raises(Conflict):
        service.execute(cid, actor())


def test_policy_publication_does_not_reopen_a_completed_action(service):
    detail = service.intake(Intake(title='Fictional completed dishwasher repair',
        property_ref='DEMO-FLAT-1', report='The dishwasher has been repaired.',
        category='appliance', work_item='Dishwasher motor repair', action='close_item',
        triage='staff'), actor())
    cid = detail['case']['id']
    for key in ('completion', 'commitments'):
        detail = verify_latest(service, submit(service, cid, key, True), key)
    result = service.execute(cid, actor())
    assert result['detail']['case']['status'] == 'verified_resolution'
    policy = service.policies()['active']
    draft = service.draft(PolicyInput(base_version=policy['version'],
        settings={**policy['settings'], 'access_immediate_review': True}), actor('policy_editor'))
    service.preview(draft['id'], actor('policy_editor'))
    service.publish(draft['id'], actor('policy_editor'))
    service.tick(cid)
    detail = service.detail(cid)
    assert detail['case']['status'] == 'verified_resolution'
    assert not detail['case']['policy_pending']
    assert not [r for r in detail['reviews'] if r['key'] == 'policy' and r['status'] == 'open']
    assert len([r for r in detail['timeline'] if r['kind'] == 'simulated_provider_receipt']) == 1


@pytest.mark.parametrize('response', ['CLARIFY', 'WAIT', 'STOP ACTION'])
def test_custom_condition_fact_can_be_verified_then_resumed(service, response):
    detail = service.intake(Intake(title='Fictional quote after earlier repair',
        property_ref='DEMO-FLAT-1', report='The dishwasher needs a repair quote.',
        category='appliance', work_item='Dishwasher repair', action='request_quote',
        triage='staff'), actor())
    cid = detail['case']['id']
    policy = service.policies()['active']
    draft = service.draft(PolicyInput(base_version=policy['version'], settings=policy['settings'],
        rules=[Rule(id='previous-completion-check', actions=['request_quote'],
                    conditions=[{'key': 'completion', 'status': 'UNKNOWN'}],
                    response=response, owner='case_manager')]), actor('policy_editor'))
    service.preview(draft['id'], actor('policy_editor'))
    service.publish(draft['id'], actor('policy_editor'))
    detail = service.evaluate_case(cid, actor())
    assert any(b['key'] == 'rule:previous-completion-check' for b in detail['decision']['blockers'])
    detail = submit(service, cid, 'completion', True)
    assert open_review(detail, 'completion')['owner'] == 'reviewer'
    detail = verify_latest(service, detail, 'completion')
    assert detail['decision']['outcome'] == 'ACT'
