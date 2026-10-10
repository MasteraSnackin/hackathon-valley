"""Shared test switches.

Tests marked ``claude`` call the real Anthropic API (key from the environment
or the git-ignored .env.local) and are skipped when no credential exists.
Every other test is offline: it uses manual staff triage or runs with the
credential removed, so no model is called.
"""
import pytest
from app.localenv import load_local_env

load_local_env()
from app import ai  # noqa: E402


def pytest_configure(config):
    config.addinivalue_line("markers", "claude: calls the real Claude API")


def pytest_collection_modifyitems(config, items):
    if ai.configured():
        return
    skip = pytest.mark.skip(reason="No Anthropic credential configured (ANTHROPIC_API_KEY or .env.local)")
    for item in items:
        if "claude" in item.keywords:
            item.add_marker(skip)


@pytest.fixture
def no_claude(monkeypatch):
    """Simulate a missing credential: every model call fails before the network."""
    monkeypatch.delenv("ANTHROPIC_API_KEY", raising=False)
    monkeypatch.delenv("ANTHROPIC_AUTH_TOKEN", raising=False)
