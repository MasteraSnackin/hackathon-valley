"""Append-only audit records plus replaceable case projections.
SQLite is local demonstration storage. PostgreSQL is the deployment target.
"""
import os, json, uuid
from pathlib import Path
from contextlib import contextmanager
from sqlalchemy import create_engine, MetaData, Table, Column, String, Text, select, insert, update, event
from .domain import stamp

ROOT=Path(__file__).resolve().parent.parent
metadata=MetaData()
records=Table('records',metadata,Column('id',String,primary_key=True),Column('kind',String,index=True,nullable=False),Column('case_id',String,index=True),Column('created_at',String,nullable=False),Column('payload',Text,nullable=False),Column('dedupe',String,unique=True))
cases=Table('cases',metadata,Column('id',String,primary_key=True),Column('payload',Text,nullable=False))
meta=Table('meta',metadata,Column('key',String,primary_key=True),Column('value',Text,nullable=False))

def make_engine(url=None):
    url=url or os.getenv('DATABASE_URL') or f'sqlite:///{ROOT}/var/property.db'
    if url.startswith('postgres://'): url='postgresql+psycopg://'+url[len('postgres://'):]
    if url.startswith('postgresql://'): url='postgresql+psycopg://'+url[len('postgresql://'):]
    engine=create_engine(url,connect_args={'check_same_thread':False,'timeout':30} if url.startswith('sqlite') else {},pool_pre_ping=True)
    if url.startswith('sqlite'):
        @event.listens_for(engine,'connect')
        def configure(dbapi,_):
            dbapi.execute('PRAGMA foreign_keys=ON'); dbapi.execute('PRAGMA journal_mode=WAL')
    with engine.begin() as c:
        # Concurrent serverless cold starts would otherwise race to create the schema.
        if engine.dialect.name!='sqlite':c.exec_driver_sql('SELECT pg_advisory_xact_lock(7240531)')
        metadata.create_all(c)
        if engine.dialect.name=='sqlite':
            c.exec_driver_sql("CREATE TRIGGER IF NOT EXISTS immutable_records_update BEFORE UPDATE ON records BEGIN SELECT RAISE(ABORT, 'Audit records are immutable'); END")
            c.exec_driver_sql("CREATE TRIGGER IF NOT EXISTS immutable_records_delete BEFORE DELETE ON records BEGIN SELECT RAISE(ABORT, 'Audit records are immutable'); END")
        else:
            c.exec_driver_sql("CREATE OR REPLACE FUNCTION reject_record_mutation() RETURNS trigger LANGUAGE plpgsql AS $$ BEGIN RAISE EXCEPTION 'Audit records are immutable'; END $$")
            c.exec_driver_sql('DROP TRIGGER IF EXISTS immutable_records ON records')
            c.exec_driver_sql('CREATE TRIGGER immutable_records BEFORE UPDATE OR DELETE ON records FOR EACH ROW EXECUTE FUNCTION reject_record_mutation()')
        if not c.execute(select(meta).where(meta.c.key=='transaction_lock')).first(): c.execute(insert(meta).values(key='transaction_lock',value='1'))
    return engine

class Store:
    def __init__(self,url=None): self.engine=make_engine(url); self.on_commit=None
    @contextmanager
    def tx(self):
        touched=set()
        with self.engine.connect() as c:
            if self.engine.dialect.name=='sqlite': c.exec_driver_sql('BEGIN IMMEDIATE')
            else:
                c.begin(); c.execute(select(meta).where(meta.c.key=='transaction_lock').with_for_update())
            # connection.info outlives a pooled checkout: always start clean.
            c.info['touched_cases']=touched
            try: yield c; c.commit()
            except: touched.clear(); c.rollback(); raise
            finally: c.info.pop('touched_cases',None)
        # Optional reader of committed records (the per-case audit trail export).
        if touched and self.on_commit: self.on_commit(touched)
    def add(self,c,kind,payload,case_id=None,dedupe=None):
        if dedupe:
            existing=c.execute(select(records).where(records.c.dedupe==dedupe)).mappings().first()
            if existing: return unpack(existing),False
        row={'id':uuid.uuid4().hex,'kind':kind,'case_id':case_id,'created_at':stamp(),'payload':json.dumps(payload,sort_keys=True),'dedupe':dedupe}
        c.execute(insert(records).values(**row))
        if case_id and 'touched_cases' in c.info: c.info['touched_cases'].add(case_id)
        return unpack(row),True
    def list(self,c,kind=None,case_id=None):
        q=select(records).order_by(records.c.created_at,records.c.id)
        if kind:q=q.where(records.c.kind==kind)
        if case_id:q=q.where(records.c.case_id==case_id)
        return [unpack(r) for r in c.execute(q).mappings()]
    def get_record(self,c,rid):
        row=c.execute(select(records).where(records.c.id==rid)).mappings().first()
        if not row: raise ValueError('Record not found')
        return unpack(row)
    def case(self,c,cid):
        row=c.execute(select(cases).where(cases.c.id==cid)).mappings().first()
        if not row: raise ValueError('Case not found')
        return json.loads(row['payload'])
    def case_list(self,c): return [json.loads(r['payload']) for r in c.execute(select(cases)).mappings()]
    def save_case(self,c,case,new=False):
        if new:c.execute(insert(cases).values(id=case['id'],payload=json.dumps(case)))
        else:c.execute(update(cases).where(cases.c.id==case['id']).values(payload=json.dumps(case)))
    def get_meta(self,c,key):
        row=c.execute(select(meta).where(meta.c.key==key)).mappings().first()
        return json.loads(row['value']) if row else None
    def set_meta(self,c,key,value):
        if self.get_meta(c,key) is not None:c.execute(update(meta).where(meta.c.key==key).values(value=json.dumps(value)))
        else:c.execute(insert(meta).values(key=key,value=json.dumps(value)))

def unpack(row): return {'id':row['id'],'kind':row['kind'],'case_id':row['case_id'],'created_at':row['created_at'],'payload':json.loads(row['payload'])}
def payload(row): return {**row['payload'],'id':row['id'],'created_at':row['created_at']}
