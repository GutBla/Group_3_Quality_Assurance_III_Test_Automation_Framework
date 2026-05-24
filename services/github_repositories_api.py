from config.config import BASE_URL, USERNAME
from services.request_manager import RequestManager


class GitHubRepositoriesAPI:

    def __init__(self):
        self.base_url = BASE_URL
        self.username = USERNAME
        self.client = RequestManager()

    def create_repo(self, payload):
        return self.client.post(f"{self.base_url}/user/repos", json=payload)

    def get_repo(self, repo_name):
        return self.client.get(f"{self.base_url}/repos/{self.username}/{repo_name}")

    def delete_repo(self, repo_name):
        return self.client.delete(f"{self.base_url}/repos/{self.username}/{repo_name}")
