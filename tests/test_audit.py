"""Per-case audit trail (.audit/<case>/history.md), with fake model answers (offline)."""
import json
import pytest
from app import ai, audit, jev
from app.domain import Intake
from app.service import Service
from app.store import Store

ACTOR = {'id': 'test-manager', 'role': 'case_manager'}
REPORT = 'The kitchen tap has been dripping constantly since yesterday. I am home weekdays after 3pm.'


@pytest.fixture
def service(tmp_path, monkeypatch):
    monkeypatch.setenv('TYPESAFE_API_KEY', 'fake-for-tests')
    answers = {'route': {'choice': 'request_quote', 'confidence': 0.9, 'probabilities': {'request_quote': 0.9}},
               'category': {'choice': 'plumbing', 'confidence': 0.9},
               'signals': {'hazard': 0.02, 'multiple_issues': 0.05, 'states_facts': 0.9, 'system_instructions': 0.01, 'sensitive': 0.05}}
    reading = {'intent': 'new_request', 'summary': 'Dripping kitchen tap.',
               'issues': [{'category': 'plumbing', 'route': 'request_quote', 'work_item': 'Kitchen tap dripping', 'source_quote': 'dripping constantly', 'relation': 'current_case'}],
               'claims': [{'key': 'access', 'value': True, 'issue_index': 0, 'source_quote': 'I am home weekdays after 3pm'}],
               'ambiguities': [{'description': 'Which tap is dripping is not stated.', 'affects_route': False}],
               'answers': [], 'risk_flags': [], 'confidence': 'high', 'rationale': 'Leak needs a quote.', 'route_objection': ''}
    monkeypatch.setattr(jev, 'ask', lambda text, context, reverse=False: (answers, {'provider': 'typesafe', 'model': 'jev-1.13.0', 'request_id': 'fake',
                                                                                     'router_version': jev.ROUTER_VERSION, 'latency_ms': 12, 'usage': {'input_tokens': 300, 'output_tokens': 9}}))
    monkeypatch.setattr(ai, 'triage', lambda text, context, router=None: (reading, {'provider': 'anthropic', 'model': 'fake-claude', 'prompt_version': 'test',
                                                                                    'request_id': 'fake', 'usage': {'input_tokens': 900, 'output_tokens': 120}}))
    return Service(Store('sqlite:///' + str(tmp_path / 'audit.db')))


def run_case(service):
    cid = service.intake(Intake(title='Fictional report', property_ref='DEMO-FLAT-1', report=REPORT), ACTOR)['case']['id']
    service.triage_messages(cid)
    return cid


def test_trail_names_who_decided_and_which_tool_ran(service):
    cid = run_case(service)
    text = audit.render(service.detail(cid))
    assert text.startswith(f'# Case {cid[:12]} audit trail')
    # Jev's routing, Claude's reading, the extracted claim and the policy gate each appear with their actor and tool.
    assert '· Jev routed the message' in text and 'TypeSafe `system_one` · step `route_case_messages`' in text
    assert 'jev_route → `request_quote` (confidence 0.90)' in text
    assert '· Claude read the message' in text and '1 claim · 1 ambiguity · 1 issue' in text and '`ai.triage`' in text and '900 in / 120 out tokens' in text
    assert 'Claim `access` = true' in text and 'unverified assertion' in text and '> I am home weekdays after 3pm' in text
    assert '**Unknown:** Which tap is dripping is not stated.' in text
    assert 'Policy gates →' in text and 'Policy engine (rules v1' in text
    # Bookkeeping records are left out; entries are numbered in order.
    assert 'Signal outbox' not in text and 'Cycle checkpoint' not in text
    assert '<a id="entry-001"></a>' in text


def test_unchanged_assessments_are_collapsed(service):
    cid = run_case(service)
    for _ in range(3): service.evaluate_case(cid, ACTOR)
    detail = service.detail(cid)
    decisions = [r for r in detail['timeline'] if r['kind'] == 'decision']
    shown = audit.render(detail).count('· Policy gates →')
    assert len(decisions) > shown >= 1


def test_commit_hook_writes_a_folder_per_case(service, tmp_path):
    folder = tmp_path / '.audit'
    service.db.on_commit = audit.exporter(service, folder)
    cid = run_case(service)
    history = (folder / cid / 'history.md').read_text()
    assert 'Claude read the message' in history
    raw = [json.loads(line) for line in (folder / cid / 'records.jsonl').read_text().splitlines()]
    assert {r['kind'] for r in raw} >= {'evidence', 'routing', 'interpretation', 'decision'}
    assert len(raw) == len(service.detail(cid)['timeline'])


def test_export_failure_never_fails_the_request(service, tmp_path):
    blocked = tmp_path / 'file-not-dir'
    blocked.write_text('')
    service.db.on_commit = audit.exporter(service, blocked)
    assert run_case(service)


def test_audit_endpoint_returns_markdown(service, monkeypatch):
    from fastapi.testclient import TestClient
    from app import main, service as service_module
    monkeypatch.setattr(service_module, '_service', service)
    cid = run_case(service)
    client = TestClient(main.app)
    assert client.get(f'/api/cases/{cid}/audit').status_code == 403
    assert client.post('/api/demo-session', json={'role': 'case_manager'}).status_code == 200
    response = client.get(f'/api/cases/{cid}/audit')
    assert response.status_code == 200 and response.headers['content-type'].startswith('text/markdown')
    assert 'Jev routed the message' in response.text
