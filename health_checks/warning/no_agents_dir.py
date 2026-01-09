"""
Detector for missing agents directory.

.claude/agents/ stores specialized subagent definitions for security reviews,
code analysis, and other specialized tasks.
"""

from pathlib import Path
from typing import Optional
from health_checks.base import BaseDetector, HealthIssue, Severity
from health_checks import register


@register
class NoAgentsDirDetector(BaseDetector):
    """Detects when .claude/agents/ directory is missing."""

    rule_id = "no-agents-dir"
    severity = Severity.WARNING
    title = "No subagents directory found"

    def check(self, project_path: Path, config: dict) -> Optional[HealthIssue]:
        """
        Check if .claude/agents/ directory exists.

        Args:
            project_path: Root path of the Claude Code project
            config: Parsed .claude/ configuration (if exists)

        Returns:
            HealthIssue if agents directory is missing, None otherwise
        """
        agents_path = project_path / ".claude" / "agents"

        if not agents_path.exists():
            return HealthIssue(
                rule_id=self.rule_id,
                severity=self.severity,
                title=self.title,
                message="No subagents directory found",
                suggestion="Create .claude/agents/ for specialized subagent definitions (security reviewer, etc.)",
                topic_slug="subagents-overview"
            )

        return None
