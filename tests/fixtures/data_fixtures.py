import pytest
from data.issue_data import CREATE_ISSUE_PAYLOAD
from data.label_data import CREATE_LABEL_PAYLOAD, LABEL_NAME, LABEL_UPDATED_NAME
from data.repository_data import CREATE_REPO_PAYLOAD


@pytest.fixture
def issue(github_api):
    response = github_api.create_issue(CREATE_ISSUE_PAYLOAD)
    issue_number = response.json()["number"]
    yield issue_number
    github_api.close_issue(issue_number)


@pytest.fixture
def closed_issue(github_api):
    response = github_api.create_issue(CREATE_ISSUE_PAYLOAD)
    issue_number = response.json()["number"]
    github_api.close_issue(issue_number)
    yield issue_number
    github_api.close_issue(issue_number)


@pytest.fixture
def label(labels_api):
    labels_api.delete_label(LABEL_NAME)
    labels_api.delete_label(LABEL_UPDATED_NAME)
    response = labels_api.create_label(CREATE_LABEL_PAYLOAD)
    label_name = response.json()["name"]
    yield label_name
    labels_api.delete_label(LABEL_NAME)
    labels_api.delete_label(LABEL_UPDATED_NAME)


@pytest.fixture
def repository(repo_api):
    repo_api.delete_repo(CREATE_REPO_PAYLOAD["name"])
    yield CREATE_REPO_PAYLOAD["name"]
    repo_api.delete_repo(CREATE_REPO_PAYLOAD["name"])


@pytest.fixture
def profile_restore(github_user_api):
    original = github_user_api.get_authenticated_user().json()
    original_bio = original.get("bio")
    original_location = original.get("location")
    original_company = original.get("company")
    original_hireable = original.get("hireable")

    yield

    restore_payload = {}
    if original_bio is not None:
        restore_payload["bio"] = original_bio
    if original_location is not None:
        restore_payload["location"] = original_location
    if original_company is not None:
        restore_payload["company"] = original_company
    if original_hireable is not None:
        restore_payload["hireable"] = original_hireable

    if restore_payload:
        github_user_api.update_profile(restore_payload)
