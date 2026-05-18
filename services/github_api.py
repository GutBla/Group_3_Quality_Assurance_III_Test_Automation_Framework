import requests

from config.config import BASE_URL


def get_user(username):

    response = requests.get(
        f"{BASE_URL}/users/{username}"
    )

    return response