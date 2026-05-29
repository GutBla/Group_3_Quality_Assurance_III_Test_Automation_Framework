import os
from services.request_manager import RequestManager

class GitHubUserAPI:
    def __init__(self):
        self.base_url = os.getenv("BASE_URL")
        self.client = RequestManager()
        
        if not self.base_url:
            raise EnvironmentError("Falta la variable de entorno: BASE_URL")

    def update_profile(self, payload):
        return self.client.patch(f"{self.base_url}/user", json=payload)

    def get_authenticated_user(self):
        return self.client.get(f"{self.base_url}/user")

    def get_user(self, username):
        return self.client.get(f"{self.base_url}/users/{username}")

    def follow_user(self, username: str):
        return self.client.put(f"{self.base_url}/user/following/{username}")

    def unfollow_user(self, username: str):
        return self.client.delete(f"{self.base_url}/user/following/{username}")

    def check_following(self, username: str):
        return self.client.head(f"{self.base_url}/user/following/{username}")

    def add_emails(self, emails: list):
        return self.client.post(f"{self.base_url}/user/emails", json={"emails": emails})