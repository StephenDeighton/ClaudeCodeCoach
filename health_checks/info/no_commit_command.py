"""
Detector for missing /commit command.

The /commit command ensures consistent git workflow and commit message style.
"""

from pathlib import Path
from typing import Optional
from health_checks.base import BaseDetector, HealthIssue, Severity
from health_checks import register


@register
class NoCommitCommandDetector(BaseDetector):
    """Detects when .claude/commands/commit.md is missing."""

    rule_id = "no-commit-command"
    severity = Severity.INFO
    title = "No /commit command found"

    fix_prompt = """My project would benefit from a /commit command for consistent git workflow.

Please create .claude/commands/commit.md:

1. **Check git status** - show what will be committed
2. **Review changes** - show git diff
3. **Create commit message** following project conventions:
   - Analyze recent commits for style (conventional commits, etc.)
   - Generate descriptive message
   - Include Co-Authored-By: Claude Sonnet 4.5 <noreply@anthropic.com>

4. **Stage and commit**:
   - Add relevant files
   - Create the commit
   - Show status after

Command structure:
```markdown
---
name: commit
description: Create a git commit with best practices
---

[Steps above]
```

Invoke with: `/commit`
This ensures consistent commit messages and workflow."""

    def check(self, project_path: Path, config: dict) -> Optional[HealthIssue]:
        """
        Check if .claude/commands/commit.md exists.

        Args:
            project_path: Root path of the Claude Code project
            config: Parsed .claude/ configuration (if exists)

        Returns:
            HealthIssue if commit command is missing, None otherwise
        """
        commit_path = project_path / ".claude" / "commands" / "commit.md"

        if not commit_path.exists():
            return HealthIssue(
                rule_id=self.rule_id,
                severity=self.severity,
                title=self.title,
                message="No /commit command found",
                suggestion="Create .claude/commands/commit.md for consistent git workflow",
                fix_prompt=self.fix_prompt,
                topic_slug="custom-slash-commands"
            )

        return None
