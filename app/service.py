"""Application service: transactions, evidence, policy, reviews and simulated tools."""
from __future__ import annotations
import uuid, json, os, re
from copy import deepcopy
from datetime import timedelta
from .store import Store, payload
from .domain import *
from .ai import interpret

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
    def intake(self,data:Intake,actor):
        self.role(actor,{'case_manager'})
        if data.action not in REQUIRED: raise ValueError('Unsupported action')
        input_hash=digest(data.model_dump(exclude={'idempotency_key'}))
        try: interpretation=interpret(data.report)
        except Exception as exc:
            # Do not silently portray a model failure as successful extraction.
            interpretation={'mode':'unavailable','summary':'Interpretation failed; manual review required.','error_type':type(exc).__name__,'category':'other','claims':[],'source_quote':''}
        with self.db.tx() as c:
            if data.idempotency_key:
                existing=next((r for r in self.db.list(c,'intake_receipt') if r['payload']['idempotency_key']==data.idempotency_key),None)
                if existing:
                    if existing['payload']['input_hash']!=input_hash:raise Conflict('Intake idempotency key belongs to a different request')
                    return self.detail_tx(c,existing['case_id'])
            case={'id':uuid.uuid4().hex,'title':data.title,'property_ref':data.property_ref,'category':data.category,'profile':'demo','revision':1,'action_revision':1,'proposal':{'action':data.action,'work_item':data.work_item,'provider':data.provider,'access_method':data.access_method,'scope':{}},'status':'open','owner':'case_manager','next_step':'Assess intake','policy_pending':False,'created_at':stamp(),'interpretation':interpretation}
            if case['category']=='other' and interpretation['category']!='other': case['category']=interpretation['category']
            self.db.save_case(c,case,True)
            if data.idempotency_key:self.db.add(c,'intake_receipt',{'idempotency_key':data.idempotency_key,'input_hash':input_hash},case['id'],dedupe='intake:'+data.idempotency_key)
            evidence,_=self.db.add(c,'evidence',{'text':data.report,'source_label':'Intake report','actor':actor,'occurred_at':stamp()},case['id'])
            self.db.add(c,'interpretation',{'source_id':evidence['id'],**interpretation},case['id'])
            for claim in interpretation.get('claims',[]):
                self.db.add(c,'claim',{**claim,'scope':claim.get('scope') or scope_of(case),'scope_origin':'model-source' if claim.get('scope') else 'case-envelope','source_id':evidence['id'],'verified':False,'supersedes':[]},case['id'])
            # The literal detector may support only a derived category, never permissions.
            if interpretation['mode']=='literal_demo' and interpretation['category']==case['category'] and case['category']!='other':
                self.db.add(c,'claim',{'key':'classification','value':True,'scope':{'property_ref':case['property_ref'],'work_item':data.work_item,'category':case['category']},'source_id':evidence['id'],'source_quote':interpretation['source_quote'],'verified':True,'verification':'demonstration literal category detector; derived label only','supersedes':[]},case['id'])
            hazard=re.search(r'\b(gas smell|smell of gas|sparks|electrical fire|ceiling collapse|major flooding)\b',data.report,re.I)
            if hazard:
                self.db.add(c,'claim',{'key':'urgent','value':True,'scope':{'property_ref':case['property_ref'],'work_item':data.work_item},'source_id':evidence['id'],'source_quote':hazard.group(),'verified':False,'verification':'Possible hazard phrase; not an emergency diagnosis','supersedes':[]},case['id'])
            if data.property_ref=='DEMO-FLAT-1':
                directory,_=self.db.add(c,'evidence',{'text':'Fictional demo directory: DEMO-FLAT-1, tenant demo-resident, verified in-app demonstration route. No real address or recipient.','source_label':'Preconfigured fictional demo directory','actor':{'id':'demo-setup','role':'case_manager'},'occurred_at':stamp()},case['id'])
                for key in ['identity','route']:
                    self.db.add(c,'claim',{'key':key,'value':True,'scope':{'property_ref':'DEMO-FLAT-1'},'source_id':directory['id'],'source_quote':'Fictional demo directory: DEMO-FLAT-1, tenant demo-resident, verified in-app demonstration route. No real address or recipient.','verified':True,'verification':'Preconfigured demonstration directory','supersedes':[]},case['id'])
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
        closed={r['question_id'] for r in self.rows(c,'question_closed',case['id'])}
        reminders=self.rows(c,'reminder',case['id']); escalations=self.rows(c,'question_escalated',case['id'])
        return [{**q,'status':'closed' if q['id'] in closed else 'open','reminders':sum(r['question_id']==q['id'] for r in reminders),'escalated':any(r['question_id']==q['id'] for r in escalations)} for q in self.rows(c,'question',case['id'])]
    def detail_tx(self,c,cid):
        case=self.db.case(c,cid); decisions=self.rows(c,'decision',cid)
        claims=self.claims(c,cid)
        replacements={old:new['id'] for new in claims if new.get('verified') for old in new.get('supersedes',[])}
        return {'case':case,'claims':[{**claim,**({'superseded_by':replacements[claim['id']]} if claim['id'] in replacements else {})} for claim in claims],'evidence':self.rows(c,'evidence',cid),'decision':decisions[-1] if decisions else None,'reviews':self.reviews(c,case),'questions':self.questions(c,case),'actions':self.action_states(c,cid),'timeline':self.db.list(c,case_id=cid)}
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
        blockers={b['key']:b for b in result['blockers']}
        questions=self.questions(c,case)
        for q in questions:
            if q['status']!='open':continue
            if q['key'] not in blockers or q['action_revision']!=case['action_revision']:
                self.db.add(c,'question_closed',{'question_id':q['id'],'reason':'Evidence satisfied the requirement or the action was superseded; old reminders cancelled.'},case['id'],dedupe='question_closed:'+q['id'])
        for b in result['blockers']:
            if b['response']=='CLARIFY' and b['claim_ids']:
                b['response']='HUMAN REVIEW'
                b['reason']='Verify the received source assertion. '+b['reason']
            if b['response']=='CLARIFY':
                # Every initial request and reminder is a visibly simulated communication.
                q=next((q for q in questions if q['status']=='open' and q['key']==b['key'] and q['action_revision']==case['action_revision']),None)
                if not q:
                    row,_=self.db.add(c,'question',{'key':b['key'],'question':b['reason'],'scope':scope_of(case),'action_revision':case['action_revision'],'policy_version':policy['version'],'opened_at':stamp(at),'reminder_at':stamp(working_after(at,policy['settings']['reminder_hours'],policy['settings']['holiday_dates'])),'deadline':stamp(working_after(at,policy['settings']['escalation_hours'],policy['settings']['holiday_dates'])),'simulated':True,'owner':b['owner']},case['id'])
                    q=payload(row)
                    self.db.add(c,'simulated_clarification',{'question_id':q['id'],'text':b['reason'],'simulated':True},case['id'])
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
    def evidence(self,cid,data:EvidenceInput,actor):
        self.role(actor,ROLES)
        try: interpretation=interpret(data.text)
        except Exception as exc:interpretation={'mode':'unavailable','summary':'Interpretation failed; manual review required.','error_type':type(exc).__name__,'claims':[],'source_quote':''}
        with self.db.tx() as c:
            case=self.db.case(c,cid)
            if data.supersedes: raise ValueError('Sources are superseded only by a reasoned, role-checked review correction')
            input_hash=digest(data.model_dump(exclude={'idempotency_key'}))
            source,created=self.db.add(c,'evidence',{'text':data.text,'source_label':data.source_label,'actor':actor,'occurred_at':data.occurred_at or stamp(),'input_hash':input_hash},cid,dedupe=('evidence:'+cid+':'+data.idempotency_key) if data.idempotency_key else None)
            if not created:
                if source['payload'].get('input_hash')!=input_hash: raise Conflict('Idempotency key already belongs to different evidence')
                return self.detail_tx(c,cid)
            self.db.add(c,'interpretation',{'source_id':source['id'],**interpretation},cid)
            case['interpretation']={**interpretation,'source_id':source['id']}
            supplied={(cl.key,json.dumps(cl.value),cl.source_quote) for cl in data.claims}
            for candidate in interpretation.get('claims',[]):
                if (candidate['key'],json.dumps(candidate['value']),candidate['source_quote']) in supplied:continue
                scope=candidate.get('scope') or scope_of(case)
                self.db.add(c,'claim',{**candidate,'scope':scope,'scope_origin':'model-source' if candidate.get('scope') else 'case-envelope','scope_valid':scope_matches(scope,case),'source_id':source['id'],'verified':False,'supersedes':[]},cid)
            for claim in data.claims:
                if claim.key=='completion' and claim.value is True:case['completion_state']='reported; awaiting verification'
                scope=claim.scope or scope_of(case)
                if not scope_matches(scope,case): raise ValueError('Claim scope must match the current property and action; create a separate item for other work')
                self.db.add(c,'claim',{**claim.model_dump(),'scope':scope,'source_id':source['id'],'verified':False,'supersedes':[]},cid)
            self.bump(c,case); self.event(c,case,'evidence_received',{'source_id':source['id']},actor); self.assess(c,case)
            return self.detail_tx(c,cid)
    def proposal(self,cid,data:ProposalInput,actor):
        self.role(actor,{'case_manager'})
        with self.db.tx() as c:
            case=self.db.case(c,cid)
            if any(a['status']=='uncertain' for a in self.action_states(c,cid)): raise Conflict('Reconcile the uncertain action before replacing its scope')
            proposal=data.model_dump();category=proposal.pop('category',None)
            if proposal==case['proposal'] and (category is None or category==case['category']):return self.detail_tx(c,cid)
            if category is not None:case['category']=category
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
            if data.decision=='approve':
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
                # Deadline recomputed from the original question under current settings.
                deadline=working_after(dt(q['opened_at']),s['escalation_hours'],s['holiday_dates'])
                reminder=working_after(dt(q['opened_at']),s['reminder_hours']*(q['reminders']+1),s['holiday_dates'])
                if at>=deadline and not q['escalated']:
                    self.db.add(c,'question_escalated',{'question_id':q['id'],'owner':q['owner'],'reason':'No relevant answer by deadline; permission remains blocked.'},cid,dedupe='escalate:'+q['id']);changed=True
                elif at>=reminder and q['reminders']<s['reminder_limit'] and not q['escalated']:
                    # Recheck permission for a reminder itself before simulated sending.
                    reminder_case={**case,'proposal':{**case['proposal'],'action':'clarify'}}
                    route=evaluate(reminder_case,self.claims(c,cid),[],policy,at=at)
                    if route['outcome']=='ACT':self.db.add(c,'reminder',{'question_id':q['id'],'number':q['reminders']+1,'simulated':True,'text':q['question']},cid,dedupe=f"reminder:{q['id']}:{q['reminders']+1}");changed=True
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
                    if q['reminders']<s['reminder_limit']: times.append(working_after(dt(q['opened_at']),s['reminder_hours']*(q['reminders']+1),s['holiday_dates']))
                    times.append(working_after(dt(q['opened_at']),s['escalation_hours'],s['holiday_dates']))
            for r in self.reviews(c,case):
                if r['status'] in {'open','deferred'}:times.append(dt(r['response']['deadline']) if r['status']=='deferred' else dt(r['expires_at']))
            # A bounded recovery heartbeat catches a committed event after a lost wake.
            times.append(at+timedelta(minutes=5))
            return {'terminal':case['status']=='administratively_archived','next_wake_at':stamp(min(t for t in times if t>at)),'revision':case['revision']}

_service=None
def get_service():
    global _service
    if _service is None:_service=Service()
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
