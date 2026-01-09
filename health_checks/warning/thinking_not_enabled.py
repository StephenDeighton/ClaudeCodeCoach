"""
Detector for missing extended thinking configuration.

Setting MAX_THINKING_TOKENS enables Claude to reason more deeply about complex tasks.
"""

from pathlib import Path
from typing import Optional
import json
from health_checks.base import BaseDetector, HealthIssue, Severity
from health_checks import register


@register
class ThinkingNotEnabledDetector(BaseDetector):
    """Detects when extended thinking is not configured."""

    rule_id = "thinking-not-enabled"
    severity = Severity.WARNING
    title = "Extended thinking not configured"

    def check(self, project_path: Path, config: dict) -> Optional[HealthIssue]:
        """
        Check if MAX_THINKING_TOKENS is set in settings.

        Args:
            project_path: Root path of the Claude Code project
            config: Parsed .claude/ configuration (if exists)

        Returns:
            HealthIssue if thinking is not enabled, None otherwise
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

                # Check for MAX_THINKING_TOKENS in env
                if "env" in settings and isinstance(settings["env"], dict):
                    if "MAX_THINKING_TOKENS" in settings["env"]:
                        return None
            except Exception:
                continue

        return HealthIssue(
            rule_id=self.rule_id,
            severity=self.severity,
            title=self.title,
            message="Extended thinking not configured",
            suggestion="Set MAX_THINKING_TOKENS: 10000 for deeper reasoning on complex tasks",
            topic_slug="extended-thinking"
        )
