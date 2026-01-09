"""
Detector for missing CHANGELOG.md file.

CHANGELOG.md tracks version history and major changes across releases.
"""

from pathlib import Path
from typing import Optional
from health_checks.base import BaseDetector, HealthIssue, Severity
from health_checks import register


@register
class NoChangelogMdDetector(BaseDetector):
    """Detects when CHANGELOG.md is missing."""

    rule_id = "no-changelog-md"
    severity = Severity.WARNING
    title = "No changelog found"

    def check(self, project_path: Path, config: dict) -> Optional[HealthIssue]:
        """
        Check if CHANGELOG.md or changelog.md exists at project root.

        Args:
            project_path: Root path of the Claude Code project
            config: Parsed .claude/ configuration (if exists)

        Returns:
            HealthIssue if changelog is missing, None otherwise
        """
        changelog_paths = [
            project_path / "CHANGELOG.md",
            project_path / "changelog.md"
        ]

        for changelog_path in changelog_paths:
            if changelog_path.exists():
                return None

        return HealthIssue(
            rule_id=self.rule_id,
            severity=self.severity,
            title=self.title,
            message="No changelog found",
            suggestion="Create CHANGELOG.md to track version history and major changes",
            topic_slug="automated-documentation"
        )
