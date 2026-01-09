"""
Detector for exposed secrets.

Checks if .env or .claude/settings.local.json exist but are not in .gitignore.
This prevents accidentally committing sensitive credentials to version control.
"""

from pathlib import Path
from typing import Optional
from health_checks.base import BaseDetector, HealthIssue, Severity
from health_checks import register


@register
class SecretsExposedDetector(BaseDetector):
    """Detects when secret files are not protected by .gitignore."""

    rule_id = "secrets-exposed"
    severity = Severity.CRITICAL
    title = "Secrets may be exposed"

    fix_prompt = """URGENT: My project has sensitive files that are not protected by .gitignore.

Please help me secure these files:

1. Add the appropriate patterns to .gitignore
2. If any secrets are already committed, tell me how to:
   - Remove them from git history (using git filter-branch or BFG Repo-Cleaner)
   - Rotate the exposed credentials
3. Create .env.example showing required variables without values
4. Document proper credential management in my README or CLAUDE.md

After adding to .gitignore, run:
   git add .gitignore
   git commit -m "docs: add secret files to gitignore"

NEVER commit the actual .env or settings.local.json files."""

    def check(self, project_path: Path, config: dict) -> Optional[HealthIssue]:
        """
        Check if sensitive files exist but are not in .gitignore.

        Args:
            project_path: Root path of the Claude Code project
            config: Parsed .claude/ configuration (if exists)

        Returns:
            HealthIssue if secrets are exposed, None otherwise
        """
        # Files that should be in .gitignore if they exist
        sensitive_files = [
            ".env",
            ".claude/settings.local.json"
        ]

        # Check if .gitignore exists
        gitignore_path = project_path / ".gitignore"
        gitignore_patterns = set()

        if gitignore_path.exists():
            try:
                with open(gitignore_path, "r", encoding="utf-8") as f:
                    gitignore_patterns = {
                        line.strip() for line in f
                        if line.strip() and not line.startswith("#")
                    }
            except Exception:
                pass

        # Check each sensitive file
        for file_pattern in sensitive_files:
            file_path = project_path / file_pattern
            if file_path.exists():
                # Check if this pattern is in .gitignore
                if file_pattern not in gitignore_patterns:
                    return HealthIssue(
                        rule_id=self.rule_id,
                        severity=self.severity,
                        title=self.title,
                        message=f"Secrets may be exposed - {file_pattern} is not in .gitignore",
                        suggestion=f"Add '{file_pattern}' to .gitignore to prevent committing secrets",
                        fix_prompt=self.fix_prompt,
                        file_path=file_path,
                        topic_slug="credential-management"
                    )

        return None
