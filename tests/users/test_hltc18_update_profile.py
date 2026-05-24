from jsonschema import validate
from data.user_data import UPDATE_PROFILE_PAYLOAD
from utils.schemas import UPDATE_PROFILE_SCHEMA


def test_should_update_authenticated_user_profile_successfully(github_user_api):
    payload = UPDATE_PROFILE_PAYLOAD

    response = github_user_api.update_profile(payload)

    assert response.status_code in [200, 204]

    if response.status_code == 200:
        body = response.json()

        assert body["bio"] == payload["bio"]
        assert body["location"] == payload["location"]

        validate(instance=body, schema=UPDATE_PROFILE_SCHEMA)

        assert body["login"] is not None
        assert isinstance(body["id"], int)
