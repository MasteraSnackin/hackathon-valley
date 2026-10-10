"""Staff planning projections; grouping and scheduling never grant case authority.

Every mutation appends an audit record. The existing case policy, conversations,
claims and proposed actions remain untouched. Resources and windows are supplied
by staff and are not connected to a contractor booking or messaging service.
"""
from __future__ import annotations

from collections import defaultdict
from copy import deepcopy
from datetime import datetime, timedelta
import re
from typing import Annotated, Literal

from fastapi import APIRouter, Depends
from pydantic import AwareDatetime, BaseModel, ConfigDict, Field, StringConstraints, field_validator, model_validator

from .domain import ROLES, digest, dt, evaluate
from .service import Conflict, get_service
from .store import payload

Text = Annotated[str, StringConstraints(strict=True, strip_whitespace=True, min_length=1, max_length=200)]
Reason = Annotated[str, StringConstraints(strict=True, strip_whitespace=True, min_length=3, max_length=2000)]
Identifier = Annotated[str, StringConstraints(strict=True, min_length=1, max_length=80, pattern=r'^[A-Za-z0-9_-]+$')]
Asset = Annotated[str, StringConstraints(strict=True, strip_whitespace=True, max_length=200)]
NOTICE = 'Tentative local planning only. No contractor booking, dispatch, permission or authority is created.'
PROFILE_NOTICE = 'Staff-confirmed grouping metadata only; original identity, address and access checks remain separate.'


class Input(BaseModel):
    model_config = ConfigDict(extra='forbid')

    @field_validator('*', mode='before')
    @classmethod
    def no_numeric_dates(cls, value, info):
        if info.field_name in {'window_start', 'window_end', 'available_from', 'available_until', 'start', 'end'}:
            if value is not None and not isinstance(value, (str, datetime)):
                raise ValueError('Use an ISO timestamp with an explicit timezone')
        return value


class ProfileInput(Input):
    property_key: Text
    asset_ref: Asset = ''
    trade: Text
    window_start: AwareDatetime | None = None
    window_end: AwareDatetime | None = None
    reason: Reason

    @model_validator(mode='after')
    def windows(self):
        if (self.window_start is None) != (self.window_end is None):
            raise ValueError('Provide both appointment window timestamps, or neither')
        if self.window_start is not None and self.window_end <= self.window_start:
            raise ValueError('The appointment window must end after it starts')
        return self


class IncidentInput(Input):
    case_ids: list[Identifier] = Field(min_length=2, max_length=50, strict=True)
    title: Text
    reason: Reason

    @field_validator('case_ids')
    @classmethod
    def unique(cls, ids):
        if len(ids) != len(set(ids)):
            raise ValueError('Case IDs must be unique')
        return ids


class IncidentStatusInput(Input):
    status: Literal['resolved', 'dismissed']
    reason: Reason


class ContractorInput(Input):
    name: Text
    trades: list[Text] = Field(min_length=1, max_length=15, strict=True)
    available_from: AwareDatetime
    available_until: AwareDatetime
    reason: Reason

    @model_validator(mode='after')
    def valid(self):
        if self.available_until <= self.available_from:
            raise ValueError('Availability must end after it starts')
        if len({trade.casefold() for trade in self.trades}) != len(self.trades):
            raise ValueError('Trades must be unique')
        return self


class PlanInput(Input):
    contractor_id: Identifier
    case_ids: list[Identifier] = Field(min_length=1, max_length=50, strict=True)
    start: AwareDatetime
    end: AwareDatetime
    reason: Reason

    @model_validator(mode='after')
    def valid(self):
        if self.end <= self.start:
            raise ValueError('The plan must end after it starts')
        if len(self.case_ids) != len(set(self.case_ids)):
            raise ValueError('Case IDs must be unique')
        return self


class ReasonInput(Input):
    reason: Reason


def _rows(service, connection, kind):
    return [payload(row) for row in service.db.list(connection, 'portfolio_' + kind)]


def _profile_view(row):
    # Normalisation keys keep browser grouping consistent with the server.
    # They are projections, not new address or asset verification claims.
    return {**row, 'property_group_key': row['property_key'].casefold(),
            'asset_group_key': row['asset_ref'].casefold()}


def _profiles(service, connection):
    return {row['case_id']: _profile_view(row) for row in _rows(service, connection, 'profile')}


def _require_profile(service, connection, case_id, profiles):
    case = service.db.case(connection, case_id)
    profile = profiles.get(case_id)
    if profile is None:
        raise ValueError('Set staff-confirmed planning metadata for every selected case first')
    return case, profile


def _source_ids(service, connection, case_id):
    # References establish which local sources were available; they do not
    # silently verify their assertions or copy their permission to other cases.
    return [row['id'] for row in service.db.list(connection, 'evidence', case_id)]


def _incidents(service, connection, profiles):
    updates = {row['incident_id']: row for row in _rows(service, connection, 'incident_status')}
    result = []
    for row in _rows(service, connection, 'incident'):
        update = updates.get(row['id'])
        stale = [cid for cid in row['case_ids'] if profiles.get(cid, {}).get('id') != row['profile_ids'][cid]]
        result.append({**row, 'status': update['status'] if update else 'confirmed',
                       'status_change': update, 'stale': bool(stale), 'stale_case_ids': stale})
    return result


def _planning_checks(service, connection, case, profile, policy):
    # Re-evaluate at read time so expired approvals and new policy are visible.
    # Add access/authority/schedule solely to this read-only inspection policy;
    # never persist this policy or a derived decision into the workflow.
    inspection = deepcopy(policy)
    required = inspection['settings'].setdefault('required_per_action', {})
    action = case['proposal']['action']
    required[action] = list(dict.fromkeys(required.get(action, []) + ['access', 'authority', 'schedule']))
    decision = evaluate(case, service.claims(connection, case['id']),
                        service.approvals(connection, case['id']), inspection,
                        uncertain=any(row['status'] == 'uncertain' for row in service.action_states(connection, case['id'])))
    blockers = [{**row, 'case_id': case['id']} for row in decision['blockers']]
    if not profile.get('window_start'):
        blockers.append({'case_id': case['id'], 'key': 'planning_window', 'status': 'UNKNOWN',
                         'reason': 'No staff-supplied appointment window is recorded.', 'owner': 'case_manager'})
    blockers.append({'case_id': case['id'], 'key': 'planned_visit', 'status': 'UNKNOWN',
                     'reason': 'The planned contractor and time are not a confirmed appointment. Existing case checks do not grant permission for this plan.',
                     'owner': 'case_manager'})
    access = next((row['status'] for row in decision['checks'] if row['key'] == 'access'), 'UNKNOWN')
    return {'case_id': case['id'], 'title': case['title'], 'current_revision': case['revision'],
            'outcome': decision['outcome'] if decision['blockers'] else 'WAIT',
            'policy_outcome': decision['outcome'], 'access_status': access, 'blockers': blockers}


def _plans(service, connection, profiles, policy):
    cancellations = {row['plan_id']: row for row in _rows(service, connection, 'plan_cancelled')}
    resources = {row['id']: row for row in _rows(service, connection, 'contractor')}
    result = []
    for row in _rows(service, connection, 'plan'):
        details = []
        for cid in row['case_ids']:
            case, profile = _require_profile(service, connection, cid, profiles)
            stale = (case['revision'] != row['case_revisions'][cid]
                     or profile['id'] != row['profile_ids'][cid]
                     or policy['version'] != row['policy_version'])
            checks = _planning_checks(service, connection, case, profile, policy)
            if profile['trade'].casefold() not in {trade.casefold() for trade in resources[row['contractor_id']]['trades']}:
                checks['blockers'].append({'case_id': cid, 'key': 'planning_trade', 'status': 'FAIL',
                                           'reason': 'The latest case trade no longer matches the planned contractor.', 'owner': 'case_manager'})
                checks['outcome'] = 'STOP ACTION'
            if profile.get('window_start') and (dt(row['start']) < dt(profile['window_start']) or dt(row['end']) > dt(profile['window_end'])):
                checks['blockers'].append({'case_id': cid, 'key': 'planning_window_conflict', 'status': 'FAIL',
                                           'reason': 'The tentative plan is outside the latest case appointment window.', 'owner': 'case_manager'})
                checks['outcome'] = 'STOP ACTION'
            details.append({**checks, 'captured_revision': row['case_revisions'][cid], 'stale': stale})
        stale_ids = [item['case_id'] for item in details if item['stale']]
        property_keys = {profiles[cid]['property_key'].casefold() for cid in row['case_ids']}
        result.append({**row, 'status': 'cancelled' if row['id'] in cancellations else 'tentative',
                       'cancellation': cancellations.get(row['id']), 'stale': bool(stale_ids),
                       'stale_case_ids': stale_ids, 'cases': details,
                       'blockers': [blocker for item in details for blocker in item['blockers']],
                       'travel_checked': False,
                       'planning_warning': ('Travel between properties is not checked. Staff must allow travel time and confirm the route.'
                                            if len(property_keys) > 1 else 'Job durations and contractor travel are not checked; staff must confirm feasibility.'),
                       'notice': NOTICE})
    return result


def _signals(service, connection, case, profile):
    evidence = service.db.list(connection, 'evidence', case['id'])
    words = re.findall(r'[a-z]{3,}', ' '.join(row['payload'].get('text', '') for row in evidence).lower())
    symptoms = sorted(set(words) & {'leak', 'leaking', 'flood', 'flooding', 'boiler', 'heating',
                                    'water', 'mould', 'damp', 'blocked', 'broken', 'lock', 'window'})
    return {'case_id': case['id'], 'title': case['title'], 'category': case.get('category', 'other'),
            'work_item': case['proposal'].get('work_item', ''), 'asset_ref': profile['asset_ref'],
            'symptoms': symptoms, 'reported_at': case['created_at'],
            'source_record_ids': [profile['id']] + [row['id'] for row in evidence]}


def _review_snapshot(incident):
    terminal = incident.get('status_change') or {}
    # Early local records lacked a terminal snapshot; retain compatibility
    # without rewriting the append-only history.
    return terminal if 'profile_ids' in terminal and 'case_revisions' in terminal else incident


def _suggestions(service, connection, profiles, incidents):
    groups = defaultdict(list)
    for case in service.db.case_list(connection):
        profile = profiles.get(case['id'])
        if profile:
            groups[profile['property_key'].casefold()].append(_signals(service, connection, case, profile))
    case_revisions = {case['id']: case['revision'] for case in service.db.case_list(connection)}
    dismissed = {row['suggestion_id'] for row in _rows(service, connection, 'suggestion_dismissed')}
    suggestions = []
    for members in groups.values():
        members.sort(key=lambda row: (row['reported_at'], row['case_id']))
        for index, first in enumerate(members):
            # Pairwise candidates avoid a chain of nearby events falsely making
            # one incident whose earliest/latest reports exceed the time bound.
            for second in members[index + 1:]:
                if abs(dt(second['reported_at']) - dt(first['reported_at'])) > timedelta(days=30):
                    continue
                ids = sorted([first['case_id'], second['case_id']])
                if any(set(ids) <= set(row['case_ids']) and (row['status'] == 'confirmed' or (
                    all(profiles.get(cid, {}).get('id') == _review_snapshot(row)['profile_ids'][cid] for cid in ids)
                    and all(case_revisions.get(cid) == _review_snapshot(row).get('case_revisions', {}).get(cid) for cid in ids)))
                       for row in incidents):
                    continue
                matches = []
                if first['category'] == second['category'] and first['category'] != 'other':
                    matches.append('same recorded category: ' + first['category'])
                if first['asset_ref'] and first['asset_ref'].casefold() == second['asset_ref'].casefold():
                    matches.append('same staff-supplied asset reference')
                work = first['work_item'].strip().casefold()
                if work and work not in {'reported maintenance', 'recorded request; scope unverified'} and work == second['work_item'].strip().casefold():
                    matches.append('same recorded work item')
                symptoms = sorted(set(first['symptoms']) & set(second['symptoms']))
                if symptoms:
                    matches.append('shared source terms: ' + ', '.join(symptoms))
                if not matches:
                    continue
                key = profiles[first['case_id']]['property_key']
                suggestion_id = digest({'case_ids': ids, 'profile_ids': [profiles[cid]['id'] for cid in ids],
                                        'case_revisions': [case_revisions[cid] for cid in ids],
                                        'source_record_ids': sorted(first['source_record_ids'] + second['source_record_ids'])})
                if suggestion_id in dismissed:
                    continue
                suggestions.append({'id': suggestion_id,
                                    'status': 'possible', 'property_key': key, 'case_ids': ids,
                                    'reason': '; '.join(matches) + '. A manager must check whether the cause is shared.',
                                    'signals': [first, second], 'window_days': 30,
                                    'time_basis': 'Case intake timestamps, not verified incident occurrence dates.'})
    return suggestions


def create_portfolio_router(actor):
    router = APIRouter(prefix='/api/portfolio', tags=['staff portfolio planning'])

    @router.get('')
    def overview(who=Depends(actor)):
        service = get_service()
        service.role(who, ROLES)
        with service.db.tx() as connection:
            profiles = _profiles(service, connection)
            incidents = _incidents(service, connection, profiles)
            return {'profiles': list(profiles.values()), 'contractors': _rows(service, connection, 'contractor'),
                    'incidents': incidents, 'suggestions': _suggestions(service, connection, profiles, incidents),
                    'plans': _plans(service, connection, profiles, service.active(connection))}

    @router.post('/cases/{cid}/profile')
    def profile(cid: str, data: ProfileInput, who=Depends(actor)):
        service = get_service()
        service.role(who, {'case_manager'})
        with service.db.tx() as connection:
            case = service.db.case(connection, cid)
            previous = _profiles(service, connection).get(cid)
            values = data.model_dump(mode='json')
            row, _ = service.db.add(connection, 'portfolio_profile', {
                **values, 'case_id': cid, 'original_property_ref': case['property_ref'],
                'case_revision': case['revision'], 'actor': who,
                'supersedes': previous['id'] if previous else None,
                'source_record_ids': _source_ids(service, connection, cid), 'notice': PROFILE_NOTICE}, cid)
            return _profile_view(payload(row))

    @router.post('/suggestions/{suggestion_id}/dismiss')
    def dismiss_suggestion(suggestion_id: str, data: ReasonInput, who=Depends(actor)):
        service = get_service()
        service.role(who, {'case_manager'})
        with service.db.tx() as connection:
            if any(row['suggestion_id'] == suggestion_id for row in _rows(service, connection, 'suggestion_dismissed')):
                raise Conflict('This suggestion snapshot is already dismissed')
            profiles = _profiles(service, connection)
            suggestion = next((row for row in _suggestions(service, connection, profiles, _incidents(service, connection, profiles))
                               if row['id'] == suggestion_id), None)
            if suggestion is None:
                raise Conflict('This suggestion is no longer current; refresh before reviewing it')
            row, _ = service.db.add(connection, 'portfolio_suggestion_dismissed', {
                'suggestion_id': suggestion_id, 'case_ids': suggestion['case_ids'], 'reason': data.reason,
                'source_record_ids': sorted({rid for signal in suggestion['signals'] for rid in signal['source_record_ids']}),
                'actor': who, 'notice': 'This snapshot was dismissed; new source evidence or grouping metadata may warrant another review.'})
            return {**payload(row), 'status': 'dismissed'}

    @router.post('/incidents')
    def create_incident(data: IncidentInput, who=Depends(actor)):
        service = get_service()
        service.role(who, {'case_manager'})
        with service.db.tx() as connection:
            profiles = _profiles(service, connection)
            selected = [_require_profile(service, connection, cid, profiles) for cid in data.case_ids]
            if len({profile['property_key'].casefold() for _, profile in selected}) != 1:
                raise ValueError('A related incident needs the same staff-confirmed property key for every case')
            ids = sorted(data.case_ids)
            if any(sorted(row['case_ids']) == ids and row['status'] == 'confirmed'
                   for row in _incidents(service, connection, profiles)):
                raise Conflict('These cases already have a confirmed incident link')
            row, _ = service.db.add(connection, 'portfolio_incident', {
                **data.model_dump(mode='json'), 'case_ids': ids, 'property_key': selected[0][1]['property_key'],
                'profile_ids': {case['id']: profile['id'] for case, profile in selected},
                'case_revisions': {case['id']: case['revision'] for case, _ in selected},
                'source_record_ids': sorted({rid for case, profile in selected for rid in [profile['id'], *_source_ids(service, connection, case['id'])]}),
                'actor': who, 'notice': 'Related investigation only. Each case retains its own permissions, evidence and conversation.'})
            return next(item for item in _incidents(service, connection, profiles) if item['id'] == row['id'])

    @router.post('/incidents/{incident_id}/status')
    def incident_status(incident_id: str, data: IncidentStatusInput, who=Depends(actor)):
        service = get_service()
        service.role(who, {'case_manager'})
        with service.db.tx() as connection:
            profiles = _profiles(service, connection)
            incident = next((item for item in _incidents(service, connection, profiles) if item['id'] == incident_id), None)
            if incident is None:
                raise ValueError('Incident not found')
            if incident['status'] != 'confirmed':
                raise Conflict('This incident link is already resolved or dismissed')
            service.db.add(connection, 'portfolio_incident_status', {
                **data.model_dump(), 'incident_id': incident_id, 'actor': who,
                'profile_ids': {cid: profiles[cid]['id'] for cid in incident['case_ids']},
                'case_revisions': {cid: service.db.case(connection, cid)['revision'] for cid in incident['case_ids']},
                'source_record_ids': sorted({rid for cid in incident['case_ids'] for rid in [profiles[cid]['id'], *_source_ids(service, connection, cid)]}),
                'notice': 'This changes the investigation link only; it does not close or resolve individual repairs.'})
            return next(item for item in _incidents(service, connection, profiles) if item['id'] == incident_id)

    @router.post('/contractors')
    def contractor(data: ContractorInput, who=Depends(actor)):
        service = get_service()
        service.role(who, {'case_manager'})
        with service.db.tx() as connection:
            if any(item['name'].casefold() == data.name.casefold() for item in _rows(service, connection, 'contractor')):
                raise Conflict('A contractor planning resource with this name already exists; use that resource to avoid duplicate scheduling')
            row, _ = service.db.add(connection, 'portfolio_contractor', {
                **data.model_dump(mode='json'), 'actor': who, 'availability_source': 'staff supplied',
                'notice': 'Local planning resource; identity, skills and availability are not externally verified.'})
            return payload(row)

    @router.post('/plans')
    def create_plan(data: PlanInput, who=Depends(actor)):
        service = get_service()
        service.role(who, {'case_manager'})
        with service.db.tx() as connection:
            profiles = _profiles(service, connection)
            selected = [_require_profile(service, connection, cid, profiles) for cid in data.case_ids]
            resource = next((item for item in _rows(service, connection, 'contractor') if item['id'] == data.contractor_id), None)
            if resource is None:
                raise ValueError('Contractor planning resource not found')
            if data.start < dt(resource['available_from']) or data.end > dt(resource['available_until']):
                raise ValueError('The plan must be inside the staff-supplied contractor availability')
            trades = {trade.casefold() for trade in resource['trades']}
            for _, profile in selected:
                if profile['trade'].casefold() not in trades:
                    raise ValueError('The contractor must list the required trade for every selected case')
                if profile.get('window_start') and (data.start < dt(profile['window_start']) or data.end > dt(profile['window_end'])):
                    raise ValueError('The plan must be inside every supplied case appointment window')
            cancelled = {item['plan_id'] for item in _rows(service, connection, 'plan_cancelled')}
            for existing in _rows(service, connection, 'plan'):
                if existing['id'] in cancelled:
                    continue
                if data.start < dt(existing['end']) and data.end > dt(existing['start']):
                    if existing['contractor_id'] == data.contractor_id or set(data.case_ids) & set(existing['case_ids']):
                        raise Conflict('This time overlaps an existing tentative plan for the contractor or a selected case')
            policy = service.active(connection)
            row, _ = service.db.add(connection, 'portfolio_plan', {
                **data.model_dump(mode='json'), 'actor': who, 'policy_version': policy['version'],
                'case_revisions': {case['id']: case['revision'] for case, _ in selected},
                'profile_ids': {case['id']: profile['id'] for case, profile in selected},
                'source_record_ids': sorted({resource['id'], *(rid for case, profile in selected for rid in [profile['id'], *_source_ids(service, connection, case['id'])])}),
                'notice': NOTICE})
            return next(item for item in _plans(service, connection, profiles, policy) if item['id'] == row['id'])

    @router.post('/plans/{plan_id}/cancel')
    def cancel_plan(plan_id: str, data: ReasonInput, who=Depends(actor)):
        service = get_service()
        service.role(who, {'case_manager'})
        with service.db.tx() as connection:
            if not any(item['id'] == plan_id for item in _rows(service, connection, 'plan')):
                raise ValueError('Plan not found')
            if any(item['plan_id'] == plan_id for item in _rows(service, connection, 'plan_cancelled')):
                raise Conflict('This tentative plan is already cancelled')
            service.db.add(connection, 'portfolio_plan_cancelled', {
                'plan_id': plan_id, 'reason': data.reason, 'actor': who, 'notice': 'Local planning cancellation only; no message was sent.'})
            return next(item for item in _plans(service, connection, _profiles(service, connection), service.active(connection)) if item['id'] == plan_id)

    return router
