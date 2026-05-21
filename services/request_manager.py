import requests
from config.config import TOKEN


class RequestManager:
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance._initialize()
        return cls._instance

    def _initialize(self):
        self.session = requests.Session()
        self.session.headers.update({
            "Authorization": f"Bearer {TOKEN}",
            "Accept": "application/vnd.github+json",
            "X-GitHub-Api-Version": "2022-11-28",
        })

    def get(self, url, **kwargs):
        return self.session.get(url, **kwargs)

    def post(self, url, **kwargs):
        return self.session.post(url, **kwargs)

    def patch(self, url, **kwargs):
        return self.session.patch(url, **kwargs)

    def delete(self, url, **kwargs):
        return self.session.delete(url, **kwargs)
