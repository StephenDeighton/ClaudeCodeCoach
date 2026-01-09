"""
Detector for missing /commit command.

The /commit command ensures consistent git workflow and commit message style.
"""

from pathlib import Path
from typing import Optional
from health_checks.base import BaseDetector, HealthIssue, Severity
from health_checks import register


@register
class NoCommitCommandDetector(BaseDetector):
    """Detects when .claude/commands/commit.md is missing."""

    rule_id = "no-commit-command"
    severity = Severity.INFO
    title = "No /commit command found"

    def check(self, project_path: Path, config: dict) -> Optional[HealthIssue]:
        """
        Check if .claude/commands/commit.md exists.

        Args:
            project_path: Root path of the Claude Code project
            config: Parsed .claude/ configuration (if exists)

        Returns:
            HealthIssue if commit command is missing, None otherwise
        """
        commit_path = project_path / ".claude" / "commands" / "commit.md"

        if not commit_path.exists():
            return HealthIssue(
                rule_id=self.rule_id,
                severity=self.severity,
                title=self.title,
                message="No /commit command found",
                suggestion="Create .claude/commands/commit.md for consistent git workflow",
                topic_slug="custom-slash-commands"
            )

        return None
