import requests
from config.config import BASE_URL, USERNAME, REPO, TOKEN


class GitHubLabelsAPI:

    def __init__(self):
        self.base_url = f"{BASE_URL}/repos/{USERNAME}/{REPO}"
        self.session = requests.Session()

        self.session.headers.update({
            "Authorization": f"Bearer {TOKEN}",
            "Accept": "application/vnd.github+json"
        })

    def create_label(self, payload):
        url = f"{self.base_url}/labels"
        return self.session.post(url, json=payload)

    def get_label(self, label_name):
        url = f"{self.base_url}/labels/{label_name}"
        return self.session.get(url)

    def update_label(self, label_name, payload):
        url = f"{self.base_url}/labels/{label_name}"
        return self.session.patch(url, json=payload)

    def delete_label(self, label_name):
        url = f"{self.base_url}/labels/{label_name}"
        return self.session.delete(url)

    def add_labels_to_issue(self, issue_number, labels):
        url = f"{self.base_url}/issues/{issue_number}/labels"
        return self.session.post(url, json={"labels": labels})

    def get_issue(self, issue_number):
        url = f"{self.base_url}/issues/{issue_number}"
        return self.session.get(url)
