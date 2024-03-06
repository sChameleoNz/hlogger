# HLogger

HLogger is a utility module that provides a flexible logging solution for Python applications.
It allows you to easily create and manage loggers with both file and stream handlers.

## Installation

You can install HLogger using pip:

> $ pip install hlogger

## Usage

### Basic Logger Setup

```python
from hlogger import create_logger

# Create a logger
logger = create_logger("app_logger", "app_log.log")

# Log messages
logger.info("Application started")
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

# Log messages with the new log file
logger.warning("Application warning")
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
