import os
from services.request_manager import RequestManager


class GitHubPullRequestsAPI:

    def __init__(self):
        self.base_url = os.getenv("BASE_URL")
        self.owner = os.getenv("GITHUB_USERNAME")
        self.repo = os.getenv("GITHUB_REPO")
        self.client = RequestManager()

        if not all([self.base_url, self.owner, self.repo]):
            raise EnvironmentError(
                "Faltan variables de entorno: BASE_URL, GITHUB_USERNAME, GITHUB_REPO"
            )

    @property
    def _pulls_base(self):
        return f"{self.base_url}/repos/{self.owner}/{self.repo}/pulls"

    @property
    def _issues_base(self):
        return f"{self.base_url}/repos/{self.owner}/{self.repo}/issues"

    def get_pull_request(self, pr_number):
        return self.client.get(f"{self._pulls_base}/{pr_number}")

    def list_pull_requests(self, state="open"):
        return self.client.get(self._pulls_base, params={"state": state})

    def update_pull_request(self, pr_number, payload):
        return self.client.patch(f"{self._pulls_base}/{pr_number}", json=payload)

    def close_pull_request(self, pr_number):
        return self.update_pull_request(pr_number, {"state": "closed"})

    def reopen_pull_request(self, pr_number):
        return self.update_pull_request(pr_number, {"state": "open"})

    def add_labels(self, pr_number, labels):
        return self.client.post(
            f"{self._issues_base}/{pr_number}/labels",
            json={"labels": labels},
        )

    def get_labels(self, pr_number):
        return self.client.get(f"{self._issues_base}/{pr_number}/labels")

    def set_labels(self, pr_number, labels):
        return self.client.put(
            f"{self._issues_base}/{pr_number}/labels",
            json={"labels": labels},
        )

    def create_label(self, name, color="ededed", description=""):
        return self.client.post(
            f"{self.base_url}/repos/{self.owner}/{self.repo}/labels",
            json={"name": name, "color": color, "description": description},
        )

    def delete_label(self, name):
        return self.client.delete(
            f"{self.base_url}/repos/{self.owner}/{self.repo}/labels/{name}"
        )