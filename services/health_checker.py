"""
Health Checker Service
=======================

Runs health check detectors against Claude Code projects
and generates health reports with scores.
"""

from dataclasses import dataclass, field
from pathlib import Path
from typing import List, Optional
from health_checks.base import BaseDetector, HealthIssue, Severity

# Import detector registry
from health_checks import get_all_detectors


@dataclass
class HealthReport:
    """Report of health check results."""

    project_path: Path
    score: int  # 0-100
    issues: List[HealthIssue] = field(default_factory=list)
    detectors_run: int = 0
    has_critical: bool = False
    has_warnings: bool = False

    def __post_init__(self):
        """Calculate derived fields."""
        self.has_critical = any(
            issue.severity == Severity.CRITICAL for issue in self.issues
        )
        self.has_warnings = any(
            issue.severity == Severity.WARNING for issue in self.issues
        )


class HealthChecker:
    """Runs health checks on Claude Code projects."""

    def __init__(self):
        # Get all registered detectors
        self.detectors: List[BaseDetector] = get_all_detectors()

    def check_project(
        self, project_path: Path, config: Optional[dict] = None
    ) -> HealthReport:
        """
        Run all health checks on a project.

        Args:
            project_path: Root path of the Claude Code project
            config: Optional parsed configuration

        Returns:
            HealthReport with all detected issues and overall score
        """
        if config is None:
            config = {}

        issues = []
        detectors_run = 0

        # Run each detector
        for detector in self.detectors:
            detectors_run += 1
            try:
                issue = detector.check(project_path, config)
                if issue:
                    issues.append(issue)
            except Exception as e:
                # Log error but continue with other checks
                print(f"Error running {detector.rule_id}: {e}")

        # Calculate score
        score = self._calculate_score(issues, detectors_run)

        report = HealthReport(
            project_path=project_path,
            score=score,
            issues=issues,
            detectors_run=detectors_run,
        )

        return report

    def _calculate_score(self, issues: List[HealthIssue], total_checks: int) -> int:
        """
        Calculate health score from 0-100.

        Algorithm:
        - Start at 100
        - Each CRITICAL issue: -20 points
        - Each WARNING issue: -10 points
        - Each INFO issue: -5 points
        - Minimum score: 0

        Args:
            issues: List of detected issues
            total_checks: Total number of checks run

        Returns:
            Score from 0-100
        """
        score = 100

        for issue in issues:
            if issue.severity == Severity.CRITICAL:
                score -= 20
            elif issue.severity == Severity.WARNING:
                score -= 10
            elif issue.severity == Severity.INFO:
                score -= 5

        # Ensure score stays in bounds
        return max(0, min(100, score))

    def get_score_color(self, score: int) -> str:
        """
        Get color code for a health score.

        Args:
            score: Health score from 0-100

        Returns:
            Color string for UI
        """
        if score >= 90:
            return "green"
        elif score >= 70:
            return "yellow"
        elif score >= 50:
            return "orange"
        else:
            return "red"

    def get_score_label(self, score: int) -> str:
        """
        Get text label for a health score.

        Args:
            score: Health score from 0-100

        Returns:
            Label string
        """
        if score >= 90:
            return "Excellent"
        elif score >= 70:
            return "Good"
        elif score >= 50:
            return "Fair"
        else:
            return "Needs Attention"


# Global singleton instance
_health_checker = None


def get_health_checker() -> HealthChecker:
    """Get the global HealthChecker instance."""
    global _health_checker
    if _health_checker is None:
        _health_checker = HealthChecker()
    return _health_checker


if __name__ == "__main__":
    # Test the health checker
    import sys

    if len(sys.argv) > 1:
        test_path = Path(sys.argv[1])
    else:
        # Default to current directory
        test_path = Path.cwd()

    print("=" * 70)
    print("Health Checker Test")
    print("=" * 70)

    checker = get_health_checker()
    report = checker.check_project(test_path)

    print(f"\n📊 Health Report for: {report.project_path}")
    print(f"   Score: {report.score}/100 ({checker.get_score_label(report.score)})")
    print(f"   Detectors run: {report.detectors_run}")
    print(f"   Issues found: {len(report.issues)}")

    if report.issues:
        print("\n🔍 Issues:")
        for issue in report.issues:
            severity_emoji = {
                Severity.CRITICAL: "🔴",
                Severity.WARNING: "🟡",
                Severity.INFO: "🔵",
            }
            print(
                f"\n   {severity_emoji.get(issue.severity, '⚪')} [{issue.severity.value.upper()}] {issue.title}"
            )
            print(f"      {issue.message}")
            if issue.file_path:
                print(f"      File: {issue.file_path}")
    else:
        print("\n✅ No issues found!")

    print("\n" + "=" * 70)
