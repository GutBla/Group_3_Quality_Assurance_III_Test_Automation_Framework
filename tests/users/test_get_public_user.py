from jsonschema import validate
from services.github_api import get_user
from data.user_data import PUBLIC_USERNAME
from utils.schemas import PUBLIC_USER_SCHEMA

def test_hltc20_get_public_user():
    # Arrange
    username = PUBLIC_USERNAME

    # Act
    response = get_user(username)
    body = response.json()

    # Assert
    assert response.status_code == 200
    assert body["login"] == username
    assert "id" in body
    validate(instance=body, schema=PUBLIC_USER_SCHEMA)