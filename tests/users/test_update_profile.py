from jsonschema import validate
from data.user_data import get_update_profile_payload
from utils.schemas import UPDATE_PROFILE_SCHEMA

def test_hltc18_update_profile(github_user_api, profile_restore):
    # Arrange
    payload = get_update_profile_payload()

    # Act
    response = github_user_api.update_profile(payload)
    body = response.json() if response.status_code == 200 else None

    # Assert
    assert response.status_code in [200, 204]
    if response.status_code == 200:
        assert body["bio"] == payload["bio"]
        assert body["location"] == payload["location"]
        validate(instance=body, schema=UPDATE_PROFILE_SCHEMA)