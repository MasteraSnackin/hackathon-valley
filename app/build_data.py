"""Strict BUILD-only chronological source loader. Index summaries never enter replay."""
from pathlib import Path
import json, hashlib, re
from .domain import Intake
ROOT=Path(__file__).resolve().parent.parent
ALLOWED={'002','005','006','008','013','016','017','018','019','020','021','023','025','027','028','031','034','036','038','041','043','045','047','048','049'}
MANIFEST=ROOT/'handoff/BUILD_MANIFEST.json'

def manifest():
    data=json.loads(MANIFEST.read_text())
    if {c['case_id'] for c in data['cases']}!=ALLOWED:raise ValueError('BUILD manifest does not match the fixed allowed partition')
    return data

def verify_sources():
    result=[]
    for item in manifest()['files']:
        if item['case_id'] not in ALLOWED:raise ValueError('Case outside BUILD partition')
        path=ROOT/'data/build'/item['path']
        if not path.resolve().is_relative_to((ROOT/'data/build'/item['case_id']).resolve()):raise ValueError('Invalid source path')
        actual=hashlib.sha256(path.read_bytes()).hexdigest()
        if actual!=item['sha256']:raise ValueError('Source hash mismatch: '+item['path'])
        result.append(item['path'])
    return result

def snapshot(case_id,event_count=1):
    if case_id not in ALLOWED:raise ValueError('Only allowed BUILD cases may be loaded')
    if isinstance(event_count,bool) or not isinstance(event_count,int) or event_count<1:raise ValueError('Choose a positive event count')
    path=ROOT/'data/build'/case_id/'history.md'
    expected=next(f['sha256'] for f in manifest()['files'] if f['path']==f'{case_id}/history.md')
    if hashlib.sha256(path.read_bytes()).hexdigest()!=expected:raise ValueError('History hash mismatch')
    parts=re.split(r'(?=<a id="event-\d+">)',path.read_text())[1:]
    if event_count>len(parts):raise ValueError('Snapshot exceeds available history')
    text='\n'.join(parts[:event_count])
    return {'case_id':case_id,'event_count':event_count,'text':text,'attachments':[],'boundary':'Only selected chronological history prefix. Current index, later events and all attachments excluded.','source_url':next(x['source_url'] for x in manifest()['cases'] if x['case_id']==case_id)+'/history.md'}

def list_build():
    return [{**c,'preview':snapshot(c['case_id'])['text'],'snapshot_event_count':1} for c in manifest()['cases']]

def import_case(service,case_id,actor,event_count=1):
    snap=snapshot(case_id,event_count)
    # Titles/categories can contain later summaries, so they are catalogue labels
    # only, not input to the decision-time interpretation or source claims.
    report=snap['text']
    found=re.search(r'(?:Address:|property at )([^\n]+)',report,re.I)
    prop=found.group(1).strip()[:200] if found else 'Unverified property — BUILD '+case_id
    result=service.intake(Intake(title=f'BUILD {case_id} · through event {event_count:03d}',property_ref=prop,report=report,category='other',work_item='Recorded request; scope unverified',action='request_quote'),actor)
    cid=result['case']['id']
    with service.db.tx() as c:
        service.db.add(c,'build_snapshot',{'case_id':case_id,'event_count':event_count,'source_url':snap['source_url'],'boundary':snap['boundary'],'attachments':[]},cid)
    return service.detail(cid)
