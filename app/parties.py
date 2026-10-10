"""Who is calling, about which property, and what they may be told.

A fictional, preconfigured directory stands in for a real contact system. Every
number is in Ofcom's reserved drama range (07700 900xxx); no real person,
address or route is used. A caller-ID match is a demonstration identity, not a
verified one: caller ID can be spoofed, so production needs a real check.

The directory never creates authority. It tells the workflow who sent a
message (so the policy can weigh whose claim counts for which fact) and who a
question should go to. Every outbound message remains simulated.
"""
from __future__ import annotations
import re

PARTY_KINDS = ('tenant', 'landlord', 'agency', 'contractor', 'other')
PARTY_LABELS = {'tenant': 'Tenant', 'landlord': 'Landlord', 'agency': 'Letting agency', 'contractor': 'Contractor', 'other': 'Unknown caller'}

PROPERTIES = {
    'DEMO-PARK-7': {'address': 'Flat 7, Park View, Demo Town', 'aliases': ['flat 7', 'park view']},
    'DEMO-LANE-2': {'address': '2 Sample Lane, Demo Town', 'aliases': ['2 sample lane', 'sample lane']},
}

PARTIES = [
    {'id': 'tenant-alex', 'kind': 'tenant', 'name': 'Alex Taylor', 'phone': '+447700900101', 'properties': ['DEMO-PARK-7']},
    {'id': 'tenant-sam', 'kind': 'tenant', 'name': 'Sam Rivera', 'phone': '+447700900102', 'properties': ['DEMO-LANE-2']},
    {'id': 'landlord-morgan', 'kind': 'landlord', 'name': 'Morgan Lee', 'phone': '+447700900201', 'properties': ['DEMO-PARK-7', 'DEMO-LANE-2']},
    {'id': 'agency-harbour', 'kind': 'agency', 'name': 'Harbour Lettings', 'phone': '+447700900301', 'properties': ['DEMO-PARK-7', 'DEMO-LANE-2'], 'acts_for': 'landlord-morgan'},
    {'id': 'contractor-demo', 'kind': 'contractor', 'name': 'Demo contractor', 'phone': '+447700900401', 'properties': ['DEMO-PARK-7', 'DEMO-LANE-2']},
]

# Whose statement counts for which policy fact. A claim from any other known
# party is stored as hearsay: shown to staff, but it cannot satisfy a check.
# A refusal (value false) still counts from anyone, so the policy fails closed.
# Facts not listed accept any party.
FACT_SOURCES = {
    'access': {'tenant'},
    'authority': {'landlord', 'agency'},
    'total': {'contractor'},
    'completion': {'tenant', 'contractor'},
}

# On directory properties, these open questions go to someone other than the
# tenant. Each topic is what the drafted message asks about.
PARTY_QUESTIONS = {'authority': ('landlord', 'approval'), 'total': ('contractor', 'quote')}
PARTY_TOPICS = ['approval', 'quote']
# Who may answer a question addressed to each party.
ANSWERED_BY = {'tenant': {'tenant'}, 'landlord': {'landlord', 'agency'}, 'contractor': {'contractor'}}


def digits(number):
    """Normalise a UK number: +44 7700 900101, 07700900101 and 447700900101 match."""
    d = re.sub(r'\D', '', number or '')
    if d.startswith('0'):
        d = '44' + d[1:]
    return d


def by_phone(number):
    want = digits(number)
    return next((p for p in PARTIES if want and digits(p['phone']) == want), None)


def by_id(party_id):
    return next((p for p in PARTIES if p['id'] == party_id), None)


def on_property(kind, property_ref):
    return next((p for p in PARTIES if p['kind'] == kind and property_ref in p['properties']), None)


def resolve_property(party, transcript):
    """The caller's only property, or the one their words name. None when unclear."""
    if not party:
        return None
    if len(party['properties']) == 1:
        return party['properties'][0]
    text = ' '.join((transcript or '').casefold().split())
    named = [ref for ref in party['properties'] if any(alias in text for alias in PROPERTIES[ref]['aliases'])]
    return named[0] if len(named) == 1 else None


def stamp_for(party, verified=True):
    """The party marker stored on evidence. Never includes a phone number."""
    if not party:
        return {'kind': 'other', 'id': None, 'name': None, 'verified': False, 'match': 'unknown_number'}
    return {'kind': party['kind'], 'id': party['id'], 'name': party['name'], 'verified': verified, 'match': 'caller_id_fictional_directory'}


def counts_for(key, value, party):
    """False when a known party's positive claim is outside its say (hearsay)."""
    if not party or value is False:
        return True
    allowed = FACT_SOURCES.get(key)
    return allowed is None or party['kind'] in allowed


def directory_view():
    """Names and kinds for the demo call panel. Numbers are fictional and reserved."""
    return {'properties': [{'ref': k, 'address': v['address']} for k, v in PROPERTIES.items()],
            'parties': [{k: p[k] for k in ('id', 'kind', 'name', 'phone', 'properties')} for p in PARTIES],
            'notice': 'Fictional directory. Numbers are in the reserved 07700 900xxx drama range.'}
