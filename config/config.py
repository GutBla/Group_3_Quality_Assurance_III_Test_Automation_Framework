import os

from dotenv import load_dotenv

load_dotenv()

BASE_URL = os.getenv("BASE_URL")
USERNAME = os.getenv("GITHUB_USERNAME")
REPO = os.getenv("GITHUB_REPO")
TOKEN = os.getenv("GITHUB_TOKEN")