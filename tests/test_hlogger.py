import os
import time
import logging

import pytest

from src.hlogger.hlogger import HLogger


TEST_LOG_FILE = "test_log.log"
NEW_TEST_LOG_FILE = "new_test_log.log"


@pytest.fixture
def cleanup():
    yield
    logging.shutdown()
    if os.path.exists(TEST_LOG_FILE):
        os.remove(TEST_LOG_FILE)
    if os.path.exists(NEW_TEST_LOG_FILE):
        os.remove(NEW_TEST_LOG_FILE)


def test_get_logger(cleanup):
    logger_name = "test_logger"
    logger = HLogger.get_logger(logger_name, TEST_LOG_FILE)

    assert isinstance(logger, logging.Logger)
    assert logger.name == logger_name


def test_set_level(cleanup):
    logger_name = "test_logger"
    logger = HLogger.get_logger(logger_name, TEST_LOG_FILE)

    # Custom level
    custom_level = logging.INFO

    # Set the log level to INFO
    HLogger.set_level(logger_name, custom_level)

    assert logger.level == custom_level
    for handler in logger.handlers:
        assert handler.level == custom_level


def test_set_formatter(cleanup):
    logger_name = "test_logger"
    logger = HLogger.get_logger(logger_name, TEST_LOG_FILE)

    # Custom formatter
    custom_formatter = logging.Formatter("%(message)s")

    # Set custom formatter
    HLogger.set_formatter(logger_name, custom_formatter)

    # Verify that all handlers have the custom formatter
    assert all(handler.formatter == custom_formatter for handler in logger.handlers)


def test_change_log_file(cleanup):
    logger_name = "test_logger"
    logger = HLogger.get_logger(logger_name, TEST_LOG_FILE)

    # Nothing to change just keep previous one
    HLogger.change_log_file(logger_name, TEST_LOG_FILE)

    # Simulate changing the log file
    HLogger.change_log_file(logger_name, NEW_TEST_LOG_FILE)

    # Verify that the new file handler was added to the logger
    assert any(
        isinstance(handler, logging.FileHandler)
        and handler.baseFilename.split(os.path.sep)[-1] == NEW_TEST_LOG_FILE
        for handler in logger.handlers
    )
    assert not any(
        isinstance(handler, logging.FileHandler)
        and handler.baseFilename.split(os.path.sep)[-1] == TEST_LOG_FILE
        for handler in logger.handlers
    )


def test_logging_to_file(cleanup):
    logger_name = "test_logger"

    # Set up logger
    logger = HLogger.get_logger(logger_name, TEST_LOG_FILE)

    # Log messages at different levels
    levels_to_test = [
        logging.DEBUG,
        logging.INFO,
        logging.WARNING,
        logging.ERROR,
        logging.CRITICAL,
    ]
    for level in levels_to_test:
        logger.log(level, f"Test log message at {logging.getLevelName(level)} level")

    # Wait for a moment to ensure the log is written to the file
    time.sleep(1)

    # Verify that the log file contains the logged message
    with open(TEST_LOG_FILE, "r") as file:
        log_content = file.read()
        for level in levels_to_test:
            assert (
                f"Test log message at {logging.getLevelName(level)} level"
                in log_content
            )
