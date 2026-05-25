from jsonschema import validate
from data.user_data import get_invalid_update_payload
from utils.schemas import UPDATE_PROFILE_SCHEMA

def test_hltc19_update_profile_invalid(github_user_api, profile_restore):
    # Arrange
    original = github_user_api.get_authenticated_user().json()
    original_login = original["login"]
    original_id = original["id"]

    payload = get_invalid_update_payload(original_login, original_id)
    new_bio = payload["bio"]

    # Act
    response = github_user_api.update_profile(payload)
    body = response.json()

    # Assert
    assert response.status_code == 200

    assert body["login"] == original_login
    assert body["id"] == original_id

    assert body["bio"] == new_bio
    validate(instance=body, schema=UPDATE_PROFILE_SCHEMA)