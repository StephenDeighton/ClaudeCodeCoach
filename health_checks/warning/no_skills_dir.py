"""
Detector for missing Skills directory.

Skills provide specialized expertise that loads on-demand via progressive disclosure.
This prevents context bloat while keeping detailed knowledge available.
"""

from pathlib import Path
from typing import Optional
from health_checks.base import BaseDetector, HealthIssue, Severity
from health_checks import register


@register
class NoSkillsDirDetector(BaseDetector):
    """Detects when .claude/skills/ directory is missing."""

    rule_id = "no-skills-dir"
    severity = Severity.WARNING
    title = "No Skills directory found"

    fix_prompt = """My project needs a Skills directory for specialized expertise that loads on-demand.

Please help me set up Skills:

1. **Create .claude/skills/ directory**
2. **Create a sample skill** - start with a commit.md skill:
   - Shows how to create good commits
   - Includes git workflow best practices
   - Uses progressive disclosure (only loaded when /commit is called)

3. **Update my CLAUDE.md** to reference the new skill:
   - Add line like: "For commit workflow, use /commit skill"

4. **Suggest other useful skills** for my project type:
   - feature-dev.md for new features
   - code-review.md for PR reviews
   - testing.md for test strategies
   - deployment.md for deployment workflows

Skills keep detailed knowledge out of main context until needed.
Each skill should be 50-200 lines of focused guidance."""

    def check(self, project_path: Path, config: dict) -> Optional[HealthIssue]:
        """
        Check if .claude/skills/ directory exists.

        Args:
            project_path: Root path of the Claude Code project
            config: Parsed .claude/ configuration (if exists)

        Returns:
            HealthIssue if skills directory is missing, None otherwise
        """
        skills_path = project_path / ".claude" / "skills"

        if not skills_path.exists():
            return HealthIssue(
                rule_id=self.rule_id,
                severity=self.severity,
                title=self.title,
                message="No Skills directory found",
                suggestion="Create .claude/skills/ for specialized expertise that loads on-demand via progressive disclosure",
                fix_prompt=self.fix_prompt,
                topic_slug="skills-overview"
            )

        return None
