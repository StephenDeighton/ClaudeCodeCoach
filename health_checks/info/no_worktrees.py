"""
Detector for missing worktrees setup.

Git worktrees enable running multiple Claude Code instances in parallel,
each working on a different branch in a separate directory.
"""

from pathlib import Path
from typing import Optional
from health_checks.base import BaseDetector, HealthIssue, Severity
from health_checks import register


@register
class NoWorktreesDetector(BaseDetector):
    """Detects when git worktrees are not configured."""

    rule_id = "no-worktrees-setup"
    severity = Severity.INFO
    title = "Not configured for git worktrees"

    fix_prompt = """My project could benefit from git worktrees for running parallel Claude Code instances.

Please set up worktrees support:

1. **Add .trees/ to .gitignore**:
   ```
   # Git worktrees for parallel Claude instances
   .trees/
   ```

2. **What worktrees enable**:
   - Run multiple Claude Code sessions in parallel
   - Each session works on a different branch
   - Separate working directories for each branch
   - No branch switching in main repo

3. **Usage example**:
   ```bash
   # Create worktree for feature branch
   git worktree add .trees/feature-x feature-x

   # Start Claude in that worktree
   cd .trees/feature-x
   claude-code

   # Work continues in parallel
   ```

4. **Benefits**:
   - Work on multiple features simultaneously
   - No context switching between branches
   - Isolated environments per feature
   - Safe experimentation

5. **Update CLAUDE.md** with worktree workflow if team uses this pattern

Git worktrees are powerful for parallel development workflows."""

    def check(self, project_path: Path, config: dict) -> Optional[HealthIssue]:
        """
        Check if .trees/ directory exists and is in .gitignore.

        Args:
            project_path: Root path of the Claude Code project
            config: Parsed .claude/ configuration (if exists)

        Returns:
            HealthIssue if worktrees not set up, None otherwise
        """
        trees_path = project_path / ".trees"
        gitignore_path = project_path / ".gitignore"

        # If .trees exists, we assume worktrees are set up
        if trees_path.exists():
            return None

        # If .trees is already in .gitignore, we assume it's set up
        if gitignore_path.exists():
            try:
                with open(gitignore_path, "r", encoding="utf-8") as f:
                    content = f.read()
                    if ".trees" in content:
                        return None
            except Exception:
                pass

        return HealthIssue(
            rule_id=self.rule_id,
            severity=self.severity,
            title=self.title,
            message="Not configured for git worktrees",
            suggestion="Add .trees/ to .gitignore to enable parallel Claude instances via git worktrees",
            fix_prompt=self.fix_prompt,
            topic_slug="git-worktrees"
        )
