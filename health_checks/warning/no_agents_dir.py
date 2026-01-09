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

    fix_prompt = """My project could benefit from specialized subagents for focused tasks.

Please set up .claude/agents/ directory with useful subagents:

1. **Create .claude/agents/ directory**

2. **Create a security-reviewer subagent** (security-reviewer.md):
   - Reviews code for security vulnerabilities
   - Checks for common OWASP issues
   - Validates input sanitization
   - Reviews authentication/authorization

3. **Create a code-reviewer subagent** (code-reviewer.md):
   - Reviews code quality and conventions
   - Checks for code smells
   - Validates test coverage
   - Ensures consistency with project patterns

4. **Create a performance-auditor subagent** (if appropriate):
   - Identifies performance bottlenecks
   - Suggests optimization strategies
   - Reviews database queries
   - Analyzes algorithm complexity

5. **Suggest subagents specific to my project needs**

Subagents provide specialized expertise that can be invoked with the Task tool.
Each subagent has focused instructions for a specific domain."""

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
                fix_prompt=self.fix_prompt,
                topic_slug="subagents-overview"
            )

        return None
