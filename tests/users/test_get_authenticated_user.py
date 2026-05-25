from jsonschema import validate
from utils.schemas import AUTH_USER_SCHEMA

def test_hltc16_get_authenticated_user(github_user_api):
    # Arrange
    # No se necesita

    # Act
    response = github_user_api.get_authenticated_user()
    body = response.json()

    # Assert
    assert response.status_code == 200
    assert body["login"] is not None
    assert isinstance(body["id"], int)
    validate(instance=body, schema=AUTH_USER_SCHEMA)