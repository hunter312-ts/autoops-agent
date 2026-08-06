import logging
import os
from app.core.config import settings
# Create logs directory if it doesn't exist
os.makedirs("logs", exist_ok=True)
def setup_logger(name: str = "AutoOps") -> logging.Logger:
    """
    Configure and return a logger.
    """
    logger = logging.getLogger(name)
    # Prevent duplicate handlers
    if logger.handlers:
        return logger

    logger.setLevel(logging.DEBUG if settings.DEBUG else logging.INFO)


    formatter = logging.Formatter(
    fmt="%(asctime)s | %(levelname)s | %(name)s | %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S"
)

    # Console Handler
    console_handler = logging.StreamHandler()
    console_handler.setFormatter(formatter)

    # File Handler
    file_handler = logging.FileHandler("logs/autoops.log",encoding="utf-8")
    file_handler.setFormatter(formatter)

    logger.addHandler(console_handler)
    logger.addHandler(file_handler)

    return logger
logger = setup_logger()