"""Centralized logging configuration using loguru."""

import sys
from pathlib import Path
from loguru import logger

# Create logs directory if it doesn't exist
log_dir = Path(__file__).parent.parent.parent / "data" / "logs"
log_dir.mkdir(parents=True, exist_ok=True)

# Remove default handler
logger.remove()

# Add console handler with color
logger.add(
    sys.stderr,
    format="<green>{time:YYYY-MM-DD HH:mm:ss}</green> | <level>{level: <8}</level> | <cyan>{name}</cyan>:<cyan>{function}</cyan>:<cyan>{line}</cyan> - <level>{message}</level>",
    level="INFO",
    colorize=True
)

# Add file handler for all logs
logger.add(
    log_dir / "app_{time:YYYY-MM-DD}.log",
    rotation="1 day",
    retention="7 days",
    level="DEBUG",
    format="{time:YYYY-MM-DD HH:mm:ss} | {level: <8} | {name}:{function}:{line} - {message}"
)

# Add file handler for errors only
logger.add(
    log_dir / "errors_{time:YYYY-MM-DD}.log",
    rotation="1 day",
    retention="30 days",
    level="ERROR",
    format="{time:YYYY-MM-DD HH:mm:ss} | {level: <8} | {name}:{function}:{line} - {message}\n{exception}"
)

def get_logger(name: str):
    """Get a logger instance with the given name."""
    return logger.bind(name=name)

# Export logger
__all__ = ["logger", "get_logger"]
