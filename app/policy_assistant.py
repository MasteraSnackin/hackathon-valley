"""Bounded plain-English policy drafting; this module never writes policy or facts.

Interpretation is deliberately deterministic. Unrecognised clauses are returned to
the editor rather than discarded. The existing PolicyInput and policy evaluator
remain the validation and decision authorities.
"""
from __future__ import annotations

from copy import deepcopy
import hashlib
import json
import re
from typing import Literal

from fastapi import APIRouter, Depends, HTTPException
from pydantic import Field, ValidationError

from .domain import PolicyInput, ROLES, Rule, StrictModel
from .service import get_service


class InterpretRequest(StrictModel):
    text: str = Field(min_length=1, max_length=4000)
    review_id: str | None = Field(default=None, min_length=1, max_length=80)


class AssistantResult(StrictModel):
    status: Literal['ready', 'clarification', 'unsupported']
    summary: str
    questions: list[str] = Field(default_factory=list)
    warnings: list[str] = Field(default_factory=list)
    draft: PolicyInput | None = None
    source_review_id: str | None = None
    suggested_text: str | None = None


PREVIEW_WARNING = 'Proposed draft only. A policy editor must save it, run an impact preview and explicitly publish it.'
GATE_WARNING = 'Required facts, refusals, conflicting evidence and scoped approvals remain controlled by the existing policy engine.'
CASE_WARNING = 'A decision or consent for one case is not permission for other visits, work items, providers or cases.'
ACTION_NAMES = {
    'clarify': 'clarify', 'clarification': 'clarify',
    'request_quote': 'request_quote', 'request quote': 'request_quote', 'requesting a quote': 'request_quote',
    'confirm_appointment': 'confirm_appointment', 'confirm appointment': 'confirm_appointment', 'confirming an appointment': 'confirm_appointment',
    'supply_keys': 'supply_keys', 'supply keys': 'supply_keys', 'supplying keys': 'supply_keys',
    'instruct_work': 'instruct_work', 'instruct work': 'instruct_work', 'instructing work': 'instruct_work', 'work instructions': 'instruct_work',
    'close_item': 'close_item', 'close item': 'close_item', 'closing an item': 'close_item', 'closing a repair': 'close_item',
    'archive': 'archive', 'archiving': 'archive',
}
FACT_NAMES = {
    'identity': 'identity', 'identity mapping': 'identity',
    'completion': 'completion', 'completion evidence': 'completion',
    'evidence': 'evidence', 'usable evidence': 'evidence',
    'schedule': 'schedule', 'scheduling': 'schedule', 'appointment': 'schedule',
    'access': 'access', 'access permission': 'access', 'consent': 'access',
    'authority': 'authority', 'financial authority': 'authority',
    'keys': 'keys', 'key custody': 'keys',
    'route': 'route', 'communication route': 'route',
    'classification': 'classification', 'commitments': 'commitments',
}
STATUS_NAMES = {
    'missing': 'UNKNOWN', 'unknown': 'UNKNOWN', 'unverified': 'UNKNOWN',
    'conflicting': 'CONFLICT', 'conflict': 'CONFLICT', 'conflicts': 'CONFLICT',
    'refused': 'FAIL', 'failed': 'FAIL', 'false': 'FAIL',
}
RESPONSE_NAMES = {
    'require human review': 'HUMAN REVIEW', 'escalate': 'HUMAN REVIEW',
    'escalate immediately': 'HUMAN REVIEW', 'stop action': 'STOP ACTION',
    'stop the action': 'STOP ACTION', 'ask for clarification': 'CLARIFY',
    'request evidence': 'CLARIFY', 'wait': 'WAIT',
}
OWNERS = {
    'case manager': 'case_manager', 'property manager': 'case_manager', 'case_manager': 'case_manager',
    'access officer': 'access_officer', 'access_officer': 'access_officer',
    'approver': 'approver', 'reviewer': 'reviewer',
    'policy editor': 'policy_editor', 'policy_editor': 'policy_editor',
}
ACTION_LABELS = {
    'clarify': 'clarification', 'request_quote': 'requesting a quote',
    'confirm_appointment': 'confirming an appointment', 'supply_keys': 'supplying keys',
    'instruct_work': 'work instructions', 'close_item': 'closing a repair', 'archive': 'archiving',
}
OWNER_LABELS = {
    'case_manager': 'property manager', 'access_officer': 'access officer',
    'approver': 'approver', 'reviewer': 'reviewer', 'policy_editor': 'policy editor',
}
STATE_LABELS = {'UNKNOWN': 'missing or unverified', 'CONFLICT': 'conflicting', 'FAIL': 'refused or failed'}
NUMBER = r'(?:\d{1,3}(?:,\d{3})+|\d+)(?:\.\d+)?'
MONEY = rf'(?:£\s*{NUMBER}|gbp\s*{NUMBER}|{NUMBER}\s*(?:pounds?|gbp))'
COUNT = r'(?:[0-9]+|zero|one|two|three|four|five)'


def _result(status, summary, *, questions=(), warnings=(), draft=None, review=None, suggested_text=None):
    return AssistantResult(status=status, summary=summary, questions=list(questions),
                           warnings=list(warnings), draft=draft,
                           source_review_id=review['id'] if review else None,
                           suggested_text=suggested_text)


def _normalise(text):
    return re.sub(r'\s+', ' ', text.strip().lower().replace('’', "'")).rstrip('.!? ')


def _unsafe(text):
    return bool(re.search(
        r'auto[- ]?approve|automatically approve|without (?:any |an? )?(?:authority|consent|permission|approval)|'
        r'(?:skip|bypass|ignore|remove|disable|waive).*(?:gate|check|authority|consent|permission|approval|requirement)|'
        r'(?:grant|assume|mark|verify|treat|allow|permit).*(?:all|every|globally|always|universal)|'
        r'(?:universal|blanket|permanent) (?:access|permission|consent|authority)', text))


def _review_context(service, connection, review_id):
    # Identical error for a missing ID, another record kind or a broken case link.
    try:
        row = service.db.get_record(connection, review_id)
        if row['kind'] != 'review':
            raise ValueError('Not a review')
        case = service.db.case(connection, row['case_id'])
        review = next(r for r in service.reviews(connection, case) if r['id'] == review_id)
    except (ValueError, StopIteration):
        raise HTTPException(status_code=404, detail='Review not found') from None
    # Match the recorded blocker, not the newly resolved fact or current outcome.
    blockers = [b for d in service.rows(connection, 'decision', case['id'])
                if d.get('policy_version') == review['policy_version']
                and d.get('action_revision') == review['action_revision']
                for b in d.get('blockers', [])
                if b['key'] == review['key'] and b['rule_id'] == review['rule_id']
                and set(b.get('claim_ids', [])) == set(review.get('claim_ids', []))]
    return {**review, 'case': case, 'original_blocker': blockers[0] if blockers else None}


def _provenance(text, review):
    reason = 'Plain-English policy proposal: ' + text[:450]
    if review:
        response = review.get('response') or {}
        sources = list(dict.fromkeys(review.get('source_ids', []) + ([response['source_id']] if response.get('source_id') else [])))
        reason += f" | Source review {review['id']}; case {review['case']['id']}; recorded decision {response.get('decision', 'unresolved')}."
        reason += ' Evidence source IDs: ' + (', '.join(sources[:6]) if sources else 'none recorded') + '.'
        if len(sources) > 6:
            reason += ' Further source IDs remain in the review audit.'
        reason += ' Case facts and permissions are not generalised.'
    return reason[:1000]


def _draft(active, text, review, *, changes=None, rule=None, replace_id=None):
    settings = deepcopy(active['settings'])
    settings.update(changes or {})
    rules = deepcopy(active.get('rules', []))
    if rule:
        if replace_id:
            rules = [rule if r['id'] == replace_id else r for r in rules]
        elif not any(r['id'] == rule['id'] for r in rules):
            rules.append(rule)
    return PolicyInput(base_version=active['version'], settings=settings, rules=rules,
                       reason=_provenance(text, review))


def _settings_clause(clause):
    """Return one explicit setting change or None; do not ignore residual text."""
    money_patterns = [
        rf'(?:set )?(?:the )?(?:spending|spend|financial) (?:review )?(?:threshold|limit) (?:to |at |is |of )?({MONEY})',
        rf'(?:require )?(?:human |financial )?review (?:for )?(?:spending|spend|work|costs?|totals?) (?:over|above|greater than|more than) ({MONEY})',
        rf'(?:send|refer) (?:spending|spend|work|costs?|totals?) (?:over|above) ({MONEY}) (?:for|to) (?:human |financial )?review',
    ]
    for pattern in money_patterns:
        match = re.fullmatch(pattern, clause)
        if match:
            amount = float(re.search(NUMBER, match[1]).group().replace(',', ''))
            return {'review_limit': amount}
    immediate = [
        r'(?:escalate|review) (?:missing|unknown|unverified) access(?: permission| consent)? immediately',
        r'(?:require )?(?:immediate )?human review (?:when|if|for) access(?: permission| consent)? (?:is )?(?:missing|unknown|unverified)(?: immediately)?',
    ]
    if any(re.fullmatch(p, clause) for p in immediate):
        return {'access_immediate_review': True}
    permission = [
        r'(?:request|ask for) access permission (?:when|if) (?:it|access permission) is (?:missing|unknown)',
        r'(?:when|if) access permission is (?:missing|unknown),? (?:request|ask for) (?:it|permission)',
        r'(?:set )?missing access(?: permission)? (?:to )?(?:request permission|clarification)',
    ]
    if any(re.fullmatch(p, clause) for p in permission):
        return {'access_immediate_review': False}
    for key, pattern in [
        ('reminder_hours', rf'(?:send (?:a |the )?)?(?:remind|reminder|follow[- ]up)(?: after| at| in| to)? ({NUMBER}) working hours?'),
        ('reminder_hours', rf'(?:set )?(?:the )?(?:reminder|follow[- ]up) (?:delay|time|interval) to ({NUMBER}) working hours?'),
        ('escalation_hours', rf'(?:escalate|escalation)(?: after| at| in| to)? ({NUMBER}) working hours?'),
        ('escalation_hours', rf'(?:set )?(?:the )?escalation (?:delay|time|interval) to ({NUMBER}) working hours?'),
    ]:
        match = re.fullmatch(pattern, clause)
        if match:
            return {key: float(match[1].replace(',', ''))}
    for pattern in [rf'(?:send |with )?(?:at most |up to |a maximum of )?({COUNT}) reminders?',
                    rf'(?:set |limit )?(?:the )?reminder (?:count|limit)(?: to| at)? ({COUNT})']:
        match = re.fullmatch(pattern, clause)
        if match:
            words = {'zero': 0, 'one': 1, 'two': 2, 'three': 3, 'four': 4, 'five': 5}
            return {'reminder_limit': words[match[1]] if match[1] in words else int(match[1])}
    return None


def _parse_settings(text):
    clauses = re.split(r'\s*;\s*|\s+and\s+|\s*,?\s+with\s+', text)
    changes = {}
    for clause in clauses:
        parsed = _settings_clause(clause.rstrip(' ,'))
        if not parsed or changes.keys() & parsed.keys():
            return None
        changes.update(parsed)
    return changes or None


def _parse_rule(text, active, review):
    """One condition, explicit response and action scope, optional quoted property."""
    replace_id = None
    update = re.match(r'(?:update|replace) rule ([a-z0-9_-]{1,80}):\s*', text)
    if update:
        replace_id = update[1]
        if not any(r['id'] == replace_id for r in active.get('rules', [])):
            return None, ['Which existing rule should be updated? That rule ID is not in the active policy.'], None
        text = text[update.end():]
    property_ref = None
    property_match = re.search(r' (?:at|for) property "([^"\n]{1,200})"$', text)
    if property_match:
        property_ref = property_match[1]
        text = text[:property_match.start()]
    owner = None
    owner_match = re.search(r' (?:to|owned by) (?:a |an |the )?(' + '|'.join(map(re.escape, OWNERS)) + r')$', text)
    if owner_match:
        owner = OWNERS[owner_match[1]]
        text = text[:owner_match.start()]
    actions = None
    action_match = re.search(r' (?:for|before|on) (all actions|' + '|'.join(sorted(map(re.escape, ACTION_NAMES), key=len, reverse=True)) + r')$', text)
    if action_match:
        actions = [] if action_match[1] == 'all actions' else [ACTION_NAMES[action_match[1]]]
        text = text[:action_match.start()]
    # Accept an owner before the action clause as well as after it.
    if not owner:
        owner_match = re.search(r' (?:to|owned by) (?:a |an |the )?(' + '|'.join(map(re.escape, OWNERS)) + r')$', text)
        if owner_match:
            owner = OWNERS[owner_match[1]]
            text = text[:owner_match.start()]
    response_pattern = '|'.join(sorted(map(re.escape, RESPONSE_NAMES), key=len, reverse=True))
    match = re.fullmatch(r'(' + response_pattern + r') (?:(?:when|if|for) )?(.+)', text)
    if not match:
        return None, [], None
    condition = match[2]
    key = status = None
    facts_pattern = '|'.join(sorted(map(re.escape, FACT_NAMES), key=len, reverse=True))
    statuses_pattern = '|'.join(map(re.escape, STATUS_NAMES))
    for pattern in [r'(' + facts_pattern + r') (?:is |has |are )?(' + statuses_pattern + r')',
                    r'(' + statuses_pattern + r') (' + facts_pattern + r')']:
        found = re.fullmatch(pattern, condition)
        if found:
            values = found.groups()
            fact, state = values if values[0] in FACT_NAMES else values[::-1]
            key, status = FACT_NAMES[fact], STATUS_NAMES[state]
            break
    if not key:
        return None, ['Which one fact and state should trigger the rule: missing, conflicting or refused? Use the structured editor for multiple conditions.'], None
    warnings = []
    if actions is None:
        if review:
            actions = [review['scope']['action']]
            warnings.append('Action scope defaults to the source review. Check it in the structured editor.')
        else:
            return None, ['Which action should this rule apply to? Specify an action such as work instructions or closing a repair, or explicitly say all actions.'], None
    if review and property_ref is None:
        property_ref = review['scope']['property_ref']
        warnings.append('Property scope defaults to the source review. This is a reusable rule for that property and action, not the single work item.')
    owner = owner or ('access_officer' if key in {'access', 'keys'} else 'approver' if key == 'authority' else 'reviewer' if key == 'completion' else 'case_manager')
    rule = Rule(id='pending', conditions=[{'key': key, 'status': status}], actions=actions,
                response=RESPONSE_NAMES[match[1]], owner=owner, property_ref=property_ref).model_dump()
    semantic = json.dumps({k: v for k, v in rule.items() if k != 'id'}, sort_keys=True)
    rule['id'] = replace_id or 'assistant-' + hashlib.sha256(semantic.encode()).hexdigest()[:16]
    return rule, [], {'replace_id': replace_id, 'warnings': warnings}


def interpret_policy(text, active, review=None):
    normalised = _normalise(text)
    if _unsafe(normalised):
        return _result('unsupported', 'Policy drafting cannot create authority, verify facts globally or remove required safeguards.',
                       warnings=[CASE_WARNING, GATE_WARNING], review=review)
    if review and normalised in {'make this a policy', 'make this policy', 'suggest a policy'}:
        return suggest_from_review(active, review)
    # Keep quoted identifiers exactly as supplied; all other grammar is case insensitive.
    quoted = re.findall(r'"[^"\n]*"', text)
    lowered_quoted = re.findall(r'"[^"\n]*"', normalised)
    for original, lowered in zip(quoted, lowered_quoted):
        normalised = normalised.replace(lowered, original, 1)
    changes = _parse_settings(normalised)
    if changes:
        try:
            draft = _draft(active, text, review, changes=changes)
        except ValidationError as error:
            questions = {
                'Invalid review limit': 'What spending threshold between £0 and £1,000,000 should be used?',
                'Invalid reminder_hours': 'What reminder delay between 0.1 and 720 working hours should be used?',
                'Invalid escalation_hours': 'What escalation delay between 0.1 and 720 working hours should be used?',
                'Escalation must follow reminder': 'What escalation delay should be used? It must be longer than the reminder delay; both run from the original request.',
                'Reminder limit must be 0 to 5': 'How many reminders should be allowed, from zero to five?',
            }
            messages = [questions.get(e['msg'].removeprefix('Value error, '),
                                      'Which supported value should be used? Check the structured policy editor.')
                        for e in error.errors()]
            return _result('clarification', 'The requested values do not form a valid policy.', questions=messages, review=review)
        summary_parts = []
        if 'review_limit' in changes:
            summary_parts.append(f"Require financial review when the verified total for work instructions is strictly above £{changes['review_limit']:g}")
        if 'access_immediate_review' in changes:
            summary_parts.append('Route missing access permission to immediate human review' if changes['access_immediate_review'] else 'Request missing access permission where a verified communication route exists')
        labels = {'reminder_hours': 'Reminder after', 'escalation_hours': 'Escalation after'}
        for key, label in labels.items():
            if key in changes:
                summary_parts.append(f'{label} {changes[key]:g} working hours from the original request')
        if 'reminder_limit' in changes:
            summary_parts.append(f"Allow at most {changes['reminder_limit']} reminders")
        warnings = [PREVIEW_WARNING, GATE_WARNING, 'These settings apply across the active demonstration policy.']
        if {'reminder_hours', 'escalation_hours'} & changes.keys():
            warnings.append('Working hours use the existing Monday–Friday, 09:00–17:00 Europe/London calendar and configured holidays.')
        if review:
            warnings.append(CASE_WARNING)
        return _result('ready', '; '.join(summary_parts) + '.', warnings=warnings, draft=draft, review=review)
    rule, questions, options = _parse_rule(normalised, active, review)
    if questions:
        return _result('clarification', 'More detail is needed before a draft can be proposed.', questions=questions, review=review)
    if rule:
        try:
            draft = _draft(active, text, review, rule=rule, replace_id=options['replace_id'])
        except ValidationError:
            return _result('unsupported', 'This proposal exceeds the existing policy format. Use the structured editor.', review=review)
        scope = ', '.join(ACTION_LABELS[action] for action in rule['actions']) or 'all actions'
        scope += f" at property {rule['property_ref']}" if rule['property_ref'] else ' across all properties'
        condition = rule['conditions'][0]
        summary = f"{'Update' if options['replace_id'] else 'Add'} a rule: {STATE_LABELS[condition['status']]} {condition['key']} requires {rule['response'].lower()} for {scope}, owned by the {OWNER_LABELS[rule['owner']]}."
        warnings = [PREVIEW_WARNING, GATE_WARNING] + options['warnings']
        if review:
            warnings.append(CASE_WARNING)
        if any(r['id'] == rule['id'] for r in active.get('rules', [])) and not options['replace_id']:
            warnings.append('An identical assistant rule already exists; no duplicate has been added.')
        return _result('ready', summary, warnings=warnings, draft=draft, review=review)
    if re.search(r'\b(?:hour|hours|day|days|minute|minutes)\b', normalised):
        return _result('clarification', 'The timing request is incomplete or outside the supported working-hours format.',
                       questions=['State each delay in working hours, for example: remind after 4 working hours and escalate after 12 working hours. Escalation is measured from the original request.'], review=review)
    if re.search(r'£|\$|€|\b(?:spend|spending|financial|threshold|pounds?|gbp|cost|limit)\b', normalised):
        return _result('clarification', 'The amount, currency, comparison or scope is not sufficiently explicit.',
                       questions=['What GBP amount should trigger review for work instructions? For example: require human review for spending over £250. The supported comparison is strictly above, not at least.'], review=review)
    return _result('unsupported', 'This wording is outside the supported policy vocabulary; no change was proposed.',
                   questions=['Use an explicit threshold, working-hours follow-up, missing-access route, or one fact/state and action scope. More complex rules can be entered in the structured editor.'], review=review)


def suggest_from_review(active, review):
    response = review.get('response') or {}
    if review['status'] != 'resolved' or response.get('decision') not in {'approve', 'correct', 'reject'}:
        return _result('clarification', 'This review has no current completed decision to use as a policy example.',
                       questions=['Complete the current review decision first, or describe the reusable rule directly.'],
                       warnings=[CASE_WARNING], review=review, suggested_text='')
    blocker = review.get('original_blocker')
    if review['key'] == 'finance':
        return _result('clarification', 'A financial approval authorises one scoped action; it does not establish a new spending threshold.',
                       questions=['What GBP threshold should apply to future work instructions? Enter an explicit amount in the policy composer.'],
                       warnings=[CASE_WARNING, PREVIEW_WARNING], review=review, suggested_text='')
    if not blocker or review['key'] not in set(FACT_NAMES.values()):
        return _result('unsupported', 'This review cannot be converted reliably into a reusable condition. Describe the intended rule in the structured editor.',
                       warnings=[CASE_WARNING], review=review, suggested_text='')
    state = {'UNKNOWN': 'missing', 'CONFLICT': 'conflicting', 'FAIL': 'refused'}.get(blocker['status'])
    if state is None:
        return _result('unsupported', 'A reusable unresolved-fact condition is not recorded for this review.', review=review, suggested_text='')
    scope = review['scope']
    verb = 'Stop action' if blocker['status'] == 'FAIL' else 'Require human review'
    suggested_text = f"{verb} when {review['key']} is {state} for {ACTION_LABELS[scope['action']]}"
    # Review scope is kept in the draft even if its property text cannot safely be
    # represented in the bounded quote grammar. No review prose is interpreted.
    result = interpret_policy(suggested_text, active, review)
    result.suggested_text = suggested_text
    result.warnings.append('This conservative suggestion uses the original blocker, not the resolution as a general fact. It may duplicate an existing safeguard; inspect the impact preview.')
    return result


def create_policy_assistant_router(actor):
    router = APIRouter(prefix='/api/policy-assistant', tags=['policy-assistant'])

    @router.post('/interpret', response_model=AssistantResult)
    def interpret_request(data: InterpretRequest, who=Depends(actor)):
        service = get_service()
        service.role(who, ROLES)
        with service.db.tx() as connection:
            review = _review_context(service, connection, data.review_id) if data.review_id else None
            return interpret_policy(data.text, service.active(connection), review)

    @router.get('/reviews/{rid}/suggestion', response_model=AssistantResult)
    def review_suggestion(rid: str, who=Depends(actor)):
        service = get_service()
        service.role(who, ROLES)
        with service.db.tx() as connection:
            review = _review_context(service, connection, rid)
            return suggest_from_review(service.active(connection), review)

    return router
