"""
Detector for missing /init command.

The /init command standardizes session startup and ensures consistent
project configuration across Claude Code sessions.
"""

from pathlib import Path
from typing import Optional
from health_checks.base import BaseDetector, HealthIssue, Severity
from health_checks import register


@register
class NoInitCommandDetector(BaseDetector):
    """Detects when .claude/commands/init.md is missing."""

    rule_id = "no-init-command"
    severity = Severity.INFO
    title = "No /init command found"

    fix_prompt = """My project would benefit from a /init command to standardize session startup.

Please create .claude/commands/init.md that:

1. **Welcomes the user** - greet and confirm project context
2. **Shows project status**:
   - Git branch and status
   - Recent commits
   - Any uncommitted changes

3. **Checks environment**:
   - Required dependencies installed?
   - Environment variables configured?
   - Database/services running?

4. **Displays TODO/status**:
   - Read status.md for recent work
   - Show high-priority TODOs
   - List blocked items

5. **Suggests next steps** based on project state

Command structure:
```markdown
---
name: init
description: Initialize Claude Code session
---

Welcome to [Project Name]!
[Startup checks and status]
```

Invoke with: `/init`
Run this at the start of each Claude Code session."""

    def check(self, project_path: Path, config: dict) -> Optional[HealthIssue]:
        """
        Check if .claude/commands/init.md exists.

        Args:
            project_path: Root path of the Claude Code project
            config: Parsed .claude/ configuration (if exists)

        Returns:
            HealthIssue if init command is missing, None otherwise
        """
        init_path = project_path / ".claude" / "commands" / "init.md"

        if not init_path.exists():
            return HealthIssue(
                rule_id=self.rule_id,
                severity=self.severity,
                title=self.title,
                message="No /init command found",
                suggestion="Create .claude/commands/init.md to standardize session startup",
                fix_prompt=self.fix_prompt,
                topic_slug="custom-slash-commands"
            )

        return None
