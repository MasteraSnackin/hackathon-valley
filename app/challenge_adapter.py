"""Mechanical adapter: organiser HackatonChallenges case folders -> Reality Test inputs.

Reads one track folder (e.g. `Property Management/`) of the organiser release
(`index.md`, `history.md`, `attachments/`) and writes a `manifest.json` plus one
`<case>.json` per case in the runner's versioned contract. It makes no decisions
and calls no model:

- `report` is history event 001 verbatim (channel, sender, recipient, body), as
  available at that event's timestamp.
- every later history event becomes one evidence source, in order, at its own
  timestamp, with its header lines kept so sender roles stay visible.
- PDF attachments are text-extracted with pypdf. The release gives no upload
  time, so each is made available at the case's decision cutoff (`Updated`),
  after all history events. Other binary attachments are listed, not read.
- `as_of` is the index `Updated` time; the index summary and title are not
  decision input beyond the title/property reference fields.

Originals are not modified; each input records the source file SHA-256 hashes
in the adapter report written next to the manifest.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import re
from datetime import datetime, timezone
from pathlib import Path

EVENT = re.compile(r'^## (\d{4}-\d\d-\d\d \d\d:\d\d:\d\d) UTC — event (\d+)\s*$', re.M)
FIELD = re.compile(r'^- \*\*(.+?):\*\* (.*)$')


def stamp(text):
    return datetime.strptime(text.strip().removesuffix(' UTC'), '%Y-%m-%d %H:%M:%S').replace(tzinfo=timezone.utc)


def index_fields(text):
    fields = {}
    for line in text.splitlines():
        match = FIELD.match(line.strip())
        if match:
            fields[match.group(1)] = match.group(2).strip()
    title = text.splitlines()[0].lstrip('# ').strip()
    return title, fields


def events(text):
    marks = list(EVENT.finditer(text))
    for i, mark in enumerate(marks):
        end = marks[i + 1].start() if i + 1 < len(marks) else len(text)
        body = text[mark.end():end]
        body = re.sub(r'<a id="event-\d+"></a>\s*$', '', body.strip()).strip()
        header, message = [], []
        for line in body.splitlines():
            match = FIELD.match(line.strip())
            if match and not message:
                header.append((match.group(1), match.group(2).strip()))
            elif line.strip() or message:
                message.append(line)
        yield {'number': mark.group(2), 'at': stamp(mark.group(1)), 'header': dict(header),
               'text': '\n'.join(message).strip()}


def event_text(event):
    h = event['header']
    lines = [f"Event {event['number']} — {h.get('Channel', 'unknown channel')}",
             f"From: {h.get('From', 'unknown')}", f"To: {h.get('To', 'unknown')}", '', event['text']]
    return '\n'.join(lines)


def pdf_text(path):
    from pypdf import PdfReader
    pages = [page.extract_text() or '' for page in PdfReader(str(path)).pages]
    return '\n\n'.join(p.strip() for p in pages).strip()


def convert_case(folder: Path):
    sha = {}
    def read(path):
        data = path.read_bytes()
        sha[str(path.relative_to(folder))] = hashlib.sha256(data).hexdigest()
        return data
    title, fields = index_fields(read(folder / 'index.md').decode())
    history = list(events(read(folder / 'history.md').decode()))
    if not history:
        raise ValueError(f'{folder}: no history events found')
    cutoff = stamp(fields['Updated'])
    first, rest = history[0], history[1:]
    evidence = [{'source_label': f"Event {e['number']} — {e['header'].get('Channel', 'message')} from {e['header'].get('From', 'unknown')}"[:200],
                 'text': event_text(e), 'available_at': e['at'].isoformat()} for e in rest]
    unread = []
    attachments = folder / 'attachments'
    for path in sorted(attachments.iterdir()) if attachments.is_dir() else []:
        read(path)
        if path.suffix.lower() == '.pdf':
            text = pdf_text(path)
            evidence.append({'source_label': f'Attachment {path.name} (PDF text extraction)',
                             'text': f'Attachment: {path.name}\nExtracted text (pypdf; layout not preserved):\n\n{text}' if text
                             else f'Attachment: {path.name}\nNo extractable text.',
                             'available_at': cutoff.isoformat()})
        else:
            unread.append(path.name)
    if unread:
        evidence.append({'source_label': 'Attachments not read by the adapter',
                         'text': 'The case file also contains these attachments, which were not converted to text and were not read: ' + ', '.join(unread),
                         'available_at': cutoff.isoformat()})
    case = {'schema_version': 1, 'title': title[:160], 'property_ref': fields.get('Property', 'unknown property')[:200],
            'as_of': cutoff.isoformat(), 'report_available_at': first['at'].isoformat(),
            'report': event_text(first), 'evidence': evidence}
    return case, {'events': len(history), 'attachments_pdf_text': sum(1 for e in evidence if e['source_label'].startswith('Attachment ')),
                  'attachments_unread': unread, 'source_sha256': sha}


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument('track', type=Path, help='Track folder, e.g. "HackatonChallenges/Property Management"')
    parser.add_argument('--out', type=Path, required=True, help='New directory for manifest.json and case inputs')
    parser.add_argument('--cases', nargs='*', help='Only these case numbers (default: all)')
    args = parser.parse_args(argv)
    args.out.mkdir(parents=True, exist_ok=False)
    folders = sorted(p for p in args.track.iterdir() if p.is_dir() and re.fullmatch(r'\d{3}', p.name))
    if args.cases:
        folders = [p for p in folders if p.name in set(args.cases)]
    refs, report = [], {}
    for folder in folders:
        case, meta = convert_case(folder)
        (args.out / f'{folder.name}.json').write_text(json.dumps(case, indent=2, ensure_ascii=False) + '\n')
        refs.append({'id': folder.name, 'input_file': f'{folder.name}.json'})
        report[folder.name] = meta
    manifest = {'schema_version': 1, 'dataset_kind': 'organiser_release', 'cases': refs}
    (args.out / 'manifest.json').write_text(json.dumps(manifest, indent=2) + '\n')
    (args.out / 'adapter-report.json').write_text(json.dumps({'track': args.track.name, 'cases': report}, indent=2) + '\n')
    print(json.dumps({'cases': len(refs), 'out': str(args.out)}))


if __name__ == '__main__':
    main()
