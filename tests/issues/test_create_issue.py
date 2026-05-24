from jsonschema import validate

from utils.schemas import CREATE_ISSUE_SCHEMA
from data.issue_data import CREATE_ISSUE_PAYLOAD


def test_should_create_issue_successfully(github_api, request):

    # Arrange
    payload = CREATE_ISSUE_PAYLOAD

    # Act
    response = github_api.create_issue(payload)
    response_body = response.json()

    issue_number = response_body["number"]

    # Postcondition: close issue regardless of test outcome
    request.addfinalizer(lambda: github_api.close_issue(issue_number))

    # Assert 1 — Status Code
    assert response.status_code == 201

    # Assert 2 — Response Body
    assert response_body["title"] == payload["title"]
    assert response_body["body"] == payload["body"]

    # Assert 3 — Schema Validation
    validate(
        instance=response_body,
        schema=CREATE_ISSUE_SCHEMA
    )

    # Assert 4 — Integrity Check via GET
    get_response = github_api.get_issue(issue_number)
    get_body = get_response.json()

    assert get_body["title"] == payload["title"]
    assert get_body["body"] == payload["body"]
    assert get_body["state"] == "open"

    # Assert 5 — Default Values
    assert response_body["labels"] == []
    assert response_body["assignees"] == []
