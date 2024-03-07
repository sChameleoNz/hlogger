# HLogger

![PyPI - Version](https://img.shields.io/pypi/v/hlogger)
![GitHub Actions Workflow Status](https://img.shields.io/github/actions/workflow/status/sChameleoNz/hlogger/test.yml)
![Codecov](https://img.shields.io/codecov/c/github/sChameleoNz/hlogger)

HLogger is a utility module that provides a flexible logging solution for Python applications.
It allows you to easily create and manage loggers with both file and stream handlers.

## Installation

You can install HLogger using pip:

> $ pip install hlogger

## Usage

### Create Logger

```python
from hlogger import create_logger

# Create a logger
logger = create_logger("app_logger", "app_log.log")

# Log messages
logger.info("Application started")
```

### Create Logger with Specified Level

```python
import logging
from hlogger import create_logger

# Create a logger
logger = create_logger("app_logger", "app_log.log", level=logging.WARNING)

# Log messages
logger.warning("WARNING: No module named 'missing_module'")
```

### Get Logger

```python
from hlogger import create_logger, get_logger

# Create a logger
logger = create_logger("app_logger", "app_log.log")

# Create another logger
logger = create_logger("app_logger2", "app_log2.log")

# Set logger to the previous one and log messages to it
logger = get_logger("app_logger")
logger.error("Application error")
```

### Change Log File

```python
from hlogger import create_logger

# Create a logger
logger = create_logger("app_logger", "app_log.log")

# Log messages
logger.info("Application started")

# Change the log file dynamically
logger = create_logger("app_logger", "new_app_log.log")

# Log messages to the new log file
logger.warning("Application warning")
```

### Change Formatter

```python
import logging
from hlogger import create_logger, set_formatter

# Create a logger
logger = create_logger("app_logger", "app_log.log")

# Change formatter
set_formatter("app_logger", logging.Formatter("%(message)s"))

# Log messages
logger.info("Application started")
```
