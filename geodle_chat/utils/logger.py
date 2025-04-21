import logging
from logging.handlers import RotatingFileHandler
import os

os.makedirs("logs", exist_ok=True)

def setup_logger(name: str, log_file: str = "logs/geodle.log", level=logging.INFO):
    formatter = logging.Formatter(
        "[%(asctime)s] [%(levelname)s] %(name)s - %(message)s"
    )

    # Log to file (with rotation, max 3 files of 1MB each)
    file_handler = RotatingFileHandler(log_file, maxBytes=1_000_000, backupCount=3)
    file_handler.setFormatter(formatter)

    # Log to console
    console_handler = logging.StreamHandler()
    console_handler.setFormatter(formatter)

    # Create logger
    logger = logging.getLogger(name)
    logger.setLevel(level)

    # Prevent duplicate handlers
    if not logger.handlers:
        logger.addHandler(file_handler)
        logger.addHandler(console_handler)

    return logger
