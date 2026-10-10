"""Offline projection tests using fabricated policy mechanics, no reserved data."""
from copy import deepcopy
from datetime import timedelta
import json

import pytest
from fastapi import FastAPI, Header
from fastapi.responses import JSONResponse
from fastapi.testclient import TestClient

from app import insights
from app.domain import ClaimInput, EvidenceInput, Intake, PolicyInput, ProposalInput, ReviewResponse, scope_of, stamp, now
from app.insights import PolicyComparisonInput, case_insights, compare_policy, create_insights_router
from app.service import Forbidden, Service
from app.store import Store


def actor(role='case_manager'):
    return {'id': 'offline-test-' + role, 'role': role}


@pytest.fixture
def service(tmp_path):
    return Service(Store('sqlite:///' + str(tmp_path / 'insights.db')))


def make(service, action='instruct_work'):
    return service.intake(Intake(title='Fictional tap repair', property_ref='DEMO-FLAT-1',
                                 report='The tap drips.', category='plumbing', work_item='Kitchen tap',
                                 action=action, triage='staff'), actor())


def source(service, cid, key, value, text, scope=None, occurred_at=None):
    return service.evidence(cid, EvidenceInput(text=text, source_label='Fictional source',
        claims=[ClaimInput(key=key, value=value, scope=scope or {}, source_quote=text)],
        occurred_at=occurred_at), actor())


def draft(service, **settings):
    active = service.policies()['active']
    return service.draft(PolicyInput(base_version=active['version'], settings={**active['settings'], **settings}), actor('policy_editor'))


def compare(service, proposal, ids=None):
    return compare_policy(service, PolicyComparisonInput(draft_id=proposal['id'], case_ids=ids), actor('policy_editor'))


def stored_state(service):
    with service.db.tx() as c:
        return deepcopy({'records': service.db.list(c), 'cases': service.db.case_list(c),
                         'active_policy': service.db.get_meta(c, 'active_policy')})


def test_comparison_does_not_confuse_wrong_scope_or_absence_with_conflict(service):
    d = make(service)
    cid = d['case']['id']
    source(service, cid, 'access', False, 'Entry refused for the old kitchen job.')
    service.proposal(cid, ProposalInput(action='instruct_work', work_item='Bathroom tap'), actor())
    source(service, cid, 'access', True, 'Tenant allows this bathroom visit.')
    comparisons = case_insights(service, cid, actor())['comparisons']
    current = next(g for g in comparisons if g['key'] == 'access' and g['applies_to_current_action'])
    other = next(g for g in comparisons if g['key'] == 'access' and not g['applies_to_current_action'])
    assert current['status'] == 'UNKNOWN'
    assert not current['claims'][0]['verified']
    assert other['status'] == 'OUT_OF_SCOPE'
    assert not any(g['status'] == 'CONFLICT' for g in comparisons)
    assert not any(g['key'] == 'completion' for g in comparisons)


def test_current_conflict_and_verified_supersession_stay_distinct(service):
    cid = make(service)['case']['id']
    d = source(service, cid, 'access', True, 'Permission granted for this visit.')
    chosen = next(c for c in d['claims'] if c['key'] == 'access')
    d = source(service, cid, 'access', False, 'Permission refused for this visit.')
    assert next(g for g in case_insights(service, cid, actor())['comparisons'] if g['key'] == 'access')['status'] == 'CONFLICT'
    review = next(r for r in reversed(d['reviews']) if r['key'] == 'access' and r['status'] == 'open')
    service.respond(review['id'], ReviewResponse(decision='correct', reason='Tenant clarified which permission applies.',
                    source_id=chosen['source_id'], claim_id=chosen['id']), actor('access_officer'))
    group = next(g for g in case_insights(service, cid, actor())['comparisons'] if g['key'] == 'access')
    assert group['status'] == 'PASS'
    assert len(group['claims']) == 3
    assert sum(c['applicability'] == 'SUPERSEDED' for c in group['claims']) == 2
    assert all(c['superseded_by'] for c in group['claims'] if c['applicability'] == 'SUPERSEDED')


def test_hearsay_and_demo_party_marker_do_not_establish_contradiction_or_identity(service):
    cid = make(service)['case']['id']
    d = source(service, cid, 'access', False, 'Tenant refuses entry.')
    with service.db.tx() as c:
        s, _ = service.db.add(c, 'evidence', {'text': 'Contractor believes access is allowed.',
            'source_label': 'Contractor report', 'actor': actor(),
            'party': {'kind': 'contractor', 'name': 'Fictional contractor', 'verified': True,
                      'match': 'caller_id_fictional_directory'}, 'occurred_at': stamp()}, cid)
        service.db.add(c, 'claim', {'key': 'access', 'value': True, 'source_id': s['id'],
            'source_quote': 'Contractor believes access is allowed.', 'scope': scope_of(d['case']),
            'verified': False, 'hearsay': True, 'supersedes': []}, cid)
    result = case_insights(service, cid, actor())
    group = next(g for g in result['comparisons'] if g['key'] == 'access')
    assert group['status'] == 'FAIL'
    hearsay = next(c for c in group['claims'] if c['hearsay'])
    assert hearsay['applicability'] == 'HEARSAY'
    assert hearsay['actor_meaning'] == 'recorded source submitter'
    assert hearsay['party']['match'] == 'caller_id_fictional_directory'
    assert 'do not establish production identity' in result['comparison_notice']


def test_expired_claims_are_visible_but_not_current_facts(service, monkeypatch):
    d = make(service)
    cid, at = d['case']['id'], now()
    with service.db.tx() as c:
        service.db.add(c, 'claim', {'key': 'access', 'value': True, 'verified': True,
            'source_id': d['evidence'][0]['id'], 'source_quote': 'The tap drips.',
            'scope': scope_of(d['case']), 'expires_at': stamp(at - timedelta(seconds=1)), 'supersedes': []}, cid)
    monkeypatch.setattr(insights, 'now', lambda: at)
    group = next(g for g in case_insights(service, cid, actor())['comparisons'] if g['key'] == 'access')
    assert group['status'] == 'EXPIRED'


def test_playback_hides_late_evidence_even_if_it_claims_an_earlier_occurrence(service):
    d = make(service)
    cid = d['case']['id']
    original = case_insights(service, cid, actor())['frames']
    first = deepcopy(original[0])
    source(service, cid, 'access', True, 'LATER_PRIVATE_SOURCE_QUOTE', occurred_at='1990-01-01T00:00:00Z')
    service.proposal(cid, ProposalInput(action='request_quote', work_item='LATER_REPLACEMENT_ITEM'), actor())
    with service.db.tx() as c:
        current = service.db.case(c, cid)
        current['title'] = 'LATER_REPLACEMENT_TITLE'
        service.db.save_case(c, current)
    frames = case_insights(service, cid, actor())['frames']
    assert frames[0] == first
    assert 'LATER_' not in json.dumps(frames[0])
    assert 'LATER_PRIVATE_SOURCE_QUOTE' in json.dumps(frames[-1]['evidence'])
    for frame in frames:
        assert frame['at'] == frame['decision']['created_at']
        assert all(e['created_at'] <= frame['at'] for e in frame['evidence'])
        assert all(e['created_at'] <= frame['at'] for e in frame['events'])
        assert frame['events'][-1]['id'] == frame['id']


def test_playback_uses_saved_decision_not_current_policy_or_assessed_future_time(service):
    cid = make(service)['case']['id']
    with service.db.tx() as c:
        recorded, _ = service.db.add(c, 'decision', {'outcome': 'WAIT', 'checks': [], 'blockers': [],
            'policy_version': 17, 'scope': {'work_item': 'Recorded only'},
            'assessed_at': '2099-01-01T00:00:00Z'}, cid)
    source(service, cid, 'completion', True, 'AFTER_FUTURE_ASSESSED_FRAME')
    frame = next(f for f in case_insights(service, cid, actor())['frames'] if f['id'] == recorded['id'])
    assert frame['decision']['policy_version'] == 17
    assert frame['decision']['outcome'] == 'WAIT'
    assert frame['at'] == recorded['created_at']
    assert 'AFTER_FUTURE_ASSESSED_FRAME' not in json.dumps(frame)


def test_policy_comparison_freezes_time_preserves_all_blockers_and_excludes_publication_hold(service, monkeypatch):
    d = make(service)
    cid = d['case']['id']
    proposal = draft(service, access_immediate_review=True)
    with service.db.tx() as c:
        current = service.db.case(c, cid)
        current['policy_pending'] = True
        service.db.save_case(c, current)
        service.db.add(c, 'action', {'business_id': 'uncertain-old-operation', 'status': 'uncertain'}, cid)
    at = now()
    monkeypatch.setattr(insights, 'now', lambda: at)
    result = compare(service, proposal)
    row = result['rows'][0]
    assert result['as_of'] == row['before']['assessed_at'] == row['after']['assessed_at'] == stamp(at)
    before = {b['key']: b for b in row['before']['blockers']}
    after = {b['key']: b for b in row['after']['blockers']}
    assert {'access', 'authority', 'schedule', 'evidence', 'total', 'automation'} <= after.keys()
    assert 'policy' not in before and 'policy' not in after
    assert before['access']['response'] == 'CLARIFY'
    assert after['access']['response'] == 'HUMAN REVIEW'
    assert any(x['key'] == 'blocker:access:require-access' for x in row['changes'])
    assert any('pure policy outcomes' in x for x in result['assumptions'])


def test_policy_comparison_keeps_custom_blocker_changes_even_if_outcome_unchanged(service):
    d = make(service)
    current = service.policies()['active']
    proposal = service.draft(PolicyInput(base_version=current['version'], settings=current['settings'], rules=[{
        'id': 'schedule-owner', 'conditions': [{'key': 'schedule', 'status': 'UNKNOWN'}],
        'actions': ['instruct_work'], 'response': 'WAIT', 'owner': 'reviewer'}]), actor('policy_editor'))
    row = compare(service, proposal, [d['case']['id']])['rows'][0]
    assert row['before']['outcome'] == row['after']['outcome'] == 'HUMAN REVIEW'
    assert any(change['key'] == 'blocker:rule:schedule-owner:schedule-owner' for change in row['changes'])


def test_approval_version_expiry_and_revocation_are_respected(service, monkeypatch):
    d = make(service, 'archive')
    cid = d['case']['id']
    proposal = draft(service)
    at = now()
    with service.db.tx() as c:
        grant, _ = service.db.add(c, 'approval', {'key': 'authority', 'scope': scope_of(d['case']),
            'action_revision': d['case']['action_revision'], 'policy_version': 1,
            'expires_at': stamp(at + timedelta(hours=1)), 'source_id': d['evidence'][0]['id']}, cid)
    monkeypatch.setattr(insights, 'now', lambda: at)
    row = compare(service, proposal)['rows'][0]
    assert row['before']['outcome'] == 'ACT'
    assert row['after']['outcome'] == 'HUMAN REVIEW'
    monkeypatch.setattr(insights, 'now', lambda: at + timedelta(hours=2))
    assert compare(service, proposal)['rows'][0]['before']['outcome'] == 'HUMAN REVIEW'
    monkeypatch.setattr(insights, 'now', lambda: at)
    with service.db.tx() as c:
        service.db.add(c, 'approval_revoked', {'approval_id': grant['id']}, cid)
    assert compare(service, proposal)['rows'][0]['before']['outcome'] == 'HUMAN REVIEW'


def test_completed_business_action_retains_recorded_decision_and_receipt(service):
    d = make(service, 'request_quote')
    cid = d['case']['id']
    receipt = service.execute(cid, actor())['action']
    proposal = draft(service, required_per_action={'request_quote': ['access']})
    row = compare(service, proposal)['rows'][0]
    assert row['completed']
    assert row['before'] == row['after']
    assert row['before']['outcome'] == 'NO FURTHER ACTION'
    assert row['before']['recorded_decision']['id'] == receipt['decision_id']
    assert row['before']['recorded_decision']['outcome'] == 'ACT'
    assert row['receipt']['id'] == receipt['receipt_id']
    assert row['changes'] == []


def test_stale_drafts_are_labelled_and_do_not_reuse_active_version(service):
    make(service)
    stale = draft(service, access_immediate_review=True)
    replacement = draft(service, reminder_hours=4)
    service.preview(replacement['id'], actor('policy_editor'))
    service.publish(replacement['id'], actor('policy_editor'))
    result = compare(service, stale)
    assert result['stale_base']
    assert result['active_version'] == 2
    assert result['proposed_version'] == 3
    assert result['rows'][0]['after']['policy_version'] == 3


def test_both_views_are_read_only_and_validate_selection(service):
    cid = make(service)['case']['id']
    proposal = draft(service)
    before = stored_state(service)
    case_insights(service, cid, actor())
    compare(service, proposal)
    compare(service, proposal, [])
    assert stored_state(service) == before
    assert compare(service, proposal, [])['rows'] == []
    assert len(compare(service, proposal, [cid, cid])['rows']) == 1
    with pytest.raises(ValueError, match='Case not found'):
        compare(service, proposal, ['absent-case'])
    with pytest.raises(ValueError, match='policy draft'):
        compare(service, service.policies()['active'])
    with pytest.raises(Forbidden):
        compare_policy(service, PolicyComparisonInput(draft_id=proposal['id']), actor())
    with pytest.raises(Forbidden):
        case_insights(service, cid, actor('tenant'))


def test_router_role_and_request_validation(service, monkeypatch):
    monkeypatch.setattr(insights, 'get_service', lambda: service)
    app = FastAPI()

    def test_actor(x_test_role: str = Header(default='unauthenticated')):
        return actor(x_test_role)

    @app.exception_handler(Forbidden)
    async def forbidden(_request, exc):
        return JSONResponse({'detail': str(exc)}, status_code=403)

    app.include_router(create_insights_router(test_actor))
    cid = make(service)['case']['id']
    proposal = draft(service)
    with TestClient(app) as client:
        assert client.get(f'/api/cases/{cid}/insights').status_code == 403
        assert client.get(f'/api/cases/{cid}/insights', headers={'x-test-role': 'reviewer'}).status_code == 200
        body = {'draft_id': proposal['id'], 'case_ids': [cid]}
        assert client.post('/api/policy-comparison', json=body, headers={'x-test-role': 'case_manager'}).status_code == 403
        assert client.post('/api/policy-comparison', json=body, headers={'x-test-role': 'policy_editor'}).status_code == 200
        assert client.post('/api/policy-comparison', json={**body, 'publish': True}, headers={'x-test-role': 'policy_editor'}).status_code == 422
