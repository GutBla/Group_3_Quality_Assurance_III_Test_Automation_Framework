import pytest
from services.github_issues_api import GitHubIssuesAPI
from services.github_labels_api import GitHubLabelsAPI
from services.github_repositories_api import GitHubRepositoriesAPI
from services.github_user_api import GitHubUserAPI


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