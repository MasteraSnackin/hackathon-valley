"""Load git-ignored local development secrets (e.g. ANTHROPIC_API_KEY).

Call only from process entry points (server, replay, tests). The workflow
sandbox re-imports application modules and forbids file access, so importing
this module must stay side-effect free. Existing environment values win and
nothing is logged.
"""
import os
from pathlib import Path


def load_local_env(path=None):
    # PROPERTY_LOCAL_ENV=off keeps a process credential-free (offline checks).
    if os.getenv('PROPERTY_LOCAL_ENV') == 'off':
        return
    path = Path(path or Path(__file__).resolve().parent.parent / '.env.local')
    if not path.is_file():
        return
    for line in path.read_text().splitlines():
        line = line.strip()
        if not line or line.startswith('#') or '=' not in line:
            continue
        key, value = line.split('=', 1)
        os.environ.setdefault(key.strip(), value.strip().strip('"').strip("'"))
