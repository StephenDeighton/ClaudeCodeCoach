"""
Detector for missing GitHub Actions.

GitHub Actions integration enables tagging Claude in issues and PRs for
automated assistance with development tasks.
"""

from pathlib import Path
from typing import Optional
from health_checks.base import BaseDetector, HealthIssue, Severity
from health_checks import register


@register
class NoGithubActionsDetector(BaseDetector):
    """Detects when GitHub Actions are not configured."""

    rule_id = "no-github-actions"
    severity = Severity.INFO
    title = "No GitHub Actions configured"

    def check(self, project_path: Path, config: dict) -> Optional[HealthIssue]:
        """
        Check if .github/workflows/ directory exists.

        Args:
            project_path: Root path of the Claude Code project
            config: Parsed .claude/ configuration (if exists)

        Returns:
            HealthIssue if GitHub Actions not configured, None otherwise
        """
        workflows_path = project_path / ".github" / "workflows"

        if not workflows_path.exists() or not workflows_path.is_dir():
            return HealthIssue(
                rule_id=self.rule_id,
                severity=self.severity,
                title=self.title,
                message="No GitHub Actions configured",
                suggestion="Run /install-gh-actions in Claude Code to enable tagging Claude in issues/PRs",
                topic_slug="github-integration"
            )

        return None
