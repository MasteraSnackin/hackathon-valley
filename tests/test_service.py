"""Clearly labelled BUILD-derived scenarios; no reserved case material."""
import pytest
from datetime import timedelta
from sqlalchemy import update
from app.domain import *
from app.service import Service,Conflict,Forbidden
from app.store import Store,records
from app.ai import Interpretation,validate_sources
from app.build_data import snapshot,verify_sources,ALLOWED

@pytest.fixture
def service(tmp_path):return Service(Store('sqlite:///'+str(tmp_path/'test.db')))
def actor(role='case_manager'):return {'id':'test-'+role,'role':role}
def make(service,action='instruct_work'):
    return service.intake(Intake(title='BUILD-derived dishwasher repair',property_ref='DEMO-FLAT-1',report='The integrated dishwasher starts then stops.',category='appliance',work_item='Dishwasher repair',action=action),actor())
def source(service,cid,key,value,text=None):
    text=text or f'Source states {key}: {value} for this action.'
    return service.evidence(cid,EvidenceInput(text=text,source_label='BUILD-derived test source',claims=[ClaimInput(key=key,value=value,source_quote=text)]),actor())
def verify(service,cid,key,value=True,role=None):
    detail=source(service,cid,key,value)
    claim=detail['claims'][-1]
    review=next(r for r in reversed(detail['reviews']) if r['key']==key and r['status']=='open')
    who=role or review['owner']
    return service.respond(review['id'],ReviewResponse(decision='correct',reason='Checked the exact source and this action scope.',claim_id=claim['id'],source_id=claim['source_id']),actor(who))
def ready(service,total=80):
    d=make(service);cid=d['case']['id']
    for k,v in [('access',True),('authority',True),('schedule',True),('evidence',True),('total',total)]:d=verify(service,cid,k,v)
    return d

def test_routine_quote_needs_no_manager_review(service):
    d=make(service,'request_quote');assert d['decision']['outcome']=='ACT';assert d['reviews']==[]
    assert service.execute(d['case']['id'],actor())['action']['status']=='succeeded'

def test_all_overlapping_blockers_and_permission_response(service):
    d=make(service);cid=d['case']['id'];assert {'access','authority','schedule','total','evidence'} <= {b['key'] for b in d['decision']['blockers']}
    d=verify(service,cid,'access');assert 'access' not in {b['key'] for b in d['decision']['blockers']};assert d['decision']['outcome']!='ACT'

def test_refused_access_stops_method(service):
    d=make(service);d=source(service,d['case']['id'],'access',False,'Tenant refuses the proposed visit using management keys.')
    assert next(b for b in d['decision']['blockers'] if b['key']=='access')['status']=='FAIL'
    with pytest.raises(Conflict):service.execute(d['case']['id'],actor())

def test_wrong_role_cannot_verify_consent(service):
    d=make(service);d=source(service,d['case']['id'],'access',True)
    r=next(r for r in reversed(d['reviews']) if r['key']=='access' and r['status']=='open');claim=d['claims'][-1]
    with pytest.raises(Forbidden):service.respond(r['id'],ReviewResponse(decision='correct',reason='I checked the source.',claim_id=claim['id'],source_id=claim['source_id']),actor('case_manager'))

def test_partial_completion_only_closes_scoped_item(service):
    d=make(service,'close_item');cid=d['case']['id'];d=verify(service,cid,'completion');assert d['decision']['outcome']!='ACT'
    d=verify(service,cid,'commitments');assert d['decision']['outcome']=='ACT'
    result=service.execute(cid,actor());assert result['detail']['case']['status']=='verified_resolution'
    d=service.proposal(cid,ProposalInput(action='close_item',work_item='Separate kitchen extractor',provider='Demo contractor'),actor())
    assert next(b for b in d['decision']['blockers'] if b['key']=='completion')['status']=='UNKNOWN'

def test_missing_photo_never_becomes_visual_fact(service):
    d=make(service);d=service.evidence(d['case']['id'],EvidenceInput(text='[photo attached, unreadable placeholder]',source_label='Unreadable attachment'),actor())
    assert next(b for b in d['decision']['blockers'] if b['key']=='evidence')['status']=='UNKNOWN'
    assert not any(c['key']=='evidence' for c in d['claims'])

def test_explicit_conflict_correction_preserves_both_sources(service):
    d=make(service);cid=d['case']['id'];d=source(service,cid,'schedule',True,'Tenant confirms Friday 10:00 for this visit.')
    d=source(service,cid,'schedule',False,'Contractor says Friday 10:00 is unavailable.')
    assert next(b for b in d['decision']['blockers'] if b['key']=='schedule')['status']=='CONFLICT'
    claim=next(c for c in d['claims'] if c['key']=='schedule' and c['value'] is True)
    r=next(r for r in reversed(d['reviews']) if r['key']=='schedule' and r['status']=='open')
    d=service.respond(r['id'],ReviewResponse(decision='correct',reason='Both parties explicitly corrected the contractor entry; Friday now agreed.',source_id=claim['source_id'],claim_id=claim['id']),actor())
    assert next(c for c in d['decision']['checks'] if c['key']=='schedule')['status']=='PASS'
    assert len([c for c in d['claims'] if c['key']=='schedule'])==3

def test_policy_publish_requires_current_preview_and_explicit_reassessment(service):
    d=ready(service);cid=d['case']['id'];p=service.policies()['active']
    settings={**p['settings'],'access_immediate_review':True}
    draft=service.draft(PolicyInput(base_version=p['version'],settings=settings),actor('policy_editor'))
    with pytest.raises(Conflict):service.publish(draft['id'],actor('policy_editor'))
    service.preview(draft['id'],actor('policy_editor'));service.publish(draft['id'],actor('policy_editor'))
    with pytest.raises(Conflict):service.execute(cid,actor())
    d=service.evaluate_case(cid,actor());assert not d['case']['policy_pending']

def test_superseded_question_and_reminder_cancelled(service):
    d=make(service);cid=d['case']['id'];q=next(q for q in d['questions'] if q['key']=='access')
    service.proposal(cid,ProposalInput(action='request_quote',work_item='Dishwasher repair'),actor())
    service.tick(cid,dt(q['deadline'])+timedelta(hours=1));d=service.detail(cid)
    assert next(x for x in d['questions'] if x['id']==q['id'])['status']=='closed'
    assert not [e for e in d['timeline'] if e['kind']=='reminder' and e['payload']['question_id']==q['id']]

def test_unanswered_request_is_bounded_and_never_permission(service):
    d=make(service);cid=d['case']['id'];q=next(q for q in d['questions'] if q['key']=='access')
    service.tick(cid,dt(q['reminder_at'])+timedelta(seconds=1));service.tick(cid,dt(q['deadline'])+timedelta(seconds=1));service.tick(cid,dt(q['deadline'])+timedelta(days=7));d=service.detail(cid)
    q=next(x for x in d['questions'] if x['id']==q['id']);assert q['reminders']==1;assert q['escalated']
    assert next(b for b in d['decision']['blockers'] if b['key']=='access')['status']=='UNKNOWN'

def test_duplicate_approval_and_scope_change(service):
    d=ready(service,120);cid=d['case']['id'];review=next(r for r in reversed(d['reviews']) if r['key']=='finance' and r['status']=='open')
    response=ReviewResponse(decision='approve',reason='Authorised the specified full commitment.',source_id=d['evidence'][0]['id'],scope=scope_of(d['case']),expires_at=stamp(now()+timedelta(hours=1)))
    service.respond(review['id'],response,actor('approver'))
    with pytest.raises(Conflict):service.respond(review['id'],response,actor('approver'))
    d=service.proposal(cid,ProposalInput(action='instruct_work',work_item='Different repair',provider='New provider'),actor())
    assert d['decision']['outcome']!='ACT'

def test_duplicate_external_and_uncertain_reconciliation(service):
    d=ready(service);cid=d['case']['id']
    result=service.execute(cid,actor(),'uncertain');assert result['action']['status']=='uncertain'
    with pytest.raises(Conflict):service.execute(cid,actor())
    service.reconcile(cid,actor());result=service.execute(cid,actor());assert result['duplicate']
    assert len([r for r in result['detail']['timeline'] if r['kind']=='simulated_provider_receipt'])==1

def test_incoming_idempotency_and_immutable_audit(service):
    d=make(service);cid=d['case']['id'];input=EvidenceInput(text='No update yet',source_label='Tenant message',idempotency_key='message-123')
    a=service.evidence(cid,input,actor());b=service.evidence(cid,input,actor());assert a['case']['revision']==b['case']['revision']
    with pytest.raises(Exception):
        with service.db.tx() as c:c.execute(update(records).values(payload='{}'))

def test_unsupported_case_has_visible_handover(service):
    d=service.intake(Intake(title='Unrecognised issue',property_ref='DEMO-FLAT-1',report='A novel concern with an unidentified object.',category='other'),actor())
    assert any(b['key']=='supported' for b in d['decision']['blockers']);assert d['decision']['outcome']!='ACT'

def test_build_hashes_and_prefix_no_future():
    assert len(verify_sources())==58
    assert len(ALLOWED)==25
    s=snapshot('008',1);assert 'event-002' not in s['text'];assert s['attachments']==[]
    with pytest.raises(ValueError):snapshot('../not-allowed')

def test_structured_model_output_needs_real_quotes():
    r=Interpretation(category='plumbing',summary='Leak',source_quote='Invented quotation')
    with pytest.raises(ValueError):validate_sources(r,'The tap drips.')

def test_continuing_reply_is_interpreted_but_not_granted(service):
    d=make(service);cid=d['case']['id']
    d=service.evidence(cid,EvidenceInput(text='I give permission for this visit while I am at home.',source_label='Fictional tenant reply'),actor())
    claim=next(c for c in reversed(d['claims']) if c['key']=='access')
    assert claim['source_quote']=='I give permission for this visit while I am at home'
    assert not claim['verified']
    assert any(b['key']=='access' for b in d['decision']['blockers'])
    assert any(e['kind']=='interpretation' and e['payload']['source_id']==claim['source_id'] for e in d['timeline'])

def test_duplicate_key_with_altered_claims_rejected(service):
    d=make(service);cid=d['case']['id'];text='Permission is addressed in this message.'
    original=EvidenceInput(text=text,source_label='Tenant',idempotency_key='reply-2')
    service.evidence(cid,original,actor())
    changed=EvidenceInput(text=text,source_label='Tenant',idempotency_key='reply-2',claims=[ClaimInput(key='access',value=True,source_quote=text)])
    with pytest.raises(Conflict):service.evidence(cid,changed,actor())

def test_intake_deduplication(service):
    data=Intake(title='Duplicate-safe report',property_ref='DEMO-FLAT-1',report='The tap drips.',idempotency_key='external-event-123')
    a=service.intake(data,actor());b=service.intake(data,actor());assert a['case']['id']==b['case']['id']
    with pytest.raises(Conflict):service.intake(data.model_copy(update={'report':'The tap is leaking heavily.'}),actor())

def test_changed_category_requires_new_classification(service):
    d=make(service,'request_quote');cid=d['case']['id']
    d=service.proposal(cid,ProposalInput(action='request_quote',category='windows',work_item=d['case']['proposal']['work_item']),actor())
    assert next(b for b in d['decision']['blockers'] if b['key']=='classification')['status']=='UNKNOWN'

def test_native_cycle_automatically_executes_permitted_action_once(service):
    d=make(service,'request_quote');cid=d['case']['id'];service.tick(cid);service.tick(cid)
    d=service.detail(cid)
    assert d['decision']['outcome']=='NO FURTHER ACTION'
    assert len([e for e in d['timeline'] if e['kind']=='simulated_provider_receipt'])==1

@pytest.mark.parametrize('route',['CLARIFY','WAIT','STOP ACTION'])
def test_custom_condition_fact_has_role_checked_resumption(service,route):
    p=service.policies()['active']
    draft=service.draft(PolicyInput(base_version=p['version'],settings=p['settings'],rules=[Rule(id='completion-check',actions=['request_quote'],conditions=[{'key':'completion','status':'UNKNOWN'}],response=route,owner='case_manager')]),actor('policy_editor'))
    service.preview(draft['id'],actor('policy_editor'));service.publish(draft['id'],actor('policy_editor'))
    d=make(service,'request_quote');cid=d['case']['id'];assert d['decision']['outcome']!='ACT'
    d=verify(service,cid,'completion',True)
    assert d['decision']['outcome']=='ACT'
