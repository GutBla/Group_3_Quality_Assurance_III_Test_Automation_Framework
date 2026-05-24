from jsonschema import validate
from utils.schemas import CREATE_REPO_SCHEMA
from data.repository_data import CREATE_REPO_PAYLOAD


def test_should_create_repository_successfully(repo_api, repository):

    # Arrange
    payload = CREATE_REPO_PAYLOAD

    # Act
    response = repo_api.create_repo(payload)
    response_body = response.json()

    # Assert 1 — Status Code
    assert response.status_code == 201

    # Assert 2 — Response Body
    assert response_body["name"] == payload["name"]
    assert response_body["description"] == payload["description"]
    assert response_body["private"] == payload["private"]
    assert response_body["has_issues"] == payload["has_issues"]

    # Assert 3 — Schema Validation
    validate(
        instance=response_body,
        schema=CREATE_REPO_SCHEMA
    )

    # Assert 4 — Integrity Check via GET
    get_response = repo_api.get_repo(response_body["name"])
    get_body = get_response.json()

    assert get_body["name"] == payload["name"]
    assert get_body["description"] == payload["description"]
    assert get_body["private"] == payload["private"]

    # Assert 5 — Default Values
    assert response_body["fork"] is False
    assert response_body["owner"]["login"] == response_body["full_name"].split("/")[0]
