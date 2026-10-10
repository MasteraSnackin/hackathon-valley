"""Jev routing and hand-off to Claude, with fake model answers (offline).

The fakes stand in for jev.ask and ai.triage so each mode is exercised
deterministically: Jev-only, Jev route with Claude extraction, hand-off to
Claude, shadow mode, unavailability and staff-set routes.
"""
import pytest
from app import ai, jev
from app.domain import DEFAULT_SETTINGS, EvidenceInput, Intake, PolicyInput, ProposalInput, ReviewResponse
from app.service import Service
from app.store import Store

ACTOR = {'id': 'test-manager', 'role': 'case_manager'}
EDITOR = {'id': 'test-editor', 'role': 'policy_editor'}
REPORT = 'The kitchen tap has been dripping constantly since yesterday.'


def answers(route='request_quote', confidence=0.9, category='plumbing', **signals):
    base = {'hazard': 0.02, 'multiple_issues': 0.05, 'states_facts': 0.05, 'system_instructions': 0.01, 'sensitive': 0.05}
    return {'route': {'choice': route, 'confidence': confidence, 'probabilities': {route: confidence}},
            'category': {'choice': category, 'confidence': 0.9}, 'signals': {**base, **signals}}


def claude_reading(route='request_quote', objection='', quote='dripping constantly'):
    return {'intent': 'new_request', 'summary': 'Dripping kitchen tap.',
            'issues': [{'category': 'plumbing', 'route': route, 'work_item': 'Kitchen tap dripping', 'source_quote': quote, 'relation': 'current_case'}],
            'claims': [], 'ambiguities': [], 'answers': [], 'risk_flags': [], 'confidence': 'high', 'rationale': 'Leak needs a quote.',
            'route_objection': objection}


@pytest.fixture
def service(tmp_path):
    return Service(Store('sqlite:///' + str(tmp_path / 'router.db')))


@pytest.fixture
def models(monkeypatch):
    """Records every fake model call; tests set the next answers."""
    calls = {'jev': [], 'claude': [], 'jev_answers': answers(), 'claude_result': claude_reading()}
    monkeypatch.setenv('TYPESAFE_API_KEY', 'fake-for-tests')

    def fake_ask(text, context, reverse=False):
        calls['jev'].append(text)
        return calls['jev_answers'], {'provider': 'typesafe', 'model': 'jev-1.13.0', 'request_id': 'fake', 'router_version': jev.ROUTER_VERSION, 'latency_ms': 1, 'usage': {}}

    def fake_triage(text, context, router=None):
        calls['claude'].append(router)
        return calls['claude_result'], {'provider': 'anthropic', 'model': 'fake-claude', 'request_id': 'fake', 'usage': {}}

    monkeypatch.setattr(jev, 'ask', fake_ask)
    monkeypatch.setattr(ai, 'triage', fake_triage)
    return calls


def report(service, text=REPORT, **extra):
    return service.intake(Intake(title='Fictional report', property_ref='DEMO-FLAT-1', report=text, **extra), ACTOR)['case']['id']


def routing(detail):
    return next(r['payload'] for r in detail['timeline'] if r['kind'] == 'routing')


def blocker(detail, key='triage'):
    return next((b for b in detail['decision']['blockers'] if b['key'] == key), None)


def publish(service, **settings):
    version = service.policies()['active']['version']
    draft = service.draft(PolicyInput(base_version=version, settings=settings, reason='Router test'), EDITOR)
    service.preview(draft['id'], EDITOR)
    return service.publish(draft['id'], EDITOR)


def test_confident_simple_first_report_is_routed_by_jev_without_claude(service, models):
    cid = report(service)
    assert service.route_messages(cid) == {'routed': 1, 'jev_only': 1}
    assert service.triage_messages(cid) == {'triaged': 0, 'spawned_case_ids': []}
    detail = service.detail(cid)
    case, triage = detail['case'], detail['case']['triage']
    assert models['claude'] == [] and len(models['jev']) == 1
    assert triage['state'] == 'done' and triage['route'] == 'request_quote' and triage['router']['mode'] == 'jev_only'
    assert case['proposal']['action'] == 'request_quote' and case['category'] == 'plumbing'
    assert case['interpretation']['mode'] == 'jev'
    reading = next(r['payload'] for r in detail['timeline'] if r['kind'] == 'interpretation')
    assert reading['provider'] == 'typesafe' and reading['result']['claims'] == []
    # Only the derived category is recorded, and a Jev-only category is never auto-accepted.
    claims = [c for c in detail['claims'] if c.get('origin') == 'claude']
    assert [(c['key'], c['verified']) for c in claims] == [('classification', False)]
    # A Jev reading is applied once, even if the step is retried.
    assert service.route_messages(cid) == {'routed': 0, 'jev_only': 0}


def test_message_with_facts_is_routed_by_jev_and_claude_extracts(service, models):
    models['jev_answers'] = answers(states_facts=0.9)
    cid = report(service)
    assert service.triage_messages(cid) == {'triaged': 1, 'spawned_case_ids': []}
    detail = service.detail(cid)
    assert routing(detail)['mode'] == 'jev_route'
    assert models['claude'][0]['route'] == 'request_quote'
    triage = detail['case']['triage']
    assert triage['route'] == 'request_quote' and triage['route_disagreement'] is None
    assert detail['case']['interpretation']['mode'] == 'jev+claude'


def test_claude_objection_holds_the_case_for_a_person(service, models):
    models['jev_answers'] = answers(states_facts=0.9)
    models['claude_result'] = claude_reading(route='clarify', objection='The message does not say which tap.')
    cid = report(service)
    service.triage_messages(cid)
    detail = service.detail(cid)
    triage = detail['case']['triage']
    # Claude's objection is applied, and the disagreement is a conflict for the case manager.
    assert triage['route'] == 'clarify' and triage['route_disagreement'] == {'jev': 'request_quote', 'claude': 'clarify', 'reason': 'The message does not say which tap.'}
    assert detail['case']['proposal']['action'] == 'clarify'
    held = blocker(detail)
    assert held['status'] == 'CONFLICT' and held['response'] == 'HUMAN REVIEW'
    # The classification is not auto-accepted while the route is disputed.
    assert not any(c['key'] == 'classification' and c['verified'] for c in detail['claims'])
    review = next(r for r in detail['reviews'] if r['key'] == 'triage' and r['status'] == 'open')
    confirmed = service.respond(review['id'], ReviewResponse(decision='approve', reason='Checked the route against the message.'), ACTOR)
    assert blocker(confirmed) is None


@pytest.mark.parametrize('jev_answers,reason', [
    (answers(route='unknown', confidence=0.7), 'unknown'),
    (answers(confidence=0.3), 'below'),
    (answers(multiple_issues=0.8), 'several issues'),
    (answers(system_instructions=0.9), 'instructions'),
])
def test_uncertain_messages_are_handed_to_claude(service, models, jev_answers, reason):
    models['jev_answers'] = jev_answers
    cid = report(service)
    service.triage_messages(cid)
    detail = service.detail(cid)
    record = routing(detail)
    assert record['mode'] == 'claude' and reason in ' '.join(record['decision']['reasons'])
    # Claude triages with no router decision, as before Jev existed.
    assert models['claude'] == [None]
    assert detail['case']['triage']['router']['mode'] == 'claude' and detail['case']['interpretation']['mode'] == 'claude'


def test_possible_hazard_escalates_even_when_claude_disagrees(service, models):
    models['jev_answers'] = answers(hazard=0.6)
    models['claude_result'] = claude_reading(quote='faint smell of gas')
    cid = report(service, 'There is a faint smell of gas near the boiler.')
    service.triage_messages(cid)
    detail = service.detail(cid)
    assert routing(detail)['route'] == 'urgent_hazard' and models['claude'][0]['route'] == 'urgent_hazard'
    triage = detail['case']['triage']
    assert triage['route'] == 'urgent_hazard' and triage['route_disagreement']['claude'] == 'request_quote'
    assert blocker(detail)['response'] == 'HUMAN REVIEW'


def test_claude_hazard_reading_wins_over_a_jev_route(service, models):
    models['jev_answers'] = answers(states_facts=0.9)
    models['claude_result'] = claude_reading(route='urgent_hazard', objection='Possible gas leak.')
    cid = report(service)
    service.triage_messages(cid)
    triage = service.detail(cid)['case']['triage']
    assert triage['route'] == 'urgent_hazard'


def test_jev_unavailable_falls_back_to_claude(service, models, monkeypatch):
    def down(text, context, reverse=False):
        raise jev.JevUnavailable('TypeSafeRateLimitError', 'HTTP 429')
    monkeypatch.setattr(jev, 'ask', down)
    cid = report(service)
    service.triage_messages(cid)
    detail = service.detail(cid)
    record = routing(detail)
    assert record['mode'] == 'claude' and record['error_type'] == 'TypeSafeRateLimitError'
    assert models['claude'] == [None] and detail['case']['triage']['state'] == 'done'


def test_both_models_unavailable_hands_the_message_to_a_person(service, no_claude, monkeypatch):
    monkeypatch.setenv('TYPESAFE_API_KEY', '')
    cid = report(service)
    service.triage_messages(cid)
    detail = service.detail(cid)
    assert routing(detail)['error_type'] == 'missing_credentials'
    assert detail['case']['triage']['state'] == 'failed' and blocker(detail)['response'] == 'HUMAN REVIEW'


def test_shadow_mode_records_jev_but_claude_decides(service, models):
    publish(service, router='jev_shadow')
    cid = report(service)
    service.triage_messages(cid)
    record = routing(service.detail(cid))
    assert record['mode'] == 'claude' and record['proposed_mode'] == 'jev_only' and record['route'] == 'request_quote'
    assert models['claude'] == [None]


def test_claude_router_policy_skips_jev(service, models):
    publish(service, router='claude')
    cid = report(service)
    service.triage_messages(cid)
    detail = service.detail(cid)
    assert models['jev'] == [] and not any(r['kind'] == 'routing' for r in detail['timeline'])
    assert models['claude'] == [None]


def test_staff_route_is_never_replaced_by_jev(service, models):
    cid = report(service)
    service.proposal(cid, ProposalInput(action='request_quote', category='plumbing', work_item='Kitchen tap'), ACTOR)
    service.evidence(cid, EvidenceInput(text='Any update on the tap?', source_label='Tenant reply'), ACTOR)
    service.triage_messages(cid)
    detail = service.detail(cid)
    staff_routed = [r['payload'] for r in detail['timeline'] if r['kind'] == 'routing' and r['payload']['decision']['reasons'][0].startswith('Staff')]
    assert staff_routed and len(models['jev']) == 0


def test_route_change_on_an_existing_case_still_goes_through_claude(service, models):
    cid = report(service)
    service.triage_messages(cid)
    models['jev_answers'] = answers(route='close_item', confidence=0.95)
    service.evidence(cid, EvidenceInput(text='All done, thanks.', source_label='Contractor email'), ACTOR)
    service.triage_messages(cid)
    record = [r['payload'] for r in service.detail(cid)['timeline'] if r['kind'] == 'routing'][-1]
    assert record['mode'] == 'jev_route' and models['claude'][-1]['route'] == 'close_item'


def test_decide_is_conservative():
    context = {'case': {'first_report': True, 'current_action': 'clarify'}, 'open_questions': []}
    s = DEFAULT_SETTINGS
    assert jev.decide(answers(), context, s)['mode'] == 'jev_only'
    assert jev.decide(answers(confidence=0.7), context, s)['mode'] == 'jev_route'
    assert jev.decide(answers(sensitive=0.5), context, s)['mode'] == 'jev_route'
    assert jev.decide(answers(route='confirm_appointment'), context, s)['mode'] == 'jev_route'
    assert jev.decide(answers(), {**context, 'open_questions': [{'id': 'q'}]}, s)['mode'] == 'jev_route'
    assert jev.decide(answers(route='urgent_hazard', confidence=0.3), context, s)['route'] == 'urgent_hazard'


def test_router_settings_are_validated():
    with pytest.raises(ValueError):
        PolicyInput(base_version=1, settings={'router': 'keywords'})
    with pytest.raises(ValueError):
        PolicyInput(base_version=1, settings={'router_jev_only_routes': ['instruct_work']})
    with pytest.raises(ValueError):
        PolicyInput(base_version=1, settings={'router_min_confidence': 0.9, 'router_jev_only_confidence': 0.6})
    with pytest.raises(ValueError):
        PolicyInput(base_version=1, settings={'router_hazard_threshold': 1.5})
