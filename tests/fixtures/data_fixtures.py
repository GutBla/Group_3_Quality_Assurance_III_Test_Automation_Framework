import pytest
from data.issue_data import CREATE_ISSUE_PAYLOAD
from data.label_data import CREATE_LABEL_PAYLOAD, LABEL_NAME, LABEL_UPDATED_NAME
from data.pull_request_data import get_dynamic_label_name
from data.repository_data import CREATE_REPO_PAYLOAD


@pytest.fixture(scope="session")
def worker_suffix(worker_id):
    return f"_{worker_id}" if worker_id else "_master"


@pytest.fixture
def issue(github_api, worker_suffix):
    payload = CREATE_ISSUE_PAYLOAD.copy()
    payload["title"] = f"{payload.get('title', 'Issue')}{worker_suffix}"
    response = github_api.create_issue(payload)
    issue_number = response.json()["number"]
    yield issue_number
    github_api.close_issue(issue_number)


@pytest.fixture
def closed_issue(github_api, worker_suffix):
    payload = CREATE_ISSUE_PAYLOAD.copy()
    payload["title"] = f"{payload.get('title', 'Issue')}{worker_suffix}"
    response = github_api.create_issue(payload)
    issue_number = response.json()["number"]
    github_api.close_issue(issue_number)
    yield issue_number
    github_api.close_issue(issue_number)


@pytest.fixture
def label(labels_api, worker_suffix):
    unique_name = f"{LABEL_NAME}{worker_suffix}"
    unique_updated = f"{LABEL_UPDATED_NAME}{worker_suffix}"
    labels_api.delete_label(unique_name)
    labels_api.delete_label(unique_updated)
    payload = CREATE_LABEL_PAYLOAD.copy()
    payload["name"] = unique_name
    response = labels_api.create_label(payload)
    label_name = response.json()["name"]
    yield label_name
    labels_api.delete_label(unique_name)
    labels_api.delete_label(unique_updated)


@pytest.fixture
def repository(repo_api, worker_suffix):
    unique_repo = f"{CREATE_REPO_PAYLOAD['name']}{worker_suffix}"
    repo_api.delete_repo(unique_repo)
    yield unique_repo
    repo_api.delete_repo(unique_repo)


@pytest.fixture
def profile_restore(github_user_api):
    original = github_user_api.get_authenticated_user().json()
    original_bio = original.get("bio")
    original_location = original.get("location")
    original_company = original.get("company")
    original_hireable = original.get("hireable")
    yield
    restore_payload = {
        "bio": original_bio or "",
        "location": original_location or "",
        "company": original_company or "",
        "hireable": original_hireable if original_hireable is not None else False
    }
    github_user_api.update_profile(restore_payload)


@pytest.fixture
def pr_state(pr_api):
    response = pr_api.get_pull_request(1)
    original = response.json()
    yield {
        "title": original.get("title"),
        "body": original.get("body"),
        "state": original.get("state"),
    }
    restore_payload = {}
    if original.get("title"):
        restore_payload["title"] = original["title"]
    if original.get("body"):
        restore_payload["body"] = original["body"]
    if original.get("state") == "open":
        restore_payload["state"] = "open"
    if restore_payload:
        pr_api.update_pull_request(1, restore_payload)


@pytest.fixture
def pr_temp_label(pr_api, worker_suffix):
    label_name = f"{get_dynamic_label_name()}{worker_suffix}"
    pr_api.create_label(label_name, color="0075ca")
    yield label_name
    current_labels_resp = pr_api.get_labels(1)
    if current_labels_resp.status_code == 200:
        labels = [
            lbl["name"] for lbl in current_labels_resp.json()
            if lbl["name"] != label_name
        ]
        pr_api.set_labels(1, labels)
    pr_api.delete_label(label_name)
