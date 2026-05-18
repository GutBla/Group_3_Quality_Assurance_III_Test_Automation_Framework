import requests
from config.config import BASE_URL, USERNAME, REPO, TOKEN


class GitHubIssuesAPI:

    def __init__(self):
        self.base_url = f"{BASE_URL}/repos/{USERNAME}/{REPO}"
        self.session = requests.Session()

        self.session.headers.update({
            "Authorization": f"Bearer {TOKEN}",
            "Accept": "application/vnd.github+json"
        })

    def create_issue(self, payload):
        url = f"{self.base_url}/issues"
        return self.session.post(url, json=payload)

    def get_issue(self, issue_number):
        url = f"{self.base_url}/issues/{issue_number}"
        return self.session.get(url)

    def close_issue(self, issue_number):
        url = f"{self.base_url}/issues/{issue_number}"
        return self.session.patch(url, json={"state": "closed"})