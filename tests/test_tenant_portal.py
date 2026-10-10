"""Fictional tenant inputs; no corpus, production data or live model is used."""
import json
from concurrent.futures import ThreadPoolExecutor

import pytest
from fastapi import FastAPI
from fastapi.testclient import TestClient

from app import service as service_module
from app.service import Service
from app.store import Store
from app import ai, tenant as tenant_module
from app.tenant import CLARIFY_OPENING, COOKIE, READY_REPLY, SENT_REPLY, create_tenant_router, extract_fields


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


def confirm(client, cid):
    return client.post(f'/api/tenant/conversations/{cid}/confirm')


def submitted(client, text=COMPLETE, key='first'):
    """Report, check the summary and confirm it: the only route to a shared case."""
    first = report(client, text, key).json()
    assert first['awaiting_confirmation'] and first['case_id'] is None
    result = confirm(client, first['id'])
    assert result.status_code == 200, result.text
    return result.json()


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


def test_complete_message_waits_for_tenant_confirmation_before_shared_case(portal):
    client, service, wakes, _ = portal
    response = start(client)
    cookie = response.headers['set-cookie']
    assert 'HttpOnly' in cookie and 'SameSite=strict' in cookie and 'Path=/api/tenant' in cookie
    assert response.json()['active'] is True
    assert 'literal demo parser' in response.json()['authentication']
    pending = report(client).json()
    assert pending['case_id'] is None and pending['missing_fields'] == []
    assert pending['awaiting_confirmation'] and pending['status'] == 'awaiting_confirmation'
    assert pending['summary'] == {'name': 'Alex Taylor', 'address': '18 Example Road',
                                  'problems': ['My kitchen tap is leaking']}
    assert pending['messages'][-1]['text'] == READY_REPLY
    assert service.list_cases() == [] and wakes == []
    result = confirm(client, pending['id']).json()
    assert result['case_id'] and not result['awaiting_confirmation']
    assert result['fields']['name'] == 'Alex Taylor'
    assert result['messages'][0]['text'] == COMPLETE
    assert len(result['messages']) == 4
    assert result['messages'][-1]['text'] == SENT_REPLY
    assert result['status'] == 'submitted' and result['next_step'] == 'Your property manager will check the details.'
    detail = service.detail(result['case_id'])
    assert detail['evidence'][0]['text'].startswith(COMPLETE + '\n\nSummary checked and confirmed by the tenant:')
    assert '- My kitchen tap is leaking' in detail['evidence'][0]['text']
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
    ask = result['messages'][-1]['text']
    assert ask.startswith(CLARIFY_OPENING) and 'name?' in ask and 'address of the property?' in ask
    address = 'Address: 42 Example Lane'
    result = message(client, result['id'], address).json()
    assert result['missing_fields'] == ['name']
    assert result['messages'][-1]['text'] == CLARIFY_OPENING + '\n- What’s your name?'
    result = message(client, result['id'], 'Jamie Fiction', 'name').json()
    assert result['awaiting_confirmation'] and not result['missing_fields'] and not result['case_id']
    result = confirm(client, result['id']).json()
    assert [m['text'] for m in result['messages'] if m['role'] == 'user'][:3] == [original, address, 'Jamie Fiction']
    assert service.detail(result['case_id'])['evidence'][0]['text'].startswith(original + '\n\n' + address + '\n\nJamie Fiction\n\n')


def test_name_and_address_do_not_invent_an_issue(portal):
    client, _, _, _ = portal
    start(client)
    result = report(client, 'My name is Alex Taylor. I live at 18 Example Road.').json()
    assert result['missing_fields'] == ['issue']
    assert result['case_id'] is None
    result = message(client, result['id'], 'The light flickers every evening.').json()
    assert result['awaiting_confirmation'] and result['fields']['issue'] == 'The light flickers every evening'


def test_duplicates_do_not_duplicate_messages_cases_or_evidence(portal):
    client, service, _, _ = portal
    start(client)
    pending = report(client).json()
    assert report(client).json() == pending
    first = confirm(client, pending['id']).json()
    assert confirm(client, pending['id']).json() == first
    update = 'I grant permission for the repair. The tap is still leaking.'
    second = message(client, first['id'], update).json()
    assert message(client, first['id'], update).json() == second
    assert len(second['messages']) == 6
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
    first = submitted(client)
    with TestClient(app) as other:
        other.cookies.set('pw_session', 'a-staff-cookie')
        assert other.get('/api/tenant/session').json()['active'] is False
        assert report(other).status_code == 403
        start(other)
        assert other.get('/api/tenant/session').json()['conversations'] == []
        assert other.get('/api/tenant/conversations/' + first['id']).status_code == 404
        assert message(other, first['id'], 'Please change this').status_code == 404
        assert confirm(other, first['id']).status_code == 404
        second = submitted(other)
        assert second['id'] != first['id'] and second['case_id'] != first['case_id']


def test_staff_data_cannot_leak_through_case_projection(portal):
    client, service, _, _ = portal
    start(client)
    result = submitted(client)
    marker = 'PRIVATE STAFF NOTE NEVER RETURN'
    with service.db.tx() as c:
        case = service.db.case(c, result['case_id'])
        case.update(next_step=marker, stage=marker, owner=marker)
        service.db.save_case(c, case)
        for kind in ('evidence', 'review', 'policy'):
            service.db.add(c, kind, {'text': marker}, case['id'])
    projection = client.get('/api/tenant/conversations/' + result['id']).json()
    assert marker not in json.dumps(projection)
    assert set(projection) == {'id', 'case_id', 'title', 'status', 'stage', 'fields', 'missing_fields',
                               'summary', 'awaiting_confirmation', 'messages', 'next_step', 'updated_at'}
    assert marker not in client.get('/api/tenant/session').text


def test_reserved_demo_address_and_corrections_never_verify_identity(portal):
    client, service, _, _ = portal
    start(client)
    first = submitted(client, 'Name: Sam Sample\nAddress: DEMO-FLAT-1\nIssue: A tap is leaking.')
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
    assert complete['awaiting_confirmation'] and complete['missing_fields'] == []


def test_name_and_address_can_be_supplied_together_without_labels(portal):
    client, _, _, _ = portal
    start(client)
    result = report(client, 'The tap is leaking.').json()
    assert result['missing_fields'] == ['name', 'address']
    result = message(client, result['id'], 'Alex Taylor, 18 Example Road').json()
    assert result['fields']['name'] == 'Alex Taylor'
    assert result['fields']['address'] == '18 Example Road'
    assert result['missing_fields'] == [] and result['awaiting_confirmation']


def test_retry_recovers_after_case_commit_before_conversation_link(portal, monkeypatch):
    client, service, _, _ = portal
    start(client)
    original = service.intake
    once = True

    def fail_after_commit(*args):
        nonlocal once
        result = original(*args)
        if once:
            once = False
            raise RuntimeError('simulated interrupted reply')
        return result

    monkeypatch.setattr(service, 'intake', fail_after_commit)
    pending = report(client).json()
    with pytest.raises(RuntimeError, match='interrupted reply'):
        confirm(client, pending['id'])
    result = confirm(client, pending['id']).json()
    assert result['case_id'] and len(result['messages']) == 4
    assert len(service.list_cases()) == 1
    assert len(service.detail(result['case_id'])['evidence']) == 1


def test_simultaneous_duplicate_intakes_and_messages_converge(portal):
    client, service, _, _ = portal
    start(client)
    with ThreadPoolExecutor(max_workers=2) as pool:
        results = list(pool.map(lambda _: report(client).json(), range(2)))
    assert results[0]['id'] == results[1]['id']
    cid = results[0]['id']
    with ThreadPoolExecutor(max_workers=2) as pool:
        confirmed = list(pool.map(lambda _: confirm(client, cid).json(), range(2)))
    assert confirmed[0]['case_id'] and confirmed[0]['case_id'] == confirmed[1]['case_id']
    with ThreadPoolExecutor(max_workers=2) as pool:
        updates = list(pool.map(lambda _: message(client, cid, 'The tap still drips.').json(), range(2)))
    assert all(len(update['messages']) == 6 for update in updates)
    assert len(service.list_cases()) == 1
    assert len(service.detail(confirmed[0]['case_id'])['evidence']) == 2


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
            ('POST', '/api/tenant/conversations/unknown/confirm', None),
        ]:
            assert client.request(method, path, json=body).status_code == 403


def test_nothing_to_confirm_until_details_are_complete(portal):
    client, service, wakes, _ = portal
    start(client)
    result = report(client, 'The tap is leaking.').json()
    assert confirm(client, result['id']).status_code == 409
    assert service.list_cases() == [] and wakes == []


def test_correction_while_awaiting_confirmation_refreshes_summary(portal):
    client, service, _, _ = portal
    start(client)
    pending = report(client).json()
    corrected = message(client, pending['id'], 'Address: 19 Other Road').json()
    assert corrected['awaiting_confirmation'] and corrected['case_id'] is None
    assert corrected['summary']['address'] == '19 Other Road'
    result = confirm(client, pending['id']).json()
    assert service.detail(result['case_id'])['case']['property_ref'] == 'Unverified address: 19 Other Road'


def reading(**overrides):
    base = {'name': None, 'address': None, 'problems': [], 'questions': [], 'reply': '',
            'ready': False, 'confirms_summary': False, 'danger': False}
    return {**base, **overrides}


@pytest.fixture
def scripted_claude(monkeypatch):
    """Offline stand-in for Claude's intake reading; the real gates still apply."""
    replies = []
    monkeypatch.setattr(ai, 'configured', lambda: True)
    monkeypatch.setattr(ai, 'tenant_intake', lambda messages, shown: (replies.pop(0), {'model': 'scripted'}))
    return replies


GARDEN = 'Weeds all over the shared garden and the hedge by the side path is overgrown.'


def test_claude_asks_friendly_questions_then_tenant_confirms_by_reply(portal, scripted_claude):
    client, service, wakes, _ = portal
    start(client)
    ask = CLARIFY_OPENING + '\n- What’s your name?\n- What’s the address of the property?'
    scripted_claude.append(reading(
        problems=[{'summary': 'Weeds in the shared garden', 'source_quote': 'Weeds all over the shared garden'},
                  {'summary': 'Overgrown hedge by the side path', 'source_quote': 'the hedge by the side path is overgrown'}],
        questions=['What’s your name?', 'What’s the address of the property?'], reply=ask))
    first = report(client, GARDEN).json()
    assert first['messages'][-1]['text'] == ask and first['case_id'] is None
    assert not first['awaiting_confirmation'] and service.list_cases() == []
    scripted_claude.append(reading(
        name='Robin Example', address='Flat 4, 9 Sample Walk',
        problems=[{'summary': 'Weeds in the shared garden', 'source_quote': 'Weeds all over the shared garden'},
                  {'summary': 'Overgrown hedge by the side path', 'source_quote': 'the hedge by the side path is overgrown'}],
        ready=True, reply='Thanks Robin! Please check the summary below before I send it.'))
    second = message(client, first['id'], 'Robin Example, Flat 4, 9 Sample Walk').json()
    assert second['awaiting_confirmation'] and second['case_id'] is None
    assert second['summary']['problems'] == ['Weeds in the shared garden', 'Overgrown hedge by the side path']
    assert second['title'] == 'Weeds in the shared garden'
    scripted_claude.append(reading(confirms_summary=True))
    third = message(client, first['id'], 'Yes that is all correct', 'yes').json()
    assert third['case_id'] and third['messages'][-1]['text'] == SENT_REPLY
    assert wakes == [third['case_id']]
    report_text = service.detail(third['case_id'])['evidence'][0]['text']
    assert report_text.startswith(GARDEN) and '- Overgrown hedge by the side path' in report_text
    assert service.detail(third['case_id'])['case']['property_ref'] == 'Unverified address: Flat 4, 9 Sample Walk'


def test_claude_cannot_invent_details_or_skip_the_gate(portal, scripted_claude):
    client, service, _, _ = portal
    start(client)
    # Claude claims readiness with a name and address the tenant never wrote.
    scripted_claude.append(reading(name='Invented Person', address='1 Nowhere Road',
                                   problems=[{'summary': 'Garden', 'source_quote': 'Weeds all over the shared garden'}],
                                   ready=True, reply='All done!', danger=True))
    result = report(client, GARDEN).json()
    assert not result['awaiting_confirmation'] and result['summary'] is None
    assert result['fields']['name'] is None and result['fields']['address'] is None
    text = result['messages'][-1]['text']
    assert text.startswith('If anyone is in danger right now, please call 999.')
    assert CLARIFY_OPENING in text
    # A confirmation is ignored when no summary was shown.
    scripted_claude.append(reading(confirms_summary=True, questions=['What’s your name?'], reply=CLARIFY_OPENING + '\n- What’s your name?'))
    assert message(client, result['id'], 'yes').json()['case_id'] is None
    assert service.list_cases() == []


def test_claude_unavailable_falls_back_to_the_local_parser(portal, monkeypatch):
    client, _, _, _ = portal
    monkeypatch.setattr(ai, 'configured', lambda: True)

    def unavailable(messages, shown):
        raise ai.ClaudeUnavailable('APIConnectionError', 'connection failed')

    monkeypatch.setattr(ai, 'tenant_intake', unavailable)
    start(client)
    result = report(client).json()
    assert result['awaiting_confirmation'] and result['messages'][-1]['text'] == READY_REPLY


@pytest.mark.claude
def test_live_claude_reads_a_fictional_garden_report():
    messages = [{'role': 'user', 'text': GARDEN}]
    result, meta = ai.tenant_intake(messages, None)
    checked = ai.checked_intake(result, GARDEN)
    assert meta['model'] and not checked['ready']
    assert checked['name'] is None and checked['address'] is None
    assert checked['reply'].startswith(CLARIFY_OPENING)
    assert len(checked['problems']) >= 2
