import pytest
from jsonschema import validate
from data.user_data import (
    PUBLIC_USERNAME, DISPOSABLE_EMAIL, FOLLOW_USERNAME,
    get_update_profile_payload, get_invalid_update_payload
)
from utils.schemas import (
    AUTH_USER_SCHEMA, PUBLIC_USER_SCHEMA,
    UPDATE_PROFILE_SCHEMA, EMAIL_ERROR_SCHEMA
)


# HLTC-16: Obtener usuario autenticado
def test_hltc16_get_authenticated_user(github_user_api):
    response = github_user_api.get_authenticated_user()
    body = response.json()

    assert response.status_code == 200
    assert body["login"] is not None
    assert isinstance(body["id"], int)
    validate(instance=body, schema=AUTH_USER_SCHEMA)


# HLTC-18: Actualizar perfil (campos editables)
def test_hltc18_update_profile(github_user_api, profile_restore):
    payload = get_update_profile_payload()

    response = github_user_api.update_profile(payload)
    body = response.json() if response.status_code == 200 else None

    assert response.status_code in [200, 204]
    if response.status_code == 200:
        assert body["bio"] == payload["bio"]
        assert body["location"] == payload["location"]
        validate(instance=body, schema=UPDATE_PROFILE_SCHEMA)


# HLTC-19: Actualizar perfil con datos inválidos (campos protegidos)
def test_hltc19_update_profile_invalid(github_user_api, profile_restore):
    original = github_user_api.get_authenticated_user().json()
    original_login = original["login"]
    original_id = original["id"]

    payload = get_invalid_update_payload(original_login, original_id, new_bio="Nueva API QA")
    expected_bio = payload["bio"]

    response = github_user_api.update_profile(payload)
    body = response.json()

    assert response.status_code == 200
    assert body["login"] == original_login
    assert body["id"] == original_id
    assert body["bio"] == expected_bio
    validate(instance=body, schema=UPDATE_PROFILE_SCHEMA)


# HLTC-20: Obtener información de perfil público (sin autenticación)
def test_hltc20_get_public_user(github_user_api):
    username = PUBLIC_USERNAME
    response = github_user_api.get_user(username)
    body = response.json()

    assert response.status_code == 200
    assert body["login"] == username
    assert "id" in body
    validate(instance=body, schema=PUBLIC_USER_SCHEMA)


# HLTC-24: Dejar de seguir a un usuario
def test_hltc24_unfollow_user(github_user_api):
    target = FOLLOW_USERNAME
    
    follow_resp = github_user_api.follow_user(target)
    assert follow_resp.status_code == 204

    check_resp = github_user_api.check_following(target)
    assert check_resp.status_code == 204

    unfollow_resp = github_user_api.unfollow_user(target)
    assert unfollow_resp.status_code == 204

    not_following_resp = github_user_api.check_following(target)
    assert not_following_resp.status_code == 404


# HLTC-25: Agregar email con dominio desechable
def test_hltc25_add_disposable_email_rejected(github_user_api):
    response = github_user_api.add_emails([DISPOSABLE_EMAIL])
    body = response.json()

    assert response.status_code == 422
    assert body["message"] == "Email domain could not be verified"
    assert "documentation_url" in body
    validate(instance=body, schema=EMAIL_ERROR_SCHEMA)