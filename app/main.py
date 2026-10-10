from __future__ import annotations
import os, secrets, hashlib, hmac, json, asyncio
from pathlib import Path
from contextlib import asynccontextmanager
from datetime import timedelta
from fastapi import FastAPI, Request, Depends, Body, Query, BackgroundTasks
from fastapi.responses import JSONResponse, FileResponse
from fastapi.staticfiles import StaticFiles
from .localenv import load_local_env
load_local_env()
from .domain import *
from .service import get_service,Forbidden,Conflict,VOICE_BRIDGE
from . import ai, jev, parties
from .build_data import list_build,import_case,snapshot
from .voice import TUNNEL_PATHS,create_voice_router

ROOT=Path(__file__).resolve().parent.parent
MODE=os.getenv('APP_MODE','demo')
WORKFLOW_MODE=os.getenv('WORKFLOW_MODE','native_local')
SESSIONS={}

async def wake(cid):
    service=get_service()
    if WORKFLOW_MODE=='manual_demo':
        # Labelled manual mode: Claude reads and drafts inline in this request;
        # timers and actions still wait for the staff buttons.
        spawned=await asyncio.to_thread(service.claude_steps,cid)
        for new_id in spawned:await wake(new_id)
        return {'mode':'manual_demo','notice':'Native workflow not running','split_case_ids':spawned}
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

async def settle(cid,result):
    """Wake the coordinator; in manual mode return the state after inline Claude steps."""
    await wake(cid)
    if WORKFLOW_MODE=='manual_demo':return await asyncio.to_thread(get_service().detail,cid)
    return result

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

def tunnelled(request):return bool({'x-forwarded-for','x-forwarded-host','forwarded'}&set(request.headers.keys()))

@app.middleware('http')
async def security(request,call_next):
    # Demo sessions trust loopback, and a tunnel (ngrok) arrives from loopback too:
    # proxied requests may only reach the secret-authenticated phone webhooks.
    if MODE=='demo' and tunnelled(request) and request.url.path not in TUNNEL_PATHS|{'/api/inbound'}:
        return JSONResponse({'detail':'Only the phone intake webhooks are reachable through a tunnel'},403)
    # No CORS, cookies SameSite strict, and reject cross-origin state changes.
    if request.method not in {'GET','HEAD','OPTIONS'}:
        origin=request.headers.get('origin')
        if origin and origin.rstrip('/')!=str(request.base_url).rstrip('/'):
            return JSONResponse({'detail':'Cross-origin mutations are not permitted'},403)
    response=await call_next(request)
    response.headers['X-Content-Type-Options']='nosniff'
    response.headers['Referrer-Policy']='same-origin'
    if request.url.path.startswith('/api/'):
        response.headers['Cache-Control']='no-store'
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

def voice_bridge(request:Request):
    """The voice agent sends Bearer VOICE_BRIDGE_TOKEN; the demo call panel uses a staff session."""
    expected=os.getenv('VOICE_BRIDGE_TOKEN','')
    token=request.headers.get('authorization','').removeprefix('Bearer ')
    if expected and token and hmac.compare_digest(hashlib.sha256(token.encode()).digest(),hashlib.sha256(expected.encode()).digest()):return VOICE_BRIDGE
    # Through a tunnel only the bridge token counts; a staff session never does.
    if tunnelled(request):raise Forbidden('Voice bridge token required')
    return {**VOICE_BRIDGE,'via':actor(request)['id']}

def model_status():
    # Reports whether a credential is configured, never the credential.
    return {'provider':'anthropic','model':ai.model_id(),'credential_configured':ai.configured(),'prompt_version':ai.PROMPT_VERSION}

@app.get('/api/session')
def session(request:Request):
    try:who=actor(request)
    except Forbidden:who=None
    return {'actor':who,'mode':MODE,'workflow_mode':WORKFLOW_MODE,'external_operations':'simulated','model':model_status(),'authentication':'Loopback-only demonstration sessions, unsuitable for production' if MODE=='demo' else 'Server-configured staff API credentials'}

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
    result=await asyncio.to_thread(get_service().intake,data,who);return await settle(result['case']['id'],result)
@app.get('/api/cases/{cid}')
def detail(cid:str,who=Depends(actor)):return get_service().detail(cid)
@app.post('/api/cases/{cid}/evidence')
async def evidence(cid:str,data:EvidenceInput,who=Depends(actor)):
    result=await asyncio.to_thread(get_service().evidence,cid,data,who);return await settle(cid,result)
@app.post('/api/cases/{cid}/proposal')
async def proposal(cid:str,data:ProposalInput,who=Depends(actor)):
    result=await asyncio.to_thread(get_service().proposal,cid,data,who);return await settle(cid,result)
@app.post('/api/cases/{cid}/evaluate')
async def assess(cid:str,who=Depends(actor)):
    result=await asyncio.to_thread(get_service().evaluate_case,cid,who);return await settle(cid,result)
@app.post('/api/cases/{cid}/execute')
async def execute(cid:str,data:dict=Body(default={}),who=Depends(actor)):
    result=await asyncio.to_thread(get_service().execute,cid,who,data.get('outcome','success'));return await settle(cid,result)
@app.post('/api/cases/{cid}/reconcile')
async def reconcile(cid:str,who=Depends(actor)):
    result=await asyncio.to_thread(get_service().reconcile,cid,who);return await settle(cid,result)
@app.post('/api/cases/{cid}/tick')
async def tick(cid:str,who=Depends(actor)):
    get_service().role(who,{'case_manager'});await asyncio.to_thread(get_service().tick,cid);await wake(cid);return await asyncio.to_thread(get_service().detail,cid)
@app.post('/api/cases/{cid}/tenant-reply')
async def tenant_reply(cid:str,data:dict=Body(...),who=Depends(actor)):
    if set(data)-{'text'} or not isinstance(data.get('text'),str) or not data['text'].strip():raise ValueError('Send {"text": "..."} only')
    result=await asyncio.to_thread(get_service().tenant_reply,cid,data['text'][:50000],who);return await settle(cid,result)
@app.post('/api/cases/{cid}/triage/retry')
async def retry_triage(cid:str,who=Depends(actor)):
    result=await asyncio.to_thread(get_service().retry_triage,cid,who);return await settle(cid,result)
@app.post('/api/messages/{mid}/approve')
async def approve_message(mid:str,data:dict=Body(default={}),who=Depends(actor)):
    if set(data)-{'text'}:raise ValueError('Only an optional edited text is accepted')
    result=await asyncio.to_thread(get_service().approve_message,mid,who,data.get('text'));return await settle(result['case']['id'],result)
@app.post('/api/messages/{mid}/reject')
async def reject_message(mid:str,data:dict=Body(...),who=Depends(actor)):
    if set(data)-{'reason','redraft'}:raise ValueError('Send reason and optional redraft only')
    result=await asyncio.to_thread(get_service().reject_message,mid,who,data.get('reason',''),bool(data.get('redraft')));return await settle(result['case']['id'],result)
@app.post('/api/reviews/{rid}/respond')
async def respond(rid:str,data:ReviewResponse,who=Depends(actor)):
    result=await asyncio.to_thread(get_service().respond,rid,data,who);return await settle(result['case']['id'],result)
@app.post('/api/inbound')
async def inbound(data:InboundCall,background:BackgroundTasks,who=Depends(voice_bridge)):
    # Answer the caller first; the case coordinator reads the message after.
    result=await asyncio.to_thread(get_service().inbound,data,who)
    if result['case_id']:background.add_task(wake,result['case_id'])
    return result
@app.get('/api/inbound/directory')
def inbound_directory(who=Depends(actor)):return parties.directory_view()
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
    result=await asyncio.to_thread(import_case,get_service(),bid,who,data.get('event_count',1));return await settle(result['case']['id'],result)
@app.get('/api/health')
def health():return {'status':'ok','mode':MODE,'workflow_mode':WORKFLOW_MODE,'external_operations':'simulated','model':model_status(),
    'router':{'provider':'typesafe','model':jev.model_id(),'credential_configured':jev.configured(),'router_version':jev.ROUTER_VERSION}}

# Tenant sessions have their own ownership-checked routes. The view switch is
# demonstration navigation; it is never used as an authorisation boundary.
from .tenant import create_tenant_router
from .policy_assistant import create_policy_assistant_router
app.include_router(create_tenant_router(wake, mode=MODE))
app.include_router(create_policy_assistant_router(actor))
app.include_router(create_voice_router(wake, actor))

@app.get('/')
def index():return FileResponse(ROOT/'static/index.html')
@app.get('/dashboard')
def dashboard():
    # React staff dashboard (web/), built into static/dashboard by `npm run build`.
    page=ROOT/'static/dashboard/index.html'
    if not page.exists():return JSONResponse({'detail':'Dashboard not built. Run `npm run build` in web/.'},404)
    return FileResponse(page)
app.mount('/static',StaticFiles(directory=ROOT/'static'),name='static')
