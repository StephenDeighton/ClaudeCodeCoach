"""
Detector for missing hooks configuration.

Hooks enable auto-formatting, logging, and custom workflows that run
automatically at specific points in the Claude Code session.
"""

from pathlib import Path
from typing import Optional
import json
from health_checks.base import BaseDetector, HealthIssue, Severity
from health_checks import register


@register
class NoHooksDetector(BaseDetector):
    """Detects when no hooks are configured."""

    rule_id = "no-hooks"
    severity = Severity.WARNING
    title = "No hooks configured"

    fix_prompt = """My project could benefit from Claude Code hooks for automation and workflow enhancement.

Please set up useful hooks in .claude/settings.json:

1. **Session start hook** - runs when Claude starts:
   ```json
   {
     "hooks": {
       "SessionStart:startup": {
         "command": "echo '✓ Session started'",
         "blocking": false
       }
     }
   }
   ```

2. **Common useful hooks:**
   - `Write:format` - Auto-format code after writing files
   - `SessionEnd:cleanup` - Clean up temp files on exit
   - `Bash:log` - Log all bash commands for auditing
   - `SessionStart:git-status` - Show git status on startup

3. **Example: Auto-format Python**:
   ```json
   {
     "hooks": {
       "Write:format": {
         "command": "black {file_path} 2>/dev/null || true",
         "blocking": false,
         "filePatterns": ["*.py"]
       }
     }
   }
   ```

4. **Suggest hooks appropriate for my project's tech stack**

Hooks automate repetitive tasks and ensure consistency across sessions."""

    def check(self, project_path: Path, config: dict) -> Optional[HealthIssue]:
        """
        Check if any hooks are configured in settings.

        Args:
            project_path: Root path of the Claude Code project
            config: Parsed .claude/ configuration (if exists)

        Returns:
            HealthIssue if no hooks configured, None otherwise
        """
        settings_paths = [
            project_path / ".claude" / "settings.json",
            project_path / ".claude" / "settings.local.json"
        ]

        for settings_path in settings_paths:
            if not settings_path.exists():
                continue

            try:
                with open(settings_path, "r", encoding="utf-8") as f:
                    settings = json.load(f)

                # Check for hooks configuration
                if "hooks" in settings and isinstance(settings["hooks"], dict):
                    if len(settings["hooks"]) > 0:
                        return None
            except Exception:
                continue

        return HealthIssue(
            rule_id=self.rule_id,
            severity=self.severity,
            title=self.title,
            message="No hooks configured",
            suggestion="Consider adding hooks for auto-formatting, logging, or custom workflows",
            fix_prompt=self.fix_prompt,
            topic_slug="hooks-system"
        )
