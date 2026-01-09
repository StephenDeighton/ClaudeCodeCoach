"""
Detector for large files.

Claude performs better with smaller, focused modules.
Files over 400 lines are harder for Claude to process efficiently.
"""

from pathlib import Path
from typing import Optional
from health_checks.base import BaseDetector, HealthIssue, Severity
from health_checks import register


@register
class LargeFilesDetector(BaseDetector):
    """Detects when files are too large (>400 lines)."""

    rule_id = "large-files"
    severity = Severity.WARNING
    title = "Large files detected"

    fix_prompt = """My project has large files (>400 lines) that could be refactored for better Claude performance.

Please help me refactor these files:

1. **Analyze the largest files** to understand what they contain

2. **Propose refactoring strategy**:
   - Split by responsibility/concern
   - Extract reusable utilities
   - Separate data from logic
   - Move types/interfaces to separate files

3. **Create a refactoring plan**:
   - Which files to split first (start with worst offenders)
   - How to split them (what goes where)
   - What to name the new files
   - Update imports across codebase

4. **Perform the refactoring**:
   - Create new smaller files
   - Move code systematically
   - Update all imports
   - Test that everything still works

5. **Benefits of smaller files**:
   - Claude processes them faster
   - Easier to understand and maintain
   - Better code organization
   - Faster context loading

Target: Keep files under 300 lines ideally, 400 lines maximum."""

    def check(self, project_path: Path, config: dict) -> Optional[HealthIssue]:
        """
        Check for files over 400 lines.

        Args:
            project_path: Root path of the Claude Code project
            config: Parsed .claude/ configuration (if exists)

        Returns:
            HealthIssue if large files found, None otherwise
        """
        # File extensions to check
        extensions = ["*.py", "*.js", "*.ts", "*.jsx", "*.tsx"]

        # Directories to exclude
        exclude_dirs = {"node_modules", "venv", ".venv", "venv_312", ".git", "__pycache__",
                       "dist", "build", ".next", ".nuxt", "site-packages"}

        large_files = []

        for ext in extensions:
            for file_path in project_path.rglob(ext):
                # Skip excluded directories
                if any(excluded in file_path.parts for excluded in exclude_dirs):
                    continue

                try:
                    with open(file_path, "r", encoding="utf-8") as f:
                        line_count = sum(1 for _ in f)

                    if line_count > 400:
                        relative_path = file_path.relative_to(project_path)
                        large_files.append((relative_path, line_count))
                except Exception:
                    # Skip files we can't read
                    continue

        if large_files:
            # Sort by line count, descending
            large_files.sort(key=lambda x: x[1], reverse=True)

            # Take top 5
            top_files = large_files[:5]

            count = len(large_files)
            file_list = "\n".join(
                f"  • {path} ({lines} lines)"
                for path, lines in top_files
            )

            message = f"{count} files over 400 lines - Claude struggles with large files\n\nLargest files:\n{file_list}"

            if count > 5:
                message += f"\n  ... and {count - 5} more"

            return HealthIssue(
                rule_id=self.rule_id,
                severity=self.severity,
                title=self.title,
                message=message,
                suggestion="Consider breaking down large files. Claude performs better with smaller, focused modules.",
                fix_prompt=self.fix_prompt,
                topic_slug="troubleshooting-slow"
            )

        return None
