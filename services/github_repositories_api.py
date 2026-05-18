import requests
from config.config import BASE_URL, USERNAME, TOKEN


class GitHubRepositoriesAPI:

    def __init__(self):
        self.base_url = BASE_URL
        self.username = USERNAME
        self.session = requests.Session()

        self.session.headers.update({
            "Authorization": f"Bearer {TOKEN}",
            "Accept": "application/vnd.github+json"
        })

    def create_repo(self, payload):
        url = f"{self.base_url}/user/repos"
        return self.session.post(url, json=payload)

    def get_repo(self, repo_name):
        url = f"{self.base_url}/repos/{self.username}/{repo_name}"
        return self.session.get(url)

    def delete_repo(self, repo_name):
        url = f"{self.base_url}/repos/{self.username}/{repo_name}"
        return self.session.delete(url)