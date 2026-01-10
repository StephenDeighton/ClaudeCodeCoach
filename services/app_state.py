"""
Simple app state management for sharing data between pages.
Follows the singleton service pattern used throughout C3.
"""

from dataclasses import dataclass, field
from datetime import datetime
from typing import List, Optional
from pathlib import Path
from health_checks.base import HealthIssue


@dataclass
class ScanResult:
    """Result of a health scan operation."""
    project_path: Path
    scan_time: datetime
    score: int
    issues: List[HealthIssue] = field(default_factory=list)
    detectors_run: int = 0


@dataclass
class AppState:
    """Global application state."""
    last_scan: Optional[ScanResult] = None
    wizard_path: Optional[Path] = None  # Path for wizard to process


# Global singleton instance
_state = AppState()


def get_state() -> AppState:
    """Get the global AppState instance."""
    return _state


def set_last_scan(result: ScanResult):
    """
    Store the results of the most recent scan.

    Args:
        result: ScanResult to store
    """
    _state.last_scan = result


def get_last_scan() -> Optional[ScanResult]:
    """
    Retrieve the results of the most recent scan.

    Returns:
        ScanResult if a scan has been performed, None otherwise
    """
    return _state.last_scan


def clear_last_scan():
    """Clear the last scan result."""
    _state.last_scan = None


def set_wizard_path(path: Path):
    """
    Store path for wizard to process.

    Args:
        path: Path to project directory
    """
    _state.wizard_path = path


def get_wizard_path() -> Optional[Path]:
    """
    Get path stored for wizard.

    Returns:
        Path if set, None otherwise
    """
    return _state.wizard_path


def clear_wizard_path():
    """Clear wizard path after processing."""
    _state.wizard_path = None
