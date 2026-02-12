"""Structured logging for interview prep system."""
import logging
import sys
from pathlib import Path
from rich.logging import RichHandler
from rich.console import Console

console = Console()


def setup_logger(name: str, level: int = logging.INFO) -> logging.Logger:
    """Set up a logger with rich formatting.

    Args:
        name: Logger name
        level: Logging level

    Returns:
        Configured logger instance
    """
    logger = logging.getLogger(name)
    logger.setLevel(level)

    # Remove existing handlers
    logger.handlers = []

    # Add rich handler for beautiful terminal output
    handler = RichHandler(
        console=console,
        show_time=True,
        show_path=False,
        markup=True
    )
    handler.setFormatter(logging.Formatter("%(message)s"))
    logger.addHandler(handler)

    return logger


# Global logger
logger = setup_logger("interview-prep")
