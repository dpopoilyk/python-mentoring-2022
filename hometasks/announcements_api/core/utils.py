import logging
import os

from uuid import uuid4


def generate_uid() -> str:
    return str(uuid4())


def get_logger(name):
    logger = logging.getLogger(name)
    logger.setLevel(os.environ.get("LOG_LEVEL", "INFO"))
    return logger

