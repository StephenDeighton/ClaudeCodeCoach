"""
Status Updater Service

Automatically updates status.md files with scan results and setup events.
Maintains a record of C3 activities in each project.
"""

from pathlib import Path
from datetime import datetime
from services.tech_stack_analyzer import TechStackInfo
from services.project_setup_service import SetupResult


class StatusUpdater:
    """Appends scan results and setup events to status.md"""

    def append_scan_result(self, project_path: Path, score: int, issues_count: int) -> None:
        """
        Append health scan result to status.md

        Args:
            project_path: Path to the project directory
            score: Health score (0-100)
            issues_count: Number of issues found
        """
        status_file = self._ensure_status_file(project_path)
        today = datetime.now().strftime("%Y-%m-%d")

        # Determine score label
        if score >= 80:
            label = "Excellent"
        elif score >= 60:
            label = "Good"
        elif score >= 40:
            label = "Fair"
        else:
            label = "Needs Attention"

        entry = f"\n## {today}\n- Health scan: {score}/100 ({label}) - {issues_count} issues found\n"

        try:
            # Check if today's section already exists
            with open(status_file, "r", encoding="utf-8") as f:
                content = f.read()

            # If today's section exists, append to it; otherwise create new section
            if f"## {today}" in content:
                # Replace today's section to update with latest scan
                lines = content.split("\n")
                new_lines = []
                skip_until_next_section = False

                for i, line in enumerate(lines):
                    if line == f"## {today}":
                        new_lines.append(line)
                        new_lines.append(f"- Health scan: {score}/100 ({label}) - {issues_count} issues found")
                        skip_until_next_section = True
                    elif skip_until_next_section and line.startswith("## "):
                        skip_until_next_section = False
                        new_lines.append(line)
                    elif not skip_until_next_section:
                        new_lines.append(line)

                with open(status_file, "w", encoding="utf-8") as f:
                    f.write("\n".join(new_lines))
            else:
                # Append new section
                with open(status_file, "a", encoding="utf-8") as f:
                    f.write(entry)

        except Exception as e:
            # If append fails, log but don't crash
            print(f"Failed to update status.md: {e}")

    def append_setup_event(self, project_path: Path, tech_info: TechStackInfo, result: SetupResult) -> None:
        """
        Append wizard setup completion to status.md

        Args:
            project_path: Path to the project directory
            tech_info: Detected tech stack info
            result: Setup result with created files
        """
        status_file = self._ensure_status_file(project_path)
        today = datetime.now().strftime("%Y-%m-%d")

        # Format tech stack
        tech_stack = ", ".join(tech_info.languages) if tech_info.languages else "Unknown"

        # Count files
        files_created = len(result.files_created)
        files_updated = len(result.files_updated)

        entry_lines = [
            f"\n## {today}",
            "### CC Setup Wizard Completed",
            f"- Tech stack detected: {tech_stack}",
            f"- Files created: {files_created}",
        ]

        if files_updated > 0:
            entry_lines.append(f"- Files updated: {files_updated}")

        entry_lines.append(f"- Expected health score: {result.expected_score}/100")
        entry_lines.append("")

        entry = "\n".join(entry_lines)

        try:
            with open(status_file, "a", encoding="utf-8") as f:
                f.write(entry)
        except Exception as e:
            print(f"Failed to update status.md: {e}")

    def _ensure_status_file(self, project_path: Path) -> Path:
        """
        Ensure status.md exists, create if missing

        Args:
            project_path: Path to the project directory

        Returns:
            Path to status.md
        """
        status_file = project_path / "status.md"

        if not status_file.exists():
            # Create basic status.md
            with open(status_file, "w", encoding="utf-8") as f:
                f.write("# Project Status\n\n")

        return status_file


# Singleton instance
_status_updater = None


def get_status_updater() -> StatusUpdater:
    """Get singleton instance of StatusUpdater"""
    global _status_updater
    if _status_updater is None:
        _status_updater = StatusUpdater()
    return _status_updater
