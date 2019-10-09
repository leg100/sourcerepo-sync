import base64
import json
import pytest
import tempfile
from unittest import mock

import main


def event(func):
    def wrapper():
        data = func()
        encoded = base64.b64encode(json.dumps(data).encode())
        return {'data': encoded}

    return wrapper


@pytest.fixture
@event
def github_data():
    return json.load(open("tests/event_github.json", "r"))


@pytest.fixture
def env_vars(monkeypatch):
    monkeypatch.setenv('GCP_PROJECT', 'my-repo-project')


@pytest.fixture
def metadata(mocker):
    mocker.patch('sourcerepo_sync.metadata.service_account',
            return_value='webhook@gserviceiamaccount.com')
    mocker.patch('sourcerepo_sync.metadata.access_token',
            return_value='LKFLJKJSAKFNKJNFSKJNFKNA')


@pytest.fixture
def tmp_dir(mocker):
    tmp = tempfile.TemporaryDirectory()
    return tmp.name


def test_sync(github_data, env_vars, metadata, mocker):
    mocker.patch('main.git.clone', create=True)
    mocker.patch('main.git.push', create=True)

    tmp_dir = mock.Mock()
    tmp_dir.__enter__ = mock.Mock(return_value='/tmp/foo')
    tmp_dir.__exit__ = mock.Mock(return_value=False)
    mocker.patch('tempfile.TemporaryDirectory', return_value=tmp_dir)

    main.sync(github_data, None)

    assert main.git.clone.assert_called()
    assert main.git.clone.assert_called_with('--mirror',
            'https://github.com/leg100/test-repo.git', _cwd='/tmp/foo')

    sourcerepo = \
        ('https://webhook%40gserviceiamaccount.com:LKFLJKJSAKFNKJNFSKJNFKNA@'
        'source.developers.google.com'
        '/p/my-repo-project'
        '/r/github_leg100_test-repo')

    assert main.git.push.assert_called_with('--mirror', sourcerepo, _cwd=tmp_dir)
