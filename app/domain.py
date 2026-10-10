"""Pure, fail-closed action policy. All defaults are demonstration choices."""
from __future__ import annotations
from datetime import datetime, timedelta, timezone
from zoneinfo import ZoneInfo
from copy import deepcopy
import hashlib, json, math
from pydantic import BaseModel, Field, ConfigDict, model_validator
from typing import Literal, Any

UTC = timezone.utc
ROLES = {'case_manager','policy_editor','access_officer','approver','reviewer'}
FACT_ROLES = {'identity':{'case_manager'}, 'route':{'case_manager'}, 'access':{'access_officer'}, 'keys':{'access_officer'}, 'authority':{'approver'}, 'total':{'approver','case_manager'}, 'schedule':{'case_manager'}, 'evidence':{'reviewer','case_manager'}, 'classification':{'case_manager'}, 'completion':{'reviewer'}, 'commitments':{'case_manager'}, 'urgent':{'case_manager'}, 'supported':{'case_manager'}}
FACTS = set(FACT_ROLES)
CATEGORIES = {'appliance','plumbing','garden','doors_locks','windows','inspection','checkout_cleaning','checkout_refurbishment','other'}
REQUIRED = {
 'clarify':['identity','route'],
 'request_quote':['identity','route','classification'],
 'confirm_appointment':['identity','route','access','authority','schedule'],
 'supply_keys':['identity','route','access','keys','authority','schedule'],
 'instruct_work':['identity','route','access','authority','schedule','evidence','classification','total'],
 'close_item':['identity','completion','commitments'],
 'archive':['identity','authority'],
}
MESSAGES = {
 'identity':'Verify the person, property and work item mapping.',
 'route':'Verify the recipient and permitted communication route.',
 'access':'Record consent for this visit and access method from the authorised person.',
 'keys':'Establish key custody and return arrangements.',
 'authority':'Obtain authority for this work item, provider and action.',
 'schedule':'Confirm the active appointment with a precise date and time.',
 'evidence':'Supply usable evidence required for this work item.',
 'classification':'Confirm that the category and work item match the source request.',
 'completion':'Verify completion of this work item with usable evidence.',
 'commitments':'Resolve or explicitly cancel every outstanding commitment for this item.',
 'total':'Establish the full comparable commitment, including tax.',
 'supported':'A case manager must define a supported action for this situation.',
 'urgent':'A possible urgent hazard needs a case manager and an approved procedure.',
 'finance':'Obtain a scoped financial review above the demonstration review limit.',
 'policy':'Explicitly reassess this case under the newly published policy.',
 'automation':'Reconcile the uncertain external result before another attempt.',
 'profile':'Resolve the unsupported or conflicting policy profile.',
 'triage':'Claude must read the latest message, or a case manager must triage it, before this action proceeds.'
}
# Claude chooses one of these workflow routes. Each maps to exactly one policy
# action; the model cannot invent a route, an action or a permission.
ROUTES = {
 'request_quote':{'action':'request_quote','description':'A repair or maintenance problem that needs a contractor quote or assessment before any work is authorised. The usual entry point for a newly reported defect.'},
 'confirm_appointment':{'action':'confirm_appointment','description':'The message is mainly about arranging, confirming, moving or cancelling a visit for an already known job.'},
 'supply_keys':{'action':'supply_keys','description':'The message is mainly about key collection, key return or contractor entry using management keys.'},
 'instruct_work':{'action':'instruct_work','description':'An already quoted or assessed job where the next step is instructing the contractor to carry out the work.'},
 'close_item':{'action':'close_item','description':'A report that work is finished, or asking for an item to be closed.'},
 'clarify':{'action':'clarify','description':'The request cannot be routed yet because essential information is missing or ambiguous.'},
 'urgent_hazard':{'action':'clarify','urgent':True,'description':'A possible safety hazard needing immediate human attention: gas smell, electrical danger, fire, major flooding, structural collapse, no heating or water for a vulnerable person.'},
 'archive':{'action':'archive','description':'No maintenance action is needed: thanks, duplicates, spam or a message clearly not about this property.'},
 'unsupported':{'action':'clarify','category':'other','description':'A genuine request outside every supported category and process. A case manager must define the handling.'},
}
# Topics Claude may ask the tenant about, and the policy facts they help resolve.
TENANT_TOPICS = ['issue_details','location','photo','availability','access','keys','completion']
TENANT_TOPIC_FOR = {'access':'access','keys':'keys','schedule':'availability','completion':'completion','evidence':'photo','classification':'issue_details','triage':'issue_details'}
CONFIDENCE_RANK = {'low':0,'medium':1,'high':2}
DEFAULT_SETTINGS = {'access_immediate_review':False,'reminder_hours':8,'escalation_hours':16,'reminder_limit':1,'review_limit':100.0,'approval_hours':48,'profile':'demo','deputy':'case_manager','required_per_action':{},'holiday_dates':[],
 'triage_auto_accept':'high','tenant_messages':'claude_decides','tenant_auto_send_topics':['issue_details','location','photo','availability','access','keys','completion'],'tenant_max_questions':3,'tenant_follow_ups':1}

class StrictModel(BaseModel):
    model_config = ConfigDict(extra='forbid')

class ClaimInput(StrictModel):
    key: str
    value: bool | float
    scope: dict = Field(default_factory=dict)
    source_quote: str = Field(min_length=1,max_length=10000)
    @model_validator(mode='after')
    def valid(self):
        if self.key not in FACTS: raise ValueError('Unsupported fact key')
        if self.key == 'total':
            if isinstance(self.value,bool) or not math.isfinite(self.value) or self.value < 0: raise ValueError('Total must be a non-negative number, not a boolean')
        elif not isinstance(self.value,bool): raise ValueError('This fact requires true or false')
        return self

class Intake(StrictModel):
    idempotency_key: str | None = Field(default=None,max_length=200)
    title: str = Field(min_length=3,max_length=160)
    property_ref: str = Field(min_length=2,max_length=200)
    report: str = Field(min_length=3,max_length=30000)
    # Unset category/action means Claude routes the message. 'other' is the
    # dashboard's "detect from report" choice and is treated as unset.
    category: str | None = None
    work_item: str = Field(default='Reported maintenance',min_length=1,max_length=200)
    action: str | None = None
    provider: str = 'Demo contractor'
    access_method: str = 'tenant_present'
    # 'staff' is manual triage: the case manager supplies category and action
    # and no model reads the report.
    triage: Literal['claude','staff'] = 'claude'
    @model_validator(mode='after')
    def valid(self):
        if self.category=='other' and self.triage=='claude': self.category=None
        if self.action=='': self.action=None
        if self.category=='': self.category=None
        if self.action is not None and self.action not in REQUIRED: raise ValueError('Unsupported action')
        if self.category is not None and self.category not in CATEGORIES: raise ValueError('Unsupported category')
        if self.triage=='staff' and (self.action is None or self.category is None): raise ValueError('Manual triage needs a category and an action')
        return self

class EvidenceInput(StrictModel):
    text: str = Field(min_length=1,max_length=50000)
    source_label: str = Field(min_length=1,max_length=200)
    claims: list[ClaimInput] = Field(default_factory=list,max_length=30)
    supersedes: list[str] = Field(default_factory=list)
    occurred_at: str | None = None
    idempotency_key: str | None = Field(default=None,max_length=200)
    @model_validator(mode='after')
    def quote_present(self):
        if self.occurred_at is not None: dt(self.occurred_at)
        for c in self.claims:
            if c.source_quote not in self.text: raise ValueError('Every source quote must occur exactly in the submitted evidence')
        return self

class ProposalInput(StrictModel):
    action: str
    category: str | None = None
    work_item: str = Field(min_length=1,max_length=200)
    provider: str = Field(default='Demo contractor',max_length=200)
    access_method: str = Field(default='tenant_present',max_length=100)
    scope: dict = Field(default_factory=dict)
    @model_validator(mode='after')
    def valid(self):
        if self.action not in REQUIRED: raise ValueError('Unsupported action')
        if self.category is not None and self.category not in CATEGORIES:raise ValueError('Unsupported category')
        if set(self.scope)&{'property_ref','work_item','provider','access_method','action','category'}: raise ValueError('Scope cannot override canonical action fields')
        return self

class Rule(StrictModel):
    id: str = Field(min_length=1,max_length=80)
    conditions: list[dict] = Field(min_length=1,max_length=10)
    match: Literal['all','any'] = 'all'
    actions: list[str] = Field(default_factory=list)
    response: Literal['CLARIFY','WAIT','HUMAN REVIEW','STOP ACTION'] = 'HUMAN REVIEW'
    owner: str = 'case_manager'
    required: bool = True
    property_ref: str | None = None
    category: str | None = None
    @model_validator(mode='after')
    def valid(self):
        if self.owner not in ROLES: raise ValueError('Unsupported owner')
        if set(self.actions)-set(REQUIRED): raise ValueError('Unsupported action')
        for c in self.conditions:
            if set(c)!={'key','status'} or c['key'] not in FACTS or c['status'] not in {'PASS','FAIL','UNKNOWN','CONFLICT'}: raise ValueError('Unsupported condition')
        return self

class PolicyInput(StrictModel):
    base_version: int
    settings: dict
    rules: list[Rule] = Field(default_factory=list,max_length=50)
    reason: str = Field(default='Demo policy adjustment',min_length=3,max_length=1000)
    @model_validator(mode='after')
    def validate_settings(self):
        unknown=set(self.settings)-set(DEFAULT_SETTINGS)
        if unknown: raise ValueError(f'Unsupported settings: {sorted(unknown)}')
        s=deepcopy(DEFAULT_SETTINGS); s.update(self.settings)
        if not isinstance(s['access_immediate_review'],bool): raise ValueError('Immediate review must be boolean')
        for k in ['reminder_hours','escalation_hours','approval_hours']:
            if isinstance(s[k],bool) or not isinstance(s[k],(int,float)) or not 0.1<=s[k]<=720: raise ValueError(f'Invalid {k}')
        if s['escalation_hours']<=s['reminder_hours']: raise ValueError('Escalation must follow reminder')
        if not isinstance(s['reminder_limit'],int) or not 0<=s['reminder_limit']<=5: raise ValueError('Reminder limit must be 0 to 5')
        if isinstance(s['review_limit'],bool) or not isinstance(s['review_limit'],(int,float)) or not math.isfinite(s['review_limit']) or not 0<=s['review_limit']<=1000000: raise ValueError('Invalid review limit')
        if s['deputy'] not in ROLES or s['profile']!='demo': raise ValueError('Only the explicitly selected demo profile is configured')
        if not isinstance(s['holiday_dates'],list): raise ValueError('Holiday dates must be a list')
        for day in s['holiday_dates']: datetime.strptime(day,'%Y-%m-%d')
        if s['triage_auto_accept'] not in {'high','medium','never'}: raise ValueError('Triage auto-accept must be high, medium or never')
        if s['tenant_messages'] not in {'claude_decides','staff_approval','off'}: raise ValueError('Tenant messages must be claude_decides, staff_approval or off')
        if not isinstance(s['tenant_auto_send_topics'],list) or set(s['tenant_auto_send_topics'])-set(TENANT_TOPICS): raise ValueError('Unsupported tenant auto-send topic')
        for k,hi in [('tenant_max_questions',5),('tenant_follow_ups',3)]:
            if isinstance(s[k],bool) or not isinstance(s[k],int) or not 0<=s[k]<=hi: raise ValueError(f'Invalid {k}')
        if s['tenant_max_questions']<1: raise ValueError('Tenant messages need at least one question')
        if not isinstance(s['required_per_action'],dict): raise ValueError('Action requirements must map actions to required facts')
        for a,keys in s['required_per_action'].items():
            if a not in REQUIRED or not isinstance(keys,list) or set(keys)-FACTS: raise ValueError('Unsupported action requirement')
        self.settings=s
        if len({r.id for r in self.rules})!=len(self.rules): raise ValueError('Duplicate rule ids')
        return self

class ReviewResponse(StrictModel):
    decision: Literal['approve','correct','reject','defer','more_evidence']
    reason: str = Field(min_length=5,max_length=3000)
    source_id: str | None = None
    claim_id: str | None = None
    key: str | None = None
    value: bool | float | None = None
    expires_at: str | None = None
    deadline: str | None = None
    scope: dict | None = None
    @model_validator(mode='after')
    def valid(self):
        if isinstance(self.value,float) and not math.isfinite(self.value): raise ValueError('A correction value must be finite')
        for date in (self.expires_at,self.deadline):
            if date is not None: dt(date)
        return self


def now(): return datetime.now(UTC)
def stamp(d=None): return (d or now()).astimezone(UTC).isoformat()
def dt(s):
    d=datetime.fromisoformat(s.replace('Z','+00:00'))
    if d.tzinfo is None: raise ValueError('An explicit timezone is required')
    return d.astimezone(UTC)
def digest(v): return hashlib.sha256(json.dumps(v,sort_keys=True,separators=(',',':')).encode()).hexdigest()
def scope_of(case):
    p=case['proposal']
    return {**p.get('scope',{}),'property_ref':case['property_ref'],'work_item':p['work_item'],'provider':p['provider'],'access_method':p['access_method'],'action':p['action'],'category':case['category']}
def approval_basis(case,claims,key,policy):
    if key=='authority': keys={'authority','total','classification'}
    elif key=='finance': keys={'total'}
    elif key.startswith('rule:'):
        rule=next((r for r in policy.get('rules',[]) if 'rule:'+r['id']==key),None)
        keys={c['key'] for c in rule['conditions']} if rule else set(FACTS)
    else: keys={key}
    superseded={x for c in claims if c.get('verified') for x in c.get('supersedes',[])}
    rows=[{'id':c['id'],'key':c['key'],'value':c['value'],'verified':c.get('verified',False)} for c in claims if c['key'] in keys and c['id'] not in superseded and scope_matches(c['scope'],case)]
    return digest(sorted(rows,key=lambda x:x['id']))

def business_id(case): return digest({'case_id':case['id'],'action_revision':case['action_revision'],'scope':scope_of(case)})
def scope_matches(scope,case):
    current=scope_of(case)
    return bool(scope) and all(k in current and current[k]==v for k,v in scope.items())

def working_after(start,hours,holidays=()):
    """Count real hours inside Mon-Fri 09:00-17:00 Europe/London (DST aware)."""
    local=start.astimezone(ZoneInfo('Europe/London')); remaining=hours*3600
    while remaining>0:
        if local.weekday()>=5 or local.date().isoformat() in holidays or local.hour>=17:
            local=(local+timedelta(days=1)).replace(hour=9,minute=0,second=0,microsecond=0); continue
        if local.hour<9: local=local.replace(hour=9,minute=0,second=0,microsecond=0)
        end=local.replace(hour=17,minute=0,second=0,microsecond=0)
        available=(end-local).total_seconds()
        used=min(remaining,available); local+=timedelta(seconds=used); remaining-=used
    return local.astimezone(UTC)

def triage_check(t):
    """Hold actions while a message is unread, unreadable or ambiguous."""
    base={'key':'triage','status':'UNKNOWN','source_ids':[t['source_id']] if t.get('source_id') else [],'claim_ids':[]}
    state=t.get('state')
    if state=='pending': return {**base,'reason':'Claude is reading the latest message. Actions wait for its reading.','response':'WAIT'}
    if state=='failed': return {**base,'reason':'Claude could not read the latest message ('+str(t.get('error') or 'unavailable')+'). A case manager must triage it manually or retry.','response':'HUMAN REVIEW'}
    if state!='done' or t.get('confirmed'): return None
    if t.get('route')=='urgent_hazard':
        # Clarifying is otherwise allowed alongside a hazard; a hazard reading
        # itself must reach a person before any automated contact.
        return {**base,'reason':'Claude read this as a possible urgent hazard. A case manager must take over now and apply the urgent procedure.','response':'HUMAN REVIEW'}
    if t.get('disagreement'):
        d=t['disagreement']; return {**base,'status':'CONFLICT','reason':f"Staff set the category to {d['staff']}, but Claude reads the message as {d['claude']}. Confirm or correct the category.",'response':'HUMAN REVIEW'}
    if t.get('open_ambiguities'):
        return {**base,'reason':'Clarify before routing: '+'; '.join(a['description'] for a in t['open_ambiguities']),'response':'CLARIFY'}
    return None

def evaluate(case,claims,approvals,policy,uncertain=False,at=None):
    at=at or now(); p=case['proposal']; action=p['action']; s=policy['settings']
    superseded={x for c in claims if c.get('verified') for x in c.get('supersedes',[])}
    current=[c for c in claims if c['id'] not in superseded and scope_matches(c['scope'],case) and (not c.get('expires_at') or dt(c['expires_at'])>at)]
    checkmap={}
    for key in FACTS:
        rows=[c for c in current if c['key']==key]
        values={json.dumps(c['value']) for c in rows}
        verified=[c for c in rows if c.get('verified')]
        if len(values)>1: status='CONFLICT'
        elif rows and any(c['value'] is False for c in rows): status='FAIL'
        elif verified: status='PASS'
        else: status='UNKNOWN'
        checkmap[key]={'key':key,'status':status,'reason':MESSAGES.get(key,key),'source_ids':list(dict.fromkeys(c['source_id'] for c in rows)),'claim_ids':[c['id'] for c in rows]}
    valid_approvals=[a for a in approvals if a['action_revision']==case['action_revision'] and a['scope']==scope_of(case) and a['policy_version']==policy['version'] and dt(a['expires_at'])>at and not a.get('revoked') and (not a.get('basis_hash') or a['basis_hash']==approval_basis(case,claims,a['key'],policy))]
    for key in ['authority','finance']:
        # A grant cannot override a refusal or material contradiction.
        if any(a['key']==key for a in valid_approvals) and checkmap.get(key,{}).get('status') not in {'FAIL','CONFLICT'}:
            checkmap[key]={'key':key,'status':'PASS','reason':'Current scoped approval recorded.','source_ids':[a['source_id'] for a in valid_approvals if a['key']==key],'claim_ids':[]}
    required=list(dict.fromkeys(REQUIRED.get(action,[])+s['required_per_action'].get(action,[])))
    if p['access_method']=='management_keys' and action in {'instruct_work','confirm_appointment','supply_keys'}: required.append('keys')
    if case['category'] not in CATEGORIES-{'other'} and action not in {'clarify','archive'}: required.append('supported')
    checks=[checkmap[k] for k in dict.fromkeys(required)]
    if action not in REQUIRED: checks.append({'key':'supported','status':'UNKNOWN','reason':MESSAGES['supported'],'source_ids':[],'claim_ids':[]})
    if any(c['key']=='urgent' and c['value'] is True for c in current) and action not in {'clarify','archive'}:
        checks.append({'key':'urgent','status':'FAIL','reason':MESSAGES['urgent'],'source_ids':[c['source_id'] for c in current if c['key']=='urgent'],'claim_ids':[]})
    totals=[c['value'] for c in current if c['key']=='total' and c.get('verified')]
    if action=='instruct_work' and totals and max(totals)>s['review_limit']:
        checks.append(checkmap.get('finance',{'key':'finance','status':'UNKNOWN','reason':MESSAGES['finance'],'source_ids':checkmap['total']['source_ids'],'claim_ids':checkmap['total']['claim_ids']}))
    if case.get('rejected_action_revision')==case['action_revision']: checks.append({'key':'rejection','status':'FAIL','reason':'This proposed action was rejected. Revise or reassign the action before reassessment.','source_ids':[],'claim_ids':[]})
    if case.get('policy_pending'): checks.append({'key':'policy','status':'UNKNOWN','reason':MESSAGES['policy'],'source_ids':[],'claim_ids':[]})
    if uncertain: checks.append({'key':'automation','status':'UNKNOWN','reason':MESSAGES['automation'],'source_ids':[],'claim_ids':[]})
    if case.get('profile','demo')!='demo': checks.append({'key':'profile','status':'CONFLICT','reason':MESSAGES['profile'],'source_ids':[],'claim_ids':[]})
    triage=triage_check(case.get('triage') or {})
    if triage and action!='archive': checks.append(triage)
    blockers=[]
    for c in checks:
        if c['status']=='PASS': continue
        k=c['key']; response='CLARIFY'; owner='case_manager'
        if k=='access': owner='access_officer'
        if k=='keys': owner='access_officer'
        if k in {'authority','finance'}: owner='approver'; response='HUMAN REVIEW'
        if k=='completion': owner='reviewer'
        if c['status']=='CONFLICT' or k in {'identity','route','urgent','supported','automation','policy','profile'}: response='HUMAN REVIEW'
        if k=='access' and s['access_immediate_review']: response='HUMAN REVIEW'
        if c['status']=='FAIL': response='STOP ACTION'
        if k=='urgent': response='HUMAN REVIEW'
        if c.get('response'): response=c['response']
        blockers.append({**c,'response':response,'owner':owner,'rule_id':f'require-{k}'})
    # Custom rules may add holds; they can never delete action requirements.
    for rule in policy.get('rules',[]):
        if rule['actions'] and action not in rule['actions']: continue
        if rule.get('property_ref') and rule['property_ref']!=case['property_ref']: continue
        if rule.get('category') and rule['category']!=case['category']: continue
        matches=[checkmap[c['key']]['status']==c['status'] for c in rule['conditions']]
        if (all(matches) if rule['match']=='all' else any(matches)):
            if rule['response']=='HUMAN REVIEW' and any(a['key']=='rule:'+rule['id'] for a in valid_approvals): continue
            selected=[checkmap[c['key']] for c in rule['conditions'] if checkmap[c['key']]['status']==c['status']]
            # Custom conditions may reference a fact outside the action defaults.
            # A received assertion needs a fact-specific role verification route;
            # approving the rule itself cannot create the missing fact.
            for fact in selected:
                if fact['status']=='UNKNOWN' and fact['claim_ids'] and not any(b['key']==fact['key'] for b in blockers):
                    owner='access_officer' if fact['key'] in {'access','keys'} else 'approver' if fact['key']=='authority' else 'reviewer' if fact['key']=='completion' else 'case_manager'
                    blockers.append({**fact,'response':'HUMAN REVIEW','owner':owner,'rule_id':'verify-custom-'+rule['id']+'-'+fact['key'],'reason':'Verify the received source assertion used by this custom rule. '+fact['reason']})
            blockers.append({'key':'rule:'+rule['id'],'status':'FAIL' if rule['response']=='STOP ACTION' else 'UNKNOWN','reason':f"Rule {rule['id']} requires {rule['response'].lower()}.",'source_ids':list({s for c in selected for s in c['source_ids']}),'claim_ids':list({i for c in selected for i in c['claim_ids']}),'response':rule['response'],'owner':rule['owner'],'rule_id':rule['id']})
    # Clarification requires a known route. It remains a staff task when no route exists.
    if checkmap['identity']['status']!='PASS' or checkmap['route']['status']!='PASS':
        for b in blockers:
            if b['response']=='CLARIFY': b['response']='HUMAN REVIEW'; b['reason']+=' A verified route is required before asking externally.'
    priority={'STOP ACTION':0,'HUMAN REVIEW':1,'CLARIFY':2,'WAIT':3}
    blockers.sort(key=lambda b:priority[b['response']])
    return {'outcome':blockers[0]['response'] if blockers else 'ACT','checks':checks,'blockers':blockers,'owner':blockers[0]['owner'] if blockers else 'case_manager','next_step':blockers[0]['reason'] if blockers else f"Ready to {action.replace('_',' ')} through the simulated adapter.",'policy_version':policy['version'],'case_revision':case['revision'],'action_revision':case['action_revision'],'scope':scope_of(case),'assessed_at':stamp(at)}
