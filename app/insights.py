"""Read-only evidence, recorded playback and policy comparison projections.

These views never reassess a stored case, create a review or run a model. Playback
uses ledger receipt order, rather than the date a sender says an event happened.
"""
from __future__ import annotations

from copy import deepcopy
import json

from fastapi import APIRouter, Depends
from pydantic import Field

from .domain import ROLES, StrictModel, business_id, dt, evaluate, now, scope_matches, scope_of, stamp
from .service import get_service
from .store import payload


class PolicyComparisonInput(StrictModel):
    draft_id: str = Field(min_length=1, max_length=200)
    case_ids: list[str] | None = Field(default=None, max_length=200)


def _comparisons(case, claims, sources, at):
    """Compare only currently applicable assertions; keep other claims visible."""
    replacements = {
        old: claim['id']
        for claim in claims if claim.get('verified')
        for old in claim.get('supersedes', [])
    }
    groups = {}
    for claim in claims:
        matches = scope_matches(claim.get('scope', {}), case)
        # A broad property claim and a narrower job claim can concern the same
        # current action. Other jobs/properties remain separate groups.
        scope = scope_of(case) if matches else claim.get('scope', {})
        group_key = (claim['key'], matches, json.dumps(scope, sort_keys=True))
        group = groups.setdefault(group_key, {'key': claim['key'], 'scope': scope,
                                               'claims': [], 'applies_to_current_action': matches})
        source = sources.get(claim['source_id'], {})
        superseded_by = replacements.get(claim['id'])
        expired = bool(claim.get('expires_at') and dt(claim['expires_at']) <= at)
        applicability = ('SUPERSEDED' if superseded_by else 'OUT_OF_SCOPE' if not matches
                         else 'EXPIRED' if expired else 'HEARSAY' if claim.get('hearsay') else 'CURRENT')
        group['claims'].append({
            'id': claim['id'], 'source_id': claim['source_id'],
            'source_label': source.get('source_label', 'Source not recorded'),
            'source_quote': claim.get('source_quote', ''), 'value': claim['value'],
            'verified': bool(claim.get('verified')), 'scope': claim.get('scope', {}),
            'created_at': claim.get('created_at'), 'occurred_at': source.get('occurred_at'),
            # This is who submitted the source, not a verified original sender.
            'actor': source.get('actor'), 'actor_meaning': 'recorded source submitter',
            'party': source.get('party'), 'hearsay': bool(claim.get('hearsay')),
            'applicability': applicability, 'superseded_by': superseded_by,
            'expires_at': claim.get('expires_at'),
            'verification': claim.get('verification'), 'verified_by': claim.get('verified_by'),
        })

    for group in groups.values():
        current = [c for c in group['claims'] if c['applicability'] == 'CURRENT']
        if not group['applies_to_current_action']:
            status, reason = 'OUT_OF_SCOPE', 'These claims do not match the current property, work item or action scope.'
        elif not current:
            statuses = {c['applicability'] for c in group['claims']}
            status = 'SUPERSEDED' if statuses == {'SUPERSEDED'} else 'EXPIRED' if statuses <= {'SUPERSEDED', 'EXPIRED'} else 'UNKNOWN'
            reason = 'No applicable current assertion remains. Superseded or expired claims and hearsay do not establish or contradict this fact.'
        elif len({json.dumps(c['value']) for c in current}) > 1:
            status, reason = 'CONFLICT', 'Current assertions disagree about the same fact for this action. Verification of one does not silently discard the others.'
        elif any(c['value'] is False for c in current):
            status, reason = 'FAIL', 'A current source asserts this condition is false; this is a refusal or failed condition, not a disagreement by itself.'
        elif any(c['verified'] for c in current):
            status, reason = 'PASS', 'The current assertions agree and at least one has a recorded verification.'
        else:
            status, reason = 'UNKNOWN', 'The current assertions agree but remain unverified. Agreement alone does not verify a fact.'
        group.update(status=status, reason=reason)
    return sorted(groups.values(), key=lambda g: (g['key'], not g['applies_to_current_action'], json.dumps(g['scope'], sort_keys=True)))


def case_insights(service, cid, who):
    service.role(who, ROLES)
    with service.db.tx() as connection:
        case = service.db.case(connection, cid)
        ledger = service.db.list(connection, case_id=cid)
        at = now()
        claims = [payload(r) for r in ledger if r['kind'] == 'claim']
        sources = {r['id']: payload(r) for r in ledger if r['kind'] == 'evidence'}
        frames, prefix, known_evidence = [], [], []
        for record in ledger:
            prefix.append(record)
            if record['kind'] == 'evidence':
                known_evidence.append(payload(record))
            if record['kind'] == 'decision':
                # No fields from the replaceable current case projection enter
                # a frame. Earlier event dates never move later receipts back.
                frames.append({'id': record['id'], 'at': record['created_at'],
                               'decision': payload(record),
                               'evidence': deepcopy(known_evidence), 'events': deepcopy(prefix)})
        return {'case_id': cid, 'as_of': stamp(at),
                'comparisons': _comparisons(case, claims, sources, at), 'frames': frames,
                'playback_notice': 'Recorded decisions only. Each frame contains evidence and ledger events received by that decision record; source occurrence dates do not establish when the system knew a fact. No decision is rerun with today\'s policy or case details.',
                'comparison_notice': 'Comparisons concern structured source assertions. Unstructured messages are shown as evidence, not automatically inferred facts. A source label or submitter is not verified sender identity. Party markers retain their recorded match method; fictional caller-ID directory matches do not establish production identity.'}


def _changes(before, after):
    changes = []
    if before['outcome'] != after['outcome']:
        changes.append({'key': 'outcome', 'before': before['outcome'], 'after': after['outcome'],
                        'reason': 'The leading response changes under the proposed policy; all blockers still apply.'})
    old_checks = {c['key']: c for c in before['checks']}
    new_checks = {c['key']: c for c in after['checks']}
    for key in sorted(old_checks.keys() | new_checks.keys()):
        old, new = old_checks.get(key), new_checks.get(key)
        if old != new:
            changes.append({'key': key, 'before': old, 'after': new,
                            'reason': (new or old).get('reason', 'The applicable requirement changes.')})
    # A custom rule can change the response or owner while fact checks and even
    # the leading outcome stay the same. Preserve each independent blocker.
    old_blockers = {(b['key'], b['rule_id']): b for b in before['blockers']}
    new_blockers = {(b['key'], b['rule_id']): b for b in after['blockers']}
    for key in sorted(old_blockers.keys() | new_blockers.keys()):
        old, new = old_blockers.get(key), new_blockers.get(key)
        if old != new:
            changes.append({'key': 'blocker:' + key[0] + ':' + key[1], 'before': old, 'after': new,
                            'reason': (new or old)['reason']})
    return changes


def compare_policy(service, data, who):
    service.role(who, {'policy_editor'})
    with service.db.tx() as connection:
        record = service.db.get_record(connection, data.draft_id)
        if record['kind'] != 'policy_draft':
            raise ValueError('Choose a policy draft for comparison')
        draft, active = payload(record), service.active(connection)
        # Even a stale draft is a hypothetical NEW publication, not the active
        # policy with overwritten settings. Existing approvals stay versioned.
        candidate = {**draft, 'version': active['version'] + 1}
        at = now()
        selected = (service.db.case_list(connection) if data.case_ids is None else
                    [service.db.case(connection, cid) for cid in dict.fromkeys(data.case_ids)])
        rows = []
        for case in selected:
            cid = case['id']
            actions = service.action_states(connection, cid)
            completed = next((a for a in actions if a['business_id'] == business_id(case) and a['status'] == 'succeeded'), None)
            row = {'case_id': cid, 'title': case['title'], 'completed': completed is not None}
            if completed:
                original = payload(service.db.get_record(connection, completed['decision_id']))
                retained = {**original, 'outcome': 'NO FURTHER ACTION', 'blockers': [],
                            'next_step': 'The current business action already has a confirmed simulated receipt. Its recorded decision is retained; this comparison cannot reopen it.',
                            'completed_action_id': completed['id'], 'recorded_decision': original}
                row.update(before=retained, after=deepcopy(retained), changes=[], action=completed,
                           receipt=(payload(service.db.get_record(connection, completed['receipt_id']))
                                    if completed.get('receipt_id') else None))
            else:
                inputs = {**case, 'policy_pending': False}
                claims = service.claims(connection, cid)
                approvals = service.approvals(connection, cid)
                uncertain = any(a['status'] == 'uncertain' for a in actions)
                before = evaluate(inputs, claims, approvals, active, uncertain=uncertain, at=at)
                after = evaluate(inputs, claims, approvals, candidate, uncertain=uncertain, at=at)
                row.update(before=before, after=after, changes=_changes(before, after))
            rows.append(row)
        return {'active_version': active['version'], 'draft_id': draft['id'],
                'stale_base': draft['base_version'] != active['version'],
                'proposed_version': candidate['version'], 'as_of': stamp(at), 'rows': rows,
                'assumptions': [
                    'Read-only rule comparison using the same current case facts, source claims, revocations and timestamp on both sides. No cases, questions, reviews or policies are changed.',
                    'These are pure policy outcomes, not the saved operational workflow outcome. Existing questions, reminders, review history and message delivery can further change operational handling.',
                    'Pending-publication reassessment holds are excluded on both sides to show the underlying rules. Other independent blockers, including uncertain actions, remain.',
                    'The draft is evaluated as a new policy version. Approvals scoped to the active version do not carry over; expired, revoked or mismatched approvals remain invalid.',
                    'Completed current business actions retain their original decision and simulated receipt. A stale draft can be inspected but must be rebased before publication.',
                ]}


def create_insights_router(actor):
    router = APIRouter()

    @router.get('/api/cases/{cid}/insights')
    def insights(cid: str, who=Depends(actor)):
        return case_insights(get_service(), cid, who)

    @router.post('/api/policy-comparison')
    def policy_comparison(data: PolicyComparisonInput, who=Depends(actor)):
        return compare_policy(get_service(), data, who)

    return router
