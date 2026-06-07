import re

import pytest

from data.issue_data import (CLOSE_ISSUE_PAYLOAD, CREATE_COMMENT_PAYLOAD,
                             CREATE_ISSUE_PAYLOAD, INVALID_AUTH_HEADERS,
                             INVALID_ISSUE_NUMBER, LONG_TITLE_PAYLOAD,
                             MISSING_TITLE_ISSUE_PAYLOAD,
                             NON_EXISTENT_REPO_NAME, UPDATE_ISSUE_PAYLOAD)
from utils.logger import logger
from utils.schema_validator import validate_schema
from utils.schemas import (CREATE_COMMENT_SCHEMA, CREATE_ISSUE_SCHEMA,
                           ERROR_NOT_FOUND_SCHEMA,
                           ERROR_VALIDATION_ISSUE_SCHEMA,
                           ERROR_VALIDATION_SCHEMA, UNAUTHORIZED_ERROR_SCHEMA,
                           UPDATE_ISSUE_SCHEMA)


@pytest.mark.functional
@pytest.mark.acceptance
@pytest.mark.smoke
def test_should_create_issue_successfully(github_api):
    # Arrange
    payload = CREATE_ISSUE_PAYLOAD
    logger.info(f"Preparing payload for issue creation: {payload['title']}")

    # Act
    logger.info("Executing API request to create a new issue")
    response = github_api.create_issue(payload)
    response_body = response.json()
    issue_number = response_body["number"]

    # Assert 1 — Status Code
    logger.info("Verifying response status code is 201")
    assert response.status_code == 201

    # Assert 2 — Response Body Match
    logger.info("Verifying response body contains matching payload data")
    assert response_body["title"] == payload["title"]
    assert response_body["body"] == payload["body"]

    # Assert 3 — Schema Validation (soft assertion)
    logger.info("Validating response schema against CREATE_ISSUE_SCHEMA")
    assert validate_schema(response_body, CREATE_ISSUE_SCHEMA)

    # Assert 4 — Integrity Check via GET
    logger.info(f"Executing integrity check via GET for issue #{issue_number}")
    get_response = github_api.get_issue(issue_number)
    get_body = get_response.json()

    assert get_body["title"] == payload["title"]
    assert get_body["body"] == payload["body"]
    assert get_body["state"] == "open"

    # Assert 5 — Default Values
    logger.info("Verifying default values for labels and assignees are empty")
    assert response_body["labels"] == []
    assert response_body["assignees"] == []


@pytest.mark.negative
@pytest.mark.regression
def test_should_fail_to_create_issue_when_title_is_missing(github_api):
    # Arrange
    payload = MISSING_TITLE_ISSUE_PAYLOAD
    logger.info("Preparing invalid payload: missing title")

    # Act
    logger.info("Executing API request to create an issue with missing title")
    response = github_api.create_issue(payload)
    response_body = response.json()

    # Assert 1 — Status Code
    logger.info("Verifying response status code is 422")
    assert response.status_code == 422

    # Assert 2 — Response Body (Error Message validation)
    logger.info("Verifying error message matches validation keywords")
    assert "message" in response_body
    if "errors" in response_body:
        assert isinstance(response_body["errors"], list)

    assert re.search(
        r"invalid|validation|request|title",
        response_body["message"],
        re.IGNORECASE
    )

    # Assert 3 — Schema Validation (soft assertion)
    logger.info("Validating error response schema")
    assert validate_schema(response_body, ERROR_VALIDATION_ISSUE_SCHEMA)

    # Assert 4 — Data Integrity Check
    logger.info("Executing integrity check via GET")
    get_all_response = github_api.client.get(
        github_api.default_base_url + "/issues")
    issues_list = get_all_response.json()

    exists_invalid = any(
        not issue.get("title") or issue.get("title") == ""
        for issue in issues_list
    )
    assert exists_invalid is False

    # Assert 5 — Negative Validation
    logger.info("Verifying no resource ID was generated")
    assert "id" not in response_body


@pytest.mark.functional
@pytest.mark.regression
def test_should_update_issue_successfully(github_api, issue):
    # Arrange
    issue_number = issue
    payload = UPDATE_ISSUE_PAYLOAD
    logger.info(f"Updating issue #{issue_number} with new title and body")

    # Act
    response = github_api.update_issue(issue_number, payload)
    response_body = response.json()

    # Assert 1 — Status Code
    logger.info("Verifying response status code is 200")
    assert response.status_code == 200

    # Assert 2 — Response Body Match
    logger.info("Verifying response body values match the updated payload")
    assert response_body["title"] == payload["title"]
    assert response_body["body"] == payload["body"]

    # Assert 3 — Schema Validation (soft assertion)
    logger.info("Validating schema against UPDATE_ISSUE_SCHEMA")
    assert validate_schema(response_body, UPDATE_ISSUE_SCHEMA)

    # Assert 4 — Data Integrity via GET
    logger.info("Executing integrity check via GET to verify persistence")
    get_response = github_api.get_issue(issue_number)
    get_body = get_response.json()

    assert get_body["title"] == payload["title"]
    assert get_body["body"] == payload["body"]
    assert get_body["number"] == issue_number

    # Assert 5 — Default Value Consistency
    logger.info("Verifying default values and state consistency")
    assert get_body["state"] in ["open", "closed"]
    assert get_body["labels"] == []
    assert get_body["assignees"] == []


@pytest.mark.negative
@pytest.mark.regression
def test_should_fail_to_update_issue_when_id_is_invalid(github_api):
    # Arrange
    invalid_id = INVALID_ISSUE_NUMBER
    payload = CLOSE_ISSUE_PAYLOAD
    logger.info(
        f"Preparing PATCH request for non-existent issue #{invalid_id}")

    # Act
    response = github_api.update_issue(invalid_id, payload)
    response_body = response.json()

    # Assert 1 — Status Code
    logger.info("Verifying response status code is 404")
    assert response.status_code == 404

    # Assert 2 — Response Body Message
    logger.info("Verifying error message includes 'Not Found'")
    assert "message" in response_body
    assert "Not Found" in response_body["message"]

    # Assert 3 — Schema Validation (soft assertion)
    logger.info("Validating 404 error response schema")
    assert validate_schema(response_body, ERROR_NOT_FOUND_SCHEMA)

    # Assert 4 — Data Integrity Check via GET
    logger.info("Executing integrity check: GET should also return 404")
    get_response = github_api.get_issue(invalid_id)
    get_body = get_response.json()

    assert get_response.status_code == 404
    assert "Not Found" in get_body["message"]

    # Assert 5 — Negative Validation
    logger.info("Verifying response doesn't contain state or id keys")
    assert "state" not in response_body
    assert "id" not in response_body


@pytest.mark.functional
@pytest.mark.acceptance
@pytest.mark.smoke
def test_should_close_issue_successfully(github_api, issue):
    # Arrange
    issue_number = issue
    payload = CLOSE_ISSUE_PAYLOAD
    logger.info(f"Changing status of issue #{issue_number} to 'closed'")

    # Act
    response = github_api.update_issue(issue_number, payload)
    response_body = response.json()

    # Assert 1 — Status Code
    logger.info("Verifying response status code is 200")
    assert response.status_code == 200

    # Assert 2 — Response Body (State Transition)
    logger.info("Verifying issue state is now 'closed' in response body")
    assert response_body["state"] == "closed"
    assert response_body["number"] == issue_number

    # Assert 3 — Schema Validation (soft assertion)
    logger.info("Validating issue response schema against UPDATE_ISSUE_SCHEMA")
    assert validate_schema(response_body, UPDATE_ISSUE_SCHEMA)

    # Assert 4 — Data Integrity Check via GET
    logger.info("Executing integrity check via GET to verify persistence")
    get_response = github_api.get_issue(issue_number)
    get_body = get_response.json()

    assert get_response.status_code == 200
    assert get_body["state"] == "closed"
    assert get_body["number"] == issue_number

    # Assert 5 — Default Value Consistency
    logger.info("Verifying core fields consistency and default values")
    assert get_body["title"] is not None
    assert get_body["body"] is not None
    assert get_body["labels"] == []
    assert get_body["assignees"] == []


@pytest.mark.negative
@pytest.mark.smoke
def test_should_fail_to_create_issue_when_token_is_invalid(github_api):
    # Arrange
    payload = CREATE_ISSUE_PAYLOAD
    headers = INVALID_AUTH_HEADERS
    logger.info(
        "Preparing valid payload but injecting an invalid authorization header")

    # Act
    logger.info("Executing API request to create an issue with bad credentials")
    response = github_api.create_issue(payload, headers=headers)
    response_body = response.json()

    # Assert 1 — Status Code
    logger.info("Verifying response status code is 401")
    assert response.status_code == 401

    # Assert 2 — Response Body Match
    logger.info(
        "Verifying error message matches GitHub standard for bad credentials")
    assert response_body["message"] == "Bad credentials"

    # Assert 3 — Schema Validation (soft assertion)
    logger.info("Validating response schema against UNAUTHORIZED_ERROR_SCHEMA")
    assert validate_schema(response_body, UNAUTHORIZED_ERROR_SCHEMA)


@pytest.mark.negative
@pytest.mark.regression
def test_should_fail_to_create_issue_when_title_exceeds_length_limit(
        github_api):
    # Arrange
    payload = LONG_TITLE_PAYLOAD
    logger.info("Preparing payload with a title exceeding 1024 characters")

    # Act
    logger.info(
        "Executing API request to create an issue with an oversized title")
    response = github_api.create_issue(payload)
    response_body = response.json()

    # Assert 1 — Status Code
    logger.info("Verifying response status code is 422")
    assert response.status_code == 422

    # Assert 2 — Response Body Match
    logger.info("Verifying response body contains validation error message")
    assert "Validation Failed" in response_body["message"]
    assert response_body["errors"][0]["field"] == "title"
    assert response_body["errors"][0]["code"] == "invalid"

    # Assert 3 — Schema Validation (soft assertion)
    logger.info("Validating response schema against ERROR_VALIDATION_SCHEMA")
    assert validate_schema(response_body, ERROR_VALIDATION_SCHEMA)


@pytest.mark.negative
@pytest.mark.regression
def test_should_fail_to_create_issue_when_repo_does_not_exist(github_api):
    # Arrange
    payload = CREATE_ISSUE_PAYLOAD
    fake_repo = NON_EXISTENT_REPO_NAME
    logger.info(
        f"Preparing to send issue payload to non-existent repo: {fake_repo}"
    )

    # Act
    logger.info(
        f"Executing API request targeting fake repository '{fake_repo}'")
    response = github_api.create_issue(payload, repo=fake_repo)
    response_body = response.json()

    # Assert 1 — Status Code
    logger.info("Verifying response status code is 404")
    assert response.status_code == 404

    # Assert 2 — Response Body Match
    logger.info("Verifying error message matches GitHub standard for Not Found")
    assert response_body["message"] == "Not Found"

    # Assert 3 — Schema Validation (soft assertion)
    logger.info("Validating response schema against ERROR_NOT_FOUND_SCHEMA")
    assert validate_schema(response_body, ERROR_NOT_FOUND_SCHEMA)


@pytest.mark.functional
@pytest.mark.regression
def test_should_add_comment_to_existing_issue_successfully(github_api, issue):
    # Arrange
    issue_number = issue
    payload = CREATE_COMMENT_PAYLOAD
    logger.info(
        f"Preparing payload for comment creation on issue #{issue_number}")

    # Act
    logger.info(
        f"Executing API request to add comment to issue #{issue_number}")
    response = github_api.create_comment(issue_number, payload)
    response_body = response.json()

    # Assert 1 — Status Code
    logger.info("Verifying response status code is 201")
    assert response.status_code == 201

    # Assert 2 — Response Body Match
    logger.info("Verifying comment body contains matching payload data")
    assert response_body["body"] == payload["body"]

    # Assert 3 — Schema Validation (soft assertion)
    logger.info("Validating response schema against CREATE_COMMENT_SCHEMA")
    assert validate_schema(response_body, CREATE_COMMENT_SCHEMA)


@pytest.mark.functional
@pytest.mark.regression
def test_should_reopen_closed_issue_successfully(github_api, closed_issue):
    # Arrange
    issue_number = closed_issue
    payload = {"state": "open"}
    logger.info(f"Preparing to reopen previously closed issue #{issue_number}")

    # Act
    logger.info(
        f"Executing API PATCH request to open state for issue #{issue_number}"
    )
    response = github_api.update_issue(issue_number, payload)
    response_body = response.json()

    # Assert 1 — Status Code
    logger.info("Verifying response status code is 200")
    assert response.status_code == 200

    # Assert 2 — Response Body Match
    logger.info("Verifying response body reflects the state change to 'open'")
    assert response_body["state"] == "open"
    assert response_body["number"] == issue_number

    # Assert 3 — Schema Validation (soft assertion)
    logger.info("Validating response schema against CREATE_ISSUE_SCHEMA")
    assert validate_schema(response_body, CREATE_ISSUE_SCHEMA)

    # Assert 4 — Integrity Check via GET
    logger.info(f"Executing integrity check via GET for issue #{issue_number}")
    get_response = github_api.get_issue(issue_number)
    get_body = get_response.json()

    assert get_body["state"] == "open"
