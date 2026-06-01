import os
import threading

import requests
from dotenv import load_dotenv

from utils.logger import logger

load_dotenv(override=True)


class RequestManager:
    _instance = None
    _lock = threading.Lock()

    def __new__(cls):
        with cls._lock:
            if cls._instance is None:
                cls._instance = super().__new__(cls)
                cls._instance._initialize()
        return cls._instance

    def _initialize(self):
        token = os.getenv("ACCESS_TOKEN")
        if not token:
            raise EnvironmentError("ACCESS_TOKEN no está configurado.")
        token = token.strip()
        self.session = requests.Session()
        self.session.headers.update({
            "Authorization": f"Bearer {token}",
            "Accept": "application/vnd.github+json",
            "X-GitHub-Api-Version": "2022-11-28",
        })

    def _log_request(self, method, url, **kwargs):
        logger.info(f"HTTP REQUEST: {method} {url}")
        if "json" in kwargs:
            logger.info(f"REQUEST BODY: {kwargs['json']}")
        if "headers" in kwargs:
            logger.info(f"OVERRIDE HEADERS: {kwargs['headers']}")

    def _log_response(self, response):
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
        self._log_request("PUT", url, **kwargs)
        response = self.session.put(url, **kwargs)
        self._log_response(response)
        return response

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
        self._log_request("HEAD", url, **kwargs)
        response = self.session.head(url, **kwargs)
        self._log_response(response)
        return response
