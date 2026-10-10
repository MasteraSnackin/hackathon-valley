"""HTTP validation and server-side role boundaries, local demonstration only."""
import pytest
from fastapi.testclient import TestClient
from app import main,service
from app.service import Service
from app.store import Store

@pytest.fixture
def client(tmp_path,monkeypatch):
    monkeypatch.setattr(service,'_service',Service(Store('sqlite:///'+str(tmp_path/'api.db'))))
    monkeypatch.setattr(main,'WORKFLOW_MODE','manual_demo')
    with TestClient(main.app) as c:yield c

def session(client,role='case_manager'):assert client.post('/api/demo-session',json={'role':role}).status_code==200

def test_api_session_roles_and_csrf(client):
    assert client.get('/api/cases').status_code==403
    session(client)
    data={'title':'BUILD-derived plumbing','property_ref':'DEMO-FLAT-1','report':'The tap drips','action':'request_quote','category':'plumbing','triage':'staff'}
    bad=client.post('/api/cases',json=data,headers={'Origin':'https://untrusted.example'});assert bad.status_code==403
    case=client.post('/api/cases',json=data).json();assert case['decision']['outcome']=='ACT'
    session(client,'reviewer');assert client.post('/api/cases',json=data).status_code==403
    assert client.get('/api/cases').status_code==200
    assert client.post('/api/policies/draft',json={'base_version':1,'settings':{}}).status_code==403

def test_api_validates_sources_and_preserves_pending_case(client,no_claude):
    session(client)
    case=client.post('/api/cases',json={'title':'BUILD-derived repair','property_ref':'Unknown flat','report':'A broken window needs repair'}).json();cid=case['case']['id']
    assert case['reviews']
    bad=client.post(f'/api/cases/{cid}/evidence',json={'text':'I am at home.','source_label':'Tenant','claims':[{'key':'access','value':True,'source_quote':'I grant permission'}]})
    assert bad.status_code==422
    good=client.post(f'/api/cases/{cid}/evidence',json={'text':'I am at home.','source_label':'Tenant'})
    assert good.status_code==200;assert good.json()['case']['revision']>case['case']['revision']
    assert good.json()['case']['triage']['state']=='failed'
    assert client.post(f'/api/cases/{cid}/execute',json={}).status_code==409

def test_reserved_cases_not_available(client):
    session(client)
    assert len(client.get('/api/build-cases').json())==25
    assert client.post('/api/build-cases/001/import',json={}).status_code==400
