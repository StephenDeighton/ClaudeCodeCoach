"""
Detector for missing .env.example template.

When .env exists but .env.example doesn't, team members won't know
what environment variables are required for the project.
"""

from pathlib import Path
from typing import Optional
from health_checks.base import BaseDetector, HealthIssue, Severity
from health_checks import register


@register
class MissingEnvExampleDetector(BaseDetector):
    """Detects when .env exists but .env.example doesn't."""

    rule_id = "missing-env-example"
    severity = Severity.INFO
    title = ".env exists but no .env.example template"

    def check(self, project_path: Path, config: dict) -> Optional[HealthIssue]:
        """
        Check if .env exists without .env.example.

        Args:
            project_path: Root path of the Claude Code project
            config: Parsed .claude/ configuration (if exists)

        Returns:
            HealthIssue if .env.example is missing, None otherwise
        """
        env_path = project_path / ".env"
        env_example_path = project_path / ".env.example"

        if env_path.exists() and not env_example_path.exists():
            return HealthIssue(
                rule_id=self.rule_id,
                severity=self.severity,
                title=self.title,
                message=".env exists but no .env.example template",
                suggestion="Create .env.example (without real values) so team knows required environment variables",
                topic_slug="credential-management"
            )

        return None
