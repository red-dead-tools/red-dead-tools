import flask
import pytest


# Create a fake "app" for generating test request contexts.
@pytest.fixture(scope="module")
def app():
    return flask.Flask(__name__)


@pytest.fixture(autouse=True)
def fix_path(monkeypatch):
    monkeypatch.syspath_prepend('gcloud-functions')


@pytest.mark.parametrize('sheet_name', ['R', 'A', 'T', ''])
def test_red_dead_tools(app, sheet_name):
    import main

    with app.test_request_context(f'?sheet_name={sheet_name}'):
        response = main.red_dead_tools(flask.request)
        data, status, headers = response
        assert status == 200
        assert {'main.date', 'length', 'version'} < data.keys()
