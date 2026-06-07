import time
import uuid
import pytest

from utils.schema_validator import validate_schema
from utils.schemas import (
    CREATE_REPO_SCHEMA,
    UPDATE_REPO_SCHEMA,
    ERROR_REPO_SCHEMA,
    LIST_REPOS_SCHEMA,
    CONTRIBUTORS_SCHEMA,
)
from data.repository_data import (
    make_repo_payload,
    UPDATE_DESCRIPTION_PAYLOAD,
    UPDATE_VISIBILITY_PAYLOAD,
)
from utils.logger import logger


@pytest.mark.functional
@pytest.mark.acceptance
@pytest.mark.smoke
def test_should_create_repository_successfully(repo_api, repository):
    # Arrange
    payload = make_repo_payload(repository)
    logger.info(f"Preparing payload for repository creation: {payload['name']}")

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

    # Assert 3 — Schema Validation (soft assertion)
    assert validate_schema(response_body, CREATE_REPO_SCHEMA)

    # Assert 4 — Integrity Check via GET
    get_response = repo_api.get_repo(response_body["name"])
    get_body = get_response.json()

    assert get_body["name"] == payload["name"]
    assert get_body["description"] == payload["description"]
    assert get_body["private"] == payload["private"]

    # Assert 5 — Default Values
    assert response_body["fork"] is False
    assert response_body["owner"]["login"] == response_body["full_name"].split("/")[0]


@pytest.mark.functional
@pytest.mark.regression
def test_should_update_repository_description(repo_api, repository):
    # Arrange
    repo_api.create_repo(make_repo_payload(repository))
    payload = UPDATE_DESCRIPTION_PAYLOAD
    logger.info(f"Updating description of repo '{repository}'")

    # Act
    response = repo_api.update_repo(repository, payload)
    response_body = response.json()

    # Assert 1 — Status Code
    assert response.status_code == 200

    # Assert 2 — Response Body
    assert response_body["description"] == payload["description"]
    assert response_body["private"] == payload["private"]

    # Assert 3 — Schema Validation (soft assertion)
    assert validate_schema(response_body, UPDATE_REPO_SCHEMA)

    # Assert 4 — Integrity Check via GET
    get_response = repo_api.get_repo(repository)
    get_body = get_response.json()
    assert get_body["description"] == payload["description"]


@pytest.mark.functional
@pytest.mark.regression
def test_should_change_repository_visibility_to_private(repo_api, repository):
    # Arrange
    repo_api.create_repo(make_repo_payload(repository))
    time.sleep(3)
    payload = UPDATE_VISIBILITY_PAYLOAD
    logger.info(f"Changing visibility of repo '{repository}' to private")

    # Act
    response = repo_api.update_repo(repository, payload)
    response_body = response.json()

    # Assert 1 — Status Code
    assert response.status_code == 200

    # Assert 2 — Response Body
    assert response_body["private"] is True
    assert response_body["visibility"] == "private"

    # Assert 3 — Schema Validation (soft assertion)
    assert validate_schema(response_body, UPDATE_REPO_SCHEMA)

    # Assert 4 — Integrity Check via GET
    get_response = repo_api.get_repo(repository)
    get_body = get_response.json()
    assert get_body["private"] is True
    assert get_body["visibility"] == "private"


@pytest.mark.functional
@pytest.mark.acceptance
@pytest.mark.smoke
def test_should_delete_existing_repository(repo_api, repository):
    # Arrange
    repo_api.create_repo(make_repo_payload(repository))
    time.sleep(3)
    logger.info(f"Preparing to delete repository '{repository}'")

    # Act
    response = repo_api.delete_repo(repository)

    # Assert 1 — Status Code
    assert response.status_code == 204

    # Assert 2 — Integrity Check via GET
    get_response = repo_api.get_repo(repository)
    assert get_response.status_code == 404


@pytest.mark.negative
@pytest.mark.regression
def test_should_fail_when_creating_duplicate_repository(repo_api, repository):
    # Arrange
    repo_api.create_repo(make_repo_payload(repository))
    time.sleep(3)
    logger.info(f"Attempting to create duplicate repo '{repository}'")

    # Act — mismo nombre,
    response = repo_api.create_repo(make_repo_payload(repository))
    response_body = response.json()

    # Assert 1 — Status Code
    assert response.status_code == 422

    # Assert 2 — Response Body
    assert "already exists" in response_body["errors"][0]["message"]

    # Assert 3 — Schema Validation (soft assertion)
    assert validate_schema(response_body, ERROR_REPO_SCHEMA)


@pytest.mark.functional
@pytest.mark.regression
def test_should_list_authenticated_user_repositories(repo_api, repository):
    # Arrange
    repo_api.create_repo(make_repo_payload(repository))
    logger.info(f"Listing repos, expecting '{repository}'")

    # Act
    response = repo_api.list_user_repos()
    response_body = response.json()

    # Assert 1 — Status Code
    assert response.status_code == 200

    # Assert 2 — Es una lista
    assert isinstance(response_body, list)
    assert len(response_body) > 0

    # Assert 3 — Schema Validation (soft assertion)
    assert validate_schema(response_body, LIST_REPOS_SCHEMA)

    # Assert 4 — Integrity
    repo_names = [r["name"] for r in response_body]
    assert repository in repo_names


@pytest.mark.functional
@pytest.mark.regression
def test_should_get_repository_contributors(repo_api, repository):
    # Arrange
    repo_api.create_repo(make_repo_payload(repository))
    logger.info(f"Getting contributors for repo '{repository}'")

    # Act
    response = repo_api.get_contributors(repository)

    # Assert 1 — Status Code
    assert response.status_code in [200, 204]

    if response.status_code == 200:
        response_body = response.json()
        assert isinstance(response_body, list)
        assert validate_schema(response_body, CONTRIBUTORS_SCHEMA)

    # Assert 4 — Integrity
    get_response = repo_api.get_repo(repository)
    assert get_response.status_code == 200


@pytest.mark.functional
@pytest.mark.regression
def test_should_create_repository_with_wiki_disabled(repo_api, repository):
    # Arrange
    payload = {
        "name": repository,
        "description": "Repo sin wiki",
        "private": False,
        "has_wiki": False,
    }
    logger.info(f"Creating repo '{repository}' with has_wiki=False")

    # Act
    response = repo_api.create_repo(payload)
    response_body = response.json()

    # Assert 1 — Status Code
    assert response.status_code == 201

    # Assert 2 — Response Body
    assert response_body["has_wiki"] is False
    assert response_body["name"] == repository

    # Assert 3 — Schema Validation (soft assertion)
    assert validate_schema(response_body, CREATE_REPO_SCHEMA)

    # Assert 4 — Integrity Check via GET
    get_response = repo_api.get_repo(repository)
    get_body = get_response.json()
    assert get_body["has_wiki"] is False


@pytest.mark.functional
@pytest.mark.regression
def test_should_disable_issues_on_existing_repository(repo_api, repository):
    # Arrange
    repo_api.create_repo(make_repo_payload(repository))
    payload = {"has_issues": False}
    logger.info(f"Disabling issues on repo '{repository}'")

    # Act
    response = repo_api.update_repo(repository, payload)
    response_body = response.json()

    # Assert 1 — Status Code
    assert response.status_code == 200

    # Assert 2 — Response Body
    assert response_body["has_issues"] is False

    # Assert 3 — Schema Validation (soft assertion)
    assert validate_schema(response_body, UPDATE_REPO_SCHEMA)

    # Assert 4 — Integrity Check via GET
    get_response = repo_api.get_repo(repository)
    get_body = get_response.json()
    assert get_body["has_issues"] is False


@pytest.mark.negative
@pytest.mark.regression
def test_should_fail_to_delete_nonexistent_repository(repo_api):
    # Arrange
    fake_repo = f"repo-inexistente-{uuid.uuid4().hex[:8]}"
    logger.info(f"Attempting to DELETE non-existent repo '{fake_repo}'")

    # Act
    response = repo_api.delete_repo(fake_repo)
    response_body = response.json()

    # Assert 1 — Status Code
    assert response.status_code == 404

    # Assert 2 — Response Body
    assert response_body["message"] == "Not Found"

    # Assert 3 — No contiene campos de repo válido
    assert "id" not in response_body
    assert "name" not in response_body
