"""
Detector for missing README.md.

README.md provides project context that Claude reads to understand
the project's purpose, setup, and usage.
"""

from pathlib import Path
from typing import Optional
from health_checks.base import BaseDetector, HealthIssue, Severity
from health_checks import register


@register
class NoReadmeDetector(BaseDetector):
    """Detects when README.md is missing."""

    rule_id = "no-readme"
    severity = Severity.WARNING
    title = "No README.md found"

    def check(self, project_path: Path, config: dict) -> Optional[HealthIssue]:
        """
        Check if README.md exists.

        Args:
            project_path: Root path of the Claude Code project
            config: Parsed .claude/ configuration (if exists)

        Returns:
            HealthIssue if README.md is missing, None otherwise
        """
        readme_paths = [
            project_path / "README.md",
            project_path / "readme.md"
        ]

        for readme_path in readme_paths:
            if readme_path.exists():
                return None

        return HealthIssue(
            rule_id=self.rule_id,
            severity=self.severity,
            title=self.title,
            message="No README.md found",
            suggestion="Create README.md to describe the project. Claude reads this for context.",
            topic_slug="project-setup-basics"
        )
