# tests/unit/test_github_pull_requests_api.py
from unittest.mock import MagicMock, patch

import pytest

from services.github_pull_requests_api import GitHubPullRequestsAPI
from services.request_manager import RequestManager


@pytest.fixture
def mock_request_manager():
    with patch.object(RequestManager, '_instance', None), \
         patch('services.github_pull_requests_api.RequestManager') as MockRequestManager:

        mock_instance = MagicMock()
        MockRequestManager.return_value = mock_instance

        mock_instance.get.return_value = MagicMock(status_code=200, json=lambda: {"id": 1, "number": 1})
        mock_instance.patch.return_value = MagicMock(status_code=200, json=lambda: {"state": "closed"})
        mock_instance.post.return_value = MagicMock(status_code=201, json=lambda: [{"name": "bug"}])
        mock_instance.put.return_value = MagicMock(status_code=200, json=lambda: [])
        mock_instance.delete.return_value = MagicMock(status_code=204)

        yield mock_instance


@pytest.fixture
def pr_api(mock_request_manager):
    with patch.dict('os.environ', {
        'BASE_URL': 'https://api.github.com',
        'GITHUB_USERNAME': 'testowner',
        'GITHUB_REPO': 'testrepo'
    }):
        api = GitHubPullRequestsAPI()
        api.client = mock_request_manager
        return api


def test_get_pull_request(pr_api, mock_request_manager):
    pr_number = 5
    response = pr_api.get_pull_request(pr_number)
    mock_request_manager.get.assert_called_once_with(
        'https://api.github.com/repos/testowner/testrepo/pulls/5'
    )
    assert response.status_code == 200


def test_list_pull_requests(pr_api, mock_request_manager):
    response = pr_api.list_pull_requests(state="closed")
    mock_request_manager.get.assert_called_once_with(
        'https://api.github.com/repos/testowner/testrepo/pulls',
        params={"state": "closed"}
    )
    assert response.status_code == 200


def test_update_pull_request(pr_api, mock_request_manager):
    payload = {"title": "new title", "body": "updated body"}
    response = pr_api.update_pull_request(5, payload)
    mock_request_manager.patch.assert_called_once_with(
        'https://api.github.com/repos/testowner/testrepo/pulls/5',
        json=payload
    )
    assert response.status_code == 200


def test_close_pull_request(pr_api, mock_request_manager):
    response = pr_api.close_pull_request(5)
    mock_request_manager.patch.assert_called_once_with(
        'https://api.github.com/repos/testowner/testrepo/pulls/5',
        json={"state": "closed"}
    )
    assert response.status_code == 200


def test_reopen_pull_request(pr_api, mock_request_manager):
    response = pr_api.reopen_pull_request(5)
    mock_request_manager.patch.assert_called_once_with(
        'https://api.github.com/repos/testowner/testrepo/pulls/5',
        json={"state": "open"}
    )
    assert response.status_code == 200


def test_add_labels(pr_api, mock_request_manager):
    labels = ["bug", "enhancement"]
    response = pr_api.add_labels(5, labels)
    mock_request_manager.post.assert_called_once_with(
        'https://api.github.com/repos/testowner/testrepo/issues/5/labels',
        json={"labels": labels}
    )
    assert response.status_code == 201


def test_get_labels(pr_api, mock_request_manager):
    response = pr_api.get_labels(5)
    mock_request_manager.get.assert_called_once_with(
        'https://api.github.com/repos/testowner/testrepo/issues/5/labels'
    )
    assert response.status_code == 200


def test_set_labels(pr_api, mock_request_manager):
    labels = ["bug"]
    response = pr_api.set_labels(5, labels)
    mock_request_manager.put.assert_called_once_with(
        'https://api.github.com/repos/testowner/testrepo/issues/5/labels',
        json={"labels": labels}
    )
    assert response.status_code == 200


def test_create_label(pr_api, mock_request_manager):
    response = pr_api.create_label("newlabel", color="FF0000", description="test")
    mock_request_manager.post.assert_called_once_with(
        'https://api.github.com/repos/testowner/testrepo/labels',
        json={"name": "newlabel", "color": "FF0000", "description": "test"}
    )
    assert response.status_code == 201


def test_delete_label(pr_api, mock_request_manager):
    response = pr_api.delete_label("oldlabel")
    mock_request_manager.delete.assert_called_once_with(
        'https://api.github.com/repos/testowner/testrepo/labels/oldlabel'
    )
    assert response.status_code == 204
