"""Phone intake: an ElevenLabs voice agent answers a Twilio number and hands over here.

The voice agent asks the caller for their name, address and problems, reads a
summary back and, once the caller says yes, calls ``POST /api/voice/report``.
That confirmation is the phone equivalent of the tenant portal's summary card:
only then does the report reach property management through ``Service.intake``,
and the case coordinator's Claude triage takes over exactly as for the portal.

After the call, ElevenLabs sends a signed ``post_call_transcription`` webhook.
The transcript is attached to the case as preserved, already-read evidence (it
repeats the confirmed report, so it is not triaged again). A call that ended
before confirmation is kept for staff and never becomes a case on its own.

Nothing said on a call is verified: speech is transcribed automatically and the
caller number is an unverified network value, not identity. Both endpoints are
authenticated with server-side secrets; neither is a browser or staff session.
"""
from __future__ import annotations

import asyncio
import hashlib
import hmac
import json
import os
import time

from fastapi import APIRouter, Depends, HTTPException, Request
from pydantic import BaseModel, ConfigDict, Field, field_validator

from .domain import EvidenceInput, Intake, digest, stamp
from .service import Conflict, get_service

PHONE_BRIDGE_ACTOR = {'id': 'phone-voice-bridge', 'role': 'case_manager',
                      'source': 'unverified phone call (ElevenLabs voice agent)'}
# The 'Tenant' prefix keeps these in the tenant-message context Claude drafts from.
CORRECTION_LABEL = 'Tenant phone call: corrected summary (automatic transcription, unverified)'
TRANSCRIPT_LABEL = 'Tenant phone call transcript (automatic transcription, unverified)'
TUNNEL_PATHS = {'/api/voice/report', '/api/voice/post-call'}
SIGNATURE_TOLERANCE_SECS = 30 * 60  # Matches the ElevenLabs SDK's construct_event window.
INDEX_KEY = 'voice_calls'


class PhoneReport(BaseModel):
    """Body of the voice agent's tool call. Every value is the caller's unverified statement."""
    # A third-party payload: ignore additions instead of failing a live call.
    model_config = ConfigDict(extra='ignore')
    conversation_id: str = Field(min_length=1, max_length=200)
    caller_confirmed: bool
    name: str = Field(min_length=1, max_length=100)
    address: str = Field(min_length=2, max_length=200)
    problems: str = Field(min_length=3, max_length=4000)
    danger: str | None = Field(default=None, max_length=1000)
    already_tried: str | None = Field(default=None, max_length=1000)
    availability: str | None = Field(default=None, max_length=1000)
    access_notes: str | None = Field(default=None, max_length=1000)

    @field_validator('name', 'address', 'problems', 'conversation_id')
    @classmethod
    def not_blank(cls, value):
        if not value.strip():
            raise ValueError('must not be blank')
        return value.strip()

    @field_validator('danger', 'already_tried', 'availability', 'access_notes')
    @classmethod
    def optional(cls, value):
        value = (value or '').strip()
        return None if value.lower() in {'', 'none', 'n/a', 'no', 'not mentioned', 'unknown'} else value


def verify_signature(body: bytes, header: str, secret: str, now: float | None = None) -> None:
    """Check ``ElevenLabs-Signature: t=<unix secs>,v0=<hex HMAC-SHA256 of "t.body">``."""
    parts = dict(p.strip().split('=', 1) for p in (header or '').split(',') if '=' in p)
    timestamp, signature = parts.get('t', ''), parts.get('v0', '')
    if not timestamp.isdigit() or not signature:
        raise HTTPException(401, 'Missing or malformed webhook signature')
    if abs((now if now is not None else time.time()) - int(timestamp)) > SIGNATURE_TOLERANCE_SECS:
        raise HTTPException(401, 'Webhook signature has expired')
    expected = hmac.new(secret.encode(), timestamp.encode() + b'.' + body, hashlib.sha256).hexdigest()
    if not hmac.compare_digest(expected, signature):
        raise HTTPException(401, 'Invalid webhook signature')


def spoken_reference(case_id: str) -> str:
    return case_id[:6].upper()


def _report(data: PhoneReport) -> str:
    lines = ['Phone call to the maintenance line, answered by an automated voice agent. '
             'Speech was transcribed automatically and the caller confirmed this summary '
             'when it was read back. Nothing here has been verified.',
             '',
             'Name: ' + data.name,
             'Address: ' + data.address,
             'Problems:',
             data.problems]
    for label, value in (('Possible danger mentioned', data.danger),
                         ('Already tried', data.already_tried),
                         ('Availability', data.availability),
                         ('Access notes', data.access_notes)):
        if value:
            lines.append(label + ': ' + value)
    return '\n'.join(lines)


def _index(db, c, conversation_id):
    ids = db.get_meta(c, INDEX_KEY) or []
    if conversation_id not in ids:
        db.set_meta(c, INDEX_KEY, ids + [conversation_id])


def submit_report(service, data: PhoneReport) -> dict:
    """Create one case per call; a later, different read-back on the same call is a correction."""
    key = 'voice_call:' + data.conversation_id
    report = _report(data)
    with service.db.tx() as c:
        call = service.db.get_meta(c, key)
    if call and call.get('case_id'):
        if call['report_hash'] != digest(report):
            service.evidence(call['case_id'], EvidenceInput(
                text='The caller corrected the summary later in the same call.\n\n' + report,
                source_label=CORRECTION_LABEL,
                idempotency_key='phone-correction:' + digest(report)[:40]), PHONE_BRIDGE_ACTOR)
            with service.db.tx() as c:
                call = service.db.get_meta(c, key)
                call['report_hash'] = digest(report)
                service.db.set_meta(c, key, call)
        return call
    try:
        result = service.intake(Intake(
            title=data.problems.splitlines()[0][:140].strip() or 'Phone report',
            property_ref='Unverified address: ' + data.address,
            report=report,  # Claude chooses the route in the case coordinator
            work_item='Tenant-reported maintenance',
            idempotency_key='phone-call:' + data.conversation_id), PHONE_BRIDGE_ACTOR)
    except Conflict:
        # A concurrent, different submission won the key; it owns this call's case.
        with service.db.tx() as c:
            call = service.db.get_meta(c, key)
        if not call:
            raise
        return call
    case_id = result['case']['id']
    with service.db.tx() as c:
        call = service.db.get_meta(c, key) or {}
        call.update(conversation_id=data.conversation_id, case_id=case_id,
                    reference=spoken_reference(case_id), report_hash=digest(report),
                    status=call.get('status') or 'submitted', submitted_at=stamp())
        service.db.set_meta(c, key, call)
        _index(service.db, c, data.conversation_id)
    return call


def _transcript(data: dict) -> str:
    lines = []
    for turn in data.get('transcript') or []:
        text = (turn.get('message') or '').strip()
        if text:
            lines.append(('Caller' if turn.get('role') == 'user' else 'Voice agent') + ': ' + text)
    return '\n'.join(lines)


def record_call(service, data: dict) -> dict:
    """Attach the transcript to the call's case, or keep an unconfirmed call for staff."""
    conversation_id = str(data.get('conversation_id') or '').strip()
    if not conversation_id:
        raise HTTPException(422, 'Webhook has no conversation_id')
    phone = (data.get('metadata') or {}).get('phone_call') or {}
    analysis = data.get('analysis') or {}
    transcript = _transcript(data)[:50000]
    key = 'voice_call:' + conversation_id
    with service.db.tx() as c:
        call = service.db.get_meta(c, key) or {'conversation_id': conversation_id, 'case_id': None}
        call.update(caller_number=phone.get('external_number'), ended_at=stamp(),
                    duration_secs=(data.get('metadata') or {}).get('call_duration_secs'),
                    summary=analysis.get('transcript_summary'))
        if call.get('case_id'):
            header = 'Caller number (unverified): ' + call['caller_number'] + '\n\n' if call.get('caller_number') else ''
            # Already-read evidence: it repeats the confirmed report and must not trigger a second triage.
            service.db.add(c, 'evidence', {
                'text': header + (transcript or 'No transcript text was supplied.'),
                'source_label': TRANSCRIPT_LABEL, 'actor': PHONE_BRIDGE_ACTOR,
                'occurred_at': stamp(), 'triage': 'not_required'},
                call['case_id'], dedupe='voice-transcript:' + conversation_id)
            call['status'] = 'transcript_attached'
        else:
            call.update(status='unconfirmed', transcript=transcript)
        service.db.set_meta(c, key, call)
        _index(service.db, c, conversation_id)
    return {'status': call['status'], 'case_id': call.get('case_id')}


def list_calls(service) -> list[dict]:
    with service.db.tx() as c:
        calls = [service.db.get_meta(c, 'voice_call:' + cid) for cid in service.db.get_meta(c, INDEX_KEY) or []]
    calls = [{k: v for k, v in call.items() if k != 'report_hash'} for call in calls if call]
    return sorted(calls, key=lambda call: call.get('ended_at') or call.get('submitted_at') or '', reverse=True)


def create_voice_router(wake, actor) -> APIRouter:
    router = APIRouter(prefix='/api/voice', tags=['voice'])

    def secret(name):
        value = os.getenv(name, '')
        if not value:
            raise HTTPException(503, 'Phone intake is not configured on this server')
        return value

    def tool_credential(request: Request):
        # A dependency, so an unauthenticated request is refused before body validation.
        if not hmac.compare_digest(request.headers.get('x-voice-tool-secret', ''), secret('VOICE_TOOL_SECRET')):
            raise HTTPException(401, 'Invalid voice tool credential')

    @router.post('/report', dependencies=[Depends(tool_credential)])
    async def report(data: PhoneReport):
        if not data.caller_confirmed:
            # The voice agent reads this and goes back to the caller.
            raise HTTPException(422, 'Read the summary back to the caller and get a clear yes before submitting.')
        call = await asyncio.to_thread(submit_report, get_service(), data)
        await wake(call['case_id'])
        reference = call['reference']
        return {'status': 'submitted', 'reference': reference,
                'reference_spoken': ' '.join(reference),
                'message': 'Saved for the property management team. Give the caller the reference, '
                           'say a person will review it and be in touch, and do not promise a visit, '
                           'time or cost.'}

    @router.post('/post-call')
    async def post_call(request: Request):
        body = await request.body()
        verify_signature(body, request.headers.get('elevenlabs-signature', ''), secret('ELEVENLABS_WEBHOOK_SECRET'))
        try:
            event = json.loads(body)
        except ValueError:
            raise HTTPException(400, 'Webhook body is not JSON')
        if event.get('type') != 'post_call_transcription':
            return {'status': 'ignored', 'type': event.get('type')}
        return await asyncio.to_thread(record_call, get_service(), event.get('data') or {})

    @router.get('/calls')
    def calls(who=Depends(actor)):
        get_service().role(who, {'case_manager'})
        return list_calls(get_service())

    return router
