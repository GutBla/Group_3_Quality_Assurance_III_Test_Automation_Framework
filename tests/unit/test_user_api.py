from unittest.mock import MagicMock, patch

import pytest

from services.github_user_api import GitHubUserAPI
from services.request_manager import RequestManager


@pytest.fixture
def mock_request_manager():
    with patch.object(RequestManager, '_instance', None), \
            patch('services.github_user_api.RequestManager') as \
            mock_request_manager_cls:
        mock_instance = MagicMock()
        mock_request_manager_cls.return_value = mock_instance

        mock_instance.get.return_value = MagicMock(
            status_code=200, json=lambda: {"login": "testuser", "id": 123}
        )
        mock_instance.patch.return_value = MagicMock(
            status_code=200, json=lambda: {"login": "testuser", "id": 123}
        )
        mock_instance.put.return_value = MagicMock(status_code=204)
        mock_instance.delete.return_value = MagicMock(status_code=204)
        mock_instance.head.return_value = MagicMock(status_code=204)
        mock_instance.post.return_value = MagicMock(
            status_code=201, json=lambda: {"emails": ["a@b.com"]}
        )

        yield mock_instance


@pytest.fixture
def user_api(mock_request_manager):
    with patch.dict('os.environ', {'BASE_URL': 'https://api.github.com'}):
        api = GitHubUserAPI()
        api.client = mock_request_manager
        return api


def test_get_authenticated_user(user_api, mock_request_manager):
    response = user_api.get_authenticated_user()
    mock_request_manager.get.assert_called_once_with('https://api.github.com/user')
    assert response.status_code == 200
    assert response.json() == {"login": "testuser", "id": 123}


def test_get_authenticated_user_with_custom_headers(
        user_api, mock_request_manager):
    custom_headers = {"Authorization": "Bearer fake"}
    user_api.get_authenticated_user(headers=custom_headers)
    mock_request_manager.get.assert_called_once_with(
        'https://api.github.com/user', headers=custom_headers
    )


def test_update_profile(user_api, mock_request_manager):
    payload = {"bio": "new bio", "location": "Mars"}
    response = user_api.update_profile(payload)
    mock_request_manager.patch.assert_called_once_with(
        'https://api.github.com/user', json=payload
    )
    assert response.status_code == 200


def test_get_user(user_api, mock_request_manager):
    username = "octocat"
    response = user_api.get_user(username)
    mock_request_manager.get.assert_called_once_with(
        'https://api.github.com/users/octocat'
    )
    assert response.status_code == 200


def test_follow_user(user_api, mock_request_manager):
    username = "testuser"
    response = user_api.follow_user(username)
    mock_request_manager.put.assert_called_once_with(
        'https://api.github.com/user/following/testuser'
    )
    assert response.status_code == 204


def test_unfollow_user(user_api, mock_request_manager):
    username = "testuser"
    response = user_api.unfollow_user(username)
    mock_request_manager.delete.assert_called_once_with(
        'https://api.github.com/user/following/testuser'
    )
    assert response.status_code == 204


def test_check_following(user_api, mock_request_manager):
    username = "testuser"
    response = user_api.check_following(username)
    mock_request_manager.head.assert_called_once_with(
        'https://api.github.com/user/following/testuser'
    )
    assert response.status_code == 204


def test_add_emails(user_api, mock_request_manager):
    emails = ["test@example.com", "test2@example.com"]
    response = user_api.add_emails(emails)
    mock_request_manager.post.assert_called_once_with(
        'https://api.github.com/user/emails', json={"emails": emails}
    )
    assert response.status_code == 201
