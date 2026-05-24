from config.config import BASE_URL, USERNAME, REPO
from services.request_manager import RequestManager


class GitHubIssuesAPI:

    def __init__(self):
        self.base_url = f"{BASE_URL}/repos/{USERNAME}/{REPO}"
        self.client = RequestManager()

    def create_issue(self, payload):
        return self.client.post(f"{self.base_url}/issues", json=payload)

    def get_issue(self, issue_number):
        return self.client.get(f"{self.base_url}/issues/{issue_number}")

    def close_issue(self, issue_number):
        return self.client.patch(f"{self.base_url}/issues/{issue_number}", json={"state": "closed"})
