from config.config import BASE_URL, USERNAME, REPO
from services.request_manager import RequestManager


class GitHubLabelsAPI:

    def __init__(self):
        self.base_url = f"{BASE_URL}/repos/{USERNAME}/{REPO}"
        self.client = RequestManager()

    def create_label(self, payload):
        return self.client.post(f"{self.base_url}/labels", json=payload)

    def get_label(self, label_name):
        return self.client.get(f"{self.base_url}/labels/{label_name}")

    def update_label(self, label_name, payload):
        return self.client.patch(f"{self.base_url}/labels/{label_name}", json=payload)

    def delete_label(self, label_name):
        return self.client.delete(f"{self.base_url}/labels/{label_name}")

    def add_labels_to_issue(self, issue_number, labels):
        return self.client.post(f"{self.base_url}/issues/{issue_number}/labels", json={"labels": labels})

    def get_issue(self, issue_number):
        return self.client.get(f"{self.base_url}/issues/{issue_number}")
