import re
from jsonschema import validate
from utils.logger import logger
from utils.schemas import (
    CREATE_ISSUE_SCHEMA,
    ERROR_VALIDATION_ISSUE_SCHEMA,
    UPDATE_ISSUE_SCHEMA,
    NOT_FOUND_ISSUE_SCHEMA
)
from data.issue_data import (
    CREATE_ISSUE_PAYLOAD,
    MISSING_TITLE_ISSUE_PAYLOAD,
    UPDATE_ISSUE_PAYLOAD,
    INVALID_ISSUE_NUMBER,
    CLOSE_ISSUE_PAYLOAD
)


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

    # Assert 3 — Schema Validation
    logger.info("Validating response schema against CREATE_ISSUE_SCHEMA")
    validate(
        instance=response_body,
        schema=CREATE_ISSUE_SCHEMA
    )

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

    # Assert 3 — Schema Validation
    logger.info("Validating error response schema")
    validate(
        instance=response_body,
        schema=ERROR_VALIDATION_ISSUE_SCHEMA
    )

    # Assert 4 — Data Integrity Check
    logger.info("Executing integrity check via GET")
    get_all_response = github_api.client.get(github_api.base_url + "/issues")
    issues_list = get_all_response.json()

    exists_invalid = any(
        not issue.get("title") or issue.get("title") == ""
        for issue in issues_list
    )
    assert exists_invalid is False

    # Assert 5 — Negative Validation
    logger.info("Verifying no resource ID was generated")
    assert "id" not in response_body


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

    # Assert 3 — Schema Validation
    logger.info("Validating schema against UPDATE_ISSUE_SCHEMA")
    validate(
        instance=response_body,
        schema=UPDATE_ISSUE_SCHEMA
    )

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


def test_should_fail_to_update_issue_when_id_is_invalid(github_api):
    # Arrange
    invalid_id = INVALID_ISSUE_NUMBER
    payload = CLOSE_ISSUE_PAYLOAD
    logger.info(f"Preparing PATCH request for non-existent issue #{invalid_id}")

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

    # Assert 3 — Schema Validation
    logger.info("Validating 404 error response schema")
    validate(
        instance=response_body,
        schema=NOT_FOUND_ISSUE_SCHEMA
    )

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

    # Assert 3 — Schema Validation
    logger.info("Validating issue response schema against UPDATE_ISSUE_SCHEMA")
    validate(
        instance=response_body,
        schema=UPDATE_ISSUE_SCHEMA
    )

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
