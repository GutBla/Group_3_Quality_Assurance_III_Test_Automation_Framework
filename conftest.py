import pytest
from services.github_issues_api import GitHubIssuesAPI
from services.github_labels_api import GitHubLabelsAPI
from data.issue_data import CREATE_ISSUE_PAYLOAD
from data.label_data import CREATE_LABEL_PAYLOAD, LABEL_NAME, LABEL_UPDATED_NAME


@pytest.fixture
def github_api():
    return GitHubIssuesAPI()


@pytest.fixture
def labels_api():
    return GitHubLabelsAPI()


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
