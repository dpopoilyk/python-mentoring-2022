import logging
import os
from datetime import datetime

from consts import LOGS_FILE, DB_FILE
from database import create_sqlite_engine, logs_table
from uuid import uuid4


class SqlLiteHandler(logging.StreamHandler):
    def __init__(self):
        self._db_engine = create_sqlite_engine(DB_FILE)
        super().__init__()

    def format(self, record: logging.LogRecord) -> str:
        insert = logs_table.insert().values(
            {
                "uid": uuid4().hex,
                "timestamp": datetime.fromtimestamp(record.created),
                "type_of_resource": record.type_of_resource,
                "name_of_resource": record.name_of_resource,
                "message": record.getMessage(),
            }
        )
        self._db_engine.execute(insert)
        return super(SqlLiteHandler, self).format(record)


def get_execution_logger(name: str, log_level=logging.INFO):
    logger = get_logger(name, log_level)
    logger.setLevel(log_level)

    if not os.path.exists(directory := os.path.dirname(LOGS_FILE)):
        os.mkdir(directory)

    file_handler = SqlLiteHandler()
    file_handler.setLevel(logging.DEBUG)
    logger.addHandler(file_handler)

    return logger


def get_logger(name: str, log_level=logging.INFO):
    logger = logging.getLogger(name)
    logger.setLevel(log_level)
    return logger
