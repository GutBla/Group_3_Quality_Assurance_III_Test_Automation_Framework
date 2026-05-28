from config.config import BASE_URL, USERNAME, REPO
from services.request_manager import RequestManager

ENDPOINT = "issues"


class GitHubIssuesAPI:

    def __init__(self):
        self.default_base_url = f"{BASE_URL}/repos/{USERNAME}/{REPO}"
        self.client = RequestManager()

    def create_issue(self, payload, repo=None, headers=None):
        if repo:
            url = f"{BASE_URL}/repos/{USERNAME}/{repo}/{ENDPOINT}"
        else:
            url = f"{self.default_base_url}/{ENDPOINT}"

        return self.client.post(url, json=payload, headers=headers)

    def get_issue(self, issue_number):
        return self.client.get(f"{self.default_base_url}/{ENDPOINT}/{issue_number}")

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
