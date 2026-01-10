"""
Project Setup Service

Generates Claude Code configuration files for new projects.
Creates .claude/ directory with settings, CLAUDE.md, and related files
tailored to the detected tech stack.
"""

from pathlib import Path
from dataclasses import dataclass, field
from typing import List, Optional
from datetime import datetime
import json

from services.tech_stack_analyzer import TechStackInfo


@dataclass
class SetupResult:
    """Result of project setup operation"""
    success: bool
    files_created: List[Path] = field(default_factory=list)
    files_updated: List[Path] = field(default_factory=list)
    expected_score: int = 0
    errors: List[str] = field(default_factory=list)


class ProjectSetupService:
    """Generates Claude Code configuration for projects"""

    # CLAUDE.md templates for different tech stacks
    CLAUDE_MD_TEMPLATES = {
        'python': """# {project_name}

## Overview
Python project managed with {package_manager}

## Tech Stack
- Python 3.x
- Package Manager: {package_manager}
- Testing: pytest

## Project Structure
Standard Python layout with source code and tests

## Code Standards
- Follow PEP 8 style guide
- Use type hints where appropriate
- Write docstrings for public functions
- Keep functions focused and testable

## Testing
- Run tests: `pytest`
- Write tests in tests/ directory
- Aim for good coverage of critical paths

## Git Workflow
- Commit after each working feature
- Update status.md with dated entries
- Keep commits atomic and descriptive
- Use conventional commit messages
""",
        'javascript': """# {project_name}

## Overview
JavaScript/Node.js project managed with {package_manager}

## Tech Stack
- Node.js
- Package Manager: {package_manager}
- Build Tools: (add your tools here)

## Project Structure
Standard Node.js layout

## Code Standards
- Follow ESLint configuration
- Use Prettier for formatting
- Write modular, reusable code
- Keep components small and focused

## Testing
- Run tests: `npm test`
- Write tests alongside features
- Test critical user flows

## Git Workflow
- Commit after each working feature
- Update status.md with dated entries
- Keep commits atomic and descriptive
- Use conventional commit messages
""",
        'go': """# {project_name}

## Overview
Go project managed with go modules

## Tech Stack
- Go
- Package Manager: go mod

## Project Structure
Standard Go layout

## Code Standards
- Follow Go conventions and idioms
- Run `go fmt` before committing
- Write clear, self-documenting code
- Use interfaces for flexibility

## Testing
- Run tests: `go test ./...`
- Write table-driven tests
- Aim for thorough coverage

## Git Workflow
- Commit after each working feature
- Update status.md with dated entries
- Keep commits atomic and descriptive
""",
        'rust': """# {project_name}

## Overview
Rust project managed with Cargo

## Tech Stack
- Rust
- Package Manager: cargo

## Project Structure
Standard Cargo project layout

## Code Standards
- Follow Rust conventions
- Run `cargo fmt` before committing
- Fix all clippy warnings
- Use Result/Option properly

## Testing
- Run tests: `cargo test`
- Write unit and integration tests
- Document edge cases

## Git Workflow
- Commit after each working feature
- Update status.md with dated entries
- Keep commits atomic and descriptive
""",
        'generic': """# {project_name}

## Overview
{description}

## Tech Stack
{tech_stack}

## Project Structure
Describe your folder organization here

## Code Standards
- Follow language conventions
- Keep code clean and readable
- Write tests for critical functionality

## Git Workflow
- Commit after each working feature
- Update status.md with dated entries
- Keep commits atomic and descriptive
- Use conventional commit messages
"""
    }

    def setup_project(self, path: Path, tech_info: TechStackInfo, overwrite: bool = False) -> SetupResult:
        """
        Set up Claude Code configuration for a project

        Args:
            path: Project directory path
            tech_info: Detected tech stack info
            overwrite: Whether to overwrite existing files

        Returns:
            SetupResult with created files and expected score
        """
        result = SetupResult(success=False)

        try:
            # Check for existing setup
            has_existing, existing_files = self._check_existing_setup(path)

            if has_existing and not overwrite:
                result.errors.append("Existing setup found. Set overwrite=True to replace.")
                result.files_updated = existing_files
                return result

            # Create .claude directory
            claude_dir = path / ".claude"
            claude_dir.mkdir(exist_ok=True)

            # Create settings.json
            settings_path = self._create_settings_json(claude_dir)
            result.files_created.append(settings_path)
            result.expected_score += 30  # Fixes 3 warnings (model, thinking, hooks)

            # Create CLAUDE.md
            claude_md_path = self._create_claude_md(path, claude_dir, tech_info)
            result.files_created.append(claude_md_path)

            # Update/create .gitignore
            gitignore_path = self._update_gitignore(path, tech_info)
            if gitignore_path:
                if gitignore_path in existing_files:
                    result.files_updated.append(gitignore_path)
                    result.expected_score += 20  # Fixes secrets_exposed
                else:
                    result.files_created.append(gitignore_path)
                    result.expected_score += 40  # Fixes no_gitignore + secrets_exposed

            # Create status.md
            status_md_path = self._create_status_md(path)
            result.files_created.append(status_md_path)
            result.expected_score += 10  # Fixes no_status_md

            # Create .env.example if .env exists
            if tech_info.has_env_file:
                env_example_path = self._create_env_example(path)
                if env_example_path:
                    result.files_created.append(env_example_path)

            # Create essential directories that health checks expect
            skills_dir = claude_dir / "skills"
            skills_dir.mkdir(exist_ok=True)
            result.files_created.append(skills_dir)

            commands_dir = claude_dir / "commands"
            commands_dir.mkdir(exist_ok=True)
            result.files_created.append(commands_dir)

            # Create README.md if it doesn't exist
            readme_path = path / "README.md"
            if not readme_path.exists():
                readme_content = self._create_readme(path, tech_info)
                readme_path.write_text(readme_content)
                result.files_created.append(readme_path)

            result.success = True
            return result

        except Exception as e:
            result.errors.append(f"Setup failed: {str(e)}")
            return result

    def _check_existing_setup(self, path: Path) -> tuple[bool, List[Path]]:
        """
        Check if project has existing Claude Code setup

        Returns:
            (has_setup, existing_files_list)
        """
        existing = []

        claude_dir = path / ".claude"
        if claude_dir.exists():
            existing.append(claude_dir)

        settings_json = claude_dir / "settings.json"
        if settings_json.exists():
            existing.append(settings_json)

        claude_md_paths = [
            claude_dir / "CLAUDE.md",
            path / "CLAUDE.md"
        ]
        for cmd_path in claude_md_paths:
            if cmd_path.exists():
                existing.append(cmd_path)

        return len(existing) > 0, existing

    def _create_settings_json(self, claude_dir: Path) -> Path:
        """Create .claude/settings.json with best practice defaults"""
        settings_path = claude_dir / "settings.json"

        settings = {
            "permissions": {
                "allow": [
                    "Bash",
                    "Read",
                    "Write",
                    "Edit",
                    "Glob",
                    "Grep",
                    "TodoWrite",
                    "Task",
                    "Skill"
                ]
            },
            "env": {
                "ANTHROPIC_MODEL": "sonnet-4.5",
                "MAX_THINKING_TOKENS": "10000"
            },
            "hooks": {
                "SessionStart": [
                    {
                        "type": "command",
                        "command": "echo \"✓ Session started - Ready to code!\"",
                        "blocking": False
                    }
                ]
            }
        }

        with open(settings_path, "w", encoding="utf-8") as f:
            json.dump(settings, f, indent=2)

        return settings_path

    def _create_claude_md(self, project_path: Path, claude_dir: Path, tech_info: TechStackInfo) -> Path:
        """Create CLAUDE.md with tech-specific template"""
        claude_md_path = claude_dir / "CLAUDE.md"

        # Determine template to use
        template_key = tech_info.primary_language if tech_info.primary_language else "generic"
        if template_key not in self.CLAUDE_MD_TEMPLATES:
            template_key = "generic"

        template = self.CLAUDE_MD_TEMPLATES[template_key]

        # Get project name from directory
        project_name = project_path.name

        # Format template variables
        package_manager = tech_info.package_managers[0] if tech_info.package_managers else "unknown"

        if template_key == "generic":
            # For generic template, provide more context
            tech_stack_str = ", ".join(tech_info.languages) if tech_info.languages else "Not detected"
            description = f"Code project with {tech_stack_str}"
            content = template.format(
                project_name=project_name,
                description=description,
                tech_stack=tech_stack_str
            )
        else:
            content = template.format(
                project_name=project_name,
                package_manager=package_manager
            )

        with open(claude_md_path, "w", encoding="utf-8") as f:
            f.write(content)

        return claude_md_path

    def _update_gitignore(self, path: Path, tech_info: TechStackInfo) -> Optional[Path]:
        """Update or create .gitignore with essential patterns"""
        gitignore_path = path / ".gitignore"

        # Patterns to add
        essential_patterns = [
            "# Claude Code local settings",
            ".claude/settings.local.json",
            "",
            "# Environment variables",
            ".env",
            ".env.local",
        ]

        # Add language-specific patterns
        if "python" in tech_info.languages:
            essential_patterns.extend([
                "",
                "# Python",
                "venv/",
                ".venv/",
                "__pycache__/",
                "*.pyc",
                "*.pyo",
                "*.egg-info/",
                ".pytest_cache/",
            ])

        if "javascript" in tech_info.languages:
            essential_patterns.extend([
                "",
                "# Node.js",
                "node_modules/",
                "npm-debug.log",
                "yarn-error.log",
            ])

        if "go" in tech_info.languages:
            essential_patterns.extend([
                "",
                "# Go",
                "bin/",
                "*.exe",
            ])

        if "rust" in tech_info.languages:
            essential_patterns.extend([
                "",
                "# Rust",
                "target/",
                "Cargo.lock",
            ])

        # Check if .gitignore exists
        if gitignore_path.exists():
            # Read existing content
            with open(gitignore_path, "r", encoding="utf-8") as f:
                existing_content = f.read()

            # Only add patterns that don't exist
            patterns_to_add = []
            for pattern in essential_patterns:
                if pattern and not pattern.startswith("#"):
                    # Check if pattern already exists
                    if pattern not in existing_content:
                        patterns_to_add.append(pattern)

            if patterns_to_add:
                # Append new patterns
                with open(gitignore_path, "a", encoding="utf-8") as f:
                    f.write("\n\n# Added by C3 Setup Wizard\n")
                    f.write("\n".join(essential_patterns))
                    f.write("\n")

            return gitignore_path
        else:
            # Create new .gitignore
            with open(gitignore_path, "w", encoding="utf-8") as f:
                f.write("\n".join(essential_patterns))
                f.write("\n")

            return gitignore_path

    def _create_status_md(self, path: Path) -> Path:
        """Create status.md template"""
        status_md_path = path / "status.md"

        today = datetime.now().strftime("%Y-%m-%d")

        content = f"""# Project Status

## {today}

### Setup
- Claude Code configuration created by C3 Setup Wizard

### Next Steps
- Start coding!
- Update this file after each session
- Track completed tasks, in-progress work, and blockers
"""

        with open(status_md_path, "w", encoding="utf-8") as f:
            f.write(content)

        return status_md_path

    def _create_env_example(self, path: Path) -> Optional[Path]:
        """Create .env.example from .env file"""
        env_path = path / ".env"
        env_example_path = path / ".env.example"

        if not env_path.exists():
            return None

        try:
            # Read .env
            with open(env_path, "r", encoding="utf-8") as f:
                env_lines = f.readlines()

            # Create .env.example with placeholder values
            example_lines = []
            for line in env_lines:
                line = line.strip()
                if not line or line.startswith("#"):
                    # Keep comments and empty lines
                    example_lines.append(line)
                elif "=" in line:
                    # Replace value with placeholder
                    key, _ = line.split("=", 1)
                    example_lines.append(f"{key}=your_value_here")
                else:
                    example_lines.append(line)

            # Write .env.example
            with open(env_example_path, "w", encoding="utf-8") as f:
                f.write("\n".join(example_lines))
                f.write("\n")

            return env_example_path

        except Exception:
            # If we can't read .env, skip creating example
            return None

    def _create_readme(self, path: Path, tech_info: TechStackInfo) -> str:
        """Create README.md template based on tech stack"""
        project_name = path.name

        # Determine primary language for instructions
        lang = tech_info.primary_language or "your language"

        # Build tech stack list
        tech_list = []
        if tech_info.languages:
            tech_list.extend(f"- {l.title()}" for l in tech_info.languages)
        if tech_info.package_managers:
            tech_list.extend(f"- {pm}" for pm in tech_info.package_managers)

        tech_stack_section = "\n".join(tech_list) if tech_list else "- Add your tech stack here"

        content = f"""# {project_name}

## Overview

Add a brief description of your project here.

## Tech Stack

{tech_stack_section}

## Getting Started

### Prerequisites

- Python 3.12+ / Node.js 18+ / etc. (update based on your stack)
- Required dependencies (see installation)

### Installation

```bash
# Add your installation commands
# e.g., npm install, pip install -r requirements.txt, etc.
```

### Running

```bash
# Add your run commands
# e.g., npm start, python main.py, cargo run, etc.
```

## Development

- Follow the patterns in `.claude/CLAUDE.md`
- Update `status.md` after each session
- Run tests before committing

## Testing

```bash
# Add your test commands
# e.g., npm test, pytest, cargo test, etc.
```

## Contributing

1. Follow existing code patterns
2. Write tests for new features
3. Update documentation
4. Use conventional commit messages

## License

[Add your license here]
"""

        return content


# Singleton instance
_project_setup_service = None


def get_project_setup_service() -> ProjectSetupService:
    """Get singleton instance of ProjectSetupService"""
    global _project_setup_service
    if _project_setup_service is None:
        _project_setup_service = ProjectSetupService()
    return _project_setup_service
