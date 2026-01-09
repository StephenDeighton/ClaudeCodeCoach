"""
Pytest configuration and shared fixtures for C3 tests.
"""

import pytest
from pathlib import Path
import tempfile
import shutil


@pytest.fixture
def temp_project_dir():
    """Create a temporary directory for test projects."""
    temp_dir = tempfile.mkdtemp()
    yield Path(temp_dir)
    shutil.rmtree(temp_dir)


@pytest.fixture
def mock_claude_project(temp_project_dir):
    """Create a mock Claude Code project structure."""
    # Create .claude directory
    claude_dir = temp_project_dir / ".claude"
    claude_dir.mkdir()

    # Create basic CLAUDE.md
    (claude_dir / "CLAUDE.md").write_text("# Test Project\n")

    # Create settings.json
    (claude_dir / "settings.json").write_text('{"permissions": {"allow": []}}')

    # Create .gitignore
    (temp_project_dir / ".gitignore").write_text("*.pyc\n__pycache__/\n")

    return temp_project_dir


@pytest.fixture
def mock_config():
    """Mock Claude Code configuration."""
    return {
        "permissions": {
            "allow": ["Bash", "Read", "Write"],
            "deny": []
        },
        "env": {
            "ANTHROPIC_MODEL": "sonnet-4.5"
        }
    }
