"""Base class for health check detectors."""

from dataclasses import dataclass
from enum import Enum
from typing import Optional
from pathlib import Path


class Severity(Enum):
    CRITICAL = "critical"
    WARNING = "warning"
    INFO = "info"


@dataclass
class HealthIssue:
    """Represents a detected health issue."""
    rule_id: str
    severity: Severity
    title: str
    message: str
    suggestion: str
    file_path: Optional[Path] = None
    fix_template: Optional[str] = None
    fix_prompt: Optional[str] = None  # Full prompt for Claude to fix the issue
    topic_slug: Optional[str] = None  # Links to knowledge base


class BaseDetector:
    """Base class for health check detectors."""

    rule_id: str = "base"
    severity: Severity = Severity.INFO
    title: str = "Base Check"

    def check(self, project_path: Path, config: dict) -> Optional[HealthIssue]:
        """
        Check for health issues.

        Args:
            project_path: Root path of the Claude Code project
            config: Parsed .claude/ configuration (if exists)

        Returns:
            HealthIssue if problem detected, None otherwise
        """
        raise NotImplementedError("Subclasses must implement check()")
