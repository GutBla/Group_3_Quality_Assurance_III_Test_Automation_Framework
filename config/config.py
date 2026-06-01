import os

from dotenv import load_dotenv

load_dotenv()

BASE_URL = os.getenv("BASE_URL")
USERNAME = os.getenv("USERNAME")
REPO_NAME = os.getenv("REPO_NAME")
ACCESS_TOKEN = os.getenv("ACCESS_TOKEN")