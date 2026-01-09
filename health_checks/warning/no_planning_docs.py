"""
Detector for missing planning documents.

Planning documents like PRD.md, EDD.md, or plan.md help Claude understand
project requirements and make better implementation decisions.
"""

from pathlib import Path
from typing import Optional
from health_checks.base import BaseDetector, HealthIssue, Severity
from health_checks import register


@register
class NoPlanningDocsDetector(BaseDetector):
    """Detects when planning documents are missing."""

    rule_id = "no-planning-docs"
    severity = Severity.WARNING
    title = "No planning documents found"

    fix_prompt = """My project needs planning documents to guide development and help Claude make better decisions.

Please create appropriate planning documentation:

1. **Create PRD.md** (Product Requirements Document):
   ```markdown
   # Product Requirements Document

   ## Overview
   Brief description of what we're building and why

   ## Goals
   - Primary goal 1
   - Primary goal 2

   ## User Stories
   - As a [user type], I want [feature] so that [benefit]

   ## Requirements
   ### Functional Requirements
   - Must have feature X
   - Should support Y

   ### Non-Functional Requirements
   - Performance: Response time < 200ms
   - Security: Authentication required
   - Scalability: Support 10k concurrent users

   ## Out of Scope
   - Features we explicitly won't build

   ## Success Criteria
   How we'll measure success
   ```

2. **Or create plan.md** for implementation planning:
   - Technical approach
   - Architecture decisions
   - Implementation phases
   - Dependencies and risks

3. **Benefits of planning docs**:
   - Claude understands requirements deeply
   - Makes implementation decisions aligned with goals
   - Prevents scope creep
   - Documents "why" behind decisions

4. **Update regularly** as requirements evolve"""

    def check(self, project_path: Path, config: dict) -> Optional[HealthIssue]:
        """
        Check if any planning documents exist.

        Args:
            project_path: Root path of the Claude Code project
            config: Parsed .claude/ configuration (if exists)

        Returns:
            HealthIssue if no planning documents found, None otherwise
        """
        planning_paths = [
            project_path / "PRD.md",
            project_path / "EDD.md",
            project_path / "plan.md",
            project_path / "PLAN.md",
            project_path / "docs" / "PRD.md",
            project_path / "docs" / "plan.md"
        ]

        for planning_path in planning_paths:
            if planning_path.exists():
                return None

        return HealthIssue(
            rule_id=self.rule_id,
            severity=self.severity,
            title=self.title,
            message="No planning documents found",
            suggestion="Create PRD.md (requirements) or plan.md to guide development. Claude makes better decisions with clear specs.",
            fix_prompt=self.fix_prompt,
            topic_slug="psb-planning-phase"
        )
