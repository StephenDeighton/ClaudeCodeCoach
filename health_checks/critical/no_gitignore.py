"""
Detector for missing .gitignore file.

A .gitignore file is essential for preventing accidental commits of secrets,
build artifacts, and local settings.
"""

from pathlib import Path
from typing import Optional
from health_checks.base import BaseDetector, HealthIssue, Severity
from health_checks import register


@register
class NoGitignoreDetector(BaseDetector):
    """Detects when .gitignore file is missing."""

    rule_id = "no-gitignore"
    severity = Severity.CRITICAL
    title = "No .gitignore file found"

    fix_prompt = """My project is missing a .gitignore file. Please create a comprehensive .gitignore that:

1. Protects secrets and credentials (.env, *.key, *.pem, credentials.*)
2. Excludes common build artifacts and dependencies (node_modules/, venv/, dist/, build/)
3. Ignores OS-specific files (.DS_Store, Thumbs.db)
4. Excludes IDE/editor files (.vscode/, .idea/, *.swp)
5. Protects Claude Code local settings (.claude/settings.local.json)
6. Is appropriate for my project's tech stack

Please analyze my project structure and create a .gitignore tailored to my needs."""

    def check(self, project_path: Path, config: dict) -> Optional[HealthIssue]:
        """
        Check if .gitignore exists at project root.

        Args:
            project_path: Root path of the Claude Code project
            config: Parsed .claude/ configuration (if exists)

        Returns:
            HealthIssue if .gitignore is missing, None otherwise
        """
        gitignore_path = project_path / ".gitignore"

        if not gitignore_path.exists():
            return HealthIssue(
                rule_id=self.rule_id,
                severity=self.severity,
                title=self.title,
                message="No .gitignore file found",
                suggestion="Create .gitignore to prevent committing secrets, build artifacts, and local settings",
                fix_prompt=self.fix_prompt,
                topic_slug="git-health"
            )

        return None
