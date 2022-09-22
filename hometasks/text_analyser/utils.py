import logging
import os

from consts import LOGS_FILE


def get_execution_logger(name: str, log_level=logging.INFO):
    logger = get_logger(name, log_level)
    logger.setLevel(log_level)

    if not os.path.exists(directory := os.path.dirname(LOGS_FILE)):
        os.mkdir(directory)

    file_handler = logging.FileHandler(LOGS_FILE)
    file_handler.setLevel(logging.DEBUG)
    file_handler.setFormatter(logging.Formatter('%(asctime)s|%(type_of_resource)s|%(name_of_resource)s|%(message)s'))
    logger.addHandler(file_handler)

    return logger


def get_logger(name: str, log_level=logging.INFO):
    logger = logging.getLogger(name)
    logger.setLevel(log_level)
    return logger
