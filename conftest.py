import pytest
from services.github_issues_api import GitHubIssuesAPI
from services.github_user_api import GitHubUserAPI
from data.issue_data import CREATE_ISSUE_PAYLOAD
from services.github_repositories_api import GitHubRepositoriesAPI
from data.repository_data import CREATE_REPO_PAYLOAD

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
def issue(github_api):
    response = github_api.create_issue(CREATE_ISSUE_PAYLOAD)
    issue_number = response.json()["number"]
    yield issue_number
    github_api.close_issue(issue_number)