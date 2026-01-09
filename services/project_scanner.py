"""
Project Scanner Service
========================

Scans Claude Code project directories to detect configuration
and extract project information.
"""

import json
from pathlib import Path
from dataclasses import dataclass
from typing import Optional, Dict, List


@dataclass
class ProjectInfo:
    """Information about a Claude Code project."""

    path: Path
    has_claude_dir: bool
    claude_md_path: Optional[Path] = None
    config_files: List[Path] = None
    parsed_config: Dict = None

    def __post_init__(self):
        if self.config_files is None:
            self.config_files = []
        if self.parsed_config is None:
            self.parsed_config = {}


class ProjectScanner:
    """Scans directories for Claude Code project configuration."""

    def scan_directory(self, directory: Path) -> Optional[ProjectInfo]:
        """
        Scan a directory for Claude Code configuration.

        Args:
            directory: Path to the directory to scan

        Returns:
            ProjectInfo if this appears to be a Claude Code project, None otherwise
        """
        if not directory or not directory.exists() or not directory.is_dir():
            return None

        claude_dir = directory / ".claude"
        has_claude_dir = claude_dir.exists() and claude_dir.is_dir()

        # If no .claude directory, check for root-level CLAUDE.md
        root_claude_md = directory / "CLAUDE.md"
        if not has_claude_dir and not root_claude_md.exists():
            return None

        # Found a Claude Code project
        project_info = ProjectInfo(
            path=directory,
            has_claude_dir=has_claude_dir,
            config_files=[],
            parsed_config={},
        )

        # Check for CLAUDE.md in .claude/ or root
        if has_claude_dir:
            claude_md = claude_dir / "CLAUDE.md"
            if claude_md.exists():
                project_info.claude_md_path = claude_md

        if project_info.claude_md_path is None and root_claude_md.exists():
            project_info.claude_md_path = root_claude_md

        # Scan for other config files
        if has_claude_dir:
            self._scan_config_files(claude_dir, project_info)

        return project_info

    def _scan_config_files(self, claude_dir: Path, project_info: ProjectInfo):
        """
        Scan .claude directory for configuration files.

        Args:
            claude_dir: Path to .claude directory
            project_info: ProjectInfo to populate
        """
        # Common config file names
        config_patterns = [
            "*.json",
            "*.yaml",
            "*.yml",
            "*.md",
        ]

        for pattern in config_patterns:
            for config_file in claude_dir.glob(pattern):
                if config_file.is_file():
                    project_info.config_files.append(config_file)

                    # Try to parse JSON files
                    if config_file.suffix == ".json":
                        try:
                            with open(config_file, "r", encoding="utf-8") as f:
                                data = json.load(f)
                                project_info.parsed_config[config_file.name] = data
                        except Exception:
                            # Skip files that can't be parsed
                            pass


# Global singleton instance
_project_scanner = None


def get_project_scanner() -> ProjectScanner:
    """Get the global ProjectScanner instance."""
    global _project_scanner
    if _project_scanner is None:
        _project_scanner = ProjectScanner()
    return _project_scanner


if __name__ == "__main__":
    # Test the scanner
    import sys

    if len(sys.argv) > 1:
        test_path = Path(sys.argv[1])
    else:
        # Default to current directory
        test_path = Path.cwd()

    print("=" * 70)
    print("Project Scanner Test")
    print("=" * 70)

    scanner = get_project_scanner()
    project = scanner.scan_directory(test_path)

    if project:
        print(f"\n✓ Found Claude Code project at: {project.path}")
        print(f"  Has .claude/ directory: {project.has_claude_dir}")
        print(f"  CLAUDE.md: {project.claude_md_path}")
        print(f"  Config files found: {len(project.config_files)}")
        for cf in project.config_files:
            print(f"    - {cf.name}")
    else:
        print(f"\n✗ Not a Claude Code project: {test_path}")

    print("\n" + "=" * 70)
