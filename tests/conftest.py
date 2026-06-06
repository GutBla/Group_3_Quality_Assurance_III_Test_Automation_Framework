import pytest
from dotenv import load_dotenv

load_dotenv()

pytest_plugins = [
    "tests.fixtures.logging_fixtures",
    "tests.fixtures.api_fixtures",
    "tests.fixtures.data_fixtures",
]


def pytest_addoption(parser):
    parser.addoption(
        "--fail-fast",
        action="store_true",
        default=False,
        help="Stop test execution after the first failure.",
    )


@pytest.hookimpl(hookwrapper=True)
def pytest_runtest_makereport(item, call):
    outcome = yield
    report = outcome.get_result()
    if report.when == "call" and report.failed:
        if item.config.getoption("--fail-fast", default=False):
            pytest.exit("Stopping after first failure (--fail-fast enabled)", returncode=1)
