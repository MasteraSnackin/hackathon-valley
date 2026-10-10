"""Read only allowed BUILD prefixes, let Claude triage them, and assess them in an isolated local store."""
from __future__ import annotations

import argparse
import json
from pathlib import Path
from tempfile import TemporaryDirectory

from . import ai
from .build_data import ALLOWED, import_case, verify_sources
from .service import Service
from .store import Store


def replay(case_ids, event_count=1):
    if set(case_ids)-ALLOWED:
        raise ValueError('Only the fixed BUILD partition is available')
    verify_sources()
    results=[]
    # Claude reads each chronological prefix (sent to the Anthropic API). No
    # outbound adapter runs: tenant messages are drafted and gated, and every
    # send stays inside the simulated thread of an isolated database.
    with TemporaryDirectory(prefix='property-build-replay-') as directory:
        service=Service(Store('sqlite:///'+str(Path(directory)/'replay.db')))
        actor={'id':'build-replay','role':'case_manager'}
        for case_id in case_ids:
            cid=import_case(service,case_id,actor,event_count)['case']['id']
            split=service.claude_steps(cid)
            for detail in [service.detail(x) for x in [cid,*split]]:
                case=detail['case'];triage=case.get('triage') or {}
                results.append({'build_case_id':case_id,'event_count':event_count,'case_id':case['id'],'split_from':case.get('parent_case_id'),
                    'triage':{k:triage.get(k) for k in ('state','route','confidence','summary','risk_flags','open_ambiguities','disagreement','error')},
                    'category':case['category'],'proposed_action':case['proposal']['action'],'work_item':case['proposal']['work_item'],
                    'outcome':detail['decision']['outcome'],
                    'blockers':[{'key':b['key'],'status':b['status'],'response':b['response']} for b in detail['decision']['blockers']],
                    'claims':[{'key':c['key'],'value':c['value'],'verified':c['verified'],'quote':c['source_quote'][:200]} for c in detail['claims'] if c.get('origin')=='claude'],
                    'tenant_messages':[{'status':m['status'],'text':m.get('text'),'gate':m.get('gate')} for m in detail['tenant_messages']],
                    'source_count':len(detail['evidence']),'action_count':len(detail['actions'])})
        service.db.engine.dispose()
    return {'partition':'BUILD','model':ai.model_id(),'prompt_version':ai.PROMPT_VERSION,'external_operations':'not executed (simulated thread only)',
        'policy_version':1,'notice':'Chronological development replay, not an accuracy score. No eventual outcome is used as ground truth. All attachments are excluded.',
        'cases':results}


def main():
    from .localenv import load_local_env
    load_local_env()
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--case',choices=sorted(ALLOWED))
    parser.add_argument('--events',type=int,default=1)
    parser.add_argument('--all-first',action='store_true')
    parser.add_argument('--output',type=Path)
    args=parser.parse_args()
    if bool(args.case)==args.all_first:parser.error('Choose --case or --all-first')
    if args.all_first and args.events!=1:parser.error('--all-first exposes only event 001')
    report=replay(sorted(ALLOWED) if args.all_first else [args.case],args.events)
    rendered=json.dumps(report,indent=2)
    if args.output:
        args.output.parent.mkdir(parents=True,exist_ok=True)
        args.output.write_text(rendered+'\n')
        print(str(args.output.resolve()))
    else:print(rendered)


if __name__=='__main__':main()
