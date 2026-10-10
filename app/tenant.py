"""Local tenant conversations: source statements, never identity or permission grants.

Claude reads the conversation, asks for anything missing and prepares a summary.
Nothing reaches property management until the tenant confirms that summary. The
local phrase parser is the offline fallback when Claude is unavailable.

Conversation ownership, pending deliveries and request receipts use Store's durable
primitives. Service.intake/evidence remain the only routes into the shared case.
The separate server bridge actor is not a browser session or a staff credential.
"""
from __future__ import annotations

import asyncio
import hashlib
import re
import secrets
import uuid
from copy import deepcopy
from datetime import timedelta

from fastapi import APIRouter, HTTPException, Request
from fastapi.responses import JSONResponse
from pydantic import Field, field_validator

from . import ai
from .domain import EvidenceInput, Intake, StrictModel, digest, dt, now, stamp
from .service import get_service

COOKIE = 'pw_tenant_session'
AUTHENTICATION = ('Loopback-only tenant demonstration session; identity is unverified. '
                  'Claude reads the conversation and the tenant confirms a summary before it is sent; '
                  'without Claude, a literal demo parser extracts common phrases.')
CLARIFY_OPENING = 'Hey, before I continue, could you clarify a few things for us?'
READY_REPLY = ('Thanks, I think I have everything. Please check the summary below '
               'before I send it to your property manager.')
SENT_REPLY = ('Thanks! I’ve sent your request to your property manager. They’ll check the details '
              'and decide the next step. You can add an update here at any time.')
CONFIRM_TEXT = 'Yes, that’s right. Please send it.'
DANGER_NOTE = 'If anyone is in danger right now, please call 999.'
BRIDGE_ACTOR = {'id': 'tenant-portal-bridge', 'role': 'case_manager',
                'source': 'unverified tenant conversation'}
FIELD_NAMES = ('name', 'address', 'issue')
ISSUE_WORDS = re.compile(
    r'\b(leak\w*|drip\w*|broken|break\w*|repair\w*|not working|stopped working|'
    r'won[’\']t|doesn[’\']t|not heating|no hot water|water|damp|mould|mold|'
    r'blocked|clog\w*|crack\w*|damage\w*|noise|noisy|smell|sparks|flood\w*|'
    r'ceiling|heating|boiler|radiator|tap|toilet|pipe|drain|shower|oven|fridge|'
    r'dishwasher|washing machine|window|door|lock|pest\w*|infestation)\b', re.I)
STREET = (r'(?:\d+[A-Za-z]?(?:[-/]\d+)?\s+[^\n.;:]{1,95}?\b'
          r'(?:Road|Street|Lane|Avenue|Close|Way|Drive|Place|Court|Terrace|'
          r'Gardens|Square|Crescent|Mews|Grove|Hill|Rd|St|Ave)\b)')


class TenantMessage(StrictModel):
    text: str = Field(min_length=1, max_length=10000)
    idempotency_key: str = Field(min_length=1, max_length=160)

    @field_validator('text', 'idempotency_key')
    @classmethod
    def not_blank(cls, value):
        if not value.strip():
            raise ValueError('A message and a request key are required')
        return value  # Keep the original message, including whitespace, as evidence.


def _clean(value):
    return value.strip(' \t\r\n,.;:')


def _name(value):
    value = _clean(value)
    words = value.split()
    excluded = {'a', 'the', 'tenant', 'reporting', 'having', 'living', 'at', 'in',
                'from', 'here', 'hello', 'hi', 'thanks', 'thank', 'there', 'it',
                'is', 'my', 'i', 'we', 'am', 'are', 'and', 'please', 'not'}
    if not 1 <= len(words) <= 5 or len(value) > 100:
        return None
    if any(w.lower() in excluded for w in words) or ISSUE_WORDS.search(value):
        return None
    if not all(re.fullmatch(r"[^\W\d_]+(?:[-’'][^\W\d_]+)*", w) for w in words):
        return None
    return value


def extract_fields(text: str, previous: dict | None = None) -> dict:
    """Conservative common-phrase extraction; originals remain in messages/evidence.

    Explicit Name:/Address:/Issue: phrases are the editable fallback. This function
    reports what the writer supplied and does not assert that any field is true.
    """
    fields = dict(previous or {key: None for key in FIELD_NAMES})
    spans = []
    explicit = {}
    labels = list(re.finditer(r'\b(name|address|issue|report)\s*:', text, re.I))
    for index, label in enumerate(labels):
        end = labels[index + 1].start() if index + 1 < len(labels) else len(text)
        value = text[label.end():end]
        # A label occupies its line or sentence; subsequent prose is still a report.
        key = 'issue' if label.group(1).lower() == 'report' else label.group(1).lower()
        if key != 'issue':
            value = re.split(r'[\n;]|\.(?:\s|$)', value, maxsplit=1)[0]
        value_end = label.end() + len(value)
        value = _clean(value)
        if key == 'name':
            value = _name(value)
        if value and (key != 'address' or 2 <= len(value) <= 175) and (key != 'issue' or len(value) >= 3):
            explicit[key] = value
            spans.append((label.start(), value_end))

    name_match = re.search(
        r'\b(?:my name is|name is|this is|I am|I[’\']m)\s+(.+?)'
        r'(?=\s+(?:and|at|from|living|I live)\b|[,.;\n]|$)', text, re.I)
    if name_match and 'name' not in explicit:
        value = _name(name_match.group(1))
        if value:
            explicit['name'] = value
            spans.append(name_match.span())

    address_match = re.search(
        r'\b(?:my address is|the address is|address is|I live at|I live in|'
        r'I[’\']m living at|I am living at)\s+(.+?)'
        r'(?=[.;\n]|\s+and\s+(?:my|the|our|I|there)\b|$)', text, re.I)
    if address_match and 'address' not in explicit:
        value = _clean(address_match.group(1))
        if 2 <= len(value) <= 175:
            explicit['address'] = value
            spans.append(address_match.span())
    if 'address' not in explicit:
        address_match = re.search(
            r'(?:(?:Flat|Apartment|Apt|Unit)\s+[\w-]+,?\s+)?' + STREET +
            r'(?:,\s*(?!(?:my|the|our|and|there|I)\b)[^\n.;:]{1,55})?', text, re.I)
        if address_match:
            value = re.split(r'\s+and\s+(?:my|the|our|I|there)\b',
                             address_match.group(), maxsplit=1, flags=re.I)[0]
            value = _clean(value)
            if 2 <= len(value) <= 175:
                explicit['address'] = value
                spans.append((address_match.start(), address_match.start() + len(value)))
    if not fields.get('name') and 'name' not in explicit and 'address' in explicit:
        combined = re.match(r'^\s*([^,.;\n]+),\s*(.+)$', text)
        if combined and combined.group(2).startswith(explicit['address']):
            value = _name(combined.group(1))
            if value:
                explicit['name'] = value
                spans.append((combined.start(1), combined.end(1)))

    remainder = text
    for start, end in sorted(spans, reverse=True):
        remainder = remainder[:start] + ' ' + remainder[end:]
    remainder = re.sub(r'^(?:\s*[,.;!]?\s*(?:hello|hi|and|at)\b[,!]?)+', '', remainder, flags=re.I)
    remainder = _clean(remainder)
    if 'issue' not in explicit and ISSUE_WORDS.search(remainder):
        explicit['issue'] = remainder

    missing_before = [key for key in FIELD_NAMES if not fields.get(key)]
    if missing_before == ['address'] and not explicit:
        candidate = _clean(text)
        address_shape = re.fullmatch(
            r'(?:(?:Flat|Apartment|Apt|Unit)\s+[\w-]+[, ]+)?'
            r'[\w’\' -]{2,100}\b(?:House|Building|Court|Lodge|Tower|Towers|Mansions)'
            r'(?:,\s*[\w -]{2,55})?', candidate, re.I)
        if address_shape and not ISSUE_WORDS.search(candidate) and len(candidate) <= 175:
            explicit['address'] = candidate
    if missing_before == ['name'] and not explicit:
        value = _name(text)
        if value:
            explicit['name'] = value
    if missing_before == ['issue'] and not explicit and len(remainder) >= 3:
        if remainder.lower() not in {'hello', 'hi', 'thanks', 'thank you', 'ok', 'okay'}:
            explicit['issue'] = remainder
    fields.update(explicit)
    return fields


def _missing(fields):
    return [key for key in FIELD_NAMES if not fields.get(key)]


def _question(missing):
    labels = {'name': 'What’s your name?', 'address': 'What’s the address of the property?',
              'issue': 'What needs attention, and where is it?'}
    return _clarify([labels[key] for key in missing])


def _clarify(questions):
    return CLARIFY_OPENING + '\n' + '\n'.join('- ' + q for q in questions)


def _read_request(messages, parser_fields, summary_shown):
    """Claude reads the whole conversation; the literal parser is the offline fallback."""
    if ai.configured():
        transcript = '\n\n'.join(m['text'] for m in messages if m['role'] == 'user')
        try:
            result, meta = ai.tenant_intake(messages, summary_shown)
            return {**ai.checked_intake(result, transcript), 'mode': 'claude', 'model': meta.get('model')}
        except ai.ClaudeUnavailable:
            pass
    missing = _missing(parser_fields)
    issue = parser_fields.get('issue')
    return {'name': parser_fields.get('name'), 'address': parser_fields.get('address'),
            'problems': [{'summary': issue[:120], 'source_quote': issue}] if issue else [],
            'questions': [], 'reply': READY_REPLY if not missing else _question(missing),
            'ready': not missing, 'confirms_summary': False, 'danger': False, 'mode': 'basic'}


def _submit_case(service, owner, cid, conversation):
    """Send the tenant-confirmed request to property management as one shared case."""
    summary = conversation['summary']
    transcript = '\n\n'.join(m['text'] for m in conversation['messages'] if m['role'] == 'user')
    # The tenant's own words come first; the confirmed summary is labelled as such.
    report = (transcript + '\n\nSummary checked and confirmed by the tenant:\n'
              + 'Name: ' + summary['name'] + '\nAddress: ' + summary['address'] + '\nProblems:\n'
              + '\n'.join('- ' + p for p in summary['problems']))
    actor = {**BRIDGE_ACTOR, 'tenant_conversation_id': cid, 'tenant_owner_id': owner}
    # A tenant cannot activate Service's reserved fictional directory alias.
    result = service.intake(Intake(
        title=summary['problems'][0][:140],
        property_ref='Unverified address: ' + summary['address'],
        report=report[:30000],  # Claude chooses the route on the staff side
        work_item='Tenant-reported maintenance',
        idempotency_key='tenant-conversation:' + cid), actor,
        # The name and address the tenant confirmed; policy decides what they unlock.
        self_identification={'name': summary['name'], 'address': summary['address'], 'conversation_id': cid})
    return result['case']['id']


def _message(role, text):
    return {'id': uuid.uuid4().hex, 'role': role, 'text': text, 'created_at': stamp()}


def _conversation_key(cid):
    return 'tenant_conversation:' + cid


def _owned(db, c, cid, owner):
    conversation = db.get_meta(c, _conversation_key(cid))
    if not conversation or conversation['owner_id'] != owner:
        raise HTTPException(404, 'Conversation not found')
    return conversation


def _projection(service, c, conversation):
    """Allowlist projection. Never return staff evidence, policy, reviews or actors."""
    missing = _missing(conversation['fields'])
    status, stage = 'collecting_details', 'awaiting_details'
    next_step = 'Answer the questions above so I can pass this on.'
    updated_at = conversation['updated_at']
    awaiting = bool(conversation.get('awaiting_confirmation') and not conversation['case_id'])
    if awaiting:
        status, stage = 'awaiting_confirmation', 'awaiting_confirmation'
        next_step = 'Check the summary and confirm it, or tell me what to change.'
    if conversation['case_id']:
        case = service.db.case(c, conversation['case_id'])
        status, stage = 'submitted', 'under_review'
        next_step = 'Your property manager will check the details.'
        if case.get('status') == 'in_progress':
            status, stage = 'in_progress', 'under_review'
            next_step = 'Your report is being handled. You can add an update here.'
        elif case.get('status') == 'verified_resolution':
            status, stage = 'resolved', 'resolved'
            next_step = 'This item is marked resolved. You can add an update here.'
        elif case.get('status') == 'administratively_archived':
            status, stage = 'archived', 'archived'
            next_step = 'This item is archived. You can add an update here.'
        if case.get('completion_state') == 'reported; awaiting verification':
            stage = 'reported_complete'
            next_step = 'Completion has been reported and is awaiting review.'
        if conversation.get('correction_pending'):
            next_step = 'Your property manager will check your corrected details.'
    return {'id': conversation['id'], 'case_id': conversation['case_id'],
            'title': conversation['title'], 'status': status, 'stage': stage,
            'fields': deepcopy(conversation['fields']), 'missing_fields': missing,
            'summary': deepcopy(conversation.get('summary')), 'awaiting_confirmation': awaiting,
            'messages': deepcopy(conversation['messages']), 'next_step': next_step,
            'updated_at': updated_at}


def _reserve(service, owner, cid, data):
    """Reserve one durable message before calling a separately transactional service."""
    db = service.db
    with db.tx() as c:
        conversation = _owned(db, c, cid, owner)
        key = 'tenant_message:' + cid + ':' + digest(data.idempotency_key)
        existing = db.get_meta(c, key)
        if existing:
            if existing['input_hash'] != digest(data.text):
                raise HTTPException(409, 'This request key already belongs to a different message')
            return conversation, existing, False
        if conversation.get('pending'):
            return conversation, db.get_meta(c, conversation['pending']), True
        fields = extract_fields(data.text, conversation['fields'])
        message = _message('user', data.text)
        messages = conversation['messages'] + [message]
        transcript = '\n\n'.join(m['text'] for m in messages if m['role'] == 'user')
        if not conversation['case_id'] and len(transcript) > 29000:
            raise HTTPException(422, 'The report is too long; please shorten this message')
        operation = {'key': key, 'input_hash': digest(data.text), 'completed': False,
                     'message': message, 'case_id': conversation['case_id'],
                     'fields': fields, 'transcript': transcript,
                     'corrected': bool(conversation['case_id'] and any(
                         fields[k] != conversation['fields'][k] for k in ('name', 'address')))}
        conversation.update(fields=fields, messages=messages, pending=key,
                            updated_at=message['created_at'])
        if fields['issue']:
            conversation['title'] = fields['issue'][:140]
        db.set_meta(c, key, operation)
        db.set_meta(c, _conversation_key(cid), conversation)
        return conversation, operation, False


def _deliver(service, owner, cid, operation):
    if operation['completed']:
        return
    case_id = operation['case_id']
    actor = {**BRIDGE_ACTOR, 'tenant_conversation_id': cid, 'tenant_owner_id': owner}
    update = {}
    if case_id:
        service.evidence(case_id, EvidenceInput(
            text=operation['message']['text'],
            source_label='Tenant conversation: unverified statement',
            idempotency_key='tenant:' + operation['message']['id']), actor)
        if operation['corrected']:
            service.identity_corrected(case_id, operation['fields'], actor)
        reply = ('Thanks, I’ve passed on your corrected details for your property manager to check.'
                 if operation['corrected'] else
                 'Thanks, I’ve added your update to the report for your property manager.')
    else:
        with service.db.tx() as c:
            conversation = _owned(service.db, c, cid, owner)
        awaiting = conversation.get('awaiting_confirmation')
        # The model call happens outside any database transaction.
        reading = _read_request(conversation['messages'], operation['fields'],
                                conversation.get('summary') if awaiting else None)
        if awaiting and reading['confirms_summary']:
            case_id = _submit_case(service, owner, cid, conversation)
            reply = SENT_REPLY
            update = {'awaiting_confirmation': False, 'confirmed_at': stamp()}
        else:
            previous = conversation['fields']
            problems = [p['summary'].strip()[:120] for p in reading['problems']]
            fields = {'name': reading['name'] or previous.get('name'),
                      'address': reading['address'] or previous.get('address'),
                      'issue': '; '.join(problems) or previous.get('issue')}
            # Claude proposes readiness; the summary needs every field and a problem.
            ready = bool(reading['ready'] and fields['name'] and fields['address'] and problems)
            if ready:
                reply = reading['reply'].strip() or READY_REPLY
            elif reading['mode'] == 'claude' and not reading.get('overruled') and reading['reply'].strip():
                reply = reading['reply'].strip()
            elif reading['questions'] and not reading.get('overruled'):
                reply = _clarify(reading['questions'])
            else:
                # The gate overruled Claude's readiness: ask for what is actually missing.
                reply = _question(_missing(fields) or ['issue'])
            if reading['danger']:
                reply = DANGER_NOTE + '\n\n' + reply
            update = {'fields': fields, 'awaiting_confirmation': ready, 'intake_mode': reading['mode'],
                      'summary': {'name': fields['name'], 'address': fields['address'],
                                  'problems': problems} if ready else None}
            if problems:
                update['title'] = problems[0][:140]

    # A repeated delivery can safely converge after an interrupted service commit.
    with service.db.tx() as c:
        conversation = _owned(service.db, c, cid, owner)
        current = service.db.get_meta(c, operation['key'])
        if current['completed']:
            return
        if conversation.get('pending') != operation['key']:
            raise HTTPException(409, 'The conversation changed; retry this same request')
        assistant = _message('assistant', reply)
        conversation['messages'].append(assistant)
        conversation.update(update)
        conversation.update(case_id=case_id, pending=None, updated_at=assistant['created_at'])
        if operation['corrected']:
            conversation['correction_pending'] = True
        current['completed'] = True
        current['case_id'] = case_id
        service.db.set_meta(c, operation['key'], current)
        service.db.set_meta(c, _conversation_key(cid), conversation)


def _submit(service, owner, cid, data):
    while True:
        conversation, operation, older_pending = _reserve(service, owner, cid, data)
        _deliver(service, owner, cid, operation)
        if not older_pending:
            break
    with service.db.tx() as c:
        return _projection(service, c, _owned(service.db, c, cid, owner))


def _confirm(service, owner, cid):
    """The tenant checked the summary; only now does the request reach property management."""
    with service.db.tx() as c:
        conversation = _owned(service.db, c, cid, owner)
        if conversation['case_id']:
            return _projection(service, c, conversation)
        if conversation.get('pending'):
            raise HTTPException(409, 'Still working on your last message; please try again in a moment')
        if not conversation.get('awaiting_confirmation') or not conversation.get('summary'):
            raise HTTPException(409, 'There is nothing to confirm yet')
    case_id = _submit_case(service, owner, cid, conversation)
    with service.db.tx() as c:
        conversation = _owned(service.db, c, cid, owner)
        if not conversation['case_id']:
            conversation['messages'] += [_message('user', CONFIRM_TEXT), _message('assistant', SENT_REPLY)]
            conversation.update(case_id=case_id, awaiting_confirmation=False, confirmed_at=stamp(),
                                updated_at=conversation['messages'][-1]['created_at'])
            service.db.set_meta(c, _conversation_key(cid), conversation)
        return _projection(service, c, conversation)


def _start(service, owner, data):
    db = service.db
    with db.tx() as c:
        key = 'tenant_start:' + digest({'owner': owner, 'key': data.idempotency_key})
        receipt = db.get_meta(c, key)
        if receipt:
            if receipt['input_hash'] != digest(data.text):
                raise HTTPException(409, 'This request key already belongs to a different report')
            cid = receipt['conversation_id']
            _owned(db, c, cid, owner)
        else:
            cid = uuid.uuid4().hex
            conversation = {'id': cid, 'owner_id': owner, 'case_id': None,
                            'title': 'New maintenance report',
                            'fields': {key: None for key in FIELD_NAMES},
                            'messages': [], 'pending': None, 'updated_at': stamp()}
            db.set_meta(c, _conversation_key(cid), conversation)
            index_key = 'tenant_owner:' + owner
            db.set_meta(c, index_key, (db.get_meta(c, index_key) or []) + [cid])
            db.set_meta(c, key, {'conversation_id': cid, 'input_hash': digest(data.text)})
    return _submit(service, owner, cid, data)


def create_tenant_router(wake, mode='demo') -> APIRouter:
    router = APIRouter(prefix='/api/tenant', tags=['tenant'])

    def guard(request):
        if mode != 'demo':
            raise HTTPException(403, 'Tenant demo identity is disabled; real tenant authentication is not configured')
        host = request.client.host if request.client else ''
        if host not in {'127.0.0.1', '::1', 'localhost', 'testclient'}:
            raise HTTPException(403, 'Tenant demonstration sessions are restricted to this computer')
        origin = request.headers.get('origin')
        if request.method not in {'GET', 'HEAD', 'OPTIONS'} and origin and origin.rstrip('/') != str(request.base_url).rstrip('/'):
            raise HTTPException(403, 'Cross-origin mutations are not permitted')

    def identity(request, required=True):
        guard(request)
        token = request.cookies.get(COOKIE, '')
        session = None
        if token:
            service = get_service()
            with service.db.tx() as c:
                session = service.db.get_meta(c, 'tenant_session:' + hashlib.sha256(token.encode()).hexdigest())
            if session and dt(session['expires_at']) <= now():
                session = None
        if required and not session:
            raise HTTPException(403, 'Start a tenant demonstration session first')
        return session

    def session_projection(session):
        conversations = []
        if session:
            service = get_service()
            with service.db.tx() as c:
                ids = service.db.get_meta(c, 'tenant_owner:' + session['id']) or []
                conversations = [_projection(service, c, _owned(service.db, c, cid, session['id'])) for cid in ids]
            conversations.sort(key=lambda item: item['updated_at'], reverse=True)
        return {'active': bool(session), 'authentication': AUTHENTICATION, 'conversations': conversations}

    @router.get('/session')
    def read_session(request: Request):
        return session_projection(identity(request, required=False))

    @router.post('/session')
    def start_session(request: Request):
        guard(request)
        token = secrets.token_urlsafe(32)
        session = {'id': uuid.uuid4().hex, 'expires_at': stamp(now() + timedelta(hours=8))}
        service = get_service()
        with service.db.tx() as c:
            service.db.set_meta(c, 'tenant_session:' + hashlib.sha256(token.encode()).hexdigest(), session)
        response = JSONResponse(session_projection(session))
        response.set_cookie(COOKIE, token, httponly=True, samesite='strict', secure=False,
                            max_age=28800, path='/api/tenant')
        return response

    @router.post('/conversations')
    async def start_conversation(request: Request, data: TenantMessage):
        session = identity(request)
        result = await asyncio.to_thread(_start, get_service(), session['id'], data)
        if result['case_id']:
            await wake(result['case_id'])
        return result

    @router.get('/conversations/{cid}')
    def read_conversation(cid: str, request: Request):
        session = identity(request)
        service = get_service()
        with service.db.tx() as c:
            return _projection(service, c, _owned(service.db, c, cid, session['id']))

    @router.post('/conversations/{cid}/messages')
    async def send_message(cid: str, request: Request, data: TenantMessage):
        session = identity(request)
        result = await asyncio.to_thread(_submit, get_service(), session['id'], cid, data)
        if result['case_id']:
            await wake(result['case_id'])
        return result

    @router.post('/conversations/{cid}/confirm')
    async def confirm(cid: str, request: Request):
        session = identity(request)
        result = await asyncio.to_thread(_confirm, get_service(), session['id'], cid)
        await wake(result['case_id'])
        return result

    return router
