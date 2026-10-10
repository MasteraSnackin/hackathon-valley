"""End-to-end router evaluation on the BUILD partition, message by message.

Each allowed case is replayed chronologically: event 001 is the intake report
and events 002..N arrive one at a time as new messages. After each message the
same service functions the workflow steps call (routing, triage) run inline in
an isolated database. Two runs use the same messages:

  shadow  Claude triages every message (the behaviour before Jev); Jev's
          independent decision is recorded but not applied
  jev     the production configuration: Jev routes first and hands off to Claude

Claude's shadow reading is the reference, so route figures are agreement with
Claude, not accuracy against ground truth. No eventual outcome, later event,
index summary or attachment is used. Tenant drafting is off and every action
stays simulated.
"""
from __future__ import annotations

import argparse, json, statistics, threading, time
from collections import Counter
from concurrent.futures import ThreadPoolExecutor
from datetime import datetime, timezone
from pathlib import Path
from tempfile import TemporaryDirectory

from . import ai, jev
from .build_data import ALLOWED, events, import_case, verify_sources
from .domain import EvidenceInput, PolicyInput
from .service import Service
from .store import Store

ACTOR = {'id': 'router-eval', 'role': 'case_manager'}
EDITOR = {'id': 'router-eval-policy', 'role': 'policy_editor'}
MODES = {'shadow': 'jev_shadow', 'jev': 'jev'}
_probe = threading.local()


def _probing_ask(ask):
    """In shadow runs, re-ask Jev with the route options reversed (option-order check)."""
    def wrapped(text, context, reverse=False):
        answers, meta = ask(text, context, reverse)
        if getattr(_probe, 'reverse', None) is not None:
            try:
                _probe.reverse.append(ask(text, context, True)[0]['route']['choice'])
            except jev.JevUnavailable:
                _probe.reverse.append(None)
        return answers, meta
    return wrapped


def _payloads(detail, kind, source_id):
    return [r['payload'] for r in detail['timeline'] if r['kind'] == kind and r['payload'].get('source_id') == source_id]


def _claude_route(reading):
    if not reading or reading.get('provider') != 'anthropic' or reading.get('status') != 'ok':
        return None
    issues = reading['result']['issues']
    primary = next((i for i in issues if i['relation'] == 'current_case'), issues[0] if issues else None)
    return primary['route'] if primary else 'none'


def run_case(case_id, mode, count, directory):
    service = Service(Store('sqlite:///' + str(Path(directory) / f'{case_id}-{mode}.db')))
    draft = service.draft(PolicyInput(base_version=1, settings={'router': MODES[mode], 'tenant_messages': 'off'}, reason='Router evaluation'), EDITOR)
    service.preview(draft['id'], EDITOR)
    service.publish(draft['id'], EDITOR)
    _probe.reverse = [] if mode == 'shadow' else None
    rows, cid = [], None
    for event in events(case_id, count):
        started = time.monotonic()
        if cid is None:
            detail = import_case(service, case_id, ACTOR, 1)
            cid = detail['case']['id']
            source_id = next(e['id'] for e in detail['evidence'] if e['source_label'] == 'Intake report')
        else:
            label = f"BUILD {case_id} event {event['number']:03d} · {event['channel']} from {event['sender']} to {event['recipient']}"[:200]
            detail = service.evidence(cid, EvidenceInput(text=event['text'] or '(empty message)', source_label=label), ACTOR)
            source_id = detail['evidence'][-1]['id']
        probes_before = len(_probe.reverse or [])
        spawned = service.claude_steps(cid)
        elapsed = time.monotonic() - started
        detail = service.detail(cid)
        routing = (_payloads(detail, 'routing', source_id) or [None])[-1]
        reading = (_payloads(detail, 'interpretation', source_id) or [None])[-1]
        case, triage = detail['case'], detail['case'].get('triage') or {}
        answers = (routing or {}).get('answers') or {}
        rows.append({
            'case': case_id, 'event': event['number'], 'channel': event['channel'], 'sender': event['sender'], 'mode': mode,
            'seconds': round(elapsed, 2),
            'router_mode': (routing or {}).get('mode'), 'proposed_mode': (routing or {}).get('proposed_mode'),
            'jev_choice': answers.get('route', {}).get('choice'), 'jev_confidence': answers.get('route', {}).get('confidence'),
            'jev_decided_route': ((routing or {}).get('decision') or {}).get('route'),
            'jev_reasons': ((routing or {}).get('decision') or {}).get('reasons'),
            'jev_signals': answers.get('signals'), 'jev_category': answers.get('category', {}).get('choice'),
            'jev_reverse_choice': _probe.reverse[probes_before] if mode == 'shadow' and len(_probe.reverse) > probes_before else None,
            'jev_latency_ms': (routing or {}).get('latency_ms'), 'jev_error': (routing or {}).get('error_type'),
            'jev_input_tokens': ((routing or {}).get('usage') or {}).get('input_tokens', 0),
            'claude_called': bool(reading and reading.get('provider') == 'anthropic'),
            'claude_status': (reading or {}).get('status') if reading and reading.get('provider') == 'anthropic' else None,
            'claude_route': _claude_route(reading), 'claude_usage': (reading or {}).get('usage') if reading and reading.get('provider') == 'anthropic' else None,
            'claude_confidence': ((reading or {}).get('result') or {}).get('confidence'),
            'claude_claims': len(((reading or {}).get('result') or {}).get('claims') or []) if reading and reading.get('provider') == 'anthropic' else 0,
            'final_route': triage.get('route'), 'triage_state': triage.get('state'), 'route_disagreement': triage.get('route_disagreement'),
            'action': case['proposal']['action'], 'category': case['category'], 'outcome': detail['decision']['outcome'],
            'blockers': sorted({f"{b['key']}:{b['response']}" for b in detail['decision']['blockers']}), 'spawned': len(spawned),
        })
    service.db.engine.dispose()
    return rows


def evaluate(case_ids, count, workers):
    verify_sources()
    jev.ask = _probing_ask(jev.ask)
    jobs = [(c, m) for c in sorted(case_ids) for m in MODES]
    results, errors = [], []
    with TemporaryDirectory(prefix='property-router-eval-') as directory, ThreadPoolExecutor(max_workers=workers) as pool:
        futures = {pool.submit(run_case, c, m, count, directory): (c, m) for c, m in jobs}
        for future, (c, m) in futures.items():
            try:
                results += future.result()
            except Exception as exc:  # noqa: BLE001 - one failed case must not hide the others
                errors.append({'case': c, 'mode': m, 'error': f'{type(exc).__name__}: {str(exc)[:300]}'})
    return {'generated_at': datetime.now(timezone.utc).isoformat(timespec='seconds'), 'partition': 'BUILD', 'cases': sorted(case_ids),
            'events_per_case': count, 'jev_model': jev.model_id(), 'router_version': jev.ROUTER_VERSION,
            'claude_model': ai.model_id(), 'prompt_version': ai.PROMPT_VERSION, 'errors': errors,
            'notice': 'Agreement with Claude, not accuracy. Chronological prefixes only; no outcome, later event, index summary or attachment used.',
            'rows': results}


def _pct(n, d):
    return f'{100 * n / d:.0f}% ({n}/{d})' if d else 'n/a'


def _tokens(rows):
    used = [r['claude_usage'] for r in rows if r['claude_usage']]
    return {k: sum(u.get(k, 0) for u in used) for k in ('input_tokens', 'output_tokens', 'cache_read_input_tokens', 'cache_creation_input_tokens')}


def summarise(report):
    rows = report['rows']
    shadow = [r for r in rows if r['mode'] == 'shadow']
    live = [r for r in rows if r['mode'] == 'jev']
    by_key = {(r['case'], r['event']): r for r in shadow}
    lines = [f"# Jev router evaluation (BUILD partition)", '',
             f"Generated {report['generated_at']} · {len(report['cases'])} cases · events 001–{report['events_per_case']:03d} of each case, one message at a time · "
             f"Jev `{report['jev_model']}` (`{report['router_version']}`) · Claude `{report['claude_model']}` (`{report['prompt_version']}`).", '',
             f"> {report['notice']} Reproduce with `python -m app.route_eval --events {report['events_per_case']}`.", '']
    if report['errors']:
        lines += ['**Errors:** ' + '; '.join(f"{e['case']}/{e['mode']}: {e['error']}" for e in report['errors']), '']

    # Shadow run: Claude decides every message, Jev's independent decision recorded.
    ref = [r for r in shadow if r['claude_route'] and r['jev_choice']]
    lines += ['## 1. Jev against Claude on every message (shadow run)', '',
              'Claude triaged every message as before; Jev answered the same message independently. Agreement compares Jev\'s route with Claude\'s route for the current case issue.', '',
              '| Jev\'s own decision | Messages | Same route as Claude |', '|---|---|---|']
    for mode, title in [('jev_only', 'Act alone (Claude skipped)'), ('jev_route', 'Route, Claude extracts'), ('claude', 'Hand off to Claude')]:
        group = [r for r in ref if r['proposed_mode'] == mode]
        route = (lambda r: r['jev_decided_route']) if mode != 'claude' else (lambda r: r['jev_choice'])
        lines.append(f"| {title} | {len(group)} | {_pct(sum(route(r) == r['claude_route'] for r in group), len(group))} |")
    lines.append(f"| **All** (Jev's raw choice) | {len(ref)} | {_pct(sum(r['jev_choice'] == r['claude_route'] for r in ref), len(ref))} |")
    acted = [r for r in ref if r['proposed_mode'] in {'jev_only', 'jev_route'}]
    alone = [r for r in shadow if r['proposed_mode'] == 'jev_only']
    lines += ['', f"Jev would have set the route itself for {_pct(len(acted), len(ref))} of messages and handed {_pct(len(ref) - len(acted), len(ref))} to Claude.",
              f"Of the messages Jev would have handled alone, Claude's reading raised a triage hold (ambiguity, hazard or conflict) on {_pct(sum(any(b.startswith('triage:') for b in r['blockers']) for r in alone), len(alone))}"
              f" and stated claims on {_pct(sum(r['claude_status'] == 'ok' and r.get('claude_claims', 0) > 0 for r in alone), len(alone))}; a Jev-only reading has neither, which is why its category always waits for a person.", '']
    reasons = Counter()
    for r in ref:
        if r['proposed_mode'] == 'claude':
            for reason in [x for x in r['jev_reasons'] or [] if not x.startswith('Shadow mode')]:
                reasons['unknown' if '"unknown"' in reason else 'low confidence' if 'below' in reason else 'several issues' if 'several' in reason else 'instructions to the system' if 'instructions' in reason else reason[:40]] += 1
    if reasons:
        lines += ['Hand-off reasons: ' + ', '.join(f'{k} {v}' for k, v in reasons.most_common()) + '.', '']
    hazards = [r for r in ref if r['claude_route'] == 'urgent_hazard']
    escalated = [r for r in ref if r['jev_decided_route'] == 'urgent_hazard']
    lines += [f"**Hazards:** Claude read {len(hazards)} message(s) as a possible urgent hazard; Jev escalated {sum(r['jev_decided_route'] == 'urgent_hazard' for r in hazards)} of them and handed "
              f"{sum(r['proposed_mode'] == 'claude' for r in hazards)} to Claude. Jev escalated {len(escalated)} message(s) in total "
              f"({sum(r['claude_route'] != 'urgent_hazard' for r in escalated)} that Claude did not read as a hazard; each goes to a person either way).", '']
    probed = [r for r in shadow if r['jev_reverse_choice']]
    lines += [f"**Option order:** with the route options reversed, Jev chose the same route for {_pct(sum(r['jev_reverse_choice'] == r['jev_choice'] for r in probed), len(probed))} of messages.", '']
    confusion = Counter((r['claude_route'], r['jev_choice']) for r in ref if r['claude_route'] != r['jev_choice'])
    if confusion:
        lines += ['Most frequent differences (Claude → Jev): ' + ', '.join(f'{c} → {j} ×{n}' for (c, j), n in confusion.most_common(8)) + '.', '']

    # Jev run: production configuration end to end.
    lines += ['## 2. End to end with Jev routing and hand-off (jev run)', '',
              '| Path | Messages | Median seconds per message |', '|---|---|---|']
    for mode, title in [('jev_only', 'Jev only (no Claude call)'), ('jev_route', 'Jev route + Claude extraction'), ('claude', 'Handed off to Claude')]:
        group = [r for r in live if r['router_mode'] == mode]
        lines.append(f"| {title} | {len(group)} | {statistics.median([r['seconds'] for r in group]):.1f} |" if group else f'| {title} | 0 | – |')
    lines.append(f"| Shadow run (Claude on every message) | {len(shadow)} | {statistics.median([r['seconds'] for r in shadow]):.1f} |" if shadow else '')
    conflicts = [r for r in live if r['route_disagreement']]
    extracted = [r for r in live if r['router_mode'] == 'jev_route' and r['claude_status'] == 'ok']
    lines += ['', f"- Claude was called for {_pct(sum(r['claude_called'] for r in live), len(live))} of messages (shadow run: {_pct(sum(r['claude_called'] for r in shadow), len(shadow))}).",
              f"- Where Jev set the route and Claude extracted, Claude objected or chose a different route for {_pct(len(conflicts), len(extracted))} of messages. Each objection is a CONFLICT held for the case manager.",
              f"- Anchoring check: where Claude extracted under Jev's route without objecting, the independent shadow reading of the same message chose a different route for "
              f"{_pct(sum(by_key.get((r['case'], r['event']), {}).get('claude_route') not in {None, r['final_route']} for r in extracted if not r['route_disagreement']), sum(1 for r in extracted if not r['route_disagreement']))}.",
              f"- Jev-only messages on an existing case that kept the current route (no change): {_pct(sum(r['event'] > 1 for r in live if r['router_mode'] == 'jev_only'), sum(r['router_mode'] == 'jev_only' for r in live))}.",
              f"- Final route matches the shadow run's route for the same message: {_pct(sum(by_key.get((r['case'], r['event']), {}).get('final_route') == r['final_route'] for r in live), len(live))}; "
              f"policy outcome matches: {_pct(sum(by_key.get((r['case'], r['event']), {}).get('outcome') == r['outcome'] for r in live), len(live))}. Later messages can differ because the case history diverges.",
              f"- Outcomes (jev run): " + ', '.join(f'{k} {v}' for k, v in Counter(r['outcome'] for r in live).most_common()) + '.',
              f"- Outcomes (shadow run): " + ', '.join(f'{k} {v}' for k, v in Counter(r['outcome'] for r in shadow).most_common()) + '.', '']
    jev_lat = [r['jev_latency_ms'] for r in rows if r['jev_latency_ms']]
    t_live, t_shadow = _tokens(live), _tokens(shadow)
    lines += ['## 3. Cost and latency', '', '| | Shadow (Claude on every message) | Jev run |', '|---|---|---|',
              f"| Claude calls | {sum(r['claude_called'] for r in shadow)} | {sum(r['claude_called'] for r in live)} |",
              f"| Claude input tokens (uncached + cache read + cache write) | {t_shadow['input_tokens']:,} + {t_shadow['cache_read_input_tokens']:,} + {t_shadow['cache_creation_input_tokens']:,} | {t_live['input_tokens']:,} + {t_live['cache_read_input_tokens']:,} + {t_live['cache_creation_input_tokens']:,} |",
              f"| Claude output tokens | {t_shadow['output_tokens']:,} | {t_live['output_tokens']:,} |",
              f"| Jev input tokens | – | {sum(r['jev_input_tokens'] for r in live):,} |", '',
              f"Jev request latency: median {statistics.median(jev_lat):.0f} ms, p90 {sorted(jev_lat)[int(0.9 * (len(jev_lat) - 1))]:.0f} ms over {len(jev_lat)} calls." if jev_lat else 'No Jev latency recorded.', '']
    errors = Counter(r['jev_error'] for r in rows if r['jev_error'])
    if errors:
        lines += ['Jev errors (handed to Claude): ' + ', '.join(f'{k} {v}' for k, v in errors.items()) + '.', '']
    return '\n'.join(line for line in lines if line is not None) + '\n'


def main():
    from .localenv import load_local_env
    load_local_env()
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument('--case', action='append', choices=sorted(ALLOWED), help='Repeat to select cases; default all 25')
    parser.add_argument('--events', type=int, default=8)
    parser.add_argument('--workers', type=int, default=8)
    parser.add_argument('--output', type=Path, default=Path('var/evals/router-eval.json'))
    parser.add_argument('--summary', type=Path)
    parser.add_argument('--from-json', type=Path, help='Re-summarise an earlier raw report without calling any model')
    args = parser.parse_args()
    if args.from_json:
        report = json.loads(args.from_json.read_text())
    else:
        if not (jev.configured() and ai.configured()):
            parser.error('Both TYPESAFE_API_KEY and ANTHROPIC_API_KEY are needed (environment or .env.local)')
        report = evaluate(args.case or sorted(ALLOWED), args.events, args.workers)
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_text(json.dumps(report, indent=1) + '\n')
        print(args.output.resolve())
    summary = summarise(report)
    if args.summary:
        args.summary.parent.mkdir(parents=True, exist_ok=True)
        args.summary.write_text(summary)
        print(args.summary.resolve())
    else:
        print(summary)


if __name__ == '__main__':
    main()
