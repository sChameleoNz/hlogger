"""APIs for user convenience."""

from typing import Optional, List

import logging

from .hlogger import HLogger


# List to store all created logger instances.
loggers: List[logging.Logger] = []


def create_logger(
    name: str,
    file_name: str,
    max_file_size: int = 10485760,
    backup_count: int = 10,
    level: int = logging.DEBUG,
) -> logging.Logger:
    """Create a logger and set it as the global logger if not already present in loggers.

    Args:
        name (str): Name of the logger
        file_name (str): Name of the logging file
        max_file_size (int): Maximum size of the logging file
        backup_count (int): Number of backup files
        level (int): Log level for the logger and handlers
    """
    global loggers

    new_logger = HLogger.get_logger(name, file_name, max_file_size, backup_count, level)
    if new_logger not in loggers:
        loggers.append(new_logger)
    return new_logger


def get_logger(name: str) -> Optional[logging.Logger]:
    """Get the global logger from the one with the specified name from loggers.

    Args:
        name (str): Name of the logger to set as the global logger

    Returns:
        The logger instance with the specified name, or None if not found.
    """
    global loggers

    for l in loggers:
        if l.name == name:
            return l


def set_formatter(name: str, formatter: logging.Formatter) -> None:
    """Set the formatter for all handlers of the logger with the specified name.

    Args:
        name (str): Name of the logger
        formatter (logging.Formatter): Formatter to use
    """
    HLogger.set_formatter(name, formatter)
