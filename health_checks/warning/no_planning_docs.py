"""
Detector for missing planning documents.

Planning documents like PRD.md, EDD.md, or plan.md help Claude understand
project requirements and make better implementation decisions.
"""

from pathlib import Path
from typing import Optional
from health_checks.base import BaseDetector, HealthIssue, Severity
from health_checks import register


@register
class NoPlanningDocsDetector(BaseDetector):
    """Detects when planning documents are missing."""

    rule_id = "no-planning-docs"
    severity = Severity.WARNING
    title = "No planning documents found"

    def check(self, project_path: Path, config: dict) -> Optional[HealthIssue]:
        """
        Check if any planning documents exist.

        Args:
            project_path: Root path of the Claude Code project
            config: Parsed .claude/ configuration (if exists)

        Returns:
            HealthIssue if no planning documents found, None otherwise
        """
        planning_paths = [
            project_path / "PRD.md",
            project_path / "EDD.md",
            project_path / "plan.md",
            project_path / "PLAN.md",
            project_path / "docs" / "PRD.md",
            project_path / "docs" / "plan.md"
        ]

        for planning_path in planning_paths:
            if planning_path.exists():
                return None

        return HealthIssue(
            rule_id=self.rule_id,
            severity=self.severity,
            title=self.title,
            message="No planning documents found",
            suggestion="Create PRD.md (requirements) or plan.md to guide development. Claude makes better decisions with clear specs.",
            topic_slug="psb-planning-phase"
        )
