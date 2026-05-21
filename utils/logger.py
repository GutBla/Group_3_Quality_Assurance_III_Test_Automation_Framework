import logging
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

if not logger.handlers:
    _handler = logging.FileHandler(_log_file, encoding="utf-8")
    _handler.setFormatter(logging.Formatter(
        fmt="%(asctime)s [%(levelname)s] %(name)s - %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S",
    ))
    logger.addHandler(_handler)
