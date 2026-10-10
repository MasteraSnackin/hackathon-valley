from __future__ import annotations
import os, secrets, hashlib, hmac, json, asyncio
from pathlib import Path
from contextlib import asynccontextmanager
from datetime import timedelta
from fastapi import FastAPI, Request, Depends, Body, Query
from fastapi.responses import JSONResponse, FileResponse
from fastapi.staticfiles import StaticFiles
from .domain import *
from .service import get_service,Forbidden,Conflict
from .build_data import list_build,import_case,snapshot

ROOT=Path(__file__).resolve().parent.parent
MODE=os.getenv('APP_MODE','demo')
WORKFLOW_MODE=os.getenv('WORKFLOW_MODE','native_local')
SESSIONS={}

async def wake(cid):
    service=get_service()
    if WORKFLOW_MODE=='manual_demo':return {'mode':'manual_demo','notice':'Native workflow not running'}
    from .workflows import start_case_coordinator,signal_case_event
    try:
        run_id=await start_case_coordinator(cid)
        detail=await asyncio.to_thread(service.detail,cid)
        events=[e for e in detail['timeline'] if e['kind']=='incoming_event']
        if events:
            e=events[-1]; receipt=await signal_case_event(cid,e['id'],detail['case']['revision'])
        else:receipt={'status':'started'}
        with service.db.tx() as c:service.db.add(c,'workflow_receipt',{'run_id':run_id,'transport':receipt,'mode':WORKFLOW_MODE},cid)
        return {**receipt,'run_id':receipt.get('run_id') or run_id}
    except Exception as exc:
        with service.db.tx() as c:service.db.add(c,'workflow_error',{'error_type':type(exc).__name__,'notice':'Event is durably stored; pending recovery. Native orchestration has not been confirmed.'},cid)
        return {'status':'pending_recovery','error_type':type(exc).__name__}

@asynccontextmanager
async def lifespan(app):
    from .workflows import validate_runtime_mode
    validate_runtime_mode(WORKFLOW_MODE)
    if MODE!='demo':
        if not os.getenv('DATABASE_URL','').startswith(('postgres','postgresql')):raise RuntimeError('Deployment requires PostgreSQL DATABASE_URL; local SQLite is not production storage')
        if not os.getenv('STAFF_TOKEN_ROLES'):raise RuntimeError('Deployment requires server-configured staff token identities; demonstration roles are disabled')
    get_service()
    if WORKFLOW_MODE=='native_local':
        from .workflows import native_runtime_lifespan,recover_local_case_steps
        async with native_runtime_lifespan():
            for case in get_service().list_cases():
                receipt=await recover_local_case_steps(case['id'])
                with get_service().db.tx() as c:get_service().db.add(c,'workflow_recovery',receipt,case['id'])
                await wake(case['id'])
            yield
    else:
        if WORKFLOW_MODE=='native_cloud':
            for case in get_service().list_cases():await wake(case['id'])
        yield

app=FastAPI(title='Property Workflow',lifespan=lifespan)

@app.exception_handler(Forbidden)
async def forbidden_handler(request,exc):return JSONResponse({'detail':str(exc)},status_code=403)
@app.exception_handler(Conflict)
async def conflict_handler(request,exc):return JSONResponse({'detail':str(exc)},status_code=409)
@app.exception_handler(ValueError)
async def value_handler(request,exc):return JSONResponse({'detail':str(exc)},status_code=400)

@app.middleware('http')
async def security(request,call_next):
    # No CORS, cookies SameSite strict, and reject cross-origin state changes.
    if request.method not in {'GET','HEAD','OPTIONS'}:
        origin=request.headers.get('origin')
        if origin and origin.rstrip('/')!=str(request.base_url).rstrip('/'):
            return JSONResponse({'detail':'Cross-origin mutations are not permitted'},403)
    response=await call_next(request)
    response.headers['X-Content-Type-Options']='nosniff'
    response.headers['Referrer-Policy']='same-origin'
    response.headers['Content-Security-Policy']="default-src 'self'; script-src 'self'; style-src 'self'; connect-src 'self'; img-src 'self' data:; frame-ancestors 'none'"
    return response

def actor(request:Request):
    if MODE=='demo':
        host=request.client.host if request.client else ''
        # TestClient is in-process; demo HTTP must be loopback.
        if host not in {'127.0.0.1','::1','localhost','testclient'}:raise Forbidden('Demo sessions are restricted to this computer')
        token=request.cookies.get('pw_session');session=SESSIONS.get(token)
        if not session:raise Forbidden('Choose a labelled demonstration session first')
        return session
    token=request.headers.get('authorization','').removeprefix('Bearer ')
    for identity in json.loads(os.environ['STAFF_TOKEN_ROLES']):
        if hmac.compare_digest(hashlib.sha256(token.encode()).hexdigest(),identity['sha256']):
            if identity['role'] not in ROLES:raise Forbidden('Unknown staff role')
            return {'id':identity['id'],'role':identity['role']}
    raise Forbidden('Valid staff authentication required')

@app.get('/api/session')
def session(request:Request):
    try:who=actor(request)
    except Forbidden:who=None
    return {'actor':who,'mode':MODE,'workflow_mode':WORKFLOW_MODE,'external_operations':'simulated','authentication':'Loopback-only demonstration sessions, unsuitable for production' if MODE=='demo' else 'Server-configured staff API credentials'}

@app.post('/api/demo-session')
def demo_session(request:Request,data:dict=Body(...)):
    if MODE!='demo' or request.client.host not in {'127.0.0.1','::1','localhost','testclient'}:raise Forbidden('Demonstration sessions unavailable')
    role=data.get('role')
    if role not in ROLES:raise ValueError('Unknown role')
    token=secrets.token_urlsafe(32);SESSIONS[token]={'id':'demo-'+role,'role':role}
    response=JSONResponse({'actor':SESSIONS[token],'mode':'demo'});response.set_cookie('pw_session',token,httponly=True,samesite='strict',secure=False,max_age=28800);return response

@app.get('/api/cases')
def case_list(who=Depends(actor)):return get_service().list_cases()
@app.post('/api/cases')
async def create(data:Intake,who=Depends(actor)):
    result=await asyncio.to_thread(get_service().intake,data,who);await wake(result['case']['id']);return result
@app.get('/api/cases/{cid}')
def detail(cid:str,who=Depends(actor)):return get_service().detail(cid)
@app.post('/api/cases/{cid}/evidence')
async def evidence(cid:str,data:EvidenceInput,who=Depends(actor)):
    result=await asyncio.to_thread(get_service().evidence,cid,data,who);await wake(cid);return result
@app.post('/api/cases/{cid}/proposal')
async def proposal(cid:str,data:ProposalInput,who=Depends(actor)):
    result=await asyncio.to_thread(get_service().proposal,cid,data,who);await wake(cid);return result
@app.post('/api/cases/{cid}/evaluate')
async def assess(cid:str,who=Depends(actor)):
    result=await asyncio.to_thread(get_service().evaluate_case,cid,who);await wake(cid);return result
@app.post('/api/cases/{cid}/execute')
async def execute(cid:str,data:dict=Body(default={}),who=Depends(actor)):
    result=await asyncio.to_thread(get_service().execute,cid,who,data.get('outcome','success'));await wake(cid);return result
@app.post('/api/cases/{cid}/reconcile')
async def reconcile(cid:str,who=Depends(actor)):
    result=await asyncio.to_thread(get_service().reconcile,cid,who);await wake(cid);return result
@app.post('/api/cases/{cid}/tick')
async def tick(cid:str,who=Depends(actor)):
    get_service().role(who,{'case_manager'});await asyncio.to_thread(get_service().tick,cid);await wake(cid);return get_service().detail(cid)
@app.post('/api/reviews/{rid}/respond')
async def respond(rid:str,data:ReviewResponse,who=Depends(actor)):
    result=await asyncio.to_thread(get_service().respond,rid,data,who);await wake(result['case']['id']);return result
@app.get('/api/policies')
def policies(who=Depends(actor)):return get_service().policies()
@app.post('/api/policies/draft')
def draft(data:PolicyInput,who=Depends(actor)):return get_service().draft(data,who)
@app.post('/api/policies/{pid}/preview')
def preview(pid:str,who=Depends(actor)):return get_service().preview(pid,who)
@app.post('/api/policies/{pid}/publish')
async def publish(pid:str,who=Depends(actor)):
    result=await asyncio.to_thread(get_service().publish,pid,who)
    for case in get_service().list_cases():await wake(case['id'])
    return result
@app.get('/api/build-cases')
def builds(who=Depends(actor)):return list_build()
@app.get('/api/build-cases/{bid}/snapshot')
def build_snapshot(bid:str,event_count:int=Query(default=1,ge=1),who=Depends(actor)):return snapshot(bid,event_count)
@app.post('/api/build-cases/{bid}/import')
async def import_build(bid:str,data:dict=Body(default={}),who=Depends(actor)):
    if set(data)-{'event_count'}:raise ValueError('Only event_count is supported')
    result=await asyncio.to_thread(import_case,get_service(),bid,who,data.get('event_count',1));await wake(result['case']['id']);return result
@app.get('/api/health')
def health():return {'status':'ok','mode':MODE,'workflow_mode':WORKFLOW_MODE,'external_operations':'simulated'}
@app.get('/')
def index():return FileResponse(ROOT/'static/index.html')
app.mount('/static',StaticFiles(directory=ROOT/'static'),name='static')
