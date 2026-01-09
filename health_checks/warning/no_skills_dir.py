"""
Detector for missing Skills directory.

Skills provide specialized expertise that loads on-demand via progressive disclosure.
This prevents context bloat while keeping detailed knowledge available.
"""

from pathlib import Path
from typing import Optional
from health_checks.base import BaseDetector, HealthIssue, Severity
from health_checks import register


@register
class NoSkillsDirDetector(BaseDetector):
    """Detects when .claude/skills/ directory is missing."""

    rule_id = "no-skills-dir"
    severity = Severity.WARNING
    title = "No Skills directory found"

    def check(self, project_path: Path, config: dict) -> Optional[HealthIssue]:
        """
        Check if .claude/skills/ directory exists.

        Args:
            project_path: Root path of the Claude Code project
            config: Parsed .claude/ configuration (if exists)

        Returns:
            HealthIssue if skills directory is missing, None otherwise
        """
        skills_path = project_path / ".claude" / "skills"

        if not skills_path.exists():
            return HealthIssue(
                rule_id=self.rule_id,
                severity=self.severity,
                title=self.title,
                message="No Skills directory found",
                suggestion="Create .claude/skills/ for specialized expertise that loads on-demand via progressive disclosure",
                topic_slug="skills-overview"
            )

        return None
