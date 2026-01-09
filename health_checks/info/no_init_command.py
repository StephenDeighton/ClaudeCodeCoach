"""
Detector for missing /init command.

The /init command standardizes session startup and ensures consistent
project configuration across Claude Code sessions.
"""

from pathlib import Path
from typing import Optional
from health_checks.base import BaseDetector, HealthIssue, Severity
from health_checks import register


@register
class NoInitCommandDetector(BaseDetector):
    """Detects when .claude/commands/init.md is missing."""

    rule_id = "no-init-command"
    severity = Severity.INFO
    title = "No /init command found"

    def check(self, project_path: Path, config: dict) -> Optional[HealthIssue]:
        """
        Check if .claude/commands/init.md exists.

        Args:
            project_path: Root path of the Claude Code project
            config: Parsed .claude/ configuration (if exists)

        Returns:
            HealthIssue if init command is missing, None otherwise
        """
        init_path = project_path / ".claude" / "commands" / "init.md"

        if not init_path.exists():
            return HealthIssue(
                rule_id=self.rule_id,
                severity=self.severity,
                title=self.title,
                message="No /init command found",
                suggestion="Create .claude/commands/init.md to standardize session startup",
                topic_slug="custom-slash-commands"
            )

        return None
