"""
Detector for missing README.md.

README.md provides project context that Claude reads to understand
the project's purpose, setup, and usage.
"""

from pathlib import Path
from typing import Optional
from health_checks.base import BaseDetector, HealthIssue, Severity
from health_checks import register


@register
class NoReadmeDetector(BaseDetector):
    """Detects when README.md is missing."""

    rule_id = "no-readme"
    severity = Severity.WARNING
    title = "No README.md found"

    fix_prompt = """My project needs a README.md file to provide essential context.

Please create a comprehensive README.md with:

1. **Project title and description** - what this project does
2. **Installation/Setup** - how to get started
   - Prerequisites
   - Installation steps
   - Configuration

3. **Usage** - basic examples and common commands

4. **Project structure** - overview of key directories and files

5. **Development workflow**:
   - How to run locally
   - How to run tests
   - How to build/deploy

6. **Contributing** - guidelines for contributors (if applicable)

7. **License** - project license information

Important: Claude reads README.md for project context, so make it informative but concise.
Focus on practical information developers need to work with the codebase."""

    def check(self, project_path: Path, config: dict) -> Optional[HealthIssue]:
        """
        Check if README.md exists.

        Args:
            project_path: Root path of the Claude Code project
            config: Parsed .claude/ configuration (if exists)

        Returns:
            HealthIssue if README.md is missing, None otherwise
        """
        readme_paths = [
            project_path / "README.md",
            project_path / "readme.md"
        ]

        for readme_path in readme_paths:
            if readme_path.exists():
                return None

        return HealthIssue(
            rule_id=self.rule_id,
            severity=self.severity,
            title=self.title,
            message="No README.md found",
            suggestion="Create README.md to describe the project. Claude reads this for context.",
            fix_prompt=self.fix_prompt,
            topic_slug="project-setup-basics"
        )
