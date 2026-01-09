"""
Logging Configuration for ClaudeCodeCoach
================================

Provides centralized logging for the packaged app.

Log Strategy:
- Location: ~/Library/Logs/ClaudeCodeCoach/
- Rotation: Keep last 7 days of logs
- Max size: 10MB per log file
- Cleanup: On app startup, delete logs older than 7 days
- Format: [timestamp] [level] [module] message

Usage:
    from services.logging_config import get_logger

    logger = get_logger(__name__)
    logger.info("Something happened")
    logger.warning("Something concerning")
    logger.error("Something broke", exc_info=True)
"""

import logging
import sys
from pathlib import Path
from datetime import datetime, timedelta
from logging.handlers import RotatingFileHandler


# Global logger instance
_logger = None
_log_dir = None


def get_log_directory() -> Path:
    """
    Get the log directory for ClaudeCodeCoach

    Returns:
        Path to ~/Library/Logs/ClaudeCodeCoach/ (creates if needed)
    """
    global _log_dir

    if _log_dir is None:
        # Standard macOS log location
        _log_dir = Path.home() / "Library" / "Logs" / "ClaudeCodeCoach"
        _log_dir.mkdir(parents=True, exist_ok=True)

    return _log_dir


def cleanup_old_logs(days_to_keep: int = 7):
    """
    Delete log files older than specified days

    Args:
        days_to_keep: Number of days of logs to keep (default: 7)
    """
    try:
        log_dir = get_log_directory()
        cutoff_date = datetime.now() - timedelta(days=days_to_keep)

        deleted_count = 0
        for log_file in log_dir.glob("*.log*"):
            try:
                # Get file modification time
                mtime = datetime.fromtimestamp(log_file.stat().st_mtime)

                if mtime < cutoff_date:
                    log_file.unlink()
                    deleted_count += 1
            except Exception:
                # Ignore errors on individual files
                pass

        if deleted_count > 0:
            # Use the logger if available, otherwise print
            if _logger:
                _logger.info(f"Cleaned up {deleted_count} old log files (older than {days_to_keep} days)")

    except Exception as e:
        # Can't log this since we might be in logger initialization
        # Just silently fail
        pass


def setup_logging(log_level: str = "INFO") -> logging.Logger:
    """
    Set up logging for ClaudeCodeCoach

    Args:
        log_level: Logging level (DEBUG, INFO, WARNING, ERROR)

    Returns:
        Configured logger instance
    """
    global _logger

    if _logger is not None:
        return _logger

    # Create logger
    logger = logging.getLogger("mexus")
    logger.setLevel(getattr(logging, log_level.upper()))

    # Clear any existing handlers
    logger.handlers.clear()

    # Create log directory
    log_dir = get_log_directory()

    # Log file with date
    today = datetime.now().strftime("%Y%m%d")
    log_file = log_dir / f"mexus_{today}.log"

    # File handler with rotation (10MB max, keep 3 backups per day)
    file_handler = RotatingFileHandler(
        log_file,
        maxBytes=10 * 1024 * 1024,  # 10MB
        backupCount=3,
        encoding='utf-8'
    )

    # Console handler (for development - won't show in packaged app)
    console_handler = logging.StreamHandler(sys.stdout)

    # Formatter
    formatter = logging.Formatter(
        '[%(asctime)s] [%(levelname)s] [%(name)s] %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S'
    )

    file_handler.setFormatter(formatter)
    console_handler.setFormatter(formatter)

    logger.addHandler(file_handler)
    logger.addHandler(console_handler)

    # Clean up old logs on startup
    cleanup_old_logs(days_to_keep=7)

    # Log startup
    logger.info("=" * 70)
    logger.info(f"ClaudeCodeCoach logging started - Log level: {log_level}")
    logger.info(f"Log file: {log_file}")
    logger.info("=" * 70)

    _logger = logger
    return logger


def get_logger(name: str = None) -> logging.Logger:
    """
    Get a logger instance

    Args:
        name: Logger name (usually __name__ of the module)

    Returns:
        Logger instance
    """
    global _logger

    # Initialize logging if not already done
    if _logger is None:
        setup_logging()

    # Return child logger with module name
    if name:
        return logging.getLogger(f"mexus.{name}")
    else:
        return logging.getLogger("mexus")


# Convenience function to get log directory for user access
def get_log_file_path() -> str:
    """
    Get the current log file path as a string

    Returns:
        Path to today's log file
    """
    log_dir = get_log_directory()
    today = datetime.now().strftime("%Y%m%d")
    return str(log_dir / f"mexus_{today}.log")


if __name__ == "__main__":
    # Test logging
    logger = get_logger(__name__)

    logger.debug("This is a debug message")
    logger.info("This is an info message")
    logger.warning("This is a warning message")
    logger.error("This is an error message")

    try:
        raise ValueError("Test exception")
    except Exception:
        logger.error("Caught exception", exc_info=True)

    print(f"\nLog file location: {get_log_file_path()}")
