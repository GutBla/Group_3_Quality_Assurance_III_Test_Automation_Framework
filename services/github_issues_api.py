import os

from services.request_manager import RequestManager

ENDPOINT = "issues"


class GitHubIssuesAPI:

    def __init__(self):
        self.base_url = os.getenv("BASE_URL")
        self.username = os.getenv("USERNAME")
        self.repo = os.getenv("REPO_NAME")

        if not all([self.base_url, self.username, self.repo]):
            raise EnvironmentError(
                "Faltan variables de entorno: BASE_URL, USERNAME, REPO_NAME")

        self.default_base_url = f"{self.base_url}/repos/{self.username}/{self.repo}"
        self.client = RequestManager()

    def create_issue(self, payload, repo=None, headers=None):
        if repo:
            url = f"{self.base_url}/repos/{self.username}/{repo}/{ENDPOINT}"
        else:
            url = f"{self.default_base_url}/{ENDPOINT}"
        return self.client.post(url, json=payload, headers=headers)

    def get_issue(self, issue_number):
        return self.client.get(
            f"{self.default_base_url}/{ENDPOINT}/{issue_number}")

    def close_issue(self, issue_number):
        return self.client.patch(
            f"{self.default_base_url}/{ENDPOINT}/{issue_number}",
            json={"state": "closed"}
        )

    def update_issue(self, issue_number, payload):
        return self.client.patch(
            f"{self.default_base_url}/{ENDPOINT}/{issue_number}",
            json=payload
        )

    def create_comment(self, issue_number, payload):
        url = f"{self.default_base_url}/{ENDPOINT}/{issue_number}/comments"
        return self.client.post(url, json=payload)
