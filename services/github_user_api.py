from config.config import BASE_URL
from services.request_manager import RequestManager


class GitHubUserAPI:

    def __init__(self):
        self.base_url = BASE_URL
        self.client = RequestManager()

    def update_profile(self, payload):
        return self.client.patch(f"{self.base_url}/user", json=payload)

    def get_authenticated_user(self):
        return self.client.get(f"{self.base_url}/user")

    def get_user(self, username):
        return self.client.get(f"{self.base_url}/users/{username}")
