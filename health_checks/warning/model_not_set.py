"""
Detector for missing model configuration.

Explicitly setting ANTHROPIC_MODEL ensures consistent model usage across sessions.
Use sonnet-4.5 for daily work, opus-4.5 for complex planning.
"""

from pathlib import Path
from typing import Optional
import json
from health_checks.base import BaseDetector, HealthIssue, Severity
from health_checks import register


@register
class ModelNotSetDetector(BaseDetector):
    """Detects when ANTHROPIC_MODEL is not explicitly configured."""

    rule_id = "model-not-set"
    severity = Severity.WARNING
    title = "No model explicitly configured"

    def check(self, project_path: Path, config: dict) -> Optional[HealthIssue]:
        """
        Check if ANTHROPIC_MODEL is set in settings.

        Args:
            project_path: Root path of the Claude Code project
            config: Parsed .claude/ configuration (if exists)

        Returns:
            HealthIssue if model is not set, None otherwise
        """
        # Check project settings first
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

                # Check for ANTHROPIC_MODEL in env
                if "env" in settings and isinstance(settings["env"], dict):
                    if "ANTHROPIC_MODEL" in settings["env"]:
                        return None
            except Exception:
                continue

        # Check global settings
        home_settings = Path.home() / ".claude" / "settings.json"
        if home_settings.exists():
            try:
                with open(home_settings, "r", encoding="utf-8") as f:
                    settings = json.load(f)

                if "env" in settings and isinstance(settings["env"], dict):
                    if "ANTHROPIC_MODEL" in settings["env"]:
                        return None
            except Exception:
                pass

        return HealthIssue(
            rule_id=self.rule_id,
            severity=self.severity,
            title=self.title,
            message="No model explicitly configured - using defaults",
            suggestion="Set ANTHROPIC_MODEL in settings to ensure consistent model usage (sonnet-4.5 for daily work, opus-4.5 for complex planning)",
            topic_slug="strategic-model-usage"
        )
