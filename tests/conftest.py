"""Shared test switches.

Tests marked ``claude`` call the real Anthropic API and tests marked ``jev``
call the real TypeSafe (Jev) API (keys from the environment or the git-ignored
.env.local); each is skipped when its credential is missing. Every other test
is offline: it uses manual staff triage, fakes, or runs with the credential
removed, so no model is called. Tests not marked ``jev`` run without the Jev
credential, so ``claude`` tests keep exercising the Claude-only path.
"""
import pytest
from app.localenv import load_local_env

load_local_env()
from app import ai, jev  # noqa: E402


def pytest_configure(config):
    config.addinivalue_line("markers", "claude: calls the real Claude API")
    config.addinivalue_line("markers", "jev: calls the real TypeSafe Jev API")


def pytest_collection_modifyitems(config, items):
    missing = {"claude": not ai.configured(), "jev": not jev.configured()}
    for item in items:
        for marker, absent in missing.items():
            if absent and marker in item.keywords:
                item.add_marker(pytest.mark.skip(reason=f"No {marker} credential configured (environment or .env.local)"))


@pytest.fixture(autouse=True)
def _jev_only_when_marked(request, monkeypatch):
    if "jev" not in request.keywords:
        # Empty rather than absent: subprocesses that load .env.local keep it empty.
        monkeypatch.setenv("TYPESAFE_API_KEY", "")


@pytest.fixture
def no_claude(monkeypatch):
    """Simulate a missing credential: every model call fails before the network."""
    monkeypatch.delenv("ANTHROPIC_API_KEY", raising=False)
    monkeypatch.delenv("ANTHROPIC_AUTH_TOKEN", raising=False)
