from dotenv import load_dotenv

load_dotenv()

pytest_plugins = [
    "tests.fixtures.logging_fixtures",
    "tests.fixtures.api_fixtures",
    "tests.fixtures.data_fixtures",
]
