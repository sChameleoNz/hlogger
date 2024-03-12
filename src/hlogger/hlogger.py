"""Utility module for logging."""

import logging
from logging.handlers import RotatingFileHandler
from threading import Lock


class HLogger:
    """Utility class for logging to both file and stream."""

    _lock = Lock()

    @classmethod
    def get_logger(
        cls,
        name: str,
        file_name: str,
        max_file_size: int = 10485760,
        backup_count: int = 10,
        level: int = logging.DEBUG,
    ) -> logging.Logger:
        """Get or create a logger with file and stream handlers.

        Args:
            name (str): Name of the logger
            file_name (str): Name of the logging file
            max_file_size (int): Maximum size of the logging file
            backup_count (int): Number of backup files
            level (int): Log level for the logger and handlers

        Returns:
            Configured logger
        """
        with cls._lock:
            logger = logging.getLogger(name)
            logger.setLevel(level)

            # File Handler
            cls._add_file_handler(logger, file_name, max_file_size, backup_count, level)

            # Stream Handler
            cls._add_stream_handler(logger, level)

            return logger

    @classmethod
    def set_level(cls, name: str, level: int) -> None:
        """Set the log level of the logger and its handlers.

        Args:
            name (str): Name of the logger
            level (int): Log level to set
        """
        with cls._lock:
            logger = logging.getLogger(name)
            for handler in logger.handlers:
                handler.setLevel(level)
            logger.setLevel(level)

    @classmethod
    def set_formatter(cls, name: str, formatter: logging.Formatter) -> None:
        """Set the formatter for all handlers of the logger.

        Args:
            name (str): Name of the logger
            formatter (logging.Formatter): Formatter to use
        """
        with cls._lock:
            logger = logging.getLogger(name)
            for handler in logger.handlers:
                handler.setFormatter(formatter)

    @classmethod
    def change_log_file(
        cls,
        name: str,
        file_name: str,
        max_file_size: int = 10485760,
        backup_count: int = 10,
        level: int = logging.DEBUG,
    ) -> None:
        """Change the log file for the logger.

        Args:
            name (str): Name of the logger
            file_name (str): New name of the logging file
            max_file_size (int): Maximum size of the new logging file
            backup_count (int): Number of backup files for the new file
            level (int): Log level for the logger and handlers
        """
        with cls._lock:
            logger = logging.getLogger(name)
            for handler in logger.handlers:
                if isinstance(handler, RotatingFileHandler):
                    if handler.baseFilename.split("/")[-1] == file_name:
                        return

                    # New File Handler
                    new_file_handler = RotatingFileHandler(
                        filename=file_name,
                        maxBytes=max_file_size,
                        backupCount=backup_count,
                    )
                    new_file_handler.setFormatter(
                        logging.Formatter(
                            "[%(asctime)s %(name)10s - %(levelname)8s] %(message)s"
                        )
                    )
                    new_file_handler.setLevel(level)

                    logger.removeHandler(handler)
                    logger.addHandler(new_file_handler)

    @classmethod
    def _add_file_handler(
        cls,
        logger: logging.Logger,
        file_name: str,
        max_file_size: int = 10485760,
        backup_count: int = 10,
        level: int = logging.DEBUG,
    ) -> None:
        """Add or update a rotating file handler to the logger.

        Args:
            logger (logging.Logger): Logger to which the handler will be added or updated
            file_name (str): Name of the logging file
            max_file_size (int): Maximum size of the logging file
            backup_count (int): Number of backup files
            level (int): Log level for the handler
        """
        for handler in logger.handlers:
            if isinstance(handler, RotatingFileHandler):
                if handler.baseFilename.split("/")[-1] != file_name:
                    logger.removeHandler(handler)
                    break
                return
        file_handler = RotatingFileHandler(
            filename=file_name, maxBytes=max_file_size, backupCount=backup_count
        )
        file_handler.setFormatter(
            logging.Formatter("[%(asctime)s %(name)10s - %(levelname)8s] %(message)s")
        )
        file_handler.setLevel(level)
        logger.addHandler(file_handler)

    @classmethod
    def _add_stream_handler(
        cls,
        logger: logging.Logger,
        level: int = logging.DEBUG,
    ) -> None:
        """Add a stream handler to the logger if not already present.

        Args:
            logger (logging.Logger): Logger to which the handler will be added
            level (int): Log level for the handler
        """
        if not any(
            type(handler) == logging.StreamHandler for handler in logger.handlers
        ):
            stream_handler = logging.StreamHandler()
            stream_handler.setFormatter(
                logging.Formatter(
                    "[%(asctime)s %(name)10s - %(levelname)8s] %(message)s"
                )
            )
            stream_handler.setLevel(level)
            logger.addHandler(stream_handler)
