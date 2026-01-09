"""
Detector for missing status.md file.

status.md tracks daily progress and prevents Claude from repeating completed work.
"""

from pathlib import Path
from typing import Optional
from health_checks.base import BaseDetector, HealthIssue, Severity
from health_checks import register


@register
class NoStatusMdDetector(BaseDetector):
    """Detects when status.md is missing."""

    rule_id = "no-status-md"
    severity = Severity.WARNING
    title = "No status.md found"

    def check(self, project_path: Path, config: dict) -> Optional[HealthIssue]:
        """
        Check if status.md exists at project root.

        Args:
            project_path: Root path of the Claude Code project
            config: Parsed .claude/ configuration (if exists)

        Returns:
            HealthIssue if status.md is missing, None otherwise
        """
        status_path = project_path / "status.md"

        if not status_path.exists():
            return HealthIssue(
                rule_id=self.rule_id,
                severity=self.severity,
                title=self.title,
                message="No status.md found - Claude may repeat completed work",
                suggestion="Create status.md to track daily progress and prevent Claude from re-doing work",
                topic_slug="automated-documentation"
            )

        return None
