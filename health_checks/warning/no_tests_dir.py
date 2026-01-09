"""
Detector for missing tests directory.

A tests directory allows Claude to run tests and verify that changes work correctly.
"""

from pathlib import Path
from typing import Optional
from health_checks.base import BaseDetector, HealthIssue, Severity
from health_checks import register


@register
class NoTestsDirDetector(BaseDetector):
    """Detects when no tests directory exists."""

    rule_id = "no-tests-dir"
    severity = Severity.WARNING
    title = "No tests directory found"

    fix_prompt = """My project needs a tests directory so Claude can verify changes work correctly.

Please set up testing infrastructure:

1. **Create appropriate test directory** based on my tech stack:
   - Python: `tests/` or `test/`
   - JavaScript/Node: `__tests__/` or `test/`
   - Ruby: `spec/`
   - Other: suggest based on my stack

2. **Set up testing framework**:
   - Install test dependencies (pytest, jest, rspec, etc.)
   - Create basic test configuration
   - Add test commands to package.json/Makefile/etc.

3. **Create example test** to demonstrate the pattern

4. **Add test commands to CLAUDE.md**:
   - How to run tests
   - How to add new tests
   - Testing best practices for this project

5. **Update .gitignore** for test artifacts (coverage reports, etc.)

Benefits:
- Claude can run tests after making changes
- Verify fixes don't break existing functionality
- Build confidence in code changes"""

    def check(self, project_path: Path, config: dict) -> Optional[HealthIssue]:
        """
        Check if tests/ or similar directory exists.

        Args:
            project_path: Root path of the Claude Code project
            config: Parsed .claude/ configuration (if exists)

        Returns:
            HealthIssue if no tests directory found, None otherwise
        """
        test_dirs = [
            project_path / "tests",
            project_path / "test",
            project_path / "__tests__",
            project_path / "spec"
        ]

        for test_dir in test_dirs:
            if test_dir.exists() and test_dir.is_dir():
                return None

        return HealthIssue(
            rule_id=self.rule_id,
            severity=self.severity,
            title=self.title,
            message="No tests directory found",
            suggestion="Create tests/ directory. Claude can run tests to verify changes work correctly.",
            fix_prompt=self.fix_prompt,
            topic_slug="codebase-cc-relevant"
        )
