"""Phone intake webhooks with fictional callers; no ElevenLabs, Twilio or model call is made."""
import hashlib
import hmac
import json
import time

import pytest
from fastapi.testclient import TestClient

from app import main, service
from app.service import Service
from app.store import Store
from app.voice import CORRECTION_LABEL, TRANSCRIPT_LABEL

TOOL_SECRET = 'test-tool-secret'
WEBHOOK_SECRET = 'test-webhook-secret'
REPORT = {'conversation_id': 'conv_test_1', 'caller_confirmed': True, 'name': 'Alex Taylor',
          'address': 'Flat 2, 18 Example Road, ZZ1 1ZZ',
          'problems': 'The bath drains very slowly after showers.',
          'danger': 'none', 'already_tried': 'Used a plunger, no change',
          'availability': 'Weekday mornings', 'access_notes': ''}


@pytest.fixture
def client(tmp_path, monkeypatch, no_claude):
    monkeypatch.setattr(service, '_service', Service(Store('sqlite:///' + str(tmp_path / 'voice.db'))))
    monkeypatch.setattr(main, 'WORKFLOW_MODE', 'manual_demo')
    monkeypatch.setenv('VOICE_TOOL_SECRET', TOOL_SECRET)
    monkeypatch.setenv('ELEVENLABS_WEBHOOK_SECRET', WEBHOOK_SECRET)
    with TestClient(main.app) as c:
        yield c


def submit(client, body=None, secret=TOOL_SECRET):
    return client.post('/api/voice/report', json=body or REPORT, headers={'X-Voice-Tool-Secret': secret})


def signed(payload, secret=WEBHOOK_SECRET, at=None):
    body = json.dumps(payload).encode()
    t = str(int(at if at is not None else time.time()))
    sig = hmac.new(secret.encode(), t.encode() + b'.' + body, hashlib.sha256).hexdigest()
    return body, {'ElevenLabs-Signature': f't={t},v0={sig}', 'Content-Type': 'application/json'}


def post_call(conversation_id='conv_test_1'):
    return {'type': 'post_call_transcription', 'event_timestamp': int(time.time()),
            'data': {'agent_id': 'agent_x', 'conversation_id': conversation_id, 'status': 'done',
                     'transcript': [{'role': 'agent', 'message': 'Property maintenance line, how can I help?'},
                                    {'role': 'user', 'message': 'My bath drains really slowly.'},
                                    {'role': 'agent', 'message': None}],
                     'metadata': {'call_duration_secs': 95, 'phone_call': {'external_number': '+447700900123'}},
                     'analysis': {'transcript_summary': 'Caller reported a slow bath drain.'}}}


def staff(client):
    assert client.post('/api/demo-session', json={'role': 'case_manager'}).status_code == 200


def test_confirmed_call_creates_one_unverified_case_with_reference(client):
    first = submit(client)
    assert first.status_code == 200, first.text
    reference = first.json()['reference']
    assert len(reference) == 6 and first.json()['reference_spoken'] == ' '.join(reference)
    # A retried tool call converges on the same case.
    assert submit(client).json()['reference'] == reference
    staff(client)
    cases = client.get('/api/cases').json()
    assert len(cases) == 1 and cases[0]['id'].upper().startswith(reference)
    assert cases[0]['property_ref'] == 'Unverified address: Flat 2, 18 Example Road, ZZ1 1ZZ'
    detail = client.get(f"/api/cases/{cases[0]['id']}").json()
    source = detail['evidence'][0]
    assert source['source_label'] == 'Intake report' and source['text'].startswith('Phone call to the maintenance line')
    assert source['actor']['id'] == 'phone-voice-bridge'
    assert 'Already tried: Used a plunger, no change' in source['text']
    assert 'Possible danger' not in source['text'] and 'Access notes' not in source['text']
    # The caller's statements never verify identity or the contact route.
    assert not any(c['verified'] for c in detail['claims'] if c['key'] in {'identity', 'route'})


def test_tool_requires_secret_and_explicit_confirmation(client):
    assert submit(client, secret='wrong').status_code == 401
    # The body schema is not disclosed to an unauthenticated caller.
    assert client.post('/api/voice/report', json={}).status_code == 401
    assert submit(client, {**REPORT, 'caller_confirmed': False}).status_code == 422
    assert submit(client, {**REPORT, 'name': '  '}).status_code == 422
    staff(client)
    assert client.get('/api/cases').json() == []


def test_corrected_read_back_is_added_to_the_same_case(client):
    reference = submit(client).json()['reference']
    corrected = {**REPORT, 'address': 'Flat 3, 18 Example Road, ZZ1 1ZZ'}
    assert submit(client, corrected).json()['reference'] == reference
    assert submit(client, corrected).json()['reference'] == reference
    staff(client)
    (case,) = client.get('/api/cases').json()
    labels = [e['source_label'] for e in client.get(f"/api/cases/{case['id']}").json()['evidence']]
    assert labels == ['Intake report', CORRECTION_LABEL]


def test_post_call_transcript_is_attached_once_without_retriage(client):
    submit(client)
    body, headers = signed(post_call())
    assert client.post('/api/voice/post-call', content=body, headers=headers).json()['status'] == 'transcript_attached'
    assert client.post('/api/voice/post-call', content=body, headers=headers).status_code == 200
    staff(client)
    (case,) = client.get('/api/cases').json()
    evidence = client.get(f"/api/cases/{case['id']}").json()['evidence']
    transcripts = [e for e in evidence if e['source_label'] == TRANSCRIPT_LABEL]
    assert len(transcripts) == 1 and transcripts[0]['triage'] == 'not_required'
    assert 'Caller: My bath drains really slowly.' in transcripts[0]['text']
    assert 'Caller number (unverified): +447700900123' in transcripts[0]['text']
    (call,) = client.get('/api/voice/calls').json()
    assert call['status'] == 'transcript_attached' and call['case_id'] == case['id']


def test_unconfirmed_call_is_kept_for_staff_but_creates_no_case(client):
    body, headers = signed(post_call('conv_dropped'))
    assert client.post('/api/voice/post-call', content=body, headers=headers).json() == {'status': 'unconfirmed', 'case_id': None}
    staff(client)
    assert client.get('/api/cases').json() == []
    (call,) = client.get('/api/voice/calls').json()
    assert call['status'] == 'unconfirmed' and 'slowly' in call['transcript']


@pytest.mark.parametrize('mutate', ['bad_secret', 'stale', 'tampered', 'missing'])
def test_post_call_rejects_unsigned_or_altered_webhooks(client, mutate):
    body, headers = signed(post_call('conv_forged'), secret='other' if mutate == 'bad_secret' else WEBHOOK_SECRET,
                           at=time.time() - 3600 if mutate == 'stale' else None)
    if mutate == 'tampered':
        body = body.replace(b'slowly', b'quickly')
    if mutate == 'missing':
        headers.pop('ElevenLabs-Signature')
    assert client.post('/api/voice/post-call', content=body, headers=headers).status_code == 401
    staff(client)
    assert client.get('/api/voice/calls').json() == []


def test_tunnelled_requests_only_reach_phone_webhooks(client):
    tunnel = {'X-Forwarded-For': '203.0.113.9', 'X-Forwarded-Host': 'example.ngrok.app'}
    assert client.post('/api/demo-session', json={'role': 'case_manager'}, headers=tunnel).status_code == 403
    assert client.get('/api/voice/calls', headers=tunnel).status_code == 403
    assert client.get('/', headers=tunnel).status_code == 403
    assert client.post('/api/voice/report', json=REPORT,
                       headers={**tunnel, 'X-Voice-Tool-Secret': TOOL_SECRET}).status_code == 200


def test_unconfigured_server_refuses_phone_intake(client, monkeypatch):
    monkeypatch.delenv('VOICE_TOOL_SECRET')
    monkeypatch.delenv('ELEVENLABS_WEBHOOK_SECRET')
    assert submit(client).status_code == 503
    body, headers = signed(post_call())
    assert client.post('/api/voice/post-call', content=body, headers=headers).status_code == 503
