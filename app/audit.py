"""Per-case audit trail: who decided what, and which tool ran, rendered from the immutable records.

The records table is the source of truth; this module only reads it. Each case
gets `.audit/<case_id>/history.md` (human trace) and `records.jsonl` (every raw
record). Internal bookkeeping (outbox signals, cycle checkpoints, intake
receipts) is left out of the markdown, and a policy assessment is shown only
when its outcome or blockers changed.
"""
from __future__ import annotations
import json, logging, os
from pathlib import Path

log = logging.getLogger(__name__)
ROOT = Path(__file__).resolve().parent.parent

SKIP = {'signal_outbox', 'cycle_checkpoint', 'intake_receipt'}
# Events whose detail is not in a dedicated record kind.
EVENTS = {'proposal_changed': 'Staff changed the proposed action', 'explicit_reassessment': 'Reassessment requested',
          'policy_published': 'New policy version published', 'self_identification_corrected': 'Tenant corrected their name or address',
          'simulated_result_reconciled': 'Uncertain action reconciled'}
STEP = {'routing': 'route_case_messages', 'interpretation': 'triage_case_messages', 'tenant_message': 'compose_tenant_messages'}
SYSTEM = {'claude': 'Claude', 'jev': 'Jev', 'native-case-coordinator': 'Case coordinator (workflow)', 'demo-setup': 'Demo setup',
          'build-replay': 'BUILD replay', 'voice-bridge': 'Voice bridge'}


def who(actor):
    if not actor: return 'System'
    name = SYSTEM.get(actor.get('id'))
    if name: return name
    return f"{actor.get('id')} ({str(actor.get('role', '')).replace('_', ' ')})"


def when(stamp):
    return stamp[:19].replace('T', ' ') + ' UTC'


def quote(text, limit=800):
    text = (text or '').strip()
    if len(text) > limit: text = text[:limit].rstrip() + ' …'
    return '\n'.join('> ' + line if line else '>' for line in text.splitlines())


def model_line(p):
    """Model, provider and token use from a model-call record."""
    bits = [p.get('model') or p.get('requested_model') or 'model not recorded']
    usage = p.get('usage') or {}
    if usage.get('input_tokens') is not None: bits.append(f"{usage['input_tokens']} in / {usage.get('output_tokens', 0)} out tokens")
    if p.get('latency_ms') is not None: bits.append(f"{p['latency_ms']} ms")
    return ' · '.join(str(b) for b in bits)


def count(n, word):
    if n == 1: return f"1 {word}"
    return f"{n} {word[:-1]}ies" if word.endswith('y') else f"{n} {word}s"


def blockers_text(blockers):
    return '; '.join(f"`{b['key']}` {b['status']} → {b['response']}" for b in blockers) or 'none'


class Trail:
    def __init__(self, timeline):
        self.timeline = timeline
        self.by_id = {r['id']: r for r in timeline}
        self.last_decision = None

    def entry(self, r):
        """One record as (title, bullets, quoted text), or None when it adds nothing."""
        kind, p = r['kind'], r['payload']
        handler = getattr(self, 'k_' + kind, None)
        if handler: return handler(p)
        if kind in SKIP: return None
        return kind.replace('_', ' ').capitalize(), [f"**Actor:** {who(p.get('actor'))}"] if p.get('actor') else [], None

    # ---- Messages in and model readings
    def k_evidence(self, p):
        party = p.get('party') or {}
        bullets = [f"**Recorded by:** {who(p.get('actor'))}"]
        if party: bullets.append(f"**Sender:** {party.get('kind')} {party.get('name') or ''} ({'directory match' if party.get('verified') else 'not verified'})".replace('  ', ' '))
        bullets.append({'pending': '**Reading:** queued for Jev routing / Claude triage', 'staff_structured': '**Reading:** structured by staff (no model)',
                        'not_required': '**Reading:** not required'}.get(p.get('triage'), f"**Reading:** {p.get('triage')}"))
        return f"Message received: {p['source_label']}", bullets, p.get('text')

    def k_inbound_call(self, p):
        party = p.get('party') or {}
        return f"Inbound {p['channel']} ({p['intent'].replace('_', ' ')})", [
            f"**Actor:** Voice bridge → {party.get('kind')} {party.get('name') or '(unknown)'}",
            f"**Tool:** `POST /api/inbound` (deterministic, no model)", f"**Outcome:** {p['outcome'].replace('_', ' ')}"], None

    def k_routing(self, p):
        d = p.get('decision') or {}
        if p.get('error_type'):
            return 'Jev unavailable → handed to Claude', [f"**Actor:** Jev ({p.get('requested_model')})", f"**Tool:** TypeSafe `system_one` · step `{STEP['routing']}`",
                                                          f"**Error:** {p['error_type']}", f"**Why:** {' '.join(d.get('reasons', []))}"], None
        if not p.get('answers'):
            return 'Jev skipped → Claude reads', ['**Actor:** Workflow (staff already set the route)', f"**Why:** {' '.join(d.get('reasons', []))}"], None
        route = f"`{p['route']}` (confidence {d.get('route_confidence', 0):.2f})" if p.get('route') else 'no route'
        signals = ' · '.join(f"{k} {v:.2f}" for k, v in (d.get('signals') or {}).items())
        bullets = [f"**Actor:** Jev ({model_line(p)})", f"**Tool:** TypeSafe `system_one` · step `{STEP['routing']}`",
                   f"**Decision:** {p['mode']} → {route}"]
        if p.get('proposed_mode') != p['mode']: bullets.append(f"**Jev proposed:** {p['proposed_mode']} (router mode `{p.get('router')}` overrides)")
        if signals: bullets.append(f"**Signals:** {signals}")
        bullets.append(f"**Why:** {' '.join(d.get('reasons', []))}")
        return 'Jev routed the message', bullets, None

    def k_interpretation(self, p):
        jev_only = p.get('provider') == 'typesafe'
        actor = f"Jev ({model_line(p)})" if jev_only else f"Claude ({model_line(p)})"
        tool = 'Jev decision applied, no generated text' if jev_only else f"Anthropic Messages API `ai.triage` (prompt {p.get('prompt_version', 'n/a')}) · step `{STEP['interpretation']}`"
        if p.get('status') == 'failed':
            return 'Claude reading failed', [f"**Actor:** {actor}", f"**Tool:** {tool}", f"**Error:** {p.get('error_type')} — the case waits for a person"], None
        res = p['result']; issues = res.get('issues', [])
        primary = next((i for i in issues if i['relation'] == 'current_case'), issues[0] if issues else None)
        bullets = [f"**Actor:** {actor}", f"**Tool:** {tool}",
                   f"**Reading:** {res['intent'].replace('_', ' ')} · route `{primary['route'] if primary else 'none'}` · {res['confidence']} confidence"]
        if primary: bullets.append(f"**Work item:** {primary['work_item']} ({primary['category']})")
        bullets.append(f"**Summary:** {res['summary']}")
        if res.get('rationale') and not jev_only: bullets.append(f"**Rationale:** {res['rationale']}")
        extracted = [count(len(res.get('claims', [])), 'claim'), count(len(res.get('ambiguities', [])), 'ambiguity'), count(len(issues), 'issue')]
        if res.get('risk_flags'): extracted.append('risk flags: ' + ', '.join(res['risk_flags']))
        bullets.append('**Extracted:** ' + ' · '.join(extracted))
        for a in res.get('ambiguities', []): bullets.append(f"**Unknown{' (affects route)' if a.get('affects_route') else ''}:** {a['description']}")
        if (res.get('route_objection') or '').strip(): bullets.append(f"**Objected to Jev's route:** {res['route_objection']}")
        return ('Jev-only reading applied' if jev_only else 'Claude read the message'), bullets, None

    def k_route_changed(self, p):
        return f"Proposed action → `{p['action']}`", [f"**Actor:** Triage reading (route `{p['route']}`)", f"**Work item:** {p['work_item']}",
                                                      f"**Action revision:** {p['action_revision']}"], None

    def k_issue_split(self, p):
        return 'Separate issue split into a new case', ['**Actor:** Claude', f"**Issue:** #{p['issue_index'] + 1} of the message"], None

    # ---- Facts
    def k_claim(self, p):
        value = p['value']
        if p['key'] == 'classification': value = p['scope'].get('category')
        if p.get('verified_by'): actor = f"Verified by {who(p['verified_by'])}"
        elif p.get('origin') == 'claude': actor = 'Claude (extracted)'
        else: actor = who((self.by_id.get(p.get('source_id')) or {}).get('payload', {}).get('actor'))
        if p.get('hearsay'): status = f"hearsay from {p.get('party')} — kept, never counts for a check"
        elif p.get('verified'): status = 'verified' + (f" — {p['verification']}" if p.get('verification') else '')
        else: status = 'unverified assertion — a person or policy must accept it'
        bullets = [f"**Actor:** {actor}", f"**Status:** {status}"]
        if p.get('supersedes'): bullets.append(f"**Supersedes:** {len(p['supersedes'])} earlier claim(s)")
        if p.get('expires_at'): bullets.append(f"**Expires:** {when(p['expires_at'])}")
        source_text = (self.by_id.get(p.get('source_id')) or {}).get('payload', {}).get('text')
        return f"Claim `{p['key']}` = {json.dumps(value)}", bullets, p['source_quote'] if p.get('source_quote') != source_text else None

    # ---- Policy gates and people
    def k_decision(self, p):
        signature = (p['outcome'], p.get('policy_version'), p.get('action_revision'), tuple((b['key'], b['status'], b['response']) for b in p['blockers']))
        if signature == self.last_decision: return None
        self.last_decision = signature
        bullets = [f"**Actor:** Policy engine (rules v{p.get('policy_version')}, `domain.evaluate`)", f"**Outcome:** {p['outcome']} · owner {p.get('owner', '').replace('_', ' ')}"]
        if p['blockers']: bullets.append('**Blockers:** ' + blockers_text(p['blockers']))
        bullets.append(f"**Next step:** {p['next_step']}")
        return f"Policy gates → {p['outcome']}", bullets, None

    def k_question(self, p):
        to = p.get('addressee') or 'staff'
        return f"Clarification opened: `{p['key']}` → {to}", ['**Actor:** Policy engine', f"**Owner:** {p['owner'].replace('_', ' ')}",
                                                              f"**Deadline:** {when(p['deadline'])}"], p['question']

    def k_simulated_clarification(self, p):
        return 'Clarification sent to staff (simulated)', ['**Tool:** simulated staff channel — no real contact'], None

    def k_question_closed(self, p):
        return 'Question closed' + (' (answered)' if p.get('answered') else ''), [f"**Why:** {p['reason']}"], None

    def k_question_followup(self, p):
        return 'Partial answer → narrower follow-up due', ['**Actor:** Claude (reading)'], p.get('source_quote')

    def k_question_escalated(self, p):
        return 'Question escalated', [f"**Owner:** {p['owner'].replace('_', ' ')}", f"**Why:** {p['reason']}"], None

    def k_reminder(self, p):
        return f"Reminder #{p['number']} sent (simulated)", ['**Actor:** Case coordinator (workflow)', '**Tool:** simulated reminder — no real contact'], None

    def k_review(self, p):
        return f"Human review opened: `{p['key']}`", ['**Actor:** Policy engine', f"**Owner:** {p['owner'].replace('_', ' ')} · rule `{p['rule_id']}`",
                                                       f"**Expires:** {when(p['expires_at'])}"], p['question']

    def k_review_response(self, p):
        bullets = [f"**Actor:** {who(p.get('actor'))}", f"**Decision:** {p['decision']}"]
        if p.get('reason'): bullets.append(f"**Reason:** {p['reason']}")
        return f"Review answered: {p['decision']}", bullets, None

    def k_rejected_review_response(self, p):
        return 'Late or duplicate review response ignored', [f"**Actor:** {who(p.get('actor'))}", f"**Why:** {p['reason']}"], None

    def k_review_superseded(self, p):
        return 'Review superseded', [f"**Why:** {p['reason']}"], None

    def k_review_overdue(self, p):
        return 'Review overdue', [f"**Escalated to:** {p['owner']}", f"**Why:** {p['reason']}"], None

    def k_approval(self, p):
        return f"Approval granted: `{p['key']}`", [f"**Actor:** {who(p.get('actor'))}", f"**Expires:** {when(p['expires_at'])}", f"**Reason:** {p['reason']}"], None

    def k_approval_revoked(self, p):
        return 'Approval revoked', [f"**Actor:** {who(p.get('actor'))}"], None

    def k_action_rejected(self, p):
        return f"Action `{p['scope'].get('action')}` rejected", [f"**Actor:** {who(p.get('actor'))}", f"**Reason:** {p['reason']}"], None

    def k_triage_confirmed(self, p):
        return 'Reading confirmed by staff', [f"**Actor:** {who(p.get('actor'))}", f"**Reason:** {p.get('reason')}"], None

    def k_triage_retry(self, p):
        return 'Reading retried', [f"**Actor:** {who(p.get('actor'))}"], None

    def k_human_evidence_request(self, p):
        return 'More evidence requested (simulated)', [f"**Actor:** {who(p.get('actor'))}", f"**Reason:** {p['reason']}"], None

    def k_policy_reassessment(self, p):
        return f"Reassessed under policy v{p['policy_version']}", [], None

    def k_incoming_event(self, p):
        title = EVENTS.get(p['event_type'])
        if not title: return None
        data = p.get('data') or {}
        bullets = [f"**Actor:** {who(p.get('actor'))}"]
        if p['event_type'] == 'proposal_changed': bullets.append(f"**Proposal:** `{data.get('action')}` · {data.get('work_item')}" + (f" · category {data['category']}" if data.get('category') else ''))
        if p['event_type'] == 'policy_published': bullets.append(f"**Version:** {data.get('version')}")
        return title, bullets, None

    # ---- Outbound tools (all simulated)
    def k_tenant_message(self, p):
        to = (p.get('recipient') or {}).get('kind', 'tenant')
        fn = 'draft_tenant_message' if to == 'tenant' else 'draft_party_message'
        bullets = [f"**Actor:** Claude ({model_line(p)})", f"**Tool:** Anthropic Messages API `ai.{fn}` · step `{STEP['tenant_message']}`"]
        if p['status'] == 'draft_failed':
            return f"Draft to {to} failed", bullets + [f"**Error:** {p.get('error_type')} — staff write or reject it"], None
        claude = p.get('claude') or {}
        bullets.append(f"**Claude's call:** {claude.get('send_decision')} — {claude.get('decision_reason')}")
        gate = p.get('gate') or {}
        bullets.append('**Send gate:** auto-send allowed' if gate.get('auto_send') else '**Send gate:** held for staff — ' + ' '.join(gate.get('reasons', [])))
        bullets.append(f"**Topics:** {', '.join(p.get('topics', []))}")
        return f"Claude drafted a message to the {to}", bullets, p.get('text')

    def k_tenant_message_sent(self, p):
        to = p.get('recipient') or {}
        bullets = [f"**Actor:** {who(p.get('actor'))}", f"**Tool:** `{p['channel']}` adapter — {p.get('label')}"]
        if p.get('edited'): bullets.append('**Edited by staff before sending**')
        return f"Message sent to {to.get('kind', 'tenant')} {to.get('name') or ''}".rstrip(), bullets, p['text'] if p.get('edited') else None

    def k_tenant_message_rejected(self, p):
        return 'Draft rejected' + (' (redraft requested)' if p.get('redraft') else ''), [f"**Actor:** {who(p.get('actor'))}", f"**Reason:** {p['reason']}"], None

    def k_simulated_provider_receipt(self, p):
        return None  # Shown on the action it confirms.

    def k_action(self, p):
        if p['status'] == 'intent': return None
        receipt = (self.by_id.get(p.get('receipt_id')) or {}).get('payload')
        bullets = [f"**Actor:** {who(p.get('reconciled_by') or p.get('actor'))}",
                   f"**Tool:** simulated provider adapter → {p['scope'].get('provider')} · " + (receipt['label'] if receipt else 'no receipt; reconcile before any retry'),
                   f"**Work item:** {p['scope'].get('work_item')}"]
        return f"Action `{p['scope'].get('action')}` {p['status']}", bullets, None


def render(detail):
    """Markdown audit trail for one case detail (as returned by Service.detail)."""
    case, timeline = detail['case'], detail['timeline']
    trail = Trail(timeline)
    entries = [(r, e) for r in timeline if (e := trail.entry(r))]
    head = [f"# Case {case['id'][:12]} audit trail", '',
            f"{case['title']} · {case['property_ref']} · status {case['status'].replace('_', ' ')} · stage {case.get('stage', 'unassessed')}", '',
            f"- **Case ID:** `{case['id']}`"]
    if case.get('parent_case_id'): head.append(f"- **Split from:** [{case['parent_case_id'][:12]}](../{case['parent_case_id']}/history.md)")
    head += [f"- **Entries:** {len(entries)} (from {len(timeline)} immutable records; bookkeeping and unchanged assessments omitted)",
             '- **Raw records:** [records.jsonl](records.jsonl)',
             '- All outbound tools are simulated adapters; no real tenant, landlord or contractor was contacted.']
    out = ['\n'.join(head)]
    for n, (r, (title, bullets, text)) in enumerate(entries, 1):
        block = [f'<a id="entry-{n:03d}"></a>', f"## {when(r['created_at'])} — {n:03d} · {title}"]
        if bullets: block += [''] + [f"- {b}" for b in bullets]
        if text: block += ['', quote(text)]
        out.append('\n'.join(block))
    return '\n\n'.join(out) + '\n'


def export(service, case_ids=None, directory=None):
    """Write `<directory>/<case_id>/history.md` and `records.jsonl`. Returns the written folders."""
    directory = Path(directory or os.getenv('AUDIT_DIR') or ROOT / '.audit')
    if case_ids is None:
        with service.db.tx() as c: case_ids = [x['id'] for x in service.db.case_list(c)]
    written = []
    for cid in case_ids:
        detail = service.detail(cid)
        folder = directory / cid
        folder.mkdir(parents=True, exist_ok=True)
        (folder / 'history.md').write_text(render(detail))
        (folder / 'records.jsonl').write_text(''.join(json.dumps(r, sort_keys=True) + '\n' for r in detail['timeline']))
        written.append(folder)
    return written


def auto_directory():
    """Local demo default: `.audit/` beside the default SQLite store. `AUDIT_DIR=off` disables it;
    a deployment (Vercel, or an explicit DATABASE_URL) writes nothing unless AUDIT_DIR is set."""
    value = os.getenv('AUDIT_DIR')
    if value == 'off': return None
    if value: return Path(value)
    if os.getenv('VERCEL') or os.getenv('DATABASE_URL'): return None
    return ROOT / '.audit'


def exporter(service, directory):
    """An after-commit hook for Store: refresh the trail of every case a transaction touched."""
    def refresh(case_ids):
        try: export(service, sorted(case_ids), directory)
        except Exception as exc:  # The audit store is authoritative; a file write never fails a request.
            log.warning('Audit trail export skipped: %s', type(exc).__name__)
    return refresh


def main():
    import argparse
    from .localenv import load_local_env
    from .service import Service
    load_local_env()
    parser = argparse.ArgumentParser(description='Write the per-case audit trail (history.md + records.jsonl).')
    parser.add_argument('--case', action='append', help='Case id (repeatable); default: every case')
    parser.add_argument('--out', type=Path, help='Output directory (default: AUDIT_DIR or ./.audit)')
    args = parser.parse_args()
    for folder in export(Service(), args.case, args.out): print(folder / 'history.md')


if __name__ == '__main__': main()
