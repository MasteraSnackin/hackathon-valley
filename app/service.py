"""Application service: transactions, evidence, policy, reviews and simulated tools."""
from __future__ import annotations
import uuid, json, os, re
from collections import Counter
from copy import deepcopy
from datetime import timedelta
from .store import Store, payload
from .domain import *
from . import ai, jev, parties
from .parties import PARTY_LABELS, PARTY_QUESTIONS, ANSWERED_BY

# Actor recorded on events and records produced from Claude's readings.
CLAUDE={'id':'claude','role':'model'}
JEV={'id':'jev','role':'model'}
DEMO_DIRECTORY='Fictional demo directory: DEMO-FLAT-1, tenant demo-resident, verified in-app demonstration route. No real address or recipient.'
VOICE_BRIDGE={'id':'voice-bridge','role':'case_manager','bridge':'voice'}
def directory_text(ref):
    names=', '.join(f"{PARTY_LABELS[p['kind']].lower()} {p['name']}" for p in parties.PARTIES if ref in p['properties'])
    return f"Fictional party directory: {ref} ({parties.PROPERTIES[ref]['address']}); {names}; verified simulated contact routes. No real address or recipient."

def arr_(value): return value if isinstance(value,list) else []
class Forbidden(ValueError): pass
class Conflict(ValueError): pass

class Service:
    def __init__(self,store=None):
        self.db=store or Store()
        with self.db.tx() as c:
            if not self.db.get_meta(c,'active_policy'):
                p,_=self.db.add(c,'policy',{'version':1,'status':'published','settings':deepcopy(DEFAULT_SETTINGS),'rules':[],'author':'demo-setup','reason':'Illustrative demonstration defaults, not official rules.','effective_at':stamp()})
                self.db.set_meta(c,'active_policy',p['id'])
    def active(self,c): return payload(self.db.get_record(c,self.db.get_meta(c,'active_policy')))
    def rows(self,c,kind,cid): return [payload(r) for r in self.db.list(c,kind,cid)]
    def role(self,actor,allowed):
        if actor.get('role') not in allowed: raise Forbidden('This decision requires one of these roles: '+', '.join(sorted(allowed)))
    def event(self,c,case,kind,data,actor):
        r,_=self.db.add(c,'incoming_event',{'event_type':kind,'data':data,'actor':actor,'revision':case['revision']},case['id'])
        self.db.add(c,'signal_outbox',{'event_id':r['id'],'revision':case['revision']},case['id'],dedupe='outbox:'+r['id'])
        return r
    def bump(self,c,case): case['revision']+=1; self.db.save_case(c,case)
    def new_case(self,c,*,title,property_ref,report,category,action,work_item,provider,access_method,actor,triage_state,category_source,route_source,source_label='Intake report',parent_case_id=None,party=None):
        case={'id':uuid.uuid4().hex,'title':title,'property_ref':property_ref,'category':category or 'other','category_source':category_source,'route_source':route_source,'profile':'demo','revision':1,'action_revision':1,'proposal':{'action':action or 'clarify','work_item':work_item,'provider':provider,'access_method':access_method,'scope':{}},'status':'open','owner':'case_manager','next_step':'Assess intake','policy_pending':False,'created_at':stamp(),'triage':{'state':triage_state}}
        if parent_case_id:case['parent_case_id']=parent_case_id
        self.db.save_case(c,case,True)
        evidence,_=self.db.add(c,'evidence',{'text':report,'source_label':source_label,'actor':actor,'occurred_at':stamp(),'triage':'pending' if triage_state=='pending' else 'not_required',**({'party':party} if party else {})},case['id'])
        if triage_state=='pending':case['triage']['source_id']=evidence['id']
        if property_ref=='DEMO-FLAT-1':
            directory,_=self.db.add(c,'evidence',{'text':DEMO_DIRECTORY,'source_label':'Preconfigured fictional demo directory','actor':{'id':'demo-setup','role':'case_manager'},'occurred_at':stamp(),'triage':'not_required'},case['id'])
            for key in ['identity','route']:
                self.db.add(c,'claim',{'key':key,'value':True,'scope':{'property_ref':'DEMO-FLAT-1'},'source_id':directory['id'],'source_quote':DEMO_DIRECTORY,'verified':True,'verification':'Preconfigured demonstration directory','supersedes':[]},case['id'])
        elif property_ref in parties.PROPERTIES:
            text=directory_text(property_ref)
            directory,_=self.db.add(c,'evidence',{'text':text,'source_label':'Preconfigured fictional party directory','actor':{'id':'demo-setup','role':'case_manager'},'occurred_at':stamp(),'triage':'not_required'},case['id'])
            for key in ['identity','route']:
                self.db.add(c,'claim',{'key':key,'value':True,'scope':{'property_ref':property_ref},'source_id':directory['id'],'source_quote':text,'verified':True,'verification':'Preconfigured fictional party directory (demonstration only)','supersedes':[]},case['id'])
        return case,evidence
    def intake(self,data:Intake,actor,self_identification=None):
        """self_identification: {name, address, conversation_id}, set only by the tenant portal bridge."""
        self.role(actor,{'case_manager'})
        input_hash=digest(data.model_dump(exclude={'idempotency_key'}))
        # The report is stored before anyone reads it; Claude triage runs in the
        # case coordinator, never inside this request.
        with self.db.tx() as c:
            if data.idempotency_key:
                existing=next((r for r in self.db.list(c,'intake_receipt') if r['payload']['idempotency_key']==data.idempotency_key),None)
                if existing:
                    if existing['payload']['input_hash']!=input_hash:raise Conflict('Intake idempotency key belongs to a different request')
                    return self.detail_tx(c,existing['case_id'])
            staff=data.triage=='staff'
            case,evidence=self.new_case(c,title=data.title,property_ref=data.property_ref,report=data.report,category=data.category,action=data.action,work_item=data.work_item,provider=data.provider,access_method=data.access_method,actor=actor,
                triage_state='staff' if staff else 'pending',category_source='staff' if data.category else 'claude',route_source='staff' if data.action else 'claude')
            if self_identification:
                case['self_identification']={**self_identification,'source_id':evidence['id'],'at':stamp(),'corrected':False}
                self.db.save_case(c,case)
            if staff and case['category']!='other':
                # Manual triage: the case manager owns the classification fact.
                self.db.add(c,'claim',{'key':'classification','value':True,'scope':{'property_ref':case['property_ref'],'work_item':data.work_item,'category':case['category']},'source_id':evidence['id'],'source_quote':data.report,'verified':True,'verification':'Manual triage by the case manager at intake','verified_by':actor,'supersedes':[]},case['id'])
            if data.idempotency_key:self.db.add(c,'intake_receipt',{'idempotency_key':data.idempotency_key,'input_hash':input_hash},case['id'],dedupe='intake:'+data.idempotency_key)
            self.event(c,case,'intake',{'evidence_id':evidence['id']},actor)
            self.assess(c,case)
            return self.detail_tx(c,case['id'])
    def claims(self,c,cid): return self.rows(c,'claim',cid)
    def approvals(self,c,cid):
        grants=self.rows(c,'approval',cid); revoked={r['approval_id'] for r in self.rows(c,'approval_revoked',cid)}
        return [{**r,'revoked':r['id'] in revoked} for r in grants]
    def action_states(self,c,cid):
        actions={}
        for r in self.rows(c,'action',cid): actions[r['business_id']]=r
        return list(actions.values())
    def reviews(self,c,case):
        responses={r['review_id']:r for r in self.rows(c,'review_response',case['id'])}
        superseded={r['review_id'] for r in self.rows(c,'review_superseded',case['id'])}
        policy=self.active(c)
        result=[]
        for r in self.rows(c,'review',case['id']):
            response=responses.get(r['id']); status='open'
            if response: status='deferred' if response['decision']=='defer' else 'resolved'
            if r['action_revision']!=case['action_revision'] or r['policy_version']!=policy['version']: status='superseded'
            if r['id'] in superseded: status='superseded'
            if dt(r['expires_at'])<=now() and status in {'open','deferred'}: status='expired'
            result.append({**r,'status':status,'response':response})
        return result
    def questions(self,c,case):
        closed={r['question_id']:r for r in self.rows(c,'question_closed',case['id'])}
        reminders=self.rows(c,'reminder',case['id']); escalations=self.rows(c,'question_escalated',case['id'])
        s=self.active(c)['settings']; result=[]
        sent={}
        for m in self.tenant_messages(c,case['id']):
            if m['status']!='sent':continue
            for qid in m['question_ids']:
                sent.setdefault(qid,{'sent_at':m['sent_at'],'message_id':m['id'],'tenant_text':next((x['text'] for x in m.get('questions',[]) if x['question_id']==qid),None)})
        for q in self.rows(c,'question',case['id']):
            # Questions to a tenant, landlord or contractor go out only in a sent
            # message; other clarifications are simulated to staff at once.
            addressee=q['addressee'] if 'addressee' in q else ('tenant' if q['key'] in TENANT_TOPIC_FOR else None)
            delivery=sent.get(q['id']) or ({} if addressee else {'sent_at':q['opened_at']})
            row={**q,**delivery,'addressee':addressee,'topic':self.topic_for(q['key'],addressee),'tenant_question':addressee=='tenant','status':'closed' if q['id'] in closed else 'open','answered':bool(closed.get(q['id'],{}).get('answered')),
                 'reminders':sum(r['question_id']==q['id'] for r in reminders),'escalated':any(r['question_id']==q['id'] for r in escalations)}
            row['reminder_at'],row['deadline']=self.question_times(row,s,row['reminders'])
            result.append(row)
        return result
    def addressee(self,case,key):
        """Who a clarification goes to: a directory party, the tenant, or staff only (None)."""
        kind=PARTY_QUESTIONS.get(key,(None,))[0]
        if kind and case['property_ref'] in parties.PROPERTIES and parties.on_property(kind,case['property_ref']):return kind
        return 'tenant' if key in TENANT_TOPIC_FOR else None
    @staticmethod
    def topic_for(key,addressee):
        return PARTY_QUESTIONS[key][1] if addressee not in {'tenant',None} else TENANT_TOPIC_FOR.get(key,key)
    @staticmethod
    def may_answer(q,party):
        """Only the party a question went to (or the agency for a landlord) can answer it."""
        addressee=q.get('addressee')
        if addressee is None:return True
        if not party:return addressee=='tenant'
        return party['kind'] in ANSWERED_BY.get(addressee,set())
    def question_times(self,q,s,reminders=0):
        """Reminders count from delivery; escalation also runs while a draft waits."""
        base=dt(q.get('sent_at') or q['opened_at'])
        reminder=stamp(working_after(base,s['reminder_hours']*(reminders+1),s['holiday_dates'])) if q.get('sent_at') else None
        return reminder,stamp(working_after(base,s['escalation_hours'],s['holiday_dates']))
    def detail_tx(self,c,cid):
        case=self.db.case(c,cid); decisions=self.rows(c,'decision',cid)
        claims=self.claims(c,cid)
        replacements={old:new['id'] for new in claims if new.get('verified') for old in new.get('supersedes',[])}
        return {'case':case,'claims':[{**claim,**({'superseded_by':replacements[claim['id']]} if claim['id'] in replacements else {})} for claim in claims],'evidence':self.rows(c,'evidence',cid),'decision':decisions[-1] if decisions else None,'reviews':self.reviews(c,case),'questions':self.questions(c,case),'tenant_messages':self.tenant_messages(c,cid),'actions':self.action_states(c,cid),'timeline':self.db.list(c,case_id=cid)}
    def detail(self,cid):
        with self.db.tx() as c:return self.detail_tx(c,cid)
    def list_cases(self):
        with self.db.tx() as c:
            result=[]
            for case in self.db.case_list(c):
                result.append({**case,'outcome':case.get('stage','unassessed'),'open_reviews':sum(r['status'] in {'open','deferred'} for r in self.reviews(c,case))})
            return sorted(result,key=lambda x:x['created_at'],reverse=True)
    def create_review(self,c,case,decision,blocker,force=False,at=None):
        at=at or now(); policy=self.active(c)
        sig=digest({'key':blocker['key'],'rule':blocker['rule_id'],'claims':blocker['claim_ids'],'action_revision':case['action_revision'],'policy':policy['version']})
        existing=[r for r in self.reviews(c,case) if r.get('signature')==sig and r['status'] in {'open','deferred'}]
        if existing and not force:return existing[0]
        review={'key':blocker['key'],'signature':sig,'question':blocker['reason'],'owner':blocker['owner'],'rule_id':blocker['rule_id'],'policy_version':policy['version'],'action_revision':case['action_revision'],'scope':scope_of(case),'source_ids':blocker['source_ids'],'claim_ids':blocker['claim_ids'],'other_blockers':[b['key'] for b in decision['blockers'] if b!=blocker],'expires_at':stamp(at+timedelta(hours=policy['settings']['approval_hours'])),'next_step':'Reassess all checks. Only this blocker can be resolved by this response.'}
        r,_=self.db.add(c,'review',review,case['id']); return payload(r)
    def assess(self,c,case,explicit=False,at=None):
        at=at or now(); policy=self.active(c)
        completed=next((a for a in self.action_states(c,case['id']) if a['business_id']==business_id(case) and a['status']=='succeeded'),None)
        if completed:
            original=payload(self.db.get_record(c,completed['decision_id']))
            result={**{k:v for k,v in original.items() if k not in {'id','created_at'}},'outcome':'NO FURTHER ACTION','blockers':[],'next_step':'This action already has a confirmed simulated receipt. Select a new proposal for further work.','owner':'case_manager','completed_action_id':completed['id'],'assessed_at':stamp(at)}
            case['policy_pending']=False;case['stage']='NO FURTHER ACTION';case['next_step']=result['next_step']
            for review in self.reviews(c,case):
                if review['status'] in {'open','deferred'}:self.db.add(c,'review_superseded',{'review_id':review['id'],'reason':'This business action is already completed; original decision retained.'},case['id'],dedupe='review_superseded:'+review['id'])
            r,_=self.db.add(c,'decision',result,case['id']);self.db.save_case(c,case);return payload(r)
        if explicit and case.get('policy_pending'):
            case['policy_pending']=False
            self.db.add(c,'policy_reassessment',{'policy_version':policy['version'],'revision':case['revision']},case['id'])
        uncertain=any(a['status']=='uncertain' for a in self.action_states(c,case['id']))
        result=evaluate(case,self.claims(c,case['id']),self.approvals(c,case['id']),policy,uncertain,at)
        if self.addressee(case,'authority')=='landlord' and all(x['status']=='PASS' for x in result['checks'] if x['key'] in {'identity','route'}):
            # On a directory property the landlord is asked first. Their answer
            # is only a claim: an approver verifies it, or takes over at the deadline.
            for b in result['blockers']:
                if b['key']=='authority' and b['status']=='UNKNOWN' and not b['claim_ids'] and b['response']=='HUMAN REVIEW':
                    b['response']='CLARIFY';b['reason']='Ask the landlord or their letting agency to approve this work. '+b['reason']
        blockers={b['key']:b for b in result['blockers']}
        questions=self.questions(c,case)
        for q in questions:
            if q['status']!='open':continue
            if q['key'] not in blockers or q['action_revision']!=case['action_revision']:
                self.db.add(c,'question_closed',{'question_id':q['id'],'reason':'Evidence satisfied the requirement or the action was superseded; old reminders cancelled.'},case['id'],dedupe='question_closed:'+q['id'])
            elif blockers[q['key']]['claim_ids']:
                # A reply asserted the fact: stop chasing, a person verifies it.
                self.db.add(c,'question_closed',{'question_id':q['id'],'answered':True,'reason':'A source asserting this fact was received; it now awaits verification.'},case['id'],dedupe='question_closed:'+q['id'])
        answered={q['key'] for q in questions if q['answered'] and q['action_revision']==case['action_revision']}
        for b in result['blockers']:
            if b['response']=='CLARIFY' and b['claim_ids']:
                b['response']='HUMAN REVIEW'
                b['reason']='Verify the received source assertion. '+b['reason']
            if b['response']=='CLARIFY' and b['key']=='classification' and (case['category']=='other' or any(x['key']=='triage' and x['response']=='CLARIFY' for x in result['blockers'])):
                # The routing question already covers it, or a person must define
                # handling for an unsupported category: never ask the tenant twice.
                b['response']='WAIT'
                b['reason']='Settled by the open routing clarification or the supported-process review. '+b['reason']
            if b['response']=='CLARIFY' and b['key'] in answered and not any(q['status']=='open' and q['key']==b['key'] and q['action_revision']==case['action_revision'] for q in questions):
                # Never ask the tenant the same thing again after a reply.
                b['response']='HUMAN REVIEW'
                b['reason']='The tenant replied, but the reply did not settle this. Review it and record the fact. '+b['reason']
            if b['response']=='CLARIFY':
                # Every initial request and reminder is a visibly simulated communication.
                q=next((q for q in questions if q['status']=='open' and q['key']==b['key'] and q['action_revision']==case['action_revision']),None)
                if not q:
                    row,_=self.db.add(c,'question',{'key':b['key'],'question':b['reason'],'addressee':self.addressee(case,b['key']),'scope':scope_of(case),'action_revision':case['action_revision'],'policy_version':policy['version'],'opened_at':stamp(at),'reminder_at':stamp(working_after(at,policy['settings']['reminder_hours'],policy['settings']['holiday_dates'])),'deadline':stamp(working_after(at,policy['settings']['escalation_hours'],policy['settings']['holiday_dates'])),'simulated':True,'owner':b['owner']},case['id'])
                    q=payload(row)
                    # Questions to the tenant, landlord or contractor are drafted by
                    # Claude in the coordinator's message step; staff get the policy text.
                    if not q['addressee']:self.db.add(c,'simulated_clarification',{'question_id':q['id'],'text':b['reason'],'simulated':True},case['id'])
                else:
                    b['response']='HUMAN REVIEW' if q.get('escalated') else 'WAIT'
                    if q.get('escalated'): b['reason']='No relevant answer by the deadline. '+b['reason']
            if b['response'] in {'HUMAN REVIEW','STOP ACTION'}: self.create_review(c,case,result,b,at=at)
        if result['blockers']:
            order={'STOP ACTION':0,'HUMAN REVIEW':1,'CLARIFY':2,'WAIT':3}
            result['blockers'].sort(key=lambda b:order[b['response']]); result['outcome']=result['blockers'][0]['response']; result['owner']=result['blockers'][0]['owner']; result['next_step']=result['blockers'][0]['reason']
        result['claim_snapshot']=[x['id'] for x in self.claims(c,case['id'])]; result['policy_id']=policy['id']
        for review in self.reviews(c,case):
            blocker=next((b for b in result['blockers'] if b['key']==review['key'] and b['rule_id']==review['rule_id']),None)
            if review['status'] in {'open','deferred'} and (blocker is None or set(blocker['claim_ids'])!=set(review['claim_ids'])):
                self.db.add(c,'review_superseded',{'review_id':review['id'],'reason':'Relevant evidence or current blockers changed; assess the current review.'},case['id'],dedupe='review_superseded:'+review['id'])
        r,_=self.db.add(c,'decision',result,case['id'])
        case['owner']=result['owner'];case['next_step']=result['next_step']; case['stage']=result['outcome'];case['last_assessed_at']=stamp(at)
        self.db.save_case(c,case)
        return payload(r)
    def evaluate_case(self,cid,actor):
        self.role(actor,{'case_manager','policy_editor','reviewer','approver','access_officer'})
        with self.db.tx() as c:
            case=self.db.case(c,cid); self.assess(c,case,explicit=True); self.event(c,case,'explicit_reassessment',{},actor); return self.detail_tx(c,cid)
    def evidence(self,cid,data:EvidenceInput,actor,party=None):
        """party: the directory match for the sender, set only by the inbound bridge."""
        self.role(actor,ROLES)
        with self.db.tx() as c:
            return self.evidence_tx(c,self.db.case(c,cid),data,actor,party)
    def evidence_tx(self,c,case,data:EvidenceInput,actor,party=None):
        cid=case['id']
        if data.supersedes: raise ValueError('Sources are superseded only by a reasoned, role-checked review correction')
        input_hash=digest(data.model_dump(exclude={'idempotency_key'}))
        # Staff-structured evidence (explicit quoted claims) is already
        # interpreted by a person; free text waits for Claude's reading.
        triage='staff_structured' if data.claims else 'pending'
        source,created=self.db.add(c,'evidence',{'text':data.text,'source_label':data.source_label,'actor':actor,'occurred_at':data.occurred_at or stamp(),'input_hash':input_hash,'triage':triage,**({'party':party} if party else {})},cid,dedupe=('evidence:'+cid+':'+data.idempotency_key) if data.idempotency_key else None)
        if not created:
            if source['payload'].get('input_hash')!=input_hash: raise Conflict('Idempotency key already belongs to different evidence')
            return self.detail_tx(c,cid)
        for claim in data.claims:
            if claim.key=='completion' and claim.value is True:case['completion_state']='reported; awaiting verification'
            scope=claim.scope or scope_of(case)
            if not scope_matches(scope,case): raise ValueError('Claim scope must match the current property and action; create a separate item for other work')
            self.db.add(c,'claim',{**claim.model_dump(),'scope':scope,'source_id':source['id'],'verified':False,'supersedes':[]},cid)
        if triage=='pending':case['triage']={**(case.get('triage') or {}),'state':'pending','source_id':source['id'],'confirmed':False}
        self.bump(c,case); self.event(c,case,'evidence_received',{'source_id':source['id']},actor); self.assess(c,case)
        return self.detail_tx(c,cid)
    def identity_corrected(self,cid,fields,actor):
        """The tenant changed their name or address: self-identification no longer counts."""
        with self.db.tx() as c:
            case=self.db.case(c,cid);sid=case.get('self_identification')
            if not sid or sid.get('corrected'):return
            case['self_identification']={**sid,'corrected':True,'corrected_to':{k:fields.get(k) for k in ('name','address')},'corrected_at':stamp()}
            self.bump(c,case);self.event(c,case,'self_identification_corrected',{},actor);self.assess(c,case)
    def tenant_reply(self,cid,text,actor):
        """A reply in the simulated in-app tenant thread, recorded as evidence."""
        return self.evidence(cid,EvidenceInput(text=text,source_label='Tenant reply (simulated in-app thread)'),actor)
    def proposal(self,cid,data:ProposalInput,actor):
        self.role(actor,{'case_manager'})
        with self.db.tx() as c:
            case=self.db.case(c,cid)
            if any(a['status']=='uncertain' for a in self.action_states(c,cid)): raise Conflict('Reconcile the uncertain action before replacing its scope')
            proposal=data.model_dump();category=proposal.pop('category',None)
            if proposal==case['proposal'] and (category is None or category==case['category']):return self.detail_tx(c,cid)
            # A staff choice is manual triage: Claude's later readings no longer
            # change this route, and a staff category settles a disagreement.
            triage=dict(case.get('triage') or {})
            if triage.get('state')=='failed':triage['state']='staff'
            if category is not None:
                case['category']=category;case['category_source']='staff'
                if triage.get('disagreement') or triage.get('route_disagreement'):triage['confirmed']=True
            case['triage']=triage;case['route_source']='staff'
            case['proposal']=proposal;case['action_revision']+=1;case['status']='open';self.bump(c,case)
            self.event(c,case,'proposal_changed',data.model_dump(),actor);self.assess(c,case)
            return self.detail_tx(c,cid)
    def respond(self,rid,data:ReviewResponse,actor):
        with self.db.tx() as c:
            row=self.db.get_record(c,rid)
            if row['kind']!='review':raise ValueError('Review not found')
            case=self.db.case(c,row['case_id']);review=next(r for r in self.reviews(c,case) if r['id']==rid)
            self.role(actor,{review['owner']})
            # Invalid/late responses are auditable, but have no effect on permissions.
            if review['status'] not in {'open','deferred'}:
                self.db.add(c,'rejected_review_response',{'review_id':rid,'reason':'stale, expired or duplicate response','actor':actor,'submitted':data.model_dump()},case['id'])
                c.commit(); raise Conflict('Review is stale, expired or already answered. Reassess the current action.')
            key=review['key'];scope=scope_of(case); policy=self.active(c)
            if data.decision=='approve' and key=='triage':
                self.role(actor,{'case_manager'})
                triage=case.get('triage') or {}
                if triage.get('state')!='done':raise ValueError('Only a completed Claude reading can be confirmed. Choose the action to triage this message manually.')
                case['triage']={**triage,'confirmed':True}
                self.db.add(c,'triage_confirmed',{'review_id':rid,'interpretation_id':triage.get('interpretation_id'),'reason':data.reason,'actor':actor},case['id'])
            elif data.decision=='approve':
                custom=next((r for r in policy.get('rules',[]) if 'rule:'+r['id']==key and r['response']=='HUMAN REVIEW'),None)
                if key not in {'authority','finance'} and not custom:raise ValueError('Approval cannot substitute for required facts or another person\'s consent')
                self.role(actor,{custom['owner']} if custom else {'approver'})
                if data.scope!=scope:raise Conflict('Approval scope must exactly match the current action')
                if not data.expires_at or not now()<dt(data.expires_at)<=now()+timedelta(hours=policy['settings']['approval_hours']):raise ValueError('Approval needs a future expiry within the policy limit')
                self.require_source(c,case['id'],data.source_id)
                claims=self.claims(c,case['id']);check=evaluate(case,claims,self.approvals(c,case['id']),policy)
                if any(b['key']==key and b['status'] in {'FAIL','CONFLICT'} for b in check['blockers']):raise Conflict('Resolve the refusal or conflicting sources before a scoped approval')
                self.db.add(c,'approval',{'key':key,'scope':scope,'action_revision':case['action_revision'],'policy_version':policy['version'],'expires_at':data.expires_at,'source_id':data.source_id,'reason':data.reason,'actor':actor,'basis_hash':approval_basis(case,claims,key,policy)},case['id'])
            elif data.decision=='correct':
                if key not in FACTS: raise ValueError('This rule requires evidence or a policy change; a generic correction cannot waive it')
                self.role(actor,FACT_ROLES[key])
                claims=self.claims(c,case['id']);claim=next((x for x in claims if x['id']==data.claim_id and x['key']==key),None)
                if not claim or not scope_matches(claim['scope'],case):raise ValueError('Choose a source claim for this requirement and current action')
                if data.source_id!=claim['source_id']:raise ValueError('Correction source must be the chosen claim\'s evidence')
                self.require_source(c,case['id'],data.source_id)
                if data.key is not None and data.key!=key:raise ValueError('Correction cannot resolve a different requirement')
                if data.value is not None and data.value!=claim['value']:raise ValueError('Correction must preserve the selected source claim; add new evidence first')
                supersedes=[x['id'] for x in claims if x['key']==key and scope_matches(x['scope'],case)]
                expires=data.expires_at
                if key in {'access','keys','authority'}:
                    expires=expires or stamp(now()+timedelta(hours=policy['settings']['approval_hours']))
                    if not now()<dt(expires)<=now()+timedelta(hours=policy['settings']['approval_hours']):raise ValueError('Permission expiry must be within the policy limit')
                self.db.add(c,'claim',{**{k:v for k,v in claim.items() if k not in {'id','created_at'}},'verified':True,'scope':scope if key in {'access','keys','authority','schedule','total','classification'} else claim['scope'],'supersedes':supersedes,'verification':data.reason,'verified_by':actor,'expires_at':expires},case['id'])
            elif data.decision=='reject':
                case['rejected_action_revision']=case['action_revision']
                self.db.add(c,'action_rejected',{'review_id':rid,'scope':scope,'action_revision':case['action_revision'],'reason':data.reason,'actor':actor},case['id'])
            elif data.decision=='defer':
                if not data.deadline or not now()<dt(data.deadline)<=now()+timedelta(hours=168):raise ValueError('Deferral needs a future deadline within seven days')
            elif data.decision=='more_evidence':
                self.db.add(c,'human_evidence_request',{'review_id':rid,'reason':data.reason,'simulated':True,'actor':actor},case['id'])
            self.db.add(c,'review_response',{'review_id':rid,'actor':actor,**data.model_dump()},case['id']); self.bump(c,case);self.event(c,case,'review_responded',{'review_id':rid,'decision':data.decision},actor);self.assess(c,case)
            return self.detail_tx(c,case['id'])
    # ---- Claude triage: read each stored message once, then route the case.
    def pending_sources(self,c,cid):
        retries=Counter(r['source_id'] for r in self.rows(c,'triage_retry',cid))
        done={(r['source_id'],r.get('attempt',0)) for r in self.rows(c,'interpretation',cid)}
        return [e for e in self.rows(c,'evidence',cid) if e.get('triage')=='pending' and (e['id'],retries[e['id']]) not in done]
    def attempt_of(self,c,cid,sid): return sum(r['source_id']==sid for r in self.rows(c,'triage_retry',cid))
    def routings(self,c,cid): return {(r['source_id'],r['attempt']):r for r in self.rows(c,'routing',cid)}
    def awaiting_route(self,c,cid):
        """Unread messages Jev has not routed yet (none when the policy router is claude)."""
        if self.active(c)['settings']['router']=='claude':return []
        routed=self.routings(c,cid)
        return [e for e in self.pending_sources(c,cid) if (e['id'],self.attempt_of(c,cid,e['id'])) not in routed]
    def awaiting_reading(self,c,cid):
        waiting={e['id'] for e in self.awaiting_route(c,cid)}
        return [e for e in self.pending_sources(c,cid) if e['id'] not in waiting]
    # ---- Jev routing: one fast calibrated call per message; uncertain messages go to Claude.
    def route_messages(self,cid):
        routed=jev_only=0
        for _ in range(20):
            with self.db.tx() as c:
                waiting=self.awaiting_route(c,cid)
                if not waiting:break
                source=waiting[0];case=self.db.case(c,cid);settings=self.active(c)['settings']
                attempt=self.attempt_of(c,cid,source['id']);context=self.triage_context(c,case,source)
            answers=error=None;meta={'provider':'typesafe','requested_model':jev.model_id(),'router_version':jev.ROUTER_VERSION}
            if case.get('route_source')=='staff':
                decision={'mode':'claude','route':None,'reasons':['Staff chose the route; Claude reads the message.']}
            else:
                # The model call happens outside any database transaction.
                try:answers,meta=jev.ask(source['text'],context)
                except jev.JevUnavailable as exc:
                    error=exc;decision={'mode':'claude','route':None,'reasons':[f'Jev unavailable ({exc.error_type}); Claude triages.']}
                else:decision=jev.decide(answers,context,settings)
            proposed=decision['mode']
            # Shadow mode records Jev's decision for comparison; Claude decides.
            if settings['router']=='jev_shadow':decision={**decision,'mode':'claude','reasons':['Shadow mode: Claude decides.',*decision['reasons']]}
            with self.db.tx() as c:
                record={**meta,'source_id':source['id'],'attempt':attempt,'router':settings['router'],'mode':decision['mode'],'proposed_mode':proposed,
                        'route':decision.get('route'),'decision':decision,'answers':answers,'error_type':error.error_type if error else None}
                rec,created=self.db.add(c,'routing',record,cid,dedupe=f"route:{source['id']}:{attempt}")
                if not created:continue
                case=self.db.case(c,cid);routed+=1
                self.event(c,case,'message_routed',{'source_id':source['id'],'routing_id':rec['id'],'mode':decision['mode'],'route':decision.get('route')},JEV)
                if decision['mode']=='jev_only':
                    jev_only+=1
                    self.apply_triage(c,cid,source,attempt,jev.reading(decision,source['text'],case),{**meta,'routing_id':rec['id']},None,routing={**record,'id':rec['id']})
        return {'routed':routed,'jev_only':jev_only}
    def triage_context(self,c,case,source):
        p=case['proposal']; t=case.get('triage') or {}
        earlier=[e for e in self.rows(c,'evidence',case['id']) if e['id']!=source['id'] and e.get('triage')!='not_required'][-6:]
        return {'case':{'property_ref':case['property_ref'],'category':case['category'],'category_set_by':case.get('category_source'),'current_action':p['action'],
                        'route_set_by':case.get('route_source'),'work_item':p['work_item'],'status':case['status'],'last_completed_action':case.get('last_verified_action'),
                        'first_report':not t.get('route') and t.get('state')!='done'},
                'open_questions':[{'id':q['id'],'topic':q['topic'],'question':q.get('tenant_text') or q['question']} for q in self.questions(c,case) if q['status']=='open' and self.may_answer(q,source.get('party'))],
                'previous_ambiguities':[a['description'] for a in t.get('open_ambiguities',[])],
                'earlier_messages':[{'label':e['source_label'],'received_at':e.get('occurred_at'),'text':e['text'][:4000],'truncated':len(e['text'])>4000} for e in earlier],
                'new_message_label':source['source_label'],
                **({'sender_party':{k:source['party'][k] for k in ('kind','name','verified')}} if source.get('party') else {})}
    def triage_messages(self,cid):
        """Claude reads each routed message: fully when Jev handed it off, as extraction when Jev routed it."""
        # Direct callers (replay, tests) may not have run the routing step yet.
        self.route_messages(cid)
        spawned=[]; count=0
        for _ in range(20):
            with self.db.tx() as c:
                case=self.db.case(c,cid); pending=self.awaiting_reading(c,cid)
                if not pending:break
                source=pending[0]; attempt=self.attempt_of(c,cid,source['id'])
                context=self.triage_context(c,case,source); routing=self.routings(c,cid).get((source['id'],attempt))
            locked=routing if routing and routing['mode']=='jev_route' else None
            # The model call happens outside any database transaction.
            try:result,meta=ai.triage(source['text'],context,{'route':locked['route'],'reasons':locked['decision']['reasons']} if locked else None);error=None
            except ai.ClaudeUnavailable as exc:result,error=None,exc;meta={'provider':'anthropic','requested_model':ai.model_id(),'prompt_version':ai.PROMPT_VERSION}
            if routing:meta={**meta,'routing_id':routing['id']}
            with self.db.tx() as c:spawned+=self.apply_triage(c,cid,source,attempt,result,meta,error,routing=routing)
            count+=1
        return {'triaged':count,'spawned_case_ids':spawned}
    def apply_triage(self,c,cid,source,attempt,result,meta,error,routing=None):
        case=self.db.case(c,cid); policy=self.active(c); s=policy['settings']
        base={'source_id':source['id'],'attempt':attempt,**meta}
        router=None
        if routing:
            d=routing['decision']
            router={'mode':routing['mode'],'proposed_mode':routing['proposed_mode'],'route':d.get('route'),'route_confidence':d.get('route_confidence'),
                    'jev_route':(routing.get('answers') or {}).get('route',{}).get('choice'),'reasons':d['reasons'],'model':routing.get('model'),'routing_id':routing['id']}
        if error:
            rec,created=self.db.add(c,'interpretation',{**base,'status':'failed','error_type':error.error_type,'error':str(error)[:300]},cid,dedupe=f"triage:{source['id']}:{attempt}")
            if not created:return []
            case['triage']={'state':'failed','source_id':source['id'],'error':error.error_type,'interpretation_id':rec['id'],'router':router}
            self.bump(c,case);self.event(c,case,'triage_failed',{'source_id':source['id'],'error_type':error.error_type},CLAUDE);self.assess(c,case)
            return []
        checked=ai.checked_triage(result,source['text'])
        rec,created=self.db.add(c,'interpretation',{**base,'status':'ok','result':checked},cid,dedupe=f"triage:{source['id']}:{attempt}")
        if not created:return []
        previous=case.get('triage') or {}; first=not previous.get('route')
        issues=checked['issues']
        primary=next((i for i in issues if i['relation']=='current_case'),issues[0] if issues else None)
        route_ambiguities=[a for a in checked['ambiguities'] if a['affects_route']]
        disagreement=route_disagreement=None;confidence=checked['confidence']
        if routing and routing['mode']=='jev_route':
            # Jev's route stands unless Claude objects. An objection applies
            # Claude's route and holds the case for a person, so a disputed
            # route never anchors later readings. A hazard is never de-escalated.
            locked=routing['route'];objection=checked.get('route_objection','').strip()
            if primary is None:route_disagreement={'jev':locked,'claude':'no actionable issue','reason':objection}
            else:
                if primary['route']!=locked or objection:route_disagreement={'jev':locked,'claude':primary['route'],'reason':objection}
                if locked=='urgent_hazard' or not route_disagreement:primary['route']=locked
            confidence=jev.combined_confidence(confidence,routing['decision'])
        if primary:
            route=ROUTES[primary['route']]; category=route.get('category',primary['category'])
            if case.get('category_source')=='staff':
                if category not in {case['category'],'other'}:disagreement={'staff':case['category'],'claude':category}
            else:case['category']=category
            uncertain=any(a['status']=='uncertain' for a in self.action_states(c,cid))
            if case.get('route_source')!='staff' and not uncertain:
                # The work item is named once; later messages move the same item
                # along its workflow so existing evidence keeps its scope.
                work_item=primary['work_item'][:200].strip() if first and primary['work_item'].strip() else case['proposal']['work_item']
                if route['action']!=case['proposal']['action'] or work_item!=case['proposal']['work_item']:
                    case['proposal']={**case['proposal'],'action':route['action'],'work_item':work_item,'scope':{}};case['action_revision']+=1;case['status']='open'
                    self.db.add(c,'route_changed',{'interpretation_id':rec['id'],'route':primary['route'],'action':route['action'],'work_item':work_item,'action_revision':case['action_revision']},cid)
            self.issue_claims(c,case,source['id'],rec['id'],{**checked,'confidence':confidence},issues.index(primary),policy,blocked=bool(route_ambiguities or disagreement or route_disagreement),
                # Jev does not look for ambiguity, so a Jev-only category waits for the case manager.
                auto_accept=not (routing and routing['mode']=='jev_only'),party=source.get('party'))
        open_q={q['id'] for q in self.questions(c,case) if q['status']=='open' and self.may_answer(q,source.get('party'))}
        for a in checked['answers']:
            if a['question_id'] not in open_q:continue
            if a['status']=='answered':
                self.db.add(c,'question_closed',{'question_id':a['question_id'],'answered':True,'source_id':source['id'],'reason':"Answered in a reply (Claude's reading). The answer is an unverified assertion."},cid,dedupe='question_closed:'+a['question_id'])
            elif a['status']=='partial':
                self.db.add(c,'question_followup',{'question_id':a['question_id'],'source_id':source['id'],'source_quote':a['source_quote']},cid,dedupe=f"followup:{a['question_id']}:{source['id']}")
        case['triage']={'state':'done','source_id':source['id'],'interpretation_id':rec['id'],'model':meta.get('model'),'intent':checked['intent'],'summary':checked['summary'],
            'route':primary['route'] if primary else previous.get('route'),'confidence':confidence,'rationale':checked['rationale'],
            'open_ambiguities':route_ambiguities,'other_ambiguities':[a for a in checked['ambiguities'] if not a['affects_route']],
            'disagreement':disagreement,'route_disagreement':route_disagreement,'router':router,'risk_flags':checked['risk_flags'],'rejected_items':checked['rejected'],'confirmed':False}
        mode='claude' if not router or router['mode']=='claude' else 'jev' if router['mode']=='jev_only' else 'jev+claude'
        # Kept for the existing dashboard panel.
        case['interpretation']={'mode':mode,'model':meta.get('model'),'summary':checked['summary'],'category':case['category'],'proposed_action':case['proposal']['action'],
            'confidence':confidence,'uncertainties':[a['description'] for a in checked['ambiguities']],'source_id':source['id'],'router':router}
        spawned=[]
        for i,issue in enumerate(issues):
            if issue is primary or issue['relation']!='new_issue':continue
            _,new=self.db.add(c,'issue_split',{'source_id':source['id'],'issue_index':i,'parent_case_id':cid},cid,dedupe=f"split:{source['id']}:{i}")
            if new:spawned.append(self.split_issue(c,case,source,rec['id'],checked,i,policy))
        self.bump(c,case)
        self.event(c,case,'triage_completed',{'source_id':source['id'],'interpretation_id':rec['id'],'route':case['triage']['route'],'mode':mode,'split_case_ids':spawned},JEV if mode=='jev' else CLAUDE)
        self.assess(c,case)
        return spawned
    def issue_claims(self,c,case,source_id,interpretation_id,checked,index,policy,blocked=False,auto_accept=True,party=None):
        """Store one issue's assertions unverified; auto-accept only the derived category label when policy allows."""
        issue=checked['issues'][index]; s=policy['settings']
        for claim in checked['claims']:
            if claim['issue_index']!=index:continue
            value=claim['amount'] if claim['key']=='total' else claim['value']
            # Authority is only read from a directory-matched sender; from anyone
            # but the landlord or agency it is hearsay, as is a tenant's quote.
            if claim['key']=='authority' and not party:continue
            extra={'party':party['kind'],**({'hearsay':True} if not parties.counts_for(claim['key'],value,party) else {})} if party else {}
            self.db.add(c,'claim',{'key':claim['key'],'value':value,'scope':scope_of(case),'scope_origin':'case-envelope','source_id':source_id,'source_quote':claim['source_quote'],'verified':False,'origin':'claude','interpretation_id':interpretation_id,'supersedes':[],**extra},case['id'])
        if ROUTES[issue['route']].get('urgent') and not any(x['key']=='urgent' and x['issue_index']==index for x in checked['claims']):
            self.db.add(c,'claim',{'key':'urgent','value':True,'scope':scope_of(case),'scope_origin':'case-envelope','source_id':source_id,'source_quote':issue['source_quote'],'verified':False,'origin':'claude','interpretation_id':interpretation_id,'supersedes':[]},case['id'])
        if case['category']=='other' or blocked:return
        scope={'property_ref':case['property_ref'],'work_item':case['proposal']['work_item'],'category':case['category']}
        if any(x['key']=='classification' and x['scope']==scope for x in self.claims(c,case['id'])):return
        threshold=s['triage_auto_accept']
        accepted=auto_accept and threshold!='never' and CONFIDENCE_RANK[checked['confidence']]>=CONFIDENCE_RANK[threshold]
        self.db.add(c,'claim',{'key':'classification','value':True,'scope':scope,'source_id':source_id,'source_quote':issue['source_quote'],'verified':accepted,'origin':'claude','interpretation_id':interpretation_id,
            'verification':f"Claude's derived category, auto-accepted by policy v{policy['version']} at {checked['confidence']} confidence" if accepted else None,'supersedes':[]},case['id'])
    def split_issue(self,c,parent,source,interpretation_id,checked,index,policy):
        issue=checked['issues'][index]; route=ROUTES[issue['route']]
        case,evidence=self.new_case(c,title=(parent['title']+' · '+issue['work_item'])[:160],property_ref=parent['property_ref'],report=source['text'],category=route.get('category',issue['category']),action=route['action'],
            work_item=issue['work_item'][:200] or 'Separate issue',provider=parent['proposal']['provider'],access_method=parent['proposal']['access_method'],actor=CLAUDE,triage_state='done',
            category_source='claude',route_source='claude',source_label=f"Split from case {parent['id'][:12]}: {source['source_label']}",parent_case_id=parent['id'],party=source.get('party'))
        self.issue_claims(c,case,evidence['id'],interpretation_id,checked,index,policy,party=source.get('party'))
        case['triage']={'state':'done','source_id':evidence['id'],'interpretation_id':interpretation_id,'route':issue['route'],'confidence':checked['confidence'],'summary':checked['summary'],
            'risk_flags':checked['risk_flags'],'open_ambiguities':[],'split_from':parent['id'],'confirmed':False}
        self.db.save_case(c,case)
        self.event(c,case,'intake',{'evidence_id':evidence['id'],'split_from':parent['id']},CLAUDE);self.assess(c,case)
        return case['id']
    def retry_triage(self,cid,actor):
        self.role(actor,{'case_manager'})
        with self.db.tx() as c:
            case=self.db.case(c,cid); t=case.get('triage') or {}
            if t.get('state')!='failed':raise Conflict('Only a failed reading can be retried')
            self.db.add(c,'triage_retry',{'source_id':t['source_id'],'actor':actor},cid)
            case['triage']={'state':'pending','source_id':t['source_id']}
            self.bump(c,case);self.event(c,case,'triage_retry',{'source_id':t['source_id']},actor);self.assess(c,case)
            return self.detail_tx(c,cid)

    # ---- Tenant thread: Claude drafts and decides; policy gates every send.
    def route_verified(self,c,case,at=None):
        checks=evaluate({**case,'proposal':{**case['proposal'],'action':'clarify'},'triage':{}},self.claims(c,case['id']),[],self.active(c),at=at)['checks']
        return all(x['status']=='PASS' for x in checks if x['key'] in {'identity','route'})
    def tenant_messages(self,c,cid):
        sent={r['message_id']:r for r in self.rows(c,'tenant_message_sent',cid)}
        rejected={r['message_id']:r for r in self.rows(c,'tenant_message_rejected',cid)}
        result=[]
        for m in self.rows(c,'tenant_message',cid):
            row={**m}
            if m['id'] in sent:row.update(status='sent',sent_at=sent[m['id']]['created_at'],sent_text=sent[m['id']]['text'],sent_by=sent[m['id']]['actor'],edited=sent[m['id']].get('edited',False))
            elif m['id'] in rejected:row.update(status='rejected',rejection=rejected[m['id']],redraft=rejected[m['id']].get('redraft',False))
            result.append(row)
        return result
    def tenant_questions_due(self,c,case,policy):
        """Open questions to the tenant or a directory party that no message covers yet."""
        s=policy['settings']; modes={'tenant':s['tenant_messages']}
        messages=[m for m in self.tenant_messages(c,case['id']) if not (m['status']=='rejected' and m.get('redraft'))]
        followups=self.rows(c,'question_followup',case['id']); due=[]
        for q in self.questions(c,case):
            if q['status']!='open' or q['escalated'] or not q['addressee'] or q['action_revision']!=case['action_revision']:continue
            if modes.get(q['addressee'],s['party_messages'])=='off':continue
            mine=[f for f in followups if f['question_id']==q['id']]
            covering=[m for m in messages if q['id'] in m['question_ids']]
            # A partial answer earns a narrower follow-up, within the policy limit.
            if mine and len(mine)<=s['tenant_follow_ups']:covering=[m for m in covering if m['created_at']>max(f['created_at'] for f in mine)]
            if not covering:due.append(q)
        return due
    def due_group(self,c,case,policy):
        """One message goes to one recipient: the first addressee with questions due."""
        due=self.tenant_questions_due(c,case,policy)
        if not due:return None,[]
        who=due[0]['addressee']
        return who,[q for q in due if q['addressee']==who][:policy['settings']['tenant_max_questions']]
    def message_gate(self,c,case,draft,questions,qids,mode,auto_topics,flags,label,route_text):
        """Deterministic send gate shared by tenant and party messages."""
        s=self.active(c)['settings'];route_ok=self.route_verified(c,case)
        current=[x for x in self.claims(c,case['id']) if x['key']=='urgent' and x['value'] is True and scope_matches(x['scope'],case)]
        reasons=[]
        if mode=='staff_approval':reasons.append(f'Policy requires staff approval for every {label}.')
        if draft['send_decision']!='auto_send':reasons.append('Claude asked for staff review: '+draft['decision_reason'])
        extra=sorted({x['topic'] for x in questions}-set(auto_topics))
        if extra:reasons.append('Policy does not allow automatic questions about: '+', '.join(extra)+'.')
        if {x['question_id'] for x in questions}!=set(qids):reasons.append('The draft does not cover every open question.')
        if flags:reasons.append('Risk flags: '+', '.join(flags)+'.')
        if not questions or not draft['message'].strip():reasons.append('No usable question was drafted.')
        if current:reasons.append('A possible urgent hazard is recorded; a person handles contact.')
        if not route_ok:reasons.append(route_text)
        return reasons,('sent' if not reasons else 'awaiting_staff' if route_ok else 'held')
    def compose_tenant_messages(self,cid):
        with self.db.tx() as c:
            case=self.db.case(c,cid); policy=self.active(c); s=policy['settings']
            who,due=self.due_group(c,case,policy)
            if not due:return {'drafted':0,'sent':0}
        if who!='tenant':return self.compose_party_message(cid,who)
        with self.db.tx() as c:
            case=self.db.case(c,cid); policy=self.active(c); s=policy['settings']
            who,due=self.due_group(c,case,policy)
            if who!='tenant' or not due:return {'drafted':0,'sent':0}
            route_ok=self.route_verified(c,case); t=case.get('triage') or {}
            history=self.tenant_messages(c,cid)
            context={'policy':{'mode':s['tenant_messages'],'auto_send_topics':s['tenant_auto_send_topics'],'max_questions':s['tenant_max_questions']},
                'tenant_identity_and_route_verified':route_ok,
                'case':{'category':case['category'],'work_item':case['proposal']['work_item'],'next_action':case['proposal']['action'],'triage_summary':t.get('summary'),'triage_risk_flags':t.get('risk_flags',[])},
                'open_questions':[{'question_id':q['id'],'topic':q['topic'],'why_needed':q['question'],
                    'partial_answers':[f['source_quote'] for f in self.rows(c,'question_followup',cid) if f['question_id']==q['id']],
                    'details':[a['description'] for a in t.get('open_ambiguities',[])] if q['key']=='triage' else []} for q in due],
                'messages_from_tenant':[{'label':e['source_label'],'text':e['text'][:4000]} for e in self.rows(c,'evidence',cid)
                    if ((e.get('party') or {}).get('kind')=='tenant') or (not e.get('party') and (e.get('triage')=='pending' or e['source_label'].startswith(('Intake','Tenant'))))][-4:],
                'messages_already_sent':[m.get('sent_text') for m in history if m['status']=='sent' and (m.get('recipient') or {}).get('kind','tenant')=='tenant'][-3:],
                'staff_feedback_on_rejected_drafts':[m['rejection']['reason'] for m in history if m['status']=='rejected']}
            key=digest({'questions':sorted(q['id'] for q in due),'follow_ups':len(self.rows(c,'question_followup',cid)),'rejected':len([m for m in history if m['status']=='rejected'])})
            tenant=parties.on_property('tenant',case['property_ref'])
            recipient={'kind':'tenant',**({'id':tenant['id'],'name':tenant['name']} if tenant else {})}
        try:draft,meta=ai.draft_tenant_message(context);error=None
        except ai.ClaudeUnavailable as exc:draft,error=None,exc;meta={'provider':'anthropic','requested_model':ai.model_id(),'prompt_version':ai.PROMPT_VERSION}
        with self.db.tx() as c:
            case=self.db.case(c,cid); policy=self.active(c); s=policy['settings']
            still={q['id'] for q in self.tenant_questions_due(c,case,policy)}
            qids=[q['id'] for q in due if q['id'] in still]
            if not qids:return {'drafted':0,'sent':0}
            base={'question_ids':qids,'topics':[q['topic'] for q in due if q['id'] in still],'recipient':recipient,'policy_version':policy['version'],'action_revision':case['action_revision'],**meta}
            if error:
                m,created=self.db.add(c,'tenant_message',{**base,'status':'draft_failed','error_type':error.error_type,'gate':{'auto_send':False,'reasons':['Claude could not draft this message ('+error.error_type+'). Write it or reject it for a redraft.']}},cid,dedupe='tenant_message:'+key)
                if created:self.bump(c,case);self.event(c,case,'tenant_message_drafted',{'message_id':m['id'],'status':'draft_failed'},CLAUDE)
                return {'drafted':0,'sent':0}
            questions=[x for x in draft['questions'] if x['question_id'] in qids][:s['tenant_max_questions']]
            t=case.get('triage') or {}
            flags=sorted(set(draft['risk_flags'])|set(t.get('risk_flags',[])))
            reasons,status=self.message_gate(c,case,draft,questions,qids,s['tenant_messages'],s['tenant_auto_send_topics'],flags,'tenant message','Tenant identity and contact route are not verified; nothing can be sent.')
            m,created=self.db.add(c,'tenant_message',{**base,'status':'awaiting_staff' if status=='sent' else status,'text':draft['message'],'questions':questions,
                'claude':{'send_decision':draft['send_decision'],'decision_reason':draft['decision_reason'],'risk_flags':draft['risk_flags']},
                'gate':{'auto_send':status=='sent','reasons':reasons}},cid,dedupe='tenant_message:'+key)
            if not created:return {'drafted':0,'sent':0}
            if status=='sent':self.send_tenant_message(c,case,payload(m),draft['message'],CLAUDE)
            self.bump(c,case);self.event(c,case,'tenant_message_drafted',{'message_id':m['id'],'status':status},CLAUDE);self.assess(c,case)
            return {'drafted':1,'sent':int(status=='sent')}
    def compose_party_message(self,cid,who):
        """Claude drafts one question to the landlord or contractor; the same gate decides sending."""
        with self.db.tx() as c:
            case=self.db.case(c,cid); policy=self.active(c); s=policy['settings']
            group,due=self.due_group(c,case,policy)
            if group!=who or not due:return {'drafted':0,'sent':0}
            person=parties.on_property(who,case['property_ref'])
            route_ok=self.route_verified(c,case); t=case.get('triage') or {}
            history=[m for m in self.tenant_messages(c,cid) if (m.get('recipient') or {}).get('kind')==who]
            totals=[x['value'] for x in self.claims(c,cid) if x['key']=='total' and not x.get('hearsay') and scope_matches(x['scope'],case)]
            context={'policy':{'mode':s['party_messages'],'auto_send_topics':s['party_auto_send_topics'],'max_questions':s['tenant_max_questions']},
                'recipient':{'kind':who,'name':person['name']},'recipient_route_verified':route_ok,
                'case':{'property':parties.PROPERTIES[case['property_ref']]['address'],'category':case['category'],'work_item':case['proposal']['work_item'],
                        'next_action':case['proposal']['action'],'quoted_total':max(totals) if totals else None,'triage_summary':t.get('summary')},
                'open_questions':[{'question_id':q['id'],'topic':q['topic'],'why_needed':q['question']} for q in due],
                'messages_already_sent':[m.get('sent_text') for m in history if m['status']=='sent'][-3:],
                'staff_feedback_on_rejected_drafts':[m['rejection']['reason'] for m in history if m['status']=='rejected']}
            key=digest({'recipient':who,'questions':sorted(q['id'] for q in due),'rejected':len([m for m in history if m['status']=='rejected'])})
            recipient={'kind':who,'id':person['id'],'name':person['name']}
        try:draft,meta=ai.draft_party_message(context);error=None
        except ai.ClaudeUnavailable as exc:draft,error=None,exc;meta={'provider':'anthropic','requested_model':ai.model_id(),'prompt_version':ai.PROMPT_VERSION}
        with self.db.tx() as c:
            case=self.db.case(c,cid); policy=self.active(c); s=policy['settings']
            still={q['id'] for q in self.tenant_questions_due(c,case,policy)}
            qids=[q['id'] for q in due if q['id'] in still]
            if not qids:return {'drafted':0,'sent':0}
            base={'question_ids':qids,'topics':[q['topic'] for q in due if q['id'] in still],'recipient':recipient,'policy_version':policy['version'],'action_revision':case['action_revision'],**meta}
            if error:
                m,created=self.db.add(c,'tenant_message',{**base,'status':'draft_failed','error_type':error.error_type,'gate':{'auto_send':False,'reasons':['Claude could not draft this message ('+error.error_type+'). Write it or reject it for a redraft.']}},cid,dedupe='party_message:'+key)
                if created:self.bump(c,case);self.event(c,case,'tenant_message_drafted',{'message_id':m['id'],'status':'draft_failed','recipient':who},CLAUDE)
                return {'drafted':0,'sent':0}
            questions=[x for x in draft['questions'] if x['question_id'] in qids][:s['tenant_max_questions']]
            reasons,status=self.message_gate(c,case,draft,questions,qids,s['party_messages'],s['party_auto_send_topics'],sorted(set(draft['risk_flags'])),
                f'message to a {PARTY_LABELS[who].lower()}',f'The {PARTY_LABELS[who].lower()}\'s contact route is not verified; nothing can be sent.')
            m,created=self.db.add(c,'tenant_message',{**base,'status':'awaiting_staff' if status=='sent' else status,'text':draft['message'],'questions':questions,
                'claude':{'send_decision':draft['send_decision'],'decision_reason':draft['decision_reason'],'risk_flags':draft['risk_flags']},
                'gate':{'auto_send':status=='sent','reasons':reasons}},cid,dedupe='party_message:'+key)
            if not created:return {'drafted':0,'sent':0}
            if status=='sent':self.send_tenant_message(c,case,payload(m),draft['message'],CLAUDE)
            self.bump(c,case);self.event(c,case,'tenant_message_drafted',{'message_id':m['id'],'status':status,'recipient':who},CLAUDE);self.assess(c,case)
            return {'drafted':1,'sent':int(status=='sent')}
    def send_tenant_message(self,c,case,message,text,actor,edited=False):
        # Simulated adapter: the stable message id is the idempotency key.
        to=(message.get('recipient') or {}).get('kind','tenant')
        self.db.add(c,'tenant_message_sent',{'message_id':message['id'],'text':text,'question_ids':message['question_ids'],'channel':'simulated_in_app_thread' if to=='tenant' else 'simulated_party_channel','recipient':message.get('recipient'),'simulated':True,
            'label':'SIMULATED — no real message was sent','actor':actor,'edited':edited},case['id'],dedupe='tenant_message_sent:'+message['id'])
    def message_row(self,c,mid):
        row=self.db.get_record(c,mid)
        if row['kind']!='tenant_message':raise ValueError('Tenant message not found')
        case=self.db.case(c,row['case_id'])
        return case,next(m for m in self.tenant_messages(c,case['id']) if m['id']==mid)
    def approve_message(self,mid,actor,text=None):
        self.role(actor,{'case_manager'})
        with self.db.tx() as c:
            case,m=self.message_row(c,mid)
            if m['status'] not in {'awaiting_staff','held','draft_failed'}:raise Conflict('This message was already sent or rejected')
            if m['action_revision']!=case['action_revision']:raise Conflict('The case moved to a different action; this draft is stale')
            if not {q['id'] for q in self.questions(c,case) if q['status']=='open'}&set(m['question_ids']):raise Conflict('Every question in this draft is already resolved')
            if not self.route_verified(c,case):raise Conflict('Verify the tenant identity and contact route before sending')
            body=(text or m.get('text') or '').strip()
            if not body:raise ValueError('Write the message text before sending')
            self.send_tenant_message(c,case,m,body,actor,edited=body!=(m.get('text') or '').strip())
            self.bump(c,case);self.event(c,case,'tenant_message_sent',{'message_id':mid},actor);self.assess(c,case)
            return self.detail_tx(c,case['id'])
    def reject_message(self,mid,actor,reason,redraft=False):
        self.role(actor,{'case_manager'})
        if not reason or len(reason.strip())<5:raise ValueError('Give a reason of at least five characters')
        with self.db.tx() as c:
            case,m=self.message_row(c,mid)
            if m['status'] not in {'awaiting_staff','held','draft_failed'}:raise Conflict('This message was already sent or rejected')
            self.db.add(c,'tenant_message_rejected',{'message_id':mid,'reason':reason.strip(),'redraft':bool(redraft),'actor':actor},case['id'],dedupe='tenant_message_rejected:'+mid)
            self.bump(c,case);self.event(c,case,'tenant_message_rejected',{'message_id':mid,'redraft':bool(redraft)},actor);self.assess(c,case)
            return self.detail_tx(c,case['id'])
    def claude_steps(self,cid):
        """Run triage and drafting inline: manual demo mode and BUILD replay only."""
        spawned=[]
        for _ in range(8):
            with self.db.tx() as c:
                case=self.db.case(c,cid);route=bool(self.awaiting_route(c,cid));triage=bool(self.pending_sources(c,cid));draft=bool(self.tenant_questions_due(c,case,self.active(c)))
            if route:self.route_messages(cid)
            elif triage:spawned+=self.triage_messages(cid)['spawned_case_ids']
            elif draft:self.compose_tenant_messages(cid)
            else:break
        return spawned
    def require_source(self,c,cid,sid):
        if not sid:raise ValueError('A case evidence source is required')
        r=self.db.get_record(c,sid)
        if r['kind']!='evidence' or r['case_id']!=cid:raise ValueError('Source must be evidence from this case')
        return r
    def execute(self,cid,actor,outcome='success'):
        self.role(actor,{'case_manager'})
        if outcome not in {'success','uncertain'}:raise ValueError('Unsupported simulated outcome')
        with self.db.tx() as c:
            return self.execute_tx(c,self.db.case(c,cid),actor,outcome)
    def execute_tx(self,c,case,actor,outcome='success'):
        cid=case['id'];bid=business_id(case);past=next((a for a in self.action_states(c,cid) if a['business_id']==bid),None)
        if past and past['status']=='succeeded':return {'duplicate':True,'action':past,'detail':self.detail_tx(c,cid)}
        if past and past['status']=='uncertain':raise Conflict('Outcome is uncertain. Reconcile it before retrying.')
        decision=self.assess(c,case)
        if decision['outcome']!='ACT':
            raise Conflict('Action remains blocked: '+', '.join(b['key'] for b in decision['blockers']))
        self.db.add(c,'action',{'business_id':bid,'status':'intent','scope':scope_of(case),'decision_id':decision['id'],'simulated':True,'actor':actor},cid)
        # The simulator receipt is the external system's ledger. Real adapters
        # must use provider idempotency and read-back before any retry.
        receipt,_=self.db.add(c,'simulated_provider_receipt',{'business_id':bid,'accepted':True,'scope':scope_of(case),'label':'SIMULATED — no external contact or charge'},cid,dedupe='provider:'+bid)
        action,_=self.db.add(c,'action',{'business_id':bid,'status':'uncertain' if outcome=='uncertain' else 'succeeded','scope':scope_of(case),'decision_id':decision['id'],'receipt_id':None if outcome=='uncertain' else receipt['id'],'simulated':True,'actor':actor},cid)
        if outcome=='success':
            if case['proposal']['action']=='close_item':case['status']='verified_resolution';case['completion_state']='verified for this work item'
            elif case['proposal']['action']=='archive':case['status']='administratively_archived'
            else:case['status']='in_progress'
            case['last_verified_action']=case['proposal']['action']
        self.bump(c,case);self.event(c,case,'simulated_action',{'business_id':bid,'status':action['payload']['status']},actor);self.assess(c,case)
        return {'duplicate':False,'action':payload(action),'detail':self.detail_tx(c,cid)}
    def reconcile(self,cid,actor):
        self.role(actor,{'case_manager'})
        with self.db.tx() as c:
            case=self.db.case(c,cid); uncertain=[a for a in self.action_states(c,cid) if a['status']=='uncertain']
            for a in uncertain:
                receipt=next((r for r in self.rows(c,'simulated_provider_receipt',cid) if r['business_id']==a['business_id']),None)
                if receipt:
                    self.db.add(c,'action',{**{k:v for k,v in a.items() if k not in {'id','created_at'}},'status':'succeeded','receipt_id':receipt['id'],'reconciled_by':actor},cid)
                    action=a['scope']['action']
                    case['last_verified_action']=action
                    case['status']='verified_resolution' if action=='close_item' else 'administratively_archived' if action=='archive' else 'in_progress'
                else:raise Conflict('No provider receipt exists; technical review is required, no automatic retry')
            self.bump(c,case);self.event(c,case,'simulated_result_reconciled',{},actor);self.assess(c,case);return self.detail_tx(c,cid)
    def policies(self):
        with self.db.tx() as c:return {'active':self.active(c),'drafts':[payload(r) for r in self.db.list(c,'policy_draft')]}
    def draft(self,data:PolicyInput,actor):
        self.role(actor,{'policy_editor'})
        with self.db.tx() as c:
            if data.base_version!=self.active(c)['version']:raise Conflict('Policy base has changed. Reload the active version.')
            r,_=self.db.add(c,'policy_draft',{**data.model_dump(),'version':data.base_version+1,'status':'draft','author':actor['id']});return payload(r)
    def preview_tx(self,c,draft):
        policy=self.active(c);affected=[]
        for case in self.db.case_list(c):
            completed=any(a['business_id']==business_id(case) and a['status']=='succeeded' for a in self.action_states(c,case['id']))
            if completed:
                affected.append({'case_id':case['id'],'title':case['title'],'revision':case['revision'],'before':'NO FURTHER ACTION','after':'NO FURTHER ACTION','blockers':[],'changed':False})
                continue
            before=evaluate({**case,'policy_pending':False},self.claims(c,case['id']),self.approvals(c,case['id']),policy)
            after=evaluate({**case,'policy_pending':False},self.claims(c,case['id']),self.approvals(c,case['id']),draft)
            affected.append({'case_id':case['id'],'title':case['title'],'revision':case['revision'],'before':before['outcome'],'after':after['outcome'],'blockers':[b['key'] for b in after['blockers']],'changed':digest(before['blockers'])!=digest(after['blockers'])})
        return {'affected':affected,'active_version':policy['version'],'draft_id':draft['id'],'snapshot_hash':digest({'active':policy['version'],'cases':[(x['id'],x['revision']) for x in self.db.case_list(c)]})}
    def preview(self,pid,actor):
        self.role(actor,{'policy_editor'})
        with self.db.tx() as c:
            row=self.db.get_record(c,pid)
            if row['kind']!='policy_draft':raise ValueError('Draft not found')
            result=self.preview_tx(c,payload(row));r,_=self.db.add(c,'policy_preview',{**result,'actor':actor});return {**result,'preview_id':r['id']}
    def publish(self,pid,actor):
        self.role(actor,{'policy_editor'})
        with self.db.tx() as c:
            row=self.db.get_record(c,pid)
            if row['kind']!='policy_draft':raise ValueError('Draft not found')
            draft=payload(row);current=self.active(c)
            if draft['base_version']!=current['version']:raise Conflict('Draft base is stale')
            previews=[r for r in self.db.list(c,'policy_preview') if r['payload']['draft_id']==pid and r['payload']['actor']['id']==actor['id']]
            if not previews or previews[-1]['payload']['snapshot_hash']!=self.preview_tx(c,draft)['snapshot_hash']:raise Conflict('Run a current impact preview before publication')
            p,_=self.db.add(c,'policy',{'version':current['version']+1,'status':'published','settings':draft['settings'],'rules':draft['rules'],'author':actor['id'],'reason':draft['reason'],'effective_at':stamp(),'draft_id':pid,'preview_id':previews[-1]['id']})
            self.db.set_meta(c,'active_policy',p['id'])
            for case in self.db.case_list(c):
                if any(a['business_id']==business_id(case) and a['status']=='succeeded' for a in self.action_states(c,case['id'])):
                    self.assess(c,case)
                    continue
                case['policy_pending']=True;self.bump(c,case);self.event(c,case,'policy_published',{'version':p['payload']['version']},actor);self.assess(c,case)
            return payload(p)
    def tick(self,cid,at=None):
        at=at or now()
        with self.db.tx() as c:
            case=self.db.case(c,cid);self.assess(c,case,at=at);policy=self.active(c);s=policy['settings'];changed=False
            checks=evaluate(case,self.claims(c,cid),self.approvals(c,cid),policy,at=at)
            blocker_keys={b['key'] for b in checks['blockers']}
            for q in self.questions(c,case):
                if q['status']!='open' or q['key'] not in blocker_keys or q['action_revision']!=case['action_revision']:continue
                # Deadlines are recomputed under current settings, from delivery
                # when the question was sent. An unsent draft still escalates.
                deadline=dt(q['deadline']);reminder=dt(q['reminder_at']) if q['reminder_at'] else None
                if at>=deadline and not q['escalated']:
                    self.db.add(c,'question_escalated',{'question_id':q['id'],'owner':q['owner'],'reason':'No relevant answer by deadline; permission remains blocked.'},cid,dedupe='escalate:'+q['id']);changed=True
                elif reminder and at>=reminder and q['reminders']<s['reminder_limit'] and not q['escalated']:
                    # Recheck permission for a reminder itself before simulated sending.
                    if self.route_verified(c,case,at):self.db.add(c,'reminder',{'question_id':q['id'],'number':q['reminders']+1,'simulated':True,'text':'Reminder: '+(q.get('tenant_text') or q['question'])},cid,dedupe=f"reminder:{q['id']}:{q['reminders']+1}");changed=True
            for r in self.reviews(c,case):
                deferred=r.get('response') if r['status']=='deferred' else None
                deadline=dt(deferred['deadline']) if deferred else dt(r['expires_at'])
                if r['status'] in {'open','deferred','expired'} and at>=deadline:
                    self.db.add(c,'review_overdue',{'review_id':r['id'],'owner':s['deputy'],'reason':'Review overdue; affected action remains held.'},cid,dedupe='review_overdue:'+r['id'])
            if changed:self.bump(c,case)
            final=self.assess(c,case,at=at)
            if final['outcome']=='ACT' and not at>now()+timedelta(seconds=5):
                self.execute_tx(c,case,{'id':'native-case-coordinator','role':'case_manager'})
            events=self.rows(c,'incoming_event',cid)
            self.db.add(c,'cycle_checkpoint',{'revision':case['revision'],'consumed_event_ids':[e['id'] for e in events],'assessed_at':stamp(at)},cid)
            times=[]
            for q in self.questions(c,case):
                if q['status']=='open' and not q['escalated']:
                    if q['reminder_at'] and q['reminders']<s['reminder_limit']: times.append(dt(q['reminder_at']))
                    times.append(dt(q['deadline']))
            for r in self.reviews(c,case):
                if r['status'] in {'open','deferred'}:times.append(dt(r['response']['deadline']) if r['status']=='deferred' else dt(r['expires_at']))
            # A bounded recovery heartbeat catches a committed event after a lost wake.
            times.append(at+timedelta(minutes=5))
            case=self.db.case(c,cid)
            return {'terminal':case['status']=='administratively_archived','next_wake_at':stamp(min(t for t in times if t>at)),'revision':case['revision'],
                    'needs_routing':bool(self.awaiting_route(c,cid)),'needs_triage':bool(self.awaiting_reading(c,cid)),'needs_tenant_message':bool(self.tenant_questions_due(c,case,policy))}

    # ---- Inbound calls: who is calling, about which case, and what they may hear.
    def cases_for(self,c,ref,open_only=True):
        rows=[x for x in self.db.case_list(c) if x['property_ref']==ref and (not open_only or x['status'] not in {'verified_resolution','administratively_archived'})]
        return sorted(rows,key=lambda x:x['created_at'],reverse=True)
    def inbound(self,data:InboundCall,actor):
        """One caller turn from the voice bridge. Fast and deterministic: no model call.

        The caller is matched by number in the fictional directory, the property
        from their directory entry (or the words they used), and the case is the
        property's latest open job. A report becomes case evidence tagged with the
        sender; the case coordinator then routes and reads it as usual. A status
        enquiry is answered from a summary filtered for that kind of caller.
        """
        self.role(actor,{'case_manager'})
        person=parties.by_phone(data.caller_number);party=parties.stamp_for(person)
        ref=parties.resolve_property(person,data.transcript)
        input_hash=digest(data.model_dump());key='inbound:'+data.call_id
        with self.db.tx() as c:
            seen=self.db.get_meta(c,key)
            if seen:
                if seen['input_hash']!=input_hash:raise Conflict('This call id already belongs to a different call turn')
                return self.inbound_reply(c,seen)
            label=f"{ {'voice':'Voice call','sms':'Text message','email':'Email'}[data.channel]} from {PARTY_LABELS[party['kind']].lower()}"+(f" {party['name']}" if party['name'] else '')+(' (caller ID in the fictional directory)' if person else ' (number not in the directory)')
            open_cases=self.cases_for(c,ref) if ref else []
            case=open_cases[0] if open_cases else None
            if person and not ref:
                # A landlord, agency or contractor with several properties did
                # not say which one: ask rather than guess.
                outcome='needs_property'
            elif data.intent=='status_enquiry':
                case=case or (self.cases_for(c,ref,open_only=False) or [None])[0] if ref else None
                outcome='status'
            elif case:
                self.evidence_tx(c,case,EvidenceInput(text=data.transcript,source_label=label,occurred_at=data.occurred_at,idempotency_key=key),actor,party)
                outcome='attached'
            else:
                where=ref or 'Unresolved caller'
                case,evidence=self.new_case(c,title=f"{PARTY_LABELS[party['kind']]} call: {' '.join(data.transcript.split())[:120]}",property_ref=where,report=data.transcript,category=None,action=None,
                    work_item='Reported maintenance',provider='Demo contractor',access_method='tenant_present',actor=actor,triage_state='pending',category_source='claude',route_source='claude',source_label=label,party=party)
                self.event(c,case,'intake',{'evidence_id':evidence['id'],'inbound':data.call_id},actor);self.assess(c,case)
                outcome='new_case'
            record={'call_id':data.call_id,'input_hash':input_hash,'channel':data.channel,'intent':data.intent,'party':party,'property_ref':ref,'case_id':case['id'] if case else None,'outcome':outcome,'received_at':stamp()}
            # The caller's number is not stored; the party marker says how they matched.
            self.db.add(c,'inbound_call',{k:v for k,v in record.items() if k!='input_hash'},record['case_id'],dedupe=key)
            self.db.set_meta(c,key,record)
            return self.inbound_reply(c,record)
    def inbound_reply(self,c,record):
        party=record['party'];case=self.db.case(c,record['case_id']) if record['case_id'] else None
        ref=record['property_ref'];address=parties.PROPERTIES[ref]['address'] if ref else None
        first=(party['name'] or '').split(' ')[0]
        # Greet people by first name; agencies and contractors are businesses.
        thanks='Thanks'+(f' {first}' if first and party['kind'] in {'tenant','landlord'} else '')+'. '
        if record['outcome']=='needs_property':say=thanks+'Which property is this about? Please tell me the address.'
        elif record['outcome']=='status':say=self.status_text(c,case,party)
        elif not ref:say=thanks+"I've passed your message to the team. Someone will check who you are and which property this is before anything happens."
        elif record['outcome']=='attached':say=thanks+f"I've added that to the {case['proposal']['work_item'].lower()} job at {address}. The team will follow up."
        else:say=thanks+f"I've logged this for {address}. We'll be in touch about next steps."
        return {'call_id':record['call_id'],'outcome':record['outcome'],'case_id':record['case_id'],
                'party':{k:party[k] for k in ('kind','name','verified','match')},
                'property':{'ref':ref,'address':address} if ref else None,'say':say,
                'simulated':True,'notice':'Fictional directory and simulated operations; no real contact is made.'}
    NEXT_STEP={'clarify':'gathering details','request_quote':'getting a quote','confirm_appointment':'confirming the appointment','supply_keys':'arranging keys',
               'instruct_work':'instructing the work','close_item':'closing the job','archive':'closing the request'}
    def status_text(self,c,case,party):
        """A short spoken summary filtered for the kind of caller. No other person's details."""
        kind=party['kind']
        if kind=='other':return "I can't share details on this line. I've passed your message to the team, who will check who you are first."
        if not case:return "I can't find a job for that property yet. If something needs fixing, tell me what it is and I'll log it."
        d=self.detail_tx(c,case['id']);ref=case['property_ref']
        where=parties.PROPERTIES[ref]['address'] if ref in parties.PROPERTIES else 'the property'
        work=case['proposal']['work_item'].lower();step=self.NEXT_STEP.get(case['proposal']['action'],'the next step')
        out=[f"For the {work} job at {where}:"]
        if case['status']=='verified_resolution':out.append('it is marked as resolved.')
        elif case['status']=='administratively_archived':out.append('it is closed.')
        else:
            if case.get('last_verified_action'):out.append(f"the last completed step was {self.NEXT_STEP.get(case['last_verified_action'],'an update')} (simulated).")
            blockers=arr_(d['decision'] and d['decision']['blockers'])
            top=blockers[0] if blockers else None
            if top is None:out.append(f"{step} is going ahead now (simulated).")
            elif top['key']=='triage' and top['response']=='WAIT':out.append("we're reading the latest message.")
            elif top['response']=='STOP ACTION':out.append(f"{step} is on hold.")
            elif top['response']=='HUMAN REVIEW':out.append(f"it's with our team for a decision before {step}.")
            else:out.append(f"we're waiting for some details before {step}.")
        mine=sorted({q['topic'] for q in d['questions'] if q['status']=='open' and q.get('sent_at') and q['addressee'] and self.may_answer(q,party)})
        if mine:out.append("We're waiting for your answer about: "+', '.join(t.replace('_',' ') for t in mine)+'.')
        current=[x for x in d['claims'] if scope_matches(x['scope'],case) and not x.get('hearsay') and not x.get('superseded_by')]
        if kind in {'landlord','agency'}:
            totals=[x for x in current if x['key']=='total']
            if totals:
                t=max(totals,key=lambda x:x['created_at']);out.append(f"The quote is £{t['value']:,.2f}"+('.' if t.get('verified') else ', not yet checked by our team.'))
            if any(x['key']=='authority' and x['value'] is True and not x.get('verified') for x in current):out.append('Your approval has been received and is being checked.')
        if kind in {'tenant','contractor'}:
            schedule=next((x for x in arr_(d['decision'] and d['decision']['checks']) if x['key']=='schedule'),None)
            if schedule:out.append('The appointment is confirmed.' if schedule['status']=='PASS' else 'No appointment is confirmed yet.')
        return ' '.join(out)

_service=None
def get_service():
    global _service
    if _service is None:
        _service=Service()
        from . import audit
        folder=audit.auto_directory()
        if folder:_service.db.on_commit=audit.exporter(_service,folder)
    return _service

def coordinator_cycle(case_id:str)->dict:
    service=get_service()
    cycle=service.tick(case_id)
    detail=service.detail(case_id)
    if detail['decision']['outcome']=='ACT':
        # Every external adapter remains simulated. Execute rechecks permission
        # after any concurrent message, revocation or policy publication.
        try:service.execute(case_id,{'id':'native-case-coordinator','role':'case_manager'})
        except Conflict:pass
        cycle=service.tick(case_id)
    return cycle

def triage_messages(case_id:str)->dict:
    """Workflow step body: Claude reads every stored, unread message for the case."""
    return get_service().triage_messages(case_id)

def route_messages(case_id:str)->dict:
    """Workflow step body: Jev routes every stored, unread message for the case."""
    return get_service().route_messages(case_id)

def compose_tenant_messages(case_id:str)->dict:
    """Workflow step body: Claude drafts tenant questions; policy decides sending."""
    return get_service().compose_tenant_messages(case_id)
