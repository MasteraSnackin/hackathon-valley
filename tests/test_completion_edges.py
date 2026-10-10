"""Integration regressions for the authorised local prototype."""
from datetime import timedelta
import pytest
from pydantic import ValidationError
from app.domain import Intake,EvidenceInput,ClaimInput,ReviewResponse,ProposalInput,now,stamp
from app.service import Service,Conflict,coordinator_cycle
from app.store import Store
from app.build_data import import_case,snapshot

ACTOR={'id':'fictional-manager','role':'case_manager'}

@pytest.fixture
def service(tmp_path):
    return Service(Store('sqlite:///'+str(tmp_path/'edge.db')))

def intake(service,**extra):
    return service.intake(Intake(title='Fictional dishwasher issue',property_ref='DEMO-FLAT-1',report='The dishwasher stops.',category='appliance',work_item='Dishwasher',action='request_quote',triage='staff',**extra),ACTOR)

def test_intake_retry_reuses_case_and_changed_payload_is_rejected(service):
    first=intake(service,idempotency_key='incoming-001')
    second=intake(service,idempotency_key='incoming-001')
    assert first['case']['id']==second['case']['id']
    assert len(service.list_cases())==1
    with pytest.raises(Conflict):
        service.intake(Intake(title='Different request',property_ref='DEMO-FLAT-1',report='The tap leaks.',idempotency_key='incoming-001'),ACTOR)

def test_same_evidence_id_cannot_change_claim(service):
    cid=intake(service)['case']['id']
    common={'text':'The source confirms permission.','source_label':'Fictional source','idempotency_key':'evidence-001'}
    original=EvidenceInput(**common,claims=[ClaimInput(key='access',value=True,source_quote=common['text'])])
    service.evidence(cid,original,ACTOR)
    assert service.evidence(cid,original,ACTOR)['case']['id']==cid
    changed=EvidenceInput(**common,claims=[ClaimInput(key='access',value=False,source_quote=common['text'])])
    with pytest.raises(Conflict):service.evidence(cid,changed,ACTOR)

@pytest.mark.parametrize('invalid',[float('nan'),float('inf'),float('-inf')])
def test_human_correction_rejects_nonfinite_values(invalid):
    with pytest.raises(ValidationError):ReviewResponse(decision='correct',reason='Source checked.',key='total',value=invalid)

def test_native_cycle_progresses_routine_action_once(service,monkeypatch):
    import app.service as module
    monkeypatch.setattr(module,'_service',service)
    cid=intake(service)['case']['id']
    coordinator_cycle(cid)
    coordinator_cycle(cid)
    detail=service.detail(cid)
    receipts=[row for row in detail['timeline'] if row['kind']=='simulated_provider_receipt']
    assert len(receipts)==1
    assert detail['actions'][0]['status']=='succeeded'
    assert detail['case']['last_verified_action']=='request_quote'

def test_selected_build_prefix_has_provenance_without_future_or_attachments(service):
    detail=import_case(service,'013',ACTOR,2)
    source=detail['evidence'][0]['text']
    assert 'event-002' in source and 'event-003' not in source
    provenance=next(row['payload'] for row in detail['timeline'] if row['kind']=='build_snapshot')
    assert provenance['event_count']==2
    assert provenance['attachments']==[]
    with pytest.raises(ValueError):snapshot('013',True)

def test_missing_credential_hands_triage_to_a_person_and_can_retry(service,no_claude):
    created=service.intake(Intake(title='Fictional report',property_ref='DEMO-FLAT-1',report='The dishwasher stops.'),ACTOR)
    cid=created['case']['id']
    assert created['case']['triage']['state']=='pending' and created['decision']['outcome']=='WAIT'
    assert service.triage_messages(cid)=={'triaged':1,'spawned_case_ids':[]}
    detail=service.detail(cid)
    assert detail['case']['triage']=={**detail['case']['triage'],'state':'failed','error':'missing_credentials'}
    assert detail['case']['proposal']['action']=='clarify' and detail['case']['category']=='other'
    failed=next(r['payload'] for r in detail['timeline'] if r['kind']=='interpretation')
    assert failed['status']=='failed' and 'result' not in failed
    # No keyword fallback, and the failure is not retried on every wake.
    assert service.triage_messages(cid)['triaged']==0
    retried=service.retry_triage(cid,ACTOR)
    assert retried['case']['triage']['state']=='pending'
    assert service.triage_messages(cid)['triaged']==1
    assert service.detail(cid)['case']['triage']['state']=='failed'
    # Manual triage settles it.
    detail=service.proposal(cid,ProposalInput(action='request_quote',category='appliance',work_item='Dishwasher'),ACTOR)
    assert detail['case']['triage']['state']=='staff' and 'triage' not in {b['key'] for b in detail['decision']['blockers']}
