"""Readable per-case Reality Test answers rendered from the recorded run evidence.

Pure formatting over `input.json`, `evidence.json` and `result.json`: it adds no
judgement, fills no gaps and never upgrades a failed or partial run. Writes:

- `ANSWER.md`    what the system received, decided, did, escalated and failed
- `REASONING.md` policy blockers, recorded claims and every model reading, with
                 references back to the input event or attachment
- `AUDIT.md`     the chronological audit trail (`app.audit.render`) per system case
- `records.jsonl` every immutable record of every system case

Re-render an existing run directory: `python -m app.answer_export <run_dir>`.
"""
from __future__ import annotations

import json
import os
from pathlib import Path

from .audit import render as audit_render

SIMULATED = ('All operational tools in this run are clearly labelled **simulated** adapters: no real tenant, landlord '
             'or contractor was contacted, nothing was paid or booked, and a simulated receipt does not prove work happened.')


def load(path, default=None):
    path = Path(path)
    return json.loads(path.read_text()) if path.exists() else default


def clip(text, limit=400):
    text = ' '.join((text or '').split())
    return text if len(text) <= limit else text[:limit].rstrip() + ' …'


def cell(text):
    return clip(text, 220).replace('|', '\\|')


def labels(detail):
    """Map application source IDs to the label the input gave them (event number / attachment)."""
    return {e['id']: e.get('source_label') or 'source' for e in detail.get('evidence', [])}


def ref(source_ids, names):
    return ', '.join(names.get(s, s[:8]) for s in source_ids or []) or 'no source recorded'


def latest_reviews(detail):
    """Open human reviews, newest per blocker key."""
    current = {}
    for review in detail.get('reviews', []):
        if review.get('status') in {'open', 'deferred'}:
            current[review['key']] = review
    return list(current.values())


def readings(detail):
    routes = {r['payload'].get('source_id'): r['payload'] for r in detail['timeline'] if r['kind'] == 'routing'}
    for row in detail['timeline']:
        if row['kind'] == 'interpretation':
            yield row['payload'], routes.get(row['payload'].get('source_id'))


def failures_of(detail):
    out = []
    for row in detail['timeline']:
        p = row['payload']
        if row['kind'] == 'interpretation' and p.get('status') == 'failed':
            out.append(f"Model reading failed ({p.get('error_type', 'unknown')}) for source {p.get('source_id', '')[:8]}; the case waits for a person.")
        elif row['kind'] == 'tenant_message' and p.get('status') == 'draft_failed':
            out.append(f"Message draft failed ({p.get('error_type', 'unknown')}).")
        elif row['kind'] == 'routing' and p.get('error_type'):
            out.append(f"Jev routing unavailable ({p['error_type']}); the product handed the message to Claude.")
        elif row['kind'] == 'workflow_error':
            out.append(f"Workflow transport error: {clip(json.dumps(p), 200)}")
        elif row['kind'] == 'action' and p.get('status') in {'failed', 'uncertain'}:
            out.append(f"Simulated action `{p['scope'].get('action')}` ended {p['status']}.")
    return out


def answer_case(detail, names):
    case, decision, triage = detail['case'], detail.get('decision') or {}, detail['case'].get('triage') or {}
    proposal = case.get('proposal') or {}
    lines = [f"## Final decision — system case `{case['id'][:12]}`", '',
             f"- **Decision (policy outcome):** **{decision.get('outcome', 'not assessed')}**",
             f"- **Proposed next action:** `{proposal.get('action', 'none')}` — {proposal.get('work_item') or 'no work item'}"
             + (f" (category {case['category']})" if case.get('category') else ''),
             f"- **Next step:** {decision.get('next_step') or case.get('next_step') or 'none recorded'}",
             f"- **Owner:** {(decision.get('owner') or case.get('owner') or 'unassigned').replace('_', ' ')}",
             f"- **Case state:** {case['status']} · policy v{decision.get('policy_version', '?')}"]
    if case.get('parent_case_id'):
        lines.append(f"- **Split from system case** `{case['parent_case_id'][:12]}` as a separate issue.")
    if triage.get('summary'):
        lines += ['', f"**Latest reading ({triage.get('model', 'model')}, {triage.get('confidence', '?')} confidence, route `{triage.get('route')}`):** {triage['summary']}"]
        if triage.get('rationale'):
            lines.append(f"\n**Why:** {triage['rationale']}")

    lines += ['', '### Actions taken', '']
    acted = False
    for action in detail.get('actions', []):
        if action.get('status') == 'intent':
            continue
        acted = True
        scope = action.get('scope') or {}
        lines.append(f"- `{scope.get('action')}` → **{action['status']}** via {scope.get('provider')} "
                     f"({'simulated adapter' if action.get('simulated', True) else 'adapter'}) — {scope.get('work_item')}")
    for message in detail.get('tenant_messages', []):
        acted = True
        to = (message.get('recipient') or {}).get('kind', 'tenant')
        state = message.get('status')
        lines.append(f"- Drafted message to {to}: **{state}** (simulated channel; not sent to a real person)"
                     + (f" — “{clip(message.get('text'), 300)}”" if message.get('text') else ''))
    for question in detail.get('questions', []):
        acted = True
        lines.append(f"- Clarification `{question.get('key')}` to {question.get('addressee') or 'staff'}: {question.get('status', 'open')} — {clip(question.get('question'), 250)}")
    if not acted:
        lines.append('- **No operational action was executed.** Nothing was booked, instructed, paid or sent. '
                     'The system recorded readings, claims and policy assessments only.')

    reviews = latest_reviews(detail)
    lines += ['', '### Escalated to a person (handover)', '']
    if reviews:
        lines.append('| Check | Owner | Rule | What the person must resolve | Evidence |')
        lines.append('|---|---|---|---|---|')
        for r in reviews:
            lines.append(f"| `{r['key']}` | {r['owner'].replace('_', ' ')} | `{r.get('rule_id')}` | {cell(r.get('question'))} | {cell(ref(r.get('source_ids'), names))} |")
    else:
        lines.append('- No open human review.')

    unknowns = [a for a in triage.get('open_ambiguities', [])] + [a for a in triage.get('other_ambiguities', [])]
    lines += ['', '### Missing information and conflicting facts', '']
    if unknowns:
        for a in unknowns:
            lines.append(f"- **{a.get('topic', 'unknown')}**{' (blocks the route)' if a.get('affects_route') else ''}: {a['description']}")
    else:
        lines.append('- None recorded by the latest reading.')
    if triage.get('disagreement'):
        lines.append(f"- Router/model disagreement recorded: {clip(json.dumps(triage['disagreement']), 300)}")
    unverified = [c for c in detail.get('claims', []) if not c.get('verified')]
    if unverified:
        lines.append(f"- {len(unverified)} extracted claim(s) remain **unverified source assertions** (see REASONING.md); none was treated as verified authority.")
    return lines


def write_answers(case_id, case_dir, provenance, config, result, track=None):
    case_dir = Path(case_dir)
    track = track or os.getenv('REALITY_TRACK') or 'Reality Test'
    try:
        data = load(case_dir / 'input.json', {})
    except ValueError:  # Malformed input is preserved as-is and reported as a failed case.
        data = {}
    if not isinstance(data, dict):
        data = {}
    evidence = load(case_dir / 'evidence.json', {'cases': []})
    label = 'OFFICIAL RUN' if config.mode == 'official' else 'PREPARATION ONLY — not official Reality Test results'
    details = evidence.get('cases', [])

    answer = [f"# {track} — case {case_id}: {data.get('title', 'untitled')}", '',
              f"*{label}. System-generated; not edited by hand.*", '',
              f"- **Property (as supplied, unverified):** {data.get('property_ref', 'unknown')}",
              f"- **Decision cutoff:** {data.get('as_of', 'unknown')}",
              f"- **Runner status:** **{result.get('status')}** · execution `{result.get('execution', 'unknown')}` · "
              f"sources processed {result.get('sources_processed', 0)} of {1 + len(data.get('evidence', []))}",
              f"- **Models:** Claude `{config.model}` (triage effort {config.triage_effort}); Jev `{config.jev_model}` routing",
              f"- **Commit:** `{provenance.get('git_commit', 'unknown')}` · input SHA-256 `{provenance.get('input_sha256', 'unknown')[:16]}…`", '',
              SIMULATED, '']

    answer += ['## What the system received', '',
               f"The initial report and {len(data.get('evidence', []))} further sources, submitted one at a time in availability order; "
               'each was processed and settled before the next became visible. Full text: `input.json`.', '',
               '| # | Available at | Source |', '|---|---|---|',
               f"| 0 | {data.get('report_available_at', '?')} | Initial report — {cell(data.get('report', '').splitlines()[0] if data.get('report') else '')} |"]
    for n, source in enumerate(data.get('evidence', []), 1):
        answer.append(f"| {n} | {source['available_at']} | {cell(source['source_label'])} |")
    answer.append('')

    if not details:
        answer += ['## Final decision', '', '**No decision was produced.** No application case evidence was produced for this input.', '']
    for detail in details:
        answer += answer_case(detail, labels(detail)) + ['']

    failures = [f for d in details for f in failures_of(d)]
    if result.get('error'):
        failures.insert(0, f"Runner: {result['error']}")
    if result.get('status') not in {'settled'}:
        failures.append(f"The run did not settle cleanly (status `{result.get('status')}`); any recorded state is partial.")
    if result.get('routing_fallback_count'):
        failures.append(f"Jev was unavailable for {result['routing_fallback_count']} recorded routing attempts; the product handed those messages "
                        f"to Claude. Recorded causes: {', '.join(result.get('routing_fallback_errors', []))}.")
    answer += ['## Failures', ''] + ([f"- {f}" for f in failures] or ['- None recorded. (Jev and Claude calls all returned; no workflow step failed.)']) + ['']
    answer += ['## Result', '',
               'No approval was invented and no human response was supplied by the runner. '
               + ('The case is waiting on the person(s) listed in the handover above.' if any(latest_reviews(d) for d in details)
                  else 'See the decision above for the recorded end state.'), '',
               'Trace: `REASONING.md` (why) · `AUDIT.md` (every step, actor and tool) · `evidence.json` / `records.jsonl` (raw records) · '
               '`checkpoint-NNN.json` (state after each source) · `worker.log`.', '']

    reasoning = [f"# Reasoning — {track} case {case_id}", '',
                 'Exported from the system\'s recorded policy assessments, claims and concise model rationales. '
                 'It is not reconstructed after the fact and does not contain hidden chain-of-thought.', '']
    for detail in details:
        names, decision = labels(detail), detail.get('decision') or {}
        reasoning += [f"## System case `{detail['case']['id'][:12]}` — {decision.get('outcome', 'not assessed')}", '',
                      '### Why this decision (policy gates)', '',
                      'The model cannot create authority: the policy engine decides from recorded checks. Each blocker below kept the action from running.', '']
        for b in decision.get('blockers', []):
            reasoning.append(f"- `{b['key']}` is **{b['status']}** → {b['response']} (rule `{b.get('rule_id')}`, owner {b.get('owner', '').replace('_', ' ')}): "
                             f"{b['reason']} — evidence: {ref(b.get('source_ids'), names)}")
        if not decision.get('blockers'):
            reasoning.append('- No blockers recorded.')
        reasoning += ['', '### Claims extracted from the sources', '',
                      'Every claim is a source assertion with an exact quote; unverified claims were never used as authority.', '']
        for c in detail.get('claims', []):
            status = 'verified' if c.get('verified') else ('hearsay' if c.get('hearsay') else 'unverified assertion')
            reasoning.append(f"- `{c['key']}` = {json.dumps(c.get('value'))} — {status}; from {names.get(c.get('source_id'), 'unknown source')}: "
                             f"“{clip(c.get('source_quote'), 220)}”")
        if not detail.get('claims'):
            reasoning.append('- None.')
        reasoning += ['', '### Reading of each source (Jev route → Claude reading)', '']
        for p, route in readings(detail):
            source = names.get(p.get('source_id'), 'source')
            jev = ''
            if route:
                d = route.get('decision') or {}
                jev = (f"Recorded router fallback: {route['error_type']}; handed to Claude" if route.get('error_type')
                       else f"Jev `{route.get('mode')}`" + (f" → `{route['route']}`" if route.get('route') else '')
                       + (f" — {' '.join(d.get('reasons', []))}" if d.get('reasons') else ''))
            if p.get('status') == 'failed':
                reasoning += [f"**{source}** — {jev}. **Reading failed:** {p.get('error_type')}.", '']
                continue
            res = p.get('result') or {}
            issues = res.get('issues', [])
            primary = next((i for i in issues if i.get('relation') == 'current_case'), issues[0] if issues else {})
            who = 'Jev only' if p.get('provider') == 'typesafe' else p.get('model', 'Claude')
            reasoning.append(f"**{source}** — {jev}. {who}: {res.get('intent', '?')}, route `{primary.get('route', 'none')}`, {res.get('confidence', '?')} confidence.")
            reasoning.append(f"{res.get('summary', '')}" + (f" *Why:* {res['rationale']}" if res.get('rationale') and p.get('provider') != 'typesafe' else ''))
            for a in res.get('ambiguities', []):
                reasoning.append(f"- Unknown{' (affects route)' if a.get('affects_route') else ''}: {a['description']}")
            if res.get('risk_flags'):
                reasoning.append(f"- Risk flags: {', '.join(res['risk_flags'])}")
            if (res.get('route_objection') or '').strip():
                reasoning.append(f"- Objected to Jev's route: {res['route_objection']}")
            reasoning.append('')
    if not details:
        reasoning += ['No application records were produced; see `result.json` and `worker.log`.', '']
    failures and reasoning.extend(['## Failures and uncertainties', ''] + [f"- {f}" for f in failures] + [''])

    from .reality_test import atomic_text
    atomic_text(case_dir / 'ANSWER.md', '\n'.join(answer))
    atomic_text(case_dir / 'REASONING.md', '\n'.join(reasoning))
    audit = [audit_render(d).replace('(records.jsonl)', '(records.jsonl)') for d in details]
    atomic_text(case_dir / 'AUDIT.md', '\n\n---\n\n'.join(audit) if audit else '# Audit trail\n\nNo application records.\n')
    atomic_text(case_dir / 'records.jsonl', ''.join(json.dumps(r, sort_keys=True) + '\n' for d in details for r in d['timeline']))


def main():
    import argparse
    from .reality_test import RunnerConfig
    parser = argparse.ArgumentParser(description='Re-render ANSWER.md / REASONING.md / AUDIT.md for a finished run directory.')
    parser.add_argument('run_dir', type=Path)
    args = parser.parse_args()
    config = RunnerConfig.model_validate(load(args.run_dir / 'config.json'))
    for case_dir in sorted((args.run_dir / 'ANSWERS').iterdir()):
        write_answers(case_dir.name, case_dir, load(case_dir / 'provenance.json', {}), config, load(case_dir / 'result.json', {}))
        print(case_dir / 'ANSWER.md')


if __name__ == '__main__':
    main()
