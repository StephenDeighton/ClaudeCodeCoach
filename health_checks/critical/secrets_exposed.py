"""
Detector for exposed secrets.

Checks if .env or .claude/settings.local.json exist but are not in .gitignore.
This prevents accidentally committing sensitive credentials to version control.
"""

from pathlib import Path
from typing import Optional
from health_checks.base import BaseDetector, HealthIssue, Severity
from health_checks import register


@register
class SecretsExposedDetector(BaseDetector):
    """Detects when secret files are not protected by .gitignore."""

    rule_id = "secrets-exposed"
    severity = Severity.CRITICAL
    title = "Secrets may be exposed"

    def check(self, project_path: Path, config: dict) -> Optional[HealthIssue]:
        """
        Check if sensitive files exist but are not in .gitignore.

        Args:
            project_path: Root path of the Claude Code project
            config: Parsed .claude/ configuration (if exists)

        Returns:
            HealthIssue if secrets are exposed, None otherwise
        """
        # Files that should be in .gitignore if they exist
        sensitive_files = [
            ".env",
            ".claude/settings.local.json"
        ]

        # Check if .gitignore exists
        gitignore_path = project_path / ".gitignore"
        gitignore_patterns = set()

        if gitignore_path.exists():
            try:
                with open(gitignore_path, "r", encoding="utf-8") as f:
                    gitignore_patterns = {
                        line.strip() for line in f
                        if line.strip() and not line.startswith("#")
                    }
            except Exception:
                pass

        # Check each sensitive file
        for file_pattern in sensitive_files:
            file_path = project_path / file_pattern
            if file_path.exists():
                # Check if this pattern is in .gitignore
                if file_pattern not in gitignore_patterns:
                    return HealthIssue(
                        rule_id=self.rule_id,
                        severity=self.severity,
                        title=self.title,
                        message=f"Secrets may be exposed - {file_pattern} is not in .gitignore",
                        suggestion=f"Add '{file_pattern}' to .gitignore to prevent committing secrets",
                        file_path=file_path,
                        topic_slug="credential-management"
                    )

        return None
