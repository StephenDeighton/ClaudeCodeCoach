"""
Detector for invalid keys in hook configurations.

Hooks in Claude Code only support specific keys. Using invalid keys
will cause validation errors at startup.
"""

from pathlib import Path
from typing import Optional
import json
from health_checks.base import BaseDetector, HealthIssue, Severity
from health_checks import register


@register
class InvalidHookKeysDetector(BaseDetector):
    """Detects when hooks contain invalid configuration keys."""

    rule_id = "invalid-hook-keys"
    severity = Severity.WARNING
    title = "Invalid hook configuration keys"

    # Valid keys for hook configurations
    VALID_HOOK_KEYS = {
        "type",           # Required: hook type (usually "command")
        "command",        # Required: shell command to execute
        "blocking",       # Optional: wait for completion
        "successMessage", # Optional: custom success message
        "errorMessage",   # Optional: custom error message
        "filePatterns",   # Optional: file patterns for file-based hooks
    }

    fix_prompt = """My hook configuration contains invalid keys that Claude Code doesn't recognize.

Valid hook keys are:
- `type` (required) - hook type (usually "command")
- `command` (required) - shell command to execute
- `blocking` (optional) - whether to wait for completion
- `successMessage` (optional) - custom message on success
- `errorMessage` (optional) - custom message on error
- `filePatterns` (optional) - file patterns for hooks like Write:format

Please:
1. Review my .claude/settings.json hooks configuration
2. Remove any invalid keys like `outputMode`, `enabled`, etc.
3. Ensure each hook only uses the valid keys listed above

Example of a valid hook:
```json
{
  "hooks": {
    "SessionStart": [
      {
        "type": "command",
        "command": "echo \\"✓ Session started\\"",
        "blocking": false,
        "successMessage": "Ready to code!"
      }
    ]
  }
}
```

Remove the invalid keys to fix the validation error."""

    def check(self, project_path: Path, config: dict) -> Optional[HealthIssue]:
        """
        Check if hooks contain only valid configuration keys.

        Args:
            project_path: Root path of the Claude Code project
            config: Parsed .claude/ configuration (if exists)

        Returns:
            HealthIssue if invalid keys found, None otherwise
        """
        settings_paths = [
            project_path / ".claude" / "settings.json",
            project_path / ".claude" / "settings.local.json"
        ]

        invalid_hooks = []

        for settings_path in settings_paths:
            if not settings_path.exists():
                continue

            try:
                with open(settings_path, "r", encoding="utf-8") as f:
                    settings = json.load(f)

                # Check hooks configuration
                if "hooks" in settings and isinstance(settings["hooks"], dict):
                    for hook_name, hook_config in settings["hooks"].items():
                        # Hook config should be a list of hook objects
                        if not isinstance(hook_config, list):
                            continue

                        # Check each hook object in the array
                        for idx, hook_obj in enumerate(hook_config):
                            if not isinstance(hook_obj, dict):
                                continue

                            # Find invalid keys
                            hook_keys = set(hook_obj.keys())
                            invalid_keys = hook_keys - self.VALID_HOOK_KEYS

                            if invalid_keys:
                                invalid_hooks.append({
                                    "hook": f"{hook_name}[{idx}]",
                                    "file": settings_path.name,
                                    "invalid_keys": sorted(invalid_keys)
                                })

            except Exception:
                continue

        if not invalid_hooks:
            return None

        # Build detailed message
        invalid_list = []
        for item in invalid_hooks:
            keys_str = ", ".join(f"`{k}`" for k in item["invalid_keys"])
            invalid_list.append(f"  - {item['file']}:{item['hook']} has invalid keys: {keys_str}")

        message = "Hook configurations contain invalid keys:\n" + "\n".join(invalid_list)

        return HealthIssue(
            rule_id=self.rule_id,
            severity=self.severity,
            title=self.title,
            message=message,
            suggestion="Remove invalid keys from hook configurations. Only use: command, blocking, successMessage, errorMessage, filePatterns",
            fix_prompt=self.fix_prompt,
            topic_slug="hooks-system"
        )
