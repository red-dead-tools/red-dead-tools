import pytest

from red_dead import base_dir


# private sub-module for portable local dev
AUTH_PATH = base_dir / 'red-dead-tools-private/.data/red-dead-tools-b475e08cb189.json'


@pytest.fixture(autouse=True)
def auth(monkeypatch):
    monkeypatch.setenv('GOOGLE_APPLICATION_CREDENTIALS', str(AUTH_PATH))
