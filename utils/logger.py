import logging
import sys
import os
from datetime import datetime

_LOG_DIR = "logs"
os.makedirs(_LOG_DIR, exist_ok=True)

_log_file = os.path.join(
    _LOG_DIR,
    f"test_run_{datetime.now().strftime('%Y%m%d_%H%M%S')}.log",
)

logger = logging.getLogger("qa_framework")
logger.setLevel(logging.INFO)

formatter = logging.Formatter(
    fmt="%(asctime)s [%(levelname)s] %(name)s - %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
)

if not logger.handlers:
    file_handler = logging.FileHandler(_log_file, encoding="utf-8")
    file_handler.setFormatter(formatter)
    logger.addHandler(file_handler)

    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setFormatter(formatter)
    logger.addHandler(console_handler)
