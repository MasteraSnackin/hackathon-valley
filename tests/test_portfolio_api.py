"""Portfolio HTTP boundaries on isolated fictional cases; no external services."""
from datetime import timedelta

import pytest
from fastapi.testclient import TestClient

from app import main, service
from app.domain import now, stamp
from app.service import Service
from app.store import Store


@pytest.fixture
def client(tmp_path, monkeypatch):
    monkeypatch.setattr(service, '_service', Service(Store('sqlite:///' + str(tmp_path / 'portfolio-api.db'))))
    monkeypatch.setattr(main, 'WORKFLOW_MODE', 'manual_demo')
    monkeypatch.setenv('ANTHROPIC_API_KEY', '')
    monkeypatch.setenv('ANTHROPIC_AUTH_TOKEN', '')
    monkeypatch.setenv('TYPESAFE_API_KEY', '')
    with TestClient(main.app) as connection:
        yield connection


def session(client, role='case_manager'):
    assert client.post('/api/demo-session', json={'role': role}).status_code == 200


def make_case(client, title):
    response = client.post('/api/cases', json={
        'title': title, 'property_ref': 'Fictional River Court',
        'report': 'The shared hot water supply is not working.',
        'category': 'plumbing', 'action': 'instruct_work', 'triage': 'staff',
        'work_item': 'Shared hot water supply',
    })
    assert response.status_code == 200, response.text
    return response.json()


def test_portfolio_requires_auth_and_manager_for_mutations(client):
    assert client.get('/api/portfolio').status_code == 403
    session(client)
    case = make_case(client, 'Fictional hot water report')
    cid = case['case']['id']
    profile = {'property_key': 'Fictional River Court', 'asset_ref': 'Boiler A', 'trade': 'plumbing', 'reason': 'Staff confirmed this fictional building grouping.'}
    assert client.post(f'/api/portfolio/cases/{cid}/profile', json=profile,
                       headers={'Origin': 'https://untrusted.example'}).status_code == 403
    session(client, 'reviewer')
    assert client.get(f'/api/cases/{cid}/insights').status_code == 200
    assert client.post(f'/api/portfolio/cases/{cid}/profile', json=profile).status_code == 403


def test_grouping_and_planning_never_clear_case_blockers(client):
    session(client)
    originals = [make_case(client, f'Fictional hot water report {n}') for n in (1, 2)]
    ids = [item['case']['id'] for item in originals]
    start, end = now() + timedelta(days=2), now() + timedelta(days=2, hours=2)
    for cid in ids:
        response = client.post(f'/api/portfolio/cases/{cid}/profile', json={
            'property_key': 'Fictional River Court', 'asset_ref': 'Shared boiler',
            'trade': 'plumbing', 'window_start': stamp(start), 'window_end': stamp(end),
            'reason': 'Confirmed grouping for the fictional planning test.',
        })
        assert response.status_code == 200, response.text
    overview = client.get('/api/portfolio').json()
    assert len(overview['profiles']) == 2
    assert overview['suggestions']
    incident = client.post('/api/portfolio/incidents', json={
        'case_ids': ids, 'title': 'Possible shared boiler fault',
        'reason': 'Same confirmed building, asset and reported symptoms.',
    })
    assert incident.status_code == 200, incident.text
    contractor = client.post('/api/portfolio/contractors', json={
        'name': 'Fictional plumbing team', 'trades': ['plumbing'],
        'available_from': stamp(start), 'available_until': stamp(end),
        'reason': 'Fictional availability supplied for this test.',
    })
    assert contractor.status_code == 200, contractor.text
    plan = client.post('/api/portfolio/plans', json={
        'contractor_id': contractor.json()['id'], 'case_ids': ids,
        'start': stamp(start), 'end': stamp(end), 'reason': 'Tentative shared inspection only.',
    })
    assert plan.status_code == 200, plan.text
    for original in originals:
        current = client.get('/api/cases/' + original['case']['id']).json()
        assert current['case']['revision'] == original['case']['revision']
        assert current['decision'] == original['decision']
        assert not current['actions']
        insights = client.get('/api/cases/' + current['case']['id'] + '/insights')
        assert insights.status_code == 200, insights.text
        assert insights.json()['frames']


def test_policy_comparison_is_role_checked_and_does_not_publish(client):
    session(client)
    case = make_case(client, 'Fictional access review')
    active = client.get('/api/policies').json()['active']
    session(client, 'policy_editor')
    draft = client.post('/api/policies/draft', json={
        'base_version': active['version'],
        'settings': {**active['settings'], 'access_immediate_review': True},
        'rules': active['rules'], 'reason': 'Compare missing access handling without publication.',
    })
    assert draft.status_code == 200, draft.text
    draft_id = draft.json()['id']
    with service.get_service().db.tx() as connection:
        before = service.get_service().db.list(connection)
    response = client.post('/api/policy-comparison', json={'draft_id': draft_id, 'case_ids': [case['case']['id']]})
    assert response.status_code == 200, response.text
    assert len(response.json()['rows']) == 1
    with service.get_service().db.tx() as connection:
        assert service.get_service().db.list(connection) == before
    assert client.get('/api/policies').json()['active']['id'] == active['id']
    session(client)
    assert client.post('/api/policy-comparison', json={'draft_id': draft_id}).status_code == 403
