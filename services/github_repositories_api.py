from config.config import BASE_URL, USERNAME
from services.request_manager import RequestManager


class GitHubRepositoriesAPI:
    def __init__(self):
        self.base_url = BASE_URL
        self.username = USERNAME
        self.client = RequestManager()

        if not all([self.base_url, self.username]):
            raise EnvironmentError("Faltan variables de entorno: BASE_URL, USERNAME")

    def create_repo(self, payload):
        return self.client.post(f"{self.base_url}/user/repos", json=payload)

    def get_repo(self, repo_name):
        url = f"{self.base_url}/repos/{self.username}/{repo_name}"
        return self.client.get(url)

    def update_repo(self, repo_name, payload):
        url = f"{self.base_url}/repos/{self.username}/{repo_name}"
        return self.client.patch(url, json=payload)

    def delete_repo(self, repo_name):
        url = f"{self.base_url}/repos/{self.username}/{repo_name}"
        return self.client.delete(url)

    def list_user_repos(self, per_page=100, sort="created", direction="desc"):
        return self.client.get(
            f"{self.base_url}/user/repos",
            params={
                "per_page": per_page,
                "sort": sort,
                "direction": direction
            }
        )

    def get_contributors(self, repo_name):
        url = f"{self.base_url}/repos/{self.username}/{repo_name}/contributors"
        return self.client.get(url)
