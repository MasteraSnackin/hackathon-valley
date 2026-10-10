"""Fictional tenant inputs; no corpus, production data or live model is used."""
import json
from concurrent.futures import ThreadPoolExecutor

import pytest
from fastapi import FastAPI
from fastapi.testclient import TestClient

from app import service as service_module
from app.service import Service
from app.store import Store
from app.tenant import COOKIE, create_tenant_router, extract_fields


COMPLETE = 'My name is Alex Taylor. I live at 18 Example Road. My kitchen tap is leaking.'


@pytest.fixture
def portal(tmp_path, monkeypatch):
    # Offline: no model credential, so Claude triage hands messages to staff.
    monkeypatch.delenv('ANTHROPIC_API_KEY', raising=False)
    service = Service(Store('sqlite:///' + str(tmp_path / 'tenant.db')))
    monkeypatch.setattr(service_module, '_service', service)
    wakes = []

    async def wake(cid):
        # The shared case and its conversation link must both be committed first.
        with service.db.tx() as c:
            service.db.case(c, cid)
        wakes.append(cid)

    app = FastAPI()
    app.include_router(create_tenant_router(wake))
    with TestClient(app) as client:
        yield client, service, wakes, app


def start(client):
    response = client.post('/api/tenant/session')
    assert response.status_code == 200, response.text
    return response


def report(client, text=COMPLETE, key='first'):
    return client.post('/api/tenant/conversations', json={'text': text, 'idempotency_key': key})


def message(client, cid, text, key='followup'):
    return client.post(f'/api/tenant/conversations/{cid}/messages',
                       json={'text': text, 'idempotency_key': key})


@pytest.mark.parametrize('text, name, address, issue', [
    (COMPLETE, 'Alex Taylor', '18 Example Road', 'My kitchen tap is leaking'),
    ("I'm Morgan Reed at 27 Fictional Street. The boiler is broken.",
     'Morgan Reed', '27 Fictional Street', 'The boiler is broken'),
    ('Name: Sam Sample\nAddress: Flat 2, 32 Sample Road\nIssue: The door will not close.',
     'Sam Sample', 'Flat 2, 32 Sample Road', 'The door will not close'),
    ('Hi, this is Sam Taylor at 14 Sample Avenue. The dishwasher won’t drain.',
     'Sam Taylor', '14 Sample Avenue', 'The dishwasher won’t drain'),
])
def test_complete_common_phrases(text, name, address, issue):
    assert extract_fields(text) == {'name': name, 'address': address, 'issue': issue}


def test_complete_initial_message_creates_shared_case_without_redundant_questions(portal):
    client, service, wakes, _ = portal
    response = start(client)
    cookie = response.headers['set-cookie']
    assert 'HttpOnly' in cookie and 'SameSite=strict' in cookie and 'Path=/api/tenant' in cookie
    assert response.json()['active'] is True
    assert 'literal demo parser' in response.json()['authentication']
    result = report(client).json()
    assert result['case_id'] and result['missing_fields'] == []
    assert result['fields']['name'] == 'Alex Taylor'
    assert result['messages'][0]['text'] == COMPLETE
    assert len(result['messages']) == 2
    assert '?' not in result['messages'][1]['text']
    detail = service.detail(result['case_id'])
    assert detail['evidence'][0]['text'] == COMPLETE
    assert detail['case']['property_ref'] == 'Unverified address: 18 Example Road'
    assert not any(claim['verified'] for claim in detail['claims']
                   if claim['key'] in {'identity', 'route', 'access', 'authority'})
    assert detail['decision']['outcome'] != 'ACT'
    assert wakes == [result['case_id']]
    assert client.get('/api/tenant/session').json()['conversations'][0]['id'] == result['id']


def test_only_missing_fields_are_requested_and_raw_sources_survive(portal):
    client, service, _, _ = portal
    start(client)
    original = '  The shower is leaking.\n'
    result = report(client, original).json()
    assert result['case_id'] is None
    assert result['missing_fields'] == ['name', 'address']
    assert result['messages'][-1]['text'].endswith('your name and the property address.')
    address = 'Address: 42 Example Lane'
    result = message(client, result['id'], address).json()
    assert result['missing_fields'] == ['name']
    assert result['messages'][-1]['text'].endswith('your name.')
    result = message(client, result['id'], 'Jamie Fiction', 'name').json()
    assert result['case_id'] and not result['missing_fields']
    assert [m['text'] for m in result['messages'] if m['role'] == 'user'] == [original, address, 'Jamie Fiction']
    assert service.detail(result['case_id'])['evidence'][0]['text'] == original + '\n\n' + address + '\n\nJamie Fiction'


def test_name_and_address_do_not_invent_an_issue(portal):
    client, _, _, _ = portal
    start(client)
    result = report(client, 'My name is Alex Taylor. I live at 18 Example Road.').json()
    assert result['missing_fields'] == ['issue']
    assert result['case_id'] is None
    result = message(client, result['id'], 'The light flickers every evening.').json()
    assert result['case_id'] and result['fields']['issue'] == 'The light flickers every evening'


def test_duplicates_do_not_duplicate_messages_cases_or_evidence(portal):
    client, service, _, _ = portal
    start(client)
    first = report(client).json()
    assert report(client).json() == first
    update = 'I grant permission for the repair. The tap is still leaking.'
    second = message(client, first['id'], update).json()
    assert message(client, first['id'], update).json() == second
    assert len(second['messages']) == 4
    assert len(service.list_cases()) == 1
    detail = service.detail(first['case_id'])
    assert len(detail['evidence']) == 2
    assert detail['evidence'][-1]['text'] == update
    assert all(not claim['verified'] for claim in detail['claims'] if claim['key'] == 'access')
    assert report(client, 'Issue: Different text').status_code == 409
    assert message(client, first['id'], 'Different update').status_code == 409


def test_cross_tenant_ownership_and_staff_cookie_cannot_authenticate(portal):
    client, _, _, app = portal
    start(client)
    first = report(client).json()
    with TestClient(app) as other:
        other.cookies.set('pw_session', 'a-staff-cookie')
        assert other.get('/api/tenant/session').json()['active'] is False
        assert report(other).status_code == 403
        start(other)
        assert other.get('/api/tenant/session').json()['conversations'] == []
        assert other.get('/api/tenant/conversations/' + first['id']).status_code == 404
        assert message(other, first['id'], 'Please change this').status_code == 404
        second = report(other).json()
        assert second['id'] != first['id'] and second['case_id'] != first['case_id']


def test_staff_data_cannot_leak_through_case_projection(portal):
    client, service, _, _ = portal
    start(client)
    result = report(client).json()
    marker = 'PRIVATE STAFF NOTE NEVER RETURN'
    with service.db.tx() as c:
        case = service.db.case(c, result['case_id'])
        case.update(next_step=marker, stage=marker, owner=marker)
        service.db.save_case(c, case)
        for kind in ('evidence', 'review', 'policy'):
            service.db.add(c, kind, {'text': marker}, case['id'])
    projection = client.get('/api/tenant/conversations/' + result['id']).json()
    assert marker not in json.dumps(projection)
    assert set(projection) == {'id', 'case_id', 'title', 'status', 'stage', 'fields',
                               'missing_fields', 'messages', 'next_step', 'updated_at'}
    assert marker not in client.get('/api/tenant/session').text


def test_reserved_demo_address_and_corrections_never_verify_identity(portal):
    client, service, _, _ = portal
    start(client)
    first = report(client, 'Name: Sam Sample\nAddress: DEMO-FLAT-1\nIssue: A tap is leaking.').json()
    assert first['case_id']
    detail = service.detail(first['case_id'])
    assert detail['case']['property_ref'] == 'Unverified address: DEMO-FLAT-1'
    assert not any(claim['key'] in {'identity', 'route'} and claim['verified'] for claim in detail['claims'])
    second = message(client, first['id'], 'Address: 19 Other Road').json()
    assert second['fields']['address'] == '19 Other Road'
    assert 'will check your corrected details' in second['next_step']
    assert 'corrected details' in second['messages'][-1]['text']
    detail = service.detail(first['case_id'])
    assert detail['case']['property_ref'] == 'Unverified address: DEMO-FLAT-1'
    assert detail['evidence'][-1]['text'] == 'Address: 19 Other Road'


def test_conversation_and_identity_survive_service_recreation(portal, monkeypatch):
    client, service, _, _ = portal
    start(client)
    result = report(client).json()
    replacement = Service(Store(str(service.db.engine.url)))
    monkeypatch.setattr(service_module, '_service', replacement)
    assert client.get('/api/tenant/session').json()['active'] is True
    assert client.get('/api/tenant/conversations/' + result['id']).json() == result


def test_single_missing_address_accepts_bare_building_but_not_repair_prose(portal):
    client, _, _, _ = portal
    start(client)
    first = report(client, 'My name is Alex Taylor. The tap is leaking.').json()
    assert first['missing_fields'] == ['address']
    still_missing = message(client, first['id'], 'The leak is getting worse.').json()
    assert still_missing['missing_fields'] == ['address']
    complete = message(client, first['id'], 'Flat 7, Willow House', 'address').json()
    assert complete['fields']['address'] == 'Flat 7, Willow House'
    assert complete['case_id'] and complete['missing_fields'] == []


def test_name_and_address_can_be_supplied_together_without_labels(portal):
    client, _, _, _ = portal
    start(client)
    result = report(client, 'The tap is leaking.').json()
    assert result['missing_fields'] == ['name', 'address']
    result = message(client, result['id'], 'Alex Taylor, 18 Example Road').json()
    assert result['fields']['name'] == 'Alex Taylor'
    assert result['fields']['address'] == '18 Example Road'
    assert result['missing_fields'] == [] and result['case_id']


def test_retry_recovers_after_case_commit_before_conversation_link(portal, monkeypatch):
    client, service, _, _ = portal
    start(client)
    original = service.intake
    once = True

    def fail_after_commit(*args, **kwargs):
        nonlocal once
        result = original(*args, **kwargs)
        if once:
            once = False
            raise RuntimeError('simulated interrupted reply')
        return result

    monkeypatch.setattr(service, 'intake', fail_after_commit)
    with pytest.raises(RuntimeError, match='interrupted reply'):
        report(client)
    result = report(client).json()
    assert result['case_id'] and len(result['messages']) == 2
    assert len(service.list_cases()) == 1
    assert len(service.detail(result['case_id'])['evidence']) == 1


def test_simultaneous_duplicate_intakes_and_messages_converge(portal):
    client, service, _, _ = portal
    start(client)
    with ThreadPoolExecutor(max_workers=2) as pool:
        results = list(pool.map(lambda _: report(client).json(), range(2)))
    assert results[0]['id'] == results[1]['id']
    assert results[0]['case_id'] == results[1]['case_id']
    cid = results[0]['id']
    with ThreadPoolExecutor(max_workers=2) as pool:
        updates = list(pool.map(lambda _: message(client, cid, 'The tap still drips.').json(), range(2)))
    assert all(len(update['messages']) == 4 for update in updates)
    assert len(service.list_cases()) == 1
    assert len(service.detail(results[0]['case_id'])['evidence']) == 2


def test_input_validation_and_same_origin_check(portal):
    client, service, _, _ = portal
    assert client.post('/api/tenant/session', headers={'Origin': 'https://elsewhere.example'}).status_code == 403
    start(client)
    assert report(client, '   ').status_code == 422
    assert client.post('/api/tenant/conversations', json={'text': COMPLETE, 'idempotency_key': 'x', 'role': 'case_manager'}).status_code == 422
    assert client.post('/api/tenant/conversations', json={'text': COMPLETE, 'idempotency_key': 'x'},
                       headers={'Origin': 'https://elsewhere.example'}).status_code == 403
    assert service.list_cases() == []


@pytest.mark.parametrize('mode, host', [('production', 'testclient'), ('demo', '203.0.113.23')])
def test_production_and_remote_demo_identity_are_disabled(portal, mode, host):
    _, _, _, _ = portal

    async def wake(_):
        raise AssertionError('No workflow may start')

    app = FastAPI()
    app.include_router(create_tenant_router(wake, mode=mode))
    with TestClient(app, client=(host, 50000)) as client:
        for method, path, body in [
            ('GET', '/api/tenant/session', None),
            ('POST', '/api/tenant/session', None),
            ('POST', '/api/tenant/conversations', {'text': COMPLETE, 'idempotency_key': 'x'}),
            ('GET', '/api/tenant/conversations/unknown', None),
            ('POST', '/api/tenant/conversations/unknown/messages', {'text': 'Update', 'idempotency_key': 'x'}),
        ]:
            assert client.request(method, path, json=body).status_code == 403


MANAGER = {'id': 'test-manager', 'role': 'case_manager'}
EDITOR = {'id': 'test-editor', 'role': 'policy_editor'}


def checks(service, case_id, action):
    """Route the case to an action (as a reading would) and return its identity/route checks."""
    from app.domain import ProposalInput
    detail = service.proposal(case_id, ProposalInput(action=action, category='plumbing', work_item='Kitchen tap leaking'), MANAGER)
    return {c['key']: c for c in detail['decision']['checks'] if c['key'] in {'identity', 'route'}}


def test_tenant_self_identification_unblocks_only_information_gathering(portal):
    client, service, _, _ = portal
    start(client)
    case_id = report(client).json()['case_id']
    sid = service.detail(case_id)['case']['self_identification']
    assert (sid['name'], sid['address'], sid['corrected']) == ('Alex Taylor', '18 Example Road', False)
    for action in ['clarify', 'request_quote']:
        found = checks(service, case_id, action)
        assert {k: c['status'] for k, c in found.items()} == {'identity': 'PASS', 'route': 'PASS'}
        assert 'Alex Taylor at 18 Example Road' in found['identity']['reason']
    # Visits, keys, work, closing and archiving still need the case manager.
    for action in ['confirm_appointment', 'supply_keys', 'instruct_work', 'close_item', 'archive']:
        assert checks(service, case_id, action)['identity']['status'] == 'UNKNOWN'
    # It never becomes a verified claim, so nothing else can reuse it.
    assert not any(c['key'] in {'identity', 'route'} and c['verified'] for c in service.detail(case_id)['claims'])


def test_corrected_details_return_identity_to_the_case_manager(portal):
    client, service, _, _ = portal
    start(client)
    first = report(client).json()
    assert checks(service, first['case_id'], 'request_quote')['identity']['status'] == 'PASS'
    message(client, first['id'], 'Address: 19 Other Road')
    case = service.detail(first['case_id'])['case']
    assert case['self_identification']['corrected'] and case['self_identification']['corrected_to']['address'] == '19 Other Road'
    assert checks(service, first['case_id'], 'request_quote')['identity']['status'] == 'UNKNOWN'


def test_policy_can_switch_tenant_self_identification_off(portal):
    from app.domain import PolicyInput
    client, service, _, _ = portal
    draft = service.draft(PolicyInput(base_version=1, settings={'tenant_self_identification': []}, reason='Always verify'), EDITOR)
    service.preview(draft['id'], EDITOR)
    service.publish(draft['id'], EDITOR)
    start(client)
    case_id = report(client).json()['case_id']
    assert checks(service, case_id, 'request_quote')['identity']['status'] == 'UNKNOWN'
    with pytest.raises(ValueError):
        PolicyInput(base_version=1, settings={'tenant_self_identification': ['instruct_work']})


def test_staff_intake_never_gets_self_identification(portal):
    from app.domain import Intake
    _, service, _, _ = portal
    detail = service.intake(Intake(title='Staff report', property_ref='18 Example Road', report='Name: Alex Taylor. Tap leaking.'), MANAGER)
    assert 'self_identification' not in detail['case']
    assert checks(service, detail['case']['id'], 'request_quote')['identity']['status'] == 'UNKNOWN'
