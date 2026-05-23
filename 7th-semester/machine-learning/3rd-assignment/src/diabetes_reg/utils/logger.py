"""Logger configuration using loguru."""

from __future__ import annotations

import sys
from pathlib import Path

from loguru import logger


def setup_logger(log_dir: Path = Path("logs")) -> None:
    """Configure loguru logger with stderr and rotating file sinks.

    Args:
        log_dir: Directory where log files are stored.
    """
    log_dir.mkdir(parents=True, exist_ok=True)
    logger.remove()
    logger.add(
        sys.stderr,
        level="INFO",
        format="<green>{time:HH:mm:ss}</green> | <level>{level}</level> | {message}",
    )
    logger.add(
        log_dir / "pipeline_{time:YYYYMMDD_HHmmss}.log",
        level="DEBUG",
        rotation="10 MB",
        retention="7 days",
    )
