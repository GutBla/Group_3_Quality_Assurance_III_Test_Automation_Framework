import requests
from config.config import BASE_URL, TOKEN

class GitHubUserAPI:
    def __init__(self):
        self.base_url = BASE_URL
        self.session = requests.Session()
        self.session.headers.update({
            "Authorization": f"Bearer {TOKEN}",
            "Accept": "application/vnd.github+json",
            "Content-Type": "application/json",
            "X-GitHub-Api-Version": "2022-11-28"
        })

    def update_profile(self, payload):
        return self.session.patch(f"{self.base_url}/user", json=payload)

    def get_authenticated_user(self):
        return self.session.get(f"{self.base_url}/user")