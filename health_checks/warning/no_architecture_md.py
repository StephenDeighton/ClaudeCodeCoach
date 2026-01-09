"""
Detector for missing architecture documentation.

architecture.md documents system design and helps Claude understand
the project structure and architectural patterns.
"""

from pathlib import Path
from typing import Optional
from health_checks.base import BaseDetector, HealthIssue, Severity
from health_checks import register


@register
class NoArchitectureMdDetector(BaseDetector):
    """Detects when architecture documentation is missing."""

    rule_id = "no-architecture-md"
    severity = Severity.WARNING
    title = "No architecture documentation found"

    fix_prompt = """My project needs architecture documentation to help Claude understand the system design.

Please create architecture.md with:

1. **System Overview**:
   - What the system does (2-3 sentences)
   - Key components and their roles
   - High-level architecture diagram (ASCII or description)

2. **Architecture Patterns**:
   - MVC, microservices, layered, etc.
   - Why this pattern was chosen
   - How components interact

3. **Tech Stack**:
   - Languages and frameworks
   - Databases and storage
   - External services/APIs
   - Development tools

4. **Key Design Decisions**:
   - Important architectural choices made
   - Trade-offs considered
   - Why alternatives were rejected

5. **Module Organization**:
   - Directory structure explained
   - Where to find different types of code
   - Naming conventions

6. **Data Flow**:
   - How data moves through the system
   - Request/response lifecycle
   - State management approach

This helps Claude make better decisions aligned with your architecture."""

    def check(self, project_path: Path, config: dict) -> Optional[HealthIssue]:
        """
        Check if architecture.md exists.

        Args:
            project_path: Root path of the Claude Code project
            config: Parsed .claude/ configuration (if exists)

        Returns:
            HealthIssue if architecture.md is missing, None otherwise
        """
        architecture_paths = [
            project_path / "architecture.md",
            project_path / "ARCHITECTURE.md",
            project_path / "docs" / "architecture.md",
            project_path / "docs" / "ARCHITECTURE.md"
        ]

        for arch_path in architecture_paths:
            if arch_path.exists():
                return None

        return HealthIssue(
            rule_id=self.rule_id,
            severity=self.severity,
            title=self.title,
            message="No architecture documentation found",
            suggestion="Create architecture.md to document system design. Helps Claude understand project structure.",
            fix_prompt=self.fix_prompt,
            topic_slug="automated-documentation"
        )
