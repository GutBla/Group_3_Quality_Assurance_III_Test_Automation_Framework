import threading
import requests
from config.config import TOKEN
from utils.logger import logger

class RequestManager:
    _instance = None
    _lock = threading.Lock()

    def __new__(cls):
        if cls._instance is None:
            with cls._lock:
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

    def _log_request(self, method, url, **kwargs):
        """Método privado para registrar los detalles de la petición en el log."""
        logger.info(f"HTTP REQUEST: {method} {url}")
        if "json" in kwargs:
            logger.info(f"REQUEST BODY: {kwargs['json']}")

    def _log_response(self, response):
        """Método privado para registrar los detalles de la respuesta en el log."""
        logger.info(f"HTTP RESPONSE STATUS: {response.status_code}")
        try:
            logger.info(f"RESPONSE BODY: {response.json()}")
        except ValueError:
            logger.info("RESPONSE BODY: [No JSON body or empty]")

    def get(self, url, **kwargs):
        self._log_request("GET", url, **kwargs)
        response = self.session.get(url, **kwargs)
        self._log_response(response)
        return response

    def post(self, url, **kwargs):
        self._log_request("POST", url, **kwargs)
        response = self.session.post(url, **kwargs)
        self._log_response(response)
        return response

    def put(self, url, **kwargs):
        return self.session.put(url, **kwargs)

    def patch(self, url, **kwargs):
        self._log_request("PATCH", url, **kwargs)
        response = self.session.patch(url, **kwargs)
        self._log_response(response)
        return response

    def delete(self, url, **kwargs):
        self._log_request("DELETE", url, **kwargs)
        response = self.session.delete(url, **kwargs)
        self._log_response(response)
        return response

    def head(self, url, **kwargs):
        return self.session.head(url, **kwargs)