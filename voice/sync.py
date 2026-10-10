"""Push the Property Desk phone agent to ElevenLabs for the current public URL.

Hackathon helper around the authenticated ``elevenlabs`` CLI. Run it whenever the
tunnel URL changes:

    .venv/bin/python voice/sync.py                   # URL from the local ngrok agent
    .venv/bin/python voice/sync.py https://example.ngrok-free.app
    .venv/bin/python voice/sync.py --phone-number-id phnum_...   # also route a number

It creates or updates, recording non-secret IDs in voice/elevenlabs/ids.json:
- a workspace secret holding VOICE_TOOL_SECRET from .env.local (sent as X-Voice-Tool-Secret);
- the ``report_maintenance_issue`` webhook tool -> {url}/api/voice/report;
- a post-call webhook -> {url}/api/voice/post-call. A webhook URL cannot be changed,
  so a new URL replaces it and its new signing secret is written to .env.local
  (restart the server afterwards);
- the agent, with its prompt from voice/agent_prompt.md.

Secrets are passed on stdin and never printed.
"""
from __future__ import annotations

import argparse
import json
import os
import re
import secrets
import subprocess
import sys
import urllib.request
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
VOICE = ROOT / 'voice'
CONFIG = VOICE / 'elevenlabs'
IDS = CONFIG / 'ids.json'
ENV = ROOT / '.env.local'
SECRET_NAME = 'property_desk_voice_tool_secret'


def cli(*args, body=None, required=True):
    """Run the ElevenLabs CLI and return its JSON output; bodies go on stdin."""
    command = ['elevenlabs', *args, '--format', 'json']
    if body is not None:
        command += ['--json', '-']
    # ELEVENLABS_API_KEY from .env.local, when present, overrides the CLI login
    # (the OAuth login lacks some scopes, e.g. webhooks_write).
    env = {**os.environ, **{k: v for k, v in read_env().items() if k == 'ELEVENLABS_API_KEY'}}
    done = subprocess.run(command, input=json.dumps(body) if body is not None else None,
                          capture_output=True, text=True, env=env)
    if done.returncode and not required:
        return None
    if done.returncode:
        sys.exit(f'elevenlabs {" ".join(args)} failed:\n{done.stderr or done.stdout}')
    return json.loads(done.stdout) if done.stdout.strip() else {}


def read_env():
    values = {}
    if ENV.is_file():
        for line in ENV.read_text().splitlines():
            if '=' in line and not line.lstrip().startswith('#'):
                key, value = line.split('=', 1)
                values[key.strip()] = value.strip()
    return values


def set_env(key, value):
    lines = ENV.read_text().splitlines() if ENV.is_file() else []
    lines = [line for line in lines if not line.startswith(key + '=')] + [f'{key}={value}']
    ENV.write_text('\n'.join(lines) + '\n')
    ENV.chmod(0o600)


def public_url(arg):
    if arg:
        return arg.rstrip('/')
    try:
        with urllib.request.urlopen('http://127.0.0.1:4040/api/tunnels', timeout=3) as response:
            tunnels = json.load(response)['tunnels']
    except OSError:
        sys.exit('No URL given and no local ngrok agent found. Start: ngrok http 8027')
    https = [t['public_url'] for t in tunnels if t['public_url'].startswith('https://')]
    if not https:
        sys.exit('ngrok is running without an https tunnel')
    return https[0].rstrip('/')


def main():
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument('url', nargs='?', help='Public https base URL that reaches this app')
    parser.add_argument('--phone-number-id', help='Route this imported phone number to the agent')
    args = parser.parse_args()
    url = public_url(args.url)
    if not re.fullmatch(r'https://[^/\s]+', url):
        sys.exit('Give the bare https base URL, e.g. https://example.ngrok-free.app')
    ids = json.loads(IDS.read_text()) if IDS.is_file() else {}
    env = read_env()

    def save():
        IDS.write_text(json.dumps(ids, indent=2, sort_keys=True) + '\n')

    # 1. Tool credential: a local secret mirrored into the ElevenLabs secret store.
    if not env.get('VOICE_TOOL_SECRET'):
        set_env('VOICE_TOOL_SECRET', secrets.token_urlsafe(32))
        ids.pop('tool_secret_id', None)
        env = read_env()
    if not ids.get('tool_secret_id'):
        ids['tool_secret_id'] = cli('agents', 'secrets', 'create', body={
            'type': 'new', 'name': SECRET_NAME, 'value': env['VOICE_TOOL_SECRET']})['secret_id']
        save()

    # 2. The webhook tool the agent calls after the caller confirms.
    tool = json.loads((CONFIG / 'tool_configs' / 'report_maintenance_issue.json').read_text())
    tool['api_schema']['url'] = url + '/api/voice/report'
    tool['api_schema']['request_headers']['X-Voice-Tool-Secret'] = {'secret_id': ids['tool_secret_id']}
    if ids.get('tool_id'):
        cli('agents', 'tools', 'update', '--tool-id', ids['tool_id'], body={'tool_config': tool})
    else:
        ids['tool_id'] = cli('agents', 'tools', 'create', body={'tool_config': tool})['id']
        save()

    # 3. Post-call webhook (signed). A changed URL needs a new webhook and secret.
    webhook_url = url + '/api/voice/post-call'
    if ids.get('webhook_id') and (ids.get('webhook_url') != webhook_url or not env.get('ELEVENLABS_WEBHOOK_SECRET')):
        cli('webhooks', 'delete', '--webhook-id', ids.pop('webhook_id'))
        save()
    restart = False
    if not ids.get('webhook_id'):
        # Optional: calls still create cases without it; only transcripts are missing.
        created = cli('webhooks', 'create', body={'settings': {
            'auth_type': 'hmac', 'name': 'Property Desk phone intake', 'webhook_url': webhook_url}},
            required=False)
        if created:
            ids.update(webhook_id=created['webhook_id'], webhook_url=webhook_url)
            set_env('ELEVENLABS_WEBHOOK_SECRET', created['webhook_secret'])
            save()
            restart = True
        else:
            print('Warning: could not create the post-call webhook (the key needs webhooks_write). '
                  'Calls still create cases; transcripts will not be attached.')

    # 4. The agent itself.
    agent = json.loads((CONFIG / 'agent_configs' / 'property-desk-phone.json').read_text())
    prompt = agent['conversation_config']['agent']['prompt']
    prompt['prompt'] = (VOICE / 'agent_prompt.md').read_text()
    prompt['tool_ids'] = [ids['tool_id']]
    agent['platform_settings']['workspace_overrides']['webhooks']['post_call_webhook_id'] = ids.get('webhook_id')
    if ids.get('agent_id'):
        cli('agents', 'update', '--agent-id', ids['agent_id'], body=agent)
    else:
        ids['agent_id'] = cli('agents', 'create', body=agent)['agent_id']
        save()

    if args.phone_number_id:
        cli('agents', 'phone-numbers', 'update', '--phone-number-id', args.phone_number_id,
            body={'agent_id': ids['agent_id']})
        ids['phone_number_id'] = args.phone_number_id

    save()
    print(f'Agent {ids["agent_id"]} now reports to {url}')
    if restart:
        print('A new webhook signing secret was saved to .env.local: restart the app server.')


if __name__ == '__main__':
    main()
