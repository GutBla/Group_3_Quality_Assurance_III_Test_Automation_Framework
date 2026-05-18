import pytest

from services.github_issues_api import GitHubIssuesAPI
from services.github_repositories_api import GitHubRepositoriesAPI  # ← agregar


@pytest.fixture
def github_api():
    return GitHubIssuesAPI()


@pytest.fixture
def repo_api():                          # ← agregar
    return GitHubRepositoriesAPI()