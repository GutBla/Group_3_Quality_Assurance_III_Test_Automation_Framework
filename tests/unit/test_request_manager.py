import os
import pytest
from unittest.mock import MagicMock, patch
from services.request_manager import RequestManager


def _make_fake_response(status_code=200, json_data=None, raise_json=False):
    mock_resp = MagicMock()
    mock_resp.status_code = status_code
    if raise_json:
        mock_resp.json.side_effect = ValueError("No es JSON")
    else:
        mock_resp.json.return_value = json_data or {}
    return mock_resp


@pytest.fixture()
def rm_with_mock_session():
    rm = RequestManager()
    mock_session = MagicMock()
    mock_session.get.return_value = _make_fake_response(200)
    mock_session.post.return_value = _make_fake_response(201)
    mock_session.put.return_value = _make_fake_response(204)
    mock_session.patch.return_value = _make_fake_response(200)
    mock_session.delete.return_value = _make_fake_response(204)
    mock_session.head.return_value = _make_fake_response(204)

    with patch.object(rm, "session", mock_session):
        yield rm, mock_session

def test_request_manager_singleton():
    rm1 = RequestManager()
    rm2 = RequestManager()
    assert rm1 is rm2

def test_log_response_non_json(rm_with_mock_session):
    rm, _ = rm_with_mock_session
    mock_response = _make_fake_response(status_code=200, raise_json=True)
    rm._log_response(mock_response)


def test_initialize_missing_token():
    with patch.object(
        RequestManager,
        "_initialize",
        side_effect=EnvironmentError("ACCESS_TOKEN no está configurado."),
    ):
        with pytest.raises(EnvironmentError, match="ACCESS_TOKEN no está configurado."):
            obj = object.__new__(RequestManager)
            obj._initialize()

def test_get_method_calls_session(rm_with_mock_session):
    rm, mock_session = rm_with_mock_session
    url = "https://api.github.com/user"

    response = rm.get(url)

    mock_session.get.assert_called_once_with(url)
    assert response.status_code == 200


def test_post_method_calls_session(rm_with_mock_session):
    rm, mock_session = rm_with_mock_session
    url = "https://api.github.com/user/emails"
    payload = {"emails": ["test@example.com"]}

    response = rm.post(url, json=payload)

    mock_session.post.assert_called_once_with(url, json=payload)
    assert response.status_code == 201


def test_patch_method_calls_session(rm_with_mock_session):
    rm, mock_session = rm_with_mock_session
    url = "https://api.github.com/user"
    payload = {"bio": "Test bio"}

    response = rm.patch(url, json=payload)

    mock_session.patch.assert_called_once_with(url, json=payload)
    assert response.status_code == 200


def test_put_method_calls_session(rm_with_mock_session):
    rm, mock_session = rm_with_mock_session
    url = "https://api.github.com/user/following/octocat"

    response = rm.put(url)

    mock_session.put.assert_called_once_with(url)
    assert response.status_code == 204


def test_delete_method_calls_session(rm_with_mock_session):
    rm, mock_session = rm_with_mock_session
    url = "https://api.github.com/user/following/octocat"

    response = rm.delete(url)

    mock_session.delete.assert_called_once_with(url)
    assert response.status_code == 204


def test_head_method_calls_session(rm_with_mock_session):
    rm, mock_session = rm_with_mock_session
    url = "https://api.github.com/user/following/octocat"

    response = rm.head(url)

    mock_session.head.assert_called_once_with(url)
    assert response.status_code == 204


def test_log_request_with_json_body(rm_with_mock_session):
    rm, _ = rm_with_mock_session
    rm._log_request("POST", "https://api.github.com/user/emails", json={"emails": []})


def test_log_request_with_override_headers(rm_with_mock_session):
    rm, _ = rm_with_mock_session
    rm._log_request(
        "GET",
        "https://api.github.com/user",
        headers={"Authorization": "Bearer bad_token"},
    )


def test_get_with_custom_headers_passes_them_through(rm_with_mock_session):
    rm, mock_session = rm_with_mock_session
    url = "https://api.github.com/user"
    bad_headers = {"Authorization": "Bearer token_invalido"}

    rm.get(url, headers=bad_headers)

    mock_session.get.assert_called_once_with(url, headers=bad_headers)