"""
Detector for missing .env.example template.

When .env exists but .env.example doesn't, team members won't know
what environment variables are required for the project.
"""

from pathlib import Path
from typing import Optional
from health_checks.base import BaseDetector, HealthIssue, Severity
from health_checks import register


@register
class MissingEnvExampleDetector(BaseDetector):
    """Detects when .env exists but .env.example doesn't."""

    rule_id = "missing-env-example"
    severity = Severity.INFO
    title = ".env exists but no .env.example template"

    fix_prompt = """My project has a .env file but no .env.example template for team members.

Please create .env.example based on my .env structure:

1. **Read my .env file** to see what variables are defined
2. **Create .env.example** with the same structure but:
   - Replace actual values with placeholders
   - Add comments explaining what each variable is for
   - Include example formats where helpful

Example:
```
# API Configuration
ANTHROPIC_API_KEY=your_api_key_here
DATABASE_URL=postgresql://user:password@localhost:5432/dbname

# Feature Flags
ENABLE_ANALYTICS=false
```

3. **Update README.md** to mention:
   - Copy .env.example to .env
   - Fill in your actual values
   - Never commit .env

4. **Verify .env is in .gitignore**

This helps team members and Claude understand required configuration."""

    def check(self, project_path: Path, config: dict) -> Optional[HealthIssue]:
        """
        Check if .env exists without .env.example.

        Args:
            project_path: Root path of the Claude Code project
            config: Parsed .claude/ configuration (if exists)

        Returns:
            HealthIssue if .env.example is missing, None otherwise
        """
        env_path = project_path / ".env"
        env_example_path = project_path / ".env.example"

        if env_path.exists() and not env_example_path.exists():
            return HealthIssue(
                rule_id=self.rule_id,
                severity=self.severity,
                title=self.title,
                message=".env exists but no .env.example template",
                suggestion="Create .env.example (without real values) so team knows required environment variables",
                fix_prompt=self.fix_prompt,
                topic_slug="credential-management"
            )

        return None
