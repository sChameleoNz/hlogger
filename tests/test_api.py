import os
import logging

import pytest

from src.hlogger import create_logger, get_logger


APP_LOG_FILE = "app_log.log"
NEW_APP_LOG_FILE = "new_app_log.log"


@pytest.fixture
def cleanup():
    yield
    logging.shutdown()
    if os.path.exists(APP_LOG_FILE):
        os.remove(APP_LOG_FILE)
    if os.path.exists(NEW_APP_LOG_FILE):
        os.remove(NEW_APP_LOG_FILE)


def test_create_logger(cleanup):
    # Set up
    logger_name = "app_logger"

    # Create logger and log a message
    logger = create_logger(logger_name, APP_LOG_FILE)
    logger.info("Application started")

    # Assertions
    assert isinstance(logger, logging.Logger)
    assert logger.name == logger_name

    # Check log content in the file
    with open(APP_LOG_FILE, "r") as file:
        log_content = file.read()
        assert f"Application started" in log_content


def test_get_logger(cleanup):
    # Set up
    logger_name1 = "app_logger1"
    logger_name2 = "app_logger2"

    # Create loggers with different names
    logger = create_logger(logger_name1, APP_LOG_FILE)
    logger = create_logger(logger_name2, NEW_APP_LOG_FILE)

    # Retrieve a logger and log a message
    logger = get_logger(logger_name1)
    logger.info("Application started")

    # Assertions
    assert isinstance(logger, logging.Logger)
    assert logger.name == logger_name1 and logger.name != logger_name2

    # Check log content in the file
    with open(APP_LOG_FILE, "r") as file:
        log_content = file.read()
        assert f"Application started" in log_content
    with open(NEW_APP_LOG_FILE, "r") as file:
        log_content = file.read()
        assert f"Application started" not in log_content


def test_change_logger(cleanup):
    # Set up
    logger_name = "app_logger1"

    # Create logger with the first log file, then change to a new log file
    logger = create_logger(logger_name, APP_LOG_FILE)
    logger = create_logger(logger_name, NEW_APP_LOG_FILE)

    # Log a message to the new log file
    logger.info("Application started")

    # Assertions
    assert isinstance(logger, logging.Logger)
    assert logger.name == logger_name

    # Check log content in the new file
    with open(NEW_APP_LOG_FILE, "r") as file:
        log_content = file.read()
        assert f"Application started" in log_content
