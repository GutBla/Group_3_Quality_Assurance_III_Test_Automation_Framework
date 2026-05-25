import time
from jsonschema import validate
from utils.schemas import CREATE_REPO_SCHEMA, UPDATE_REPO_SCHEMA, ERROR_REPO_SCHEMA
from data.repository_data import ( CREATE_REPO_PAYLOAD, UPDATE_DESCRIPTION_PAYLOAD, UPDATE_VISIBILITY_PAYLOAD, DUPLICATE_REPO_PAYLOAD)


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
    validate(instance=response_body, schema=CREATE_REPO_SCHEMA)

    # Assert 4 — Integrity Check via GET
    get_response = repo_api.get_repo(response_body["name"])
    get_body = get_response.json()

    assert get_body["name"] == payload["name"]
    assert get_body["description"] == payload["description"]
    assert get_body["private"] == payload["private"]

    # Assert 5 — Default Values
    assert response_body["fork"] is False
    assert response_body["owner"]["login"] == response_body["full_name"].split("/")[0]


def test_should_update_repository_description(repo_api, repository):

    # Arrange
    repo_api.create_repo(CREATE_REPO_PAYLOAD)
    payload = UPDATE_DESCRIPTION_PAYLOAD

    # Act
    response = repo_api.update_repo(CREATE_REPO_PAYLOAD["name"], payload)
    response_body = response.json()

    # Assert 1 — Status Code
    assert response.status_code == 200

    # Assert 2 — Response Body
    assert response_body["description"] == payload["description"]
    assert response_body["private"] == payload["private"]

    # Assert 3 — Schema Validation
    validate(instance=response_body, schema=UPDATE_REPO_SCHEMA)

    # Assert 4 — Integrity Check via GET
    get_response = repo_api.get_repo(CREATE_REPO_PAYLOAD["name"])
    get_body = get_response.json()

    assert get_body["description"] == payload["description"]


def test_should_change_repository_visibility_to_private(repo_api, repository):

    # Arrange
    repo_api.create_repo(CREATE_REPO_PAYLOAD)
    time.sleep(3)
    payload = UPDATE_VISIBILITY_PAYLOAD

    # Act
    response = repo_api.update_repo(CREATE_REPO_PAYLOAD["name"], payload)
    response_body = response.json()

    # Assert 1 — Status Code
    assert response.status_code == 200

    # Assert 2 — Response Body
    assert response_body["private"] is True
    assert response_body["visibility"] == "private"

    # Assert 3 — Schema Validation
    validate(instance=response_body, schema=UPDATE_REPO_SCHEMA)

    # Assert 4 — Integrity Check via GET
    get_response = repo_api.get_repo(CREATE_REPO_PAYLOAD["name"])
    get_body = get_response.json()

    assert get_body["private"] is True
    assert get_body["visibility"] == "private"



def test_should_delete_existing_repository(repo_api, repository):

    # Arrange
    repo_api.create_repo(CREATE_REPO_PAYLOAD)
    time.sleep(3)
    repo_name = CREATE_REPO_PAYLOAD["name"]

    # Act
    response = repo_api.delete_repo(repo_name)

    # Assert 1 — Status Code
    assert response.status_code == 204

    # Assert 2 — Integrity Check via GET
    get_response = repo_api.get_repo(repo_name)

    assert get_response.status_code == 404


def test_should_fail_when_creating_duplicate_repository(repo_api, repository):

    # Arrange
    repo_api.create_repo(CREATE_REPO_PAYLOAD)
    time.sleep(3)
    payload = DUPLICATE_REPO_PAYLOAD

    # Act
    response = repo_api.create_repo(payload)
    response_body = response.json()

    # Assert 1 — Status Code
    assert response.status_code == 422

    # Assert 2 — Response Body
    assert "already exists" in response_body["errors"][0]["message"]

    # Assert 3 — Schema Validation
    validate(instance=response_body, schema=ERROR_REPO_SCHEMA)