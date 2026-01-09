"""
Detector for bloated CLAUDE.md files.

Claude Code projects should keep their CLAUDE.md files concise.
Large instruction files make it harder for Claude to process context efficiently.
"""

from pathlib import Path
from typing import Optional
from health_checks.base import BaseDetector, HealthIssue, Severity
from health_checks import register


@register
class BloatedClaudeMdDetector(BaseDetector):
    """Detects when CLAUDE.md is too large."""

    rule_id = "bloated_claude_md"
    severity = Severity.CRITICAL
    title = "CLAUDE.md is too large"

    fix_prompt = """My CLAUDE.md file is too large and needs to be refactored for better performance.

Please help me restructure my project instructions:

1. **Analyze my current CLAUDE.md** - identify what content should stay vs. move
2. **Create a slim CLAUDE.md** (under 50 lines) with only:
   - Project overview (2-3 sentences)
   - Core architecture patterns
   - Critical conventions
   - Links to Skills for detailed workflows

3. **Create Skills** for detailed content:
   - Create .claude/skills/ directory if needed
   - Move step-by-step guides to individual Skill files
   - Create skill files like: commit.md, feature-dev.md, etc.
   - Use progressive disclosure - Claude loads Skills only when needed

4. **Update my CLAUDE.md** with references to the new Skills

Example structure:
```
CLAUDE.md: "For commit workflow, use /commit skill"
.claude/skills/commit.md: [detailed commit instructions]
```

This keeps my project context lean while maintaining detailed guidance."""

    def check(self, project_path: Path, config: dict) -> Optional[HealthIssue]:
        """
        Check if CLAUDE.md or .claude/CLAUDE.md exists and is too large.

        Args:
            project_path: Root path of the Claude Code project
            config: Parsed .claude/ configuration (if exists)

        Returns:
            HealthIssue if file is too large, None otherwise
        """
        # Check both possible locations
        claude_md_paths = [
            project_path / ".claude" / "CLAUDE.md",
            project_path / "CLAUDE.md",
        ]

        for claude_md_path in claude_md_paths:
            if not claude_md_path.exists():
                continue

            # Count lines
            try:
                with open(claude_md_path, "r", encoding="utf-8") as f:
                    lines = f.readlines()
                    line_count = len(lines)

                # Determine severity
                if line_count > 100:
                    severity = Severity.CRITICAL
                    message = (
                        f"Your CLAUDE.md has {line_count} lines. "
                        f"This is critically too large and will impact Claude's ability to process your project efficiently."
                    )
                elif line_count > 50:
                    severity = Severity.WARNING
                    message = (
                        f"Your CLAUDE.md has {line_count} lines. "
                        f"Consider trimming it down for better performance."
                    )
                else:
                    # File is fine
                    return None

                return HealthIssue(
                    rule_id=self.rule_id,
                    severity=severity,
                    title=self.title,
                    message=message,
                    suggestion=(
                        "Move detailed documentation to Skills instead of CLAUDE.md. "
                        "Keep CLAUDE.md under 50 lines by focusing on:\n"
                        "  • Project overview (2-3 sentences)\n"
                        "  • Architecture patterns\n"
                        "  • Critical conventions\n"
                        "  • Links to Skills for detailed workflows\n\n"
                        "Skills are better for step-by-step guides and detailed procedures."
                    ),
                    fix_prompt=self.fix_prompt,
                    file_path=claude_md_path,
                    topic_slug="claude-md-best-practices",
                )

            except Exception as e:
                # If we can't read the file, skip it
                continue

        return None
