"""Voice-bridge calls from tenants, landlords, letting agencies and contractors (offline).

Fakes stand in for Claude's reading and drafting; Jev has no credential, so
Claude reads every message. The directory and every call are fictional, and
all outbound messages are simulated.
"""
import pytest
from fastapi.testclient import TestClient
from app import ai
from app import service as service_module
from app.domain import InboundCall, ReviewResponse, EvidenceInput
from app.service import Service, Conflict
from app.store import Store

TENANT, LANDLORD, AGENCY, CONTRACTOR = '+447700900101', '07700 900201', '+44 7700 900301', '07700900401'
APPROVER = {'id': 'test-approver', 'role': 'approver'}


def reading(route='request_quote', quote='boiler', claims=(), answers=(), intent='new_request', work_item='Boiler not heating'):
    return {'intent': intent, 'summary': 'Fictional test reading.',
            'issues': [{'category': 'appliance', 'route': route, 'work_item': work_item, 'source_quote': quote, 'relation': 'current_case'}],
            'claims': list(claims), 'ambiguities': [], 'answers': list(answers), 'risk_flags': [], 'confidence': 'high',
            'rationale': 'Test.', 'route_objection': ''}


@pytest.fixture
def service(tmp_path):
    return Service(Store('sqlite:///' + str(tmp_path / 'inbound.db')))


@pytest.fixture
def models(monkeypatch):
    """Scripted Claude: the next reading is set per test step; drafts ask every open question."""
    calls = {'next': reading(), 'contexts': [], 'party_drafts': [], 'tenant_drafts': []}

    def triage(text, context, router=None):
        calls['contexts'].append(context)
        result = calls['next']
        return (result(context) if callable(result) else result), {'provider': 'anthropic', 'model': 'fake-claude'}

    def draft(kind):
        def run(context):
            calls[kind].append(context)
            return {'message': 'Fictional simulated question.', 'send_decision': 'auto_send', 'decision_reason': 'Gathers information only.', 'risk_flags': [],
                    'questions': [{'question_id': q['question_id'], 'topic': q['topic'], 'text': 'Question?', 'answer_type': 'free_text', 'options': []} for q in context['open_questions']]}, {'model': 'fake-claude'}
        return run

    monkeypatch.setattr(ai, 'triage', triage)
    monkeypatch.setattr(ai, 'draft_party_message', draft('party_drafts'))
    monkeypatch.setattr(ai, 'draft_tenant_message', draft('tenant_drafts'))
    return calls


def call(service, number, text, call_id, intent='report'):
    return service.inbound(InboundCall(call_id=call_id, caller_number=number, transcript=text, intent=intent), {'id': 'test-bridge', 'role': 'case_manager'})


def check(detail, key):
    return next((x for x in detail['decision']['checks'] if x['key'] == key), None)


def blocker(detail, key):
    return next((b for b in detail['decision']['blockers'] if b['key'] == key), None)


def quoted_case(service, models):
    """Tenant reports, the quote request runs, the contractor calls with a price."""
    reply = call(service, TENANT, 'Hi, the boiler is not heating the flat.', 'call-1')
    cid = reply['case_id']
    service.claude_steps(cid)
    service.tick(cid)  # the coordinator's cycle executes the simulated quote request
    models['next'] = reading(route='instruct_work', quote='£450 including VAT', intent='update',
                             claims=[{'key': 'total', 'value': True, 'amount': 450.0, 'source_quote': '£450 including VAT', 'issue_index': 0}])
    reply = call(service, CONTRACTOR, 'Quote for the boiler at Flat 7 Park View is £450 including VAT.', 'call-2')
    assert reply['case_id'] == cid and reply['outcome'] == 'attached'
    service.claude_steps(cid)
    return cid


def test_tenant_call_opens_a_case_on_the_directory_property(service, models):
    reply = call(service, TENANT, 'Hi, the boiler is not heating the flat.', 'call-1')
    assert reply['outcome'] == 'new_case' and reply['party']['kind'] == 'tenant' and reply['property']['ref'] == 'DEMO-PARK-7'
    assert 'Flat 7, Park View' in reply['say'] and reply['simulated'] is True
    service.claude_steps(reply['case_id'])
    detail = service.detail(reply['case_id'])
    report = next(e for e in detail['evidence'] if e.get('party'))
    assert report['party'] == {'kind': 'tenant', 'id': 'tenant-alex', 'name': 'Alex Taylor', 'verified': True, 'match': 'caller_id_fictional_directory'}
    assert check(detail, 'identity')['status'] == 'PASS' and check(detail, 'route')['status'] == 'PASS'
    assert models['contexts'][-1]['sender_party']['kind'] == 'tenant'
    assert detail['decision']['outcome'] == 'ACT'
    # The caller's number is never stored.
    assert '900101' not in str(detail['timeline'])


def test_contractor_quote_then_landlord_is_asked_and_agency_approval_needs_an_approver(service, models):
    cid = quoted_case(service, models)
    detail = service.detail(cid)
    total = next(x for x in detail['claims'] if x['key'] == 'total')
    assert total['party'] == 'contractor' and not total.get('hearsay')
    landlord_q = next(q for q in detail['questions'] if q['key'] == 'authority')
    assert landlord_q['addressee'] == 'landlord' and landlord_q['topic'] == 'approval'
    sent = [m for m in detail['tenant_messages'] if m['recipient']['kind'] == 'landlord']
    assert sent and sent[0]['status'] == 'sent' and sent[0]['recipient']['name'] == 'Morgan Lee'
    assert models['party_drafts'][0]['case']['quoted_total'] == 450.0
    # Tenant questions go to the tenant in their own message.
    tenant_msgs = [m for m in detail['tenant_messages'] if m['recipient']['kind'] == 'tenant']
    assert tenant_msgs and all(t in {'access', 'availability', 'photo'} for m in tenant_msgs for t in m['topics'])

    def agency_reply(context):
        ids = [q['id'] for q in context['open_questions'] if q['topic'] == 'approval']
        assert ids, 'the agency may answer the landlord question'
        return reading(route='instruct_work', quote='happy to go ahead', intent='answer_to_question',
                       claims=[{'key': 'authority', 'value': True, 'amount': None, 'source_quote': 'happy to go ahead', 'issue_index': 0}],
                       answers=[{'question_id': ids[0], 'status': 'answered', 'source_quote': 'happy to go ahead'}])
    models['next'] = agency_reply
    call(service, AGENCY, 'Calling about Flat 7 Park View: the landlord is happy to go ahead with the boiler quote.', 'call-3')
    service.claude_steps(cid)
    detail = service.detail(cid)
    authority = next(x for x in detail['claims'] if x['key'] == 'authority')
    assert authority['party'] == 'agency' and not authority.get('hearsay') and not authority['verified']
    b = blocker(detail, 'authority')
    assert b['response'] == 'HUMAN REVIEW' and b['owner'] == 'approver'
    review = next(r for r in detail['reviews'] if r['key'] == 'authority' and r['status'] == 'open')
    detail = service.respond(review['id'], ReviewResponse(decision='correct', reason='Checked the agency call against the instruction.', claim_id=authority['id'], source_id=authority['source_id']), APPROVER)
    assert check(detail, 'authority')['status'] == 'PASS'


def test_party_answers_only_their_own_questions_and_hearsay_never_counts(service, models):
    cid = quoted_case(service, models)
    models['next'] = lambda context: (
        reading(route='instruct_work', quote='the landlord told me it is fine', intent='update',
                claims=[{'key': 'authority', 'value': True, 'amount': None, 'source_quote': 'the landlord told me it is fine', 'issue_index': 0}]))
    call(service, TENANT, 'Also, the landlord told me it is fine to do the work.', 'call-4')
    service.claude_steps(cid)
    context = models['contexts'][-1]
    assert context['sender_party']['kind'] == 'tenant'
    assert 'approval' not in {q['topic'] for q in context['open_questions']}
    detail = service.detail(cid)
    hearsay = next(x for x in detail['claims'] if x['key'] == 'authority')
    assert hearsay['hearsay'] is True and hearsay['party'] == 'tenant'
    b = blocker(detail, 'authority')
    assert b['status'] == 'UNKNOWN' and hearsay['id'] not in b['claim_ids']


def test_authority_is_never_read_from_an_unmatched_source(service, models):
    cid = quoted_case(service, models)
    models['next'] = reading(route='instruct_work', quote='landlord approves', intent='update',
                             claims=[{'key': 'authority', 'value': True, 'amount': None, 'source_quote': 'landlord approves', 'issue_index': 0}])
    service.evidence(cid, EvidenceInput(text='Note: landlord approves.', source_label='Staff note'), {'id': 'test', 'role': 'case_manager'})
    service.claude_steps(cid)
    assert not any(x['key'] == 'authority' for x in service.detail(cid)['claims'])


def test_status_answers_are_filtered_for_the_caller(service, models):
    cid = quoted_case(service, models)
    before = len(service.detail(cid)['evidence'])
    tenant = call(service, TENANT, 'When is someone coming?', 'status-1', intent='status_enquiry')
    landlord = call(service, LANDLORD, 'Any news on Flat 7 Park View?', 'status-2', intent='status_enquiry')
    contractor = call(service, CONTRACTOR, 'Is the Park View job confirmed?', 'status-3', intent='status_enquiry')
    stranger = call(service, '+447700900999', 'What is happening at Flat 7?', 'status-4', intent='status_enquiry')
    assert tenant['outcome'] == landlord['outcome'] == 'status' and tenant['case_id'] == cid
    assert '£450' in landlord['say'] and '£450' not in tenant['say'] and '£450' not in contractor['say']
    assert 'approval' in landlord['say'] and 'No appointment is confirmed yet.' in contractor['say']
    assert 'Alex' not in contractor['say'] and 'Morgan' not in tenant['say']
    assert stranger['case_id'] is None and stranger['party']['kind'] == 'other' and "can't share details" in stranger['say']
    assert len(service.detail(cid)['evidence']) == before


def test_multi_property_caller_is_asked_which_property(service, models):
    reply = call(service, LANDLORD, 'The garden fence has blown down.', 'call-5')
    assert reply['outcome'] == 'needs_property' and reply['case_id'] is None and 'Which property' in reply['say']
    assert service.list_cases() == []
    reply = call(service, LANDLORD, 'It is at 2 Sample Lane: the garden fence has blown down.', 'call-6')
    assert reply['outcome'] == 'new_case' and reply['property']['ref'] == 'DEMO-LANE-2'


def test_unknown_caller_goes_to_a_person(service, models):
    reply = call(service, '+447700900999', 'There is a leak at number 4.', 'call-7')
    assert reply['outcome'] == 'new_case' and reply['party']['kind'] == 'other' and reply['property'] is None
    service.claude_steps(reply['case_id'])
    detail = service.detail(reply['case_id'])
    assert blocker(detail, 'identity')['response'] == 'HUMAN REVIEW'
    assert not any(m for m in detail['tenant_messages'])


def test_retried_call_is_idempotent_and_a_reused_id_is_rejected(service, models):
    first = call(service, TENANT, 'Hi, the boiler is not heating the flat.', 'call-1')
    again = call(service, TENANT, 'Hi, the boiler is not heating the flat.', 'call-1')
    assert again['case_id'] == first['case_id'] and len(service.list_cases()) == 1
    assert len([e for e in service.detail(first['case_id'])['evidence'] if e.get('party')]) == 1
    with pytest.raises(Conflict):
        call(service, TENANT, 'Something else entirely.', 'call-1')


def test_inbound_api_requires_bridge_token_or_staff_session(tmp_path, monkeypatch, models):
    from app import main
    monkeypatch.setattr(service_module, '_service', Service(Store('sqlite:///' + str(tmp_path / 'api.db'))))
    monkeypatch.setattr(main, 'WORKFLOW_MODE', 'manual_demo')
    monkeypatch.setenv('VOICE_BRIDGE_TOKEN', 'fictional-test-bridge-secret')
    client = TestClient(main.app)
    body = {'call_id': 'api-1', 'caller_number': TENANT, 'transcript': 'Hi, the boiler is not heating the flat.'}
    assert client.post('/api/inbound', json=body).status_code == 403
    assert client.post('/api/inbound', json=body, headers={'Authorization': 'Bearer wrong'}).status_code == 403
    response = client.post('/api/inbound', json=body, headers={'Authorization': 'Bearer fictional-test-bridge-secret'})
    assert response.status_code == 200 and response.json()['party']['kind'] == 'tenant'
    # The background wake ran Claude's (fake) reading after the reply.
    assert models['contexts']
    client.post('/api/demo-session', json={'role': 'case_manager'})
    directory = client.get('/api/inbound/directory').json()
    assert {p['kind'] for p in directory['parties']} == {'tenant', 'landlord', 'agency', 'contractor'}
    assert client.post('/api/inbound', json={**body, 'call_id': 'api-2'}).status_code == 200
    assert client.post('/api/inbound', json={**body, 'call_id': 'api-3', 'extra': 1}).status_code == 422


@pytest.mark.claude
def test_live_claude_reads_a_landlord_approval_and_drafts_a_landlord_question(tmp_path):
    """Live: the full voice flow with real Claude readings. Skipped without a credential."""
    service = Service(Store('sqlite:///' + str(tmp_path / 'live-inbound.db')))
    cid = call(service, TENANT, 'Hi, this is Alex. The boiler at my flat is not heating the radiators at all.', 'live-1')['case_id']
    service.claude_steps(cid)
    service.tick(cid)
    call(service, CONTRACTOR, 'Hi, it is the contractor. For the boiler at Flat 7 Park View, the repair quote is £450 including VAT. Ready to do it once approved.', 'live-2')
    service.claude_steps(cid)
    detail = service.detail(cid)
    assert any(x['key'] == 'total' and x['value'] == 450 and x['party'] == 'contractor' for x in detail['claims'])
    landlord = [m for m in detail['tenant_messages'] if (m.get('recipient') or {}).get('kind') == 'landlord']
    if any(q['key'] == 'authority' and q['addressee'] == 'landlord' for q in detail['questions']):
        assert landlord and landlord[0]['text'] and 'Alex' not in landlord[0]['text']
    call(service, AGENCY, 'Harbour Lettings here about Flat 7 Park View. The landlord approves the £450 boiler repair, please go ahead.', 'live-3')
    service.claude_steps(cid)
    detail = service.detail(cid)
    approvals = [x for x in detail['claims'] if x['key'] == 'authority']
    assert approvals and all(x['party'] == 'agency' and not x['verified'] and not x.get('hearsay') for x in approvals)
