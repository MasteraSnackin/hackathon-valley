"""Assemble a read-only overview from reviewed BUILD-only source notes."""
from pathlib import Path
import csv
import hashlib
import json
import re

HERE = Path(__file__).resolve().parent
ROOT = HERE.parent.parent
metadata = json.loads((HERE / 'metadata.json').read_text())
manifest = json.loads((ROOT / 'handoff/BUILD_MANIFEST.json').read_text())
assert {row['case_id'] for row in metadata['properties']} == set(manifest['allowed_case_ids'])
assert metadata['source_revision'] == manifest['source_commit']
source_hashes_checked = 0
for source in manifest['files']:
    if source['path'].endswith('.md'):
        assert source['case_id'] in manifest['allowed_case_ids']
        assert hashlib.sha256((ROOT / 'data/build' / source['path']).read_bytes()).hexdigest() == source['sha256'], source['path']
        source_hashes_checked += 1
guidance = json.loads((HERE / 'review-guidance.json').read_text())
assert len(guidance) == 25 and {row['case_id'] for row in guidance} == set(manifest['allowed_case_ids'])
guidance_by_id = {row['case_id']: row for row in guidance}
valid_states = {'reported_complete', 'unconfirmed', 'planned', 'reported', 'disputed'}
valid_tags = {'scope', 'documents', 'chronology', 'identity', 'permission', 'communication', 'other'}
map_config = json.loads((HERE / 'map-locations.json').read_text())
assert map_config['mode'] == 'demo'
assert set(map_config['locations']) == {row['case_id'] for row in metadata['properties']}
metadata['map_display'] = {k: v for k, v in map_config.items() if k != 'locations'}
parts = [json.loads((HERE / name).read_text()) for name in ('part-a.json', 'part-b.json')]
records = [row for part in parts for row in part]
ids = [row['case_id'] for row in records]
allowed = {row['case_id'] for row in metadata['properties']}
assert len(ids) == len(set(ids)) == 25 and set(ids) == allowed
by_id = {row['case_id']: row for row in records}
quote_checks = 0
guidance_quote_checks = 0
for row in metadata['properties']:
    reviewed = by_id[row['case_id']]
    row.update(reviewed)
    annotation = guidance_by_id[row['case_id']]
    assert [x['issue_label'] for x in annotation['issue_states']] == [x['label'] for x in row['issues']], row['case_id']
    assert [x['question_label'] for x in annotation['question_groups']] == [x['label'] for x in row['caveats']], row['case_id']
    for state in annotation['issue_states']:
        assert state['state'] in valid_states and state['label'] and state['note'] and state['evidence']
    for group in annotation['question_groups']:
        assert group['tags'] and set(group['tags']) <= valid_tags
    assert annotation['next_check']['question'] and annotation['next_check']['rationale'] and annotation['next_check']['evidence']
    row['review_guidance'] = annotation
    row['display_location'] = map_config['locations'][row['case_id']]
    location = row['display_location']
    assert location['kind'] == 'demo' and location['provenance']
    assert -90 <= location['latitude'] <= 90 and -180 <= location['longitude'] <= 180
    sources = {name: (ROOT / 'data/build' / row['case_id'] / name).read_text()
               for name in ('index.md', 'history.md')}
    event_count = len(re.findall(r'<a id="event-\d+">', sources['history.md']))
    assert event_count == row['history_events'], row['case_id']
    assert row['issues']
    for issue in row['issues']:
        assert issue['kind'] in {'reported_issue', 'recorded_work', 'follow_up'}
    groups = row['issues'] + row['caveats'] + [{'evidence': row.get('outcome_evidence', [])}]
    annotation_groups = annotation['issue_states'] + [annotation['next_check']]
    guidance_quote_checks += sum(len(group['evidence']) for group in annotation_groups)
    groups += annotation_groups
    for group in groups:
        for ev in group['evidence']:
            assert ev['file'] in sources
            text = sources[ev['file']]
            if ev.get('event'):
                anchor = '<a id="' + ev['event'] + '"></a>'
                assert anchor in text, (row['case_id'], ev)
                text = text.split(anchor, 1)[1].split('<a id="event-', 1)[0]
            assert 0 < len(ev['quote']) <= 180 and ev['quote'] in text, (row['case_id'], ev)
            quote_checks += 1
    assert not re.search(r'\b(?:07700|[\w.+-]+@[\w.-]+\.[a-z]{2,})', json.dumps(reviewed), re.I), row['case_id']

inventory = json.dumps(metadata, indent=2, ensure_ascii=False)
(HERE / 'property-inventory.json').write_text(inventory + '\n')
page = (HERE / 'template.html').read_text().replace('__INVENTORY_JSON__', inventory.replace('</', '<\\/'))
(HERE / 'index.html').write_text(page)
with (HERE / 'property-issues.csv').open('w', newline='') as f:
    writer = csv.DictWriter(f, fieldnames=['case_id', 'property', 'case_type', 'issue', 'location', 'kind', 'recorded_case_status', 'evidence_url'])
    writer.writeheader()
    for row in metadata['properties']:
        for issue in row['issues']:
            evidence = issue['evidence'][0]
            writer.writerow({'case_id': row['case_id'], 'property': row['property'], 'case_type': row['family'],
                'issue': issue['label'], 'location': issue['location'] or 'Not stated', 'kind': issue['kind'],
                'recorded_case_status': row['recorded_status'],
                'evidence_url': row['source_url'] + '/' + evidence['file'] + ('#' + evidence['event'] if evidence.get('event') else '')})
report = {'scope': 'Authorised BUILD files only; no runtime app state, PDFs or reserved evaluation cases accessed.',
          'dataset_revision': metadata['source_revision'], 'properties': len(records),
          'unique_property_labels': len({r['property'] for r in metadata['properties']}),
          'issues': sum(len(r['issues']) for r in records), 'caveats': sum(len(r['caveats']) for r in records),
          'history_events': sum(r['history_events'] for r in metadata['properties']),
          'source_markdown_hashes_verified': source_hashes_checked, 'exact_quotes_verified': quote_checks,
          'issue_evidence_states': sum(len(row['issue_states']) for row in guidance),
          'suggested_next_checks': len(guidance), 'guidance_quotes_verified': guidance_quote_checks,
          'outcomes_with_direct_evidence': sum(bool(r.get('outcome_evidence')) for r in records),
          'demo_locations': len(map_config['locations']), 'verified_locations': 0,
          'html_sha256': hashlib.sha256((HERE / 'index.html').read_bytes()).hexdigest()}
(HERE / 'validation.json').write_text(json.dumps(report, indent=2) + '\n')
print(json.dumps(report, indent=2))
