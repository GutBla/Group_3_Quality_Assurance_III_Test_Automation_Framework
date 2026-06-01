import pytest

from data.issue_data import CREATE_ISSUE_PAYLOAD
from data.label_data import (CREATE_LABEL_PAYLOAD, LABEL_NAME,
                             LABEL_UPDATED_NAME)
from data.pull_request_data import get_dynamic_label_name  # NUEVO
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

PR_NUMBER = 1 


@pytest.fixture
def pr_state(pr_api):
    response = pr_api.get_pull_request(PR_NUMBER)
    original = response.json()
    original_title = original.get("title")
    original_body = original.get("body")
    original_state = original.get("state")

    yield {
        "title": original_title,
        "body": original_body,
        "state": original_state,
    }

    restore_payload = {}
    if original_title is not None:
        restore_payload["title"] = original_title
    if original_body is not None:
        restore_payload["body"] = original_body
    if original_state == "open":
        restore_payload["state"] = "open"

    if restore_payload:
        pr_api.update_pull_request(PR_NUMBER, restore_payload)


@pytest.fixture
def pr_temp_label(pr_api):
    
    label_name = get_dynamic_label_name()
    pr_api.create_label(label_name, color="0075ca")

    yield label_name
    
    current_labels_resp = pr_api.get_labels(PR_NUMBER)
    if current_labels_resp.status_code == 200:
        labels = [
            lbl["name"]
            for lbl in current_labels_resp.json()
            if lbl["name"] != label_name
        ]
        pr_api.set_labels(PR_NUMBER, labels)

    pr_api.delete_label(label_name)