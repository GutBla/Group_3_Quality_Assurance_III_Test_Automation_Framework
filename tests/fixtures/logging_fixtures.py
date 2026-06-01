from utils.logger import logger

# --- Session-level hooks (before all / after all) ---

def pytest_sessionstart(session):
    print("\n[SETUP] Starting test session")


def pytest_sessionfinish(session, exitstatus):
    print(f"\n[TEARDOWN] Test session ended with status: {exitstatus}")


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
