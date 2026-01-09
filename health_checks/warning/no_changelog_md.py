"""
Detector for missing CHANGELOG.md file.

CHANGELOG.md tracks version history and major changes across releases.
"""

from pathlib import Path
from typing import Optional
from health_checks.base import BaseDetector, HealthIssue, Severity
from health_checks import register


@register
class NoChangelogMdDetector(BaseDetector):
    """Detects when CHANGELOG.md is missing."""

    rule_id = "no-changelog-md"
    severity = Severity.WARNING
    title = "No changelog found"

    fix_prompt = """My project needs a CHANGELOG.md to track version history and major changes.

Please create CHANGELOG.md following Keep a Changelog format:

1. **Create CHANGELOG.md** with structure:
   ```markdown
   # Changelog

   All notable changes to this project will be documented in this file.

   The format is based on [Keep a Changelog](https://keepachangelog.com/),
   and this project adheres to [Semantic Versioning](https://semver.org/).

   ## [Unreleased]
   ### Added
   - New features go here

   ### Changed
   - Changes to existing functionality

   ### Fixed
   - Bug fixes

   ## [1.0.0] - 2026-01-09
   ### Added
   - Initial release
   ```

2. **Categories to use**:
   - Added: New features
   - Changed: Changes to existing functionality
   - Deprecated: Soon-to-be removed features
   - Removed: Removed features
   - Fixed: Bug fixes
   - Security: Security fixes

3. **Update CLAUDE.md** to mention:
   - Update CHANGELOG.md for significant changes
   - Use semantic versioning for releases

4. **Benefits**:
   - Users know what changed between versions
   - Documents evolution of the project
   - Helps with release notes
   - Claude can reference it for context"""

    def check(self, project_path: Path, config: dict) -> Optional[HealthIssue]:
        """
        Check if CHANGELOG.md or changelog.md exists at project root.

        Args:
            project_path: Root path of the Claude Code project
            config: Parsed .claude/ configuration (if exists)

        Returns:
            HealthIssue if changelog is missing, None otherwise
        """
        changelog_paths = [
            project_path / "CHANGELOG.md",
            project_path / "changelog.md"
        ]

        for changelog_path in changelog_paths:
            if changelog_path.exists():
                return None

        return HealthIssue(
            rule_id=self.rule_id,
            severity=self.severity,
            title=self.title,
            message="No changelog found",
            suggestion="Create CHANGELOG.md to track version history and major changes",
            fix_prompt=self.fix_prompt,
            topic_slug="automated-documentation"
        )
