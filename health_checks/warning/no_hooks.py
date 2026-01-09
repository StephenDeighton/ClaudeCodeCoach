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
            topic_slug="hooks-system"
        )
