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
