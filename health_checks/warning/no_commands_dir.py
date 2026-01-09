"""
Detector for missing commands directory.

Custom commands (slash commands) provide reusable workflows like /init, /commit, /status.
"""

from pathlib import Path
from typing import Optional
from health_checks.base import BaseDetector, HealthIssue, Severity
from health_checks import register


@register
class NoCommandsDirDetector(BaseDetector):
    """Detects when .claude/commands/ directory is missing."""

    rule_id = "no-commands-dir"
    severity = Severity.WARNING
    title = "No custom commands directory found"

    def check(self, project_path: Path, config: dict) -> Optional[HealthIssue]:
        """
        Check if .claude/commands/ directory exists.

        Args:
            project_path: Root path of the Claude Code project
            config: Parsed .claude/ configuration (if exists)

        Returns:
            HealthIssue if commands directory is missing, None otherwise
        """
        commands_path = project_path / ".claude" / "commands"

        if not commands_path.exists():
            return HealthIssue(
                rule_id=self.rule_id,
                severity=self.severity,
                title=self.title,
                message="No custom commands directory found",
                suggestion="Create .claude/commands/ for reusable slash commands like /init, /commit, /status",
                topic_slug="custom-slash-commands"
            )

        return None
