"""
Detector for missing commands directory.

Custom commands (slash commands) provide reusable workflows like /init, /commit, /status.
"""

from pathlib import Path
from typing import Optional
from health_checks.base import BaseDetector, HealthIssue, Severity
from health_checks import register


@register
class NoCommandsDirDetector(BaseDetector):
    """Detects when .claude/commands/ directory is missing."""

    rule_id = "no-commands-dir"
    severity = Severity.WARNING
    title = "No custom commands directory found"

    fix_prompt = """My project could benefit from custom slash commands for reusable workflows.

Please create .claude/commands/ directory with useful commands:

1. **Create .claude/commands/ directory**

2. **Create init.md** - project initialization command:
   ```markdown
   ---
   name: init
   description: Initialize a new Claude Code session
   ---

   Welcome! Starting new session for this project...
   [steps to initialize]
   ```

3. **Create commit.md** - git commit workflow:
   - Check git status
   - Show diff
   - Create descriptive commit message
   - Follow project commit conventions

4. **Create status.md** - update status tracking:
   - Show recent changes
   - Update status.md file
   - List what's completed/in-progress

5. **Suggest commands specific to my project**:
   - Build/deploy commands?
   - Testing workflows?
   - Code generation?
   - Documentation updates?

Commands are invoked like: /init, /commit, /status
They save time by codifying project-specific workflows."""

    def check(self, project_path: Path, config: dict) -> Optional[HealthIssue]:
        """
        Check if .claude/commands/ directory exists.

        Args:
            project_path: Root path of the Claude Code project
            config: Parsed .claude/ configuration (if exists)

        Returns:
            HealthIssue if commands directory is missing, None otherwise
        """
        commands_path = project_path / ".claude" / "commands"

        if not commands_path.exists():
            return HealthIssue(
                rule_id=self.rule_id,
                severity=self.severity,
                title=self.title,
                message="No custom commands directory found",
                suggestion="Create .claude/commands/ for reusable slash commands like /init, /commit, /status",
                fix_prompt=self.fix_prompt,
                topic_slug="custom-slash-commands"
            )

        return None
