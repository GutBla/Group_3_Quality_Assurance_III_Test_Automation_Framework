import datetime
from utils.logger import logger


# --- Session-level hooks (before all / after all) ---


def pytest_sessionstart(session):
    print("\n[SETUP] Starting test session")


def pytest_sessionfinish(session, exitstatus):
    print(f"\n[TEARDOWN] Test session ended with status: {exitstatus}")


def pytest_configure(config):
    config._metadata = {
        "Project": "Group 3 — QA III Test Automation Framework",
        "Team": "Group 3",
        "API": "GitHub REST API",
        "Base URL": "https://api.github.com",
        "Date": datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "Total Tests": "40",
    }


def pytest_html_report_title(report):
    report.title = "Group 3 — QA III Automation Report"


# --- Per-test logging hooks ---


def pytest_runtest_setup(item):
    logger.info(f"START  {item.nodeid}")


def pytest_runtest_logreport(report):
    if report.when != "call":
        return
    if report.passed:
        logger.info(f"PASSED {report.nodeid}")
    elif report.failed:
        logger.error(f"FAILED {report.nodeid}\n{report.longreprtext}")
    elif report.skipped:
        logger.warning(f"SKIPPED {report.nodeid}")
