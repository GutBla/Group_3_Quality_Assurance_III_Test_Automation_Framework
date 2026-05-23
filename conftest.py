import pytest
from services.github_issues_api import GitHubIssuesAPI
from services.github_labels_api import GitHubLabelsAPI
from services.github_user_api import GitHubUserAPI
from services.github_repositories_api import GitHubRepositoriesAPI
from data.issue_data import CREATE_ISSUE_PAYLOAD
from data.label_data import CREATE_LABEL_PAYLOAD, LABEL_NAME, LABEL_UPDATED_NAME
from data.repository_data import CREATE_REPO_PAYLOAD


# --- Session-level hooks (before all / after all) ---

def pytest_sessionstart(session):
    print("\n[SETUP] Starting test session")


def pytest_sessionend(session, exitstatus):
    print(f"\n[TEARDOWN] Test session ended with status: {exitstatus}")


# --- API client fixtures ---

@pytest.fixture
def github_api():
    return GitHubIssuesAPI()


@pytest.fixture
def github_user_api():
    return GitHubUserAPI()


@pytest.fixture
def repo_api():
    return GitHubRepositoriesAPI()


@pytest.fixture
def labels_api():
    return GitHubLabelsAPI()


# --- Precondition / postcondition fixtures ---

@pytest.fixture
def issue(github_api):
    response = github_api.create_issue(CREATE_ISSUE_PAYLOAD)
    issue_number = response.json()["number"]
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
