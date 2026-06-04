import time
import pytest
from jsonschema import validate

from utils.schemas import (
    CREATE_REPO_SCHEMA,
    UPDATE_REPO_SCHEMA,
    ERROR_REPO_SCHEMA,
    LIST_REPOS_SCHEMA,
    CONTRIBUTORS_SCHEMA)
from data.repository_data import (
    CREATE_REPO_PAYLOAD,
    UPDATE_DESCRIPTION_PAYLOAD,
    UPDATE_VISIBILITY_PAYLOAD,
    DUPLICATE_REPO_PAYLOAD, )
from utils.logger import logger


@pytest.mark.functional
@pytest.mark.acceptance
@pytest.mark.smoke
def test_should_create_repository_successfully(repo_api, repository):
    # Arrange
    payload = CREATE_REPO_PAYLOAD.copy()
    payload["name"] = repository
    logger.info(f"Preparing payload for repository creation: {payload['name']}")

    # Act
    logger.info("Executing API request to create a new repository")
    response = repo_api.create_repo(payload)
    response_body = response.json()

    # Assert 1 — Status Code
    logger.info("Verifying response status code is 201")
    assert response.status_code == 201

    # Assert 2 — Response Body
    logger.info("Verifying response body contains matching payload data")
    assert response_body["name"] == repository
    assert response_body["description"] == payload["description"]
    assert response_body["private"] == payload["private"]
    assert response_body["has_issues"] == payload["has_issues"]

    # Assert 3 — Schema Validation
    logger.info("Validating response schema against CREATE_REPO_SCHEMA")
    validate(instance=response_body, schema=CREATE_REPO_SCHEMA)

    # Assert 4 — Integrity Check via GET
    logger.info(f"Executing integrity check via GET for repo '{response_body['name']}'")
    get_response = repo_api.get_repo(response_body["name"])
    get_body = get_response.json()

    assert get_body["name"] == repository
    assert get_body["description"] == payload["description"]
    assert get_body["private"] == payload["private"]

    # Assert 5 — Default Values
    logger.info("Verifying default values: fork is False and owner matches")
    assert response_body["fork"] is False
    assert response_body["owner"]["login"] == response_body["full_name"].split("/")[0]


@pytest.mark.functional
@pytest.mark.regression
def test_should_update_repository_description(repo_api, repository):
    # Arrange
    repo_api.create_repo({**CREATE_REPO_PAYLOAD, "name": repository})
    payload = UPDATE_DESCRIPTION_PAYLOAD
    logger.info(f"Updating description of repo '{repository}'")

    # Act
    logger.info("Executing PATCH request to update repository description")
    response = repo_api.update_repo(repository, payload)
    response_body = response.json()

    # Assert 1 — Status Code
    logger.info("Verifying response status code is 200")
    assert response.status_code == 200

    # Assert 2 — Response Body
    logger.info("Verifying description and private fields match payload")
    assert response_body["description"] == payload["description"]
    assert response_body["private"] == payload["private"]

    # Assert 3 — Schema Validation
    logger.info("Validating response schema against UPDATE_REPO_SCHEMA")
    validate(instance=response_body, schema=UPDATE_REPO_SCHEMA)

    # Assert 4 — Integrity Check via GET
    logger.info("Executing integrity check via GET to verify description persistence")
    get_response = repo_api.get_repo(repository)
    get_body = get_response.json()

    assert get_body["description"] == payload["description"]


@pytest.mark.functional
@pytest.mark.regression
def test_should_change_repository_visibility_to_private(repo_api, repository):
    # Arrange
    repo_api.create_repo({**CREATE_REPO_PAYLOAD, "name": repository})
    time.sleep(3)
    payload = UPDATE_VISIBILITY_PAYLOAD
    logger.info(f"Changing visibility of repo '{repository}' to private")

    # Act
    logger.info("Executing PATCH request to change repository visibility")
    response = repo_api.update_repo(repository, payload)
    response_body = response.json()

    # Assert 1 — Status Code
    logger.info("Verifying response status code is 200")
    assert response.status_code == 200

    # Assert 2 — Response Body
    logger.info("Verifying private is True and visibility is 'private'")
    assert response_body["private"] is True
    assert response_body["visibility"] == "private"

    # Assert 3 — Schema Validation
    logger.info("Validating response schema against UPDATE_REPO_SCHEMA")
    validate(instance=response_body, schema=UPDATE_REPO_SCHEMA)

    # Assert 4 — Integrity Check via GET
    logger.info("Executing integrity check via GET to verify visibility persistence")
    get_response = repo_api.get_repo(repository)
    get_body = get_response.json()

    assert get_body["private"] is True
    assert get_body["visibility"] == "private"


@pytest.mark.functional
@pytest.mark.acceptance
@pytest.mark.smoke
def test_should_delete_existing_repository(repo_api, repository):
    # Arrange
    repo_api.create_repo({**CREATE_REPO_PAYLOAD, "name": repository})
    time.sleep(3)
    logger.info(f"Preparing to delete repository '{repository}'")

    # Act
    logger.info("Executing DELETE request to remove repository")
    response = repo_api.delete_repo(repository)

    # Assert 1 — Status Code
    logger.info("Verifying response status code is 204")
    assert response.status_code == 204

    # Assert 2 — Integrity Check via GET
    logger.info("Executing integrity check via GET: repo should return 404")
    get_response = repo_api.get_repo(repository)

    assert get_response.status_code == 404


@pytest.mark.negative
@pytest.mark.regression
def test_should_fail_when_creating_duplicate_repository(repo_api, repository):
    # Arrange
    repo_api.create_repo({**CREATE_REPO_PAYLOAD, "name": repository})
    time.sleep(3)
    payload = DUPLICATE_REPO_PAYLOAD.copy()
    payload["name"] = repository
    logger.info(f"Attempting to create duplicate repo '{payload['name']}'")

    # Act
    logger.info("Executing second POST request with same repository name")
    response = repo_api.create_repo(payload)
    response_body = response.json()

    # Assert 1 — Status Code
    logger.info("Verifying response status code is 422")
    assert response.status_code == 422

    # Assert 2 — Response Body
    logger.info("Verifying error message contains 'already exists'")
    assert "already exists" in response_body["errors"][0]["message"]

    # Assert 3 — Schema Validation
    logger.info("Validating error response schema against ERROR_REPO_SCHEMA")
    validate(instance=response_body, schema=ERROR_REPO_SCHEMA)


@pytest.mark.functional
@pytest.mark.regression
def test_should_list_authenticated_user_repositories(repo_api, repository):
    # Arrange
    repo_api.create_repo({**CREATE_REPO_PAYLOAD, "name": repository})
    logger.info(f"Listing repos for authenticated user, expecting '{repository}'")

    # Act
    response = repo_api.list_user_repos()
    response_body = response.json()

    # Assert 1 — Status Code
    assert response.status_code == 200

    # Assert 2 — Es una lista
    assert isinstance(response_body, list)
    assert len(response_body) > 0

    # Assert 3 — Schema Validation
    validate(instance=response_body, schema=LIST_REPOS_SCHEMA)

    # Assert 4 — Integrity:
    repo_names = [r["name"] for r in response_body]
    assert repository in repo_names


@pytest.mark.functional
@pytest.mark.regression
def test_should_get_repository_contributors(repo_api, repository):
    # Arrange
    repo_api.create_repo({**CREATE_REPO_PAYLOAD, "name": repository})
    logger.info(f"Getting contributors for repo '{repository}'")

    # Act
    response = repo_api.get_contributors(repository)

    # Assert 1 — Status Code
    assert response.status_code in [200, 204]

    if response.status_code == 200:
        response_body = response.json()

        # Assert 2 — Es una lista
        assert isinstance(response_body, list)

        # Assert 3 — Schema Validation
        validate(instance=response_body, schema=CONTRIBUTORS_SCHEMA)

    # Assert 4 — Integrity: el repo existe
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
    logger.info(f"Creating repo '{payload['name']}' with has_wiki=False")

    # Act
    response = repo_api.create_repo(payload)
    response_body = response.json()

    # Assert 1 — Status Code
    assert response.status_code == 201

    # Assert 2 — Response Body
    assert response_body["has_wiki"] is False
    assert response_body["name"] == payload["name"]

    # Assert 3 — Schema Validation
    validate(instance=response_body, schema=CREATE_REPO_SCHEMA)

    # Assert 4 — Integrity Check via GET
    get_response = repo_api.get_repo(payload["name"])
    get_body = get_response.json()
    assert get_body["has_wiki"] is False


@pytest.mark.functional
@pytest.mark.regression
def test_should_disable_issues_on_existing_repository(repo_api, repository):
    # Arrange
    repo_api.create_repo({**CREATE_REPO_PAYLOAD, "name": repository})
    payload = {"has_issues": False}
    logger.info(f"Disabling issues on repo '{repository}'")

    # Act
    response = repo_api.update_repo(repository, payload)
    response_body = response.json()

    # Assert 1 — Status Code
    assert response.status_code == 200

    # Assert 2 — Response Body
    assert response_body["has_issues"] is False

    # Assert 3 — Schema Validation
    validate(instance=response_body, schema=UPDATE_REPO_SCHEMA)

    # Assert 4 — Integrity Check via GET
    get_response = repo_api.get_repo(repository)
    get_body = get_response.json()
    assert get_body["has_issues"] is False


@pytest.mark.negative
@pytest.mark.regression
def test_should_fail_to_delete_nonexistent_repository(repo_api):
    # Arrange
    fake_repo = "repo-que-no-existe-xyz-99999"
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
