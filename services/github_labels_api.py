import os

from services.request_manager import RequestManager


class GitHubLabelsAPI:
    def __init__(self):
        self.base_url_base = os.getenv("BASE_URL")
        self.username = os.getenv("USERNAME")
        self.repo = os.getenv("REPO_NAME")

        if not all([self.base_url_base, self.username, self.repo]):
            raise EnvironmentError("Faltan variables de entorno para etiquetas")

        self.base_url = f"{self.base_url_base}/repos/{self.username}/{self.repo}"
        self.client = RequestManager()

    def create_label(self, payload):
        return self.client.post(f"{self.base_url}/labels", json=payload)

    def get_label(self, label_name):
        return self.client.get(f"{self.base_url}/labels/{label_name}")

    def update_label(self, label_name, payload):
        return self.client.patch(
            f"{self.base_url}/labels/{label_name}", json=payload
        )

    def delete_label(self, label_name):
        return self.client.delete(f"{self.base_url}/labels/{label_name}")

    def list_labels(self):
        return self.client.get(f"{self.base_url}/labels")

    def add_labels_to_issue(self, issue_number, labels):
        return self.client.post(
            f"{self.base_url}/issues/{issue_number}/labels",
            json={"labels": labels}
        )

    def get_issue(self, issue_number):
        return self.client.get(f"{self.base_url}/issues/{issue_number}")
