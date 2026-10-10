"""Fictional planning fixtures; no BUILD/EVAL access or external operations."""
from datetime import timedelta

import pytest
from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from fastapi.testclient import TestClient

from app import service as service_module
from app.domain import ClaimInput, EvidenceInput, Intake, PolicyInput, ReviewResponse, now, stamp
from app.portfolio import create_portfolio_router
from app.service import Conflict, Forbidden, Service
from app.store import Store


MANAGER = {'id': 'fictional-manager', 'role': 'case_manager'}


@pytest.fixture
def service(tmp_path, monkeypatch):
    instance = Service(Store('sqlite:///' + str(tmp_path / 'portfolio.db')))
    monkeypatch.setattr(service_module, '_service', instance)
    return instance


@pytest.fixture
def client(service):
    app = FastAPI()

    def actor(request: Request):
        role = request.headers.get('x-test-role')
        if role is None:
            raise Forbidden('Staff authentication required')
        return {'id': 'fictional-' + role, 'role': role}

    @app.exception_handler(Forbidden)
    async def forbidden(request, exc):
        return JSONResponse({'detail': str(exc)}, 403)

    @app.exception_handler(Conflict)
    async def conflict(request, exc):
        return JSONResponse({'detail': str(exc)}, 409)

    @app.exception_handler(ValueError)
    async def invalid(request, exc):
        return JSONResponse({'detail': str(exc)}, 400)

    app.include_router(create_portfolio_router(actor))
    with TestClient(app) as result:
        yield result


def post(client, path, data, role='case_manager'):
    return client.post('/api/portfolio' + path, json=data, headers={'x-test-role': role})


def overview(client, role='case_manager'):
    return client.get('/api/portfolio', headers={'x-test-role': role})


def new_case(service, title='Fictional leaking tap', property_ref='UNVERIFIED-FLAT-A', category='plumbing'):
    return service.intake(Intake(title=title, property_ref=property_ref, report='A fictional tap is leaking.',
                                category=category, action='request_quote', work_item='Kitchen tap', triage='staff'), MANAGER)['case']


def profile(client, case, **overrides):
    data = {'property_key': 'fictional-building-a', 'asset_ref': '', 'trade': 'plumbing',
            'reason': 'Staff confirmed the grouping from a fictional property register.'}
    data.update(overrides)
    response = post(client, f'/cases/{case["id"]}/profile', data)
    assert response.status_code == 200, response.text
    return response.json()


def resource(client, **overrides):
    data = {'name': 'Fictional local plumber', 'trades': ['plumbing'],
            'available_from': '2026-12-01T09:00:00+00:00', 'available_until': '2026-12-01T17:00:00+00:00',
            'reason': 'Fictional staff-supplied availability.'}
    data.update(overrides)
    response = post(client, '/contractors', data)
    assert response.status_code == 200, response.text
    return response.json()


def plan_request(contractor, cases, **overrides):
    data = {'contractor_id': contractor['id'], 'case_ids': [case['id'] for case in cases],
            'start': '2026-12-01T10:00:00Z', 'end': '2026-12-01T11:00:00Z',
            'reason': 'Tentative visit for staff review only.'}
    data.update(overrides)
    return data


def test_read_requires_staff_and_every_mutation_requires_manager(client, service):
    case = new_case(service)
    p = profile(client, case)
    contractor = resource(client)
    first_plan = post(client, '/plans', plan_request(contractor, [case])).json()
    second = new_case(service, property_ref='UNVERIFIED-FLAT-B')
    profile(client, second)
    incident = post(client, '/incidents', {'case_ids': [case['id'], second['id']], 'title': 'Fictional shared pipe', 'reason': 'Staff checked this link.'}).json()
    assert client.get('/api/portfolio').status_code == 403
    assert overview(client, 'tenant').status_code == 403
    assert overview(client, 'access_officer').status_code == 200
    attempts = [
        (f'/cases/{case["id"]}/profile', {k: p[k] for k in ['property_key', 'asset_ref', 'trade', 'reason']}),
        ('/contractors', {k: contractor[k] for k in ['name', 'trades', 'available_from', 'available_until', 'reason']}),
        ('/incidents', {'case_ids': [case['id'], second['id']], 'title': 'Duplicate', 'reason': 'Fictional reason'}),
        (f'/incidents/{incident["id"]}/status', {'status': 'resolved', 'reason': 'Reviewed link'}),
        ('/plans', plan_request(contractor, [case])),
        (f'/plans/{first_plan["id"]}/cancel', {'reason': 'Fictional cancellation'}),
    ]
    for path, data in attempts:
        assert post(client, path, data, role='approver').status_code == 403


def test_grouping_and_planning_never_modify_case_facts_permissions_or_actions(client, service):
    cases = [new_case(service), new_case(service, property_ref='UNVERIFIED-FLAT-B')]
    before = {case['id']: service.detail(case['id']) for case in cases}
    for case in cases:
        profile(client, case)
    incident = post(client, '/incidents', {'case_ids': [case['id'] for case in cases], 'title': 'Possible shared leak', 'reason': 'Staff checked these sources.'})
    assert incident.status_code == 200, incident.text
    contractor = resource(client)
    result = post(client, '/plans', plan_request(contractor, cases))
    assert result.status_code == 200, result.text
    plan = result.json()
    assert plan['status'] == 'tentative'
    assert not plan['stale']
    for case in cases:
        after = service.detail(case['id'])
        for key in ['case', 'claims', 'evidence', 'actions', 'reviews', 'questions', 'decision']:
            assert after[key] == before[case['id']][key], key
        blockers = [row for row in plan['blockers'] if row['case_id'] == case['id']]
        assert {'access', 'authority', 'schedule', 'planned_visit', 'planning_window'} <= {row['key'] for row in blockers}
    assert all(row['access_status'] == 'UNKNOWN' for row in plan['cases'])


def test_suggestions_require_confirmed_property_and_bounded_intake_time(client, service):
    first, second, third = [new_case(service, property_ref='FICTIONAL-' + suffix) for suffix in ['A', 'B', 'C']]
    assert overview(client).json()['suggestions'] == []
    profile(client, first)
    profile(client, second)
    profile(client, third, property_key='different-building')
    suggestions = overview(client).json()['suggestions']
    assert len(suggestions) == 1
    assert set(suggestions[0]['case_ids']) == {first['id'], second['id']}
    assert suggestions[0]['status'] == 'possible'
    assert suggestions[0]['window_days'] == 30
    assert 'intake' in suggestions[0]['time_basis']
    assert all(signal['source_record_ids'] for signal in suggestions[0]['signals'])
    with service.db.tx() as connection:
        old = service.db.case(connection, second['id'])
        old['created_at'] = stamp(now() - timedelta(days=31))
        service.db.save_case(connection, old)
    assert overview(client).json()['suggestions'] == []


def test_incident_rejects_cross_property_and_duplicate_case_ids_and_keeps_closure_separate(client, service):
    first, second = new_case(service), new_case(service, property_ref='FICTIONAL-B')
    profile(client, first)
    profile(client, second, property_key='different-building')
    data = {'case_ids': [first['id'], second['id']], 'title': 'Fictional incident', 'reason': 'Staff-confirmed link'}
    assert post(client, '/incidents', data).status_code == 400
    assert post(client, '/incidents', {**data, 'case_ids': [first['id'], first['id']]}).status_code == 422
    profile(client, second)
    incident = post(client, '/incidents', data).json()
    assert incident['source_record_ids'] and incident['actor']['role'] == 'case_manager'
    assert post(client, '/incidents', {**data, 'case_ids': list(reversed(data['case_ids']))}).status_code == 409
    assert overview(client).json()['suggestions'] == []
    profile(client, second, asset_ref='changed grouping detail')
    updated = overview(client).json()['incidents'][0]
    assert updated['stale'] and updated['stale_case_ids'] == [second['id']]
    before = service.detail(first['id'])['case']
    response = post(client, f'/incidents/{incident["id"]}/status', {'status': 'resolved', 'reason': 'Investigation link resolved only.'})
    assert response.status_code == 200
    assert response.json()['status'] == 'resolved'
    assert service.detail(first['id'])['case'] == before
    assert post(client, f'/incidents/{incident["id"]}/status', {'status': 'dismissed', 'reason': 'Already terminal'}).status_code == 409


@pytest.mark.parametrize('change', [
    {'start': '2026-12-01T10:00:00'},
    {'start': 1796119200},
    {'end': '2026-12-01T09:00:00Z'},
    {'dispatch': True},
    {'reason': '  '},
])
def test_plan_rejects_invalid_or_ambiguous_input(client, service, change):
    case = new_case(service)
    profile(client, case)
    contractor = resource(client)
    assert post(client, '/plans', plan_request(contractor, [case], **change)).status_code == 422


def test_plan_windows_trade_and_missing_references(client, service):
    case = new_case(service)
    contractor = resource(client)
    assert post(client, '/plans', plan_request(contractor, [case])).status_code == 400
    profile(client, case, window_start='2026-12-01T10:00:00Z', window_end='2026-12-01T12:00:00Z')
    assert post(client, '/plans', plan_request(contractor, [case], start='2026-12-01T09:00:00Z')).status_code == 400
    assert post(client, '/plans', plan_request(contractor, [case], end='2026-12-01T18:00:00Z')).status_code == 400
    wrong_trade = resource(client, name='Fictional gardener', trades=['gardening'])
    assert post(client, '/plans', plan_request(wrong_trade, [case])).status_code == 400
    assert post(client, '/plans', plan_request(contractor, [case], contractor_id='missing')).status_code == 400
    assert post(client, '/plans', plan_request(contractor, [case], case_ids=[case['id'], case['id']])).status_code == 422
    assert post(client, '/plans', plan_request(contractor, [case])).status_code == 200


def test_conflicts_are_transactional_cancel_releases_slot_and_adjacency_allowed(client, service):
    first, second = new_case(service), new_case(service)
    for case in [first, second]:
        profile(client, case)
    contractor, other = resource(client), resource(client, name='Second fictional resource')
    created = post(client, '/plans', plan_request(contractor, [first])).json()
    assert post(client, '/plans', plan_request(contractor, [second])).status_code == 409
    assert post(client, '/plans', plan_request(other, [first])).status_code == 409
    assert post(client, '/plans', plan_request(contractor, [second], start='2026-12-01T11:00:00Z', end='2026-12-01T12:00:00Z')).status_code == 200
    assert post(client, f'/plans/{created["id"]}/cancel', {'reason': 'A revised plan is required.'}).status_code == 200
    assert post(client, '/plans', plan_request(contractor, [first])).status_code == 200
    assert post(client, f'/plans/{created["id"]}/cancel', {'reason': 'Cannot cancel twice.'}).status_code == 409


def test_append_only_audit_restart_and_staleness(client, service, monkeypatch):
    case = new_case(service)
    first_profile = profile(client, case)
    contractor = resource(client)
    created = post(client, '/plans', plan_request(contractor, [case])).json()
    db_url = str(service.db.engine.url)
    replacement = Service(Store(db_url))
    monkeypatch.setattr(service_module, '_service', replacement)
    saved = overview(client).json()
    assert saved['profiles'][0]['id'] == first_profile['id']
    assert saved['contractors'][0]['id'] == contractor['id']
    assert saved['plans'][0]['id'] == created['id']
    assert not saved['plans'][0]['stale']
    next_profile = profile(client, case, asset_ref='Fictional main pipe')
    assert next_profile['supersedes'] == first_profile['id']
    assert overview(client).json()['plans'][0]['stale_case_ids'] == [case['id']]
    with replacement.db.tx() as connection:
        profiles = replacement.db.list(connection, 'portfolio_profile', case['id'])
        assert len(profiles) == 2
        assert profiles[0]['payload']['asset_ref'] == ''
        assert profiles[1]['payload']['actor']['role'] == 'case_manager'


def test_new_evidence_or_policy_makes_existing_plan_stale(client, service):
    case = new_case(service)
    profile(client, case)
    contractor = resource(client)
    post(client, '/plans', plan_request(contractor, [case]))
    service.evidence(case['id'], EvidenceInput(text='Additional fictional inspection information.', source_label='Fictional follow-up'), MANAGER)
    changed = overview(client).json()['plans'][0]
    assert changed['stale']
    assert changed['cases'][0]['current_revision'] > changed['cases'][0]['captured_revision']


def test_policy_publication_marks_plan_stale_without_granting_authority(client, service):
    case = new_case(service)
    profile(client, case)
    contractor = resource(client)
    post(client, '/plans', plan_request(contractor, [case]))
    with service.db.tx() as connection:
        active = service.active(connection)
    editor = {'id': 'fictional-policy-editor', 'role': 'policy_editor'}
    draft = service.draft(PolicyInput(base_version=active['version'], settings=active['settings'],
                                     reason='Fictional policy revision for a stale planning test.'), editor)
    service.preview(draft['id'], editor)
    service.publish(draft['id'], editor)
    changed = overview(client).json()['plans'][0]
    assert changed['stale']
    assert 'authority' in {blocker['key'] for blocker in changed['blockers']}


def test_multiple_properties_warn_about_unchecked_travel_and_resource_names_are_unique(client, service):
    first, second = new_case(service), new_case(service)
    profile(client, first)
    profile(client, second, property_key='different-fictional-building')
    contractor = resource(client)
    plan = post(client, '/plans', plan_request(contractor, [first, second])).json()
    assert plan['travel_checked'] is False
    assert 'between properties' in plan['planning_warning']
    request = {key: contractor[key] for key in ['name', 'trades', 'available_from', 'available_until', 'reason']}
    assert post(client, '/contractors', {**request, 'name': request['name'].upper()}).status_code == 409


def test_stale_plan_explains_current_trade_and_window_conflicts(client, service):
    case = new_case(service)
    profile(client, case)
    contractor = resource(client)
    post(client, '/plans', plan_request(contractor, [case]))
    profile(client, case, trade='electrical', window_start='2026-12-01T13:00:00Z', window_end='2026-12-01T15:00:00Z')
    plan = overview(client).json()['plans'][0]
    assert plan['stale']
    assert {'planning_trade', 'planning_window_conflict'} <= {blocker['key'] for blocker in plan['blockers']}
    assert plan['cases'][0]['outcome'] == 'STOP ACTION'


def test_dismissed_suggestion_stays_dismissed_until_new_source_or_profile(client, service):
    cases = [new_case(service), new_case(service)]
    for case in cases:
        profile(client, case)
    data = {'case_ids': [case['id'] for case in cases], 'title': 'Fictional investigation', 'reason': 'Possible link reviewed by staff.'}
    incident = post(client, '/incidents', data).json()
    post(client, f'/incidents/{incident["id"]}/status', {'status': 'dismissed', 'reason': 'The two faults are independent.'})
    assert overview(client).json()['suggestions'] == []
    service.evidence(cases[0]['id'], EvidenceInput(text='New fictional information about the shared water supply.', source_label='Fictional new report'), MANAGER)
    assert len(overview(client).json()['suggestions']) == 1


def test_direct_suggestion_dismissal_is_audited_role_checked_and_snapshot_scoped(client, service):
    cases = [new_case(service), new_case(service)]
    for case in cases:
        profile(client, case)
    suggestion = overview(client).json()['suggestions'][0]
    endpoint = f'/suggestions/{suggestion["id"]}/dismiss'
    request = {'reason': 'Staff checked the reports; these are unrelated fixtures.'}
    assert post(client, endpoint, request, role='reviewer').status_code == 403
    response = post(client, endpoint, request)
    assert response.status_code == 200, response.text
    assert response.json()['source_record_ids']
    assert overview(client).json()['suggestions'] == []
    assert overview(client).json()['incidents'] == []
    assert post(client, endpoint, request).status_code == 409
    service.evidence(cases[0]['id'], EvidenceInput(text='New fictional shared boiler failure information.', source_label='New fictional report'), MANAGER)
    changed = overview(client).json()['suggestions'][0]
    assert changed['id'] != suggestion['id']
    stale_endpoint = f'/suggestions/{changed["id"]}/dismiss'
    profile(client, cases[0], asset_ref='A new verified planning reference')
    assert post(client, stale_endpoint, request).status_code == 409


def test_confirmed_larger_incident_suppresses_its_subsets_and_resolved_waits_for_new_source(client, service):
    cases = [new_case(service) for _ in range(3)]
    for case in cases:
        profile(client, case)
    assert len(overview(client).json()['suggestions']) == 3
    incident = post(client, '/incidents', {'case_ids': [case['id'] for case in cases], 'title': 'Fictional building incident', 'reason': 'Staff confirmed the three related reports.'}).json()
    assert overview(client).json()['suggestions'] == []
    post(client, f'/incidents/{incident["id"]}/status', {'status': 'resolved', 'reason': 'The shared investigation is complete.'})
    assert overview(client).json()['suggestions'] == []
    service.evidence(cases[0]['id'], EvidenceInput(text='A further fictional related leak report.', source_label='New fictional report'), MANAGER)
    suggestions = overview(client).json()['suggestions']
    assert len(suggestions) == 2
    assert all(cases[0]['id'] in item['case_ids'] for item in suggestions)


@pytest.mark.parametrize('status', ['resolved', 'dismissed'])
def test_terminal_incident_records_the_latest_reviewed_sources(client, service, status):
    cases = [new_case(service), new_case(service)]
    for case in cases:
        profile(client, case)
    incident = post(client, '/incidents', {'case_ids': [case['id'] for case in cases], 'title': 'Fictional investigation', 'reason': 'Related reports confirmed.'}).json()
    service.evidence(cases[0]['id'], EvidenceInput(text='Additional fictional evidence staff will review now.', source_label='Fictional report before decision'), MANAGER)
    terminal = post(client, f'/incidents/{incident["id"]}/status', {'status': status, 'reason': 'Staff reviewed all the latest evidence.'}).json()
    assert terminal['status_change']['source_record_ids']
    assert overview(client).json()['suggestions'] == []
    service.evidence(cases[0]['id'], EvidenceInput(text='Another fictional report arrived after the decision.', source_label='Fictional report after decision'), MANAGER)
    assert len(overview(client).json()['suggestions']) == 1


def test_early_local_terminal_records_without_snapshot_remain_readable(client, service):
    cases = [new_case(service), new_case(service)]
    for case in cases:
        profile(client, case)
    incident = post(client, '/incidents', {'case_ids': [case['id'] for case in cases], 'title': 'Earlier fictional link', 'reason': 'A pre-snapshot local fixture.'}).json()
    with service.db.tx() as connection:
        service.db.add(connection, 'portfolio_incident_status', {
            'incident_id': incident['id'], 'status': 'dismissed', 'reason': 'Earlier local record.', 'actor': MANAGER})
    response = overview(client)
    assert response.status_code == 200, response.text
    assert response.json()['suggestions'] == []


def test_verified_access_stays_with_its_case_when_grouped_and_planned(client, service):
    first = service.intake(Intake(title='Fictional appointment', property_ref='FICTIONAL-A',
                                 report='Fictional plumbing appointment needed.', category='plumbing',
                                 action='confirm_appointment', work_item='Kitchen tap', triage='staff'), MANAGER)['case']
    second = new_case(service, property_ref='FICTIONAL-B')
    source = 'Fictional resident consents to the current scoped visit.'
    detail = service.evidence(first['id'], EvidenceInput(text=source, source_label='Fictional consent',
                             claims=[ClaimInput(key='access', value=True, source_quote=source)]), MANAGER)
    review = next(row for row in detail['reviews'] if row['key'] == 'access' and row['status'] == 'open')
    claim = next(row for row in detail['claims'] if row['key'] == 'access')
    service.respond(review['id'], ReviewResponse(decision='correct', reason='Checked this case and current visit only.',
                    claim_id=claim['id'], source_id=claim['source_id']), {'id': 'fictional-access', 'role': 'access_officer'})
    for case in [first, second]:
        profile(client, case)
    post(client, '/incidents', {'case_ids': [first['id'], second['id']], 'title': 'Related fictional plumbing', 'reason': 'Staff confirmed related investigation only.'})
    contractor = resource(client)
    plan = post(client, '/plans', plan_request(contractor, [first, second])).json()
    checks = {item['case_id']: item for item in plan['cases']}
    assert checks[first['id']]['access_status'] == 'PASS'
    assert checks[second['id']]['access_status'] == 'UNKNOWN'
    assert all('planned_visit' in {blocker['key'] for blocker in item['blockers']} for item in checks.values())
    assert not any(claim['key'] == 'access' for claim in service.detail(second['id'])['claims'])


def test_profile_validation_is_bounded_and_cannot_claim_permissions(client, service):
    case = new_case(service)
    base = {'property_key': 'fictional-building', 'trade': 'plumbing', 'reason': 'Reviewed planning label'}
    for changes in [{'property_key': ' '}, {'property_key': 123}, {'asset_ref': 'a' * 201}, {'access': True},
                    {'window_start': '2026-12-01T10:00:00Z'}, {'window_start': '2026-12-01T10:00:00', 'window_end': '2026-12-01T11:00:00Z'}]:
        assert post(client, f'/cases/{case["id"]}/profile', {**base, **changes}).status_code == 422
    assert post(client, '/cases/missing/profile', base).status_code == 400


def test_profile_group_keys_match_server_unicode_casefold_without_rewriting_sources(client, service):
    first, second = new_case(service), new_case(service)
    first_profile = profile(client, first, property_key='Straße-A', asset_ref='Rohr-ß')
    second_profile = profile(client, second, property_key='STRASSE-A', asset_ref='ROHR-SS')
    assert first_profile['property_group_key'] == second_profile['property_group_key'] == 'strasse-a'
    assert first_profile['asset_group_key'] == second_profile['asset_group_key'] == 'rohr-ss'
    saved = overview(client).json()
    assert {item['property_group_key'] for item in saved['profiles']} == {'strasse-a'}
    assert {item['property_key'] for item in saved['profiles']} == {'Straße-A', 'STRASSE-A'}
    assert len(saved['suggestions']) == 1
    with service.db.tx() as connection:
        raw = service.db.get_record(connection, first_profile['id'])['payload']
    assert raw['property_key'] == 'Straße-A' and raw['asset_ref'] == 'Rohr-ß'
    assert 'property_group_key' not in raw and 'asset_group_key' not in raw
