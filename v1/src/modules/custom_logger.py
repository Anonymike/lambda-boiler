import os
import sys
import json
import logging

from pythonjsonlogger import jsonlogger

STAGE = os.environ.get('STAGE', '')
SERVICE = os.environ.get('SERVICE', '')
LOG_LEVEL = os.environ.get('LOG_LEVEL', 'INFO').upper()


class LambdaLoggerFilter(logging.Filter):
    def filter(self, record):
        record.stage = STAGE
        record.service = SERVICE
        return True


def _create_logger():
    logger = logging.getLogger()

    # If aws, get created handler
    existing_handler = False
    if logger.handlers:
        logHandler = logger.handlers[0]
        existing_handler = True
    # Create handler if needed
    if not existing_handler:
        logHandler = logging.StreamHandler(sys.stdout)

    # Create formatter and filter
    formatter = jsonlogger.JsonFormatter(('%(asctime)s %(levelname)s %(message)s %(lineno)s'
                                        ' %(module)s %(funcName)s %(aws_request_id)s %(stage)s'
                                        ' %(service)s'),
                                        datefmt="%Y-%m-%dT%H:%M:%S%z")
    logHandler.setFormatter(formatter)
    logHandler.addFilter(LambdaLoggerFilter())

    # Save handler if new
    if not existing_handler:
        logger.addHandler(logHandler)

    # Set log level
    logger.setLevel(LOG_LEVEL)

    return logger


logger = _create_logger()