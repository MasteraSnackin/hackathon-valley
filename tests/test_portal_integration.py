"""Independent HTTP checks for tenant/staff separation and the learning loop.

Fictional inputs only. These exercise the mounted routes, shared case service,
and existing publication gates with an isolated temporary database.
"""
import pytest
from fastapi.testclient import TestClient
from app import main, service
from app.service import Service
from app.store import Store


@pytest.fixture
def portal(tmp_path, monkeypatch):
    monkeypatch.setattr(service, '_service', Service(Store('sqlite:///' + str(tmp_path / 'portal.db'))))
    monkeypatch.setattr(main, 'WORKFLOW_MODE', 'manual_demo')
    # Offline: no model credential, so Claude triage hands messages to staff.
    monkeypatch.delenv('ANTHROPIC_API_KEY', raising=False)
    with TestClient(main.app) as client:
        yield client


def staff(client, role='case_manager'):
    response = client.post('/api/demo-session', json={'role': role})
    assert response.status_code == 200, response.text


def test_tenant_request_becomes_one_shared_staff_case(portal):
    assert portal.post('/api/tenant/session').status_code == 200
    submitted = {'text': 'My name is Alex Taylor. I live at 18 Example Road. My kitchen tap is leaking.', 'idempotency_key': 'fictional-intake-1'}
    response = portal.post('/api/tenant/conversations', json=submitted)
    assert response.status_code == 200, response.text
    conversation = response.json()
    assert conversation['case_id'] and not conversation['missing_fields']
    assert portal.post('/api/tenant/conversations', json=submitted).json()['id'] == conversation['id']
    assert portal.get('/api/cases').status_code == 403
    assert portal.get('/api/policies').status_code == 403
    assert portal.post('/api/policy-assistant/interpret', json={'text': 'Set the spending review threshold to £250'}).status_code == 403
    staff(portal)
    cases = portal.get('/api/cases').json()
    assert len(cases) == 1 and cases[0]['id'] == conversation['case_id']
    detail = portal.get('/api/cases/' + conversation['case_id']).json()
    assert any(submitted['text'] in item['text'] for item in detail['evidence'])
    assert not any(c['key'] == 'identity' and c['verified'] for c in detail['claims'])
    before = detail['case']['revision']
    note = {'text': 'The leak is now reaching the floor.', 'idempotency_key': 'fictional-followup-1'}
    assert portal.post('/api/tenant/conversations/' + conversation['id'] + '/messages', json=note).status_code == 200
    assert portal.post('/api/tenant/conversations/' + conversation['id'] + '/messages', json=note).status_code == 200
    after = portal.get('/api/cases/' + conversation['case_id']).json()
    # One stored update (the repeat is deduplicated), then its manual-mode reading.
    assert after['case']['revision'] > before
    assert sum(item['text'] == note['text'] for item in after['evidence']) == 1


def test_tenant_mutations_obey_same_origin(portal):
    response = portal.post('/api/tenant/session', headers={'Origin': 'https://untrusted.example'})
    assert response.status_code == 403
    assert portal.get('/api/tenant/session').json()['active'] is False


def test_policy_interpretation_cannot_publish_without_existing_role_and_preview(portal):
    staff(portal)
    active = portal.get('/api/policies').json()['active']
    result = portal.post('/api/policy-assistant/interpret', json={'text': 'Set the spending review threshold to £250'})
    assert result.status_code == 200, result.text
    suggestion = result.json()
    assert suggestion['status'] == 'ready', suggestion
    assert suggestion['draft']['settings']['review_limit'] == 250
    assert portal.get('/api/policies').json()['active'] == active
    assert portal.get('/api/policies').json()['drafts'] == []
    assert portal.post('/api/policies/draft', json=suggestion['draft']).status_code == 403
    staff(portal, 'policy_editor')
    draft = portal.post('/api/policies/draft', json=suggestion['draft']).json()
    assert portal.post(f"/api/policies/{draft['id']}/publish").status_code == 409
    assert portal.post(f"/api/policies/{draft['id']}/preview").status_code == 200
    published = portal.post(f"/api/policies/{draft['id']}/publish")
    assert published.status_code == 200, published.text
    assert published.json()['settings']['review_limit'] == 250
    assert published.json()['version'] == active['version'] + 1


def test_resolved_access_review_suggests_policy_without_granting_global_permission(portal):
    staff(portal, 'policy_editor')
    active = portal.get('/api/policies').json()['active']
    draft = portal.post('/api/policies/draft', json={
        'base_version': active['version'],
        'settings': {**active['settings'], 'access_immediate_review': True},
        'rules': active['rules'], 'reason': 'Fictional review flow check',
    }).json()
    assert portal.post(f"/api/policies/{draft['id']}/preview").status_code == 200
    assert portal.post(f"/api/policies/{draft['id']}/publish").status_code == 200
    staff(portal)
    detail = portal.post('/api/cases', json={
        'title': 'Fictional window repair', 'property_ref': 'DEMO-FLAT-1',
        'report': 'The window handle is broken.', 'category': 'windows',
        'action': 'instruct_work', 'triage': 'staff',
    }).json()
    review = next(r for r in detail['reviews'] if r['key'] == 'access' and r['status'] == 'open')
    staff(portal, 'access_officer')
    resolved = portal.post('/api/reviews/' + review['id'] + '/respond', json={
        'decision': 'reject', 'reason': 'Do not enter before permission for this visit is established.',
    })
    assert resolved.status_code == 200, resolved.text
    policies_before = portal.get('/api/policies').json()
    response = portal.get('/api/policy-assistant/reviews/' + review['id'] + '/suggestion')
    assert response.status_code == 200, response.text
    suggestion = response.json()
    assert suggestion['source_review_id'] == review['id']
    assert suggestion['suggested_text']
    assert portal.get('/api/policies').json() == policies_before
    # The review decision still blocks this case; suggesting a reusable rule
    # must never mint a permission claim or approve unrelated work.
    current = portal.get('/api/cases/' + detail['case']['id']).json()
    assert current['decision']['outcome'] != 'ACT'
    assert not any(c['key'] == 'access' and c['verified'] and c['value'] for c in current['claims'])
