"""
Detector for missing status.md file.

status.md tracks daily progress and prevents Claude from repeating completed work.
"""

from pathlib import Path
from typing import Optional
from health_checks.base import BaseDetector, HealthIssue, Severity
from health_checks import register


@register
class NoStatusMdDetector(BaseDetector):
    """Detects when status.md is missing."""

    rule_id = "no-status-md"
    severity = Severity.WARNING
    title = "No status.md found"

    fix_prompt = """My project needs a status.md file to track daily progress and prevent repeated work.

Please create a status.md file with:

1. **Header section** with project name and current sprint/milestone
2. **Today's Progress** section for dated entries
3. **Template format** that's easy to update:
   ```markdown
   # Project Status

   ## 2026-01-09
   ### Completed
   - [x] Feature implementation
   - [x] Tests passing

   ### In Progress
   - [ ] Code review feedback

   ### Blocked
   - [ ] Waiting on API keys
   ```

4. **Add to CLAUDE.md**: Instruct me to update status.md after each session

Benefits:
- Prevents Claude from repeating completed work
- Creates a searchable history of project progress
- Helps with handoffs between sessions
- Documents decisions and context"""

    def check(self, project_path: Path, config: dict) -> Optional[HealthIssue]:
        """
        Check if status.md exists at project root.

        Args:
            project_path: Root path of the Claude Code project
            config: Parsed .claude/ configuration (if exists)

        Returns:
            HealthIssue if status.md is missing, None otherwise
        """
        status_path = project_path / "status.md"

        if not status_path.exists():
            return HealthIssue(
                rule_id=self.rule_id,
                severity=self.severity,
                title=self.title,
                message="No status.md found - Claude may repeat completed work",
                suggestion="Create status.md to track daily progress and prevent Claude from re-doing work",
                fix_prompt=self.fix_prompt,
                topic_slug="automated-documentation"
            )

        return None
