"""
Detector for MCP server overload.

Checks if too many MCP servers are configured, which can bloat context on startup.
Each MCP server loads its documentation into Claude's context at session start.
"""

from pathlib import Path
from typing import Optional
import json
from health_checks.base import BaseDetector, HealthIssue, Severity
from health_checks import register


@register
class McpOverloadDetector(BaseDetector):
    """Detects when too many MCP servers are configured."""

    rule_id = "mcp-overload"
    severity = Severity.CRITICAL
    title = "Too many MCP servers configured"

    def check(self, project_path: Path, config: dict) -> Optional[HealthIssue]:
        """
        Check if more than 3 MCP servers are configured.

        Args:
            project_path: Root path of the Claude Code project
            config: Parsed .claude/ configuration (if exists)

        Returns:
            HealthIssue if too many MCP servers, None otherwise
        """
        # Check both settings.json and settings.local.json
        settings_paths = [
            project_path / ".claude" / "settings.json",
            project_path / ".claude" / "settings.local.json"
        ]

        total_servers = 0

        for settings_path in settings_paths:
            if not settings_path.exists():
                continue

            try:
                with open(settings_path, "r", encoding="utf-8") as f:
                    settings = json.load(f)

                # Check for MCP servers in mcpServers key
                if "mcpServers" in settings:
                    mcp_servers = settings["mcpServers"]
                    if isinstance(mcp_servers, dict):
                        total_servers += len(mcp_servers)
            except Exception:
                # If we can't parse the file, skip it
                continue

        # Threshold: more than 3 servers
        if total_servers > 3:
            return HealthIssue(
                rule_id=self.rule_id,
                severity=self.severity,
                title=self.title,
                message=f"{total_servers} MCP servers configured - this may bloat context on startup",
                suggestion="Consider disabling unused MCP servers. Each server loads into context at session start.",
                topic_slug="mcp-context-warning"
            )

        return None
